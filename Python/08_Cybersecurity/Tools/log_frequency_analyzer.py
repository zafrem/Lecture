#!/usr/bin/env python3
"""
Log Frequency Analyzer
---------------------
Analyzes log files and identifies the most frequently occurring log entries.

Input: One or more log files
Output: Summary of most common log patterns and their frequencies

Usage:
  python log_frequency_analyzer.py --files /var/log/syslog
  python log_frequency_analyzer.py --files /var/log/apache2/access.log --top 20
  python log_frequency_analyzer.py --files /var/log/auth.log /var/log/syslog --format syslog
  python log_frequency_analyzer.py --files app.log --output summary.txt --remove-timestamps

Features:
- Automatic log format detection
- Configurable similarity matching for grouping similar logs
- Support for various log formats
- Detailed frequency reports with examples
"""

import re
import os
import sys
import argparse
import datetime
from collections import Counter, defaultdict
from difflib import SequenceMatcher


class LogFrequencyAnalyzer:
    """Analyze logs and find most frequently occurring patterns"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.log_entries = []
        self.patterns = Counter()
        self.examples = defaultdict(list)
        self.similarity_threshold = 0.8  # Default similarity threshold
        
        # Common log format patterns
        self.formats = {
            'syslog': r'^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+[\w\-\.]+\s+([^:]+):\s+(.*)$',
            'apache': r'^(\S+) \S+ \S+ \[([^\]]+)\] "([^"]*)" (\d+) (\d+|-)',
            'nginx': r'^(\S+) - \S+ \[([^\]]+)\] "([^"]*)" (\d+) (\d+)',
            'json': r'.*"message":("[^"]+"|\[[^\]]+\]|\{[^\}]+\}|[^,"]+)',
            'default': r'^.*$'
        }
    
    def detect_format(self, sample_lines, format_hint=None):
        """Try to detect the log format from sample lines"""
        if format_hint and format_hint in self.formats:
            return format_hint
            
        # Count matches for each format
        format_matches = {fmt: 0 for fmt in self.formats}
        
        # Test each format against sample lines
        for line in sample_lines:
            for fmt, pattern in self.formats.items():
                if re.match(pattern, line):
                    format_matches[fmt] += 1
        
        # Find the format with the most matches
        best_format = max(format_matches, key=format_matches.get)
        if format_matches[best_format] > len(sample_lines) / 2:
            return best_format
        else:
            return 'default'
    
    def process_file(self, file_path, log_format=None, remove_timestamps=False):
        """Process a log file and extract patterns"""
        print(f"Processing {file_path}...")
        
        try:
            # Read the file
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                
            if not lines:
                print(f"Warning: {file_path} is empty")
                return 0
                
            # Detect format if not specified
            if not log_format:
                log_format = self.detect_format(lines[:100], None)
                print(f"Detected log format: {log_format}")
            
            # Process each line
            processed = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                processed += 1
                pattern = self.extract_pattern(line, log_format, remove_timestamps)
                self.patterns[pattern] += 1
                
                # Store a few examples of each pattern (up to 3)
                if len(self.examples[pattern]) < 3:
                    self.examples[pattern].append(line)
            
            print(f"Processed {processed} lines from {file_path}")
            return processed
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0
    
    def extract_pattern(self, line, log_format, remove_timestamps=False):
        """Extract the core pattern from a log line based on the format"""
        # If removing timestamps, do it before further processing
        if remove_timestamps:
            # Remove common timestamp patterns
            line = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:?\d{2}|Z)?', '<TIMESTAMP>', line)
            line = re.sub(r'\d{2}/\d{2}/\d{4}[ :]\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', line)
            line = re.sub(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', line)
            line = re.sub(r'\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', line)
            line = re.sub(r'\[\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s+[+-]\d{4}\]', '<TIMESTAMP>', line)
        
        # Format-specific pattern extraction
        if log_format == 'syslog':
            # For syslog, extract the program name and message
            match = re.match(self.formats['syslog'], line)
            if match:
                program, message = match.groups()
                # Normalize variable parts in the message
                message = self._normalize_message(message)
                return f"{program}: {message}"
                
        elif log_format in ('apache', 'nginx'):
            # For web server logs, extract the request and status
            match = re.match(self.formats[log_format], line)
            if match:
                if log_format == 'apache':
                    _, timestamp, request, status, _ = match.groups()
                else:
                    _, timestamp, request, status, _ = match.groups()
                # Normalize IP addresses and specific IDs in URLs
                request = re.sub(r'/\d+', '/<id>', request)
                return f"{request} (status {status})"
                
        elif log_format == 'json':
            # For JSON logs, try to extract the message field
            match = re.search(self.formats['json'], line)
            if match:
                message = match.group(1)
                # Normalize variable parts
                message = self._normalize_message(message)
                return message
        
        # Default: normalize the entire line
        return self._normalize_message(line)
    
    def _normalize_message(self, message):
        """Normalize a message by replacing variable parts with placeholders"""
        # Replace common variable patterns
        normalized = message
        
        # Replace hexadecimal identifiers/hashes
        normalized = re.sub(r'0x[0-9a-f]+', '<HEX>', normalized)
        
        # Replace UUIDs
        normalized = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', normalized)
        
        # Replace IP addresses
        normalized = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', normalized)
        
        # Replace file paths with variable names but keep the extension
        normalized = re.sub(r'(?<!/)[/\w\.-]+/[/\w\.-]+\.\w+', '<PATH>', normalized)
        
        # Replace numbers (but not if they're part of a word or specific error codes)
        normalized = re.sub(r'(?<!\w)\d+(?!\w)', '<NUM>', normalized)
        
        # Special case: Keep HTTP status codes as they are often significant
        normalized = re.sub(r'<NUM><NUM><NUM>', lambda m: message[m.start():m.end()], normalized)
        
        return normalized
    
    def group_similar_patterns(self, similarity_threshold=None):
        """Group similar patterns together to reduce noise"""
        if similarity_threshold is not None:
            self.similarity_threshold = similarity_threshold
            
        print(f"Grouping similar patterns (similarity threshold: {self.similarity_threshold})...")
        
        # Start with the most common patterns
        sorted_patterns = sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)
        
        # Group similar patterns
        groups = []
        remaining = list(sorted_patterns)
        
        while remaining:
            # Take the most common pattern as a new group
            current = remaining.pop(0)
            current_pattern, current_count = current
            
            # Find similar patterns
            similar = []
            i = 0
            while i < len(remaining):
                pattern, count = remaining[i]
                
                # Check similarity
                similarity = self._pattern_similarity(current_pattern, pattern)
                if similarity >= self.similarity_threshold:
                    similar.append(remaining.pop(i))
                else:
                    i += 1
            
            # Create a group
            group = {
                'pattern': current_pattern,
                'count': current_count,
                'similar': similar,
                'total': current_count + sum(count for _, count in similar),
                'examples': self.examples[current_pattern]
            }
            
            groups.append(group)
        
        return sorted(groups, key=lambda x: x['total'], reverse=True)
    
    def _pattern_similarity(self, pattern1, pattern2):
        """Calculate similarity between two patterns"""
        return SequenceMatcher(None, pattern1, pattern2).ratio()
    
    def generate_report(self, groups, top_n=10, output_file=None):
        """Generate a report of the most common log patterns"""
        report = []
        report.append("=" * 80)
        report.append(f"LOG FREQUENCY ANALYSIS REPORT - {datetime.datetime.now().isoformat()}")
        report.append("=" * 80)
        report.append(f"Top {min(top_n, len(groups))} log patterns:")
        report.append("")
        
        # Show top N groups
        for i, group in enumerate(groups[:top_n], 1):
            report.append(f"{i}. Pattern: {group['pattern']}")
            report.append(f"   Occurrences: {group['total']} ({group['count']} exact, {len(group['similar'])} similar)")
            
            # Show examples
            report.append("   Examples:")
            for example in group['examples']:
                report.append(f"   - {example[:100]}" + ("..." if len(example) > 100 else ""))
            
            # Show similar patterns if any
            if group['similar']:
                report.append("   Similar patterns:")
                for pattern, count in group['similar'][:3]:  # Show up to 3 similar patterns
                    report.append(f"   - {pattern} ({count} occurrences)")
                
                if len(group['similar']) > 3:
                    report.append(f"   - ... and {len(group['similar']) - 3} more similar patterns")
            
            report.append("")
        
        report_text = "\n".join(report)
        
        # Write to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                print(f"Report saved to {output_file}")
            except Exception as e:
                print(f"Error saving report: {e}")
                print(report_text)
        else:
            print(report_text)
            
        return report_text


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze log files and find most frequent patterns")
    parser.add_argument('--files', nargs='+', required=True,
                      help="Log file(s) to analyze")
    parser.add_argument('--format', choices=['syslog', 'apache', 'nginx', 'json', 'default'],
                      help="Log format (auto-detect if not specified)")
    parser.add_argument('--top', type=int, default=10,
                      help="Number of top patterns to show")
    parser.add_argument('--similarity', type=float, default=0.8,
                      help="Similarity threshold for grouping (0.0-1.0)")
    parser.add_argument('--output',
                      help="Output file for the report")
    parser.add_argument('--remove-timestamps', action='store_true',
                      help="Remove timestamps from log entries")
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    
    analyzer = LogFrequencyAnalyzer()
    
    # Process each file
    total_processed = 0
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue
            
        processed = analyzer.process_file(
            file_path, 
            log_format=args.format,
            remove_timestamps=args.remove_timestamps
        )
        total_processed += processed
    
    if total_processed == 0:
        print("No log entries were processed. Exiting.")
        sys.exit(1)
    
    # Group similar patterns
    groups = analyzer.group_similar_patterns(args.similarity)
    
    # Generate report
    analyzer.generate_report(groups, top_n=args.top, output_file=args.output)
    
    print(f"Analyzed {total_processed} log entries across {len(args.files)} files")


if __name__ == "__main__":
    main()
