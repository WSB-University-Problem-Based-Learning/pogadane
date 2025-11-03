"""
Pogadane - Setup Configuration

This setup.py enables proper installation of Pogadane as a Python package.
It handles Python dependencies and package structure, while external binaries
(faster-whisper-xxl.exe, yt-dlp.exe) are managed by tools/install.py.

Installation:
    pip install -e .                    # Development install
    pip install .                       # Regular install
    python tools/install.py             # Full installation with external tools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements from requirements.txt
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="pogadane",
    version="0.1.8",
    author="WSB University - Problem Based Learning",
    author_email="",
    description="Transform audio recordings and YouTube videos into transcripts and AI-powered summaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WSB-University-Problem-Based-Learning/pogadane",
    project_urls={
        "Bug Tracker": "https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues",
        "Documentation": "https://github.com/WSB-University-Problem-Based-Learning/pogadane/blob/main/README.md",
        "Source Code": "https://github.com/WSB-University-Problem-Based-Learning/pogadane",
    },
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Include non-Python files
    include_package_data=True,
    package_data={
        "pogadane": [
            "gui_utils/*.py",
        ],
        "": [
            ".config/config.py",
            "doc/*.md",
            "doc/cli_help/*.txt",
        ],
    },
    
    # Python version requirement
    python_requires=">=3.7",
    
    # Dependencies
    install_requires=requirements,
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "coverage>=7.2.0",
        ],
    },
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "pogadane-gui=pogadane.gui:main",
            "pogadane-cli=pogadane.transcribe_summarize_working:main",
            "pogadane-doctor=pogadane_doctor:main",
        ],
    },
    
    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    
    keywords="transcription summarization ai whisper youtube audio speech-to-text ollama gemini",
    
    zip_safe=False,
)
