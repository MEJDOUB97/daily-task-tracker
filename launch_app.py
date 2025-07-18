#!/usr/bin/env python3
"""
Reliable App Launcher for Daily Task Tracker Pro
This launcher ensures the app starts properly with or without splash screen.
"""

import sys
import os
import time

def launch_with_splash():
    """Launch app with splash screen"""
    try:
        print("🎭 Starting with splash screen...")
        
        # Import splash screen
        from splash_screen import SplashScreen
        
        def start_main_app():
            """Start the main application"""
            try:
                # Try different import methods
                import importlib.util
                
                # Method 1: Direct module import
                try:
                    spec = importlib.util.spec_from_file_location("task_tracker", "task_tracker.py")
                    task_tracker_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(task_tracker_module)
                    
                    app = task_tracker_module.TaskTracker()
                    app.run()
                    return
                    
                except Exception as e1:
                    print(f"⚠️  Method 1 failed: {e1}")
                
                # Method 2: Add to path and import
                try:
                    sys.path.insert(0, os.getcwd())
                    import task_tracker
                    importlib.reload(task_tracker)  # Ensure fresh import
                    
                    app = task_tracker.TaskTracker()
                    app.run()
                    return
                    
                except Exception as e2:
                    print(f"⚠️  Method 2 failed: {e2}")
                
                # Method 3: Subprocess fallback
                print("🔄 Using subprocess fallback...")
                import subprocess
                result = subprocess.run([sys.executable, "task_tracker.py"], 
                                      cwd=os.getcwd())
                
            except Exception as e:
                print(f"❌ Error starting main app: {e}")
                import traceback
                traceback.print_exc()
        
        # Create and show splash
        splash = SplashScreen(start_main_app)
        splash.show()
        
    except Exception as e:
        print(f"❌ Splash screen failed: {e}")
        print("🔄 Falling back to direct launch...")
        launch_direct()

def launch_direct():
    """Launch app directly without splash"""
    try:
        print("🚀 Starting app directly...")
        
        # Method 1: Try subprocess (most reliable)
        try:
            import subprocess
            print("   Using subprocess method...")
            result = subprocess.run([sys.executable, "task_tracker.py"], 
                                  cwd=os.getcwd())
            if result.returncode == 0:
                print("✅ App launched successfully via subprocess")
                return
        except Exception as e1:
            print(f"   Subprocess method failed: {e1}")
        
        # Method 2: Try direct import
        try:
            print("   Using direct import method...")
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("task_tracker", "task_tracker.py")
            task_tracker_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(task_tracker_module)
            
            app = task_tracker_module.TaskTracker()
            app.run()
            return
            
        except Exception as e2:
            print(f"   Direct import method failed: {e2}")
        
        # Method 3: Add to path and import
        try:
            print("   Using path import method...")
            sys.path.insert(0, os.getcwd())
            import task_tracker
            
            app = task_tracker.TaskTracker()
            app.run()
            return
            
        except Exception as e3:
            print(f"   Path import method failed: {e3}")
        
        print("❌ All launch methods failed")
        
    except Exception as e:
        print(f"❌ Direct launch failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main launcher function"""
    print("📋 Daily Task Tracker Pro - Reliable Launcher")
    print("=" * 50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Check if main app exists
    if not os.path.exists("task_tracker.py"):
        print("❌ task_tracker.py not found!")
        print("   Make sure you're running this from the correct directory.")
        input("Press Enter to exit...")
        return
    
    # Check for splash screen
    has_splash = os.path.exists("splash_screen.py")
    print(f"🎭 Splash screen available: {'Yes' if has_splash else 'No'}")
    
    # Check dependencies
    try:
        import customtkinter
        print("✅ CustomTkinter available")
    except ImportError:
        print("⚠️  CustomTkinter not found, installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
            print("✅ CustomTkinter installed")
        except Exception as e:
            print(f"❌ Failed to install CustomTkinter: {e}")
            return
    
    # Launch based on availability and user preference
    if len(sys.argv) > 1 and sys.argv[1] == "--direct":
        print("🚀 Direct launch requested")
        launch_direct()
    elif has_splash:
        print("🎭 Launching with splash screen...")
        launch_with_splash()
    else:
        print("🚀 No splash screen, launching directly...")
        launch_direct()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Launch cancelled by user")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Keep console open if there was an error
        if len(sys.argv) > 1 and sys.argv[1] == "--pause":
            input("\nPress Enter to exit...")