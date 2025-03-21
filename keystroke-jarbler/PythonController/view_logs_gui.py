import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from cryptography.fernet import Fernet
import threading
import psutil
import re
from datetime import datetime

LOG_FILE = "encrypted_keystrokes.log"
KEY_FILE = "aes_key.key"

SUSPICIOUS_PATTERNS = [
    r"key.*log", r"spy.*", r"stealth", r"capture", r"intercept", r"sniff", r"logger"
]

class LogViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("ObfusKey: Viewer + Monitor")
        master.geometry("800x500")

        self.tab_control = ttk.Notebook(master)
        self.viewer_tab = ttk.Frame(self.tab_control)
        self.monitor_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.viewer_tab, text="Log Viewer")
        self.tab_control.add(self.monitor_tab, text="Keylogger Monitor")
        self.tab_control.pack(expand=1, fill="both")

        self.init_viewer_tab()
        self.init_monitor_tab()

    def init_viewer_tab(self):
        top_frame = tk.Frame(self.viewer_tab)
        top_frame.pack(fill=tk.X)

        self.search_entry = tk.Entry(top_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=5)

        self.search_button = tk.Button(top_frame, text="Search", command=self.search_logs)
        self.search_button.pack(side=tk.LEFT)

        self.export_button = tk.Button(top_frame, text="Export", command=self.export_logs)
        self.export_button.pack(side=tk.LEFT, padx=10)

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Encrypted Log", command=self.open_log)
        file_menu.add_command(label="Open Key File", command=self.open_key)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        self.viewer_text_area = scrolledtext.ScrolledText(self.viewer_tab, wrap=tk.WORD, font=("Consolas", 10))
        self.viewer_text_area.pack(fill=tk.BOTH, expand=True)

        self.key = None
        self.decrypted_lines = []

    def init_monitor_tab(self):
        self.monitor_text_area = scrolledtext.ScrolledText(self.monitor_tab, wrap=tk.WORD, font=("Consolas", 10))
        self.monitor_text_area.pack(fill=tk.BOTH, expand=True)
        self.monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        self.monitor_thread.start()

    def monitor_processes(self):
        seen = set()
        while True:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    name = proc.info['name'] or ""
                    exe = proc.info['exe'] or ""
                    if any(re.search(pattern, name.lower()) for pattern in SUSPICIOUS_PATTERNS):
                        identity = f"{proc.pid}:{name}"
                        if identity not in seen:
                            seen.add(identity)
                            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            entry = f"[{now}] Suspicious: {name} (PID {proc.pid}) at {exe}"
                            self.monitor_text_area.insert(tk.END, entry + "\n")
                            self.monitor_text_area.see(tk.END)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

    def open_key(self):
        path = filedialog.askopenfilename(title="Select AES Key File")
        if path:
            try:
                with open(path, "rb") as f:
                    self.key = f.read()
                messagebox.showinfo("Key Loaded", "AES key loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load key: {e}")

    def open_log(self):
        path = filedialog.askopenfilename(title="Select Encrypted Log File")
        if not self.key:
            messagebox.showerror("Error", "Load the AES key first.")
            return
        if path:
            try:
                with open(path, "rb") as f:
                    lines = f.readlines()
                fernet = Fernet(self.key)
                self.decrypted_lines = []
                for line in lines:
                    if line.strip():
                        try:
                            msg = fernet.decrypt(line.strip()).decode()
                            self.decrypted_lines.append(msg)
                        except Exception:
                            self.decrypted_lines.append(f"[Decryption Failed]")
                self.display_logs(self.decrypted_lines)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt log: {e}")

    def display_logs(self, logs):
        self.viewer_text_area.delete(1.0, tk.END)
        self.viewer_text_area.insert(tk.END, "\n".join(logs))

    def search_logs(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            return
        filtered = [line for line in self.decrypted_lines if query in line.lower()]
        self.display_logs(filtered)

    def export_logs(self):
        if not self.decrypted_lines:
            messagebox.showinfo("Nothing to Export", "No logs loaded to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Decrypted Logs As")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.decrypted_lines))
                messagebox.showinfo("Exported", f"Logs saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export logs: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()