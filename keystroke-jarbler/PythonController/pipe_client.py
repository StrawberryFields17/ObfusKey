import os
import time
import win32pipe
import win32file

PIPE_NAME = r'\\.\pipe\JarblePipe'

def send_message(message):
    try:
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        win32file.WriteFile(handle, message.encode())
        handle.close()
    except Exception as e:
        print("Error sending to pipe:", e)

# Example usage
if __name__ == '__main__':
    send_message("TOGGLE_JARBLE")