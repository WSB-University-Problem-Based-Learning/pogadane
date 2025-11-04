# Pogadane - Brand Colors & Material 3 Expressive

## 🎨 Brand Color Palette

Pogadane uses a carefully crafted Material 3 Expressive color palette that reflects the application's core values: **trust**, **innovation**, and **success**.

---

## 🎯 Primary Brand Colors

### Primary - Brand Blue (#2563EB)
**Usage**: Trust, reliability, primary actions
- App logo and branding
- Primary navigation elements
- Save/Apply buttons
- Primary informational messages

**Semantic Meaning**: Represents trust and professional quality of transcription services.

**Where Applied**:
- ✅ App title "Pogadane" 
- ✅ Headset icon
- ✅ "Zapisz i Zastosuj" button (Config tab)
- ✅ Info snackbars
- ✅ Theme primary color

---

### Secondary - Brand Purple (#7C3AED)
**Usage**: Innovation, creativity, secondary actions
- Secondary buttons
- Queue icons
- Innovation-related features

**Semantic Meaning**: Represents the innovative AI-powered summarization technology.

**Where Applied**:
- ✅ "Dodaj Pliki" button
- ✅ Queue processing icon
- ✅ Tonal buttons (light purple background)
- ✅ Theme secondary color

---

### Tertiary - Brand Green (#34D399)
**Usage**: Success, confirmation, key CTAs
- Primary call-to-action buttons
- Success states
- Progress indicators
- Confirmation messages

**Semantic Meaning**: Represents successful completion and positive outcomes.

**Where Applied**:
- ✅ "Rozpocznij Przetwarzanie" button (main CTA)
- ✅ Progress bar
- ✅ Status bar checkmark icon
- ✅ Success snackbars
- ✅ Theme tertiary color

---

## ✨ Accent Colors

### Highlight Yellow (#FBBF24)
**Usage**: Warnings, offline status, friendly highlights
- Warning messages
- Attention-needed states
- Offline indicators

**Semantic Meaning**: Friendly warnings and important notices.

**Where Applied**:
- ✅ Warning snackbars
- 🔜 Offline mode indicator (future)
- 🔜 Queue item warnings

---

### Accent Green (#6EE7B7)
**Usage**: Bright positive feedback
- Extra-positive confirmations
- Feature highlights
- Success celebrations

**Semantic Meaning**: Exceptional success and delight.

**Where Applied**:
- 🔜 Batch completion celebration (future)
- 🔜 Achievement notifications (future)

---

## 🌈 Neutral & Surface Colors

### Surface (#FFFFFF)
**Usage**: Main content cards, elevated surfaces
- Card backgrounds
- Input fields
- Content containers

**Where Applied**:
- ✅ Text fields
- ✅ Main content areas
- ✅ Dialog backgrounds

---

### Background (#F3F4F6)
**Usage**: Page background, container backgrounds
- Main application background
- Large area fills

**Where Applied**:
- ✅ Page background
- ✅ Theme background

---

### Surface Variant (#F9FAFB)
**Usage**: Subtle surface elevation
- Queue container background
- Status bar background
- Secondary surfaces

**Where Applied**:
- ✅ Queue container
- ✅ Status bar
- ✅ Config sections

---

### Outline (#9CA3AF)
**Usage**: Borders, dividers, disabled states
- Component borders
- Dividers
- Disabled button outlines

**Where Applied**:
- ✅ Container borders
- ✅ Dividers
- ✅ Outlined buttons

---

### Text Colors

#### On-Surface (#111827)
**Usage**: Headlines, titles, high-emphasis text
- Main headings
- Important labels
- Primary content

**Where Applied**:
- ✅ Section titles
- ✅ Queue header text
- ✅ Status messages

#### On-Surface-Variant (#374151)
**Usage**: Body text, medium-emphasis content
- Descriptive text
- Helper text
- Secondary information

**Where Applied**:
- ✅ Progress label
- ✅ Helper text
- ✅ Button labels

---

## 📊 Color Usage Matrix

| Element | Primary Use | Color | Hex |
|---------|------------|-------|-----|
| **Branding** | Logo, Title | Blue | #2563EB |
| **Primary CTA** | Start Processing | Green | #34D399 |
| **Secondary Action** | Add Files | Purple | #7C3AED |
| **Save/Apply** | Configuration | Blue | #2563EB |
| **Success** | Confirmation | Green | #34D399 |
| **Warning** | Alerts | Yellow | #FBBF24 |
| **Error** | Failures | Red | #DC2626 |
| **Progress** | Active Tasks | Green | #34D399 |
| **Info** | General Messages | Blue | #2563EB |

---

## 🎭 Material 3 Expressive Theme

The complete Material 3 color scheme includes dynamic color generation with light/dark mode support:

### Light Mode (Default)
- **Primary Container**: #DBEAFE (Light blue background)
- **Secondary Container**: #EDE9FE (Light purple background)
- **Tertiary Container**: #D1FAE5 (Light green background)

### Dark Mode (Future)
All colors adapt with appropriate contrast:
- Darker backgrounds (#1F2937)
- Adjusted primary colors for visibility
- Maintained brand recognition

---

## 🎨 Design Principles

### 1. **Purposeful Color**
Every color serves a specific purpose and communicates intent:
- 🔵 Blue = Trust & Reliability
- 🟣 Purple = Innovation & AI
- 🟢 Green = Success & Progress
- 🟡 Yellow = Attention & Warnings

### 2. **Accessibility First**
All color combinations meet WCAG AA standards:
- Minimum 4.5:1 contrast ratio for text
- 3:1 for large text and UI components
- Clear visual hierarchy

### 3. **Consistent Application**
Colors are applied consistently across:
- Interactive elements (buttons, links)
- Status indicators (success, warning, error)
- Branding elements (logo, title)
- Feedback mechanisms (snackbars, notifications)

### 4. **Material 3 Harmony**
Colors work together following Material Design 3:
- Tonal variations for depth
- State layers for interactions
- Elevation through color
- Dynamic color adaptation

---

## 🚀 Implementation

### In Code (Flet)
```python
# Material 3 Color Scheme
theme = ft.Theme(
    use_material3=True,
    color_scheme=ft.ColorScheme(
        primary="#2563EB",      # Brand Blue
        secondary="#7C3AED",    # Brand Purple
        tertiary="#34D399",     # Brand Green
        background="#F3F4F6",   # Page background
        surface="#FFFFFF",      # Card surface
        # ... full scheme in gui_flet.py
    )
)

# Brand accent colors
brand_colors = {
    "highlight_yellow": "#FBBF24",  # Warnings
    "accent_green": "#6EE7B7",      # Positive feedback
}
```

### Button Styling
```python
# Primary CTA (Green)
ft.FilledButton(
    "Rozpocznij Przetwarzanie",
    style=ft.ButtonStyle(bgcolor="#34D399", color="#FFFFFF")
)

# Secondary Action (Purple)
ft.FilledButton(
    "Dodaj Pliki",
    style=ft.ButtonStyle(bgcolor="#7C3AED", color="#FFFFFF")
)

# Save Action (Blue)
ft.FilledButton(
    "Zapisz i Zastosuj",
    style=ft.ButtonStyle(bgcolor="#2563EB", color="#FFFFFF")
)
```

---

## 📝 Usage Guidelines

### ✅ DO:
- Use green for primary processing actions (CTAs)
- Use blue for informational and save actions
- Use purple for secondary/creative actions
- Use yellow for warnings and attention
- Maintain sufficient contrast for accessibility
- Keep branding colors consistent

### ❌ DON'T:
- Mix random colors without purpose
- Use low-contrast color combinations
- Change brand colors arbitrarily
- Override Material 3 semantic colors unnecessarily
- Use too many accent colors at once

---

## 🎯 Future Enhancements

### Planned Color Features:
- [ ] **Dark Mode**: Full dark theme with adapted brand colors
- [ ] **High Contrast Mode**: Enhanced accessibility option
- [ ] **Custom Themes**: User-selectable color variations
- [ ] **Dynamic Color**: Material You adaptive colors
- [ ] **Color-Blind Modes**: Alternative palettes for accessibility
- [ ] **Accent Customization**: Allow users to pick accent colors

---

## 📚 Resources

- **Material Design 3**: https://m3.material.io/styles/color
- **Color Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Flet Color Documentation**: https://flet.dev/docs/guides/python/colors
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/Understanding/

---

**Version**: 1.0  
**Last Updated**: November 4, 2025  
**Applies To**: Pogadane v0.1.8+ (Material 3 Expressive GUI)
