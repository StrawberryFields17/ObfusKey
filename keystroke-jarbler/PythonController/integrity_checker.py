from pathlib import Path
from hash_utils import HashUtils

class IntegrityChecker:
    def __init__(self, key: str):
        self.key = key

    def compute_log_hmac(self, log_path: Path) -> str:
        content = log_path.read_text(encoding="utf-8")
        return HashUtils.hmac_sha256(content, self.key)

    def verify_log_hmac(self, log_path: Path, known_hmac: str) -> bool:
        current_hmac = self.compute_log_hmac(log_path)
        match = HashUtils.verify_hmac(log_path.read_text(), known_hmac, self.key)
        print(f"[i] Current HMAC: {current_hmac}")
        print(f"[i] Known   HMAC: {known_hmac}")
        return match

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Verify HMAC integrity of a log file.")
    parser.add_argument("logfile", type=str, help="Path to log file")
    parser.add_argument("--hmac", type=str, help="Known HMAC to verify against")
    parser.add_argument("--print", action="store_true", help="Print HMAC without verifying")

    args = parser.parse_args()
    key = HashUtils.load_hmac_key()
    checker = IntegrityChecker(key)
    log_path = Path(args.logfile)

    if args.print:
        hmac_val = checker.compute_log_hmac(log_path)
        print(f"[+] HMAC: {hmac_val}")
    elif args.hmac:
        if checker.verify_log_hmac(log_path, args.hmac):
            print("[✓] HMAC verified: log file is intact")
        else:
            print("[✗] HMAC mismatch: log file may have been modified")
    else:
        print("[!] Please specify either --print or --hmac for verification.")
