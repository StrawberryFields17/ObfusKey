from cryptography.fernet import Fernet
import datetime
import os

LOG_FILE = "encrypted_keystrokes.log"
KEY_FILE = "aes_key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def log_keystroke(text):
    key = load_key()
    fernet = Fernet(key)
    timestamp = datetime.datetime.now().isoformat()
    message = f"{timestamp} :: {text}"
    encrypted = fernet.encrypt(message.encode())
    with open(LOG_FILE, "ab") as log_file:
        log_file.write(encrypted + b"\n")

# Example usage:
# log_keystroke("A")