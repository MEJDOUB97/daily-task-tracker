#!/usr/bin/env python3
"""
Professional Shortcut Creator for Daily Task Tracker Pro
Creates clean shortcuts using existing launchers with splash screen option.
"""

import os
import sys
import subprocess

def create_professional_shortcuts():
    """Create professional shortcuts using existing files"""
    print("🔗 Daily Task Tracker Pro - Professional Shortcut Creator")
    print("=" * 65)
    
    # Get current directory and desktop
    current_dir = os.getcwd()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    print(f"📁 Project Directory: {current_dir}")
    print(f"🖥️  Desktop Path: {desktop}")
    
    # Check existing files
    files_to_check = {
        "task_tracker.py": "Main application",
        "splash_screen.py": "Splash screen",
        "run_invisible.vbs": "Invisible launcher",
        "run_task_tracker.bat": "Visible launcher"
    }
    
    print("\n🔍 Checking existing files:")
    existing_files = {}
    for filename, description in files_to_check.items():
        if os.path.exists(filename):
            print(f"   ✅ {filename} - {description}")
            existing_files[filename] = True
        else:
            print(f"   ❌ {filename} - {description} (missing)")
            existing_files[filename] = False
    
    if not existing_files["task_tracker.py"]:
        print("\n❌ Main application not found! Cannot create shortcuts.")
        input("Press Enter to exit...")
        return
    
    print("\n🎯 Choose your shortcut style:")
    print("1. 🎭 Professional with Splash Screen (Recommended)")
    print("2. 🚀 Instant Launch (No splash, direct start)")
    print("3. 📱 Both options")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice in ["1", "3"]:
        create_splash_shortcut(current_dir, desktop, existing_files)
    
    if choice in ["2", "3"]:
        create_instant_shortcut(current_dir, desktop, existing_files)
    
    print("\n🎉 Professional shortcut creation complete!")
    print("\n💡 Pro Tips:")
    print("   • Pin shortcuts to taskbar for quick access")
    print("   • Right-click shortcuts to customize icons")
    print("   • Shortcuts work even if you move the project folder")

def create_splash_shortcut(current_dir, desktop, existing_files):
    """Create shortcut with splash screen"""
    print("\n🎭 Creating Professional Splash Screen Shortcut...")
    
    if not existing_files["splash_screen.py"]:
        print("   ❌ Splash screen not found, skipping...")
        return
    
    try:
        # Update invisible launcher to use splash screen
        splash_vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
Dim scriptPath
scriptPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\\"))

' Run with beautiful splash screen (console hidden, GUI visible)
WshShell.Run "cmd /c cd /d """ & scriptPath & """ && python splash_screen.py", 0, False'''
        
        splash_launcher = os.path.join(current_dir, "launch_with_splash.vbs")
        with open(splash_launcher, "w") as f:
            f.write(splash_vbs_content)
        
        print(f"   ✅ Created splash launcher: {splash_launcher}")
        
        # Create professional shortcut
        shortcut_vbs = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\Daily Task Tracker Pro.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{splash_launcher}"
oLink.WorkingDirectory = "{current_dir}"
oLink.Description = "Daily Task Tracker Pro - Professional Task Management"
oLink.Save
'''
        
        temp_vbs = "temp_create_splash_shortcut.vbs"
        with open(temp_vbs, "w") as f:
            f.write(shortcut_vbs)
        
        result = subprocess.run(["cscript", "//nologo", temp_vbs], 
                              capture_output=True, text=True)
        os.remove(temp_vbs)
        
        if result.returncode == 0:
            print("   ✅ Professional splash shortcut created on desktop!")
            print("   🎭 Features: Beautiful loading screen + invisible console")
        else:
            print(f"   ⚠️  Shortcut creation had issues: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Failed to create splash shortcut: {e}")

def create_instant_shortcut(current_dir, desktop, existing_files):
    """Create instant launch shortcut"""
    print("\n🚀 Creating Instant Launch Shortcut...")
    
    try:
        # Choose best launcher
        if existing_files["run_invisible.vbs"]:
            launcher_path = os.path.join(current_dir, "run_invisible.vbs")
            launcher_type = "invisible VBS"
        elif existing_files["run_task_tracker.bat"]:
            launcher_path = os.path.join(current_dir, "run_task_tracker.bat")
            launcher_type = "batch file"
        else:
            # Create minimal launcher
            launcher_content = f'''@echo off
cd /d "{current_dir}"
python task_tracker.py 2>nul
'''
            launcher_path = os.path.join(current_dir, "quick_launch.bat")
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            launcher_type = "quick batch"
            print(f"   ✅ Created quick launcher: {launcher_path}")
        
        # Create instant shortcut
        shortcut_vbs = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\Daily Task Tracker Pro (Instant).lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{launcher_path}"
oLink.WorkingDirectory = "{current_dir}"
oLink.Description = "Daily Task Tracker Pro - Instant Launch"
oLink.Save
'''
        
        temp_vbs = "temp_create_instant_shortcut.vbs"
        with open(temp_vbs, "w") as f:
            f.write(shortcut_vbs)
        
        result = subprocess.run(["cscript", "//nologo", temp_vbs], 
                              capture_output=True, text=True)
        os.remove(temp_vbs)
        
        if result.returncode == 0:
            print(f"   ✅ Instant launch shortcut created using {launcher_type}!")
            print("   🚀 Features: Direct start + minimal/no console")
        else:
            print(f"   ⚠️  Shortcut creation had issues: {result.stderr}")
        
        # Also create simple batch shortcut as backup
        simple_shortcut_content = f'''@echo off
cd /d "{current_dir}"
python task_tracker.py
'''
        
        simple_shortcut_path = os.path.join(desktop, "Daily Task Tracker Pro (Simple).bat")
        with open(simple_shortcut_path, "w") as f:
            f.write(simple_shortcut_content)
        
        print(f"   ✅ Simple backup shortcut: {simple_shortcut_path}")
            
    except Exception as e:
        print(f"   ❌ Failed to create instant shortcut: {e}")

def main():
    """Main function"""
    try:
        create_professional_shortcuts()
    except KeyboardInterrupt:
        print("\n\n⚠️  Shortcut creation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()