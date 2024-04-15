# tree_dot

This project provides a set of Python scripts designed to create a comprehensive markdown documentation of a project's file structure and contents. It's particularly useful for developers and teams who need a quick and organized overview of their project files, including specific details like programming language syntax highlighting in markdown format for improved readability.

## Quick Start

```bash
curl -L -o dot_v2.py https://raw.githubusercontent.com/eugen-hoppe/tree_dot/main/dot.py

```

or

```bash
curl -L -o dot_v2.py https://raw.githubusercontent.com/eugen-hoppe/tree_dot/main/dot.py && python3 dot_v2.py

```

## Features

- **Project Tree Generation**: Automatically generates a tree view of the project's directory structure, including all relevant files based on specified extensions.
- **Content Extraction**: Reads and extracts the content of files, allowing for easy inclusion in the generated markdown documentation.
- **Markdown Formatting**: Outputs the directory tree and file contents into a well-formatted markdown file (`overview.md`), using syntax highlighting for various programming languages to enhance the readability and understandability of code blocks.
- **Dynamic Configuration**: Allows customization of included file types, excluded directories and files, and specific syntax highlighting mappings through editable configurations.

## Configuration

Modify the following configurations in the script as per your project needs:

- `INCLUDE_EXTENSIONS`: List of file extensions to include in the documentation.
- `EXCLUDE_DIR_PREFIXES`: List of directory prefixes to exclude from the documentation.
- `EXCLUDE_FILE_PREFIXES`: List of file prefixes to exclude from the documentation.
- `CODE_BLOCK_LABELS`: Dictionary mapping file extensions to their respective code languages for markdown syntax highlighting.

## Requirements

- Python 3.10 or higher
- Access to the file system for which the documentation is to be generated

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements. Ensure you provide a detailed description of your changes and the benefits they bring.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



_[v1.0(depricated)](https://github.com/eugen-hoppe/tree_dot/tree/ec180515428d47d62e4833f017cd620f8542fc4c)_

