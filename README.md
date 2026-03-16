# Smart File Search

A fast and efficient Python-based file searching tool with multiple search capabilities.

## Features

- 🔍 **Search by filename** - Find files using pattern matching with wildcard support
- 📄 **Search by file type** - Filter files by extension (.py, .txt, .json, etc.)
- 🔎 **Search by keyword** - Search for specific keywords inside file contents
- 🎯 **Combined search** - Use multiple criteria simultaneously for precise results
- 📊 **Detailed results** - View file paths, sizes, and match counts
- ⚡ **Fast scanning** - Efficiently walks through directory trees
- 🛡️ **Safe handling** - Gracefully handles binary files and permission errors

## Installation

### Requirements
- Python 3.6 or higher
- No external dependencies required (uses standard library only)

### Setup
1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd smart-file-search
   ```

3. Make the main script executable (optional):
   ```bash
   chmod +x main.py
   ```

## Usage

### Basic Syntax
```bash
python main.py <search_path> [OPTIONS]
```

### Search Options

| Option | Description | Example |
|--------|-------------|---------|
| `-n, --name` | Search by filename pattern (wildcards supported) | `--name "*.py"` |
| `-t, --type` | Search by file extension | `--type txt` |
| `-k, --keyword` | Search for keyword in file contents | `--keyword "TODO"` |
| `-e, --extensions` | Limit keyword search to specific extensions | `--extensions py txt` |
| `-c, --case-sensitive` | Enable case-sensitive search | `--case-sensitive` |
| `-m, --max-size` | Max file size for content search (MB) | `--max-size 5` |
| `-l, --limit` | Limit number of results shown | `--limit 10` |
| `-v, --verbose` | Show detailed file information | `--verbose` |

## Examples

### 1. Search by Filename Pattern
Find all Python files:
```bash
python main.py /path/to/search --name "*.py"
```

Find files starting with "config":
```bash
python main.py /path/to/search --name "config*"
```

### 2. Search by File Type
Find all text files:
```bash
python main.py /path/to/search --type txt
```

Find all JSON files:
```bash
python main.py /path/to/search --type json
```

### 3. Search by Keyword in Files
Find files containing "TODO":
```bash
python main.py /path/to/search --keyword "TODO"
```

Case-sensitive keyword search:
```bash
python main.py /path/to/search --keyword "Error" --case-sensitive
```

Limit keyword search to Python and text files:
```bash
python main.py /path/to/search --keyword "import" --extensions py txt
```

### 4. Combined Search
Find Python files with "TODO" in their content:
```bash
python main.py /path/to/search --type py --keyword "TODO"
```

Find config files (name pattern + type + keyword):
```bash
python main.py /path/to/search --name "config*" --type json --keyword "database"
```

### 5. Advanced Options
Search with verbose output:
```bash
python main.py /path/to/search --name "*.log" --verbose
```

Limit results to first 5 matches:
```bash
python main.py /path/to/search --keyword "error" --limit 5
```

Search large files (up to 50MB):
```bash
python main.py /path/to/search --keyword "exception" --max-size 50
```

## Project Structure

```
smart-file-search/
│
├── src/
│   ├── __init__.py           # Package initialization
│   ├── file_searcher.py      # Core search functionality
│   └── cli.py                # Command-line interface
│
├── examples/                 # Example files for testing
│   ├── example.py
│   ├── sample.txt
│   └── config.json
│
├── tests/                    # Unit tests (to be implemented)
│
├── main.py                   # Main entry point
└── README.md                 # This file
```

## Core Components

### FileSearcher Class
The main search engine located in `src/file_searcher.py`:

- `search_by_name(pattern, case_sensitive)` - Search by filename pattern
- `search_by_type(file_extension)` - Search by file type
- `search_by_keyword(keyword, file_extensions, case_sensitive)` - Search file contents
- `search_combined(...)` - Combine multiple search criteria

### CLI Interface
User-friendly command-line interface in `src/cli.py`:
- Argument parsing and validation
- Result formatting and display
- Error handling

## Output Format

### Compact Mode (default)
```
Found 3 file(s):

1. /path/to/file1.py (2 matches)
2. /path/to/file2.py (5 matches)
3. /path/to/config.json
```

### Verbose Mode (`--verbose`)
```
================================================================================
Result #1
================================================================================
Name:      example.py
Path:      /path/to/example.py
Directory: /path/to
Size:      2.45 KB
Extension: .py
Matches:   2
```

## Technical Details

### Search Algorithms
- **Filename search**: Uses `fnmatch` for wildcard pattern matching
- **Content search**: Reads files with UTF-8 encoding (ignores binary files)
- **File type search**: Direct extension matching

### Performance Considerations
- Files larger than configured max size are skipped in content search
- Binary files are automatically detected and skipped
- Permission errors are handled gracefully
- Memory-efficient file iteration using `os.walk()`

### Safety Features
- Path validation before searching
- Exception handling for unreadable files
- Configurable file size limits
- Encoding error handling

## Use Cases

1. **Development**: Find TODO/FIXME comments across a codebase
2. **Configuration**: Locate config files containing specific settings
3. **Documentation**: Search for documentation files by name or content
4. **Log analysis**: Find log files with specific error messages
5. **Code review**: Locate files with specific function names or imports
6. **Cleanup**: Find unused files or deprecated code markers

## Limitations

- Content search only works with text files (binary files are skipped)
- Very large files may be slow to search (use `--max-size` to limit)
- Symbolic links are followed by default
- No regex support for filename patterns (uses fnmatch wildcards)

## Future Enhancements

- [ ] Add regular expression support for patterns
- [ ] Implement exclude patterns (ignore certain directories/files)
- [ ] Add export results to file (CSV, JSON)
- [ ] Parallel processing for large directory trees
- [ ] GUI interface
- [ ] Configuration file support
- [ ] Search result caching

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Author

Created as a demonstration of Python file handling and CLI development.

## Support

For issues, questions, or suggestions, please open an issue in the project repository.
