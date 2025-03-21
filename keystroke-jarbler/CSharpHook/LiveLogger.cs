using System.IO.Pipes;
using System.Text;

class LiveLogger
{
    private static NamedPipeClientStream pipeClient;

    public static void Init()
    {
        try
        {
            pipeClient = new NamedPipeClientStream(".", "JarbleLogPipe", PipeDirection.Out);
            pipeClient.Connect(1000);
        }
        catch { }
    }

    public static void Log(string key)
    {
        try
        {
            if (pipeClient != null && pipeClient.IsConnected)
            {
                byte[] msg = Encoding.UTF8.GetBytes(key);
                pipeClient.Write(msg, 0, msg.Length);
            }
        }
        catch { }
    }
}