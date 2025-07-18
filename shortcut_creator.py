#!/usr/bin/env python3
"""
Dynamic Shortcut Creator for Daily Task Tracker Pro
This script intelligently creates shortcuts with dynamic path detection.
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path

class DynamicShortcutCreator:
    def __init__(self):
        self.system = platform.system()
        self.project_dir = os.getcwd()
        self.app_name = "Daily Task Tracker Pro"
        self.config_file = "shortcut_config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """Load or create configuration for dynamic shortcuts"""
        default_config = {
            "app_name": self.app_name,
            "main_files": ["task_tracker.py", "app.py", "main.py", "daily_task_tracker.py"],
            "launcher_files": {
                "windows": "run_task_tracker.bat",
                "macos": "run_task_tracker.sh",
                "linux": "run_task_tracker.sh"
            },
            "icon_preferences": ["app.ico", "icon.ico", "tasktracker.ico"],
            "categories": {
                "windows": "Productivity",
                "macos": "Productivity",
                "linux": "Office;ProductivityApp"
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
            except:
                pass
                
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
    
    def detect_main_file(self):
        """Dynamically detect the main application file"""
        for filename in self.config["main_files"]:
            if os.path.exists(filename):
                return filename
        return None
    
    def detect_python_command(self):
        """Dynamically detect Python command"""
        commands = ["python", "python3", "py"]
        
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                continue
        return None
    
    def get_launcher_script(self):
        """Get the appropriate launcher script for the current OS"""
        system_key = self.system.lower()
        if system_key == "darwin":
            system_key = "macos"
        
        return self.config["launcher_files"].get(system_key)
    
    def create_windows_shortcut(self):
        """Create dynamic Windows shortcut"""
        print("\n🔄 Attempting to create Windows shortcut...")
        
        try:
            # Try multiple methods for maximum compatibility
            methods = [
                ("COM Objects (pywin32)", self.create_windows_shortcut_com),
                ("VBS Script", self.create_windows_shortcut_vbs),
                ("PowerShell", self.create_windows_shortcut_powershell),
                ("Simple Batch", self.create_windows_shortcut_simple)
            ]
            
            for method_name, method in methods:
                try:
                    print(f"   Trying {method_name}...")
                    if method():
                        print(f"   ✅ Success with {method_name}")
                        return True
                except Exception as e:
                    print(f"   ❌ {method_name} failed: {e}")
                    continue
            
            print("   ❌ All methods failed")
            self.print_manual_instructions()
            return False
            
        except Exception as e:
            print(f"❌ Error creating Windows shortcut: {e}")
            self.print_manual_instructions()
            return False
    
    def create_windows_shortcut_com(self):
        """Create shortcut using COM objects"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
            
            # Detect target
            launcher = self.get_launcher_script()
            main_file = self.detect_main_file()
            
            if launcher and os.path.exists(launcher):
                target = os.path.join(self.project_dir, launcher)
            elif main_file:
                python_cmd = self.detect_python_command()
                target = f'"{python_cmd}" "{os.path.join(self.project_dir, main_file)}"'
            else:
                return False
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = self.project_dir
            shortcut.Description = f"{self.app_name} - Modern Task Management"
            
            # Try to set icon
            icon_path = self.find_icon()
            if icon_path:
                shortcut.IconLocation = icon_path
            
            shortcut.save()
            
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            return True
            
        except ImportError:
            # Try to install winshell and pywin32
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "winshell"])
                return self.create_windows_shortcut_com()
            except:
                return False
        except Exception:
            return False
    
    def create_windows_shortcut_vbs(self):
        """Create shortcut using VBS script"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
            
            # Detect target
            launcher = self.get_launcher_script()
            if launcher and os.path.exists(launcher):
                target = os.path.join(self.project_dir, launcher)
            else:
                main_file = self.detect_main_file()
                python_cmd = self.detect_python_command()
                if main_file and python_cmd:
                    target = f'"{python_cmd}" "{os.path.join(self.project_dir, main_file)}"'
                else:
                    return False
            
            vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target}"
oLink.WorkingDirectory = "{self.project_dir}"
oLink.Description = "{self.app_name} - Modern Task Management"
oLink.Save
'''
            
            vbs_file = "create_shortcut_temp.vbs"
            with open(vbs_file, "w") as f:
                f.write(vbs_script)
            
            result = subprocess.run(["cscript", "//nologo", vbs_file], 
                                  capture_output=True, text=True)
            os.remove(vbs_file)
            
            if result.returncode == 0:
                print(f"✅ Desktop shortcut created: {shortcut_path}")
                return True
            return False
            
        except Exception:
            return False
    
    def create_windows_shortcut_powershell(self):
        """Create shortcut using PowerShell"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
            
            launcher = self.get_launcher_script()
            if launcher and os.path.exists(launcher):
                target = os.path.join(self.project_dir, launcher)
            else:
                main_file = self.detect_main_file()
                python_cmd = self.detect_python_command()
                if main_file and python_cmd:
                    target = f'"{python_cmd}" "{os.path.join(self.project_dir, main_file)}"'
                else:
                    return False
            
            ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{target}"
$Shortcut.WorkingDirectory = "{self.project_dir}"
$Shortcut.Description = "{self.app_name} - Modern Task Management"
$Shortcut.Save()
'''
            
            result = subprocess.run(["powershell", "-Command", ps_script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Desktop shortcut created: {shortcut_path}")
                return True
            return False
            
        except Exception:
            return False
    
    def create_windows_shortcut_simple(self):
        """Create shortcut using simple file copy method"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # Check if launcher exists, if not create it
            launcher = self.get_launcher_script()
            if not launcher or not os.path.exists(launcher):
                print(f"   Creating launcher script: {launcher}")
                self.create_launcher_script()
                
            launcher_path = os.path.join(self.project_dir, launcher)
            
            if not os.path.exists(launcher_path):
                print(f"   ❌ Launcher script not found: {launcher_path}")
                return False
            
            # Create a simple batch file that calls the launcher
            shortcut_content = f'''@echo off
cd /d "{self.project_dir}"
call "{launcher}"
'''
            
            shortcut_path = os.path.join(desktop, f"{self.app_name}.bat")
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            
            print(f"✅ Simple batch shortcut created: {shortcut_path}")
            return True
            
        except Exception as e:
            print(f"   Simple method error: {e}")
            return False
    
    def create_launcher_script(self):
        """Create the launcher script if it doesn't exist"""
        launcher_name = self.get_launcher_script()
        if not launcher_name:
            return False
            
        launcher_path = os.path.join(self.project_dir, launcher_name)
        
        if self.system == "Windows":
            launcher_content = f'''@echo off
echo Starting {self.app_name}...
cd /d "{self.project_dir}"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install Python.
    pause
    exit /b 1
)

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing CustomTkinter...
    pip install customtkinter
)

python task_tracker.py
if %errorlevel% neq 0 (
    echo Application error occurred.
    pause
)
'''
        else:
            launcher_content = f'''#!/bin/bash
echo "Starting {self.app_name}..."
cd "{self.project_dir}"

if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python not found! Please install Python."
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

if ! $PYTHON_CMD -c "import customtkinter" &> /dev/null; then
    echo "Installing CustomTkinter..."
    $PYTHON_CMD -m pip install customtkinter --user
fi

$PYTHON_CMD task_tracker.py
'''
        
        try:
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            
            if self.system != "Windows":
                os.chmod(launcher_path, 0o755)
            
            print(f"   ✅ Created launcher script: {launcher_path}")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to create launcher script: {e}")
            return False
    
    def print_manual_instructions(self):
        """Print manual instructions as last resort"""
        print("\n📋 Manual Shortcut Creation Instructions:")
        print("=" * 50)
        print("1. Right-click on your desktop")
        print("2. Select 'New' → 'Shortcut'")
        print("3. In the location field, enter one of these:")
        
        # Option 1: Direct Python command
        main_file = self.detect_main_file()
        python_cmd = self.detect_python_command()
        if main_file and python_cmd:
            print(f"   Option 1: {python_cmd} \"{os.path.join(self.project_dir, main_file)}\"")
        
        # Option 2: Batch file
        launcher = self.get_launcher_script()
        if launcher:
            launcher_path = os.path.join(self.project_dir, launcher)
            print(f"   Option 2: {launcher_path}")
        
        print(f"4. Name it: '{self.app_name}'")
        print("5. Click 'Finish'")
        print("\n💡 You can also just double-click the .bat file directly!")
    
    def find_icon(self):
        """Find the best available icon"""
        for icon_name in self.config["icon_preferences"]:
            icon_path = os.path.join(self.project_dir, icon_name)
            if os.path.exists(icon_path):
                return icon_path
        
        # Use Python executable icon as fallback
        return sys.executable
    
    def create_shortcuts(self):
        """Main method to create shortcuts dynamically"""
        print(f"🔗 {self.app_name} - Dynamic Shortcut Creator")
        print("=" * 60)
        print(f"📱 Detected OS: {self.system}")
        print(f"📁 Project Directory: {self.project_dir}")
        
        # Detect application
        main_file = self.detect_main_file()
        if main_file:
            print(f"✅ Found main application: {main_file}")
        else:
            print("❌ No main application file found!")
            print(f"   Looking for: {', '.join(self.config['main_files'])}")
            return False
        
        # Detect Python
        python_cmd = self.detect_python_command()
        if python_cmd:
            print(f"✅ Found Python command: {python_cmd}")
        else:
            print("❌ Python not found in PATH!")
            return False
        
        # Create OS-specific shortcuts
        if self.system == "Windows":
            return self.create_windows_shortcut()
        elif self.system == "Darwin":
            return self.create_macos_shortcut()
        elif self.system == "Linux":
            return self.create_linux_shortcut()
        else:
            print(f"❌ Unsupported operating system: {self.system}")
            return False
    
    def create_macos_shortcut(self):
        """Create dynamic macOS application bundle"""
        print("macOS shortcut creation not implemented in this version")
        return False
    
    def create_linux_shortcut(self):
        """Create dynamic Linux desktop entry"""
        print("Linux shortcut creation not implemented in this version")
        return False

def main():
    creator = DynamicShortcutCreator()
    
    if creator.create_shortcuts():
        print("\n🎉 Dynamic shortcut creation complete!")
        print("\n💡 Features:")
        print("   • Automatically detects Python installation")
        print("   • Finds main application file dynamically")
        print("   • Uses best available shortcut creation method")
        print("   • Saves configuration for future use")
        print("   • Cross-platform compatibility")
    else:
        print("\n❌ Shortcut creation failed!")
        print("   Check the error messages above for details")

if __name__ == "__main__":
    main()