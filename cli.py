"""
Smart File Search - Command Line Interface
Provides a user-friendly CLI for file searching.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict
from src.file_searcher import FileSearcher


class CLI:
    """Command Line Interface for Smart File Search"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser"""
        parser = argparse.ArgumentParser(
            description='Smart File Search - Fast file searching tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Search by filename pattern
  python main.py /path/to/search --name "*.txt"
  
  # Search by file type
  python main.py /path/to/search --type py
  
  # Search by keyword in files
  python main.py /path/to/search --keyword "TODO"
  
  # Combined search
  python main.py /path/to/search --name "config*" --type json --keyword "database"
  
  # Case-sensitive search
  python main.py /path/to/search --keyword "Error" --case-sensitive
            """
        )
        
        parser.add_argument(
            'path',
            type=str,
            help='Directory path to search in'
        )
        
        parser.add_argument(
            '-n', '--name',
            type=str,
            help='Search by filename pattern (supports wildcards like *.txt)'
        )
        
        parser.add_argument(
            '-t', '--type',
            type=str,
            help='Search by file type/extension (e.g., txt, py, json)'
        )
        
        parser.add_argument(
            '-k', '--keyword',
            type=str,
            help='Search for keyword inside files'
        )
        
        parser.add_argument(
            '-e', '--extensions',
            type=str,
            nargs='+',
            help='Limit keyword search to specific file extensions'
        )
        
        parser.add_argument(
            '-c', '--case-sensitive',
            action='store_true',
            help='Perform case-sensitive search'
        )
        
        parser.add_argument(
            '-m', '--max-size',
            type=int,
            default=10,
            help='Maximum file size in MB for content search (default: 10)'
        )
        
        parser.add_argument(
            '-l', '--limit',
            type=int,
            help='Limit number of results displayed'
        )
        
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Show detailed file information'
        )
        
        return parser
    
    def run(self, args=None):
        """Run the CLI application"""
        parsed_args = self.parser.parse_args(args)
        
        try:
            # Initialize searcher
            searcher = FileSearcher(parsed_args.path)
            
            # Perform search based on provided arguments
            results = self._perform_search(searcher, parsed_args)
            
            # Display results
            self._display_results(results, parsed_args)
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nSearch cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _perform_search(self, searcher: FileSearcher, args) -> List[Dict[str, str]]:
        """Perform the appropriate search based on arguments"""
        
        # Check if multiple search criteria are provided
        has_name = args.name is not None
        has_type = args.type is not None
        has_keyword = args.keyword is not None
        
        if has_name and has_type and has_keyword:
            # Combined search
            print(f"Searching for files matching all criteria...")
            return searcher.search_combined(
                name_pattern=args.name,
                file_type=args.type,
                keyword=args.keyword,
                case_sensitive=args.case_sensitive
            )
        
        elif has_name and has_type:
            # Name + Type combined
            return searcher.search_combined(
                name_pattern=args.name,
                file_type=args.type,
                case_sensitive=args.case_sensitive
            )
        
        elif has_name and has_keyword:
            # Name + Keyword combined
            return searcher.search_combined(
                name_pattern=args.name,
                keyword=args.keyword,
                case_sensitive=args.case_sensitive
            )
        
        elif has_type and has_keyword:
            # Type + Keyword combined
            return searcher.search_combined(
                file_type=args.type,
                keyword=args.keyword,
                case_sensitive=args.case_sensitive
            )
        
        elif has_name:
            # Name only
            print(f"Searching for files by name pattern: {args.name}")
            return searcher.search_by_name(args.name, args.case_sensitive)
        
        elif has_type:
            # Type only
            print(f"Searching for files by type: .{args.type}")
            return searcher.search_by_type(args.type)
        
        elif has_keyword:
            # Keyword only
            print(f"Searching for keyword: '{args.keyword}'")
            return searcher.search_by_keyword(
                args.keyword,
                file_extensions=args.extensions,
                case_sensitive=args.case_sensitive,
                max_file_size_mb=args.max_size
            )
        
        else:
            print("Error: Please specify at least one search criterion (--name, --type, or --keyword)")
            sys.exit(1)
    
    def _display_results(self, results: List[Dict[str, str]], args):
        """Display search results"""
        
        if not results:
            print("\nNo files found matching the criteria.")
            return
        
        # Apply limit if specified
        total_results = len(results)
        if args.limit and args.limit < total_results:
            results = results[:args.limit]
            print(f"\nShowing {args.limit} of {total_results} results:\n")
        else:
            print(f"\nFound {total_results} file(s):\n")
        
        # Display results
        for idx, file_info in enumerate(results, 1):
            if args.verbose:
                self._display_verbose(idx, file_info)
            else:
                self._display_compact(idx, file_info)
        
        if args.limit and args.limit < total_results:
            print(f"\n... and {total_results - args.limit} more results.")
            print(f"Use --limit to see more or remove it to see all results.")
    
    def _display_compact(self, idx: int, file_info: Dict[str, str]):
        """Display file information in compact format"""
        matches = file_info.get('matches', '')
        match_info = f" ({matches} matches)" if matches else ""
        print(f"{idx}. {file_info['path']}{match_info}")
    
    def _display_verbose(self, idx: int, file_info: Dict[str, str]):
        """Display file information in verbose format"""
        print(f"{'='*80}")
        print(f"Result #{idx}")
        print(f"{'='*80}")
        print(f"Name:      {file_info['name']}")
        print(f"Path:      {file_info['path']}")
        print(f"Directory: {file_info['directory']}")
        print(f"Size:      {file_info['size']}")
        print(f"Extension: {file_info['extension']}")
        
        if 'matches' in file_info:
            print(f"Matches:   {file_info['matches']}")
        
        print()


def main():
    """Entry point for CLI"""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()
