"""
MCP Code Editor - A FastMCP server providing powerful code editing tools.

This package provides comprehensive code editing functionality including:
- Precise file modifications with diff-based operations
- File creation and reading with line numbers
- Project analysis and structure inspection
- AST (Abstract Syntax Tree) analysis for Python code
- Console tools for interactive processes
- Library indexing for external dependencies
- Code definition search and navigation
"""

__version__ = "0.1.4"
__author__ = "MCP Code Editor Team"
__email__ = "mcpcodeeditor@example.com"

# Import main components
from .core import DiffBlock, DiffBuilder, FileModifier

__all__ = [
    "DiffBlock",
    "DiffBuilder", 
    "FileModifier",
    "__version__",
    "__author__",
    "__email__"
]
