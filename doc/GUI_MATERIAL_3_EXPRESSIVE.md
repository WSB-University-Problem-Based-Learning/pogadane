# Pogadane - Material 3 Expressive GUI 🎨

## 🌟 Overview

The **Material 3 Expressive GUI** is the most modern, beautiful interface for Pogadane, built with **Flet** (Flutter-based). It brings Google's latest Material Design 3 with expressive, dynamic theming, smooth animations, and a truly native-feeling experience.

## ✨ Latest Enhancements (v1.1.0)

### 🎯 New Features

- **🎨 Custom Branded Icon**: Professional Pogadane icon in taskbar/dock
- **🌙 Complete Dark Mode**: Beautiful dark theme with adapted brand colors
- **✨ Comprehensive Animations**: Material 3 animations throughout UI
- **🔔 Enhanced Snackbars**: Contextual icons and floating notifications
- **🎭 Theme Toggle**: One-click switching between light/dark modes

See [GUI Enhancements Summary](GUI_ENHANCEMENTS_SUMMARY.md) for complete details.

## ✨ Material 3 Expressive Features

### 🎨 Design Philosophy
- **Material 3 Expressive**: Latest Google design language
- **Dynamic Color**: Adaptive color schemes
- **Smooth Animations**: Flutter-powered 60fps animations
- **Rounded Corners**: Consistent 12-16px radius throughout
- **Elevated Components**: Proper material elevation and shadows
- **Adaptive Layouts**: Responsive design for all screen sizes
- **Dual Themes**: Light and dark modes with brand colors

### 🌈 Visual Excellence
- 🎭 **True Material 3**: Not just inspired - actual Material 3 implementation
- 🌓 **Dark Mode**: Complete dark theme with adapted Pogadane colors
- 💫 **Micro-animations**: Delightful transitions and hover effects
- 🎯 **Consistent Spacing**: 4px/8px/16px/24px design grid
- 📐 **Typography Scale**: Material 3 type system
- 🎨 **Color Science**: Material You dynamic color
- 🎪 **Custom Icon**: Branded application icon

### 🚀 Modern Features
- ✅ **Native Feel**: Flutter-based rendering
- ✅ **Snackbar Notifications**: Material 3 feedback system with icons
- ✅ **File Pickers**: Native OS dialogs
- ✅ **Progress Indicators**: Animated progress bars
- ✅ **Chips & Cards**: Modern component library
- ✅ **Icon Buttons**: Material 3 icon button styles
- ✅ **Dropdowns**: Beautiful select menus
- ✅ **Switches**: Animated toggle switches
- ✅ **Theme Toggle**: Instant light/dark mode switching

## 🚀 Running the Material 3 Expressive GUI

### Desktop Application
```bash
python run_gui_flet.py
```

### Web Application (Experimental)
```bash
flet run src/pogadane/gui_flet.py --web
```

### Mobile (Future)
```bash
flet build apk  # Android
flet build ipa  # iOS
```

## 📱 Interface Overview

### 🎯 App Bar
- **Left**: Pogadane icon and title with version badge
- **Right**: Theme toggle, font size controls
- **Material 3**: Elevated app bar with proper shadow
- **Adaptive**: Changes color based on theme

### 📥 Input Section
**Material 3 Card Layout**
- **Text Field**: Multi-line input with helper text
- **Action Buttons**: 
  - "Dodaj Pliki" - Filled button (primary action)
  - "Rozpocznij Przetwarzanie" - Filled button (success color)
- **Queue Viewer**: Elevated list with individual file cards
- **Progress Bar**: Linear progress with percentage text

### 📑 Tabs

#### 1️⃣ Konsola (Console)
- **Large Text Area**: Read-only console with logs
- **Action Buttons**:
  - "Zapisz Log" - Filled tonal button
  - "Wyczyść" - Outlined button
- **Auto-scroll**: Latest messages always visible

#### 2️⃣ Wyniki (Results)
- **File Selector**: Material 3 dropdown with all processed files
- **Split View**: Two equal panels
  - Left: 📝 Transcription output
  - Right: 📌 Summary output
- **Scrollable**: Independent scroll for each panel

#### 3️⃣ Konfiguracja (Configuration)
- **Organized Sections**:
  - 🤖 Summary Settings (elevated card)
  - 🎙️ Transcription Settings (elevated card)
- **Field Types**:
  - Dropdowns for selections
  - Text fields for strings
  - Password fields with reveal button
  - File pickers with browse button
  - Switches for booleans
- **Save Button**: Large filled button at bottom

### 📊 Status Bar
- **Status Icon**: Checkmark (success) or spinner (processing)
- **Status Text**: Current operation message
- **File Count**: Number of files in queue

## 🎨 Material 3 Components Used

### Buttons
- **FilledButton**: Primary actions (blue)
- **FilledTonalButton**: Secondary actions (surface variant)
- **OutlinedButton**: Tertiary actions (outline only)
- **IconButton**: Icon-only actions (rounded)

### Input
- **TextField**: Single/multi-line text input
- **Dropdown**: Selection menus
- **Switch**: Boolean toggles
- **FilePicker**: Native file dialogs

### Layout
- **Container**: Padding, margins, backgrounds
- **Row/Column**: Flex layouts
- **ListView**: Scrollable lists
- **Tabs**: Tab navigation

### Feedback
- **SnackBar**: Temporary messages
- **ProgressBar**: Linear progress
- **Tooltip**: Hover information

## 🎯 Advantages Over Other GUIs

| Feature | Legacy (tkinter) | Material (CTk) | Material 3 (Flet) |
|---------|------------------|----------------|-------------------|
| **Framework** | ttkbootstrap | CustomTkinter | Flutter/Flet |
| **Design** | Bootstrap 5 | Material 2 | Material 3 ✅ |
| **Animations** | None | Limited | Full 60fps ✅ |
| **Theming** | Fixed | Basic | Dynamic ✅ |
| **Mobile** | ❌ | ❌ | ✅ Future |
| **Web** | ❌ | ❌ | ✅ Yes |
| **Native Feel** | ⚠️ OK | ⚠️ Good | ✅ Excellent |
| **Rendering** | tkinter | tkinter | Flutter ✅ |
| **File Pickers** | tkinter | tkinter | Native OS ✅ |
| **Snackbars** | Custom | Custom | Material 3 ✅ |
| **Performance** | Good | Good | Excellent ✅ |

## 🔧 Customization

### Change Primary Color
Edit `gui_flet.py`:
```python
self.page.theme = ft.Theme(
    color_scheme_seed=ft.colors.PURPLE,  # Change from BLUE
    use_material3=True,
)
```

Available colors: `BLUE`, `GREEN`, `PURPLE`, `RED`, `ORANGE`, `PINK`, etc.

### Force Theme Mode
```python
self.page.theme_mode = ft.ThemeMode.DARK  # or LIGHT
```

### Custom Font
```python
self.page.fonts = {
    "CustomFont": "path/to/font.ttf"
}
self.page.theme = ft.Theme(
    font_family="CustomFont",
)
```

## 🌐 Platform Support

### Desktop
- ✅ **Windows**: Native executable
- ✅ **macOS**: Native app bundle
- ✅ **Linux**: Native binary

### Web
- ✅ **Browser**: Run in any modern browser
- ✅ **PWA**: Install as progressive web app
- ✅ **Responsive**: Adapts to screen size

### Mobile (Future)
- 🔜 **Android**: APK/AAB packages
- 🔜 **iOS**: IPA packages
- 🔜 **Tablet**: Optimized layouts

## 🎬 Animations & Transitions

### Built-in Animations
- **Tab Switch**: 300ms smooth transition
- **Theme Toggle**: Animated color changes
- **Button Hover**: Ripple effect
- **Progress Bar**: Smooth value changes
- **Snackbar**: Slide-in from bottom
- **Dropdown**: Expand/collapse animation

### Performance
- **60fps**: Flutter's rendering engine
- **GPU Accelerated**: Hardware acceleration
- **Smooth Scrolling**: Native feel
- **Optimized**: Minimal resource usage

## 🛠️ Troubleshooting

### ImportError: No module named 'flet'
```bash
pip install flet>=0.24.0
```

### GUI doesn't open
Check if Flet runtime is installed:
```bash
flet --version
```

### Slow performance
Enable hardware acceleration in your graphics settings.

### Theme not changing
Flet uses system theme by default. Check your OS theme settings.

### File picker not working
Ensure you have proper permissions for file access.

## 📚 Resources

- **Flet Documentation**: https://flet.dev/docs/
- **Material 3 Guidelines**: https://m3.material.io/
- **Flutter Widgets**: https://docs.flutter.dev/ui/widgets
- **GitHub Discussions**: Report issues or request features

## 🎓 Learning Material 3

### Key Concepts
1. **Dynamic Color**: Colors adapt to content
2. **Elevation**: Surfaces at different heights
3. **State Layers**: Hover, pressed, focused states
4. **Motion**: Purposeful, expressive animations
5. **Typography**: Clear hierarchy and readability

### Design Tokens
- **Spacing**: 4, 8, 12, 16, 24, 32px
- **Radius**: 12, 16, 20, 24px
- **Elevation**: 0-5 levels
- **Animation**: 100, 200, 300ms durations

## 🚀 Future Features

### Planned
- [ ] Drag-and-drop file support
- [ ] Keyboard shortcuts (Ctrl+O, Ctrl+S)
- [ ] Advanced animations (page transitions)
- [ ] Result export wizard
- [ ] Batch templates manager
- [ ] Live transcription preview
- [ ] Audio waveform visualization
- [ ] Settings profiles
- [ ] Recent files list
- [ ] Dark/Light/Auto theme persistence

### Mobile Specific
- [ ] Touch gestures
- [ ] Pull-to-refresh
- [ ] Swipe actions
- [ ] Mobile-optimized layouts
- [ ] Offline mode
- [ ] Share functionality

## 💡 Tips

1. **Use System Theme**: Let OS control light/dark mode
2. **Resize Window**: Fully responsive - try different sizes
3. **Hover for Tooltips**: All buttons have helpful hints
4. **Keyboard Navigation**: Tab through fields efficiently
5. **Snackbar Messages**: Watch bottom for notifications
6. **Save Frequently**: Use Ctrl+S in config tab (future)

## 🎨 Design Philosophy

### Material 3 Expressive
- **Bold**: Strong visual hierarchy
- **Dynamic**: Adaptive to content and user
- **Personal**: Customizable and flexible
- **Accessible**: High contrast, large touch targets
- **Delightful**: Smooth, purposeful animations

### Why Flet?
- ✅ **True Material 3**: Not approximated - real Material components
- ✅ **Cross-platform**: One codebase, all platforms
- ✅ **Python**: No need to learn Dart/Flutter
- ✅ **Fast Development**: Hot reload, quick iterations
- ✅ **Modern**: Built for 2025 and beyond

## � Related Documentation

### Enhancement Guides
- [GUI Enhancements Summary](GUI_ENHANCEMENTS_SUMMARY.md) - Overview of all enhancements
- [Dark Mode Guide](DARK_MODE_GUIDE.md) - Complete dark mode reference
- [Animations Guide](ANIMATIONS_GUIDE.md) - Animation catalog and guidelines

### Design & Branding
- [Brand Colors](BRAND_COLORS.md) - Pogadane color palette and usage
- [Visual Design Comparison](VISUAL_DESIGN_COMPARISON.md) - Compare all GUI versions

### Getting Started
- [Quick Start Material 3](QUICK_START_MATERIAL_3.md) - Fast setup guide
- [GUI Comparison](GUI_COMPARISON_ALL.md) - Compare Legacy, Material Design, and Material 3
- [Material 3 Implementation](MATERIAL_3_EXPRESSIVE_IMPLEMENTATION.md) - Technical details

## �📝 License

Same as Pogadane main project. See LICENSE file.

---

**Experience the future of Pogadane! 🎉**

**Material 3 Expressive** - Beautiful. Fast. Modern. Now with Dark Mode & Animations!
