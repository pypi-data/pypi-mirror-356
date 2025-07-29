from setuptools import setup, find_packages

setup(
    name="mcp_code_editor",
    version="0.1.1",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "uvx",
        "fastmcp",  # Add this if it's a separate package
    ],
    entry_points={
        "console_scripts": [
            "mcp-code-editor=mcp_code_editor:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A code editor package using uvx",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-code-editor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Updated to Python 3.8+ for async support
)