import customtkinter as ctk
import sqlite3
from datetime import datetime, date, timedelta
import json
from tkinter import messagebox, filedialog
import calendar
import os
import threading
import time
import csv
from typing import List, Dict, Optional
import webbrowser

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TaskTracker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Daily Task Tracker Pro 2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Enhanced features
        self.current_selected_date = date.today()
        self.search_term = ""
        self.notifications_enabled = True
        self.auto_save_enabled = True
        self.theme_mode = "dark"
        
        # Timer functionality
        self.active_timer = None
        self.timer_task_id = None
        self.timer_start_time = None
        self.timer_running = False
        
        # Statistics
        self.productivity_data = []
        
        # Initialize database with enhanced schema
        self.init_enhanced_database()
        
        # Load settings
        self.load_settings()
        
        # Create enhanced GUI
        self.create_enhanced_widgets()
        
        # Load tasks for selected date
        self.load_tasks()
        
        # Start auto-save thread
        self.start_auto_save()
        
    def init_enhanced_database(self):
        """Initialize SQLite database with enhanced schema"""
        self.conn = sqlite3.connect('tasks_enhanced.db')
        self.cursor = self.conn.cursor()
        
        # Enhanced tasks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'Medium',
                category TEXT DEFAULT 'General',
                completed INTEGER DEFAULT 0,
                date_created DATE DEFAULT CURRENT_DATE,
                date_completed DATE,
                estimated_time INTEGER DEFAULT 30,
                actual_time INTEGER DEFAULT 0,
                tags TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                recurring_type TEXT DEFAULT 'none',
                recurring_interval INTEGER DEFAULT 0,
                parent_task_id INTEGER DEFAULT NULL,
                progress INTEGER DEFAULT 0,
                archived INTEGER DEFAULT 0
            )
        ''')
        
        # Time tracking table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration INTEGER,
                notes TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        # Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Productivity analytics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productivity_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                tasks_completed INTEGER,
                total_time_worked INTEGER,
                efficiency_score REAL,
                focus_score REAL
            )
        ''')
        
        self.conn.commit()
        
    def load_settings(self):
        """Load user settings from database"""
        self.cursor.execute('SELECT key, value FROM settings')
        settings = dict(self.cursor.fetchall())
        
        self.notifications_enabled = settings.get('notifications', 'true') == 'true'
        self.auto_save_enabled = settings.get('auto_save', 'true') == 'true'
        self.theme_mode = settings.get('theme', 'dark')
        
    def save_settings(self):
        """Save user settings to database"""
        settings = {
            'notifications': str(self.notifications_enabled).lower(),
            'auto_save': str(self.auto_save_enabled).lower(),
            'theme': self.theme_mode
        }
        
        for key, value in settings.items():
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
            ''', (key, value))
        self.conn.commit()
        
    def create_enhanced_widgets(self):
        """Create the enhanced GUI elements"""
        # Main container
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Enhanced header with toolbar
        self.create_enhanced_header(main_container)
        
        # Main content area with tabs
        self.create_tabbed_interface(main_container)
        
    def create_enhanced_header(self, parent):
        """Create enhanced header with toolbar"""
        header_frame = ctk.CTkFrame(parent, corner_radius=15, height=120)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Top row - Title and settings
        top_row = ctk.CTkFrame(header_frame, corner_radius=10)
        top_row.pack(fill="x", padx=15, pady=(10, 5))
        
        # App title with version
        title_label = ctk.CTkLabel(top_row, text="📋 Daily Task Tracker Pro 2.0", 
                                 font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(side="left", pady=10)
        
        # Settings and tools buttons
        tools_frame = ctk.CTkFrame(top_row, corner_radius=8)
        tools_frame.pack(side="right", padx=10, pady=5)
        
        # Theme toggle
        theme_btn = ctk.CTkButton(tools_frame, text="🌙/☀️", width=40, height=35,
                                command=self.toggle_theme, corner_radius=8)
        theme_btn.pack(side="left", padx=2)
        
        # Export button
        export_btn = ctk.CTkButton(tools_frame, text="📤", width=40, height=35,
                                 command=self.export_data, corner_radius=8)
        export_btn.pack(side="left", padx=2)
        
        # Settings button
        settings_btn = ctk.CTkButton(tools_frame, text="⚙️", width=40, height=35,
                                   command=self.open_settings, corner_radius=8)
        settings_btn.pack(side="left", padx=2)
        
        # Bottom row - Search and quick stats
        bottom_row = ctk.CTkFrame(header_frame, corner_radius=10)
        bottom_row.pack(fill="x", padx=15, pady=(0, 10))
        
        # Search functionality
        search_frame = ctk.CTkFrame(bottom_row, corner_radius=8)
        search_frame.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=5)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=16))
        search_label.pack(side="left", padx=5)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search tasks...", 
                                       height=35, corner_radius=8)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Quick stats display
        self.quick_stats_frame = ctk.CTkFrame(bottom_row, corner_radius=8)
        self.quick_stats_frame.pack(side="right", padx=5, pady=5)
        
        self.update_quick_stats()
        
    def create_tabbed_interface(self, parent):
        """Create tabbed interface for different views"""
        # Tab view
        self.tab_view = ctk.CTkTabview(parent, corner_radius=15)
        self.tab_view.pack(fill="both", expand=True)
        
        # Main tabs
        self.tasks_tab = self.tab_view.add("📋 Tasks")
        self.calendar_tab = self.tab_view.add("📅 Calendar") 
        self.analytics_tab = self.tab_view.add("📊 Analytics")
        self.timer_tab = self.tab_view.add("⏱️ Timer")
        
        # Create content for each tab
        self.create_tasks_tab()
        self.create_calendar_tab()
        self.create_analytics_tab()
        self.create_timer_tab()
        
    def create_tasks_tab(self):
        """Create the main tasks management tab"""
        # Split into left (controls) and right (tasks)
        content_frame = ctk.CTkFrame(self.tasks_tab, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Left panel - Task controls
        left_panel = ctk.CTkFrame(content_frame, corner_radius=10, width=400)
        left_panel.pack(side="left", fill="y", padx=(15, 7), pady=15)
        left_panel.pack_propagate(False)
        
        # Right panel - Tasks display
        right_panel = ctk.CTkFrame(content_frame, corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=(7, 15), pady=15)
        
        # Create left panel content
        self.create_task_controls(left_panel)
        
        # Create right panel content
        self.create_tasks_display(right_panel)
        
    def create_task_controls(self, parent):
        """Create task input and control panel"""
        # Date selection
        date_frame = ctk.CTkFrame(parent, corner_radius=10)
        date_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        date_label = ctk.CTkLabel(date_frame, text="📅 Selected Date", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        date_label.pack(pady=(10, 5))
        
        # Date navigation
        nav_frame = ctk.CTkFrame(date_frame, corner_radius=8)
        nav_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        prev_btn = ctk.CTkButton(nav_frame, text="◀", width=40, height=35,
                               command=self.previous_day, corner_radius=8)
        prev_btn.pack(side="left", padx=5, pady=5)
        
        self.date_label = ctk.CTkLabel(nav_frame, text="", 
                                     font=ctk.CTkFont(size=14, weight="bold"))
        self.date_label.pack(side="left", expand=True, padx=10)
        
        next_btn = ctk.CTkButton(nav_frame, text="▶", width=40, height=35,
                               command=self.next_day, corner_radius=8)
        next_btn.pack(side="right", padx=5, pady=5)
        
        # Quick date buttons
        quick_frame = ctk.CTkFrame(date_frame, corner_radius=8)
        quick_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        today_btn = ctk.CTkButton(quick_frame, text="Today", height=30,
                                command=self.go_to_today, corner_radius=6)
        today_btn.pack(fill="x", padx=5, pady=2)
        
        # Add task section
        add_frame = ctk.CTkFrame(parent, corner_radius=10)
        add_frame.pack(fill="x", padx=15, pady=10)
        
        add_title = ctk.CTkLabel(add_frame, text="✨ Add New Task", 
                               font=ctk.CTkFont(size=16, weight="bold"))
        add_title.pack(pady=(15, 10))
        
        # Task title
        self.task_entry = ctk.CTkEntry(add_frame, placeholder_text="Task title...", 
                                     height=35, corner_radius=8)
        self.task_entry.pack(fill="x", padx=15, pady=5)
        
        # Description
        self.desc_entry = ctk.CTkEntry(add_frame, placeholder_text="Description (optional)...", 
                                     height=35, corner_radius=8)
        self.desc_entry.pack(fill="x", padx=15, pady=5)
        
        # Priority and category row
        row1 = ctk.CTkFrame(add_frame, corner_radius=8)
        row1.pack(fill="x", padx=15, pady=5)
        
        self.priority_var = ctk.StringVar(value="⚡ Medium")
        priority_menu = ctk.CTkOptionMenu(row1, variable=self.priority_var,
                                        values=["🔥 High", "⚡ Medium", "🟢 Low"],
                                        height=35, corner_radius=8)
        priority_menu.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        self.category_var = ctk.StringVar(value="General")
        category_menu = ctk.CTkOptionMenu(row1, variable=self.category_var,
                                        values=["General", "Work", "Personal", "Health", "Learning", "Shopping"],
                                        height=35, corner_radius=8)
        category_menu.pack(side="right", padx=5, pady=5, fill="x", expand=True)
        
        # Time estimate and tags
        row2 = ctk.CTkFrame(add_frame, corner_radius=8)
        row2.pack(fill="x", padx=15, pady=5)
        
        time_label = ctk.CTkLabel(row2, text="Time (min):")
        time_label.pack(side="left", padx=5)
        
        self.time_entry = ctk.CTkEntry(row2, placeholder_text="30", width=80, height=35)
        self.time_entry.pack(side="left", padx=5, pady=5)
        
        self.tags_entry = ctk.CTkEntry(row2, placeholder_text="Tags (comma-separated)...", 
                                     height=35, corner_radius=8)
        self.tags_entry.pack(side="right", fill="x", expand=True, padx=5, pady=5)
        
        # Add button
        add_btn = ctk.CTkButton(add_frame, text="➕ Add Task", height=40,
                              command=self.add_enhanced_task, corner_radius=8,
                              font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.pack(fill="x", padx=15, pady=(5, 15))
        
        # Filters section
        filter_frame = ctk.CTkFrame(parent, corner_radius=10)
        filter_frame.pack(fill="x", padx=15, pady=10)
        
        filter_title = ctk.CTkLabel(filter_frame, text="🔧 Filters", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        filter_title.pack(pady=(15, 10))
        
        self.filter_var = ctk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(filter_frame, variable=self.filter_var,
                                      values=["All", "Completed", "Pending", "High Priority", "Overdue"],
                                      command=self.filter_tasks, corner_radius=8)
        filter_menu.pack(fill="x", padx=15, pady=(0, 15))
        
        # Bind Enter key
        self.task_entry.bind("<Return>", lambda e: self.add_enhanced_task())
        
    def create_tasks_display(self, parent):
        """Create the tasks display area"""
        # Header with date and stats
        header_frame = ctk.CTkFrame(parent, corner_radius=10, height=80)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        self.selected_date_label = ctk.CTkLabel(header_frame, text="", 
                                              font=ctk.CTkFont(size=20, weight="bold"))
        self.selected_date_label.pack(pady=20)
        
        # Tasks scrollable area
        self.tasks_scrollable = ctk.CTkScrollableFrame(parent, corner_radius=10)
        self.tasks_scrollable.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_calendar_tab(self):
        """Create calendar view tab"""
        cal_frame = ctk.CTkFrame(self.calendar_tab, corner_radius=10)
        cal_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Calendar header
        cal_header = ctk.CTkLabel(cal_frame, text="📅 Monthly Calendar View", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        cal_header.pack(pady=20)
        
        # Month navigation
        month_nav = ctk.CTkFrame(cal_frame, corner_radius=10)
        month_nav.pack(pady=10)
        
        prev_month_btn = ctk.CTkButton(month_nav, text="◀ Previous", height=40,
                                     command=self.prev_month, corner_radius=8)
        prev_month_btn.pack(side="left", padx=10, pady=10)
        
        self.month_year_label = ctk.CTkLabel(month_nav, text="", 
                                           font=ctk.CTkFont(size=18, weight="bold"))
        self.month_year_label.pack(side="left", padx=20, pady=10)
        
        next_month_btn = ctk.CTkButton(month_nav, text="Next ▶", height=40,
                                     command=self.next_month, corner_radius=8)
        next_month_btn.pack(side="left", padx=10, pady=10)
        
        # Calendar grid
        self.calendar_grid_frame = ctk.CTkFrame(cal_frame, corner_radius=10)
        self.calendar_grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_calendar_grid()
        
    def create_analytics_tab(self):
        """Create analytics and productivity tab"""
        analytics_frame = ctk.CTkFrame(self.analytics_tab, corner_radius=10)
        analytics_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Analytics header
        analytics_header = ctk.CTkLabel(analytics_frame, text="📊 Productivity Analytics", 
                                      font=ctk.CTkFont(size=24, weight="bold"))
        analytics_header.pack(pady=20)
        
        # Stats panels
        stats_container = ctk.CTkFrame(analytics_frame, corner_radius=10)
        stats_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Weekly overview
        weekly_frame = ctk.CTkFrame(stats_container, corner_radius=10)
        weekly_frame.pack(fill="x", padx=15, pady=10)
        
        weekly_label = ctk.CTkLabel(weekly_frame, text="📈 Weekly Overview", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        weekly_label.pack(pady=15)
        
        self.weekly_stats_frame = ctk.CTkFrame(weekly_frame, corner_radius=8)
        self.weekly_stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Productivity trends
        trends_frame = ctk.CTkFrame(stats_container, corner_radius=10)
        trends_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        trends_label = ctk.CTkLabel(trends_frame, text="📈 Productivity Trends", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        trends_label.pack(pady=15)
        
        self.trends_content = ctk.CTkFrame(trends_frame, corner_radius=8)
        self.trends_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_timer_tab(self):
        """Create Pomodoro timer tab"""
        timer_frame = ctk.CTkFrame(self.timer_tab, corner_radius=10)
        timer_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Timer header
        timer_header = ctk.CTkLabel(timer_frame, text="⏱️ Focus Timer", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        timer_header.pack(pady=20)
        
        # Timer display
        self.timer_display = ctk.CTkLabel(timer_frame, text="25:00", 
                                        font=ctk.CTkFont(size=72, weight="bold"))
        self.timer_display.pack(pady=30)
        
        # Timer controls
        timer_controls = ctk.CTkFrame(timer_frame, corner_radius=10)
        timer_controls.pack(pady=20)
        
        self.start_timer_btn = ctk.CTkButton(timer_controls, text="▶️ Start", 
                                           height=50, width=120,
                                           command=self.toggle_timer,
                                           font=ctk.CTkFont(size=16, weight="bold"))
        self.start_timer_btn.pack(side="left", padx=10, pady=10)
        
        reset_timer_btn = ctk.CTkButton(timer_controls, text="🔄 Reset", 
                                      height=50, width=120,
                                      command=self.reset_timer,
                                      fg_color="gray40", hover_color="gray50")
        reset_timer_btn.pack(side="left", padx=10, pady=10)
        
        # Timer settings
        timer_settings = ctk.CTkFrame(timer_frame, corner_radius=10)
        timer_settings.pack(pady=20)
        
        settings_label = ctk.CTkLabel(timer_settings, text="Timer Duration (minutes):", 
                                    font=ctk.CTkFont(size=14))
        settings_label.pack(pady=5)
        
        self.timer_duration = ctk.CTkSlider(timer_settings, from_=5, to=60, 
                                          number_of_steps=11, command=self.update_timer_display)
        self.timer_duration.pack(pady=10)
        self.timer_duration.set(25)  # Default Pomodoro time
        
        # Task selection for timer
        task_select_frame = ctk.CTkFrame(timer_frame, corner_radius=10)
        task_select_frame.pack(fill="x", padx=50, pady=20)
        
        task_select_label = ctk.CTkLabel(task_select_frame, text="Select task to work on:", 
                                       font=ctk.CTkFont(size=14))
        task_select_label.pack(pady=5)
        
        self.timer_task_var = ctk.StringVar(value="No task selected")
        self.timer_task_menu = ctk.CTkOptionMenu(task_select_frame, variable=self.timer_task_var,
                                               values=["No task selected"])
        self.timer_task_menu.pack(fill="x", padx=20, pady=10)
        
    def add_enhanced_task(self):
        """Add a new task with enhanced features"""
        title = self.task_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority_text = self.priority_var.get()
        priority = priority_text.split()[1] if " " in priority_text else priority_text
        category = self.category_var.get()
        time_estimate = self.time_entry.get().strip() or "30"
        tags = self.tags_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title!")
            return
            
        try:
            time_estimate = int(time_estimate)
        except ValueError:
            time_estimate = 30
            
        # Insert enhanced task
        self.cursor.execute('''
            INSERT INTO tasks (title, description, priority, category, estimated_time, 
                             date_created, tags, notes, progress)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, priority, category, time_estimate, 
              self.current_selected_date, tags, '', 0))
        self.conn.commit()
        
        # Clear inputs
        self.task_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')
        self.tags_entry.delete(0, 'end')
        self.priority_var.set("⚡ Medium")
        self.category_var.set("General")
        
        # Refresh displays
        self.load_tasks()
        self.update_timer_task_list()
        
    def create_enhanced_task_widget(self, task):
        """Create enhanced task widget with progress tracking"""
        task_id, title, description, priority, category, completed, estimated_time, actual_time, tags, notes, progress = task[:11]
        
        # Main task frame
        task_frame = ctk.CTkFrame(self.tasks_scrollable, corner_radius=12, height=120)
        task_frame.pack(fill="x", padx=5, pady=8)
        task_frame.pack_propagate(False)
        
        # Left side - main content
        left_frame = ctk.CTkFrame(task_frame, corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Top row - checkbox, title, priority
        top_row = ctk.CTkFrame(left_frame, corner_radius=8)
        top_row.pack(fill="x", padx=5, pady=5)
        
        # Checkbox
        checkbox = ctk.CTkCheckBox(top_row, text="", width=25, height=25,
                                 command=lambda: self.toggle_enhanced_task(task_id))
        checkbox.pack(side="left", padx=5, pady=5)
        
        if completed:
            checkbox.select()
        
        # Title with progress
        title_text = f"{'✓ ' if completed else ''}{title}"
        if progress > 0 and not completed:
            title_text += f" ({progress}%)"
            
        title_label = ctk.CTkLabel(top_row, text=title_text,
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left", padx=10, pady=5)
        
        # Priority and category badges
        badges_frame = ctk.CTkFrame(top_row, corner_radius=5)
        badges_frame.pack(side="right", padx=5, pady=5)
        
        priority_colors = {"High": "red", "Medium": "orange", "Low": "green"}
        priority_emoji = {"High": "🔥", "Medium": "⚡", "Low": "🟢"}
        
        priority_label = ctk.CTkLabel(badges_frame, 
                                    text=f"{priority_emoji.get(priority, '')} {priority}",
                                    text_color=priority_colors.get(priority, "gray"),
                                    font=ctk.CTkFont(size=11, weight="bold"))
        priority_label.pack(side="top", padx=3, pady=2)
        
        category_label = ctk.CTkLabel(badges_frame, text=f"📁 {category}",
                                    text_color="gray70", font=ctk.CTkFont(size=10))
        category_label.pack(side="top", padx=3, pady=2)
        
        # Middle row - description and tags
        if description or tags:
            middle_row = ctk.CTkFrame(left_frame, corner_radius=8)
            middle_row.pack(fill="x", padx=5, pady=2)
            
            if description:
                desc_label = ctk.CTkLabel(middle_row, text=f"📝 {description}",
                                        font=ctk.CTkFont(size=12), text_color="gray60")
                desc_label.pack(side="left", padx=5, pady=2, anchor="w")
            
            if tags:
                tags_label = ctk.CTkLabel(middle_row, text=f"🏷️ {tags}",
                                        font=ctk.CTkFont(size=11), text_color="blue")
                tags_label.pack(side="right", padx=5, pady=2)
        
        # Bottom row - time info and progress
        bottom_row = ctk.CTkFrame(left_frame, corner_radius=8)
        bottom_row.pack(fill="x", padx=5, pady=2)
        
        # Time information
        time_info = f"⏱️ Est: {estimated_time}m"
        if actual_time > 0:
            time_info += f" | Actual: {actual_time}m"
            
        time_label = ctk.CTkLabel(bottom_row, text=time_info,
                                font=ctk.CTkFont(size=11), text_color="gray60")
        time_label.pack(side="left", padx=5, pady=2)
        
        # Progress bar for incomplete tasks
        if not completed and progress > 0:
            progress_bar = ctk.CTkProgressBar(bottom_row, width=100, height=15)
            progress_bar.pack(side="right", padx=5, pady=2)
            progress_bar.set(progress / 100)
        
        # Right side - enhanced actions
        actions_frame = ctk.CTkFrame(task_frame, corner_radius=10, width=60)
        actions_frame.pack(side="right", fill="y", padx=10, pady=10)
        actions_frame.pack_propagate(False)
        
        # Timer button
        timer_btn = ctk.CTkButton(actions_frame, text="⏱️", width=40, height=30,
                                command=lambda: self.start_task_timer(task_id),
                                fg_color="green", hover_color="darkgreen", corner_radius=6)
        timer_btn.pack(pady=2)
        
        # Edit button
        edit_btn = ctk.CTkButton(actions_frame, text="✏️", width=40, height=30,
                               command=lambda: self.edit_enhanced_task(task_id),
                               fg_color="blue", hover_color="darkblue", corner_radius=6)
        edit_btn.pack(pady=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(actions_frame, text="🗑️", width=40, height=30,
                                 command=lambda: self.delete_task(task_id),
                                 fg_color="red", hover_color="darkred", corner_radius=6)
        delete_btn.pack(pady=2)
        
    def create_calendar_grid(self):
        """Create monthly calendar grid with task indicators"""
        # Clear existing grid
        for widget in self.calendar_grid_frame.winfo_children():
            widget.destroy()
            
        # Current month/year
        cal_year = self.current_selected_date.year
        cal_month = self.current_selected_date.month
        
        # Update month label
        month_name = calendar.month_name[cal_month]
        self.month_year_label.configure(text=f"{month_name} {cal_year}")
        
        # Days of week headers
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, day in enumerate(days):
            header_label = ctk.CTkLabel(self.calendar_grid_frame, text=day, 
                                      font=ctk.CTkFont(size=14, weight="bold"))
            header_label.grid(row=0, column=i, padx=2, pady=5, sticky="nsew")
            
        # Get task counts for each day
        self.cursor.execute('''
            SELECT date_created, COUNT(*), SUM(completed) 
            FROM tasks 
            WHERE date_created LIKE ? 
            GROUP BY date_created
        ''', (f"{cal_year}-{cal_month:02d}-%",))
        
        task_data = {row[0]: (row[1], row[2]) for row in self.cursor.fetchall()}
        
        # Calendar days
        cal = calendar.monthcalendar(cal_year, cal_month)
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                    
                day_date = date(cal_year, cal_month, day)
                day_str = day_date.strftime("%Y-%m-%d")
                
                # Create day frame
                day_frame = ctk.CTkFrame(self.calendar_grid_frame, corner_radius=8)
                day_frame.grid(row=week_num, column=day_num, padx=2, pady=2, sticky="nsew")
                
                # Day number
                day_label = ctk.CTkLabel(day_frame, text=str(day), 
                                       font=ctk.CTkFont(size=16, weight="bold"))
                day_label.pack(pady=2)
                
                # Task indicator
                if day_str in task_data:
                    total_tasks, completed_tasks = task_data[day_str]
                    if total_tasks > 0:
                        completion_rate = (completed_tasks / total_tasks) * 100
                        indicator_text = f"{completed_tasks}/{total_tasks}"
                        
                        if completion_rate == 100:
                            color = "green"
                        elif completion_rate >= 50:
                            color = "orange"
                        else:
                            color = "red"
                            
                        indicator_label = ctk.CTkLabel(day_frame, text=indicator_text,
                                                     text_color=color, font=ctk.CTkFont(size=10))
                        indicator_label.pack(pady=1)
                
                # Highlight selected day
                if day_date == self.current_selected_date:
                    day_frame.configure(fg_color="blue")
                elif day_date == date.today():
                    day_frame.configure(fg_color="green")
                    
                # Make clickable
                day_frame.bind("<Button-1>", lambda e, d=day_date: self.select_calendar_date(d))
                day_label.bind("<Button-1>", lambda e, d=day_date: self.select_calendar_date(d))
                
        # Configure grid weights
        for i in range(7):
            self.calendar_grid_frame.grid_columnconfigure(i, weight=1)
            
    def select_calendar_date(self, selected_date):
        """Select date from calendar"""
        self.current_selected_date = selected_date
        self.update_all_displays()
        self.tab_view.set("📋 Tasks")  # Switch to tasks tab
        
    def update_all_displays(self):
        """Update all date-related displays"""
        # Update date labels
        selected_str = self.current_selected_date.strftime("%A, %B %d, %Y")
        nav_str = self.current_selected_date.strftime("%m/%d/%Y")
        
        self.date_label.configure(text=nav_str)
        
        # Add day indicator
        if self.current_selected_date == date.today():
            display_text = f"📅 Today - {selected_str}"
        elif self.current_selected_date == date.today() - timedelta(days=1):
            display_text = f"📅 Yesterday - {selected_str}"
        elif self.current_selected_date == date.today() + timedelta(days=1):
            display_text = f"📅 Tomorrow - {selected_str}"
        else:
            display_text = f"📅 {selected_str}"
            
        self.selected_date_label.configure(text=display_text)
        
        # Update calendar grid
        self.create_calendar_grid()
        
        # Update quick stats
        self.update_quick_stats()
        
    def load_tasks(self):
        """Load and display tasks with enhanced filtering"""
        # Clear existing widgets
        for widget in self.tasks_scrollable.winfo_children():
            widget.destroy()
            
        # Build query based on filters and search
        base_query = '''
            SELECT id, title, description, priority, category, completed, 
                   estimated_time, actual_time, tags, notes, progress
            FROM tasks 
            WHERE date_created = ? AND archived = 0
        '''
        params = [self.current_selected_date]
        
        # Apply search filter
        if self.search_term:
            base_query += ' AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)'
            search_pattern = f'%{self.search_term}%'
            params.extend([search_pattern, search_pattern, search_pattern])
            
        # Apply status filter
        filter_type = self.filter_var.get()
        if filter_type == "Completed":
            base_query += ' AND completed = 1'
        elif filter_type == "Pending":
            base_query += ' AND completed = 0'
        elif filter_type == "High Priority":
            base_query += ' AND priority = "High"'
        elif filter_type == "Overdue":
            base_query += ' AND completed = 0 AND date_created < ?'
            params.append(date.today())
            
        # Order by priority and completion
        base_query += '''
            ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                END,
                completed ASC,
                progress DESC
        '''
        
        self.cursor.execute(base_query, params)
        tasks = self.cursor.fetchall()
        
        if not tasks:
            no_tasks_label = ctk.CTkLabel(self.tasks_scrollable, 
                                        text="🎯 No tasks found.\nTry adjusting your filters or add some tasks!", 
                                        font=ctk.CTkFont(size=16))
            no_tasks_label.pack(pady=50)
        else:
            for task in tasks:
                self.create_enhanced_task_widget(task)
                
    def update_quick_stats(self):
        """Update quick statistics in header"""
        # Clear existing stats
        for widget in self.quick_stats_frame.winfo_children():
            widget.destroy()
            
        # Get stats for current date
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(completed) as completed,
                SUM(estimated_time) as total_time,
                AVG(CASE WHEN completed = 1 AND actual_time > 0 
                    THEN (estimated_time * 1.0 / actual_time) ELSE NULL END) as efficiency
            FROM tasks 
            WHERE date_created = ? AND archived = 0
        ''', (self.current_selected_date,))
        
        result = self.cursor.fetchone()
        total = result[0] if result[0] else 0
        completed = result[1] if result[1] else 0
        total_time = result[2] if result[2] else 0
        efficiency = result[3] if result[3] else 1.0
        
        # Create compact stats display
        if total > 0:
            completion_rate = (completed / total) * 100
            
            stats_text = f"📊 {completed}/{total} tasks ({completion_rate:.0f}%)"
            stats_label = ctk.CTkLabel(self.quick_stats_frame, text=stats_text,
                                     font=ctk.CTkFont(size=14, weight="bold"))
            stats_label.pack(side="left", padx=10, pady=8)
            
            time_text = f"⏱️ {total_time}min planned"
            time_label = ctk.CTkLabel(self.quick_stats_frame, text=time_text,
                                    font=ctk.CTkFont(size=12), text_color="gray70")
            time_label.pack(side="left", padx=10, pady=8)
            
            if efficiency and efficiency != 1.0:
                eff_text = f"⚡ {efficiency:.1f}x efficiency"
                eff_color = "green" if efficiency >= 1.0 else "orange"
                eff_label = ctk.CTkLabel(self.quick_stats_frame, text=eff_text,
                                       font=ctk.CTkFont(size=12), text_color=eff_color)
                eff_label.pack(side="left", padx=10, pady=8)
        else:
            no_stats_label = ctk.CTkLabel(self.quick_stats_frame, text="📊 No tasks for today",
                                        font=ctk.CTkFont(size=14))
            no_stats_label.pack(padx=10, pady=8)
            
    # Timer functionality
    def update_timer_task_list(self):
        """Update the task list for timer selection"""
        self.cursor.execute('''
            SELECT id, title FROM tasks 
            WHERE date_created = ? AND completed = 0 AND archived = 0
            ORDER BY priority DESC
        ''', (self.current_selected_date,))
        
        tasks = self.cursor.fetchall()
        task_options = ["No task selected"] + [f"{task[1]} (ID: {task[0]})" for task in tasks]
        
        self.timer_task_menu.configure(values=task_options)
        
    def start_task_timer(self, task_id):
        """Start timer for specific task"""
        self.timer_task_id = task_id
        
        # Get task title
        self.cursor.execute('SELECT title FROM tasks WHERE id = ?', (task_id,))
        task_title = self.cursor.fetchone()[0]
        
        # Set timer task selection
        self.timer_task_var.set(f"{task_title} (ID: {task_id})")
        
        # Switch to timer tab
        self.tab_view.set("⏱️ Timer")
        
        # Start timer if not running
        if not self.timer_running:
            self.toggle_timer()
            
    def toggle_timer(self):
        """Toggle timer start/stop"""
        if not self.timer_running:
            self.start_timer()
        else:
            self.stop_timer()
            
    def start_timer(self):
        """Start the focus timer"""
        self.timer_running = True
        self.timer_start_time = time.time()
        
        # Get selected task ID if any
        task_selection = self.timer_task_var.get()
        if "ID: " in task_selection:
            self.timer_task_id = int(task_selection.split("ID: ")[1].split(")")[0])
        
        self.start_timer_btn.configure(text="⏸️ Pause")
        self.update_timer()
        
    def stop_timer(self):
        """Stop the timer and log time"""
        if self.timer_running and self.timer_start_time:
            elapsed_time = int(time.time() - self.timer_start_time)
            
            # Log time if task is selected
            if self.timer_task_id:
                self.log_work_time(self.timer_task_id, elapsed_time)
            
            self.timer_running = False
            self.start_timer_btn.configure(text="▶️ Start")
            
            # Show completion notification
            messagebox.showinfo("Timer Complete", 
                              f"Focus session complete!\nTime worked: {elapsed_time // 60}:{elapsed_time % 60:02d}")
            
    def reset_timer(self):
        """Reset timer to default duration"""
        self.timer_running = False
        self.timer_start_time = None
        self.start_timer_btn.configure(text="▶️ Start")
        self.update_timer_display()
        
    def update_timer(self):
        """Update timer display while running"""
        if self.timer_running and self.timer_start_time:
            elapsed = time.time() - self.timer_start_time
            duration_seconds = int(self.timer_duration.get() * 60)
            remaining = max(0, duration_seconds - elapsed)
            
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            
            self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
            
            if remaining <= 0:
                self.stop_timer()
            else:
                # Schedule next update
                self.root.after(1000, self.update_timer)
                
    def update_timer_display(self, value=None):
        """Update timer display with current duration setting"""
        if not self.timer_running:
            duration = int(self.timer_duration.get())
            self.timer_display.configure(text=f"{duration:02d}:00")
            
    def log_work_time(self, task_id, duration_seconds):
        """Log work time for a task"""
        # Insert time log
        self.cursor.execute('''
            INSERT INTO time_logs (task_id, start_time, end_time, duration, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, 
              datetime.fromtimestamp(self.timer_start_time),
              datetime.now(),
              duration_seconds,
              "Focus timer session"))
        
        # Update task actual time
        self.cursor.execute('''
            UPDATE tasks 
            SET actual_time = actual_time + ?
            WHERE id = ?
        ''', (duration_seconds // 60, task_id))
        
        self.conn.commit()
        self.load_tasks()  # Refresh task display
        
    # Enhanced task operations
    def toggle_enhanced_task(self, task_id):
        """Toggle task completion with time tracking"""
        self.cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        current_status = self.cursor.fetchone()[0]
        
        new_status = 1 if current_status == 0 else 0
        completion_date = date.today() if new_status == 1 else None
        
        self.cursor.execute('''
            UPDATE tasks 
            SET completed = ?, date_completed = ?, progress = ?
            WHERE id = ?
        ''', (new_status, completion_date, 100 if new_status == 1 else 0, task_id))
        
        self.conn.commit()
        self.load_tasks()
        self.update_quick_stats()
        
    def edit_enhanced_task(self, task_id):
        """Open enhanced task editor"""
        self.open_task_editor(task_id)
        
    def open_task_editor(self, task_id):
        """Open task editing window"""
        # Get current task data
        self.cursor.execute('''
            SELECT title, description, priority, category, estimated_time, tags, notes, progress
            FROM tasks WHERE id = ?
        ''', (task_id,))
        
        task_data = self.cursor.fetchone()
        if not task_data:
            return
            
        # Create edit window
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("500x600")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Form fields
        title_label = ctk.CTkLabel(edit_window, text="Title:", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=(20, 5))
        
        title_entry = ctk.CTkEntry(edit_window, height=35, corner_radius=8)
        title_entry.pack(fill="x", padx=20, pady=5)
        title_entry.insert(0, task_data[0])
        
        desc_label = ctk.CTkLabel(edit_window, text="Description:", font=ctk.CTkFont(size=14, weight="bold"))
        desc_label.pack(pady=(15, 5))
        
        desc_text = ctk.CTkTextbox(edit_window, height=80, corner_radius=8)
        desc_text.pack(fill="x", padx=20, pady=5)
        desc_text.insert("1.0", task_data[1] or "")
        
        # Priority and category
        row_frame = ctk.CTkFrame(edit_window, corner_radius=8)
        row_frame.pack(fill="x", padx=20, pady=15)
        
        priority_label = ctk.CTkLabel(row_frame, text="Priority:", font=ctk.CTkFont(size=14))
        priority_label.pack(side="left", padx=5, pady=10)
        
        priority_var = ctk.StringVar(value=f"⚡ {task_data[2]}")
        priority_menu = ctk.CTkOptionMenu(row_frame, variable=priority_var,
                                        values=["🔥 High", "⚡ Medium", "🟢 Low"])
        priority_menu.pack(side="left", padx=10, pady=10)
        
        category_label = ctk.CTkLabel(row_frame, text="Category:", font=ctk.CTkFont(size=14))
        category_label.pack(side="left", padx=5, pady=10)
        
        category_var = ctk.StringVar(value=task_data[3])
        category_menu = ctk.CTkOptionMenu(row_frame, variable=category_var,
                                        values=["General", "Work", "Personal", "Health", "Learning", "Shopping"])
        category_menu.pack(side="left", padx=10, pady=10)
        
        # Time and tags
        time_frame = ctk.CTkFrame(edit_window, corner_radius=8)
        time_frame.pack(fill="x", padx=20, pady=10)
        
        time_label = ctk.CTkLabel(time_frame, text="Est. Time (min):", font=ctk.CTkFont(size=14))
        time_label.pack(side="left", padx=5, pady=10)
        
        time_entry = ctk.CTkEntry(time_frame, width=80, height=35)
        time_entry.pack(side="left", padx=10, pady=10)
        time_entry.insert(0, str(task_data[4]))
        
        tags_label = ctk.CTkLabel(time_frame, text="Tags:", font=ctk.CTkFont(size=14))
        tags_label.pack(side="left", padx=5, pady=10)
        
        tags_entry = ctk.CTkEntry(time_frame, height=35)
        tags_entry.pack(side="right", fill="x", expand=True, padx=10, pady=10)
        tags_entry.insert(0, task_data[5] or "")
        
        # Progress slider
        progress_label = ctk.CTkLabel(edit_window, text="Progress:", font=ctk.CTkFont(size=14, weight="bold"))
        progress_label.pack(pady=(15, 5))
        
        progress_slider = ctk.CTkSlider(edit_window, from_=0, to=100, number_of_steps=20)
        progress_slider.pack(fill="x", padx=20, pady=5)
        progress_slider.set(task_data[7] or 0)
        
        progress_value_label = ctk.CTkLabel(edit_window, text=f"{task_data[7] or 0}%")
        progress_value_label.pack(pady=5)
        
        def update_progress_label(value):
            progress_value_label.configure(text=f"{int(value)}%")
            
        progress_slider.configure(command=update_progress_label)
        
        # Notes
        notes_label = ctk.CTkLabel(edit_window, text="Notes:", font=ctk.CTkFont(size=14, weight="bold"))
        notes_label.pack(pady=(15, 5))
        
        notes_text = ctk.CTkTextbox(edit_window, height=80, corner_radius=8)
        notes_text.pack(fill="x", padx=20, pady=5)
        notes_text.insert("1.0", task_data[6] or "")
        
        # Buttons
        button_frame = ctk.CTkFrame(edit_window, corner_radius=8)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def save_changes():
            new_title = title_entry.get().strip()
            if not new_title:
                messagebox.showwarning("Warning", "Title cannot be empty!")
                return
                
            new_desc = desc_text.get("1.0", "end-1c").strip()
            new_priority = priority_var.get().split()[1]
            new_category = category_var.get()
            new_time = int(time_entry.get() or "30")
            new_tags = tags_entry.get().strip()
            new_progress = int(progress_slider.get())
            new_notes = notes_text.get("1.0", "end-1c").strip()
            
            self.cursor.execute('''
                UPDATE tasks 
                SET title=?, description=?, priority=?, category=?, estimated_time=?, 
                    tags=?, notes=?, progress=?
                WHERE id=?
            ''', (new_title, new_desc, new_priority, new_category, new_time, 
                  new_tags, new_notes, new_progress, task_id))
            
            self.conn.commit()
            edit_window.destroy()
            self.load_tasks()
            
        save_btn = ctk.CTkButton(button_frame, text="💾 Save Changes", 
                               command=save_changes, height=40,
                               font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="left", padx=10, pady=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ Cancel", 
                                 command=edit_window.destroy, height=40,
                                 fg_color="gray40", hover_color="gray50")
        cancel_btn.pack(side="right", padx=10, pady=10)
        
    def delete_task(self, task_id):
        """Delete a task with confirmation"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.cursor.execute('DELETE FROM time_logs WHERE task_id = ?', (task_id,))
            self.conn.commit()
            self.load_tasks()
            self.update_quick_stats()
            
    # Search functionality
    def on_search_change(self, event):
        """Handle search term changes"""
        self.search_term = self.search_entry.get().strip()
        self.load_tasks()
        
    def filter_tasks(self, *args):
        """Handle filter changes"""
        self.load_tasks()
        
    # Navigation functions
    def previous_day(self):
        """Go to previous day"""
        self.current_selected_date -= timedelta(days=1)
        self.update_all_displays()
        self.load_tasks()
        self.update_timer_task_list()
        
    def next_day(self):
        """Go to next day"""
        self.current_selected_date += timedelta(days=1)
        self.update_all_displays()
        self.load_tasks()
        self.update_timer_task_list()
        
    def go_to_today(self):
        """Go to today"""
        self.current_selected_date = date.today()
        self.update_all_displays()
        self.load_tasks()
        self.update_timer_task_list()
        
    def prev_month(self):
        """Go to previous month"""
        if self.current_selected_date.month == 1:
            self.current_selected_date = self.current_selected_date.replace(
                year=self.current_selected_date.year-1, month=12)
        else:
            self.current_selected_date = self.current_selected_date.replace(
                month=self.current_selected_date.month-1)
        self.update_all_displays()
        
    def next_month(self):
        """Go to next month"""
        if self.current_selected_date.month == 12:
            self.current_selected_date = self.current_selected_date.replace(
                year=self.current_selected_date.year+1, month=1)
        else:
            self.current_selected_date = self.current_selected_date.replace(
                month=self.current_selected_date.month+1)
        self.update_all_displays()
        
    # Enhanced features
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.theme_mode == "dark":
            ctk.set_appearance_mode("light")
            self.theme_mode = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.theme_mode = "dark"
        self.save_settings()
        
    def export_data(self):
        """Export tasks to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Tasks"
        )
        
        if file_path:
            try:
                self.cursor.execute('''
                    SELECT date_created, title, description, priority, category, 
                           completed, estimated_time, actual_time, tags, notes, progress
                    FROM tasks ORDER BY date_created DESC
                ''')
                
                tasks = self.cursor.fetchall()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Date', 'Title', 'Description', 'Priority', 'Category', 
                                   'Completed', 'Estimated Time (min)', 'Actual Time (min)', 
                                   'Tags', 'Notes', 'Progress (%)'])
                    writer.writerows(tasks)
                
                messagebox.showinfo("Export Complete", f"Tasks exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export tasks: {str(e)}")
                
    def open_settings(self):
        """Open settings window"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        settings_label = ctk.CTkLabel(settings_window, text="⚙️ Settings", 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        settings_label.pack(pady=20)
        
        # Notifications toggle
        notifications_var = ctk.BooleanVar(value=self.notifications_enabled)
        notifications_check = ctk.CTkCheckBox(settings_window, 
                                            text="Enable notifications",
                                            variable=notifications_var)
        notifications_check.pack(pady=10)
        
        # Auto-save toggle
        auto_save_var = ctk.BooleanVar(value=self.auto_save_enabled)
        auto_save_check = ctk.CTkCheckBox(settings_window, 
                                        text="Enable auto-save",
                                        variable=auto_save_var)
        auto_save_check.pack(pady=10)
        
        # Save button
        def save_settings():
            self.notifications_enabled = notifications_var.get()
            self.auto_save_enabled = auto_save_var.get()
            self.save_settings()
            settings_window.destroy()
            
        save_btn = ctk.CTkButton(settings_window, text="💾 Save Settings",
                               command=save_settings, height=40)
        save_btn.pack(pady=20)
        
    def start_auto_save(self):
        """Start auto-save thread"""
        def auto_save_worker():
            while True:
                time.sleep(30)  # Auto-save every 30 seconds
                if self.auto_save_enabled:
                    try:
                        self.conn.commit()
                    except:
                        pass
                        
        if self.auto_save_enabled:
            auto_save_thread = threading.Thread(target=auto_save_worker, daemon=True)
            auto_save_thread.start()
            
    def update_analytics(self):
        """Update analytics displays"""
        # Weekly stats
        week_start = self.current_selected_date - timedelta(days=self.current_selected_date.weekday())
        week_end = week_start + timedelta(days=6)
        
        self.cursor.execute('''
            SELECT 
                date_created,
                COUNT(*) as total_tasks,
                SUM(completed) as completed_tasks,
                SUM(estimated_time) as estimated_time,
                SUM(actual_time) as actual_time
            FROM tasks 
            WHERE date_created BETWEEN ? AND ? AND archived = 0
            GROUP BY date_created
            ORDER BY date_created
        ''', (week_start, week_end))
        
        weekly_data = self.cursor.fetchall()
        
        # Clear existing weekly stats
        for widget in self.weekly_stats_frame.winfo_children():
            widget.destroy()
            
        if weekly_data:
            # Create weekly overview chart
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            for i, day in enumerate(days):
                day_date = week_start + timedelta(days=i)
                day_data = next((d for d in weekly_data if d[0] == day_date.strftime('%Y-%m-%d')), None)
                
                day_frame = ctk.CTkFrame(self.weekly_stats_frame, corner_radius=8, width=80)
                day_frame.pack(side="left", padx=5, pady=10)
                day_frame.pack_propagate(False)
                
                day_label = ctk.CTkLabel(day_frame, text=day, font=ctk.CTkFont(size=12, weight="bold"))
                day_label.pack(pady=2)
                
                if day_data:
                    total, completed, est_time, actual_time = day_data[1], day_data[2], day_data[3], day_data[4]
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    
                    # Completion rate bar
                    progress_bar = ctk.CTkProgressBar(day_frame, width=60, height=8)
                    progress_bar.pack(pady=2)
                    progress_bar.set(completion_rate / 100)
                    
                    # Stats text
                    stats_text = f"{completed}/{total}"
                    stats_label = ctk.CTkLabel(day_frame, text=stats_text, font=ctk.CTkFont(size=10))
                    stats_label.pack(pady=1)
                    
                    if actual_time and est_time:
                        efficiency = actual_time / est_time if est_time > 0 else 1
                        eff_color = "green" if efficiency <= 1.2 else "orange" if efficiency <= 1.5 else "red"
                        eff_label = ctk.CTkLabel(day_frame, text=f"{efficiency:.1f}x", 
                                               font=ctk.CTkFont(size=9), text_color=eff_color)
                        eff_label.pack()
                else:
                    no_data_label = ctk.CTkLabel(day_frame, text="No tasks", 
                                               font=ctk.CTkFont(size=9), text_color="gray")
                    no_data_label.pack(pady=10)
                    
        # Update trends
        self.update_productivity_trends()
        
    def update_productivity_trends(self):
        """Update productivity trends display"""
        # Clear existing trends
        for widget in self.trends_content.winfo_children():
            widget.destroy()
            
        # Get last 30 days of data
        end_date = date.today()
        start_date = end_date - timedelta(days=29)
        
        self.cursor.execute('''
            SELECT 
                date_created,
                COUNT(*) as total_tasks,
                SUM(completed) as completed_tasks,
                AVG(CASE WHEN completed = 1 AND actual_time > 0 AND estimated_time > 0
                    THEN (estimated_time * 1.0 / actual_time) ELSE NULL END) as avg_efficiency
            FROM tasks 
            WHERE date_created BETWEEN ? AND ? AND archived = 0
            GROUP BY date_created
            ORDER BY date_created DESC
            LIMIT 10
        ''', (start_date, end_date))
        
        trend_data = self.cursor.fetchall()
        
        if trend_data:
            # Create trend summary
            total_days = len(trend_data)
            avg_tasks_per_day = sum(row[1] for row in trend_data) / total_days
            avg_completion_rate = sum((row[2] or 0) / row[1] * 100 for row in trend_data) / total_days
            avg_efficiency = sum(row[3] for row in trend_data if row[3]) / len([r for r in trend_data if r[3]]) if any(row[3] for row in trend_data) else 1.0
            
            # Summary stats
            summary_frame = ctk.CTkFrame(self.trends_content, corner_radius=8)
            summary_frame.pack(fill="x", padx=15, pady=10)
            
            summary_title = ctk.CTkLabel(summary_frame, text="📈 30-Day Summary", 
                                       font=ctk.CTkFont(size=16, weight="bold"))
            summary_title.pack(pady=10)
            
            stats_grid = ctk.CTkFrame(summary_frame, corner_radius=8)
            stats_grid.pack(fill="x", padx=15, pady=(0, 15))
            
            # Avg tasks per day
            tasks_frame = ctk.CTkFrame(stats_grid, corner_radius=6)
            tasks_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(tasks_frame, text="📋 Avg Tasks/Day", 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(pady=2)
            ctk.CTkLabel(tasks_frame, text=f"{avg_tasks_per_day:.1f}", 
                        font=ctk.CTkFont(size=16), text_color="blue").pack(pady=2)
            
            # Completion rate
            completion_frame = ctk.CTkFrame(stats_grid, corner_radius=6)
            completion_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(completion_frame, text="✅ Completion Rate", 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(pady=2)
            ctk.CTkLabel(completion_frame, text=f"{avg_completion_rate:.1f}%", 
                        font=ctk.CTkFont(size=16), text_color="green").pack(pady=2)
            
            # Efficiency
            efficiency_frame = ctk.CTkFrame(stats_grid, corner_radius=6)
            efficiency_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(efficiency_frame, text="⚡ Avg Efficiency", 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(pady=2)
            eff_color = "green" if avg_efficiency >= 1.0 else "orange"
            ctk.CTkLabel(efficiency_frame, text=f"{avg_efficiency:.1f}x", 
                        font=ctk.CTkFont(size=16), text_color=eff_color).pack(pady=2)
            
            # Recent activity list
            recent_frame = ctk.CTkFrame(self.trends_content, corner_radius=8)
            recent_frame.pack(fill="both", expand=True, padx=15, pady=10)
            
            recent_title = ctk.CTkLabel(recent_frame, text="📅 Recent Activity", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
            recent_title.pack(pady=(15, 10))
            
            recent_scroll = ctk.CTkScrollableFrame(recent_frame, corner_radius=8)
            recent_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
            
            for row in trend_data:
                activity_date, total, completed, efficiency = row
                completion_rate = (completed / total * 100) if total > 0 else 0
                
                activity_item = ctk.CTkFrame(recent_scroll, corner_radius=6)
                activity_item.pack(fill="x", padx=5, pady=3)
                
                # Date
                date_obj = datetime.strptime(activity_date, '%Y-%m-%d').date()
                date_str = date_obj.strftime('%m/%d')
                if date_obj == date.today():
                    date_str = "Today"
                elif date_obj == date.today() - timedelta(days=1):
                    date_str = "Yesterday"
                    
                date_label = ctk.CTkLabel(activity_item, text=date_str, 
                                        font=ctk.CTkFont(size=12, weight="bold"), width=80)
                date_label.pack(side="left", padx=10, pady=5)
                
                # Tasks completed
                tasks_text = f"{completed}/{total} tasks"
                tasks_label = ctk.CTkLabel(activity_item, text=tasks_text, 
                                         font=ctk.CTkFont(size=11))
                tasks_label.pack(side="left", padx=10, pady=5)
                
                # Completion rate
                rate_color = "green" if completion_rate >= 80 else "orange" if completion_rate >= 60 else "red"
                rate_label = ctk.CTkLabel(activity_item, text=f"{completion_rate:.0f}%", 
                                        font=ctk.CTkFont(size=11), text_color=rate_color)
                rate_label.pack(side="right", padx=10, pady=5)
        else:
            no_data_label = ctk.CTkLabel(self.trends_content, 
                                       text="📊 No productivity data available yet.\nStart completing tasks to see trends!", 
                                       font=ctk.CTkFont(size=16))
            no_data_label.pack(expand=True)
            
    def run(self):
        """Start the enhanced application"""
        # Initialize displays
        self.update_all_displays()
        self.load_tasks()
        self.update_timer_task_list()
        self.update_analytics()
        
        # Set up periodic updates
        def periodic_update():
            if self.timer_running:
                self.update_timer()
            self.update_quick_stats()
            # Schedule next update
            self.root.after(1000, periodic_update)
            
        periodic_update()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the main loop
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        # Save any pending changes
        self.save_settings()
        self.conn.commit()
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    # Check dependencies
    try:
        import customtkinter as ctk
    except ImportError:
        print("CustomTkinter is not installed. Please install it using:")
        print("pip install customtkinter")
        exit(1)
    
    print("🚀 Starting Daily Task Tracker Pro 2.0...")
    print("📋 Enhanced features loaded:")
    print("   • Advanced task management with progress tracking")
    print("   • Integrated Pomodoro timer with time logging")
    print("   • Comprehensive analytics and productivity insights")
    print("   • Enhanced calendar view with task indicators")
    print("   • Search and advanced filtering")
    print("   • Data export capabilities")
    print("   • Theme switching and customizable settings")
    print("   • Auto-save functionality")
    print()
    
    app = TaskTracker()
    app.run()