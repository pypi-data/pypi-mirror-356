"""Patch operations for AgenticScrum framework updates.

This module contains all the specific patch operations that can be performed
on the AgenticScrum framework, including template updates, MCP services,
CLI fixes, and more.
"""

from .add_template import AddTemplateOperation
from .update_mcp import UpdateMCPOperation
from .fix_cli import FixCLIOperation
from .add_command import AddCommandOperation
from .sync_changes import SyncChangesOperation

__all__ = [
    'AddTemplateOperation',
    'UpdateMCPOperation', 
    'FixCLIOperation',
    'AddCommandOperation',
    'SyncChangesOperation'
]