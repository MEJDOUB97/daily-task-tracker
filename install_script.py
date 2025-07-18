#!/usr/bin/env python3
"""
Daily Task Tracker Pro - Easy Installation Script
This script helps you install and set up the Daily Task Tracker Pro application.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print the installation banner"""
    print("=" * 60)
    print("📋 Daily Task Tracker Pro - Installation Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected - Compatible!")

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip is not installed. Please install pip first.")
        return False

def install_requirements():
    """Install required packages"""
    print("\n🔄 Installing dependencies...")
    
    requirements = ["customtkinter>=5.2.0"]
    
    for package in requirements:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--user"
            ])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        import customtkinter
        print("   ✅ CustomTkinter imported successfully")
        
        # Test if we can create the main app class
        with open("task_tracker.py", "r") as f:
            if "class TaskTracker:" in f.read():
                print("   ✅ Main application file found")
            else:
                print("   ❌ Main application file appears corrupted")
                return False
                
    except ImportError as e:
        print(f"   ❌ Import test failed: {e}")
        return False
    except FileNotFoundError:
        print("   ❌ task_tracker.py not found in current directory")
        return False
    
    return True

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if platform.system() != "Windows":
        return
        
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Task Tracker Pro.lnk")
        target = os.path.join(os.getcwd(), "task_tracker.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("   ✅ Desktop shortcut created")
    except ImportError:
        print("   ⚠️  Could not create desktop shortcut (pywin32 not available)")
    except Exception as e:
        print(f"   ⚠️  Could not create desktop shortcut: {e}")

def print_usage_instructions():
    """Print instructions on how to use the application"""
    print("\n" + "=" * 60)
    print("🎉 Installation Complete!")
    print("=" * 60)
    print()
    print("📖 How to run the application:")
    print("   1. Open terminal/command prompt")
    print("   2. Navigate to this directory")
    print("   3. Run: python task_tracker.py")
    print()
    print("🔧 Features included:")
    print("   • Beautiful modern interface with dark theme")
    print("   • Interactive calendar for date navigation")
    print("   • Task categories and priority levels")
    print("   • Progress tracking and statistics")
    print("   • Local SQLite database for data persistence")
    print()
    print("💡 Tips:")
    print("   • Use the calendar to navigate between dates")
    print("   • Set time estimates to track productivity")
    print("   • Use filters to focus on specific tasks")
    print("   • Your data is automatically saved locally")
    print()
    print("🐛 Issues or questions?")
    print("   • Check the README.md file")
    print("   • Visit: https://github.com/yourusername/daily-task-tracker")
    print()

def main():
    """Main installation function"""
    print_banner()
    
    # Check system requirements
    check_python_version()
    
    if not check_pip():
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        print("\n❌ Installation failed during dependency installation.")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed.")
        sys.exit(1)
    
    # Create shortcuts (Windows only)
    if platform.system() == "Windows":
        print("\n🔗 Creating desktop shortcut...")
        create_desktop_shortcut()
    
    # Print success message and instructions
    print_usage_instructions()

if __name__ == "__main__":
    main()