using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

class ObfusKey
{
    private static IntPtr _hookID = IntPtr.Zero;
    private static bool _jarbleEnabled = true;

    public static void Start()
    {
        _hookID = SetHook(HookCallback);
        Application.Run();
        UnhookWindowsHookEx(_hookID);
    }

    public static void Toggleobfuscation()
    {
        _jarbleEnabled = !_jarbleEnabled;
        Console.WriteLine("obfuscation is now " + (_jarbleEnabled ? "ENABLED" : "DISABLED"));
    }

    public static bool Isobfuscation()
    {
        return _jarbleEnabled;
    }

    private static IntPtr SetHook(LowLevelKeyboardProc proc)
    {
        using (Process curProcess = Process.GetCurrentProcess())
        using (ProcessModule curModule = curProcess.MainModule)
        {
            return SetWindowsHookEx(WH_KEYBOARD_LL, proc,
                GetModuleHandle(curModule.ModuleName), 0);
        }
    }

    private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam)
    {
        if (!_jarbleEnabled || nCode < 0 || wParam != (IntPtr)WM_KEYDOWN)
            return CallNextHookEx(_hookID, nCode, wParam, lParam);

        int vkCode = Marshal.ReadInt32(lParam);
        JarbleAndInject((ushort)vkCode);
        return (IntPtr)1; // Suppress original key
    }

    private static void JarbleAndInject(ushort vkCode)
    {
        Random rnd = new Random();
        Thread.Sleep(rnd.Next(15, 70));

        INPUT input = new INPUT
        {
            type = 1,
            U = new InputUnion
            {
                ki = new KEYBDINPUT
                {
                    wVk = vkCode,
                    dwFlags = 0
                }
            }
        };
        SendInput(1, new INPUT[] { input }, Marshal.SizeOf(typeof(INPUT)));
    }

    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;

    [DllImport("user32.dll")]
    private static extern IntPtr SetWindowsHookEx(int idHook,
        LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll")]
    private static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll")]
    private static extern IntPtr CallNextHookEx(IntPtr hhk,
        int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    private static extern uint SendInput(uint nInputs,
        INPUT[] pInputs, int cbSize);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto)]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    private struct INPUT
    {
        public uint type;
        public InputUnion U;
    }

    [StructLayout(LayoutKind.Explicit)]
    private struct InputUnion
    {
        [FieldOffset(0)]
        public KEYBDINPUT ki;
    }

    private struct KEYBDINPUT
    {
        public ushort wVk;
        public ushort wScan;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }
}