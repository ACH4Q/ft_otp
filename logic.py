import os
import time
import hmac
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _derive_key(password: bytes, salt: bytes) -> bytes:
    """Derives a secure encryption key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_data(data: bytes, password: str) -> bytes:
    """Encrypts data using a password-derived key."""
    salt = os.urandom(16)
    key = _derive_key(password.encode(), salt)
    f = Fernet(key)
    return salt + f.encrypt(data)

def decrypt_data(encrypted_data: bytes, password: str) -> bytes:
    """Decrypts data using a password-derived key."""
    salt = encrypted_data[:16]
    encrypted_payload = encrypted_data[16:]
    key = _derive_key(password.encode(), salt)
    f = Fernet(key)
    return f.decrypt(encrypted_payload)

def generate_totp(hex_key: str) -> str:
    """Generates a 6-digit Time-based One-Time Password."""
    try:
        key_bytes = bytes.fromhex(hex_key)
    except ValueError:
        raise ValueError("Invalid hexadecimal key.")

    time_step = 30
    counter = int(time.time()) // time_step
    counter_bytes = counter.to_bytes(8, 'big')
    hmac_hash = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated_hash = hmac_hash[offset:offset+4]
    
    code = int.from_bytes(truncated_hash, 'big') & 0x7FFFFFFF
    otp = code % 1000000
    
    return f"{otp:06d}"