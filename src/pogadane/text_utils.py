"""
Text processing utilities.

This module contains utility functions for text manipulation,
ANSI code stripping, and markdown rendering.
"""

import re
from typing import Tuple
from tkinter import Text, END, DISABLED, NORMAL


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape codes from text.
    
    Args:
        text: Text containing ANSI codes
        
    Returns:
        Clean text without ANSI codes
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return re.sub(ansi_escape, "", text)


def extract_transcription_and_summary(
    full_log: str,
    transcription_start: str = "--- POCZĄTEK TRANSKRYPCJI ---",
    transcription_end: str = "--- KONIEC TRANSKRYPCJI ---",
    summary_start: str = "--- POCZĄTEK STRESZCZENIA ---",
    summary_end: str = "--- KONIEC STRESZCZENIA ---"
) -> Tuple[str, str]:
    """
    Extract transcription and summary from log text using markers.
    
    Args:
        full_log: Complete log text
        transcription_start: Start marker for transcription
        transcription_end: End marker for transcription
        summary_start: Start marker for summary
        summary_end: End marker for summary
        
    Returns:
        Tuple of (transcription_text, summary_text)
    """
    transcription = "Nie znaleziono transkrypcji w logu."
    summary = "Nie znaleziono streszczenia w logu."
    
    # Extract transcription
    trans_start_idx = full_log.find(transcription_start)
    if trans_start_idx != -1:
        trans_end_idx = full_log.find(transcription_end, trans_start_idx + len(transcription_start))
        if trans_end_idx != -1:
            transcription = full_log[trans_start_idx + len(transcription_start):trans_end_idx].strip()
        else:
            transcription = full_log[trans_start_idx + len(transcription_start):].strip()
    
    # Extract summary
    summary_start_idx = full_log.find(summary_start)
    if summary_start_idx != -1:
        summary_end_idx = full_log.find(summary_end, summary_start_idx + len(summary_start))
        if summary_end_idx != -1:
            summary = full_log[summary_start_idx + len(summary_start):summary_end_idx].strip()
        else:
            summary = full_log[summary_start_idx + len(summary_start):].strip()
    
    return transcription, summary


def insert_with_markdown(text_widget: Text, text_content: str):
    """
    Insert text with basic markdown rendering into a Text widget.
    
    Supports:
    - Headers (# ## ###)
    - Bold (**text**)
    - Italic (*text*)
    - Bullet points (- * at line start)
    
    Args:
        text_widget: tkinter Text widget (must have .text attribute for ScrolledText)
        text_content: Markdown-formatted text content
    """
    # Handle ScrolledText wrapper
    actual_widget = getattr(text_widget, 'text', text_widget)
    
    actual_widget.config(state=NORMAL)
    actual_widget.delete("1.0", END)
    
    # Get font size
    try:
        font_size = actual_widget.cget("font").actual("size")
    except:
        font_size = 10
    
    # Configure tags
    actual_widget.tag_configure("bold", font=("Segoe UI", font_size, "bold"))
    actual_widget.tag_configure("italic", font=("Segoe UI", font_size, "italic"))
    actual_widget.tag_configure("h1", font=("Segoe UI", font_size + 4, "bold"), spacing1=10, spacing3=5)
    actual_widget.tag_configure("h2", font=("Segoe UI", font_size + 2, "bold"), spacing1=8, spacing3=4)
    actual_widget.tag_configure("bullet", lmargin1=20, lmargin2=35, font=("Segoe UI", font_size))
    
    # Process each line
    for line in text_content.splitlines():
        stripped_line = line.lstrip()
        
        # Headers
        if stripped_line.startswith("### "):
            actual_widget.insert(END, stripped_line[4:] + "\n", "h2")
        elif stripped_line.startswith("## "):
            actual_widget.insert(END, stripped_line[3:] + "\n", "h2")
        elif stripped_line.startswith("# "):
            actual_widget.insert(END, stripped_line[2:] + "\n", "h1")
        # Bullet points
        elif stripped_line.startswith("* ") or stripped_line.startswith("- "):
            actual_widget.insert(END, "• " + stripped_line[2:] + "\n", "bullet")
        # Regular text with inline formatting
        else:
            parts = re.split(r"(\*\*.*?\*\*|\*.*?\*)", line)
            for part in parts:
                if part.startswith("**") and part.endswith("**") and len(part) > 4:
                    actual_widget.insert(END, part[2:-2], "bold")
                elif part.startswith("*") and part.endswith("*") and len(part) > 2:
                    actual_widget.insert(END, part[1:-1], "italic")
                else:
                    actual_widget.insert(END, part)
            actual_widget.insert(END, "\n")
    
    actual_widget.config(state=DISABLED)


def is_valid_url(text: str) -> bool:
    """
    Check if text is a valid HTTP(S) URL.
    
    Args:
        text: Text to validate
        
    Returns:
        True if text starts with http:// or https://
    """
    return re.match(r'^https?://', text) is not None
