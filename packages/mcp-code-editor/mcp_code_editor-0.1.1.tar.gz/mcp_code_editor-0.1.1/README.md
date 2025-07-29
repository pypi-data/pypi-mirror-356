# MCP Code Editor

MCP Code Editor is a Python package that provides powerful code editing functionality using the uvx framework.

## Installation

You can install MCP Code Editor using pip:

```
pip install mcp-code-editor
```

## Usage

After installation, you can run the MCP Code Editor using the following command:

```
uvx mcp-code-editor
```

## Features

- Precise file modifications with diff-based operations
- File creation and reading with line numbers
- Project structure analysis and intelligent file management
- Code definition search and indexing
- External library indexing and searching
- AST-based code analysis

## API

The `MCPCodeEditor` class provides the following main methods:

- `apply_diff_tool`: Apply precise file modifications using structured diff blocks
- `create_file_tool`: Create a new file with specified content
- `read_file_with_lines_tool`: Read a text file and return its content with line numbers
- `delete_file_tool`: Delete a file with optional backup creation
- `setup_code_editor_tool`: Setup code editor by analyzing project structure
- `project_files_tool`: Get project files using cached setup with filtering options
- `get_code_definition`: Get definitions of functions, classes, variables, and imports
- `index_library_tool`: Index an external Python library for code analysis
- `search_library_tool`: Search for definitions within indexed libraries
- `list_indexed_libraries_tool`: List all indexed libraries and their summaries

For detailed usage of each method, please refer to the docstrings in the code.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.