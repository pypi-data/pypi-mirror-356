"""Output types and enums for AutoMake.

This module will contain MessageType enum and other output-related types
moved from automake/utils/output.py during Phase 2 of the migration.
"""

# TODO: Move MessageType enum from automake/utils/output.py
# TODO: Move any other output-related type definitions
# TODO: Update imports in automake/utils/output/__init__.py

from enum import Enum


class MessageType(Enum):
    """Types of messages that can be displayed."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    HINT = "hint"
