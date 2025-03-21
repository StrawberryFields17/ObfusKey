using System;
using System.IO.Pipes;
using System.Text;
using System.Threading.Tasks;

class PipeServer
{
    public static void Start()
    {
        Task.Run(() =>
        {
            using (var server = new NamedPipeServerStream("JarblePipe", PipeDirection.In))
            {
                Console.WriteLine("Waiting for Python pipe...");
                server.WaitForConnection();
                Console.WriteLine("Python connected.");

                byte[] buffer = new byte[256];
                while (true)
                {
                    int bytesRead = server.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string message = Encoding.UTF8.GetString(buffer, 0, bytesRead).Trim();
                        Console.WriteLine("Received: " + message);
                        if (message == "TOGGLE_JARBLE")
                        {
                            ObfusKey.Toggleobfuscation();
                        }
                    }
                }
            }
        });
    }
}