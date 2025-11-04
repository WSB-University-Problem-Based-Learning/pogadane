# Pogadane - Material 3 Expressive Design System

## Overview
Pogadane implements Google's Material Design 3 (M3) Expressive guidelines to create a modern, accessible, and visually appealing user interface. This document outlines the design tokens, patterns, and best practices used throughout the application.

---

## 🎨 Design Tokens

### Spacing Scale (8px Base Unit)
Following M3's 8-point grid system for consistent spatial rhythm:

```python
spacing = {
    "xs": 4px,    # Extra small - tight spacing between related elements
    "sm": 8px,    # Small - compact layouts, list items
    "md": 16px,   # Medium - default spacing, standard gaps
    "lg": 24px,   # Large - generous spacing, section padding
    "xl": 32px,   # Extra large - major section separation
    "xxl": 48px,  # Double XL - hero sections, page-level spacing
}
```

**Usage Guidelines:**
- Use `xs` (4px) for icon-text gaps, badge offsets
- Use `sm` (8px) for button groups, form field spacing
- Use `md` (16px) for card padding, list item spacing
- Use `lg` (24px) for container padding, section margins
- Use `xl` (32px) for page-level sections
- Use `xxl` (48px) for hero sections, major visual breaks

---

### Border Radius (M3 Expressive Curves)
Enhanced roundness for expressive, friendly interfaces:

```python
radius = {
    "none": 0px,     # Sharp edges for data tables, code blocks
    "sm": 8px,       # Small components (chips, tags)
    "md": 12px,      # Standard components (buttons, inputs)
    "lg": 16px,      # Cards, containers, dialogs
    "xl": 20px,      # Large cards, featured content
    "xxl": 28px,     # Hero elements, special highlights
    "full": 9999px,  # Pills, circular avatars
}
```

**M3 Expressive Principle:**
- More pronounced curves than M2 (which used 4px, 8px)
- Creates softer, more approachable visual language
- Balances modern aesthetics with usability

---

### Typography Scale
M3 Expressive type system with 15 distinct roles:

#### Display (Large headlines, hero sections)
- **Display Large**: 57px / 400 weight / 64px line height
- **Display Medium**: 45px / 400 weight / 52px line height
- **Display Small**: 36px / 400 weight / 44px line height

#### Headline (Section headers)
- **Headline Large**: 32px / 400 weight / 40px line height
- **Headline Medium**: 28px / 400 weight / 36px line height (App Bar title)
- **Headline Small**: 24px / 400 weight / 32px line height (Tab headers)

#### Title (Subsection headers)
- **Title Large**: 22px / 400 weight / 28px line height
- **Title Medium**: 16px / 500 weight / 24px line height (Card titles)
- **Title Small**: 14px / 500 weight / 20px line height (List headers)

#### Body (Content text)
- **Body Large**: 16px / 400 weight / 24px line height (Primary content)
- **Body Medium**: 14px / 400 weight / 20px line height (Secondary content)
- **Body Small**: 12px / 400 weight / 16px line height (Captions, meta)

#### Label (UI labels, buttons)
- **Label Large**: 14px / 500 weight / 20px line height (Buttons)
- **Label Medium**: 12px / 500 weight / 16px line height (Form labels)
- **Label Small**: 11px / 500 weight / 16px line height (Helper text)

**Implementation Example:**
```python
def get_text(text, style_key, **kwargs):
    style = design_tokens["typography"][style_key]
    return ft.Text(
        text,
        size=style["size"],
        weight=style["weight"],
        **kwargs
    )

# Usage
title = get_text("Pogadane", "headline_medium", color="#2563EB")
```

---

### Elevation System
Layered shadows for depth perception:

```python
elevation = {
    "0": "none",                                    # Flat surfaces
    "1": "0 1px 2px 0 rgb(0 0 0 / 0.05)",         # Subtle lift
    "2": "0 1px 3px 0 rgb(0 0 0 / 0.1)...",       # Cards at rest
    "3": "0 4px 6px -1px rgb(0 0 0 / 0.1)...",    # Raised cards
    "4": "0 10px 15px -3px rgb(0 0 0 / 0.1)...",  # Dialogs, dropdowns
    "5": "0 20px 25px -5px rgb(0 0 0 / 0.1)...",  # Modal overlays
}
```

**Elevation Hierarchy:**
1. **Level 0**: Background, base layer
2. **Level 1**: Buttons at rest, inactive elements
3. **Level 2**: Cards, contained elements
4. **Level 3**: Raised cards on hover, selected states
5. **Level 4**: App bars, dialogs, menus
6. **Level 5**: Modal dialogs, tooltips

---

### Motion System
Animation durations following M3 motion principles:

```python
motion = {
    "instant": 0ms,    # No animation
    "fast": 100ms,     # Quick feedback (button press, toggle)
    "medium": 200ms,   # Standard transitions (panel slide, fade)
    "slow": 300ms,     # Deliberate animations (dialog open, page transition)
    "slower": 500ms,   # Emphasized motion (loading states)
}
```

**Easing Curves:**
- **Standard**: General UI transitions
- **Decelerate**: Elements entering the screen
- **Accelerate**: Elements leaving the screen
- **Sharp**: Very fast, precise movements

---

### Icon Sizes

```python
icon_size = {
    "sm": 16px,   # Inline icons, decorative
    "md": 20px,   # Button icons, form icons
    "lg": 24px,   # App bar icons, primary actions
    "xl": 32px,   # Large touch targets
    "xxl": 48px,  # Hero icons, branding
}
```

---

## 🎨 Color System

### Light Theme
Based on Pogadane brand colors with M3 tonal palettes:

#### Primary (Brand Blue - Trust, Primary Actions)
- Primary: `#2563EB`
- On Primary: `#FFFFFF`
- Primary Container: `#DBEAFE`
- On Primary Container: `#1E3A8A`

#### Secondary (Brand Purple - Innovation)
- Secondary: `#7C3AED`
- On Secondary: `#FFFFFF`
- Secondary Container: `#EDE9FE`
- On Secondary Container: `#5B21B6`

#### Tertiary (Brand Green - Success, CTAs)
- Tertiary: `#34D399`
- On Tertiary: `#FFFFFF`
- Tertiary Container: `#D1FAE5`
- On Tertiary Container: `#047857`

#### Surfaces
- Background: `#F3F4F6` (Neutral gray)
- Surface: `#FFFFFF` (Pure white)
- Surface Variant: `#F9FAFB` (Subtle gray)

### Dark Theme
Adapted colors for dark mode with increased contrast:

#### Primary (Brighter for Readability)
- Primary: `#60A5FA`
- Primary Container: `#1E40AF`

#### Surfaces
- Background: `#111827` (Deep gray)
- Surface: `#1F2937` (Dark gray)
- Surface Variant: `#374151`

---

## 📐 Layout Patterns

### App Bar (Top Navigation)
- **Height**: Auto (content + padding)
- **Padding**: `24px horizontal, 16px vertical`
- **Background**: Surface color
- **Elevation**: Level 0 (separated by divider)
- **Content**: Logo + Title | Spacer | Action Icons

### Content Area
- **Padding**: `24px` (lg token)
- **Max Width**: Responsive (follows window size)
- **Background**: Background color

### Cards
- **Border Radius**: `16px` (lg token)
- **Padding**: `16px` or `24px` (md or lg)
- **Elevation**: Level 2 (at rest), Level 3 (hover)
- **Gap**: `16px` between cards

### Buttons
- **Primary**: FilledButton with brand blue
- **Secondary**: OutlinedButton
- **Tertiary**: TextButton
- **Border Radius**: `12px` (md token)
- **Padding**: `16px horizontal, 12px vertical`

### Dialogs
- **Border Radius**: `28px` (xxl token)
- **Padding**: `24px` (lg token)
- **Elevation**: Level 5
- **Max Width**: `600px` (optimal reading width)

---

## ♿ Accessibility

### Color Contrast
All color combinations meet WCAG 2.1 AA standards:
- **Normal Text**: 4.5:1 minimum contrast ratio
- **Large Text**: 3:1 minimum contrast ratio
- **UI Components**: 3:1 minimum contrast ratio

### Touch Targets
Minimum 48x48px for all interactive elements (M3 standard)

### Keyboard Navigation
All interactive elements are keyboard accessible with visible focus indicators

### Screen Readers
Semantic HTML and ARIA labels for assistive technologies

---

## 🎯 Component Patterns

### Input Fields
```python
ft.TextField(
    border_radius=design_tokens["radius"]["lg"],  # 16px
    filled=True,
    text_size=design_tokens["typography"]["body_large"]["size"],  # 16px
)
```

### Buttons
```python
ft.FilledButton(
    "Action",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=design_tokens["radius"]["md"]),  # 12px
        padding=ft.padding.symmetric(
            horizontal=design_tokens["spacing"]["lg"],  # 24px
            vertical=design_tokens["spacing"]["md"],     # 16px
        ),
        animation_duration=design_tokens["motion"]["fast"],  # 100ms
    ),
)
```

### Cards
```python
ft.Container(
    content=...,
    padding=design_tokens["spacing"]["lg"],      # 24px
    border_radius=design_tokens["radius"]["lg"],  # 16px
    border=ft.border.all(1, "#E5E7EB"),
)
```

---

## 📱 Responsive Breakpoints

Following M3 responsive guidelines:

- **Compact**: < 600px (Phone portrait)
- **Medium**: 600-840px (Phone landscape, small tablet)
- **Expanded**: > 840px (Tablet, desktop)

### Adaptive Layouts
- Compact: Single column, bottom navigation
- Medium: Two columns, side navigation
- Expanded: Multi-column, persistent navigation

---

## 🌐 Internationalization

### RTL Support
Layout automatically flips for right-to-left languages

### Dynamic Type
Font sizes scale with system accessibility settings

---

## 📚 References

- [Material Design 3 Guidelines](https://m3.material.io/)
- [M3 Color System](https://m3.material.io/styles/color/the-color-system/overview)
- [M3 Typography](https://m3.material.io/styles/typography/overview)
- [M3 Motion](https://m3.material.io/styles/motion/overview)
- [Pogadane Brand Guidelines](./BRAND_GUIDELINES.md)

---

## 🔄 Version History

- **v1.0.0** (Nov 2025): Initial M3 Expressive implementation
  - Complete design token system
  - Brand color integration
  - Typography scale
  - Motion system
  - Responsive layouts

---

**Last Updated**: November 4, 2025  
**Maintained by**: Pogadane Development Team
