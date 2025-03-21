using System;
using System.Windows.Forms;

public class MainForm : Form
{
    private Button toggleButton;
    private Label statusLabel;

    public MainForm()
    {
        toggleButton = new Button();
        toggleButton.Text = "Toggle obfuscation";
        toggleButton.Width = 200;
        toggleButton.Height = 40;
        toggleButton.Top = 20;
        toggleButton.Left = 50;
        toggleButton.Click += ToggleButton_Click;

        statusLabel = new Label();
        statusLabel.Width = 200;
        statusLabel.Height = 30;
        statusLabel.Top = 70;
        statusLabel.Left = 50;
        UpdateStatus();

        Controls.Add(toggleButton);
        Controls.Add(statusLabel);
        Text = "ObfusKey";
        Width = 300;
        Height = 160;
    }

    private void ToggleButton_Click(object sender, EventArgs e)
    {
        ObfusKey.Toggleobfuscation();
        UpdateStatus();
    }

    private void UpdateStatus()
    {
        statusLabel.Text = "Status: " + (ObfusKey.Isobfuscation() ? "ENABLED" : "DISABLED");
    }
}