# AutoMake Specifications

## 1. Project Overview
AutoMake is a Python-based, agent-first command-line tool. It uses a sophisticated multi-agent system, built on the `smolagents` framework, to interpret and execute a wide range of natural language commands. The user can interact with a Manager Agent that orchestrates a team of specialists to perform tasks like running `Makefile` targets, executing terminal commands, writing code, and searching the web. This design transforms AutoMake from a simple `Makefile` wrapper into a powerful, general-purpose AI assistant for the command line. The initial implementation is now complete, delivering the core features outlined in the specification library.

## 2. Specification Library
The following table links to the detailed specifications for each domain and technical topic.

| Filename                                             | Description                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| `specs/01-core-functionality.md`                     | Defines the agent-first architecture where a Manager Agent orchestrates all tasks. |
| `specs/02-cli-and-ux.md`                             | Outlines the `automake` CLI, focusing on the agent as the primary command entry point. |
| `specs/03-architecture-and-tech-stack.md`            | Specifies the overall architecture, technology choices, and development standards. |
| `specs/04-configuration-management.md`               | Details the `config.toml` file for user-specific settings like the Ollama model. |
| `specs/05-ai-prompting.md`                           | Defines the precise prompt templates for reliable LLM-based command interpretation. |
| `specs/06-logging-strategy.md`                       | Outlines the PID-based, file-logging approach with startup-based cleanup for concurrent session support. |
| `specs/07-packaging-and-distribution.md`             | Details the `pyproject.toml` setup for `uvx` installation and distribution. |
| `specs/08-cicd-pipeline.md`                          | Defines the GitHub Actions CI pipeline for automated testing and coverage reporting. |
| `specs/09-model-context-protocol.md`                 | Describes the integration with Anthropic's Model Context Protocol (MCP) for autonomous use by LLMs. |
| `specs/10-interactive-sessions.md`                   | Specifies the interactive session for resolving ambiguous commands based on LLM confidence scores. |
| `specs/11-live-output-component.md`                  | Defines a real-time, updatable box for streaming content like AI model tokens. |
| `specs/12-autonomous-agent-mode.md`                  | Specifies a multi-agent architecture for autonomous, interactive task execution. |
| `specs/14-agent-interaction-scaffolding.md`          | Defines a standardized scaffolding and ABC for managing interactive agent sessions. |
| `specs/15-rag-agent.md`                              | A high-level sketch for a RAG agent to provide project-aware Q&A. (Deprioritized in favor of Codebase Exploration Agent) |
| `specs/16-project-init-agent.md`                     | A high-level sketch for an agent that can scaffold new projects. |
| `specs/17-codebase-exploration-agent.md`             | Defines a coding agent that uses dynamic codebase exploration instead of RAG. |
| `specs/18-concurrent-sessions.md` | Defines the process-isolated logging mechanism to enable multiple, simultaneous agent sessions. |
| `specs/19-hardware-aware-model-recommendation.md`    | Specifies an interactive, hardware-aware model recommender for `automake init`. |
| `specs/20-signal-handling.md`                        | Defines graceful shutdown procedures for `Ctrl+C` and `Ctrl+D`. |
| `specs/21-automake-agent.md`                         | Defines a specialist agent for interpreting `automake`'s own commands. |
| `specs/22-mermaid-agent.md`                          | Defines a specialist agent for generating Mermaid diagrams from source code. |
| `specs/23-animated-text-display.md`                  | Specifies a typewriter-style animation for all `rich` box outputs. |

## 3. Implementation Summaries
- **Phase 2**: [Concurrent Session Support](./docs/PHASE2_IMPLEMENTATION_SUMMARY.md)
- **Phase 4**: [Non-Interactive Agent Mode](./docs/PHASE4_IMPLEMENTATION_SUMMARY.md)

## 4. Future Work
This section captures features and ideas that are currently out of scope but are being considered for future versions:
- **Simplified Command Invocation**: Make `run` the default subcommand, allowing users to execute commands directly (e.g., `automake "build the project"` instead of `automake run "build the project"`).
- **GitAgent**: A specialist agent for intelligent, repository-aware source control operations (e.g., summarizing branch changes, structured status reports).
- **Dry-Run Mode**: Add a flag (e.g., `--dry-run`) to display the interpreted command without executing it.
- **Failure Detection**: Implement logic to detect when the LLM fails to return a valid command or when the executed command fails.
- **Makefile Generation**: Add a new command, `automake makefile`, that intelligently scans the repository for DevOps patterns (e.g., `Dockerfile`, CI scripts) and generates a comprehensive `Makefile` using the configured LLM.
- **Multi-Provider LLM Support**: Extend `automake init` to support configuring major LLM providers like OpenAI and Anthropic via API keys, in addition to the default Ollama integration.

## 5. Implementation Plan
This plan outlines the steps to implement the agent-first architecture for AutoMake.

| Phase | Focus Area                  | Key Deliverables                                                                                                                                                             | Related Specs                                                                                               | Status |
| ----- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------ |
| 1     | Foundational Agent Setup    | - Implement the core `ManagerAgent` and specialist `ManagedAgent` instances.<br>- Create the `FileSystemAgent` and `CodingAgent` with `uv`-based sandboxing.<br>- Refactor the main CLI entry point to invoke the `ManagerAgent`. | `specs/01-core-functionality.md`<br>`specs/12-autonomous-agent-mode.md`                                    | ✅ Done    |
| 2     | Concurrent Session Support  | - Implement PID-based unique log filenames.<br>- Replace timed rotation with a startup-based cleanup mechanism for old log files.                                           | `specs/06-logging-strategy.md`<br>`specs/18-concurrent-sessions.md`                                        | ✅ Done   |
| 3     | Agent Scaffolding           | - Implement the `InteractiveSession` ABC and the `RichInteractiveSession` concrete class for managing the chat UI.                                                             | `specs/14-agent-interaction-scaffolding.md`                                                                 | ✅ Done    |
| 4     | Non-Interactive Agent Mode  | - Implement the `automake "<prompt>"` flow.<br>- Ensure agent output is streamed correctly to the terminal using the `LiveBox` component.                                      | `specs/02-cli-and-ux.md`<br>`specs/11-live-output-component.md`                                            | ✅ Done    |
| 5     | Interactive Agent Mode      | - Implement the `automake agent` command to launch the `rich`-based interactive chat UI, using the new `RichInteractiveSession`.                                               | `specs/02-cli-and-ux.md`<br>`specs/12-autonomous-agent-mode.md`                                            | ✅ Done    |
| 6     | Intelligent Error Handling  | - Implement the `try/except` wrapper around the CLI to capture errors.<br>- Create the agent prompt for suggesting corrections and implement the user confirmation flow.       | `specs/01-core-functionality.md`                                                                            | ✅ Done    |
| 7     | Action Confirmation         | - Add `agent.require_confirmation` to config.<br>- Implement the `get_confirmation` UI component in the `RichInteractiveSession`.<br>- Integrate the confirmation check before executing agent actions. | `specs/04-configuration-management.md`<br>`specs/14-agent-interaction-scaffolding.md`                      | ✅ Done    |
| 8     | Interactive Model Config    | - Implement `automake config model` command.<br>- Build the `rich`-based UI to list local Ollama models.<br>- Add online search and selection functionality.                   | `specs/04-configuration-management.md`<br>`specs/02-cli-and-ux.md`                                         | ✅ Done    |
| 9     | Animated Text Display       | - Create a utility function for typewriter-style text animation in `rich` boxes.<br>- Refactor existing UI components to use the new animation utility.<br>- Add a configuration option to enable/disable the animation. | `specs/23-animated-text-display.md`                                                                       | ✅ Done    |
| 10    | Documentation Overhaul      | - Update `README.md` and all specifications to reflect the agent-first architecture.<br>- Create a comprehensive user guide for the new agent capabilities.                      | `README.md`<br>All `specs/*.md` files                                                                       | TBD    |
| 11    | Codebase Exploration Agent  | - Implement the `CodebaseExplorationAgent` with tools for dynamic file system and code analysis.<br>- Develop tools for AST parsing and dependency tracing.             | `specs/17-codebase-exploration-agent.md`                                                                    | TBD    |
| 12    | Project Init Agent          | - Implement the `
| 13    | Robust Signal Handling      | - Implement a global signal handler for `SIGINT` (Ctrl+C).<br>- Ensure graceful shutdown of agent processes.<br>- Handle `EOFError` (Ctrl+D) in interactive sessions to exit cleanly.<br>- Prevent zombie processes on abrupt termination. | `specs/20-signal-handling.md`                                                                               | TBD    |
| 14    | AutoMake Agent              | - Implement the `AutoMakeAgent` with context from `automake --help`.<br>- Update `ManagerAgent` to route `automake`-specific commands. | `specs/21-automake-agent.md`<br>`specs/12-autonomous-agent-mode.md`                                        | TBD    |
| 15    | Mermaid Agent               | - Implement the `MermaidAgent` with tools to read files and write `.mmd` files.<br>- Update `ManagerAgent` to recognize and delegate diagramming tasks. | `specs/22-mermaid-agent.md`<br>`specs/12-autonomous-agent-mode.md`                                        | TBD    |
