#!/usr/bin/env python3
"""
Professional Shortcut Creator - Creates clean, invisible shortcuts
This creates shortcuts using the invisible VBS launcher for a professional experience.
"""

import os
import sys

def create_professional_shortcut():
    """Create a professional, invisible shortcut"""
    print("🔗 Professional Shortcut Creator")
    print("=" * 35)
    
    # Get current directory and desktop
    current_dir = os.getcwd()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    print(f"📁 Current directory: {current_dir}")
    print(f"🖥️  Desktop path: {desktop}")
    
    # Check if task_tracker.py exists
    main_file = "task_tracker.py"
    if not os.path.exists(main_file):
        print(f"❌ {main_file} not found!")
        print("   Make sure you're running this from the correct folder.")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Found {main_file}")
    
    # Create the invisible VBS launcher
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
Dim scriptPath
scriptPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\\"))

' Change to the app directory and run Python script invisibly
' The 0 parameter means the window will be hidden completely
WshShell.Run "cmd /c cd /d """ & scriptPath & """ && python task_tracker.py", 0, False'''
    
    invisible_launcher = os.path.join(current_dir, "run_invisible.vbs")
    
    try:
        with open(invisible_launcher, "w") as f:
            f.write(vbs_content)
        print(f"✅ Created invisible launcher: {invisible_launcher}")
    except Exception as e:
        print(f"❌ Failed to create invisible launcher: {e}")
        return
    
    # Method 1: Create VBS shortcut (completely invisible)
    try:
        vbs_shortcut_content = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\Daily Task Tracker Pro.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{invisible_launcher}"
oLink.WorkingDirectory = "{current_dir}"
oLink.Description = "Daily Task Tracker Pro - Modern Task Management"
oLink.WindowStyle = 7
oLink.Save
WScript.Echo "Professional shortcut created successfully!"
'''
        
        vbs_file = "create_professional_shortcut.vbs"
        with open(vbs_file, "w") as f:
            f.write(vbs_shortcut_content)
        
        print("\n🔄 Creating professional .lnk shortcut...")
        import subprocess
        result = subprocess.run(["cscript", "//nologo", vbs_file], 
                              capture_output=True, text=True)
        
        os.remove(vbs_file)  # Clean up
        
        if result.returncode == 0:
            print("✅ Created professional .lnk shortcut on desktop!")
            print("   This shortcut runs completely invisibly - no console windows!")
        else:
            print(f"⚠️  .lnk creation had issues: {result.stderr}")
            
    except Exception as e:
        print(f"⚠️  VBS method failed: {e}")
    
    # Method 2: Also create a backup visible launcher
    try:
        visible_launcher_content = f'''@echo off
title Daily Task Tracker Pro
cd /d "{current_dir}"

REM Check dependencies
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install customtkinter --quiet
)

echo Loading Daily Task Tracker Pro...
python task_tracker.py 2>nul
'''
        
        visible_launcher = os.path.join(current_dir, "run_visible.bat")
        with open(visible_launcher, "w") as f:
            f.write(visible_launcher_content)
        
        print(f"✅ Created backup visible launcher: {visible_launcher}")
        
        # Create desktop shortcut for visible launcher too
        visible_shortcut_content = f'''@echo off
cd /d "{current_dir}"
call "{visible_launcher}"
'''
        
        visible_shortcut_path = os.path.join(desktop, "Daily Task Tracker Pro (Visible).bat")
        with open(visible_shortcut_path, "w") as f:
            f.write(visible_shortcut_content)
        
        print(f"✅ Created visible backup shortcut: {visible_shortcut_path}")
        
    except Exception as e:
        print(f"⚠️  Backup launcher creation failed: {e}")
    
    # Method 3: Instructions for manual creation
    print("\n📋 Manual Method (if needed):")
    print("1. Right-click on desktop → New → Shortcut")
    print(f"2. Target: {invisible_launcher}")
    print("3. Name: Daily Task Tracker Pro")
    
    print("\n🎉 Professional shortcut creation complete!")
    print("\n💡 You now have:")
    print("   📱 'Daily Task Tracker Pro.lnk' - Runs completely invisibly")
    print("   📱 'Daily Task Tracker Pro (Visible).bat' - Shows minimal loading info")
    print("   🔧 'run_invisible.vbs' - The invisible launcher")
    print("   🔧 'run_visible.bat' - The visible launcher")
    
    print("\n✨ Professional Features:")
    print("   • No console windows or warnings")
    print("   • Clean, commercial-style launch")
    print("   • Automatic dependency management")
    print("   • Multiple launch options")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    create_professional_shortcut()