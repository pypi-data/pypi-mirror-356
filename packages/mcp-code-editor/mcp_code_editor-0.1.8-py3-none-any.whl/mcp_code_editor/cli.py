#!/usr/bin/env python3
"""
Entry point script for MCP Code Editor.
This script handles the import path issues when run via uvx.
"""

def main():
    """Main entry point that handles import issues."""
    import sys
    import os
    from pathlib import Path
    
    # Ensure the package directory is in the Python path
    package_dir = Path(__file__).parent
    if str(package_dir) not in sys.path:
        sys.path.insert(0, str(package_dir))
    
    # Now import and run the main function
    try:
        from mcp_code_editor.main import main as main_func
        main_func()
    except ImportError:
        # Fallback: try different import paths
        try:
            # Add parent directory to path
            parent_dir = package_dir.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            from mcp_code_editor.main import main as main_func
            main_func()
        except ImportError as e:
            print(f"Error importing MCP Code Editor: {e}")
            print("Please ensure the package is properly installed.")
            sys.exit(1)

if __name__ == "__main__":
    main()
