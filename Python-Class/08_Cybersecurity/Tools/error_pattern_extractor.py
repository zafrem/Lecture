#!/usr/bin/env python3
"""
Error Pattern Extractor
---------------------
Extracts and summarizes error and warning patterns from log files.

Input: One or more log files
Output: Summary of errors and warnings categorized by severity and type

Usage:
  python error_pattern_extractor.py --files /var/log/syslog
  python error_pattern_extractor.py --files /var/log/apache2/error.log --format apache
  python error_pattern_extractor.py --files app.log --output error_summary.txt
  python error_pattern_extractor.py --files system.log application.log --severity error warning

Features:
- Automatic error and warning detection
- Severity classification (critical, error, warning, notice)
- Error categorization by type
- Context analysis for related errors
"""

import re
import os
import sys
import argparse
import datetime
import json
from collections import defaultdict, Counter


class ErrorPatternExtractor:
    """Extract and analyze error patterns from log files"""
    
    def __init__(self):
        """Initialize extractor"""
        self.errors = []
        self.stats = {
            'critical': 0,
            'error': 0,
            'warning': 0,
            'notice': 0
        }
        
        # Error patterns by log format
        self.error_patterns = {
            'general': [
                (r'critical|fatal|panic', 'critical'),
                (r'error|exception|fail|failed|failure', 'error'),
                (r'warn|warning', 'warning'),
                (r'notice', 'notice')
            ],
            'syslog': [
                (r'emerg |alert |crit ', 'critical'),
                (r'err ', 'error'),
                (r'warn ', 'warning'),
                (r'notice ', 'notice')
            ],
            'apache': [
                (r'\[emerg\]|\[alert\]|\[crit\]', 'critical'),
                (r'\[error\]', 'error'),
                (r'\[warn\]', 'warning'),
                (r'\[notice\]', 'notice')
            ],
            'nginx': [
                (r'\[emerg\]|\[alert\]|\[crit\]', 'critical'),
                (r'\[error\]', 'error'),
                (r'\[warn\]', 'warning'),
                (r'\[notice\]', 'notice')
            ],
            'python': [
                (r'critical:', 'critical'),
                (r'error:|exception:|traceback', 'error'),
                (r'warning:', 'warning'),
                (r'notice:', 'notice')
            ],
            'java': [
                (r'FATAL |severe', 'critical'),
                (r'ERROR |Exception', 'error'),
                (r'WARN |WARNING', 'warning'),
                (r'INFO ', 'notice')
            ]
        }
        
        # Common error types and their patterns
        self.error_types = {
            'permission': r'permission denied|access denied|not allowed|unauthorized',
            'not_found': r'not found|no such file|does not exist|404|missing',
            'timeout': r'timeout|timed out|expired|too slow|too long',
            'connection': r'connection (failed|refused|reset|closed)|unable to connect|unreachable',
            'auth': r'authentication (failed|error)|invalid (password|credential)|unauthorized|forbidden|403',
            'syntax': r'syntax error|invalid syntax|parse error|malformed|illegal|invalid format',
            'memory': r'out of memory|memory (allocation|exhausted)|memory leak|insufficient memory',
            'disk': r'disk full|no space left|not enough space|io error|input/output error',
            'database': r'database error|sql error|query failed|deadlock|foreign key|constraint violation',
            'config': r'configuration error|invalid config|missing config|unknown option',
            'dependency': r'missing dependency|required module|not installed|no such module',
            'crash': r'crash|abort|terminated|killed|segmentation fault|core dump'
        }
    
    def _extract_timestamp(self, line):
        """Extract timestamp from log line if present"""
        timestamp_patterns = [
            # ISO format: 2023-01-15T14:32:09.123Z
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:?\d{2}|Z)?)',
            # Common log format: 10/Oct/2023:13:55:36 +0000
            r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]',
            # Syslog: Jan 15 14:32:09
            r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
            # Simple date: 2023/01/15 14:32:09
            r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})',
        ]
        
        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        
        return None
    
    def process_file(self, file_path, log_format=None, severity_filter=None):
        """Process a log file and extract error patterns"""
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
                # Simple format detection based on file name and content
                if 'apache' in file_path or 'httpd' in file_path:
                    log_format = 'apache'
                elif 'nginx' in file_path:
                    log_format = 'nginx'
                elif 'syslog' in file_path or 'system' in file_path:
                    log_format = 'syslog'
                elif '.py' in file_path or 'python' in file_path:
                    log_format = 'python'
                elif '.java' in file_path or '.log' in file_path and 'Exception' in ''.join(lines[:100]):
                    log_format = 'java'
                else:
                    log_format = 'general'
                
                print(f"Using log format: {log_format}")
            
            # Process each line
            errors_found = 0
            context = []  # Keep a few lines of context
            context_size = 5  # Number of lines to keep as context
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Add to rolling context
                context.append(line)
                if len(context) > context_size:
                    context.pop(0)
                
                # Check if this is an error line
                severity = self._detect_severity(line, log_format)
                
                # Skip if it doesn't match severity filter
                if severity_filter and severity not in severity_filter:
                    continue
                    
                if severity:
                    # Get timestamp if available
                    timestamp = self._extract_timestamp(line)
                    
                    # Determine error type
                    error_type = self._classify_error_type(line)
                    
                    # Extract relevant part of the error message
                    error_message = self._extract_error_message(line, log_format)
                    
                    # Create error entry
                    error_entry = {
                        'file': os.path.basename(file_path),
                        'line_num': i + 1,
                        'timestamp': timestamp,
                        'severity': severity,
                        'type': error_type,
                        'message': error_message,
                        'line': line,
                        'context': list(context)  # Copy current context
                    }
                    
                    self.errors.append(error_entry)
                    self.stats[severity] += 1
                    errors_found += 1
            
            print(f"Found {errors_found} errors/warnings in {file_path}")
            return errors_found
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0
    
    def _detect_severity(self, line, log_format):
        """Detect the severity of a log line"""
        # Try format-specific patterns first
        if log_format in self.error_patterns:
            for pattern, severity in self.error_patterns[log_format]:
                if re.search(pattern, line, re.IGNORECASE):
                    return severity
        
        # Fall back to general patterns
        for pattern, severity in self.error_patterns['general']:
            if re.search(pattern, line, re.IGNORECASE):
                return severity
        
        return None
    
    def _classify_error_type(self, line):
        """Classify the type of error based on content"""
        for error_type, pattern in self.error_types.items():
            if re.search(pattern, line, re.IGNORECASE):
                return error_type
        
        return 'other'
    
    def _extract_error_message(self, line, log_format):
        """Extract the relevant part of the error message"""
        # Format-specific extractors
        if log_format == 'syslog':
            # Try to extract the message part after program name
            match = re.search(r'^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+[\w\-\.]+\s+([^:]+):\s+(.*)$', line)
            if match:
                return match.group(2)
        elif log_format == 'apache':
            # Extract message after severity indicator
            match = re.search(r'\[(error|warn|notice|crit|alert|emerg)\]\s*(?:\[[^\]]+\]\s*)?(.+)$', line)
            if match:
                return match.group(2)
        elif log_format == 'python':
            # Extract the exception message
            match = re.search(r'(error|exception|warning|critical):\s*(.+)$', line, re.IGNORECASE)
            if match:
                return match.group(2)
        
        # Default: return the whole line
        return line
    
    def group_errors(self):
        """Group errors by type and severity"""
        error_groups = {
            'critical': defaultdict(list),
            'error': defaultdict(list),
            'warning': defaultdict(list),
            'notice': defaultdict(list)
        }
        
        # Group errors by severity and type
        for error in self.errors:
            severity = error['severity']
            error_type = error['type']
            error_groups[severity][error_type].append(error)
        
        return error_groups
    
    def find_error_patterns(self):
        """Find patterns in errors of the same type"""
        patterns = {}
        
        for severity in ['critical', 'error', 'warning', 'notice']:
            patterns[severity] = {}
            
            # Group by error type
            by_type = defaultdict(list)
            for error in [e for e in self.errors if e['severity'] == severity]:
                by_type[error['type']].append(error)
            
            # Find common patterns in each type
            for error_type, errors in by_type.items():
                if not errors:
                    continue
                    
                # Count message occurrences
                message_counts = Counter()
                for error in errors:
                    # Normalize message to find patterns
                    normalized = self._normalize_error_message(error['message'])
                    message_counts[normalized] += 1
                
                # Get most common patterns
                common_patterns = message_counts.most_common(5)
                
                patterns[severity][error_type] = {
                    'count': len(errors),
                    'patterns': common_patterns,
                    'examples': errors[:3]  # Include a few examples
                }
        
        return patterns
    
    def _normalize_error_message(self, message):
        """Normalize error message to identify patterns"""
        # Replace specific values with placeholders
        normalized = message
        
        # Replace file paths
        normalized = re.sub(r'(?<!/)[/\w\.-]+/[/\w\.-]+\.\w+', '<PATH>', normalized)
        
        # Replace numbers
        normalized = re.sub(r'(?<!\w)\d+(?!\w)', '<NUM>', normalized)
        
        # Replace hexadecimal values
        normalized = re.sub(r'0x[0-9a-f]+', '<HEX>', normalized)
        
        # Replace UUIDs and other IDs
        normalized = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', normalized)
        
        # Replace IP addresses
        normalized = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', normalized)
        
        return normalized
    
    def generate_report(self, patterns, output_file=None):
        """Generate a report of the error patterns"""
        report = []
        report.append("=" * 80)
        report.append(f"ERROR PATTERN ANALYSIS REPORT - {datetime.datetime.now().isoformat()}")
        report.append("=" * 80)
        report.append(f"Total issues found: {sum(self.stats.values())}")
        report.append(f"  Critical: {self.stats['critical']}")
        report.append(f"  Error: {self.stats['error']}")
        report.append(f"  Warning: {self.stats['warning']}")
        report.append(f"  Notice: {self.stats['notice']}")
        report.append("")
        
        # Show patterns by severity and type
        for severity in ['critical', 'error', 'warning', 'notice']:
            if self.stats[severity] == 0:
                continue
                
            report.append(f"{severity.upper()} ISSUES ({self.stats[severity]} total)")
            report.append("=" * 40)
            
            # Sort by count
            sorted_types = sorted(
                patterns[severity].items(), 
                key=lambda x: x[1]['count'], 
                reverse=True
            )
            
            for error_type, data in sorted_types:
                report.append(f"\n{error_type.upper()} ({data['count']} occurrences)")
                report.append("-" * 40)
                
                # Show common patterns
                if data['patterns']:
                    report.append("Common patterns:")
                    for pattern, count in data['patterns']:
                        report.append(f"  - {pattern} ({count} occurrences)")
                
                # Show examples
                if data['examples']:
                    report.append("\nExamples:")
                    for i, example in enumerate(data['examples'], 1):
                        report.append(f"  {i}. {example['message'][:100]}" + 
                                    ("..." if len(example['message']) > 100 else ""))
                        if example['timestamp']:
                            report.append(f"     Time: {example['timestamp']}")
                        report.append(f"     File: {example['file']} (Line {example['line_num']})")
                        report.append("")
            
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
    parser = argparse.ArgumentParser(description="Extract and analyze error patterns from log files")
    parser.add_argument('--files', nargs='+', required=True,
                      help="Log file(s) to analyze")
    parser.add_argument('--format', choices=['general', 'syslog', 'apache', 'nginx', 'python', 'java'],
                      help="Log format (auto-detect if not specified)")
    parser.add_argument('--severity', nargs='+', choices=['critical', 'error', 'warning', 'notice'],
                      help="Severity levels to include (default: all)")
    parser.add_argument('--output',
                      help="Output file for the report")
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    
    extractor = ErrorPatternExtractor()
    
    # Process each file
    total_errors = 0
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue
            
        errors = extractor.process_file(
            file_path, 
            log_format=args.format,
            severity_filter=args.severity
        )
        total_errors += errors
    
    if total_errors == 0:
        print("No errors or warnings found. Exiting.")
        sys.exit(0)
    
    # Group errors and find patterns
    patterns = extractor.find_error_patterns()
    
    # Generate report
    extractor.generate_report(patterns, output_file=args.output)
    
    print(f"Analyzed {len(args.files)} log files, found {total_errors} issues")


if __name__ == "__main__":
    main()
