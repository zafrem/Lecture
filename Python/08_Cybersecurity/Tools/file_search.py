#!/usr/bin/env python3
"""
Local PC File Search Tool
------------------------
This tool searches your local PC for files matching specified patterns and generates a detailed report.

Input: File patterns, search path, and various filters
Output: Detailed report of matching files with metadata

Usage:
  python file_search.py --pattern "*.pdf" --path /Users/username/Documents
  python file_search.py --pattern "password*.txt" "config*.ini" --path /Users --sensitive
  python file_search.py --pattern "*.mp3" --path /Users --size-min 10MB --size-max 50MB
  python file_search.py --pattern "*.log" --path /var/log --modified-after 2023-01-01
  
Features:
- Multiple pattern search with wildcards
- Content search within files (including sensitive data detection)
- Metadata collection (size, timestamps, permissions)
- Size and date filtering
- Comprehensive reporting in various formats (text, CSV, JSON)
"""

import os
import sys
import glob
import re
import time
import stat
import json
import csv
import hashlib
import argparse
import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import magic  # python-magic for file type detection

# Regular expressions for sensitive data
PATTERNS = {
    'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
    'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
    'api_key': r'\b[A-Za-z0-9_-]{20,40}\b',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'password_field': r'password[\s]*[=:][^\n]{3,}'
}


class FileSearch:
    """Search for files based on pattern and collect metadata"""
    
    def __init__(self, patterns, base_path, recursive=True, 
                 check_content=False, sensitive_check=False,
                 max_file_size=10*1024*1024, max_threads=10):
        """
        Initialize file search with patterns and options
        
        Args:
            patterns (list): List of file patterns to search for (e.g., ["*.pdf", "*.txt"])
            base_path (str): Base path to start the search
            recursive (bool): Whether to search recursively
            check_content (bool): Whether to check file content
            sensitive_check (bool): Whether to check for sensitive information
            max_file_size (int): Maximum file size to check content (in bytes)
            max_threads (int): Maximum number of threads to use
        """
        self.patterns = patterns
        self.base_path = os.path.abspath(base_path)
        self.recursive = recursive
        self.check_content = check_content
        self.sensitive_check = sensitive_check
        self.max_file_size = max_file_size
        self.max_threads = max_threads
        self.found_files = []
        self.errors = []
    
    def search(self, size_min=None, size_max=None, 
               modified_after=None, modified_before=None,
               created_after=None, created_before=None):
        """
        Search for files matching the specified criteria
        
        Args:
            size_min (int): Minimum file size in bytes
            size_max (int): Maximum file size in bytes
            modified_after (datetime): Files modified after this date
            modified_before (datetime): Files modified before this date
            created_after (datetime): Files created after this date
            created_before (datetime): Files created before this date
            
        Returns:
            list: List of dictionaries with file information
        """
        print(f"Searching in {self.base_path}...")
        print(f"Patterns: {', '.join(self.patterns)}")
        
        self.found_files = []
        matches = []
        
        # Convert to glob patterns with base path
        for pattern in self.patterns:
            if self.recursive:
                # For recursive search, we need to use os.walk
                for root, dirs, files in os.walk(self.base_path):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        if glob.fnmatch.fnmatch(file, pattern):
                            full_path = os.path.join(root, file)
                            matches.append(full_path)
            else:
                # For non-recursive search, we can use glob directly
                pattern_path = os.path.join(self.base_path, pattern)
                matches.extend(glob.glob(pattern_path))
        
        # Remove duplicates
        matches = list(set(matches))
        
        # Apply filters
        filtered_matches = []
        for file_path in matches:
            try:
                # Skip if not a file
                if not os.path.isfile(file_path):
                    continue
                    
                # Get file stats
                stats = os.stat(file_path)
                file_size = stats.st_size
                modified_time = datetime.datetime.fromtimestamp(stats.st_mtime)
                created_time = datetime.datetime.fromtimestamp(stats.st_ctime)
                
                # Apply filters
                if size_min and file_size < size_min:
                    continue
                if size_max and file_size > size_max:
                    continue
                if modified_after and modified_time < modified_after:
                    continue
                if modified_before and modified_time > modified_before:
                    continue
                if created_after and created_time < created_after:
                    continue
                if created_before and created_time > created_before:
                    continue
                
                filtered_matches.append(file_path)
            except Exception as e:
                self.errors.append(f"Error filtering {file_path}: {str(e)}")
        
        print(f"Found {len(filtered_matches)} matches after filtering")
        
        # Process files with metadata using thread pool for speed
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = list(executor.map(self.process_file, filtered_matches))
        
        # Filter out None results (from errors)
        self.found_files = [r for r in results if r]
        
        print(f"Processed {len(self.found_files)} files")
        return self.found_files
    
    def process_file(self, file_path):
        """Process a single file and collect metadata"""
        try:
            # Get file stats
            stats = os.stat(file_path)
            
            # Basic file info
            file_info = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'directory': os.path.dirname(file_path),
                'size': stats.st_size,
                'size_human': self.human_readable_size(stats.st_size),
                'created': datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                'modified': datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
                'accessed': datetime.datetime.fromtimestamp(stats.st_atime).isoformat(),
                'permissions': oct(stats.st_mode)[-3:],
                'owner_id': stats.st_uid,
                'group_id': stats.st_gid
            }
            
            # Try to detect file type
            try:
                file_info['mime_type'] = magic.from_file(file_path, mime=True)
                file_info['file_type'] = magic.from_file(file_path)
            except:
                file_info['mime_type'] = 'unknown'
                file_info['file_type'] = 'unknown'
            
            # Check content if requested and file is not too large
            if (self.check_content or self.sensitive_check) and stats.st_size <= self.max_file_size:
                # Skip binary files for content search
                if file_info['mime_type'] and ('text/' in file_info['mime_type'] or 
                                            'application/json' in file_info['mime_type'] or
                                            'application/xml' in file_info['mime_type']):
                    try:
                        sensitive_data = self.check_file_content(file_path)
                        if sensitive_data:
                            file_info['sensitive_data'] = sensitive_data
                    except Exception as e:
                        file_info['content_error'] = str(e)
            
            # Calculate hash for small files
            if stats.st_size <= self.max_file_size:
                try:
                    file_info['md5'] = self.get_file_hash(file_path)
                except Exception as e:
                    file_info['hash_error'] = str(e)
            
            return file_info
            
        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {str(e)}")
            return None
    
    def check_file_content(self, file_path):
        """Check file content for sensitive information"""
        sensitive_data = {}
        
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                
            # Check each pattern
            for pattern_name, regex in PATTERNS.items():
                matches = re.findall(regex, content)
                if matches:
                    # Truncate matches to avoid overwhelming output
                    displayed_matches = matches[:3]  
                    if len(matches) > 3:
                        displayed_matches.append(f"... and {len(matches) - 3} more")
                    sensitive_data[pattern_name] = displayed_matches
            
            return sensitive_data if sensitive_data else None
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()
    
    def human_readable_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ("B", "KB", "MB", "GB", "TB", "PB")
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
        return f"{size_bytes:.2f}{size_names[i]}"
    
    def generate_report(self, output_format='text', output_file=None):
        """Generate a report of found files"""
        if not self.found_files:
            print("No files to report")
            return False
            
        # Sort files by size (largest first)
        sorted_files = sorted(self.found_files, key=lambda x: x.get('size', 0), reverse=True)
        
        if output_format == 'text':
            return self._generate_text_report(sorted_files, output_file)
        elif output_format == 'csv':
            return self._generate_csv_report(sorted_files, output_file)
        elif output_format == 'json':
            return self._generate_json_report(sorted_files, output_file)
        else:
            print(f"Unsupported output format: {output_format}")
            return False
    
    def _generate_text_report(self, files, output_file=None):
        """Generate a plain text report"""
        report = []
        report.append("=" * 80)
        report.append(f"FILE SEARCH REPORT - {datetime.datetime.now().isoformat()}")
        report.append("=" * 80)
        report.append(f"Search path: {self.base_path}")
        report.append(f"Patterns: {', '.join(self.patterns)}")
        report.append(f"Files found: {len(files)}")
        report.append("=" * 80)
        
        for i, file in enumerate(files, 1):
            report.append(f"\n{i}. {file['name']}")
            report.append(f"   Path: {file['path']}")
            report.append(f"   Size: {file['size_human']} ({file['size']} bytes)")
            report.append(f"   Type: {file.get('file_type', 'Unknown')}")
            report.append(f"   Modified: {file['modified']}")
            report.append(f"   Created: {file['created']}")
            report.append(f"   Permissions: {file['permissions']}")
            
            if 'md5' in file:
                report.append(f"   MD5: {file['md5']}")
                
            if 'sensitive_data' in file:
                report.append("   Sensitive data found:")
                for data_type, matches in file['sensitive_data'].items():
                    report.append(f"     - {data_type}: {matches}")
        
        # Add errors if any
        if self.errors:
            report.append("\n" + "=" * 80)
            report.append("ERRORS")
            report.append("=" * 80)
            for error in self.errors:
                report.append(f"- {error}")
        
        report_text = "\n".join(report)
        
        # Write to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                print(f"Report saved to {output_file}")
                return True
            except Exception as e:
                print(f"Error saving report: {e}")
                return False
        else:
            print(report_text)
            return True
    
    def _generate_csv_report(self, files, output_file):
        """Generate a CSV report"""
        if not output_file:
            print("Output file is required for CSV format")
            return False
            
        try:
            with open(output_file, 'w', newline='') as f:
                # Determine all possible fields
                fields = set()
                for file in files:
                    fields.update(file.keys())
                
                # Sort fields for consistent output
                fieldnames = sorted(list(fields))
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for file in files:
                    # Convert any complex objects to strings
                    row = {}
                    for key, value in file.items():
                        if isinstance(value, dict):
                            row[key] = json.dumps(value)
                        else:
                            row[key] = value
                    writer.writerow(row)
                    
            print(f"CSV report saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving CSV report: {e}")
            return False
    
    def _generate_json_report(self, files, output_file):
        """Generate a JSON report"""
        try:
            report = {
                'metadata': {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'search_path': self.base_path,
                    'patterns': self.patterns,
                    'files_found': len(files)
                },
                'files': files,
                'errors': self.errors
            }
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                print(f"JSON report saved to {output_file}")
            else:
                print(json.dumps(report, indent=2, default=str))
            return True
        except Exception as e:
            print(f"Error generating JSON report: {e}")
            return False


def parse_size(size_str):
    """Parse a human-readable size string to bytes"""
    if not size_str:
        return None
        
    size_str = size_str.upper()
    
    # Check if already a number
    if size_str.isdigit():
        return int(size_str)
    
    # Parse size with unit
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                size = float(size_str[:-len(unit)])
                return int(size * multiplier)
            except ValueError:
                raise ValueError(f"Invalid size format: {size_str}")
    
    raise ValueError(f"Invalid size format: {size_str}")


def parse_date(date_str):
    """Parse a date string to datetime object"""
    if not date_str:
        return None
        
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD or similar format.")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Search for files matching patterns and generate reports")
    
    # Required arguments
    parser.add_argument('--pattern', '-p', nargs='+', required=True,
                      help="File pattern(s) to search for (e.g., *.pdf *.txt)")
    parser.add_argument('--path', required=True,
                      help="Base path to start the search")
    
    # Search options
    parser.add_argument('--no-recursive', action='store_true',
                      help="Don't search subdirectories")
    parser.add_argument('--check-content', action='store_true',
                      help="Check file content (slower)")
    parser.add_argument('--sensitive', action='store_true',
                      help="Check for sensitive information in files")
    parser.add_argument('--max-file-size', default="10MB",
                      help="Maximum file size to check content (e.g., 10MB)")
    parser.add_argument('--threads', type=int, default=10,
                      help="Maximum number of threads to use")
    
    # Filters
    parser.add_argument('--size-min',
                      help="Minimum file size (e.g., 1MB)")
    parser.add_argument('--size-max',
                      help="Maximum file size (e.g., 10MB)")
    parser.add_argument('--modified-after',
                      help="Files modified after this date (YYYY-MM-DD)")
    parser.add_argument('--modified-before',
                      help="Files modified before this date (YYYY-MM-DD)")
    parser.add_argument('--created-after',
                      help="Files created after this date (YYYY-MM-DD)")
    parser.add_argument('--created-before',
                      help="Files created before this date (YYYY-MM-DD)")
    
    # Output options
    parser.add_argument('--format', choices=['text', 'csv', 'json'], default='text',
                      help="Output format")
    parser.add_argument('--output', '-o',
                      help="Output file")
    
    return parser.parse_args()


def main():
    """Main function"""
    # Parse arguments
    args = parse_arguments()
    
    # Convert size arguments
    max_file_size = parse_size(args.max_file_size)
    size_min = parse_size(args.size_min) if args.size_min else None
    size_max = parse_size(args.size_max) if args.size_max else None
    
    # Convert date arguments
    modified_after = parse_date(args.modified_after) if args.modified_after else None
    modified_before = parse_date(args.modified_before) if args.modified_before else None
    created_after = parse_date(args.created_after) if args.created_after else None
    created_before = parse_date(args.created_before) if args.created_before else None
    
    # Create file search
    search = FileSearch(
        patterns=args.pattern,
        base_path=args.path,
        recursive=not args.no_recursive,
        check_content=args.check_content or args.sensitive,
        sensitive_check=args.sensitive,
        max_file_size=max_file_size,
        max_threads=args.threads
    )
    
    # Start timer
    start_time = time.time()
    
    # Search files
    files = search.search(
        size_min=size_min,
        size_max=size_max,
        modified_after=modified_after,
        modified_before=modified_before,
        created_after=created_after,
        created_before=created_before
    )
    
    # Generate report
    if files:
        search.generate_report(output_format=args.format, output_file=args.output)
        
    # Print summary
    elapsed = time.time() - start_time
    print(f"\nSearch completed in {elapsed:.2f} seconds")
    print(f"Found {len(files)} matching files")
    
    if search.errors:
        print(f"Encountered {len(search.errors)} errors during search")


if __name__ == "__main__":
    main()
