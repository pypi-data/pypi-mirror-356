"""
MCP Code Editor

A Python package providing powerful code editing tools including:
- Precise file modifications with diff-based operations
- File creation and reading with line numbers
- And more tools for code editing workflows

This modular package is designed to be easily extensible and used with uvx.
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

# Import tool functions
from .tools import (
    apply_diff, create_file, read_file_with_lines, delete_file,
    setup_code_editor, project_files, ProjectState,
    setup_code_editor_with_ast, search_definitions, get_file_definitions,
    update_file_ast_index, has_structural_changes,
    index_library, search_library, get_indexed_libraries, get_library_summary
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPCodeEditor:
    def __init__(self):
        self.project_state = ProjectState()

    async def apply_diff_tool(self, path: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply precise file modifications using structured diff blocks."""
        result = apply_diff(path, blocks)
        
        if result.get("success"):
            state = self.project_state
            if state and state.ast_enabled:
                if has_structural_changes(blocks):
                    state.ast_index = update_file_ast_index(path, state.ast_index)
                    logger.info(f"AST index updated for {path}")
        
        return result

    def create_file_tool(self, path: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        """Create a new file with the specified content."""
        return create_file(path, content, overwrite)

    def read_file_with_lines_tool(self, path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
        """Read a text file and return its content with line numbers."""
        return read_file_with_lines(path, start_line, end_line)

    def delete_file_tool(self, path: str, create_backup: bool = True) -> Dict[str, Any]:
        """Delete a file with optional backup creation."""
        return delete_file(path, create_backup)

    async def setup_code_editor_tool(self, path: str, analyze_ast: bool = True) -> Dict[str, Any]:
        """Setup code editor by analyzing project structure, .gitignore rules, and optionally AST."""
        result = setup_code_editor_with_ast(path, analyze_ast)
        
        if result.get("success"):
            self.project_state = ProjectState.from_setup_result(result, path)
            logger.info(f"Project setup complete: {self.project_state.total_files} files indexed")
        
        return result

    async def project_files_tool(self, filter_extensions: Optional[List[str]] = None, 
                                 max_depth: Optional[int] = None, 
                                 format_as_tree: bool = True) -> Dict[str, Any]:
        """Get project files using cached setup with filtering options."""
        if not self.project_state.setup_complete:
            return {
                "success": False,
                "error": "ProjectNotSetup",
                "message": "Project not setup. Please run setup_code_editor_tool first."
            }
        
        return project_files(self.project_state, filter_extensions, max_depth, format_as_tree)

    async def get_code_definition(self, identifier: str, context_file: Optional[str] = None,
                                  definition_type: str = "any", include_usage: bool = False) -> Dict[str, Any]:
        """Get definitions of functions, classes, variables, and imports from the project."""
        if not self.project_state.setup_complete or not self.project_state.ast_enabled:
            return {
                "success": False,
                "error": "ASTNotEnabled",
                "message": "AST analysis is not enabled. Please run setup_code_editor_tool with analyze_ast=True."
            }
        
        result = search_definitions(
            self.project_state.ast_index,
            identifier,
            context_file,
            definition_type,
            include_usage
        )
        
        return {
            "success": True,
            "definitions": result['definitions'],
            "metadata": result['metadata']
        }

    async def index_library_tool(self, library_name: str) -> Dict[str, Any]:
        """Index an external Python library for code analysis."""
        return index_library(library_name)

    async def search_library_tool(self, query: str, library_name: Optional[str] = None,
                                  search_type: str = "any", max_results: int = 10) -> Dict[str, Any]:
        """Search for definitions within indexed libraries."""
        return search_library(query, library_name, search_type, max_results)

    async def list_indexed_libraries_tool(self) -> Dict[str, Any]:
        """List all indexed libraries and their summaries."""
        indexed_libraries = get_indexed_libraries()
        summaries = {library: get_library_summary(library) for library in indexed_libraries}
        
        return {
            "success": True,
            "indexed_libraries": indexed_libraries,
            "summaries": summaries
        }

def main():
    """Entry point for the uvx command."""
    editor = MCPCodeEditor()
    # Here you would typically set up your uvx server and route the commands to the appropriate methods of the MCPCodeEditor class
    print("MCP Code Editor is running. Use 'uvx mcp-code-editor' to interact with it.")

if __name__ == "__main__":
    main()
