#!/usr/bin/env python3
"""
Incident Response & Forensics Examples
------------------------------------
This script demonstrates basic incident response and forensics concepts in Python:
1. System event log collection
2. File metadata analysis
3. Timeline creation from system events
4. Basic memory analysis simulation
"""

import os
import sys
import time
import csv
import json
import hashlib
import datetime
import platform
import argparse
import logging
import subprocess
from collections import defaultdict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('ir_forensics')


# ---- 1. System Event Log Collection ----

class LogCollector:
    """Collect and analyze system logs"""
    
    def __init__(self, output_dir="./collected_logs"):
        """Initialize with output directory for collected logs"""
        self.output_dir = output_dir
        self.os_type = platform.system().lower()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    
    def collect_logs(self):
        """Collect system logs based on OS type"""
        logger.info(f"Starting log collection on {self.os_type} system")
        
        if self.os_type == "linux":
            return self._collect_linux_logs()
        elif self.os_type == "darwin":  # macOS
            return self._collect_macos_logs()
        elif self.os_type == "windows":
            return self._collect_windows_logs()
        else:
            logger.error(f"Unsupported operating system: {self.os_type}")
            return False
    
    def _collect_linux_logs(self):
        """Collect logs on Linux systems"""
        log_sources = [
            "/var/log/syslog",
            "/var/log/auth.log",
            "/var/log/secure",
            "/var/log/messages",
            "/var/log/apache2/access.log",
            "/var/log/apache2/error.log"
        ]
        
        collected = []
        
        for source in log_sources:
            if os.path.exists(source):
                try:
                    # Create a timestamped filename for the collected log
                    filename = os.path.basename(source)
                    dest_file = os.path.join(
                        self.output_dir, 
                        f"{filename}_{int(time.time())}.log"
                    )
                    
                    # For demo purposes, we don't actually copy the logs
                    # We'd use shutil.copy2(source, dest_file) in a real situation
                    
                    logger.info(f"Would collect {source} to {dest_file}")
                    collected.append(source)
                except Exception as e:
                    logger.error(f"Error collecting {source}: {e}")
            else:
                logger.info(f"Log source not found: {source}")
        
        return collected
    
    def _collect_macos_logs(self):
        """Collect logs on macOS systems"""
        # For demonstration only
        logger.info("Collecting macOS logs (demonstration)")
        
        # In a real implementation, we would use log command:
        # subprocess.run(["log", "show", "--last", "1d", "--output", os.path.join(self.output_dir, "system_logs.log")])
        
        collected = ["System logs", "Application logs"]
        return collected
    
    def _collect_windows_logs(self):
        """Collect logs on Windows systems"""
        # For demonstration only
        logger.info("Collecting Windows logs (demonstration)")
        
        # In a real implementation, we would use wevtutil or PowerShell:
        # subprocess.run(["wevtutil", "epl", "System", os.path.join(self.output_dir, "system.evtx")])
        # subprocess.run(["wevtutil", "epl", "Security", os.path.join(self.output_dir, "security.evtx")])
        
        collected = ["System logs", "Security logs", "Application logs"]
        return collected
    
    def parse_log(self, log_file, log_type=None):
        """Parse a collected log file (demonstration only)"""
        if not os.path.exists(log_file):
            logger.error(f"Log file does not exist: {log_file}")
            return []
            
        logger.info(f"Parsing log file: {log_file}")
        
        # In a real implementation, we would parse the log based on its format
        # For this demonstration, we'll just read the first few lines
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()[:10]  # First 10 lines
                
            logger.info(f"Read {len(lines)} lines from {log_file}")
            return lines
        except Exception as e:
            logger.error(f"Error parsing log file: {e}")
            return []


# ---- 2. File Metadata Analysis ----

class FileAnalyzer:
    """Analyze file metadata for forensic investigation"""
    
    def __init__(self):
        """Initialize file analyzer"""
        pass
    
    def get_file_metadata(self, filepath):
        """Get comprehensive metadata for a file"""
        if not os.path.exists(filepath):
            logger.error(f"File does not exist: {filepath}")
            return {}
            
        try:
            # Get file stats
            file_stat = os.stat(filepath)
            
            # Calculate file hashes
            md5_hash = self._get_file_hash(filepath, 'md5')
            sha256_hash = self._get_file_hash(filepath, 'sha256')
            
            # Get file type (basic implementation)
            file_type = self._guess_file_type(filepath)
            
            # Compile metadata
            metadata = {
                'filename': os.path.basename(filepath),
                'path': os.path.abspath(filepath),
                'size': file_stat.st_size,
                'created_time': datetime.datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified_time': datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'accessed_time': datetime.datetime.fromtimestamp(file_stat.st_atime).isoformat(),
                'permissions': oct(file_stat.st_mode)[-3:],
                'owner_id': file_stat.st_uid,
                'group_id': file_stat.st_gid,
                'md5': md5_hash,
                'sha256': sha256_hash,
                'file_type': file_type
            }
            
            return metadata
        except Exception as e:
            logger.error(f"Error getting metadata for {filepath}: {e}")
            return {}
    
    def _get_file_hash(self, filepath, hash_type='md5'):
        """Calculate file hash"""
        hash_funcs = {
            'md5': hashlib.md5(),
            'sha1': hashlib.sha1(),
            'sha256': hashlib.sha256()
        }
        
        if hash_type not in hash_funcs:
            return "Unsupported hash type"
            
        h = hash_funcs[hash_type]
        
        try:
            with open(filepath, 'rb') as f:
                # Read in chunks for large files
                chunk = f.read(8192)
                while chunk:
                    h.update(chunk)
                    chunk = f.read(8192)
                    
            return h.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating {hash_type} hash: {e}")
            return "Error calculating hash"
    
    def _guess_file_type(self, filepath):
        """Guess file type based on extension and content"""
        # Check extension first
        extension = os.path.splitext(filepath)[1].lower()
        
        # Map common extensions to types
        extension_map = {
            '.txt': 'Text file',
            '.log': 'Log file',
            '.pdf': 'PDF document',
            '.doc': 'Word document',
            '.docx': 'Word document',
            '.xls': 'Excel spreadsheet',
            '.xlsx': 'Excel spreadsheet',
            '.ppt': 'PowerPoint presentation',
            '.pptx': 'PowerPoint presentation',
            '.zip': 'ZIP archive',
            '.tar': 'TAR archive',
            '.gz': 'GZip archive',
            '.exe': 'Windows executable',
            '.dll': 'Windows library',
            '.py': 'Python script',
            '.sh': 'Shell script',
            '.jpg': 'JPEG image',
            '.png': 'PNG image',
            '.gif': 'GIF image',
            '.mp3': 'MP3 audio',
            '.mp4': 'MP4 video'
        }
        
        if extension in extension_map:
            return extension_map[extension]
            
        # If extension not recognized, try to determine from content
        try:
            with open(filepath, 'rb') as f:
                header = f.read(8)  # Read first 8 bytes
                
            # Check common file signatures
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'PNG image'
            elif header.startswith(b'\xff\xd8'):
                return 'JPEG image'
            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                return 'GIF image'
            elif header.startswith(b'%PDF'):
                return 'PDF document'
            elif header.startswith(b'PK\x03\x04'):
                return 'ZIP archive'
            elif header.startswith(b'\x7fELF'):
                return 'ELF binary'
            elif header.startswith(b'MZ'):
                return 'Windows executable'
            
            # Try to detect text files
            try:
                with open(filepath, 'r') as f:
                    f.read(1024)  # Try to read as text
                return 'Text file'
            except UnicodeDecodeError:
                return 'Binary data'
                
        except Exception:
            return 'Unknown'
    
    def analyze_directory(self, directory_path, recursive=True):
        """Analyze all files in a directory"""
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            logger.error(f"Directory does not exist: {directory_path}")
            return []
            
        results = []
        
        # Walk through directory
        for root, _, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                metadata = self.get_file_metadata(filepath)
                if metadata:
                    results.append(metadata)
            
            # If not recursive, break after first level
            if not recursive:
                break
                
        return results


# ---- 3. Timeline Creation ----

class TimelineCreator:
    """Create timeline from system events and file metadata"""
    
    def __init__(self):
        """Initialize timeline creator"""
        self.events = []
    
    def add_file_events(self, file_metadata_list):
        """Add file metadata to timeline"""
        for metadata in file_metadata_list:
            # Add file creation event
            self.events.append({
                'timestamp': metadata.get('created_time'),
                'source': 'file',
                'event_type': 'file_created',
                'description': f"File created: {metadata.get('filename')}",
                'path': metadata.get('path'),
                'metadata': metadata
            })
            
            # Add file modification event
            self.events.append({
                'timestamp': metadata.get('modified_time'),
                'source': 'file',
                'event_type': 'file_modified',
                'description': f"File modified: {metadata.get('filename')}",
                'path': metadata.get('path'),
                'metadata': metadata
            })
    
    def add_log_events(self, log_events):
        """Add parsed log events to timeline"""
        for event in log_events:
            self.events.append({
                'timestamp': event.get('timestamp'),
                'source': event.get('source', 'log'),
                'event_type': event.get('type', 'log_entry'),
                'description': event.get('message', 'Unknown log entry'),
                'metadata': event
            })
    
    def generate_timeline(self):
        """Generate timeline from collected events"""
        # Sort events by timestamp
        sorted_events = sorted(self.events, key=lambda x: x.get('timestamp', ''))
        
        return sorted_events
    
    def export_timeline_csv(self, output_file):
        """Export timeline to CSV file"""
        if not self.events:
            logger.warning("No events to export")
            return False
            
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Timestamp', 'Source', 'Event Type', 'Description', 'Path/Info'])
                
                # Write events
                for event in self.generate_timeline():
                    writer.writerow([
                        event.get('timestamp', ''),
                        event.get('source', ''),
                        event.get('event_type', ''),
                        event.get('description', ''),
                        event.get('path', '')
                    ])
                    
            logger.info(f"Timeline exported to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error exporting timeline: {e}")
            return False
    
    def export_timeline_json(self, output_file):
        """Export timeline to JSON file"""
        if not self.events:
            logger.warning("No events to export")
            return False
            
        try:
            with open(output_file, 'w') as f:
                json.dump(self.generate_timeline(), f, indent=2)
                
            logger.info(f"Timeline exported to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error exporting timeline: {e}")
            return False


# ---- 4. Memory Analysis Simulation ----

class MemoryAnalysisSimulator:
    """Simulate memory analysis techniques (for educational purposes)"""
    
    def __init__(self):
        """Initialize memory analyzer"""
        self.analysis_results = {}
    
    def list_running_processes(self):
        """List running processes (basic implementation)"""
        processes = []
        
        try:
            if platform.system() == 'Windows':
                # Windows implementation
                output = subprocess.check_output(['tasklist', '/fo', 'csv'], 
                                               universal_newlines=True)
                for line in output.splitlines()[1:]:  # Skip header
                    if not line.strip():
                        continue
                        
                    parts = line.split('","')
                    if len(parts) >= 2:
                        name = parts[0].strip('"')
                        pid = parts[1].strip('"')
                        processes.append({
                            'name': name,
                            'pid': pid
                        })
            else:
                # Unix-like implementation
                output = subprocess.check_output(['ps', 'aux'], 
                                               universal_newlines=True)
                for line in output.splitlines()[1:]:  # Skip header
                    parts = line.split(None, 10)
                    if len(parts) >= 2:
                        user = parts[0]
                        pid = parts[1]
                        cpu = parts[2]
                        mem = parts[3]
                        cmd = parts[10] if len(parts) > 10 else ""
                        processes.append({
                            'user': user,
                            'pid': pid,
                            'cpu': cpu,
                            'mem': mem,
                            'command': cmd
                        })
        except Exception as e:
            logger.error(f"Error listing processes: {e}")
            
        return processes
    
    def simulate_memory_dump(self, output_file="memory_dump_simulation.bin"):
        """Simulate a memory dump (for educational purposes only)"""
        logger.info("Simulating memory dump (this is a demo and does not create a real dump)")
        
        try:
            # In a real scenario, we would use tools like:
            # - Windows: procdump, winpmem
            # - Linux: LiME, /proc/kcore
            # - macOS: osxpmem
            
            # For the demo, create a small fake "dump" file
            with open(output_file, 'wb') as f:
                # Write some random data as an example
                f.write(os.urandom(1024))  # 1KB of random data
                
            logger.info(f"Created simulated memory dump: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error creating simulated dump: {e}")
            return None
    
    def simulate_memory_analysis(self, dump_file=None):
        """Simulate memory analysis (for educational purposes)"""
        logger.info("Simulating memory analysis (educational demonstration only)")
        
        # In a real scenario, we would use tools like Volatility
        
        # Simulated findings
        findings = [
            {
                'type': 'suspicious_process',
                'details': {
                    'name': 'malware.exe',
                    'pid': '1234',
                    'path': 'C:\\Windows\\Temp\\malware.exe',
                    'signatures': ['Creates registry run keys', 'Connects to known C2 server']
                }
            },
            {
                'type': 'network_connection',
                'details': {
                    'local_addr': '192.168.1.5:49152',
                    'remote_addr': '203.0.113.42:443',
                    'state': 'ESTABLISHED',
                    'process': 'explorer.exe'
                }
            },
            {
                'type': 'injected_code',
                'details': {
                    'process': 'svchost.exe',
                    'pid': '2345',
                    'technique': 'Process hollowing',
                    'indicators': ['Unmapped memory sections', 'Modified entry point']
                }
            }
        ]
        
        logger.info(f"Analysis complete. Found {len(findings)} suspicious items.")
        return findings
    
    def list_open_files(self):
        """List open files (basic implementation)"""
        open_files = []
        
        try:
            if platform.system() != 'Windows':
                # Unix-like implementation using lsof
                output = subprocess.check_output(['lsof'], 
                                               universal_newlines=True)
                for line in output.splitlines()[1:]:  # Skip header
                    parts = line.split(None, 8)
                    if len(parts) >= 8:
                        command = parts[0]
                        pid = parts[1]
                        user = parts[2]
                        fd = parts[3]
                        file_path = parts[8] if len(parts) > 8 else ""
                        
                        open_files.append({
                            'command': command,
                            'pid': pid,
                            'user': user,
                            'fd': fd,
                            'path': file_path
                        })
            else:
                # Windows doesn't have a direct equivalent to lsof
                # For demo purposes only
                logger.info("File handle listing not implemented for Windows in this demo")
                
        except Exception as e:
            logger.error(f"Error listing open files: {e}")
            
        return open_files


# ---- Demo ----

def demonstrate_incident_response():
    print("===== INCIDENT RESPONSE & FORENSICS DEMO =====\n")
    
    # 1. System Event Log Collection
    print("1. System Event Log Collection Demo")
    collector = LogCollector("./ir_demo_logs")
    collector.collect_logs()
    print("")
    
    # 2. File Metadata Analysis
    print("2. File Metadata Analysis Demo")
    analyzer = FileAnalyzer()
    
    # Find some files to analyze
    demo_files = []
    for root, _, files in os.walk(".", topdown=True, followlinks=False):
        for name in files:
            if name.endswith(".py"):
                demo_files.append(os.path.join(root, name))
                if len(demo_files) >= 3:  # Limit to 3 files for demo
                    break
        if len(demo_files) >= 3:
            break
    
    file_metadata = []
    for file_path in demo_files:
        print(f"\nAnalyzing file: {file_path}")
        metadata = analyzer.get_file_metadata(file_path)
        if metadata:
            file_metadata.append(metadata)
            print(f"  Type: {metadata.get('file_type')}")
            print(f"  Size: {metadata.get('size')} bytes")
            print(f"  Created: {metadata.get('created_time')}")
            print(f"  Modified: {metadata.get('modified_time')}")
            print(f"  MD5: {metadata.get('md5')}")
    print("")
    
    # 3. Timeline Creation
    print("3. Timeline Creation Demo")
    timeline = TimelineCreator()
    
    # Add file events to timeline
    timeline.add_file_events(file_metadata)
    
    # Add some simulated log events
    log_events = [
        {
            'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(),
            'source': 'auth.log',
            'type': 'authentication',
            'message': 'Failed login attempt for user admin from 203.0.113.42'
        },
        {
            'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=30)).isoformat(),
            'source': 'auth.log',
            'type': 'authentication',
            'message': 'Successful login for user john from 192.168.1.5'
        },
        {
            'timestamp': datetime.datetime.now().isoformat(),
            'source': 'system.log',
            'type': 'system',
            'message': 'System shutdown initiated by user john'
        }
    ]
    timeline.add_log_events(log_events)
    
    # Generate and display timeline
    events = timeline.generate_timeline()
    print(f"Generated timeline with {len(events)} events")
    
    # Export timeline
    timeline.export_csv = "incident_timeline.csv"
    timeline.export_json = "incident_timeline.json"
    print("")
    
    # 4. Memory Analysis Simulation
    print("4. Memory Analysis Simulation Demo")
    memory_analyzer = MemoryAnalysisSimulator()
    
    # List processes
    processes = memory_analyzer.list_running_processes()
    if processes:
        print(f"\nRunning processes ({len(processes)}):")
        for i, proc in enumerate(processes[:5]):  # Show only first 5
            if 'command' in proc:
                print(f"  {i+1}. {proc.get('pid', 'N/A')}: {proc.get('command', 'Unknown')[:50]}")
            else:
                print(f"  {i+1}. {proc.get('pid', 'N/A')}: {proc.get('name', 'Unknown')}")
        
        if len(processes) > 5:
            print(f"  ...and {len(processes) - 5} more processes")
    
    # Simulate memory analysis
    print("\nSimulating memory analysis...")
    dump_file = memory_analyzer.simulate_memory_dump()
    if dump_file:
        findings = memory_analyzer.simulate_memory_analysis(dump_file)
        
        print("\nSimulated findings:")
        for finding in findings:
            print(f"  Type: {finding['type']}")
            if finding['type'] == 'suspicious_process':
                details = finding['details']
                print(f"  Process: {details['name']} (PID: {details['pid']})")
                print(f"  Signatures: {', '.join(details['signatures'])}")
            elif finding['type'] == 'network_connection':
                details = finding['details']
                print(f"  Connection: {details['local_addr']} -> {details['remote_addr']} ({details['state']})")
                print(f"  Process: {details['process']}")
            print("")
            
        # Cleanup
        if os.path.exists(dump_file):
            os.remove(dump_file)
            

if __name__ == "__main__":
    demonstrate_incident_response()
