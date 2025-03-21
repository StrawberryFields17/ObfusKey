# 🛠️ Installation Guide: ObfusKey Suite

This guide helps you install and run the full ObfusKey suite, including:
- Python control and logging
- C# hook and GUI
- Live encryption
- Decrypted log viewer

---

## 🧰 Requirements

### 🪟 Windows Only
- This tool is designed for Windows OS (tested on Windows 10/11).

### ✅ C# Side
- .NET Framework 4.7+ or .NET 6+
- Visual Studio 2022 (or later)

### ✅ Python Side
Install Python 3.10+ from [python.org](https://www.python.org/).

Then open PowerShell or CMD:

```bash
pip install cryptography pywin32 psutil
```

---

## 🔋 Running Components

### 🔹 1. Build C# App
Open `CSharpHook/CSharpHook.csproj` in Visual Studio:
- Set `MainForm.cs` as the startup object
- Build and run
- You'll see a toggle GUI with current obfuscation status

### 🔹 2. Start Python Pipe Logger
```bash
cd PythonController
python pipe_logger_server.py
```

This listens for encrypted keystroke messages sent from the C# app.

### 🔹 3. Send Commands from Python
```bash
python pipe_client.py
# This sends TOGGLE_JARBLE to enable/disable protection
```

### 🔹 4. View Logs
```bash
python view_logs_gui.py
```
This launches a GUI for:
- Loading the AES key
- Viewing decrypted logs
- Searching for entries
- Exporting logs to plain text

---

## 📝 Notes
- All encrypted logs are stored in `encrypted_keystrokes.log`
- AES key is saved as `aes_key.key`
- Do not share your key or logs unencrypted!

---

## 📦 Optional Bundling
To create an installer:
- Use [Inno Setup](https://jrsoftware.org/isinfo.php) to bundle C# binaries and Python EXEs
- Use `pyinstaller` to convert Python scripts into `.exe`

Example:
```bash
pyinstaller --onefile pipe_logger_server.py
pyinstaller --onefile view_logs_gui.py
```

---

For questions or contributions, contact **Elementary-Penguin** 🐧