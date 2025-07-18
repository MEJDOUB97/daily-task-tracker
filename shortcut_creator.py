#!/usr/bin/env python3
"""
Shortcut Creator for Daily Task Tracker Pro
This script creates desktop shortcuts for easy access to the application.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def create_windows_shortcut():
    """Create a Windows desktop shortcut"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Daily Task Tracker Pro.lnk")
        
        # Path to the batch file
        batch_file = os.path.join(os.getcwd(), "run_task_tracker.bat")
        
        # Create the shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = batch_file
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable  # Use Python icon
        shortcut.Description = "Daily Task Tracker Pro - Modern Task Management"
        shortcut.save()
        
        print("✅ Desktop shortcut created successfully!")
        print(f"   Location: {shortcut_path}")
        
        # Also create in Start Menu
        try:
            start_menu = winshell.start_menu()
            start_shortcut = os.path.join(start_menu, "Daily Task Tracker Pro.lnk")
            
            shortcut2 = shell.CreateShortCut(start_shortcut)
            shortcut2.Targetpath = batch_file
            shortcut2.WorkingDirectory = os.getcwd()
            shortcut2.IconLocation = sys.executable
            shortcut2.Description = "Daily Task Tracker Pro - Modern Task Management"
            shortcut2.save()
            
            print("✅ Start Menu shortcut created successfully!")
            print(f"   Location: {start_shortcut}")
        except:
            print("⚠️  Could not create Start Menu shortcut")
            
    except ImportError:
        print("❌ pywin32 not available. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
            print("✅ pywin32 installed. Please run this script again.")
        except:
            print("❌ Could not install pywin32. Creating manual shortcut instructions...")
            print_manual_windows_instructions()
    except Exception as e:
        print(f"❌ Error creating shortcut: {e}")
        print_manual_windows_instructions()

def print_manual_windows_instructions():
    """Print manual instructions for Windows shortcut creation"""
    batch_file = os.path.join(os.getcwd(), "run_task_tracker.bat")
    
    print("\n📋 Manual Windows Shortcut Instructions:")
    print("=" * 50)
    print("1. Right-click on your desktop")
    print("2. Select 'New' > 'Shortcut'")
    print(f"3. Browse to and select: {batch_file}")
    print("4. Name it: 'Daily Task Tracker Pro'")
    print("5. Click 'Finish'")
    print("\n💡 You can also pin the .bat file to your taskbar!")

def create_macos_shortcut():
    """Create a macOS application bundle"""
    app_name = "Daily Task Tracker Pro"
    app_path = f"/Applications/{app_name}.app"
    
    try:
        # Create the app bundle structure
        contents_dir = f"{app_path}/Contents"
        macos_dir = f"{contents_dir}/MacOS"
        resources_dir = f"{contents_dir}/Resources"
        
        os.makedirs(macos_dir, exist_ok=True)
        os.makedirs(resources_dir, exist_ok=True)
        
        # Create Info.plist
        info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.tasktracker.dailytasktrackerpro</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
</dict>
</plist>"""
        
        with open(f"{contents_dir}/Info.plist", "w") as f:
            f.write(info_plist)
        
        # Create executable script
        script_content = f"""#!/bin/bash
cd "{os.getcwd()}"
./run_task_tracker.sh
"""
        
        script_path = f"{macos_dir}/{app_name}"
        with open(script_path, "w") as f:
            f.write(script_content)
        
        # Make it executable
        os.chmod(script_path, 0o755)
        
        print("✅ macOS application created successfully!")
        print(f"   Location: {app_path}")
        print("   You can now launch it from Applications folder or Spotlight")
        
    except Exception as e:
        print(f"❌ Error creating macOS app: {e}")
        print_manual_macos_instructions()

def print_manual_macos_instructions():
    """Print manual instructions for macOS"""
    script_path = os.path.join(os.getcwd(), "run_task_tracker.sh")
    
    print("\n📋 Manual macOS Instructions:")
    print("=" * 40)
    print("1. Open Terminal")
    print(f"2. Navigate to: {os.getcwd()}")
    print("3. Run: chmod +x run_task_tracker.sh")
    print("4. Double-click run_task_tracker.sh to launch")
    print("\n💡 You can also drag the .sh file to your dock!")

def create_linux_shortcut():
    """Create a Linux desktop entry"""
    try:
        desktop_dir = os.path.expanduser("~/Desktop")
        applications_dir = os.path.expanduser("~/.local/share/applications")
        
        # Desktop entry content
        desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Daily Task Tracker Pro
Comment=Modern Task Management Application
Exec={os.path.join(os.getcwd(), "run_task_tracker.sh")}
Icon=applications-office
Terminal=false
Categories=Office;ProductivityApp;
StartupNotify=true
Path={os.getcwd()}
"""
        
        # Create desktop shortcut
        if os.path.exists(desktop_dir):
            desktop_file = os.path.join(desktop_dir, "daily-task-tracker-pro.desktop")
            with open(desktop_file, "w") as f:
                f.write(desktop_entry)
            os.chmod(desktop_file, 0o755)
            print("✅ Desktop shortcut created successfully!")
            print(f"   Location: {desktop_file}")
        
        # Create applications menu entry
        os.makedirs(applications_dir, exist_ok=True)
        app_file = os.path.join(applications_dir, "daily-task-tracker-pro.desktop")
        with open(app_file, "w") as f:
            f.write(desktop_entry)
        os.chmod(app_file, 0o755)
        
        print("✅ Applications menu entry created successfully!")
        print(f"   Location: {app_file}")
        
    except Exception as e:
        print(f"❌ Error creating Linux shortcut: {e}")
        print_manual_linux_instructions()

def print_manual_linux_instructions():
    """Print manual instructions for Linux"""
    script_path = os.path.join(os.getcwd(), "run_task_tracker.sh")
    
    print("\n📋 Manual Linux Instructions:")
    print("=" * 40)
    print("1. Open Terminal")
    print(f"2. Navigate to: {os.getcwd()}")
    print("3. Run: chmod +x run_task_tracker.sh")
    print("4. Double-click run_task_tracker.sh to launch")
    print("\n💡 You can also create a custom .desktop file!")

def main():
    """Main function to create shortcuts based on the operating system"""
    print("🔗 Daily Task Tracker Pro - Shortcut Creator")
    print("=" * 50)
    
    # Detect operating system
    system = platform.system()
    print(f"📱 Detected OS: {system}")
    
    # Make sure shell scripts are executable on Unix systems
    if system in ["Darwin", "Linux"]:
        script_path = "run_task_tracker.sh"
        if os.path.exists(script_path):
            os.chmod(script_path, 0o755)
            print(f"✅ Made {script_path} executable")
    
    # Create shortcuts based on OS
    if system == "Windows":
        create_windows_shortcut()
    elif system == "Darwin":  # macOS
        create_macos_shortcut()
    elif system == "Linux":
        create_linux_shortcut()
    else:
        print(f"❌ Unsupported operating system: {system}")
        return
    
    print("\n🎉 Shortcut creation complete!")
    print("\n💡 Additional Tips:")
    print("   • You can pin shortcuts to your taskbar/dock")
    print("   • Right-click shortcuts to customize icons")
    print("   • The app will automatically install dependencies if needed")

if __name__ == "__main__":
    main()