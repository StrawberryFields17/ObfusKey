import hashlib
from pathlib import Path

class HashUtils:
    @staticmethod
    def sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def sha512_hash(data: str) -> str:
        return hashlib.sha512(data.encode()).hexdigest()

    @staticmethod
    def hash_file(path: Path, algo: str = "sha256") -> str:
        hasher = hashlib.new(algo)
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

# Example usage:
if __name__ == "__main__":
    print("SHA-256 of 'ObfusKey':", HashUtils.sha256_hash("ObfusKey"))
    print("SHA-512 of 'ObfusKey':", HashUtils.sha512_hash("ObfusKey"))

    # For file hashing
    # from pathlib import Path
    # print("File SHA-256:", HashUtils.hash_file(Path("log_utils.py")))
