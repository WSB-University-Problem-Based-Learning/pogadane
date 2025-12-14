"""
Creates a simple EXE launcher for Pogadane.

This script creates a minimal .exe file that launches 'python -m pogadane'.
No PyInstaller needed - uses built-in Windows tools.

Run from project root: python _dev/create_launcher.py
"""

import subprocess
import tempfile
import shutil
from pathlib import Path


def create_exe_launcher():
    """Create EXE launcher using PowerShell and .NET."""
    
    # Output to project root (parent of _dev)
    project_root = Path(__file__).parent.parent
    exe_path = project_root / "Pogadane.exe"
    
    # C# code for minimal launcher (compatible with older .NET)
    # Uses _app/.venv Python if available, falls back to system Python
    cs_code = r'''
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

class Program {
    static void Main() {
        string dir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        
        // Try _app/.venv Python first, then system Python
        string venvPython = Path.Combine(dir, "_app", ".venv", "Scripts", "python.exe");
        string pythonExe = File.Exists(venvPython) ? venvPython : "python";
        
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = pythonExe;
        psi.Arguments = "-m pogadane";
        psi.WorkingDirectory = dir;
        psi.UseShellExecute = false;
        psi.CreateNoWindow = false;
        try {
            Process p = Process.Start(psi);
            if (p != null) p.WaitForExit();
        } catch (Exception e) {
            Console.WriteLine("Error: " + e.Message);
            Console.WriteLine("Make sure Python is installed.");
            Console.WriteLine("Expected venv at: " + venvPython);
            Console.ReadKey();
        }
    }
}
'''
    
    # Use PowerShell to compile C# to EXE
    ps_script = f'''
$code = @"
{cs_code}
"@

Add-Type -TypeDefinition $code -OutputAssembly "{exe_path}" -OutputType ConsoleApplication
'''
    
    print("Creating Pogadane.exe launcher...")
    
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
        capture_output=True,
        text=True
    )
    
    if exe_path.exists():
        print(f"✓ Created: {exe_path.absolute()}")
        print(f"  Size: {exe_path.stat().st_size / 1024:.1f} KB")
        print("\nDouble-click Pogadane.exe to run the application!")
    else:
        print("✗ Failed to create EXE")
        if result.stderr:
            print(f"Error: {result.stderr}")
        print("\nAlternative: Use Pogadane.bat instead (works the same way)")


if __name__ == "__main__":
    create_exe_launcher()
