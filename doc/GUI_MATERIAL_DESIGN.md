# Pogadane - Material Design GUI

## 🎨 Overview

The new Material Design GUI for Pogadane provides a modern, clean, and intuitive interface built with CustomTkinter. It follows Google's Material Design 3 principles for a professional and user-friendly experience.

## ✨ Features

### Visual Design
- **Material Design 3**: Modern flat design with proper elevation and spacing
- **Dark/Light Theme**: Toggle between light and dark modes with one click
- **Responsive Layout**: Adapts to different window sizes
- **Card-Based UI**: Organized content in clean, separated sections
- **Rounded Corners**: Smooth, modern aesthetics throughout
- **Material Colors**: Carefully selected color palette for readability

### Functionality
- **Font Scaling**: A+/A- buttons for accessibility
- **Batch Processing**: Queue multiple files or YouTube URLs
- **Real-time Progress**: Visual progress bar with status updates
- **Tabbed Interface**: Organized into Console, Results, and Configuration
- **Tooltips**: Helpful hints on hover for all controls
- **Theme Persistence**: Remembers your theme preference

## 🚀 Running the Material Design GUI

### Option 1: Direct Launch
```bash
python run_gui_material.py
```

### Option 2: From Package
```bash
python -m pogadane.gui_material
```

### Option 3: Using the Legacy GUI
The original ttkbootstrap GUI is still available:
```bash
python gui.py
```

## 📋 Interface Sections

### Header
- **App Title**: "🎧 Pogadane" with version number
- **Theme Toggle**: 🌙 Switch between light/dark mode
- **Font Controls**: A-/A+ buttons for text size adjustment

### Input Section
- **File/URL Input**: Multi-line text area for batch input
- **Add Files Button**: Browse for audio files from your system
- **Process Button**: Start batch processing with visual feedback
- **Queue Display**: Shows all queued files with status
- **Progress Bar**: Real-time progress tracking

### Console Tab (🖥️ Konsola)
- **Live Output**: Real-time logs from processing
- **Save Log**: Export console output to text file
- **Clear Button**: Clear console for fresh start

### Results Tab (📊 Wyniki)
- **File Selector**: Dropdown to choose processed files
- **Split View**: Side-by-side transcription and summary
- **Copy/Export**: Easy access to results

### Configuration Tab (⚙️ Konfiguracja)
- **Scrollable Form**: All settings in organized sections
- **Summary Settings**: Configure AI model, language, providers
- **Transcription Settings**: Whisper model, language, paths
- **Save & Apply**: Persist changes to config.py

## 🎯 Key Improvements Over Legacy GUI

### Visual Polish
| Aspect | Legacy | Material Design |
|--------|--------|-----------------|
| Framework | ttkbootstrap | CustomTkinter |
| Design | Bootstrap-inspired | Material Design 3 |
| Theme Support | Fixed | Dynamic (Light/Dark) |
| Corners | Sharp | Rounded |
| Spacing | Standard | Optimized |
| Colors | Bootstrap palette | Material palette |

### User Experience
- ✅ **Better tooltips**: More informative and visually appealing
- ✅ **Smoother transitions**: Professional feel
- ✅ **Clearer hierarchy**: Better visual organization
- ✅ **Modern icons**: Emoji-based for universal recognition
- ✅ **Status feedback**: Clear communication of app state

### Technical Advantages
- **CustomTkinter**: Modern, actively maintained framework
- **Better scaling**: Improved DPI awareness
- **Performance**: Smoother rendering
- **Customization**: Easier to theme and modify
- **Cross-platform**: Consistent look on Windows, Mac, Linux

## 🛠️ Customization

### Changing Colors
Edit `gui_material.py` and modify the color theme:
```python
# Change default color theme
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
```

### Custom Theme
Create custom theme JSON and load it:
```python
ctk.set_default_color_theme("path/to/custom_theme.json")
```

### Font Customization
Modify font families in the widget creation:
```python
font=("Your Font", size, "bold")
```

## 🐛 Troubleshooting

### ImportError: No module named 'customtkinter'
Install CustomTkinter:
```bash
pip install customtkinter>=5.2.0
```

### Display Issues on High DPI
CustomTkinter automatically handles DPI scaling, but if you experience issues:
```python
# Force scaling factor (in gui_material.py)
ctk.set_widget_scaling(1.5)  # 150% scaling
ctk.set_window_scaling(1.5)  # 150% window scaling
```

### Theme Not Persisting
The theme toggle is session-based. To set default:
```python
# In gui_material.py, change:
ctk.set_appearance_mode("Dark")  # Force dark mode
```

## 📚 Resources

- **CustomTkinter Docs**: https://customtkinter.tomschimansky.com/
- **Material Design**: https://m3.material.io/
- **GitHub Issues**: Report bugs or request features

## 🔄 Migration from Legacy GUI

The Material Design GUI is a **drop-in replacement** with the same functionality:

1. **Same features**: All buttons, tabs, and functions preserved
2. **Same config**: Uses the same `config.py` file
3. **Same workflow**: Batch processing works identically
4. **Better UX**: Just looks and feels more modern

You can run both GUIs side-by-side and choose your preference.

## 🎨 Screenshots

### Light Mode
- Clean, professional appearance
- Easy on the eyes for long sessions
- High contrast for readability

### Dark Mode
- Modern dark theme
- Reduced eye strain in low light
- OLED-friendly

## 💡 Tips

1. **Use keyboard shortcuts**: Tab to navigate between fields
2. **Drag and drop**: (Future feature) Drop files directly into input area
3. **Save logs regularly**: Use the "Save Log" button to preserve output
4. **Configure once**: Save configuration and reuse for all projects
5. **Theme toggle**: Try both light and dark modes to find your preference

## 🚀 Future Enhancements

Planned improvements for the Material Design GUI:

- [ ] Drag-and-drop file support
- [ ] Keyboard shortcuts (Ctrl+O for open, Ctrl+S for save, etc.)
- [ ] Animation transitions between tabs
- [ ] Advanced result viewer with syntax highlighting
- [ ] Export results to various formats (PDF, DOCX, MD)
- [ ] Batch operation templates
- [ ] Multi-language UI support
- [ ] Custom color themes
- [ ] Window state persistence (size, position)
- [ ] Recent files quick access

## 📝 License

Same as Pogadane main project. See LICENSE file.

---

**Enjoy the new Material Design experience! 🎉**
