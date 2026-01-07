#!/usr/bin/env python3
"""
Time-Based Log Visualizer
------------------------
Analyzes logs over time and visualizes patterns, trends, and anomalies.

Input: One or more log files
Output: Time-based visualization and analysis of log activity

Usage:
  python time_based_log_visualizer.py --files /var/log/syslog
  python time_based_log_visualizer.py --files /var/log/apache2/access.log --format apache
  python time_based_log_visualizer.py --files app.log --output activity_report.html
  python time_based_log_visualizer.py --files system.log --time-window hourly

Features:
- Parses timestamps from various log formats
- Visualizes log activity over time
- Detects activity spikes and anomalies
- Generates HTML reports with interactive charts
- Groups logs by severity and type over time
"""

import re
import os
import sys
import argparse
import datetime
from collections import defaultdict, Counter
import json
import math
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


class TimeBasedLogVisualizer:
    """Analyze logs over time and visualize patterns"""
    
    def __init__(self):
        """Initialize visualizer"""
        self.logs = []
        self.time_windows = {
            'minute': timedelta(minutes=1),
            'hourly': timedelta(hours=1),
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1)
        }
        
        # Timestamp patterns for various log formats
        self.timestamp_patterns = [
            # ISO format: 2023-01-15T14:32:09.123Z
            (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:?\d{2}|Z)?)',
             '%Y-%m-%dT%H:%M:%S'),
            # Common log format: 10/Oct/2023:13:55:36 +0000
            (r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]',
             '%d/%b/%Y:%H:%M:%S %z'),
            # Syslog: Jan 15 14:32:09
            (r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
             '%b %d %H:%M:%S'),
            # Simple date: 2023/01/15 14:32:09
            (r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})',
             '%Y/%m/%d %H:%M:%S'),
            # Simple date with dash: 2023-01-15 14:32:09
            (r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
             '%Y-%m-%d %H:%M:%S'),
        ]
        
        # Severity patterns
        self.severity_patterns = {
            'critical': r'critical|fatal|panic|emerg|alert|crit|\[crit\]|\[fatal\]|\[emerg\]',
            'error': r'error|exception|fail|failed|failure|\[error\]|err',
            'warning': r'warn|warning|\[warn\]',
            'info': r'info|notice|information|\[info\]|\[notice\]',
            'debug': r'debug|\[debug\]'
        }
    
    def process_file(self, file_path, log_format=None, year=None):
        """Process a log file and extract timestamped entries"""
        print(f"Processing {file_path}...")
        
        try:
            # Read the file
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                
            if not lines:
                print(f"Warning: {file_path} is empty")
                return 0
            
            # Process each line
            logs_found = 0
            current_year = year or datetime.datetime.now().year
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Extract timestamp
                timestamp, dt = self._extract_timestamp(line, current_year)
                
                if dt:
                    # Determine severity
                    severity = self._detect_severity(line)
                    
                    # Create log entry
                    log_entry = {
                        'file': os.path.basename(file_path),
                        'line_num': i + 1,
                        'timestamp': timestamp,
                        'datetime': dt,
                        'severity': severity,
                        'line': line[:200]  # Truncate long lines
                    }
                    
                    self.logs.append(log_entry)
                    logs_found += 1
            
            print(f"Found {logs_found} timestamped entries in {file_path}")
            return logs_found
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0
    
    def _extract_timestamp(self, line, current_year=None):
        """Extract timestamp from log line and parse to datetime"""
        for pattern, date_format in self.timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                timestamp_str = match.group(1)
                try:
                    # Special handling for syslog format which may not include year
                    if '%Y' not in date_format and current_year:
                        dt = datetime.datetime.strptime(timestamp_str, date_format)
                        dt = dt.replace(year=current_year)
                    else:
                        dt = datetime.datetime.strptime(timestamp_str, date_format)
                    return timestamp_str, dt
                except ValueError:
                    # If parsing fails, try the next pattern
                    pass
        
        return None, None
    
    def _detect_severity(self, line):
        """Detect the severity level of a log line"""
        line_lower = line.lower()
        
        for severity, pattern in self.severity_patterns.items():
            if re.search(pattern, line_lower):
                return severity
        
        return 'info'  # Default severity
    
    def analyze_time_distribution(self, time_window='hourly'):
        """Analyze the distribution of logs over time"""
        if not self.logs:
            print("No logs to analyze")
            return None
            
        # Sort logs by time
        sorted_logs = sorted(self.logs, key=lambda x: x['datetime'])
        
        # Get time window delta
        delta = self.time_windows.get(time_window, self.time_windows['hourly'])
        
        # Group logs by time window
        time_groups = defaultdict(list)
        severity_counts = defaultdict(lambda: defaultdict(int))
        
        for log in sorted_logs:
            # Round time to the nearest window
            if time_window == 'minute':
                window_time = log['datetime'].replace(second=0, microsecond=0)
            elif time_window == 'hourly':
                window_time = log['datetime'].replace(minute=0, second=0, microsecond=0)
            elif time_window == 'daily':
                window_time = log['datetime'].replace(hour=0, minute=0, second=0, microsecond=0)
            elif time_window == 'weekly':
                # Find the start of the week (Monday)
                weekday = log['datetime'].weekday()
                window_time = (log['datetime'] - timedelta(days=weekday)).replace(
                    hour=0, minute=0, second=0, microsecond=0)
            else:
                window_time = log['datetime']
            
            time_groups[window_time].append(log)
            severity_counts[window_time][log['severity']] += 1
        
        # Calculate statistics
        stats = {
            'start_time': min(time_groups.keys()),
            'end_time': max(time_groups.keys()),
            'total_windows': len(time_groups),
            'window_counts': {t.isoformat(): len(logs) for t, logs in time_groups.items()},
            'severity_counts': {t.isoformat(): counts for t, counts in severity_counts.items()},
            'time_windows': list(time_groups.keys()),
            'counts': [len(logs) for logs in time_groups.values()]
        }
        
        # Find anomalies and spikes
        if len(stats['counts']) > 1:
            mean_count = sum(stats['counts']) / len(stats['counts'])
            std_dev = math.sqrt(sum((x - mean_count) ** 2 for x in stats['counts']) / len(stats['counts']))
            
            # Consider windows with counts > mean + 2*std_dev as spikes
            threshold = mean_count + 2 * std_dev
            
            spikes = []
            for time, count in zip(stats['time_windows'], stats['counts']):
                if count > threshold:
                    spikes.append((time, count))
            
            stats['mean_count'] = mean_count
            stats['std_dev'] = std_dev
            stats['threshold'] = threshold
            stats['spikes'] = spikes
            
        return stats
    
    def generate_visualizations(self, stats, output_prefix='log_activity'):
        """Generate visualizations based on time analysis"""
        if not stats or not stats['time_windows']:
            print("No data to visualize")
            return False
            
        try:
            # Time series of log activity
            plt.figure(figsize=(12, 6))
            plt.plot(stats['time_windows'], stats['counts'])
            plt.title('Log Activity Over Time')
            plt.xlabel('Time')
            plt.ylabel('Number of Log Entries')
            plt.grid(True)
            
            # Format x-axis based on time span
            time_span = stats['end_time'] - stats['start_time']
            if time_span.days > 30:
                plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            elif time_span.days > 1:
                plt.gca().xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
            else:
                plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
                
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Add threshold line if available
            if 'threshold' in stats:
                plt.axhline(y=stats['threshold'], color='r', linestyle='--', label='Anomaly Threshold')
                plt.legend()
            
            # Mark spikes if available
            if 'spikes' in stats and stats['spikes']:
                spike_times, spike_counts = zip(*stats['spikes'])
                plt.plot(spike_times, spike_counts, 'ro', label='Activity Spikes')
                plt.legend()
            
            # Save figure
            activity_file = f"{output_prefix}_activity.png"
            plt.savefig(activity_file)
            print(f"Saved activity chart to {activity_file}")
            
            # Severity distribution if we have severity data
            if 'severity_counts' in stats and stats['severity_counts']:
                # Prepare data for stacked area chart
                times = sorted(stats['time_windows'])
                severities = ['critical', 'error', 'warning', 'info', 'debug']
                
                # Create data arrays
                severity_data = {}
                for severity in severities:
                    severity_data[severity] = []
                    
                for time in times:
                    time_iso = time.isoformat()
                    for severity in severities:
                        severity_data[severity].append(
                            stats['severity_counts'].get(time_iso, {}).get(severity, 0)
                        )
                
                # Plot stacked area chart
                plt.figure(figsize=(12, 6))
                plt.stackplot(times, 
                            [severity_data[s] for s in severities],
                            labels=severities,
                            colors=['darkred', 'red', 'orange', 'green', 'blue'])
                
                plt.title('Log Severity Distribution Over Time')
                plt.xlabel('Time')
                plt.ylabel('Number of Log Entries')
                plt.legend(loc='upper left')
                plt.grid(True)
                
                # Format x-axis based on time span
                if time_span.days > 30:
                    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
                elif time_span.days > 1:
                    plt.gca().xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
                else:
                    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
                    
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Save figure
                severity_file = f"{output_prefix}_severity.png"
                plt.savefig(severity_file)
                print(f"Saved severity distribution chart to {severity_file}")
            
            return True
            
        except Exception as e:
            print(f"Error generating visualizations: {e}")
            return False
    
    def generate_html_report(self, stats, output_file='log_activity_report.html'):
        """Generate an HTML report with the time analysis and visualizations"""
        if not stats:
            print("No data for HTML report")
            return False
            
        try:
            # Generate visualizations first
            output_prefix = os.path.splitext(output_file)[0]
            self.generate_visualizations(stats, output_prefix)
            
            # Basic HTML template
            html = [
                '<!DOCTYPE html>',
                '<html>',
                '<head>',
                '  <title>Log Activity Report</title>',
                '  <style>',
                '    body { font-family: Arial, sans-serif; margin: 20px; }',
                '    h1, h2 { color: #333; }',
                '    .container { max-width: 1200px; margin: 0 auto; }',
                '    .chart { margin: 20px 0; text-align: center; }',
                '    .chart img { max-width: 100%; }',
                '    .stats { margin: 20px 0; }',
                '    .stats table { border-collapse: collapse; width: 100%; }',
                '    .stats th, .stats td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
                '    .stats th { background-color: #f2f2f2; }',
                '    .spikes { color: red; font-weight: bold; }',
                '  </style>',
                '</head>',
                '<body>',
                '  <div class="container">',
                f'    <h1>Log Activity Report</h1>',
                f'    <p>Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
                
                '    <div class="stats">',
                '      <h2>Analysis Summary</h2>',
                '      <table>',
                '        <tr><th>Metric</th><th>Value</th></tr>',
                f'        <tr><td>Time Range</td><td>{stats["start_time"]} to {stats["end_time"]}</td></tr>',
                f'        <tr><td>Total Time Windows</td><td>{stats["total_windows"]}</td></tr>'
            ]
            
            # Add statistics if available
            if 'mean_count' in stats:
                html.extend([
                    f'        <tr><td>Average Logs per Window</td><td>{stats["mean_count"]:.2f}</td></tr>',
                    f'        <tr><td>Standard Deviation</td><td>{stats["std_dev"]:.2f}</td></tr>',
                    f'        <tr><td>Anomaly Threshold</td><td>{stats["threshold"]:.2f}</td></tr>',
                    f'        <tr><td>Number of Anomalies/Spikes</td><td>{len(stats["spikes"])}</td></tr>'
                ])
            
            html.append('      </table>')
            
            # Add spikes table if available
            if 'spikes' in stats and stats['spikes']:
                html.extend([
                    '      <h2>Activity Spikes</h2>',
                    '      <table>',
                    '        <tr><th>Time</th><th>Log Count</th></tr>'
                ])
                
                for time, count in stats['spikes']:
                    html.append(f'        <tr><td>{time}</td><td class="spikes">{count}</td></tr>')
                
                html.append('      </table>')
            
            html.extend([
                '    </div>',
                
                '    <div class="chart">',
                '      <h2>Log Activity Over Time</h2>',
                f'      <img src="{output_prefix}_activity.png" alt="Log Activity Chart">',
                '    </div>'
            ])
            
            # Add severity chart if available
            if os.path.exists(f"{output_prefix}_severity.png"):
                html.extend([
                    '    <div class="chart">',
                    '      <h2>Log Severity Distribution</h2>',
                    f'      <img src="{output_prefix}_severity.png" alt="Severity Distribution Chart">',
                    '    </div>'
                ])
            
            html.extend([
                '  </div>',
                '</body>',
                '</html>'
            ])
            
            # Write HTML file
            with open(output_file, 'w') as f:
                f.write('\n'.join(html))
                
            print(f"HTML report saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error generating HTML report: {e}")
            return False


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze log files over time and visualize patterns")
    parser.add_argument('--files', nargs='+', required=True,
                      help="Log file(s) to analyze")
    parser.add_argument('--format', choices=['syslog', 'apache', 'nginx', 'custom'],
                      help="Log format (auto-detect if not specified)")
    parser.add_argument('--time-window', choices=['minute', 'hourly', 'daily', 'weekly'],
                      default='hourly',
                      help="Time window for grouping logs")
    parser.add_argument('--output',
                      default='log_activity_report.html',
                      help="Output HTML report file")
    parser.add_argument('--year', type=int,
                      help="Year to use for logs without year information")
    return parser.parse_args()


def main():
    """Main function"""
    try:
        # Check if matplotlib is available
        import matplotlib
        print(f"Using matplotlib version {matplotlib.__version__}")
    except ImportError:
        print("Error: This tool requires matplotlib.")
        print("Please install it using: pip install matplotlib")
        sys.exit(1)
    
    args = parse_arguments()
    
    visualizer = TimeBasedLogVisualizer()
    
    # Process each file
    total_logs = 0
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            continue
            
        logs = visualizer.process_file(
            file_path,
            log_format=args.format,
            year=args.year
        )
        total_logs += logs
    
    if total_logs == 0:
        print("No timestamped log entries were found. Exiting.")
        sys.exit(1)
    
    # Analyze time distribution
    print(f"Analyzing {total_logs} log entries with {args.time_window} time windows...")
    stats = visualizer.analyze_time_distribution(time_window=args.time_window)
    
    if not stats:
        print("Could not analyze time distribution. Exiting.")
        sys.exit(1)
    
    # Generate HTML report
    visualizer.generate_html_report(stats, output_file=args.output)
    
    print(f"Analyzed {total_logs} log entries across {len(args.files)} files")
    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
