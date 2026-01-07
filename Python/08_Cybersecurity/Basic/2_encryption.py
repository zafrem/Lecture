#!/usr/bin/env python3
"""
Encryption & Data Protection Examples
------------------------------------
This script demonstrates encryption and data protection concepts in Python:
1. Symmetric encryption (AES)
2. Asymmetric encryption (RSA)
3. Digital signatures 
4. Secure key management simulation
"""

import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key,
    Encoding, PrivateFormat, PublicFormat, NoEncryption
)
from cryptography.exceptions import InvalidSignature


# ---- 1. Symmetric Encryption (AES) ----

class AESCipher:
    """AES encryption using CBC mode with secure padding"""
    
    def __init__(self, key=None):
        """Initialize with a key or generate a new one"""
        if key is None:
            # Generate a secure random 256-bit key (32 bytes)
            self.key = os.urandom(32)
        else:
            # Use provided key (must be 16, 24, or 32 bytes for AES-128/192/256)
            self.key = key
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using AES-CBC with secure padding"""
        # Generate a random IV (initialization vector)
        iv = os.urandom(16)
        
        # Create padder and cipher
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        
        # Create AES cipher with CBC mode
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Encrypt the data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + ciphertext (IV needs to be stored with the ciphertext)
        return {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
        }
    
    def decrypt(self, encrypted_data):
        """Decrypt ciphertext using AES-CBC"""
        # Extract IV and ciphertext
        iv = base64.b64decode(encrypted_data['iv'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        
        # Create cipher
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        # Decrypt data
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')

    def get_key_base64(self):
        """Return the key in base64 encoding for storage or transmission"""
        return base64.b64encode(self.key).decode('utf-8')
    
    @classmethod
    def from_base64_key(cls, base64_key):
        """Create a cipher instance from a base64-encoded key"""
        key = base64.b64decode(base64_key)
        return cls(key)


# ---- 2. Asymmetric Encryption (RSA) ----

class RSACipher:
    """RSA encryption for secure key exchange and small data encryption"""
    
    def __init__(self, private_key=None, public_key=None):
        """Initialize with keys or generate new key pair"""
        if private_key is None and public_key is None:
            # Generate a new 2048-bit RSA key pair
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,  # Standard value for e
                key_size=2048
            )
            self.public_key = self.private_key.public_key()
        else:
            # Use provided keys
            self.private_key = private_key
            self.public_key = public_key
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using the public key"""
        # RSA has a limit on plaintext size, typically:
        # key_size_in_bytes - padding_overhead = max_plaintext_size
        # For 2048-bit keys with OAEP padding, ~220-240 bytes is the limit
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode('utf-8')
            
        ciphertext = self.public_key.encrypt(
            plaintext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using the private key"""
        if not self.private_key:
            raise ValueError("Private key required for decryption")
            
        ciphertext_bytes = base64.b64decode(ciphertext)
        plaintext = self.private_key.decrypt(
            ciphertext_bytes,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')
    
    def export_public_key(self):
        """Export the public key in PEM format"""
        return self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def export_private_key(self):
        """Export the private key in PEM format (should be protected in practice)"""
        if not self.private_key:
            raise ValueError("No private key to export")
            
        return self.private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        ).decode('utf-8')
    
    @classmethod
    def from_pem(cls, public_pem=None, private_pem=None):
        """Create an RSA cipher from PEM-formatted keys"""
        public_key = None
        private_key = None
        
        if public_pem:
            public_key = load_pem_public_key(public_pem.encode('utf-8'))
            
        if private_pem:
            private_key = load_pem_private_key(
                private_pem.encode('utf-8'),
                password=None
            )
            
        return cls(private_key=private_key, public_key=public_key)


# ---- 3. Digital Signatures ----

class DigitalSigner:
    """Create and verify digital signatures using RSA"""
    
    def __init__(self, private_key=None):
        """Initialize with an optional private key"""
        if private_key is None:
            # Generate a new key for signing
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
        else:
            self.private_key = private_key
            
        # Get the public key from the private key
        self.public_key = self.private_key.public_key()
    
    def sign(self, message):
        """Sign a message with the private key"""
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
            
        signature = self.private_key.sign(
            message,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    def verify(self, message, signature, public_key=None):
        """Verify a signature using the public key"""
        if public_key is None:
            public_key = self.public_key
            
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
            
        signature_bytes = base64.b64decode(signature)
        
        try:
            public_key.verify(
                signature_bytes,
                message,
                asym_padding.PSS(
                    mgf=asym_padding.MGF1(hashes.SHA256()),
                    salt_length=asym_padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
    
    def export_public_key(self):
        """Export the public key for signature verification"""
        return self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')


# ---- 4. Secure Key Storage Simulation ----

class KeyVaultSimulator:
    """Simulates a secure key vault for storing encryption keys"""
    
    def __init__(self, vault_file=None):
        self.vault_file = vault_file or "key_vault.json"
        self.vault = {}
        
        # Master key to encrypt the vault
        # In a real system, this would be derived from a password or HSM
        self.master_key = os.urandom(32)
        self.master_cipher = AESCipher(self.master_key)
        
        # Try to load existing vault
        self._load_vault()
    
    def _load_vault(self):
        """Load the vault from file if it exists"""
        try:
            if os.path.exists(self.vault_file):
                with open(self.vault_file, 'r') as f:
                    encrypted_data = json.load(f)
                    # Decrypt the vault with the master key
                    vault_data = self.master_cipher.decrypt(encrypted_data)
                    self.vault = json.loads(vault_data)
        except Exception as e:
            print(f"Error loading vault: {e}")
            self.vault = {}
    
    def _save_vault(self):
        """Save the vault to file"""
        try:
            # Encrypt the vault with the master key
            vault_json = json.dumps(self.vault)
            encrypted_data = self.master_cipher.encrypt(vault_json)
            
            with open(self.vault_file, 'w') as f:
                json.dump(encrypted_data, f)
        except Exception as e:
            print(f"Error saving vault: {e}")
    
    def store_key(self, key_id, key_data):
        """Store a key in the vault"""
        self.vault[key_id] = key_data
        self._save_vault()
    
    def retrieve_key(self, key_id):
        """Retrieve a key from the vault"""
        if key_id in self.vault:
            return self.vault[key_id]
        return None
    
    def delete_key(self, key_id):
        """Delete a key from the vault"""
        if key_id in self.vault:
            del self.vault[key_id]
            self._save_vault()
            return True
        return False
    
    def list_keys(self):
        """List all key IDs in the vault"""
        return list(self.vault.keys())


# ---- Demo ----

def demonstrate_encryption():
    print("===== ENCRYPTION & DATA PROTECTION DEMO =====\n")
    
    # 1. Symmetric Encryption (AES)
    print("1. Symmetric Encryption (AES)")
    aes = AESCipher()
    plaintext = "This is a secret message that needs to be encrypted securely!"
    
    print(f"Original text: {plaintext}")
    print(f"AES Key (Base64): {aes.get_key_base64()}")
    
    encrypted = aes.encrypt(plaintext)
    print(f"Encrypted (Base64): {encrypted}")
    
    decrypted = aes.decrypt(encrypted)
    print(f"Decrypted: {decrypted}\n")
    
    # 2. Asymmetric Encryption (RSA)
    print("2. Asymmetric Encryption (RSA)")
    rsa_cipher = RSACipher()
    message = "This message will be encrypted with RSA"
    
    print(f"Original message: {message}")
    encrypted_msg = rsa_cipher.encrypt(message)
    print(f"RSA Encrypted (Base64): {encrypted_msg}")
    
    decrypted_msg = rsa_cipher.decrypt(encrypted_msg)
    print(f"RSA Decrypted: {decrypted_msg}")
    
    # Export keys demonstration
    public_pem = rsa_cipher.export_public_key()
    print(f"Public Key (PEM format, first 50 chars): {public_pem[:50]}...\n")
    
    # 3. Digital Signatures
    print("3. Digital Signatures")
    signer = DigitalSigner()
    document = "This document needs to be signed to verify its authenticity"
    
    print(f"Document: {document}")
    signature = signer.sign(document)
    print(f"Signature (Base64): {signature}")
    
    is_valid = signer.verify(document, signature)
    print(f"Signature verification: {is_valid}")
    
    tampered_document = document + " (tampered)"
    tampered_valid = signer.verify(tampered_document, signature)
    print(f"Tampered document verification: {tampered_valid}\n")
    
    # 4. Key Vault Simulation
    print("4. Secure Key Storage Simulation")
    vault = KeyVaultSimulator("demo_vault.json")
    
    # Store a key
    vault.store_key("app1_encryption_key", aes.get_key_base64())
    print(f"Stored key with ID: app1_encryption_key")
    
    # Retrieve the key
    retrieved_key = vault.retrieve_key("app1_encryption_key")
    print(f"Retrieved key: {retrieved_key}")
    
    # List all keys
    all_keys = vault.list_keys()
    print(f"All keys in vault: {all_keys}")
    
    # Clean up demo file
    if os.path.exists("demo_vault.json"):
        os.remove("demo_vault.json")
        print("Demo vault file cleaned up")


if __name__ == "__main__":
    demonstrate_encryption()
