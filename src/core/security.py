from cryptography.fernet import Fernet
from src.core.config import settings


class SecurityService:
    """Сервис для шифрования/дешифрования чувствительных данных"""
    
    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt(self, data: str) -> str:
        """Шифрование строки"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Дешифрование строки"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()


security_service = SecurityService()