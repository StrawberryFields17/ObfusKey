import hashlib
import hmac
import os
from pathlib import Path

class HashUtils:
    @staticmethod
    def sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def sha512_hash(data: str) -> str:
        return hashlib.sha512(data.encode()).hexdigest()

    @staticmethod
    def hmac_sha256(data: str, key: str) -> str:
        return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def salted_hash(data: str, salt: bytes = None) -> tuple[str, str]:
        if salt is None:
            salt = os.urandom(16)
        salted = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100_000)
        return salted.hex(), salt.hex()

    @staticmethod
    def hash_file(path: Path, algo: str = "sha256") -> str:
        hasher = hashlib.new(algo)
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

# CLI tool
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hashing Utility Tool")
    parser.add_argument("data", help="Input string or file path")
    parser.add_argument("--file", action="store_true", help="Hash the input as a file")
    parser.add_argument("--algo", default="sha256", help="Hash algorithm (default: sha256)")
    parser.add_argument("--hmac", help="Use HMAC with the given key")
    parser.add_argument("--salt", action="store_true", help="Use salted hash (only with --data)")

    args = parser.parse_args()

    if args.file:
        path = Path(args.data)
        print(f"{args.algo.upper()} hash of file {path}:")
        print(HashUtils.hash_file(path, args.algo))
    elif args.hmac:
        print(f"HMAC-{args.algo.upper()} of input:")
        print(HashUtils.hmac_sha256(args.data, args.hmac))
    elif args.salt:
        hash_hex, salt_hex = HashUtils.salted_hash(args.data)
        print(f"Salted Hash: {hash_hex}")
        print(f"Salt (hex): {salt_hex}")
    else:
        print(f"{args.algo.upper()} hash of input:")
        if args.algo == "sha256":
            print(HashUtils.sha256_hash(args.data))
        else:
            print(HashUtils.sha512_hash(args.data))
