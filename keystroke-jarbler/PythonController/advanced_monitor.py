import psutil
import time
import re
import json
from datetime import datetime

SUSPICIOUS_PATTERNS = [
    r"key.*log", r"spy.*", r"stealth", r"capture", r"intercept", r"sniff", r"logger"
]

KNOWN_BAD_HASHES = set()  # Future expansion: hash suspicious binaries

def is_suspicious(name):
    return any(re.search(pattern, name.lower()) for pattern in SUSPICIOUS_PATTERNS)

def scan_processes():
    found = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            name = proc.info['name'] or ""
            exe = proc.info['exe'] or ""
            if is_suspicious(name) or is_suspicious(exe):
                found.append({
                    'pid': proc.pid,
                    'name': name,
                    'exe': exe,
                    'time': datetime.now().isoformat()
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found

def save_results(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"suspicious_processes_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)

def monitor_loop(interval=10):
    print("Monitoring for suspicious processes...")
    while True:
        results = scan_processes()
        if results:
            print(f"[!] Suspicious processes detected: {len(results)}")
            for r in results:
                print(f"  - PID {r['pid']}: {r['name']} @ {r['exe']}")
            save_results(results)
        time.sleep(interval)

if __name__ == '__main__':
    monitor_loop()