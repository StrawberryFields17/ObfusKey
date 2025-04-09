from cryptography.fernet import Fernet
from pathlib import Path

class CryptoUtils:
    def __init__(self, key_path: Path = Path(__file__).parent.parent / "data" / "aes_key.key"):
        self.key_path = key_path
        self.key = self._load_or_create_key()
        self.fernet = Fernet(self.key)

    def _load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            return self.key_path.read_bytes()
        key = Fernet.generate_key()
        self.key_path.parent.mkdir(parents=True, exist_ok=True)
        self.key_path.write_bytes(key)
        return key

    def encrypt_message(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt_message(self, token: bytes) -> str:
        return self.fernet.decrypt(token).decode()

# ✅ Example usage:
if __name__ == "__main__":
    crypto = CryptoUtils()
    secret = "ObfusKey lives"
    
    token = crypto.encrypt_message(secret)
    print("[+] Encrypted:", token.decode())

    original = crypto.decrypt_message(token)
    print("[✓] Decrypted:", original)
