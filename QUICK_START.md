# Pogadane - Quick Start Guide for Beginners
### Get transcriptions and summaries from audio files in minutes!

<img src="https://repository-images.githubusercontent.com/966910196/a983cd9b-5685-4635-a5b4-7ebeaef27d50" alt="Logo Pogadane" width="400"/>

---

## What is Pogadane?

**Pogadane** helps you turn long audio recordings (meetings, podcasts, YouTube videos) into **text transcripts** and **short summaries** - all on your computer, keeping your data private and secure!

**Perfect for:**
- 📝 Transcribing meeting recordings
- 🎧 Summarizing podcasts
- 🎬 Getting YouTube video transcripts
- 📚 Creating notes from lectures

---

## Before You Start - What You Need

✅ A Windows computer  
✅ Internet connection (for initial setup and downloading from YouTube)  
✅ About 30 minutes for first-time setup  
✅ At least 4GB free disk space  

**No programming experience needed!** Just follow these steps carefully.

---

## Step-by-Step Installation

### Part 1: Install Python (The Foundation)

Python is a programming language that Pogadane needs to run.

1. **Download Python:**
   - Go to: https://www.python.org/downloads/windows/
   - Click the big yellow button **"Download Python 3.x.x"**
   - Save the file to your Downloads folder

2. **Install Python:**
   - Find the downloaded file (usually `python-3.x.x-amd64.exe`)
   - **Double-click** to run it
   - ⚠️ **IMPORTANT:** Check the box that says **"Add Python to PATH"**
   - Click **"Install Now"**
   - Wait for installation to complete
   - Click **"Close"**

3. **Verify Python Works:**
   - Press `Windows Key + R`
   - Type `powershell` and press Enter
   - In the blue window that appears, type: `python --version`
   - You should see something like `Python 3.11.5`
   - ✅ If you see this, Python is installed correctly!

---

### Part 2: Download Pogadane Project

1. **Create a Folder:**
   - Open File Explorer
   - Go to your Documents folder
   - Right-click → New → Folder
   - Name it: `Pogadane`

2. **Download Project Files:**
   - Go to: https://github.com/WSB-University-Problem-Based-Learning/pogadane
   - Click the green **"Code"** button
   - Click **"Download ZIP"**
   - Save the file

3. **Extract Files:**
   - Find the downloaded `pogadane-main.zip` in your Downloads
   - Right-click → **"Extract All..."**
   - Choose to extract to your `Documents\Pogadane` folder
   - You should now have a `pogadane-main` folder inside `Pogadane`

---

### Part 3: Automatic Setup with Doctor Script

The easiest way to set up everything!

1. **Open PowerShell in Your Pogadane Folder:**
   - Open File Explorer
   - Navigate to `Documents\Pogadane\pogadane-main`
   - Hold `Shift` and right-click in empty space
   - Select **"Open PowerShell window here"**

2. **Run the Doctor Script:**
   - Type this command and press Enter:
     ```powershell
     python tools/pogadane_doctor.py
     ```
   - The script will:
     - ✅ Check your Python version
     - ✅ Install required Python libraries
     - ✅ Download latest project files
     - ✅ Create necessary folders

3. **Wait for Completion:**
   - You'll see green ✅ checkmarks as each step completes
   - This may take 2-5 minutes depending on your internet speed

---

### Part 4: Download Required Tools

You need two additional programs that work with Pogadane:

#### A. Download yt-dlp (For YouTube Videos)

1. Go to: https://github.com/yt-dlp/yt-dlp/releases/latest
2. Scroll down to "Assets"
3. Click on **`yt-dlp.exe`** to download
4. Move the downloaded `yt-dlp.exe` to your `Documents\Pogadane\pogadane-main` folder

#### B. Download Faster-Whisper (For Transcription)

1. Go to: https://github.com/Purfview/whisper-standalone-win/releases
2. Find **Faster-Whisper-XXL r245.4** (or newer)
3. Download **`Faster-Whisper-XXL_r245.4_windows.7z`**
4. You'll need **7-Zip** to extract it:
   - If you don't have 7-Zip, download from: https://www.7-zip.org/
   - Install 7-Zip first
5. Right-click the downloaded `.7z` file
6. Select **"7-Zip" → "Extract Here"**
7. Open the extracted folder → Find the `Faster-Whisper-XXL` subfolder
8. Copy `faster-whisper-xxl.exe` to your `Documents\Pogadane\pogadane-main` folder

---

### Part 5: Install Ollama (For AI Summaries)

Ollama runs AI models on your computer to create summaries.

1. **Download Ollama:**
   - Go to: https://ollama.com/
   - Click **"Download for Windows"**
   - Run the installer

2. **Download AI Model:**
   - After installing Ollama, open PowerShell
   - Type this command:
     ```powershell
     ollama pull gemma3:4b
     ```
   - This downloads the AI model (about 2.5 GB)
   - Takes 5-15 minutes depending on your internet speed

3. **Verify Ollama:**
   - Type: `ollama list`
   - You should see `gemma3:4b` in the list

---

## Your First Transcription!

Now let's test if everything works:

### Using the Graphical Interface (Easiest)

1. **Start Pogadane:**
   - Open PowerShell in your `Documents\Pogadane\pogadane-main` folder
   - Type:
     ```powershell
     python -m pogadane.gui
     ```
   - A window will open!

2. **Add a Test File:**
   - You can use the sample file included: `samples/Styrta się pali.mp3`
   - Click **"➕ Dodaj Pliki Audio"** button
   - Browse to `samples` folder
   - Select `Styrta się pali.mp3`
   - Click Open

3. **Configure Settings (First Time Only):**
   - Click the **"⚙️ Konfiguracja"** tab
   - Check these settings:
     - **Dostawca podsumowania:** should be `ollama`
     - **Model Ollama:** should be `gemma3:4b`
     - **Język transkrypcji:** `Polish` (or your language)
     - **Język podsumowania:** `Polish` (or your language)
   - Click **"💾 Zapisz i Zastosuj"**

4. **Start Processing:**
   - Go back to the main window
   - Click **"🚀 Rozpocznij Przetwarzanie Wsadowe"**
   - Watch the progress in the "Kolejka Przetwarzania" table
   - See detailed logs in the **"🖥️ Konsola"** tab

5. **View Results:**
   - Click the **"📊 Wyniki"** tab
   - Select your file from the dropdown
   - See the transcription on the left
   - See the AI summary on the right

**Congratulations! 🎉 You just transcribed and summarized your first audio file!**

---

## Common Tasks

### How to Process a YouTube Video

1. Copy the YouTube URL (e.g., `https://www.youtube.com/watch?v=example`)
2. In Pogadane GUI, paste the URL in the input field
3. Click **"🚀 Rozpocznij Przetwarzanie Wsadowe"**
4. Pogadane will:
   - Download the audio
   - Create a transcript
   - Generate a summary

### How to Process Multiple Files at Once

1. In the input field, add each file or URL on a **new line**:
   ```
   C:\Users\You\Documents\meeting1.mp3
   C:\Users\You\Documents\meeting2.mp3
   https://www.youtube.com/watch?v=example1
   https://www.youtube.com/watch?v=example2
   ```
2. Click **"🚀 Rozpocznij Przetwarzanie Wsadowe"**
3. Each file will be processed one by one
4. View individual results in the **"📊 Wyniki"** tab

### How to Change Font Size

- Click **"A+"** button to make text bigger
- Click **"A-"** button to make text smaller

### How to Save Your Results

1. Go to **"📊 Wyniki"** tab
2. Select a file from the dropdown
3. Copy the text you want (transcription or summary)
4. Paste into Word, Notepad, or any text editor
5. Save the file

---

## Troubleshooting

### "Python is not recognized..."
- You forgot to check "Add Python to PATH" during installation
- Reinstall Python and make sure to check that box!

### "No module named 'ttkbootstrap'"
- Run: `pip install ttkbootstrap google-generativeai`

### Transcription is in wrong language
- Open **"⚙️ Konfiguracja"** tab
- Change **"Język transkrypcji"** to your language
- Click **"💾 Zapisz i Zastosuj"**

### Summary is not working
- Make sure Ollama is running (check system tray)
- Verify the model is downloaded: `ollama list`
- Check **"⚙️ Konfiguracja"** → **"Dostawca podsumowania"** is set to `ollama`

### "File not found: faster-whisper-xxl.exe"
- In **"⚙️ Konfiguracja"** tab
- Click the **📂** button next to "Plik Faster Whisper"
- Browse to where you put `faster-whisper-xxl.exe`
- Click **"💾 Zapisz i Zastosuj"**

---

## Tips for Best Results

1. **Audio Quality Matters:**
   - Clear audio = better transcription
   - Minimize background noise
   - Use good microphone for recordings

2. **Language Settings:**
   - Always set the correct language in Configuration
   - For English content, use `English` in both fields

3. **First Run is Slower:**
   - Faster-Whisper downloads AI models on first use
   - This is normal and happens only once
   - Subsequent transcriptions are faster

4. **Save Your Configurations:**
   - After setting everything up in GUI
   - Your settings are saved automatically
   - Next time you won't need to configure again

---

## What's Next?

- **Try Different Prompt Templates:** In Configuration, experiment with different summary styles (Action Items, Key Topics, ELI5)
- **Use Speaker Diarization:** Enable "Włącz diaryzację" to identify different speakers in recordings
- **Explore Advanced Features:** Check the full README.md for command-line options

---

## Getting Help

- **Full Documentation:** See `README.md` in your project folder
- **Issues or Questions:** Visit https://github.com/WSB-University-Problem-Based-Learning/pogadane/issues
- **License Information:** See `doc/NOTICES.md` for third-party software licenses

---

## Privacy & Security

✅ **Your data stays on your computer** - When using Ollama, nothing is sent to the internet  
✅ **No accounts needed** - No sign-ups or registrations  
✅ **Open Source** - You can see exactly what the code does  

**Note:** If you choose to use Google Gemini API instead of Ollama, your transcripts will be sent to Google for processing. This requires an API key and internet connection.

---

**Enjoy using Pogadane! 🎉**

*This guide was created for absolute beginners. If you find any steps unclear, please let us know so we can improve it!*
