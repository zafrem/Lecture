#!/usr/bin/env python3
"""
Subnet Ping Scanner
------------------
This tool scans a given subnet for live hosts using ICMP echo requests (ping).
Input: Subnet in CIDR notation (e.g., 192.168.1.0/24)
Output: List of live IPs found on the network

Usage:
  python subnet_scanner.py 192.168.1.0/24
  python subnet_scanner.py 10.0.0.0/24 --timeout 0.5 --count 2
  python subnet_scanner.py 172.16.0.0/24 --output live_hosts.txt
  python subnet_scanner.py 192.168.0.0/16 --threads 100

Features:
- Multithreaded scanning for speed
- Adjustable timeout and ping count
- Progress reporting
"""

import argparse
import ipaddress
import subprocess
import sys
import platform
import threading
import time
import queue
import signal
from concurrent.futures import ThreadPoolExecutor

# Graceful exit handling
stop_scan = False

def signal_handler(sig, frame):
    """Handle interrupt signals to stop gracefully"""
    global stop_scan
    print('\nScan interrupted. Stopping gracefully...')
    stop_scan = True

signal.signal(signal.SIGINT, signal_handler)


class SubnetScanner:
    """Scan a subnet for live hosts using ping"""
    
    def __init__(self, subnet, timeout=1.0, count=1, max_threads=50):
        """Initialize with subnet in CIDR notation"""
        self.subnet = subnet
        self.timeout = timeout
        self.count = count
        self.max_threads = max_threads
        self.live_hosts = []
        self.lock = threading.Lock()
        self.total_hosts = 0
        self.scanned_hosts = 0
        self.start_time = 0
        
    def ping_host(self, ip_address):
        """Ping a single host to check if it's online"""
        if stop_scan:
            return
            
        try:
            # Platform-specific ping command construction
            if platform.system().lower() == 'windows':
                # Windows ping command
                params = [
                    'ping', '-n', str(self.count), 
                    '-w', str(int(self.timeout * 1000)), 
                    str(ip_address)
                ]
            else:
                # Unix-like ping command
                params = [
                    'ping', '-c', str(self.count), 
                    '-W', str(int(self.timeout)), 
                    str(ip_address)
                ]
                
            # Run ping command
            result = subprocess.run(
                params,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=self.timeout * self.count + 1
            )
            
            # Check if ping was successful (exit code 0)
            if result.returncode == 0:
                with self.lock:
                    self.live_hosts.append(str(ip_address))
                    print(f"✓ {ip_address} is alive")
                    
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            # Host is not responding
            pass
            
        finally:
            # Update progress counter
            with self.lock:
                self.scanned_hosts += 1
                
                # Calculate and print progress
                progress = self.scanned_hosts / self.total_hosts * 100
                elapsed = time.time() - self.start_time
                
                # Only print status update every 10 hosts or on completion
                if self.scanned_hosts % 10 == 0 or self.scanned_hosts == self.total_hosts:
                    # Calculate ETA
                    if elapsed > 0 and self.scanned_hosts > 0:
                        hosts_per_second = self.scanned_hosts / elapsed
                        remaining_hosts = self.total_hosts - self.scanned_hosts
                        eta_seconds = remaining_hosts / hosts_per_second if hosts_per_second > 0 else 0
                        
                        # Format ETA
                        if eta_seconds < 60:
                            eta = f"{int(eta_seconds)} seconds"
                        elif eta_seconds < 3600:
                            eta = f"{int(eta_seconds / 60)} minutes"
                        else:
                            eta = f"{int(eta_seconds / 3600)} hours"
                            
                        # Print progress
                        sys.stdout.write(f"\rScanning: {self.scanned_hosts}/{self.total_hosts} " 
                                       f"({progress:.1f}%) - Found: {len(self.live_hosts)} - ETA: {eta}")
                    else:
                        sys.stdout.write(f"\rScanning: {self.scanned_hosts}/{self.total_hosts} "
                                       f"({progress:.1f}%) - Found: {len(self.live_hosts)}")
                    sys.stdout.flush()
    
    def scan(self):
        """Scan the subnet for live hosts"""
        try:
            # Parse subnet
            network = ipaddress.ip_network(self.subnet)
            self.total_hosts = network.num_addresses
            
            # Subtract network and broadcast addresses for IPv4
            if isinstance(network, ipaddress.IPv4Network) and self.total_hosts > 2:
                self.total_hosts -= 2  # Exclude network and broadcast addresses
                
            print(f"Starting scan of {self.subnet} ({self.total_hosts} hosts)")
            print(f"Using timeout of {self.timeout}s and {self.count} ping(s) per host")
            
            self.start_time = time.time()
            
            # Create thread pool
            num_threads = min(self.max_threads, self.total_hosts)
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit ping tasks
                for ip in network.hosts():
                    if stop_scan:
                        break
                    executor.submit(self.ping_host, ip)
                    
            # Print final results
            elapsed = time.time() - self.start_time
            print(f"\n\nScan completed in {elapsed:.2f} seconds")
            print(f"Found {len(self.live_hosts)} live hosts in {self.subnet}")
            
            return self.live_hosts
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please provide a valid subnet in CIDR notation (e.g., 192.168.1.0/24)")
            return []


def save_results(hosts, output_file):
    """Save results to a file"""
    try:
        with open(output_file, 'w') as f:
            for host in hosts:
                f.write(f"{host}\n")
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Scan a subnet for live hosts using ping")
    parser.add_argument("subnet", help="Subnet in CIDR notation (e.g., 192.168.1.0/24)")
    parser.add_argument("--timeout", type=float, default=1.0, 
                      help="Timeout in seconds for each ping (default: 1.0)")
    parser.add_argument("--count", type=int, default=1, 
                      help="Number of ping packets to send (default: 1)")
    parser.add_argument("--threads", type=int, default=50, 
                      help="Maximum number of threads (default: 50)")
    parser.add_argument("--output", type=str, 
                      help="Output file to save results")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()
    
    # Create and run scanner
    scanner = SubnetScanner(
        subnet=args.subnet, 
        timeout=args.timeout,
        count=args.count,
        max_threads=args.threads
    )
    
    # Run scan
    live_hosts = scanner.scan()
    
    # Print results
    if live_hosts:
        print("\nLive hosts:")
        for host in live_hosts:
            print(f"  {host}")
            
        # Save results if output file specified
        if args.output:
            save_results(live_hosts, args.output)
    else:
        print("No live hosts found.")
