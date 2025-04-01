import hashlib
import hmac
import os
import base64
import json
from pathlib import Path

class HashUtils:
    @staticmethod
    def sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def sha512_hash(data: str) -> str:
        return hashlib.sha512(data.encode()).hexdigest()

    @staticmethod
    def blake2b_hash(data: str) -> str:
        return hashlib.blake2b(data.encode()).hexdigest()

    @staticmethod
    def sha3_256_hash(data: str) -> str:
        return hashlib.sha3_256(data.encode()).hexdigest()

    @staticmethod
    def hmac_sha256(data: str, key: str) -> str:
        return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_hmac(data: str, expected: str, key: str) -> bool:
        actual = HashUtils.hmac_sha256(data, key)
        return hmac.compare_digest(actual, expected)

    @staticmethod
    def salted_hash(data: str, salt: bytes = None) -> tuple[str, str]:
        if salt is None:
            salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100_000)
        return hash_bytes.hex(), salt.hex()

    @staticmethod
    def verify_salted_hash(data: str, stored_hash: str, salt_hex: str) -> bool:
        salt = bytes.fromhex(salt_hex)
        new_hash, _ = HashUtils.salted_hash(data, salt)
        return new_hash == stored_hash

    @staticmethod
    def hash_file(path: Path, algo: str = "sha256") -> str:
        hasher = hashlib.new(algo)
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def load_hmac_key() -> str:
        # Priority: ENV > secrets.json > fallback
        if "HMAC_SECRET" in os.environ:
            return os.environ["HMAC_SECRET"]
        config_path = Path(__file__).parent.parent / "secrets.json"
        if config_path.exists():
            with config_path.open("r") as f:
                return json.load(f).get("HMAC_SECRET", "default_key")
        return "default_key"

# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hashing Utility Tool")
    parser.add_argument("data", help="Input string or file path")
    parser.add_argument("--file", action="store_true", help="Hash input as a file")
    parser.add_argument("--algo", default="sha256", help="Hash algorithm (sha256, sha512, blake2b, sha3_256)")
    parser.add_argument("--hmac", action="store_true", help="Use HMAC with secret key")
    parser.add_argument("--salt", action="store_true", help="Use salted hash")
    parser.add_argument("--format", choices=["hex", "base64"], default="hex", help="Output format")

    args = parser.parse_args()
    key = HashUtils.load_hmac_key()

    if args.file:
        digest = HashUtils.hash_file(Path(args.data), args.algo)
    elif args.hmac:
        digest = HashUtils.hmac_sha256(args.data, key)
    elif args.salt:
        digest, salt = HashUtils.salted_hash(args.data)
        print("Salted Hash:", digest)
        print("Salt (hex):", salt)
        exit(0)
    else:
        algo_map = {
            "sha256": HashUtils.sha256_hash,
            "sha512": HashUtils.sha512_hash,
            "blake2b": HashUtils.blake2b_hash,
            "sha3_256": HashUtils.sha3_256_hash,
        }
        digest = algo_map.get(args.algo, HashUtils.sha256_hash)(args.data)

    if args.format == "base64":
        raw_bytes = bytes.fromhex(digest)
        print(base64.b64encode(raw_bytes).decode())
    else:
        print(digest)
