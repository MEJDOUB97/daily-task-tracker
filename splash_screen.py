import customtkinter as ctk
import threading
import time
from datetime import datetime

class SplashScreen:
    def __init__(self, main_app_callback):
        self.main_app_callback = main_app_callback
        self.splash = None
        self.progress_bar = None
        self.status_label = None
        
    def create_splash(self):
        """Create and show the splash screen"""
        # Create splash window
        self.splash = ctk.CTk()
        self.splash.title("Daily Task Tracker Pro")
        self.splash.geometry("500x350")
        self.splash.resizable(False, False)
        
        # Center the splash screen
        self.splash.eval('tk::PlaceWindow . center')
        
        # Remove window decorations for a modern look
        self.splash.overrideredirect(True)
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Main container with rounded corners
        main_frame = ctk.CTkFrame(self.splash, corner_radius=20, fg_color=("gray90", "gray13"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # App icon/logo area
        logo_frame = ctk.CTkFrame(main_frame, corner_radius=15, height=80, fg_color="transparent")
        logo_frame.pack(fill="x", padx=30, pady=(30, 20))
        logo_frame.pack_propagate(False)
        
        # App title with icon
        title_label = ctk.CTkLabel(
            logo_frame, 
            text="📋 Daily Task Tracker Pro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Modern Task Management for Productive People",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60")
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Version and date info
        info_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        info_frame.pack(fill="x", padx=30, pady=10)
        
        version_label = ctk.CTkLabel(
            info_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        version_label.pack(side="left")
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=f"Today: {datetime.now().strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        date_label.pack(side="right")
        
        # Progress section
        progress_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=("gray85", "gray20"))
        progress_frame.pack(fill="x", padx=30, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Initializing...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "gray80")
        )
        self.status_label.pack(pady=(15, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=12,
            corner_radius=6
        )
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        # Loading animation dots
        self.dots_label = ctk.CTkLabel(
            progress_frame,
            text="●○○",
            font=ctk.CTkFont(size=16),
            text_color=("gray40", "gray60")
        )
        self.dots_label.pack(pady=(0, 10))
        
        # Footer with features
        features_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        features_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        features_text = "📅 Calendar Integration  •  📊 Progress Tracking  •  🎯 Smart Categories"
        features_label = ctk.CTkLabel(
            features_frame,
            text=features_text,
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")
        )
        features_label.pack()
        
        # Make splash stay on top
        self.splash.attributes('-topmost', True)
        
        return self.splash
    
    def update_progress(self, value, status_text):
        """Update progress bar and status"""
        if self.progress_bar and self.status_label:
            self.progress_bar.set(value)
            self.status_label.configure(text=status_text)
            self.splash.update()
    
    def animate_dots(self):
        """Animate loading dots"""
        dot_patterns = ["●○○", "○●○", "○○●", "●●○", "●●●"]
        pattern_index = 0
        
        while hasattr(self, 'splash') and self.splash and self.splash.winfo_exists():
            try:
                if self.dots_label:
                    self.dots_label.configure(text=dot_patterns[pattern_index])
                    pattern_index = (pattern_index + 1) % len(dot_patterns)
                    self.splash.update()
                time.sleep(0.3)
            except:
                break
    
    def loading_sequence(self):
        """Simulate loading sequence"""
        steps = [
            (0.1, "Loading libraries..."),
            (0.25, "Initializing database..."),
            (0.4, "Setting up interface..."),
            (0.6, "Loading calendar..."),
            (0.8, "Preparing workspace..."),
            (0.95, "Almost ready..."),
            (1.0, "Starting application...")
        ]
        
        for progress, status in steps:
            self.update_progress(progress, status)
            time.sleep(0.5)  # Simulate work being done
        
        # Small delay before launching main app
        time.sleep(0.5)
        
        # Launch main application
        self.launch_main_app()
    
    def launch_main_app(self):
        """Launch the main application and close splash"""
        try:
            # Close splash screen first
            if self.splash:
                self.splash.quit()  # Use quit() instead of destroy()
                self.splash.destroy()
            
            # Small delay to ensure splash is closed
            time.sleep(0.1)
            
            # Launch main app in the same process
            self.main_app_callback()
            
        except Exception as e:
            print(f"Error launching main app: {e}")
            # If splash still exists, close it
            if self.splash:
                try:
                    self.splash.destroy()
                except:
                    pass
    
    def show(self):
        """Show splash screen and start loading"""
        self.create_splash()
        
        # Start loading animation in separate thread
        loading_thread = threading.Thread(target=self.loading_sequence, daemon=True)
        loading_thread.start()
        
        # Start dots animation in separate thread
        dots_thread = threading.Thread(target=self.animate_dots, daemon=True)
        dots_thread.start()
        
        # Start the splash screen event loop
        self.splash.mainloop()

def main():
    """Main function to show splash and launch app"""
    def launch_task_tracker():
        """Launch the actual task tracker"""
        try:
            # Import and run the main app
            import task_tracker
            app = task_tracker.TaskTracker()
            app.run()
        except Exception as e:
            print(f"Failed to launch task tracker: {e}")
            import traceback
            traceback.print_exc()
    
    # Show splash screen
    try:
        splash = SplashScreen(launch_task_tracker)
        splash.show()
    except Exception as e:
        print(f"Splash screen error: {e}")
        # If splash fails, launch app directly
        launch_task_tracker()

if __name__ == "__main__":
    main()