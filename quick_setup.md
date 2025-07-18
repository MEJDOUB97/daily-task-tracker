# 🚀 Quick Setup - Create Desktop Shortcuts

This guide helps you create desktop shortcuts to launch Daily Task Tracker Pro without using the command line.

## 🪟 Windows Users

### Automatic Method (Recommended)
1. **Run the shortcut creator:**
   ```cmd
   python create_shortcuts.py
   ```

2. **If that doesn't work, use the batch file:**
   - Double-click `run_task_tracker.bat`
   - A desktop shortcut will be created automatically

### Manual Method
1. **Right-click on your desktop**
2. **Select "New" > "Shortcut"**
3. **Browse to your project folder and select `run_task_tracker.bat`**
4. **Name it "Daily Task Tracker Pro"**
5. **Click "Finish"**

### Pro Tips for Windows:
- 📌 **Pin to Taskbar:** Right-click the shortcut → "Pin to taskbar"
- 🎨 **Custom Icon:** Right-click shortcut → Properties → Change Icon
- ⚡ **Start Menu:** Copy shortcut to `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`

---

## 🍎 macOS Users

### Automatic Method (Recommended)
1. **Run the shortcut creator:**
   ```bash
   python3 create_shortcuts.py
   ```

2. **This creates a full macOS app in your Applications folder**

### Manual Method
1. **Make the script executable:**
   ```bash
   chmod +x run_task_tracker.sh
   ```

2. **Double-click `run_task_tracker.sh` to launch**

### Pro Tips for macOS:
- 🚀 **Spotlight Search:** The app will appear in Spotlight as "Daily Task Tracker Pro"
- 📌 **Dock:** Drag the app from Applications to your Dock
- 🎨 **Custom Icon:** Right-click app → Get Info → Drag new icon to the icon area

---

## 🐧 Linux Users

### Automatic Method (Recommended)
1. **Run the shortcut creator:**
   ```bash
   python3 create_shortcuts.py
   ```

2. **This creates both desktop and applications menu entries**

### Manual Method
1. **Make the script executable:**
   ```bash
   chmod +x run_task_tracker.sh
   ```

2. **Create a desktop file:**
   ```bash
   nano ~/Desktop/task-tracker.desktop
   ```

3. **Add this content:**
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Daily Task Tracker Pro
   Comment=Modern Task Management
   Exec=/path/to/your/project/run_task_tracker.sh
   Icon=applications-office
   Terminal=false
   Categories=Office;
   ```

4. **Make it executable:**
   ```bash
   chmod +x ~/Desktop/task-tracker.desktop
   ```

### Pro Tips for Linux:
- 🎯 **Application Menu:** The app will appear in your applications menu under "Office"
- 📌 **Panel:** Right-click the desktop icon → "Add to Panel"
- 🎨 **Custom Icon:** Edit the desktop file and change the Icon= line

---

## 🔧 What Each File Does

### `run_task_tracker.bat` (Windows)
- 🔍 **Checks if Python is installed**
- 📦 **Auto-installs CustomTkinter if missing**
- 🚀 **Launches the application**
- ❌ **Shows helpful error messages**

### `run_task_tracker.sh` (macOS/Linux)
- 🔍 **Checks for Python3/Python**
- 📦 **Auto-installs dependencies**
- 🎨 **Colorful terminal output**
- ❌ **Graceful error handling**

### `create_shortcuts.py` (All Platforms)
- 🖥️ **Detects your operating system**
- 🔗 **Creates appropriate shortcuts**
- 📁 **Places them in the right locations**
- 🎯 **Handles different OS conventions**

---

## 🚨 Troubleshooting

### "Python not found"
- **Windows:** Install Python from [python.org](https://python.org) and check "Add to PATH"
- **macOS:** Install Python3 using Homebrew: `brew install python3`
- **Linux:** Install via package manager: `sudo apt install python3` (Ubuntu/Debian)

### "Permission denied" (macOS/Linux)
```bash
chmod +x run_task_tracker.sh
chmod +x create_shortcuts.py
```

### "CustomTkinter not found"
The scripts will automatically install it, but you can also run:
```bash
pip install customtkinter
```

### "Can't find task_tracker.py"
Make sure you're running the scripts from the same folder as your `task_tracker.py` file.

---

## 🎉 Success!

Once set up, you can:
- 🖱️ **Double-click the desktop icon** to launch
- 🔍 **Search for "Daily Task Tracker Pro"** in your OS search
- 📌 **Pin to taskbar/dock** for quick access
- 🎯 **Launch from applications menu**

**No more command line needed!** Just click and go! 🚀

---

## 📞 Need Help?

If you encounter issues:
1. Check the console output for error messages
2. Ensure Python 3.8+ is installed
3. Try running `python task_tracker.py` manually first
4. Check the GitHub issues page for solutions

**Happy task tracking!** 📋✨