#!/usr/bin/env python3
"""
Infrastructure & Configuration Security Examples
----------------------------------------------
This script demonstrates basic infrastructure and configuration security concepts:
1. File permission checker
2. Open port scanner
3. Basic Docker image security checker
4. Simple AWS security configuration checker
"""

import os
import stat
import socket
import json
import subprocess
from pathlib import Path
import platform
import docker

# Optional imports - used if available
try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False


# ---- 1. File Permission Checker ----

class FilePermissionChecker:
    """Check file permissions for security issues"""
    
    def __init__(self, target_dir="."):
        """Initialize with target directory"""
        self.target_dir = target_dir
        self.issues = []
    
    def check_permissions(self, check_world_writable=True, check_setuid=True,
                         check_executable=True):
        """Check for insecure file permissions"""
        print(f"Checking file permissions in {self.target_dir}...")
        
        # Scan the directory
        for root, dirs, files in os.walk(self.target_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    # Get file stats
                    file_stat = os.stat(filepath)
                    file_mode = file_stat.st_mode
                    
                    # Check for world-writable files
                    if check_world_writable and file_mode & stat.S_IWOTH:
                        self.issues.append({
                            'file': filepath,
                            'issue': 'World-writable',
                            'mode': oct(file_mode)[-3:],
                            'risk': 'high'
                        })
                    
                    # Check for setuid/setgid
                    if check_setuid:
                        if file_mode & stat.S_ISUID:
                            self.issues.append({
                                'file': filepath,
                                'issue': 'SetUID',
                                'mode': oct(file_mode)[-3:],
                                'risk': 'high'
                            })
                        elif file_mode & stat.S_ISGID:
                            self.issues.append({
                                'file': filepath,
                                'issue': 'SetGID',
                                'mode': oct(file_mode)[-3:],
                                'risk': 'medium'
                            })
                    
                    # Check for executable scripts
                    if check_executable and file_mode & stat.S_IXUSR:
                        file_ext = os.path.splitext(filename)[1].lower()
                        if file_ext in ['.sh', '.py', '.pl', '.rb']:
                            self.issues.append({
                                'file': filepath,
                                'issue': 'Executable script',
                                'mode': oct(file_mode)[-3:],
                                'risk': 'info'
                            })
                            
                except (PermissionError, FileNotFoundError) as e:
                    print(f"Error accessing {filepath}: {e}")
        
        return self.issues
    
    def report_issues(self):
        """Print a summary of permission issues"""
        if not self.issues:
            print("No permission issues found.")
            return
            
        print(f"\nFound {len(self.issues)} permission issues:")
        
        # Group by issue type
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue['issue']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        # Print summary by type
        for issue_type, issues in issues_by_type.items():
            print(f"\n{issue_type} files ({len(issues)}):")
            for issue in issues[:5]:  # Limit to 5 examples
                print(f"  {issue['file']} (mode: {issue['mode']}, risk: {issue['risk']})")
            
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")


# ---- 2. Open Port Scanner ----

class LocalPortScanner:
    """Scan local system for open ports"""
    
    def __init__(self):
        """Initialize port scanner"""
        self.open_ports = []
        self.common_services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            115: "SFTP",
            135: "RPC",
            139: "NetBIOS",
            143: "IMAP",
            194: "IRC",
            443: "HTTPS",
            445: "SMB",
            1433: "MSSQL",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Alt"
        }
    
    def scan_ports(self, start_port=1, end_port=1024):
        """Scan local system for open ports"""
        print(f"Scanning local system for open ports ({start_port}-{end_port})...")
        
        self.open_ports = []
        
        for port in range(start_port, end_port + 1):
            try:
                # Create socket and try to connect to localhost
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                result = s.connect_ex(('127.0.0.1', port))
                s.close()
                
                # If port is open
                if result == 0:
                    service = self.common_services.get(port, "Unknown")
                    self.open_ports.append({
                        'port': port,
                        'service': service
                    })
                    print(f"Found open port {port} ({service})")
            except:
                pass
        
        print(f"Scan complete. Found {len(self.open_ports)} open ports.")
        return self.open_ports
    
    def get_listening_processes(self):
        """Get processes listening on ports (platform specific)"""
        listening = []
        
        try:
            if platform.system() == 'Linux' or platform.system() == 'Darwin':
                # Use netstat on Linux/macOS
                cmd = ['netstat', '-tulnp']
                if platform.system() == 'Darwin':  # macOS doesn't support -p
                    cmd = ['netstat', '-tuln']
                    
                output = subprocess.check_output(cmd, universal_newlines=True)
                print("\nListening processes:")
                print(output)
            elif platform.system() == 'Windows':
                # Use netstat on Windows
                output = subprocess.check_output(['netstat', '-ano'], universal_newlines=True)
                print("\nListening processes:")
                print(output)
            else:
                print(f"Unsupported platform: {platform.system()}")
        except subprocess.SubprocessError as e:
            print(f"Error running command: {e}")
            
        return listening


# ---- 3. Docker Security Scanner ----

class DockerSecurityScanner:
    """Basic Docker image security checker"""
    
    def __init__(self):
        """Initialize Docker client if available"""
        try:
            self.client = docker.from_env()
            self.available = True
        except Exception as e:
            print(f"Docker not available: {e}")
            self.available = False
    
    def list_images(self):
        """List available Docker images"""
        if not self.available:
            return []
            
        try:
            return self.client.images.list()
        except docker.errors.APIError as e:
            print(f"Docker API error: {e}")
            return []
    
    def check_image(self, image_name):
        """Check a Docker image for basic security issues"""
        if not self.available:
            print("Docker not available")
            return {}
            
        security_issues = []
        
        try:
            # Pull image if not available
            try:
                image = self.client.images.get(image_name)
            except docker.errors.ImageNotFound:
                print(f"Image {image_name} not found locally. Pulling...")
                image = self.client.images.pull(image_name)
            
            # Get image details
            image_details = {
                'id': image.id,
                'tags': image.tags,
                'created': image.attrs['Created'],
                'size': image.attrs['Size'] / (1024*1024),  # MB
            }
            
            print(f"\nImage: {image_name}")
            print(f"ID: {image_details['id']}")
            print(f"Created: {image_details['created']}")
            print(f"Size: {image_details['size']:.1f} MB")
            
            # Check if image is running as root
            try:
                config = image.attrs['Config']
                if 'User' not in config or not config['User']:
                    security_issues.append({
                        'issue': 'Running as root',
                        'description': 'Image runs as root by default',
                        'severity': 'high'
                    })
            except KeyError:
                pass
            
            # Check exposed ports
            try:
                exposed_ports = image.attrs['Config'].get('ExposedPorts', {})
                if exposed_ports:
                    ports_list = list(exposed_ports.keys())
                    security_issues.append({
                        'issue': 'Exposed ports',
                        'description': f"Image exposes ports: {', '.join(ports_list)}",
                        'severity': 'medium'
                    })
            except KeyError:
                pass
                
            # Check if image has health check
            try:
                if 'Healthcheck' not in image.attrs['Config']:
                    security_issues.append({
                        'issue': 'No healthcheck',
                        'description': 'Image does not define a healthcheck',
                        'severity': 'low'
                    })
            except KeyError:
                pass
            
            # Report issues
            if security_issues:
                print("\nSecurity Issues:")
                for issue in security_issues:
                    print(f"- [{issue['severity'].upper()}] {issue['issue']}: {issue['description']}")
            else:
                print("\nNo basic security issues found.")
            
            return {
                'image': image_details,
                'issues': security_issues
            }
            
        except docker.errors.APIError as e:
            print(f"Docker API error: {e}")
            return {}


# ---- 4. AWS Security Checker ----

class AWSSecurityChecker:
    """Basic AWS security configuration checker"""
    
    def __init__(self):
        """Initialize AWS client if available"""
        self.available = AWS_AVAILABLE
        self.services = {}
        
        if self.available:
            try:
                # Initialize session
                self.session = boto3.Session()
                
                # Check available regions
                self.regions = self.session.get_available_regions('ec2')
                
                # Initialize service clients
                self.services['iam'] = self.session.client('iam')
                self.services['s3'] = self.session.client('s3')
                
                # Set current region
                self.current_region = self.session.region_name or 'us-east-1'
                
                self.ec2_clients = {}
            except Exception as e:
                print(f"AWS initialization error: {e}")
                self.available = False
    
    def check_security(self, check_s3=True, check_iam=True, check_ec2=False):
        """Run basic AWS security checks"""
        if not self.available:
            print("AWS SDK not available. Install boto3 to use this feature.")
            return {}
            
        security_issues = []
        
        print("\nRunning AWS security checks (DEMO MODE)...")
        
        try:
            # Check IAM users
            if check_iam:
                print("Checking IAM configurations...")
                # This is a simulation - in a real environment we'd check for:
                # - Users without MFA
                # - Access keys older than 90 days
                # - Password policies
                
                # Simulate findings for demo
                security_issues.append({
                    'service': 'IAM',
                    'issue': 'Users without MFA',
                    'description': 'Some IAM users do not have multi-factor authentication enabled',
                    'severity': 'high'
                })
                
                security_issues.append({
                    'service': 'IAM',
                    'issue': 'Old access keys',
                    'description': 'Some access keys are older than 90 days',
                    'severity': 'medium'
                })
            
            # Check S3 buckets
            if check_s3:
                print("Checking S3 bucket configurations...")
                # This is a simulation - in a real environment we'd check for:
                # - Public buckets
                # - Buckets without encryption
                # - Buckets without logging
                
                # Simulate findings for demo
                security_issues.append({
                    'service': 'S3',
                    'issue': 'Public bucket',
                    'description': 'Some S3 buckets have public access',
                    'severity': 'high'
                })
                
                security_issues.append({
                    'service': 'S3',
                    'issue': 'Unencrypted buckets',
                    'description': 'Some S3 buckets do not have default encryption',
                    'severity': 'medium'
                })
                
            # Check EC2 instances
            if check_ec2:
                print("Checking EC2 configurations...")
                # This is a simulation - in a real environment we'd check for:
                # - Security groups with open access
                # - Instances without encryption
                # - Public AMIs
                
                # Simulate findings for demo
                security_issues.append({
                    'service': 'EC2',
                    'issue': 'Open security groups',
                    'description': 'Some security groups allow unrestricted access (0.0.0.0/0)',
                    'severity': 'high'
                })
            
            # Report issues
            if security_issues:
                print("\nSecurity Issues Found:")
                for issue in security_issues:
                    print(f"- [{issue['severity'].upper()}] {issue['service']} - {issue['issue']}: {issue['description']}")
            else:
                print("\nNo security issues found.")
            
            return security_issues
            
        except Exception as e:
            print(f"AWS check error: {e}")
            return []


# ---- Demo ----

def demonstrate_infrastructure_security():
    print("===== INFRASTRUCTURE & CONFIGURATION SECURITY DEMO =====\n")
    
    # 1. File Permission Checker
    print("1. File Permission Checker Demo")
    # Check current directory permissions
    perm_checker = FilePermissionChecker(".")
    perm_checker.check_permissions()
    perm_checker.report_issues()
    print("")
    
    # 2. Open Port Scanner
    print("2. Local Port Scanner Demo")
    port_scanner = LocalPortScanner()
    # Scan a small range of ports for the demo
    port_scanner.scan_ports(1, 1000)
    port_scanner.get_listening_processes()
    print("")
    
    # 3. Docker Security Scanner
    print("3. Docker Security Scanner Demo")
    docker_scanner = DockerSecurityScanner()
    if docker_scanner.available:
        images = docker_scanner.list_images()
        
        if images:
            print(f"Found {len(images)} local Docker images")
            # Check first image as an example
            docker_scanner.check_image(images[0].tags[0] if images[0].tags else images[0].id)
        else:
            print("No Docker images found locally")
    print("")
    
    # 4. AWS Security Checker
    print("4. AWS Security Checker Demo")
    aws_checker = AWSSecurityChecker()
    if aws_checker.available:
        aws_checker.check_security()
    else:
        print("AWS SDK not available. Install boto3 to use this feature.")
    

if __name__ == "__main__":
    demonstrate_infrastructure_security()
