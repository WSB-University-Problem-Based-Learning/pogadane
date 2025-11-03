"""
Pogadane GUI Installer

User-friendly graphical installer for Pogadane with step-by-step wizard.
Handles all dependencies, configuration, and setup with visual feedback.

Usage:
    python tools/install_gui.py
"""

import sys
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import json
import webbrowser

# Try to import ttkbootstrap for better styling, fallback to standard ttk
try:
    import ttkbootstrap as ttk_bootstrap
    from ttkbootstrap.constants import *
    BOOTSTRAP_AVAILABLE = True
except ImportError:
    BOOTSTRAP_AVAILABLE = False

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


class InstallationStep:
    """Represents a single installation step."""
    
    def __init__(self, name, description, function, optional=False):
        self.name = name
        self.description = description
        self.function = function
        self.optional = optional
        self.status = "pending"  # pending, running, success, failed, skipped
        self.message = ""


class PogadaneInstallerGUI:
    """Main GUI installer application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pogadane Installer")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Installation state
        self.current_step = 0
        self.installation_running = False
        self.installation_cancelled = False
        
        # Configuration options
        self.install_ollama = tk.BooleanVar(value=True)
        self.install_faster_whisper = tk.BooleanVar(value=True)
        self.install_yt_dlp = tk.BooleanVar(value=True)
        self.install_transformers = tk.BooleanVar(value=False)
        self.install_whisper = tk.BooleanVar(value=False)
        self.install_dev_tools = tk.BooleanVar(value=False)
        
        # Setup UI
        self.setup_ui()
        
        # Define installation steps (will be populated based on selections)
        self.steps = []
        
    def setup_ui(self):
        """Create the user interface."""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text="🎙️ Pogadane Installation Wizard",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Audio transcription and AI-powered summaries",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack()
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
        
        # Main content area (will switch between pages)
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Bottom button area
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.back_button = ttk.Button(
            button_frame,
            text="← Back",
            command=self.go_back,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_installation
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Next →",
            command=self.go_next
        )
        self.next_button.pack(side=tk.RIGHT)
        
        # Show welcome page
        self.show_welcome_page()
    
    def clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_welcome_page(self):
        """Display welcome page."""
        self.clear_content()
        self.current_page = "welcome"
        
        # Welcome message
        welcome_text = ttk.Label(
            self.content_frame,
            text="Welcome to Pogadane!",
            font=("Segoe UI", 14, "bold")
        )
        welcome_text.pack(pady=20)
        
        info_frame = ttk.Frame(self.content_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        info_text = """
This installer will help you set up Pogadane with all necessary components:

✅ Python package dependencies
✅ External tools (yt-dlp, Faster-Whisper)
✅ AI models (Ollama, Transformers, or Google Gemini)
✅ Transcription engines (Faster-Whisper or Python Whisper)
✅ Configuration files

The installation process typically takes 5-15 minutes depending on 
your internet connection and selected options.

Requirements:
• Windows operating system
• Python 3.7 or newer
• Internet connection
• Approximately 2-5GB free disk space

Click "Next" to choose your installation options.
        """
        
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT,
            wraplength=700
        )
        info_label.pack(anchor=tk.W)
        
        self.back_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL, text="Next →")
    
    def show_options_page(self):
        """Display installation options page."""
        self.clear_content()
        self.current_page = "options"
        
        # Page title
        title = ttk.Label(
            self.content_frame,
            text="Choose Installation Options",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(pady=10)
        
        # Scrollable frame for options
        canvas = tk.Canvas(self.content_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Core Components
        core_label = ttk.Label(
            scrollable_frame,
            text="📦 Core Components (Required)",
            font=("Segoe UI", 11, "bold")
        )
        core_label.pack(anchor=tk.W, pady=(10, 5))
        
        core_info = ttk.Label(
            scrollable_frame,
            text="• Python packages (ttkbootstrap, google-generativeai, etc.)",
            font=("Segoe UI", 9)
        )
        core_info.pack(anchor=tk.W, padx=20)
        
        # Transcription Options
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        trans_label = ttk.Label(
            scrollable_frame,
            text="🎙️ Transcription Engine",
            font=("Segoe UI", 11, "bold")
        )
        trans_label.pack(anchor=tk.W, pady=(10, 5))
        
        fw_check = ttk.Checkbutton(
            scrollable_frame,
            text="Faster-Whisper (Recommended) - High quality, GPU support, ~1.5GB",
            variable=self.install_faster_whisper
        )
        fw_check.pack(anchor=tk.W, padx=20)
        
        whisper_check = ttk.Checkbutton(
            scrollable_frame,
            text="Whisper (Python) - Lightweight, pure Python, 75MB-3GB",
            variable=self.install_whisper
        )
        whisper_check.pack(anchor=tk.W, padx=20)
        
        # YouTube Support
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        yt_label = ttk.Label(
            scrollable_frame,
            text="📹 YouTube Support",
            font=("Segoe UI", 11, "bold")
        )
        yt_label.pack(anchor=tk.W, pady=(10, 5))
        
        yt_check = ttk.Checkbutton(
            scrollable_frame,
            text="yt-dlp - Download audio from YouTube videos",
            variable=self.install_yt_dlp
        )
        yt_check.pack(anchor=tk.W, padx=20)
        
        # AI Summarization
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ai_label = ttk.Label(
            scrollable_frame,
            text="🤖 AI Summarization (Choose at least one)",
            font=("Segoe UI", 11, "bold")
        )
        ai_label.pack(anchor=tk.W, pady=(10, 5))
        
        ollama_check = ttk.Checkbutton(
            scrollable_frame,
            text="Ollama (Recommended) - Best quality, multi-language, ~3GB",
            variable=self.install_ollama
        )
        ollama_check.pack(anchor=tk.W, padx=20)
        
        transformers_check = ttk.Checkbutton(
            scrollable_frame,
            text="Transformers - Lightweight, pure Python, English only, 300MB-1.6GB",
            variable=self.install_transformers
        )
        transformers_check.pack(anchor=tk.W, padx=20)
        
        gemini_info = ttk.Label(
            scrollable_frame,
            text="• Google Gemini - Configure API key later in settings (cloud-based)",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        gemini_info.pack(anchor=tk.W, padx=20)
        
        # Development Tools
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        dev_label = ttk.Label(
            scrollable_frame,
            text="🔧 Development Tools (Optional)",
            font=("Segoe UI", 11, "bold")
        )
        dev_label.pack(anchor=tk.W, pady=(10, 5))
        
        dev_check = ttk.Checkbutton(
            scrollable_frame,
            text="Install development dependencies (pytest, pylint, etc.)",
            variable=self.install_dev_tools
        )
        dev_check.pack(anchor=tk.W, padx=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Estimated size
        size_frame = ttk.Frame(self.content_frame)
        size_frame.pack(fill=tk.X, pady=10)
        
        self.size_label = ttk.Label(
            size_frame,
            text="Estimated download: Calculating...",
            font=("Segoe UI", 9, "italic")
        )
        self.size_label.pack()
        
        self.update_estimated_size()
        
        # Bind checkboxes to update size
        for var in [self.install_ollama, self.install_faster_whisper, 
                    self.install_transformers, self.install_whisper]:
            var.trace("w", lambda *args: self.update_estimated_size())
        
        self.back_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL, text="Install →")
    
    def update_estimated_size(self):
        """Update estimated download size based on selections."""
        size_mb = 50  # Base Python packages
        
        if self.install_faster_whisper.get():
            size_mb += 1500
        if self.install_whisper.get():
            size_mb += 150  # Base model
        if self.install_yt_dlp.get():
            size_mb += 10
        if self.install_ollama.get():
            size_mb += 3000
        if self.install_transformers.get():
            size_mb += 1600
        
        size_gb = size_mb / 1024
        
        if size_gb >= 1:
            self.size_label.config(text=f"Estimated download: ~{size_gb:.1f} GB")
        else:
            self.size_label.config(text=f"Estimated download: ~{size_mb} MB")
    
    def show_installation_page(self):
        """Display installation progress page."""
        self.clear_content()
        self.current_page = "installation"
        
        # Page title
        title = ttk.Label(
            self.content_frame,
            text="Installing Pogadane...",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(pady=10)
        
        # Progress frame
        progress_frame = ttk.Frame(self.content_frame)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress_label = ttk.Label(
            progress_frame,
            text="Preparing installation...",
            font=("Segoe UI", 10)
        )
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode="determinate",
            length=700
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Step list
        step_frame = ttk.LabelFrame(
            self.content_frame,
            text="Installation Steps",
            padding=10
        )
        step_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrolled text for step details
        self.step_text = scrolledtext.ScrolledText(
            step_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.step_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.step_text.tag_config("success", foreground="green")
        self.step_text.tag_config("error", foreground="red")
        self.step_text.tag_config("warning", foreground="orange")
        self.step_text.tag_config("info", foreground="blue")
        
        self.back_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Start installation in background thread
        self.prepare_installation_steps()
        threading.Thread(target=self.run_installation, daemon=True).start()
    
    def show_completion_page(self, success=True):
        """Display installation completion page."""
        self.clear_content()
        self.current_page = "completion"
        
        if success:
            # Success message
            title = ttk.Label(
                self.content_frame,
                text="✅ Installation Complete!",
                font=("Segoe UI", 16, "bold"),
                foreground="green"
            )
            title.pack(pady=20)
            
            message_text = """
Pogadane has been successfully installed!

Next steps:
1. Configure your settings in .config/config.py
2. If you installed Ollama, pull a model: ollama pull gemma3:4b
3. Run the GUI: python -m pogadane.gui

Would you like to:
            """
        else:
            # Failure message
            title = ttk.Label(
                self.content_frame,
                text="⚠️ Installation Incomplete",
                font=("Segoe UI", 16, "bold"),
                foreground="orange"
            )
            title.pack(pady=20)
            
            message_text = """
The installation encountered some issues, but you may still be able
to use Pogadane with manual configuration.

Please check the installation log above for details.

Options:
            """
        
        message = ttk.Label(
            self.content_frame,
            text=message_text,
            justify=tk.LEFT,
            font=("Segoe UI", 10)
        )
        message.pack(pady=10)
        
        # Action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(pady=20)
        
        if success:
            launch_button = ttk.Button(
                action_frame,
                text="🚀 Launch Pogadane GUI",
                command=self.launch_pogadane
            )
            launch_button.pack(pady=5, fill=tk.X)
        
        readme_button = ttk.Button(
            action_frame,
            text="📖 Open Documentation",
            command=self.open_readme
        )
        readme_button.pack(pady=5, fill=tk.X)
        
        config_button = ttk.Button(
            action_frame,
            text="⚙️ Open Configuration File",
            command=self.open_config
        )
        config_button.pack(pady=5, fill=tk.X)
        
        self.back_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL, text="Finish")
    
    def prepare_installation_steps(self):
        """Prepare list of installation steps based on user selections."""
        self.steps = []
        
        # Always check Python
        self.steps.append(InstallationStep(
            "Check Python",
            "Verifying Python installation and version",
            self.check_python
        ))
        
        # Always upgrade pip
        self.steps.append(InstallationStep(
            "Upgrade pip",
            "Updating pip to latest version",
            self.upgrade_pip
        ))
        
        # Always install core packages
        self.steps.append(InstallationStep(
            "Install Core Packages",
            "Installing required Python packages",
            self.install_core_packages
        ))
        
        # yt-dlp
        if self.install_yt_dlp.get():
            self.steps.append(InstallationStep(
                "Install yt-dlp",
                "Downloading yt-dlp for YouTube support",
                self.install_ytdlp,
                optional=True
            ))
        
        # Faster-Whisper
        if self.install_faster_whisper.get():
            self.steps.append(InstallationStep(
                "Install Faster-Whisper",
                "Downloading and extracting Faster-Whisper",
                self.install_fasterwhisper,
                optional=True
            ))
        
        # Whisper (Python)
        if self.install_whisper.get():
            self.steps.append(InstallationStep(
                "Install Whisper",
                "Installing OpenAI Whisper Python library",
                self.install_whisper_python,
                optional=True
            ))
        
        # Transformers
        if self.install_transformers.get():
            self.steps.append(InstallationStep(
                "Install Transformers",
                "Installing Hugging Face Transformers",
                self.install_transformers_lib,
                optional=True
            ))
        
        # Ollama
        if self.install_ollama.get():
            self.steps.append(InstallationStep(
                "Install Ollama",
                "Downloading Ollama installer",
                self.install_ollama_exe,
                optional=True
            ))
        
        # Dev tools
        if self.install_dev_tools.get():
            self.steps.append(InstallationStep(
                "Install Dev Tools",
                "Installing development dependencies",
                self.install_dev_packages,
                optional=True
            ))
        
        # Always update config
        self.steps.append(InstallationStep(
            "Update Configuration",
            "Updating configuration files with installed paths",
            self.update_config
        ))
        
        # Always verify
        self.steps.append(InstallationStep(
            "Verify Installation",
            "Checking all components",
            self.verify_installation
        ))
    
    def run_installation(self):
        """Run all installation steps."""
        self.installation_running = True
        total_steps = len(self.steps)
        
        for i, step in enumerate(self.steps):
            if self.installation_cancelled:
                self.log_message(f"\n❌ Installation cancelled by user\n", "error")
                self.root.after(0, lambda: self.show_completion_page(success=False))
                return
            
            # Update progress
            progress = int((i / total_steps) * 100)
            self.root.after(0, lambda p=progress: self.progress_bar.config(value=p))
            self.root.after(0, lambda s=step: self.progress_label.config(
                text=f"Step {i+1}/{total_steps}: {s.name}"))
            
            self.log_message(f"\n{'='*60}\n", "info")
            self.log_message(f"Step {i+1}/{total_steps}: {step.name}\n", "info")
            self.log_message(f"{step.description}\n", "info")
            self.log_message(f"{'='*60}\n", "info")
            
            # Run step
            step.status = "running"
            try:
                result = step.function()
                if result:
                    step.status = "success"
                    self.log_message(f"✅ {step.name} completed successfully\n", "success")
                else:
                    if step.optional:
                        step.status = "skipped"
                        self.log_message(f"⚠️ {step.name} skipped (optional)\n", "warning")
                    else:
                        step.status = "failed"
                        self.log_message(f"❌ {step.name} failed\n", "error")
                        self.root.after(0, lambda: self.show_completion_page(success=False))
                        return
            except Exception as e:
                step.status = "failed"
                step.message = str(e)
                self.log_message(f"❌ {step.name} failed: {e}\n", "error")
                if not step.optional:
                    self.root.after(0, lambda: self.show_completion_page(success=False))
                    return
        
        # All steps completed
        self.progress_bar.config(value=100)
        self.progress_label.config(text="Installation complete!")
        self.log_message(f"\n{'='*60}\n", "success")
        self.log_message("🎉 All installation steps completed!\n", "success")
        self.log_message(f"{'='*60}\n", "success")
        
        self.installation_running = False
        self.root.after(0, lambda: self.show_completion_page(success=True))
    
    def log_message(self, message, tag=""):
        """Add message to installation log."""
        def _log():
            self.step_text.insert(tk.END, message, tag)
            self.step_text.see(tk.END)
        
        self.root.after(0, _log)
    
    def run_command(self, command, description=""):
        """Run a shell command and log output."""
        if description:
            self.log_message(f"▶️ {description}\n")
        
        self.log_message(f"Command: {' '.join(command)}\n", "info")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Read output in real-time
            for line in process.stdout:
                self.log_message(line)
            
            process.wait()
            
            if process.returncode == 0:
                self.log_message(f"✅ Command completed successfully\n", "success")
                return True
            else:
                stderr_output = process.stderr.read()
                self.log_message(f"⚠️ Command returned code {process.returncode}\n", "warning")
                if stderr_output:
                    self.log_message(f"Error output:\n{stderr_output}\n", "error")
                return False
        except Exception as e:
            self.log_message(f"❌ Command failed: {e}\n", "error")
            return False
    
    # Installation step implementations
    
    def check_python(self):
        """Check Python version."""
        try:
            version_info = sys.version_info
            version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
            self.log_message(f"Python version: {version_str}\n")
            
            if version_info.major >= 3 and version_info.minor >= 7:
                self.log_message(f"✅ Python version is compatible\n", "success")
                return True
            else:
                self.log_message(f"⚠️ Python 3.7+ recommended, you have {version_str}\n", "warning")
                return True  # Still continue
        except Exception as e:
            self.log_message(f"❌ Failed to check Python: {e}\n", "error")
            return False
    
    def upgrade_pip(self):
        """Upgrade pip to latest version."""
        return self.run_command(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            "Upgrading pip"
        )
    
    def install_core_packages(self):
        """Install core Python packages."""
        requirements_file = project_root / "requirements.txt"
        if not requirements_file.exists():
            self.log_message(f"⚠️ requirements.txt not found, skipping\n", "warning")
            return True
        
        return self.run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            "Installing core packages from requirements.txt"
        )
    
    def install_ytdlp(self):
        """Install yt-dlp."""
        # Import dependency manager
        try:
            from tools.dependency_manager import DependencyManager
            dm = DependencyManager()
            
            self.log_message("Downloading yt-dlp...\n")
            result = dm.install_yt_dlp()
            
            if result:
                self.log_message("✅ yt-dlp installed successfully\n", "success")
            return result
        except Exception as e:
            self.log_message(f"❌ Failed to install yt-dlp: {e}\n", "error")
            return False
    
    def install_fasterwhisper(self):
        """Install Faster-Whisper."""
        try:
            from tools.dependency_manager import DependencyManager
            dm = DependencyManager()
            
            self.log_message("Downloading Faster-Whisper (this may take a while)...\n")
            result = dm.install_faster_whisper()
            
            if result:
                self.log_message("✅ Faster-Whisper installed successfully\n", "success")
            return result
        except Exception as e:
            self.log_message(f"❌ Failed to install Faster-Whisper: {e}\n", "error")
            return False
    
    def install_whisper_python(self):
        """Install Whisper Python library."""
        requirements_file = project_root / "requirements-whisper.txt"
        if not requirements_file.exists():
            self.log_message(f"⚠️ requirements-whisper.txt not found\n", "warning")
            return False
        
        return self.run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            "Installing Whisper (Python)"
        )
    
    def install_transformers_lib(self):
        """Install Transformers library."""
        requirements_file = project_root / "requirements-transformers.txt"
        if not requirements_file.exists():
            self.log_message(f"⚠️ requirements-transformers.txt not found\n", "warning")
            return False
        
        return self.run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            "Installing Transformers"
        )
    
    def install_ollama_exe(self):
        """Install Ollama."""
        try:
            from tools.dependency_manager import DependencyManager
            dm = DependencyManager()
            
            self.log_message("Downloading Ollama installer...\n")
            result = dm.install_ollama()
            
            if result:
                self.log_message("✅ Ollama installer downloaded\n", "success")
                self.log_message("ℹ️ Please run the installer manually after this wizard completes\n", "info")
            return result
        except Exception as e:
            self.log_message(f"❌ Failed to download Ollama: {e}\n", "error")
            return False
    
    def install_dev_packages(self):
        """Install development packages."""
        requirements_file = project_root / "requirements-dev.txt"
        if not requirements_file.exists():
            self.log_message(f"⚠️ requirements-dev.txt not found, skipping\n", "warning")
            return True
        
        return self.run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            "Installing development tools"
        )
    
    def update_config(self):
        """Update configuration files."""
        self.log_message("Updating configuration...\n")
        
        config_file = project_root / ".config" / "config.py"
        if not config_file.exists():
            self.log_message("⚠️ Configuration file not found\n", "warning")
            return True
        
        # Update paths in config based on what was installed
        try:
            # Read current config
            config_text = config_file.read_text(encoding='utf-8')
            
            # Update paths if components were installed
            if self.install_faster_whisper.get():
                fw_path = project_root / "dep" / "faster-whisper" / "faster-whisper-xxl.exe"
                if fw_path.exists():
                    config_text = config_text.replace(
                        'FASTER_WHISPER_EXE = "faster-whisper-xxl.exe"',
                        f'FASTER_WHISPER_EXE = r"{fw_path}"'
                    )
                    self.log_message(f"Updated FASTER_WHISPER_EXE path\n", "success")
            
            if self.install_yt_dlp.get():
                yt_path = project_root / "dep" / "yt-dlp" / "yt-dlp.exe"
                if yt_path.exists():
                    config_text = config_text.replace(
                        'YT_DLP_EXE = "yt-dlp.exe"',
                        f'YT_DLP_EXE = r"{yt_path}"'
                    )
                    self.log_message(f"Updated YT_DLP_EXE path\n", "success")
            
            # Set default providers based on what was installed
            if self.install_whisper.get() and not self.install_faster_whisper.get():
                config_text = config_text.replace(
                    'TRANSCRIPTION_PROVIDER = "faster-whisper"',
                    'TRANSCRIPTION_PROVIDER = "whisper"'
                )
                self.log_message(f"Set default transcription provider to whisper\n", "info")
            
            if self.install_transformers.get() and not self.install_ollama.get():
                config_text = config_text.replace(
                    'SUMMARY_PROVIDER = "ollama"',
                    'SUMMARY_PROVIDER = "transformers"'
                )
                self.log_message(f"Set default summary provider to transformers\n", "info")
            
            # Write updated config
            config_file.write_text(config_text, encoding='utf-8')
            self.log_message("✅ Configuration updated\n", "success")
            return True
            
        except Exception as e:
            self.log_message(f"⚠️ Failed to update config: {e}\n", "warning")
            return True  # Non-critical
    
    def verify_installation(self):
        """Verify installation was successful."""
        self.log_message("Verifying installation...\n")
        
        success = True
        
        # Check Python packages
        try:
            import ttkbootstrap
            self.log_message("✅ ttkbootstrap installed\n", "success")
        except ImportError:
            self.log_message("⚠️ ttkbootstrap not installed\n", "warning")
        
        # Check installed files
        if self.install_faster_whisper.get():
            fw_path = project_root / "dep" / "faster-whisper" / "faster-whisper-xxl.exe"
            if fw_path.exists():
                self.log_message(f"✅ Faster-Whisper found at {fw_path}\n", "success")
            else:
                self.log_message(f"⚠️ Faster-Whisper not found\n", "warning")
        
        if self.install_yt_dlp.get():
            yt_path = project_root / "dep" / "yt-dlp" / "yt-dlp.exe"
            if yt_path.exists():
                self.log_message(f"✅ yt-dlp found at {yt_path}\n", "success")
            else:
                self.log_message(f"⚠️ yt-dlp not found\n", "warning")
        
        return True
    
    # Navigation methods
    
    def go_next(self):
        """Go to next page."""
        if self.current_page == "welcome":
            self.show_options_page()
        elif self.current_page == "options":
            # Validate at least one option selected
            if not any([
                self.install_ollama.get(),
                self.install_transformers.get(),
                self.install_faster_whisper.get(),
                self.install_whisper.get()
            ]):
                messagebox.showwarning(
                    "No Options Selected",
                    "Please select at least one transcription engine and one AI provider."
                )
                return
            
            self.show_installation_page()
        elif self.current_page == "completion":
            self.root.quit()
    
    def go_back(self):
        """Go to previous page."""
        if self.current_page == "options":
            self.show_welcome_page()
    
    def cancel_installation(self):
        """Cancel installation."""
        if self.installation_running:
            if messagebox.askyesno(
                "Cancel Installation",
                "Are you sure you want to cancel the installation?\n\n"
                "This may leave your installation in an incomplete state."
            ):
                self.installation_cancelled = True
                self.cancel_button.config(state=tk.DISABLED)
        else:
            if messagebox.askyesno(
                "Exit Installer",
                "Are you sure you want to exit the installer?"
            ):
                self.root.quit()
    
    # Action methods
    
    def launch_pogadane(self):
        """Launch Pogadane GUI."""
        try:
            subprocess.Popen(
                [sys.executable, "-m", "pogadane.gui"],
                cwd=project_root
            )
            self.root.quit()
        except Exception as e:
            messagebox.showerror(
                "Launch Failed",
                f"Failed to launch Pogadane:\n{e}"
            )
    
    def open_readme(self):
        """Open README file."""
        readme_path = project_root / "README.md"
        if readme_path.exists():
            webbrowser.open(str(readme_path))
        else:
            messagebox.showwarning("File Not Found", "README.md not found")
    
    def open_config(self):
        """Open configuration file."""
        config_path = project_root / ".config" / "config.py"
        if config_path.exists():
            # Try to open with default editor
            if sys.platform == "win32":
                os.startfile(str(config_path))
            else:
                webbrowser.open(str(config_path))
        else:
            messagebox.showwarning("File Not Found", "Configuration file not found")


def main():
    """Main entry point."""
    # Check if we're in the right directory
    if not (project_root / "src" / "pogadane").exists():
        messagebox.showerror(
            "Wrong Directory",
            "Please run this installer from the Pogadane project root directory."
        )
        sys.exit(1)
    
    # Create and run GUI
    if BOOTSTRAP_AVAILABLE:
        root = ttk_bootstrap.Window(themename="cosmo")
    else:
        root = tk.Tk()
    
    app = PogadaneInstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
