# Basic Security Concepts

This directory contains Python implementations of fundamental cybersecurity concepts. Each module is designed to demonstrate a specific area of security through practical examples.

## Contents

### 1. Authentication & Access Control

Demonstrates how to securely handle user identities and permissions using industry-standard libraries.

<details>
<summary>View Code Snippets</summary>

**Password Hashing (bcrypt)**
```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

**JSON Web Tokens (JWT)**
```python
import jwt
from datetime import datetime, timedelta

def generate_token(user_id, secret_key):
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')
```
</details>

*   **Hashing**: Uses `bcrypt` and `Argon2` for secure password storage.
*   **MFA**: Simulates Time-based One-Time Passwords (TOTP).
*   **RBAC**: Implements a Role-Based Access Control system to manage permissions.

---

### 2. Encryption & Data Protection

Covers both symmetric and asymmetric encryption techniques to protect data at rest and in transit.

<details>
<summary>View Code Snippets</summary>

**Symmetric Encryption (AES-CBC)**
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_aes(plaintext, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    # ... handle padding and encryption
    return iv, ciphertext
```

**Digital Signatures (RSA)**
```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def sign_data(message, private_key):
    return private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
```
</details>

*   **AES**: Secure symmetric encryption for large data sets.
*   **RSA**: Asymmetric encryption for secure key exchange and digital signatures.
*   **Key Vault**: A simulation of secure key storage and management.

---

### 3. Network Security

Explores network-level security tasks including scanning, sniffing, and certificate verification.

<details>
<summary>View Code Snippets</summary>

**Port Scanning**
```python
import socket

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s.connect_ex((ip, port)) == 0
```

**TLS Verification**
```python
import ssl, socket

def verify_cert(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return ssock.getpeercert()
```
</details>

*   **Port Scanner**: Identifies open ports and common services on a host.
*   **Packet Sniffing**: Uses `scapy` to capture and analyze network traffic.
*   **Firewall Demo**: Demonstrates the logic behind creating firewall rules on different platforms.

---

### 4. Vulnerability Assessment

Implements basic logic for identifying security weaknesses in web applications and configurations.

<details>
<summary>View Code Snippets</summary>

**Web Vulnerability Check (XSS/SQLi Simulation)**
```python
# Simulating a check for XSS payloads in form inputs
def check_xss(form_action, payload):
    print(f"Testing {form_action} with payload: {payload}")
    # ... logic to analyze response
```

**File Integrity Monitoring**
```python
import hashlib

def calculate_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()
```
</details>

*   **Web Scanner**: Simulates detection of XSS and SQL injection vulnerabilities.
*   **Password Checker**: Evaluates password strength against common patterns and lists.
*   **Integrity Monitor**: Tracks changes in files by comparing SHA-256 hashes.

---

### 5. Logging & Monitoring

Focuses on creating secure, auditable logs and monitoring system resources for anomalies.

<details>
<summary>View Code Snippets</summary>

**Structured JSON Logging**
```python
from pythonjsonlogger import jsonlogger
import logging

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```
</details>

*   **Secure Logger**: Implements rotating logs and structured JSON formatting for easy analysis.
*   **Resource Monitor**: Tracks CPU, memory, and disk usage using `psutil`.
*   **Anomaly Detection**: Identifies sudden spikes or unusual trends in system metrics.

---

### 6. Infrastructure Security

Provides scripts for hardening systems and checking security configurations.

<details>
<summary>View Code Snippets</summary>

**Permission Checker**
```python
import os, stat

def check_world_writable(filepath):
    mode = os.stat(filepath).st_mode
    return bool(mode & stat.S_IWOTH)
```
</details>

*   **Permission Auditor**: Scans for world-writable files and dangerous SetUID/SetGID bits.
*   **Docker Security**: Basic checks for image configurations (e.g., running as root).
*   **AWS Checker**: Simulates security group and S3 bucket configuration audits.

---

### 7. Incident Response & Forensics

Tools for collecting evidence and analyzing events after a security incident.

<details>
<summary>View Code Snippets</summary>

**Metadata Extraction**
```python
import os, datetime

def get_metadata(filepath):
    stat = os.stat(filepath)
    return {
        'size': stat.st_size,
        'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'md5': calculate_md5(filepath)
    }
```
</details>

*   **Log Collector**: Automates the gathering of system logs for forensic analysis.
*   **Timeline Creator**: Builds a unified chronological sequence of file and log events.
*   **Memory Simulation**: Demonstrates how to list running processes and identify suspicious behavior.