using System;
using System.Windows.Forms;

static class Program
{
    [STAThread]
    static void Main()
    {
        PipeServer.Start();
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        ObfusKey.Start();
        Application.Run(new MainForm());
    }
}