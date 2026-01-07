#!/usr/bin/env python3
"""
Network Security Examples
------------------------
This script demonstrates network security concepts in Python:
1. Simple port scanner
2. Basic packet sniffing with scapy
3. TLS/SSL verification
4. Basic firewall rule creation (demo only)
"""

import socket
import ssl
import ipaddress
import subprocess
import platform
from datetime import datetime
from scapy.all import sniff, IP, TCP

# ---- 1. Port Scanner ----

class PortScanner:
    """Simple port scanner to check for open ports on a target host"""
    
    def __init__(self, target_host):
        """Initialize with target host (IP or domain)"""
        self.target_host = target_host
        self.open_ports = []
        
        # Try to resolve hostname to IP if a domain is provided
        try:
            self.target_ip = socket.gethostbyname(target_host)
            print(f"Target IP: {self.target_ip}")
        except socket.gaierror:
            print(f"Could not resolve hostname: {target_host}")
            self.target_ip = None
    
    def scan_port(self, port, timeout=1):
        """Scan a single port and return True if open"""
        if self.target_ip is None:
            return False
            
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            
            # Try to connect to the port
            result = s.connect_ex((self.target_ip, port))
            s.close()
            
            # If result is 0, the port is open
            return result == 0
        except Exception:
            return False
    
    def scan_port_range(self, start_port, end_port, timeout=1):
        """Scan a range of ports and store open ones"""
        print(f"Scanning ports {start_port}-{end_port} on {self.target_host}...")
        start_time = datetime.now()
        
        self.open_ports = []
        
        for port in range(start_port, end_port + 1):
            if self.scan_port(port, timeout):
                self.open_ports.append(port)
                service = self._get_common_service(port)
                print(f"Port {port} is open - {service}")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"Scan completed in {duration.total_seconds():.2f} seconds")
        print(f"Found {len(self.open_ports)} open ports")
        
        return self.open_ports
    
    def _get_common_service(self, port):
        """Return common service name for well-known ports"""
        common_ports = {
            20: "FTP (Data)",
            21: "FTP (Control)",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            465: "SMTPS",
            587: "SMTP (Submission)",
            993: "IMAPS",
            995: "POP3S",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP (Alt)",
            8443: "HTTPS (Alt)"
        }
        
        return common_ports.get(port, "Unknown")


# ---- 2. Packet Sniffer ----

class PacketSniffer:
    """Basic packet sniffer using Scapy"""
    
    def __init__(self):
        self.packet_count = 0
        self.captured_packets = []
    
    def start_capture(self, interface=None, packet_count=10, 
                      filter_str="ip", save_packets=True):
        """
        Start capturing packets on the specified interface
        
        Note: Capturing packets typically requires root/admin privileges
        """
        print(f"Starting packet capture on {'any interface' if interface is None else interface}")
        print(f"Filter: {filter_str}")
        print(f"Will capture {packet_count} packets...")
        
        try:
            self.packet_count = 0
            if save_packets:
                self.captured_packets = []
                
            # Start sniffing
            sniff(
                iface=interface,
                prn=self._process_packet,
                filter=filter_str,
                store=save_packets,
                count=packet_count
            )
            
            print(f"Captured {self.packet_count} packets")
        except Exception as e:
            print(f"Error capturing packets: {e}")
            print("Note: Packet sniffing usually requires root/admin privileges")
    
    def _process_packet(self, packet):
        """Process and display basic information about captured packet"""
        self.packet_count += 1
        
        # Basic packet details
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            
            # Convert protocol number to name
            if proto == 6:
                proto_name = "TCP"
            elif proto == 17:
                proto_name = "UDP"
            elif proto == 1:
                proto_name = "ICMP"
            else:
                proto_name = f"Proto {proto}"
            
            # Get ports for TCP packets
            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                flags = packet[TCP].flags
                
                print(f"Packet {self.packet_count}: "
                      f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} "
                      f"[{proto_name}] Flags: {flags}")
            else:
                print(f"Packet {self.packet_count}: "
                      f"{src_ip} -> {dst_ip} [{proto_name}]")
        else:
            print(f"Packet {self.packet_count}: (Non-IP packet)")


# ---- 3. SSL/TLS Certificate Verification ----

class TLSVerifier:
    """Verify and display information about SSL/TLS certificates"""
    
    def verify_cert(self, hostname, port=443):
        """Connect to a server and verify its TLS certificate"""
        context = ssl.create_default_context()
        
        try:
            print(f"Connecting to {hostname}:{port} with TLS...")
            
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    # Get the certificate
                    cert = ssock.getpeercert()
                    
                    # Print certificate details
                    print("Certificate verified successfully!")
                    self._print_cert_info(cert)
                    
                    # Get the TLS version
                    version = ssock.version()
                    print(f"TLS Protocol Version: {version}")
                    
                    return True, cert, version
        except ssl.SSLCertVerificationError as e:
            print(f"Certificate verification failed: {e}")
            return False, None, None
        except ssl.SSLError as e:
            print(f"SSL/TLS error: {e}")
            return False, None, None
        except socket.error as e:
            print(f"Connection error: {e}")
            return False, None, None
    
    def _print_cert_info(self, cert):
        """Print human-readable certificate information"""
        if not cert:
            print("No certificate information available")
            return
            
        # Subject details
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer = dict(x[0] for x in cert.get('issuer', []))
        
        print("\nCertificate Information:")
        print("-----------------------")
        
        print("Subject:")
        if 'commonName' in subject:
            print(f"  Common Name: {subject['commonName']}")
        if 'organizationName' in subject:
            print(f"  Organization: {subject['organizationName']}")
            
        print("\nIssuer:")
        if 'commonName' in issuer:
            print(f"  Common Name: {issuer['commonName']}")
        if 'organizationName' in issuer:
            print(f"  Organization: {issuer['organizationName']}")
            
        # Validity dates
        if 'notBefore' in cert:
            print(f"\nValid From: {cert['notBefore']}")
        if 'notAfter' in cert:
            print(f"Valid Until: {cert['notAfter']}")
            
        # Alternative names
        if 'subjectAltName' in cert:
            print("\nSubject Alternative Names:")
            for name_type, name in cert['subjectAltName']:
                print(f"  {name_type}: {name}")


# ---- 4. Firewall Rule Demonstrator ----

class FirewallDemo:
    """Demonstrate firewall rule concepts (no actual rule modification)"""
    
    def __init__(self):
        self.os_type = platform.system().lower()
        self.rules = []
    
    def get_firewall_status(self):
        """Get current firewall status (demonstration only)"""
        print("Checking firewall status...")
        
        if self.os_type == "linux":
            try:
                # For Linux systems with iptables
                output = subprocess.check_output(
                    ["iptables", "-L"], 
                    stderr=subprocess.STDOUT, 
                    universal_newlines=True
                )
                return "Linux iptables firewall is active"
            except Exception:
                return "Could not check iptables status (may need sudo privileges)"
                
        elif self.os_type == "darwin":  # macOS
            try:
                # For macOS
                output = subprocess.check_output(
                    ["pfctl", "-s", "info"], 
                    stderr=subprocess.STDOUT, 
                    universal_newlines=True
                )
                return "macOS PF firewall is active"
            except Exception:
                return "Could not check PF firewall status (may need sudo privileges)"
                
        elif self.os_type == "windows":
            try:
                # For Windows
                output = subprocess.check_output(
                    ["netsh", "advfirewall", "show", "currentprofile"], 
                    stderr=subprocess.STDOUT, 
                    universal_newlines=True
                )
                if "State                                 ON" in output:
                    return "Windows Defender Firewall is ON"
                else:
                    return "Windows Defender Firewall is OFF"
            except Exception:
                return "Could not check Windows firewall status"
                
        return f"Unsupported OS: {self.os_type}"
    
    def demo_add_rule(self, name, port, protocol="tcp", action="allow", direction="in"):
        """Demonstrate firewall rule creation (does not actually modify firewall)"""
        # Validate inputs
        try:
            port = int(port)
            if port < 1 or port > 65535:
                return "Invalid port number (must be 1-65535)"
        except ValueError:
            return "Port must be a number"
            
        if protocol.lower() not in ["tcp", "udp", "icmp"]:
            return "Protocol must be tcp, udp, or icmp"
            
        if action.lower() not in ["allow", "deny", "block"]:
            return "Action must be allow, deny, or block"
            
        if direction.lower() not in ["in", "out", "both"]:
            return "Direction must be in, out, or both"
        
        # Create a rule representation (demo only)
        rule = {
            "name": name,
            "port": port,
            "protocol": protocol.lower(),
            "action": action.lower(),
            "direction": direction.lower(),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.rules.append(rule)
        
        # Show what the command would look like on different platforms
        print("\nFirewall Rule Creation (DEMONSTRATION ONLY - NO ACTUAL CHANGES)")
        print("---------------------------------------------------------------")
        print(f"Rule: {action.upper()} {direction.upper()}BOUND {protocol.upper()} port {port} - '{name}'")
        
        # Linux (iptables) equivalent
        chain = "INPUT" if direction.lower() == "in" else "OUTPUT"
        iptables_action = "ACCEPT" if action.lower() == "allow" else "DROP"
        print("\nLinux (iptables) equivalent command:")
        print(f"sudo iptables -A {chain} -p {protocol.lower()} --dport {port} -j {iptables_action} -m comment --comment \"{name}\"")
        
        # macOS (pf) equivalent - simplified
        print("\nmacOS (pf) equivalent rule (would be added to pf.conf):")
        pf_action = "pass" if action.lower() == "allow" else "block"
        pf_direction = "in" if direction.lower() == "in" else "out"
        print(f"{pf_action} {pf_direction} proto {protocol.lower()} from any to any port {port} # {name}")
        
        # Windows equivalent
        print("\nWindows PowerShell equivalent command:")
        win_action = "Allow" if action.lower() == "allow" else "Block"
        win_direction = "Inbound" if direction.lower() == "in" else "Outbound"
        print(f"New-NetFirewallRule -DisplayName \"{name}\" -Direction {win_direction} -Protocol {protocol.upper()} -LocalPort {port} -Action {win_action}")
        
        return f"Demo rule '{name}' created successfully (not actually implemented)"
    
    def list_demo_rules(self):
        """List all demo rules"""
        if not self.rules:
            return "No demo rules have been created"
            
        print("\nDemo Firewall Rules:")
        print("-------------------")
        
        for i, rule in enumerate(self.rules, 1):
            print(f"Rule {i}: {rule['name']}")
            print(f"  - Port: {rule['port']}/{rule['protocol']}")
            print(f"  - Action: {rule['action'].upper()}")
            print(f"  - Direction: {rule['direction'].upper()}")
            print(f"  - Created: {rule['created']}")
            print("")
            
        return f"Total rules: {len(self.rules)}"


# ---- Demo ----

def demonstrate_network_security():
    print("===== NETWORK SECURITY DEMO =====\n")
    
    # 1. Port Scanner (use a safe target like localhost)
    print("1. Port Scanner Demo")
    print("Note: We'll scan localhost for the demo")
    scanner = PortScanner("localhost")
    scanner.scan_port_range(80, 100)  # Small range for demo
    print("")
    
    # 2. Packet Sniffer (limited capture)
    print("2. Packet Sniffer Demo")
    print("Note: Full packet sniffing requires root/admin privileges")
    sniffer = PacketSniffer()
    try:
        # Only capture 3 packets in the demo, with a basic filter
        sniffer.start_capture(packet_count=3, filter_str="tcp")
    except Exception as e:
        print(f"Could not run packet capture: {e}")
    print("")
    
    # 3. TLS Certificate Verification
    print("3. TLS Certificate Verification Demo")
    verifier = TLSVerifier()
    # Use a well-known HTTPS site
    verifier.verify_cert("www.python.org")
    print("")
    
    # 4. Firewall Rules Demo
    print("4. Firewall Rules Demo")
    fw = FirewallDemo()
    status = fw.get_firewall_status()
    print(f"Current firewall status: {status}")
    
    # Demo creating some rules (no actual changes made)
    fw.demo_add_rule("Allow HTTP", 80, "tcp", "allow", "in")
    fw.demo_add_rule("Block Telnet", 23, "tcp", "deny", "in")
    fw.list_demo_rules()


if __name__ == "__main__":
    demonstrate_network_security()
