import subprocess

def log_securely_with_rust(text):
    try:
        subprocess.run(["../RustLogger/target/release/rust_logger.exe", text], check=True)
    except Exception as e:
        print("Rust logging failed:", e)

# Example
if __name__ == "__main__":
    log_securely_with_rust("Test keystroke from Python")
