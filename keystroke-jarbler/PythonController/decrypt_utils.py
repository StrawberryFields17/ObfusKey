from cryptography.fernet import Fernet
from pathlib import Path
from datetime import datetime
import argparse

class LogDecryptor:
    def __init__(self, key_path: Path):
        self.key_path = key_path
        self.fernet = Fernet(self._load_key())

    def _load_key(self) -> bytes:
        if not self.key_path.exists():
            raise FileNotFoundError(f"Key file not found: {self.key_path}")
        return self.key_path.read_bytes()

    def decrypt_log_file(self, log_path: Path) -> list[str]:
        if not log_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_path}")
        decrypted_lines = []
        with log_path.open("rb") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        decrypted = self.fernet.decrypt(line).decode()
                        decrypted_lines.append(decrypted)
                    except Exception:
                        decrypted_lines.append("[Decryption failed]")
        return decrypted_lines

    def batch_decrypt(self, log_dir: Path) -> list[str]:
        logs = sorted(log_dir.glob("encrypted_keystrokes*.log"))
        all_lines = []
        for log_file in logs:
            try:
                all_lines.extend(self.decrypt_log_file(log_file))
            except Exception as e:
                print(f"[!] Skipping {log_file.name}: {e}")
        return all_lines

def filter_logs(logs: list[str], since: str = None, limit: int = None) -> list[str]:
    filtered = logs
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            filtered = [line for line in filtered if line.startswith("[") and datetime.fromisoformat(line[1:line.index("]")]) >= since_dt]
        except Exception:
            print("[!] Invalid --since timestamp format")
    if limit:
        filtered = filtered[-limit:]
    return filtered

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt encrypted log files.")
    parser.add_argument("--key", type=str, default=str(Path(__file__).parent.parent / "data" / "aes_key.key"))
    parser.add_argument("--dir", type=str, default=str(Path(__file__).parent.parent / "data"))
    parser.add_argument("--outfile", type=str, help="Write output to plaintext file instead of console")
    parser.add_argument("--limit", type=int, help="Show only the most recent N entries")
    parser.add_argument("--since", type=str, help="Only show logs after this ISO timestamp (e.g., 2025-03-29T10:00:00)")

    args = parser.parse_args()

    decryptor = LogDecryptor(Path(args.key))
    all_logs = decryptor.batch_decrypt(Path(args.dir))
    filtered_logs = filter_logs(all_logs, since=args.since, limit=args.limit)

    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_logs))
        print(f"[+] Exported {len(filtered_logs)} entries to {args.outfile}")
    else:
        for line in filtered_logs:
            print(line)
