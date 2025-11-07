# Sample Audio Files

This directory contains sample audio files used for testing and demonstration of Pogadane's transcription capabilities.

## ⚠️ Important Legal Notice

**Sample files are NOT included in the Git repository or distributed with Pogadane.**

These files are sourced from YouTube and other platforms and are subject to their original creators' copyright. They are used locally for testing purposes only under fair use/educational use provisions.

## Sample Files Documentation

### Serial 1670 - Scena "Powrót do alkoholizmu"

- **Filename:** `serial1670-Powrót_do_alkoholizmu.mp3`
- **Source:** [YouTube Video](https://www.youtube.com/watch?v=StBTOpmUEjw)
- **Channel:** [Kurse.pl](https://www.youtube.com/@KursePl)
- **Published:** April 21, 2013
- **Views:** 9,576,891 (as of April 2013)
- **Duration:** ~4 minutes (scene excerpt)
- **Language:** Polish
- **Content:** Dramatic scene from Polish TV series "1670"
- **Copyright:** Original copyright holder (TV series producer)
- **Usage:** Local testing and demonstration only

**How to obtain:**
```bash
# Download using yt-dlp (included with Pogadane)
yt-dlp -x --audio-format mp3 -o "samples/serial1670-Powrót_do_alkoholizmu.mp3" "https://www.youtube.com/watch?v=StBTOpmUEjw"
```

### Styrta się pali

- **Filename:** `Styrta_się_pali.mp3`
- **Source:** YouTube (URL to be documented)
- **Language:** Polish
- **Usage:** Local testing and demonstration only

**How to obtain:**
```bash
# Download using yt-dlp or add manually
# Place audio file in this directory
```

## Legal Compliance

### For Developers

1. **Do NOT commit** audio files to Git repository
2. **Do NOT distribute** sample files with Pogadane releases
3. **Do NOT redistribute** these files without permission from copyright holders
4. Sample files are `.gitignore`d to prevent accidental commits

### For Users

1. **Download samples** using the commands above or manually from YouTube
2. **Personal use only** - these files are for testing Pogadane locally
3. **Respect copyright** - do not redistribute or use commercially without permission
4. **YouTube ToS compliance** - follow [YouTube Terms of Service](https://www.youtube.com/static?template=terms)

### Fair Use / Educational Use

Sample files are used under fair use provisions for:
- **Testing** speech recognition software functionality
- **Development** and debugging of transcription features
- **Demonstration** of Pogadane capabilities
- **Educational purposes** in learning Polish language processing

## Attribution

All sample files retain their original copyright. See `NOTICES.md` in the project root for complete attribution and licensing information.

## Adding Your Own Samples

To test Pogadane with your own audio:

1. Place audio files in this directory (supported: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`)
2. Run Pogadane GUI: `python run_gui_flet.py`
3. Add file path or use "➕ Dodaj Pliki Audio" button
4. Process and review transcription results

**Supported sources:**
- Local audio files (any format supported by FFmpeg)
- YouTube URLs (downloaded automatically)
- Direct audio URLs (downloaded automatically)

## Contact

If you have questions about sample file licensing or want to contribute properly licensed samples, please:
- File an issue: https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
- Contact project maintainers

---

**Last updated:** November 7, 2025
