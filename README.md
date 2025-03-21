ObfusKey

A hybrid C# + Python security tool that protects against keyloggers by:

    Intercepting physical keyboard input.
    Suppressing it from normal OS channels.
    Re-injecting the same keys through software (SendInput) to confuse spyware.
    Securely encrypting keystrokes and optionally logging them.
    Providing a GUI interface and Python control layer.

📁 Project Structure

ObfusKey/
├── CSharpHook/              # C# project with low-level keyboard hook and GUI
│   ├── Program.cs           # Main launcher
│   ├── ObfusKey.cs           # Keyboard hook logic + key injection
│   ├── LiveLogger.cs        # Named pipe client for Python logging
│   ├── PipeServer.cs        # Receives control commands from Python
│   ├── MainForm.cs          # WinForms GUI with toggle/status
│   └── CSharpHook.csproj    # .NET project file
│
├── PythonController/
│   ├── aes_logger.py        # AES-encrypted keystroke logger
│   ├── pipe_client.py       # Sends commands to C# (e.g., toggle obfuscation)
│   ├── pipe_logger_server.py # Listens for logs from C# via named pipe
│   └── monitor.py           # Detects known keyloggers (future expansion)
│
├── shared/
│   └── config.json          # Settings and options (obfuscation, filtering)
│
└── README.md                # This file

 Features
1.  Secure Keyboard Hook

    Intercepts all key presses.
    Prevents propagation to OS through normal channels (making keyloggers blind).
    Re-injects keys using SendInput, simulating natural behavior.

2.  Named Pipe Control (Python → C#)

    Send TOGGLE_JARBLE command from Python to toggle protection.
    Fully decoupled control layer.

3.  GUI Interface (C#)

    Simple Windows Form with a toggle button.
    Live display of obfuscation status (ENABLED / DISABLED).

4.  AES-Encrypted Logging

    Logs keystrokes securely to encrypted_keystrokes.log.
    Uses Python's cryptography module (Fernet/AES-256).
    Includes timestamp for each keystroke.

5.  Live Logging (C# → Python)

    C# sends each re-injected keystroke to a Python pipe server.
    Pipe server writes them encrypted in real-time.
    Avoids local plaintext leaks.

 How To Run
1. Build and Run C# Hook

    Open CSharpHook.csproj in Visual Studio.
    Set MainForm.cs as startup object.
    Build and run.

2. Start Python Logging Server

cd PythonController
python pipe_logger_server.py

3. Send Control Commands (Optional)

python pipe_client.py
# Sends "TOGGLE_JARBLE" to C# app

Installer (optional)

You can package this using:

    pyinstaller for Python scripts → EXE
    Inno Setup / NSIS for bundling C# binary + Python layer into one installer
GUI Decrypted Log Viewer (planned)

    Future integration to view and decrypt logs from the GUI.

 Filtering and Detection (planned)

    Add keyword filters to ignore certain inputs (e.g., CTRL, ALT).
    Add keylogger detection logic in monitor.py.

 Security Notes

    This tool does not defend against kernel-level keyloggers.
    Best used on trusted systems or VMs to reduce attack surface.
 Requirements

C# Side

    Windows
    .NET Framework or .NET 6+

Python Side

pip install cryptography pywin32 psutil


