#!/usr/bin/env python3
"""
Authentication & Access Control Examples
---------------------------------------
This script demonstrates basic authentication and access control concepts in Python:
1. Password hashing with bcrypt
2. Password verification
3. Multi-factor authentication simulation
4. JWT token handling for authentication
5. Role-based access control (RBAC)
"""

import bcrypt
import hmac
import hashlib
import time
import jwt
import argon2
from datetime import datetime, timedelta
import secrets
import base64

# ---- 1. Password Hashing ----

def hash_password_bcrypt(password):
    """Hash a password using bcrypt (widely recommended)"""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password_bcrypt(stored_hash, provided_password):
    """Verify a password against a bcrypt hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

def hash_password_argon2(password):
    """Hash a password using Argon2 (memory-hard function, recommended for sensitive contexts)"""
    ph = argon2.PasswordHasher()
    hash = ph.hash(password)
    return hash

def verify_password_argon2(stored_hash, provided_password):
    """Verify a password against an Argon2 hash"""
    ph = argon2.PasswordHasher()
    try:
        ph.verify(stored_hash, provided_password)
        return True
    except (argon2.exceptions.VerifyMismatchError, ValueError):
        return False

# ---- 2. Multi-Factor Authentication ----

class MFASystem:
    """Simple Time-based One-Time Password (TOTP) implementation"""
    
    def __init__(self, secret=None):
        # Generate a random secret key for TOTP if not provided
        if secret is None:
            self.secret = base64.b32encode(secrets.token_bytes(10)).decode('utf-8')
        else:
            self.secret = secret
    
    def get_totp_token(self):
        """Generate a TOTP token (time-based one-time password)"""
        # Get current time in 30-second intervals
        counter = int(time.time()) // 30
        return self._generate_totp(counter)
    
    def verify_totp(self, token):
        """Verify a TOTP token"""
        # Check current time interval
        counter = int(time.time()) // 30
        
        # Check if the provided token matches current interval or previous interval
        # (for clock drift allowance)
        return (token == self._generate_totp(counter) or 
                token == self._generate_totp(counter - 1))
    
    def _generate_totp(self, counter):
        """Generate a TOTP code based on counter value"""
        # Convert counter to bytes
        counter_bytes = counter.to_bytes(8, byteorder='big')
        
        # Generate HMAC-SHA1
        hmac_result = hmac.new(
            base64.b32decode(self.secret, casefold=True), 
            counter_bytes, 
            hashlib.sha1
        ).digest()
        
        # Dynamic truncation
        offset = hmac_result[-1] & 0x0F
        code = ((hmac_result[offset] & 0x7F) << 24 |
                (hmac_result[offset + 1] & 0xFF) << 16 |
                (hmac_result[offset + 2] & 0xFF) << 8 |
                (hmac_result[offset + 3] & 0xFF))
        
        # Restrict to 6 digits
        code = code % 1000000
        return f"{code:06d}"  # Return as 6-digit string

# ---- 3. JWT Token Handling ----

class JWTHandler:
    """JWT token generation and validation for authentication"""
    
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def generate_token(self, user_id, username, roles=None, expiry_hours=24):
        """Generate a JWT token with user information and expiry time"""
        if roles is None:
            roles = ["user"]  # Default role
            
        payload = {
            'sub': user_id,  # Subject (user identifier)
            'username': username,
            'roles': roles,
            'iat': datetime.utcnow(),  # Issued at
            'exp': datetime.utcnow() + timedelta(hours=expiry_hours)  # Expiry
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
    
    def validate_token(self, token):
        """Validate a JWT token and return its payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

# ---- 4. Role-Based Access Control (RBAC) ----

class RBACSystem:
    """Simple Role-Based Access Control implementation"""
    
    def __init__(self):
        # Initialize roles and permissions
        self.roles = {
            'user': ['read'],
            'editor': ['read', 'write'],
            'admin': ['read', 'write', 'delete', 'manage_users']
        }
        
        # Initialize resources and required permissions
        self.resources = {
            'articles': {'view': 'read', 'edit': 'write', 'delete': 'delete'},
            'users': {'view': 'read', 'edit': 'manage_users'},
            'settings': {'view': 'read', 'edit': 'manage_users'}
        }
    
    def check_permission(self, user_roles, resource, action):
        """Check if user has permission to perform action on resource"""
        if not isinstance(user_roles, list):
            user_roles = [user_roles]
            
        # Get the permission required for this resource and action
        if resource not in self.resources or action not in self.resources[resource]:
            return False
            
        required_permission = self.resources[resource][action]
        
        # Check if any of the user's roles have this permission
        for role in user_roles:
            if role in self.roles and required_permission in self.roles[role]:
                return True
                
        return False


# ---- Demo ----

def demonstrate_authentication():
    print("===== AUTHENTICATION & ACCESS CONTROL DEMO =====\n")
    
    # 1. Password hashing
    print("1. Password Hashing")
    password = "SecureP@ssw0rd!"
    hashed_bcrypt = hash_password_bcrypt(password)
    hashed_argon2 = hash_password_argon2(password)
    
    print(f"Original password: {password}")
    print(f"Bcrypt hash: {hashed_bcrypt}")
    print(f"Argon2 hash: {hashed_argon2}")
    
    # Verification
    correct = verify_password_bcrypt(hashed_bcrypt, password)
    incorrect = verify_password_bcrypt(hashed_bcrypt, "WrongPassword")
    print(f"Correct password verification: {correct}")
    print(f"Incorrect password verification: {incorrect}\n")
    
    # 2. MFA
    print("2. Multi-Factor Authentication (MFA)")
    mfa = MFASystem("JBSWY3DPEHPK3PXP")  # Example secret
    totp = mfa.get_totp_token()
    print(f"Generated TOTP token: {totp}")
    print(f"Token verification: {mfa.verify_totp(totp)}\n")
    
    # 3. JWT
    print("3. JWT Token Handling")
    jwt_handler = JWTHandler("very-secure-jwt-secret-key")
    token = jwt_handler.generate_token(123, "alice", ["admin", "editor"])
    print(f"JWT token: {token}")
    payload = jwt_handler.validate_token(token)
    print(f"Validated token payload: {payload}\n")
    
    # 4. RBAC
    print("4. Role-Based Access Control")
    rbac = RBACSystem()
    
    # User with different roles
    admin = ["admin"]
    editor = ["editor"]
    regular_user = ["user"]
    
    # Check permissions
    print(f"Admin can edit articles: {rbac.check_permission(admin, 'articles', 'edit')}")
    print(f"Editor can edit articles: {rbac.check_permission(editor, 'articles', 'edit')}")
    print(f"Regular user can edit articles: {rbac.check_permission(regular_user, 'articles', 'edit')}")
    print(f"Editor can edit users: {rbac.check_permission(editor, 'users', 'edit')}")
    print(f"Admin can edit users: {rbac.check_permission(admin, 'users', 'edit')}")


if __name__ == "__main__":
    demonstrate_authentication()
