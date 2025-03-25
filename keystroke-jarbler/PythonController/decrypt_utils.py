from cryptography.fernet import Fernet
from pathlib import Path

class LogDecryptor:
    def __init__(self, key_path: Path, log_path: Path):
        self.key_path = key_path
        self.log_path = log_path
        self.fernet = Fernet(self._load_key())

    def _load_key(self) -> bytes:
        if not self.key_path.exists():
            raise FileNotFoundError(f"Key file not found: {self.key_path}")
        return self.key_path.read_bytes()

    def decrypt_logs(self) -> list[str]:
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log file not found: {self.log_path}")
        decrypted_lines = []
        with self.log_path.open("rb") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        decrypted = self.fernet.decrypt(line).decode()
                        decrypted_lines.append(decrypted)
                    except Exception:
                        decrypted_lines.append("[Decryption failed]")
        return decrypted_lines

# Example usage
if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data"
    key_file = data_dir / "aes_key.key"
    log_file = data_dir / "encrypted_keystrokes.log"

    decryptor = LogDecryptor(key_file, log_file)
    lines = decryptor.decrypt_logs()

    for line in lines:
        print(line)
