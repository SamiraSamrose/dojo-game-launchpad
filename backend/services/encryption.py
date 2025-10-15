# backend/services/encryption.py
# End-to-end encryption for private communications (Wootzapp)

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())


class EncryptionService:
    """End-to-end encryption for private communications"""
    
    def __init__(self, key: bytes = ENCRYPTION_KEY):
        self.cipher = Fernet(key)
    
    def encrypt_message(self, message: str) -> str:
        """Encrypt a message"""
        encrypted = self.cipher.encrypt(message.encode())
        return encrypted.decode()
    
    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a message"""
        decrypted = self.cipher.decrypt(encrypted_message.encode())
        return decrypted.decode()
    
    def generate_user_key(self, user_id: str, password: str) -> bytes:
        """Generate user-specific encryption key"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=user_id.encode(),
            iterations=100000,
        )
        key = kdf.derive(password.encode())
        return key
