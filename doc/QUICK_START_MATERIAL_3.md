# 🚀 Quick Start: Material 3 Expressive GUI

## One-Command Launch

```bash
python run_gui_flet.py
```

That's it! The beautiful Material 3 GUI will open.

## First-Time Setup

### 1. Install Dependencies
```bash
pip install flet>=0.24.0
```

### 2. Run the GUI
```bash
python run_gui_flet.py
```

## 🎨 What You'll See

### Beautiful Material 3 Interface
- 🎭 Smooth 60fps animations
- 🌓 Automatic theme detection (matches your OS)
- 💫 Delightful micro-interactions
- 🎯 Clean, modern design

### Three Main Sections

#### 1️⃣ Input Area (Top)
- Text field for files/URLs
- "Dodaj Pliki" button to browse
- "Rozpocznij Przetwarzanie" button to start

#### 2️⃣ Tabs (Middle)
- **Konsola**: See processing logs
- **Wyniki**: View transcriptions and summaries
- **Konfiguracja**: Adjust settings

#### 3️⃣ Status Bar (Bottom)
- Current status message
- File count

## 📝 Basic Usage

### Add Files
1. Click "Dodaj Pliki" button
2. Select audio files (MP3, WAV, M4A, etc.)
3. Files appear in the input field

### Or Add YouTube URLs
1. Paste YouTube URL in the text field
2. Each URL on a new line

### Start Processing
1. Click "Rozpocznij Przetwarzanie"
2. Watch progress in real-time
3. Check "Konsola" tab for logs
4. View results in "Wyniki" tab

### Configure Settings
1. Go to "Konfiguracja" tab
2. Adjust AI model, language, etc.
3. Click "Zapisz i Zastosuj"

## 🌙 Toggle Theme

Click the 🌗 icon in the top-right to switch between:
- ☀️ Light mode
- 🌙 Dark mode
- 🔄 Auto (system theme)

## 🔤 Change Font Size

Use the A-/A+ buttons in the top-right:
- **A-**: Make text smaller
- **A+**: Make text larger

## 💡 Tips

- **Hover** over buttons for helpful tooltips
- **Tab key** to navigate between fields
- **Smooth animations** make everything feel responsive
- **Notifications** appear at the bottom for important messages

## 🌐 Web Version (Experimental)

Want to run in your browser?

```bash
flet run src/pogadane/gui_flet.py --web
```

Opens in your default browser!

## 🆚 Try Other GUIs

### Material Design (CustomTkinter)
```bash
python run_gui_material.py
```

### Legacy Bootstrap
```bash
python -m pogadane.gui
```

See [GUI Comparison](GUI_COMPARISON_ALL.md) for differences.

## ❓ Troubleshooting

### GUI doesn't open?
```bash
# Reinstall Flet
pip install --upgrade flet
```

### Slow performance?
Enable GPU acceleration in your system settings.

### Theme issues?
The GUI follows your OS theme. Change it in system settings or use the theme toggle.

## 📚 Learn More

- [Full Documentation](GUI_MATERIAL_3_EXPRESSIVE.md)
- [Comparison with other GUIs](GUI_COMPARISON_ALL.md)
- [Main README](../README.md)

---

**Enjoy the Material 3 Expressive experience! 🎉**
