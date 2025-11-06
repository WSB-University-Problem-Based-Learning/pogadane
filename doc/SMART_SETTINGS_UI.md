# 🎨 Smart Settings UI - Conditional Visibility Design

## Overview

The settings dialog has been redesigned with **conditional visibility** - a UX pattern where only relevant options are shown based on the user's choices. This eliminates visual clutter and makes the interface more intuitive.

## Key Features

### 🎯 Provider-Based Conditional Display

#### **Transcription Provider**
When user selects a provider, only relevant options appear:

**faster-whisper** (selected):
- ⚡ Akcelerator Sprzętowy (auto/cuda/cpu)
- Batch Size
- Typ Obliczeń (auto/int8/float16/int8_float16)
- Voice Activity Detection (checkbox)

**whisper** (selected):
- 💡 Info box: "OpenAI Whisper używa domyślnych ustawień"

#### **Summary Provider**
Dynamic options based on AI provider:

**transformers** (Offline):
- 🤖 Model AI Transformers dropdown
  - 9 models: BART, DistilBART, FLAN-T5 (base/small/large), T5 (small/base/large), Gemma 2-2B
- 💡 Info: "Modele pobierane automatycznie przy pierwszym użyciu"
- Color theme: Blue (#EFF6FF)

**ollama** (Local Server):
- 🦙 Nazwa Modelu Ollama (text input)
- 💡 Helper text: "Przykład: gemma3:4b, llama3:8b, mistral:7b"
- 🔗 Link: "Zainstaluj: https://ollama.ai"
- Color theme: Purple (#FAF5FF)

**google** (Cloud API):
- 🔑 Klucz API Google Gemini (password field with reveal)
- 🌟 Model Gemini dropdown (flash/pro/gemini-pro)
- 💡 Helper: "Pobierz z: https://aistudio.google.com/app/apikey"
- ⚠️ Warning: "Wymaga połączenia z internetem"
- Color theme: Red (#FEF2F2)

## Implementation Architecture

### Core Methods

```python
def open_settings_dialog(self, e):
    """Creates smart settings with conditional containers"""
    - Main provider dropdowns with on_change handlers
    - Empty containers: transcription_settings_container, summary_settings_container
    - Initial build based on current provider values
    - Dialog stored in self.settings_dialog for updates

def build_transcription_settings(self, provider: str):
    """Builds provider-specific transcription UI"""
    - Clears container
    - Adds fields to self.config_fields dictionary
    - Populates container with styled sections
    - Calls page.update() if dialog exists

def build_summary_settings(self, provider: str):
    """Builds provider-specific summary UI"""
    - Clears container
    - Creates provider-specific controls
    - Color-coded sections per provider
    - Adds helpful context (icons, links, warnings)

def update_transcription_settings(self):
    """Triggered by provider dropdown on_change"""
    - Gets selected provider
    - Calls build_transcription_settings()

def update_summary_settings(self):
    """Triggered by provider dropdown on_change"""
    - Gets selected provider
    - Calls build_summary_settings()
```

### Data Flow

```
User selects provider → on_change event
    ↓
update_[transcription|summary]_settings()
    ↓
build_[transcription|summary]_settings(provider)
    ↓
1. Clear container.controls
2. Create provider-specific fields
3. Add to self.config_fields[key]
4. Populate container with styled UI
5. page.update()
```

### Configuration Persistence

The `save_config()` method remains unchanged:
- Iterates through `self.config_fields` dictionary
- Extracts values from all registered fields
- Preserves config.py structure and comments
- Only saves fields that were actually created (no null values)

## Visual Design

### Color Coding by Provider

| Provider | Background | Border | Icon Color | Purpose |
|----------|-----------|--------|-----------|----------|
| Transformers | #EFF6FF (Blue) | #93C5FD | #1D4ED8 | Offline/Local |
| Ollama | #FAF5FF (Purple) | #C4B5FD | #7C3AED | Local Server |
| Google | #FEF2F2 (Red) | #FCA5A5 | #DC2626 | Cloud API |
| Faster-Whisper | #FFFBEB (Yellow) | #FCD34D | #92400E | Performance |

### Spacing & Layout

```
Provider Dropdown (60px height)
    ↓ 8px spacing
Conditional Settings Container
    ↓ 8px spacing
Common Settings (Model, Language)
```

### Typography

- **Section Headers:** 16px, Bold, #1F2937
- **Subsection Headers:** 13px, Bold, Provider-specific color
- **Labels:** 14px, Provider dropdown / 13px, Other fields
- **Helper Text:** 11-12px, #6B7280, Italic
- **Info Text:** 11px, #6B7280

## Benefits

### 🧹 Reduced Clutter
- **Before:** 10+ fields visible simultaneously
- **After:** 3-5 relevant fields per provider
- **Reduction:** ~50-70% fewer visible controls

### 🎯 Improved Clarity
- Users see only what they need
- No confusion about which fields apply
- Clear visual indication of provider requirements

### 🚀 Better Onboarding
- New users aren't overwhelmed
- Provider-specific help text
- Contextual warnings and links

### ⚡ Faster Configuration
- Less scrolling required
- Immediate visual feedback
- Clear dependency relationships

## Example User Flows

### Flow 1: Switching to Google Gemini

```
1. User opens settings
2. Default: "Transformers" selected → shows model dropdown
3. User clicks "Summary Provider" → selects "Google"
4. UI instantly clears Transformers section
5. UI shows:
   - 🔑 API Key field (password with reveal)
   - 🌟 Gemini model dropdown
   - ⚠️ Internet requirement warning
   - 🔗 API key registration link
6. User enters API key
7. Saves → only relevant fields persisted
```

### Flow 2: Optimizing Faster-Whisper

```
1. User opens settings
2. "Faster-Whisper" already selected
3. UI automatically shows:
   - ⚡ Hardware accelerator
   - Batch size
   - Compute type
   - VAD filter
4. User adjusts settings with inline helpers
5. Saves → Whisper settings hidden, Faster-Whisper saved
```

## Technical Notes

### State Management

- **Provider state:** Stored in dropdown.value
- **Field references:** self.config_fields dictionary
- **Container references:** self.transcription_settings_container, self.summary_settings_container
- **Dialog reference:** self.settings_dialog (for page.update())

### Event Handling

```python
# Provider dropdown configuration
summary_provider_dropdown = ft.Dropdown(
    # ... other properties ...
    on_change=lambda _: self.update_summary_settings(),
)
```

The lambda captures self and triggers the update method when value changes.

### Field Registration

All created fields MUST be added to self.config_fields:

```python
self.config_fields["TRANSFORMERS_MODEL"] = model_dropdown
self.config_fields["OLLAMA_MODEL"] = ollama_model
self.config_fields["GOOGLE_API_KEY"] = api_key
self.config_fields["GOOGLE_GEMINI_MODEL"] = gemini_model
```

This ensures save_config() can persist all values.

### Container Management

```python
# Clear before rebuilding
self.summary_settings_container.controls.clear()

# Add new controls
self.summary_settings_container.controls = [
    ft.Container(...),  # New UI
]

# Refresh if dialog open
if hasattr(self, 'settings_dialog'):
    self.page.update()
```

## Future Enhancements

### Potential Additions

1. **Animated Transitions**
   - Fade-out old fields
   - Fade-in new fields
   - Smooth height transitions

2. **Provider Status Indicators**
   - ✅ Ready to use
   - ⚠️ Requires setup
   - 🔌 Offline/Online status

3. **Smart Defaults**
   - Auto-detect GPU capability
   - Suggest optimal batch size
   - Recommend models based on RAM

4. **Validation**
   - Test API keys before saving
   - Check Ollama server availability
   - Verify model accessibility

5. **Provider Help**
   - Click icon → opens setup guide
   - Inline video tutorials
   - Troubleshooting tips

## Testing Checklist

- [ ] Switch between all transcription providers
- [ ] Switch between all summary providers
- [ ] Verify fields save correctly for each provider
- [ ] Check that unused fields don't appear in config.py
- [ ] Test with missing GOOGLE_GEMINI_MODEL in config
- [ ] Verify helper text displays correctly
- [ ] Check color themes in light/dark mode
- [ ] Test keyboard navigation
- [ ] Verify password reveal works (Google API)
- [ ] Test rapid provider switching (no lag)

## Maintenance

### Adding New Providers

1. **Add to dropdown options** in `open_settings_dialog()`
2. **Create elif branch** in `build_summary_settings()`
3. **Define provider-specific fields**
4. **Add to self.config_fields**
5. **Style with unique color theme**
6. **Add helper text/warnings**
7. **Update this documentation**

### Adding Fields to Existing Provider

1. **Create field control** in appropriate `build_*_settings()` method
2. **Add to self.config_fields[key]**
3. **Add to container.controls list**
4. **Ensure config constant exists**
5. **Update helper text if needed**

---

**Status:** ✅ Implemented  
**Version:** 1.0  
**Date:** 2025-01-24  
**Author:** GitHub Copilot with User Feedback
