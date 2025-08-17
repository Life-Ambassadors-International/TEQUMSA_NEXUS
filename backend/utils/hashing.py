"""Hashing utilities for TEQUMSA Level 100."""
import hashlib
import hmac
import secrets
from typing import Union, Optional, Dict, Any
import json


class HashUtil:
    """Hashing utility class."""
    
    @staticmethod
    def sha256(data: Union[str, bytes]) -> str:
        """Generate SHA256 hash."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def sha256_short(data: Union[str, bytes], length: int = 16) -> str:
        """Generate short SHA256 hash."""
        return HashUtil.sha256(data)[:length]
    
    @staticmethod
    def md5(data: Union[str, bytes]) -> str:
        """Generate MD5 hash."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """Generate HMAC-SHA256."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hmac.new(key, data, hashlib.sha256).hexdigest()
    
    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """Generate cryptographic salt."""
        return secrets.token_hex(length // 2)
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
        """Hash password with salt."""
        if salt is None:
            salt = HashUtil.generate_salt()
        
        # Use PBKDF2 for password hashing
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        hashed = key.hex()
        
        return {
            'hash': hashed,
            'salt': salt,
            'algorithm': 'pbkdf2_sha256',
            'iterations': 100000
        }
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str, iterations: int = 100000) -> bool:
        """Verify password against stored hash."""
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
        return key.hex() == stored_hash
    
    @staticmethod
    def hash_dict(data: Dict[str, Any], sort_keys: bool = True) -> str:
        """Generate hash of a dictionary."""
        json_str = json.dumps(data, sort_keys=sort_keys, separators=(',', ':'))
        return HashUtil.sha256(json_str)
    
    @staticmethod
    def content_hash(content: Union[str, bytes], algorithm: str = 'sha256') -> str:
        """Generate content hash with specified algorithm."""
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        if algorithm == 'sha256':
            return hashlib.sha256(content).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(content).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(content).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def checksum(data: Union[str, bytes]) -> str:
        """Generate simple checksum for data integrity."""
        return HashUtil.sha256_short(data, 8)
    
    @staticmethod
    def entity_fingerprint(entity_type: str, entity_id: str, properties: Dict[str, Any]) -> str:
        """Generate fingerprint for ECS entity."""
        fingerprint_data = {
            'type': entity_type,
            'id': entity_id,
            'properties': properties
        }
        return HashUtil.hash_dict(fingerprint_data)
    
    @staticmethod
    def consent_hash(account_id: str, action: str, timestamp: str, details: Dict[str, Any]) -> str:
        """Generate hash for consent record."""
        consent_data = {
            'account_id': account_id,
            'action': action,
            'timestamp': timestamp,
            'details': details
        }
        return HashUtil.hash_dict(consent_data)


# Convenience functions
def hash_string(text: str) -> str:
    """Hash a string using SHA256."""
    return HashUtil.sha256(text)


def short_hash(text: str, length: int = 8) -> str:
    """Generate short hash of a string."""
    return HashUtil.sha256_short(text, length)


def secure_random_string(length: int = 32) -> str:
    """Generate secure random string."""
    return secrets.token_urlsafe(length)


def generate_api_key() -> str:
    """Generate API key."""
    return f"tequmsa_{secrets.token_urlsafe(32)}"


def verify_checksum(data: Union[str, bytes], expected_checksum: str) -> bool:
    """Verify data against checksum."""
    return HashUtil.checksum(data) == expected_checksum