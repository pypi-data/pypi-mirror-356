"""AI Agent module for AutoMake.

This module implements the smolagent responsible for interpreting natural language
commands and translating them into Makefile targets using Ollama LLM.
"""

import builtins
import io
import json
import logging
import warnings
from contextlib import contextmanager, redirect_stderr, redirect_stdout

import ollama
from smolagents import CodeAgent, LiteLLMModel

from ..config import Config
from ..utils.ollama_manager import OllamaManagerError, ensure_ollama_running
from .makefile_reader import MakefileReader

# Suppress Pydantic serialization warnings from LiteLLM
warnings.filterwarnings(
    "ignore",
    message=".*PydanticSerializationUnexpectedValue.*",
    category=UserWarning,
    module="pydantic.*",
)

# Also suppress the broader Pydantic serializer warnings
warnings.filterwarnings(
    "ignore",
    message=".*Pydantic serializer warnings.*",
    category=UserWarning,
)

logger = logging.getLogger(__name__)


@contextmanager
def suppress_agent_output():
    """Context manager to completely suppress all output from the agent."""
    # Capture both stdout and stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Also suppress print statements
    original_print = builtins.print

    def silent_print(*args, **kwargs):
        pass

    builtins.print = silent_print

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            yield
    finally:
        builtins.print = original_print


class CommandInterpretationError(Exception):
    """Raised when there's an error interpreting the command."""

    pass


class CommandResponse:
    """Represents the response from the AI agent for command interpretation."""

    def __init__(
        self,
        reasoning: str,
        command: str | None,
        alternatives: list[str],
        confidence: int,
    ):
        """Initialize the command response.

        Args:
            reasoning: Brief explanation of why the command was chosen
            command: The most appropriate make target (None if no suitable command
                found)
            alternatives: List of alternative commands that could be relevant
            confidence: Confidence level (0-100) in the chosen command
        """
        self.reasoning = reasoning
        self.command = command
        self.alternatives = alternatives
        self.confidence = confidence

    @classmethod
    def from_json(cls, json_str: str) -> "CommandResponse":
        """Parse a CommandResponse from JSON string.

        Args:
            json_str: JSON string containing the response data

        Returns:
            CommandResponse instance

        Raises:
            CommandInterpretationError: If JSON parsing fails or required fields
                are missing
        """
        try:
            # Handle JSON wrapped in markdown code blocks
            if "```json" in json_str:
                start = json_str.find("```json") + 7
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()
            elif "```" in json_str:
                start = json_str.find("```") + 3
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()

            data = json.loads(json_str)

            # Validate required fields
            required_fields = ["reasoning", "command", "alternatives", "confidence"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise CommandInterpretationError(
                    f"Missing required fields: {missing_fields}"
                )

            # Validate types and values
            if not isinstance(data["reasoning"], str):
                raise CommandInterpretationError("'reasoning' must be a string")
            if data["command"] is not None and not isinstance(data["command"], str):
                raise CommandInterpretationError("'command' must be a string or null")
            if not isinstance(data["alternatives"], list):
                raise CommandInterpretationError("'alternatives' must be a list")
            if not all(isinstance(alt, str) for alt in data["alternatives"]):
                raise CommandInterpretationError(
                    "All items in 'alternatives' must be strings"
                )

            # Handle confidence as string or int
            if isinstance(data["confidence"], str):
                try:
                    data["confidence"] = int(data["confidence"])
                except ValueError as e:
                    raise CommandInterpretationError(
                        "'confidence' must be an integer"
                    ) from e
            elif not isinstance(data["confidence"], int):
                raise CommandInterpretationError("'confidence' must be an integer")

            if not 0 <= data["confidence"] <= 100:
                raise CommandInterpretationError(
                    "'confidence' must be between 0 and 100"
                )

            # Validate business logic
            if data["command"] is None and data["confidence"] != 0:
                raise CommandInterpretationError(
                    "If 'command' is null, 'confidence' must be 0"
                )

            return cls(
                reasoning=data["reasoning"],
                command=data["command"],
                alternatives=data["alternatives"] or [],
                confidence=data["confidence"],
            )

        except json.JSONDecodeError as e:
            # Include the actual response content for debugging
            truncated_response = (
                json_str[:500] + "..." if len(json_str) > 500 else json_str
            )
            raise CommandInterpretationError(
                f"Invalid JSON response: {e}\n\n"
                f"Actual response received:\n{truncated_response}"
            ) from e
        except (KeyError, TypeError) as e:
            # Include the actual response content for debugging
            truncated_response = (
                json_str[:500] + "..." if len(json_str) > 500 else json_str
            )
            raise CommandInterpretationError(
                f"Invalid response format: {e}\n\n"
                f"Actual response received:\n{truncated_response}"
            ) from e


class MakefileCommandAgent:
    """AI agent for interpreting natural language commands into Makefile targets."""

    def __init__(self, config: Config):
        """Initialize the AI agent.

        Args:
            config: Configuration object containing Ollama settings

        Raises:
            CommandInterpretationError: If agent initialization fails
        """
        self.config = config
        try:
            # Create LiteLLM model for Ollama
            model_name = f"ollama/{config.ollama_model}"
            self.model = LiteLLMModel(
                model_id=model_name,
                api_base=config.ollama_base_url,
            )

            # Initialize the CodeAgent with minimal tools
            self.agent = CodeAgent(
                tools=[],  # No tools needed for our use case
                model=self.model,
                max_steps=3,  # Allow a few steps for command interpretation
                additional_authorized_imports=["json"],  # Allow json import
            )

            logger.info("AI agent initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize AI agent: %s", e)
            raise CommandInterpretationError(
                f"Failed to initialize AI agent: {e}"
            ) from e

    def interpret_command(
        self, user_command: str, makefile_reader: MakefileReader
    ) -> CommandResponse:
        """Interpret a natural language command into a Makefile target.

        Args:
            user_command: The natural language command from the user
            makefile_reader: MakefileReader instance with target information

        Returns:
            CommandResponse with the interpretation results

        Raises:
            CommandInterpretationError: If command interpretation fails
        """
        try:
            # Get targets with descriptions
            targets_with_descriptions = makefile_reader.targets_with_descriptions

            # Log debug information about targets and descriptions
            logger.debug(
                "Processing %d targets for command interpretation",
                len(targets_with_descriptions),
            )

            targets_with_desc_count = sum(
                1 for desc in targets_with_descriptions.values() if desc
            )
            logger.debug(
                "Found %d targets with descriptions, %d without descriptions",
                targets_with_desc_count,
                len(targets_with_descriptions) - targets_with_desc_count,
            )

            # Create the prompt for command interpretation
            prompt = self._create_interpretation_prompt(
                user_command, targets_with_descriptions
            )

            # Use the agent to interpret the command with selective output suppression
            with suppress_agent_output():
                result = self.agent.run(prompt)

            # Parse the result as JSON
            response = CommandResponse.from_json(str(result))

            logger.info(
                "Command interpreted: %s -> %s (confidence: %d%%)",
                user_command,
                response.command,
                response.confidence,
            )

            return response

        except CommandInterpretationError:
            # Re-raise CommandInterpretationError as-is (it already has debugging info)
            raise
        except Exception as e:
            logger.error("Failed to interpret command '%s': %s", user_command, e)
            # Try to include the raw AI response if available
            try:
                raw_response = (
                    str(result) if "result" in locals() else "No response captured"
                )
                truncated_response = (
                    raw_response[:500] + "..."
                    if len(raw_response) > 500
                    else raw_response
                )
                raise CommandInterpretationError(
                    f"Failed to interpret command: {e}\n\n"
                    f"Raw AI response:\n{truncated_response}"
                ) from e
            except Exception:  # noqa: BLE001
                # Fallback if we can't access the result
                raise CommandInterpretationError(
                    f"Failed to interpret command: {e}"
                ) from e

    def _create_interpretation_prompt(
        self, user_command: str, targets_with_descriptions: dict[str, str]
    ) -> str:
        """Create the prompt for command interpretation.

        Args:
            user_command: The user's natural language command
            targets_with_descriptions: Dictionary mapping target names to descriptions

        Returns:
            Formatted prompt string
        """
        # Create targets list with descriptions when available
        targets_list_parts = []
        for target, description in targets_with_descriptions.items():
            if description:
                targets_list_parts.append(f"- {target}: {description}")
            else:
                targets_list_parts.append(f"- {target}")

        targets_list = "\n".join(targets_list_parts)

        # Log the enhanced prompt information in debug mode
        logger.debug(
            "Created prompt with %d targets for command: %s",
            len(targets_with_descriptions),
            user_command,
        )

        return f"""You are an AI assistant that interprets natural language commands and maps them to Makefile targets.

Given the user command: "{user_command}"

Available Makefile targets (with descriptions where available):
{targets_list}

Your task is to analyze the user command and write Python code that returns a JSON response using the final_answer() function.

IMPORTANT: You must write Python code in a code block starting with ```py

The JSON response should have this structure:
{{
    "reasoning": "Brief explanation of why this command was chosen",
    "command": "most_appropriate_target_name_or_null",
    "alternatives": ["list", "of", "alternative", "targets"],
    "confidence": 85
}}

Rules:
1. If no suitable target exists, set "command" to null
2. Confidence should be 0-100 (0 = no match, 100 = perfect match)
3. Include 2-3 alternatives even if confidence is high
4. Consider semantic similarity, not just exact matches
5. Use the target descriptions to better understand what each target does
6. Use final_answer() to return the JSON string

You must follow this exact format:

```py
import json

# Analyze the command and targets
response = {{
    "reasoning": "Your reasoning here",
    "command": "target_name_or_null",
    "alternatives": ["alt1", "alt2"],
    "confidence": 85
}}

# Return the JSON response
final_answer(json.dumps(response))
```

Now analyze the command and provide your Python code:"""  # noqa: E501


def create_ai_agent(config: Config) -> tuple[MakefileCommandAgent, bool]:
    """Create and initialize an AI agent.

    Args:
        config: Configuration object

    Returns:
        Tuple of (initialized MakefileCommandAgent, was_ollama_started_automatically)

    Raises:
        CommandInterpretationError: If agent creation fails
    """
    try:
        # Ensure Ollama is running, starting it automatically if needed
        try:
            is_running, was_started = ensure_ollama_running(config)
        except OllamaManagerError as e:
            raise CommandInterpretationError(f"Failed to start Ollama: {e}") from e

        # Verify Ollama connection and model availability
        client = ollama.Client(host=config.ollama_base_url)
        models_response = client.list()

        # Extract model names from the response
        available_models = []
        if hasattr(models_response, "models"):
            # New ollama client API - models_response is a ListResponse object
            for model in models_response.models:
                if hasattr(model, "model"):
                    available_models.append(model.model)
                elif hasattr(model, "name"):
                    available_models.append(model.name)
        elif isinstance(models_response, dict) and "models" in models_response:
            # Legacy API - models_response is a dictionary
            model_list = models_response["models"]
            for model in model_list:
                if isinstance(model, dict):
                    model_name = (
                        model.get("name") or model.get("model") or model.get("id")
                    )
                    if model_name:
                        available_models.append(model_name)
                elif isinstance(model, str):
                    available_models.append(model)
        else:
            # Fallback for other response types
            model_list = models_response
            for model in model_list:
                if isinstance(model, dict):
                    model_name = (
                        model.get("name") or model.get("model") or model.get("id")
                    )
                    if model_name:
                        available_models.append(model_name)
                elif isinstance(model, str):
                    available_models.append(model)

        if config.ollama_model not in available_models:
            raise CommandInterpretationError(
                f"Model '{config.ollama_model}' not found. "
                f"Available models: {available_models}"
            )

        logger.info(
            "Ollama connection verified, model '%s' is available", config.ollama_model
        )

        return MakefileCommandAgent(config), was_started

    except Exception as e:
        if "ollama" in str(type(e)).lower() or "response" in str(type(e)).lower():
            logger.error("Failed to connect to Ollama: %s", e)
            raise CommandInterpretationError(f"Failed to connect to Ollama: {e}") from e
        else:
            logger.error("Unexpected error creating AI agent: %s", e)
            raise CommandInterpretationError(f"Failed to create AI agent: {e}") from e
