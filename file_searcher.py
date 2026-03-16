"""
Smart File Search - Core Search Module
Provides file searching capabilities by name, type, and content.
"""

import os
import fnmatch
from pathlib import Path
from typing import List, Dict, Optional


class FileSearcher:
    """
    A class for searching files in a directory with various criteria.
    """
    
    def __init__(self, search_path: str):
        """
        Initialize the FileSearcher with a base search path.
        
        Args:
            search_path: Root directory to search in
        """
        self.search_path = Path(search_path).resolve()
        if not self.search_path.exists():
            raise ValueError(f"Search path does not exist: {search_path}")
        if not self.search_path.is_dir():
            raise ValueError(f"Search path is not a directory: {search_path}")
    
    def search_by_name(self, pattern: str, case_sensitive: bool = False) -> List[Dict[str, str]]:
        """
        Search for files by name pattern.
        
        Args:
            pattern: Pattern to match (supports wildcards like *.txt)
            case_sensitive: Whether to perform case-sensitive search
            
        Returns:
            List of dictionaries containing file information
        """
        results = []
        
        for root, dirs, files in os.walk(self.search_path):
            for filename in files:
                match_name = filename if case_sensitive else filename.lower()
                match_pattern = pattern if case_sensitive else pattern.lower()
                
                if fnmatch.fnmatch(match_name, match_pattern):
                    file_path = os.path.join(root, filename)
                    results.append(self._get_file_info(file_path))
        
        return results
    
    def search_by_type(self, file_extension: str) -> List[Dict[str, str]]:
        """
        Search for files by file type/extension.
        
        Args:
            file_extension: File extension to search for (e.g., 'txt', '.txt', 'py')
            
        Returns:
            List of dictionaries containing file information
        """
        # Normalize extension
        if not file_extension.startswith('.'):
            file_extension = '.' + file_extension
        
        results = []
        
        for root, dirs, files in os.walk(self.search_path):
            for filename in files:
                if filename.endswith(file_extension):
                    file_path = os.path.join(root, filename)
                    results.append(self._get_file_info(file_path))
        
        return results
    
    def search_by_keyword(self, keyword: str, file_extensions: Optional[List[str]] = None,
                         case_sensitive: bool = False, max_file_size_mb: int = 10) -> List[Dict[str, str]]:
        """
        Search for files containing a specific keyword.
        
        Args:
            keyword: Keyword to search for in file contents
            file_extensions: Optional list of file extensions to limit search
            case_sensitive: Whether to perform case-sensitive search
            max_file_size_mb: Maximum file size to search (in MB) to avoid memory issues
            
        Returns:
            List of dictionaries containing file information and match details
        """
        results = []
        max_size_bytes = max_file_size_mb * 1024 * 1024
        
        # Prepare keyword for search
        search_keyword = keyword if case_sensitive else keyword.lower()
        
        for root, dirs, files in os.walk(self.search_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Check file extension if specified
                if file_extensions:
                    if not any(filename.endswith(ext if ext.startswith('.') else '.' + ext) 
                              for ext in file_extensions):
                        continue
                
                # Skip files that are too large
                try:
                    if os.path.getsize(file_path) > max_size_bytes:
                        continue
                except OSError:
                    continue
                
                # Try to read and search file content
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        search_content = content if case_sensitive else content.lower()
                        
                        if search_keyword in search_content:
                            file_info = self._get_file_info(file_path)
                            # Count occurrences
                            file_info['matches'] = search_content.count(search_keyword)
                            results.append(file_info)
                except (UnicodeDecodeError, PermissionError, OSError):
                    # Skip binary files or files we can't read
                    continue
        
        return results
    
    def search_combined(self, name_pattern: Optional[str] = None, 
                       file_type: Optional[str] = None,
                       keyword: Optional[str] = None,
                       case_sensitive: bool = False) -> List[Dict[str, str]]:
        """
        Perform a combined search with multiple criteria.
        
        Args:
            name_pattern: Optional filename pattern
            file_type: Optional file extension
            keyword: Optional keyword to search in content
            case_sensitive: Whether to perform case-sensitive search
            
        Returns:
            List of dictionaries containing file information
        """
        all_files = []
        
        # Start with all files in directory
        for root, dirs, files in os.walk(self.search_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                all_files.append((file_path, filename))
        
        results = []
        
        for file_path, filename in all_files:
            matches = True
            
            # Check name pattern
            if name_pattern:
                match_name = filename if case_sensitive else filename.lower()
                match_pattern = name_pattern if case_sensitive else name_pattern.lower()
                if not fnmatch.fnmatch(match_name, match_pattern):
                    matches = False
            
            # Check file type
            if matches and file_type:
                ext = file_type if file_type.startswith('.') else '.' + file_type
                if not filename.endswith(ext):
                    matches = False
            
            # Check keyword
            if matches and keyword:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        search_content = content if case_sensitive else content.lower()
                        search_keyword = keyword if case_sensitive else keyword.lower()
                        
                        if search_keyword not in search_content:
                            matches = False
                except (UnicodeDecodeError, PermissionError, OSError):
                    matches = False
            
            if matches:
                file_info = self._get_file_info(file_path)
                results.append(file_info)
        
        return results
    
    def _get_file_info(self, file_path: str) -> Dict[str, str]:
        """
        Get detailed information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
        """
        stat_info = os.stat(file_path)
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size': self._format_size(stat_info.st_size),
            'size_bytes': stat_info.st_size,
            'extension': os.path.splitext(file_path)[1],
            'directory': os.path.dirname(file_path)
        }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
