import customtkinter as ctk
import sqlite3
from datetime import datetime, date, timedelta
import json
from tkinter import messagebox
import calendar
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TaskTracker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Daily Task Tracker Pro")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Current selected date
        self.selected_date = date.today()
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Load tasks for selected date
        self.load_tasks()
        
    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        
        # Create tasks table
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
                estimated_time INTEGER DEFAULT 30
            )
        ''')
        
        # Check if we need to add new columns (for existing databases)
        self.cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'category' not in columns:
            self.cursor.execute('ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT "General"')
            
        if 'estimated_time' not in columns:
            self.cursor.execute('ALTER TABLE tasks ADD COLUMN estimated_time INTEGER DEFAULT 30')
        
        self.conn.commit()
        
    def create_widgets(self):
        """Create the main GUI elements"""
        # Main container with padding
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Content area - split into left and right
        content_frame = ctk.CTkFrame(main_container, corner_radius=15)
        content_frame.pack(fill="both", expand=True, pady=20)
        
        # Left side - Calendar and date navigation
        left_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        left_frame.pack(side="left", fill="y", padx=20, pady=20, ipadx=10)
        
        # Right side - Task management
        right_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
        
        # Create left panel (calendar)
        self.create_calendar_panel(left_frame)
        
        # Create right panel (tasks)
        self.create_tasks_panel(right_frame)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ctk.CTkFrame(parent, corner_radius=15, height=100)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # App title
        title_label = ctk.CTkLabel(header_frame, text="📋 Daily Task Tracker Pro", 
                                 font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(header_frame, text="Stay organized and boost your productivity", 
                                    font=ctk.CTkFont(size=16), text_color="gray70")
        subtitle_label.pack(pady=(0, 15))
        
    def create_calendar_panel(self, parent):
        """Create the calendar and date navigation panel"""
        # Calendar header
        cal_header = ctk.CTkLabel(parent, text="📅 Calendar", 
                                font=ctk.CTkFont(size=20, weight="bold"))
        cal_header.pack(pady=(20, 10))
        
        # Date navigation
        nav_frame = ctk.CTkFrame(parent, corner_radius=10)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Previous day button
        prev_btn = ctk.CTkButton(nav_frame, text="◀", width=40, height=40,
                               command=self.previous_day, corner_radius=20,
                               font=ctk.CTkFont(size=16, weight="bold"))
        prev_btn.pack(side="left", padx=5, pady=5)
        
        # Current date display
        self.date_label = ctk.CTkLabel(nav_frame, text="", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        self.date_label.pack(side="left", expand=True, padx=10)
        
        # Next day button
        next_btn = ctk.CTkButton(nav_frame, text="▶", width=40, height=40,
                               command=self.next_day, corner_radius=20,
                               font=ctk.CTkFont(size=16, weight="bold"))
        next_btn.pack(side="right", padx=5, pady=5)
        
        # Quick date buttons
        quick_dates_frame = ctk.CTkFrame(parent, corner_radius=10)
        quick_dates_frame.pack(fill="x", padx=10, pady=10)
        
        today_btn = ctk.CTkButton(quick_dates_frame, text="Today", 
                                command=self.go_to_today, height=35,
                                corner_radius=8)
        today_btn.pack(fill="x", padx=5, pady=5)
        
        yesterday_btn = ctk.CTkButton(quick_dates_frame, text="Yesterday", 
                                    command=self.go_to_yesterday, height=35,
                                    corner_radius=8, fg_color="gray40", hover_color="gray50")
        yesterday_btn.pack(fill="x", padx=5, pady=5)
        
        tomorrow_btn = ctk.CTkButton(quick_dates_frame, text="Tomorrow", 
                                   command=self.go_to_tomorrow, height=35,
                                   corner_radius=8, fg_color="gray40", hover_color="gray50")
        tomorrow_btn.pack(fill="x", padx=5, pady=5)
        
        # Mini calendar
        self.create_mini_calendar(parent)
        
        # Statistics panel
        self.create_stats_panel(parent)
        
    def create_mini_calendar(self, parent):
        """Create a mini calendar widget"""
        cal_frame = ctk.CTkFrame(parent, corner_radius=10)
        cal_frame.pack(fill="x", padx=10, pady=10)
        
        # Calendar title
        cal_title = ctk.CTkLabel(cal_frame, text="Quick Select", 
                               font=ctk.CTkFont(size=16, weight="bold"))
        cal_title.pack(pady=(10, 5))
        
        # Month navigation
        month_nav = ctk.CTkFrame(cal_frame, corner_radius=8)
        month_nav.pack(fill="x", padx=10, pady=5)
        
        prev_month_btn = ctk.CTkButton(month_nav, text="◀", width=30,
                                     command=self.prev_month, corner_radius=5)
        prev_month_btn.pack(side="left", padx=2)
        
        self.month_label = ctk.CTkLabel(month_nav, text="", 
                                      font=ctk.CTkFont(size=14, weight="bold"))
        self.month_label.pack(side="left", expand=True)
        
        next_month_btn = ctk.CTkButton(month_nav, text="▶", width=30,
                                     command=self.next_month, corner_radius=5)
        next_month_btn.pack(side="right", padx=2)
        
        # Calendar grid
        self.calendar_frame = ctk.CTkFrame(cal_frame, corner_radius=8)
        self.calendar_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.update_calendar()
        
    def create_stats_panel(self, parent):
        """Create statistics panel"""
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        stats_title = ctk.CTkLabel(stats_frame, text="📊 Statistics", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        stats_title.pack(pady=(10, 5))
        
        self.stats_content = ctk.CTkFrame(stats_frame, corner_radius=8)
        self.stats_content.pack(fill="x", padx=10, pady=(0, 10))
        
    def create_tasks_panel(self, parent):
        """Create the main tasks panel"""
        # Tasks header
        tasks_header_frame = ctk.CTkFrame(parent, corner_radius=10, height=80)
        tasks_header_frame.pack(fill="x", padx=20, pady=(20, 10))
        tasks_header_frame.pack_propagate(False)
        
        # Selected date display
        self.selected_date_label = ctk.CTkLabel(tasks_header_frame, text="", 
                                              font=ctk.CTkFont(size=24, weight="bold"))
        self.selected_date_label.pack(pady=15)
        
        # Add task section
        add_task_frame = ctk.CTkFrame(parent, corner_radius=10)
        add_task_frame.pack(fill="x", padx=20, pady=10)
        
        # Add task title
        add_title = ctk.CTkLabel(add_task_frame, text="✨ Add New Task", 
                               font=ctk.CTkFont(size=18, weight="bold"))
        add_title.pack(pady=(15, 10))
        
        # Task input row
        input_row1 = ctk.CTkFrame(add_task_frame, corner_radius=8)
        input_row1.pack(fill="x", padx=15, pady=5)
        
        self.task_entry = ctk.CTkEntry(input_row1, placeholder_text="Enter task title...", 
                                     height=40, corner_radius=8, font=ctk.CTkFont(size=14))
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Category selection
        self.category_var = ctk.StringVar(value="General")
        category_menu = ctk.CTkOptionMenu(input_row1, variable=self.category_var,
                                        values=["General", "Work", "Personal", "Health", "Learning"],
                                        height=40, corner_radius=8)
        category_menu.pack(side="right", padx=5, pady=5)
        
        # Description and priority row
        input_row2 = ctk.CTkFrame(add_task_frame, corner_radius=8)
        input_row2.pack(fill="x", padx=15, pady=5)
        
        self.desc_entry = ctk.CTkEntry(input_row2, placeholder_text="Description (optional)...", 
                                     height=40, corner_radius=8, font=ctk.CTkFont(size=14))
        self.desc_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Priority selection
        self.priority_var = ctk.StringVar(value="⚡ Medium")
        priority_menu = ctk.CTkOptionMenu(input_row2, variable=self.priority_var,
                                        values=["🔥 High", "⚡ Medium", "🟢 Low"],
                                        height=40, corner_radius=8)
        priority_menu.pack(side="right", padx=5, pady=5)
        
        # Time estimate and add button row
        input_row3 = ctk.CTkFrame(add_task_frame, corner_radius=8)
        input_row3.pack(fill="x", padx=15, pady=(5, 15))
        
        time_label = ctk.CTkLabel(input_row3, text="Est. Time (min):")
        time_label.pack(side="left", padx=5, pady=5)
        
        self.time_entry = ctk.CTkEntry(input_row3, placeholder_text="30", width=80,
                                     height=40, corner_radius=8)
        self.time_entry.pack(side="left", padx=5, pady=5)
        
        # Add button
        add_btn = ctk.CTkButton(input_row3, text="➕ Add Task", 
                              command=self.add_task, height=40, corner_radius=8,
                              font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.pack(side="right", padx=5, pady=5)
        
        # Tasks list section
        tasks_list_frame = ctk.CTkFrame(parent, corner_radius=10)
        tasks_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Filter and sort options
        filter_frame = ctk.CTkFrame(tasks_list_frame, corner_radius=8)
        filter_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        filter_label = ctk.CTkLabel(filter_frame, text="Filter:", font=ctk.CTkFont(size=14))
        filter_label.pack(side="left", padx=5)
        
        self.filter_var = ctk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(filter_frame, variable=self.filter_var,
                                      values=["All", "Completed", "Pending", "High Priority"],
                                      command=self.filter_tasks, corner_radius=8)
        filter_menu.pack(side="left", padx=5)
        
        # Tasks scrollable area
        self.tasks_scrollable = ctk.CTkScrollableFrame(tasks_list_frame, corner_radius=8)
        self.tasks_scrollable.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Bind Enter key to add task
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Update date displays
        self.update_date_displays()
        
    def update_date_displays(self):
        """Update all date-related displays"""
        # Format dates
        selected_str = self.selected_date.strftime("%A, %B %d, %Y")
        nav_str = self.selected_date.strftime("%m/%d/%Y")
        
        # Update labels
        self.date_label.configure(text=nav_str)
        self.selected_date_label.configure(text=selected_str)
        
        # Update calendar
        self.update_calendar()
        
        # Add today indicator
        if self.selected_date == date.today():
            self.selected_date_label.configure(text=f"📅 Today - {selected_str}")
        elif self.selected_date == date.today() - timedelta(days=1):
            self.selected_date_label.configure(text=f"📅 Yesterday - {selected_str}")
        elif self.selected_date == date.today() + timedelta(days=1):
            self.selected_date_label.configure(text=f"📅 Tomorrow - {selected_str}")
        
    def update_calendar(self):
        """Update the mini calendar"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Current month/year
        cal_year = self.selected_date.year
        cal_month = self.selected_date.month
        
        # Month label
        month_name = calendar.month_name[cal_month]
        self.month_label.configure(text=f"{month_name} {cal_year}")
        
        # Days of week headers
        days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for i, day in enumerate(days):
            label = ctk.CTkLabel(self.calendar_frame, text=day, 
                               font=ctk.CTkFont(size=10, weight="bold"))
            label.grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
            
        # Calendar days
        cal = calendar.monthcalendar(cal_year, cal_month)
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                    
                # Create date for this day
                day_date = date(cal_year, cal_month, day)
                
                # Button styling
                if day_date == self.selected_date:
                    fg_color = "blue"
                    hover_color = "darkblue"
                elif day_date == date.today():
                    fg_color = "green"
                    hover_color = "darkgreen"
                else:
                    fg_color = "gray40"
                    hover_color = "gray50"
                    
                btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=30, height=25,
                                  command=lambda d=day_date: self.select_date(d),
                                  fg_color=fg_color, hover_color=hover_color,
                                  corner_radius=5, font=ctk.CTkFont(size=10))
                btn.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                
        # Configure grid weights
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
            
    def select_date(self, selected_date):
        """Select a specific date"""
        self.selected_date = selected_date
        self.update_date_displays()
        self.load_tasks()
        
    def previous_day(self):
        """Go to previous day"""
        self.selected_date -= timedelta(days=1)
        self.update_date_displays()
        self.load_tasks()
        
    def next_day(self):
        """Go to next day"""
        self.selected_date += timedelta(days=1)
        self.update_date_displays()
        self.load_tasks()
        
    def go_to_today(self):
        """Go to today"""
        self.selected_date = date.today()
        self.update_date_displays()
        self.load_tasks()
        
    def go_to_yesterday(self):
        """Go to yesterday"""
        self.selected_date = date.today() - timedelta(days=1)
        self.update_date_displays()
        self.load_tasks()
        
    def go_to_tomorrow(self):
        """Go to tomorrow"""
        self.selected_date = date.today() + timedelta(days=1)
        self.update_date_displays()
        self.load_tasks()
        
    def prev_month(self):
        """Go to previous month"""
        if self.selected_date.month == 1:
            self.selected_date = self.selected_date.replace(year=self.selected_date.year-1, month=12)
        else:
            self.selected_date = self.selected_date.replace(month=self.selected_date.month-1)
        self.update_date_displays()
        self.load_tasks()
        
    def next_month(self):
        """Go to next month"""
        if self.selected_date.month == 12:
            self.selected_date = self.selected_date.replace(year=self.selected_date.year+1, month=1)
        else:
            self.selected_date = self.selected_date.replace(month=self.selected_date.month+1)
        self.update_date_displays()
        self.load_tasks()
        
    def add_task(self):
        """Add a new task to the database"""
        title = self.task_entry.get().strip()
        description = self.desc_entry.get().strip()
        # Extract priority text, removing emoji
        priority_text = self.priority_var.get()
        if " " in priority_text:
            priority = priority_text.split()[1]  # Remove emoji
        else:
            priority = priority_text  # Fallback if no emoji
        category = self.category_var.get()
        time_estimate = self.time_entry.get().strip() or "30"
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title!")
            return
            
        try:
            time_estimate = int(time_estimate)
        except ValueError:
            time_estimate = 30
            
        # Insert into database
        self.cursor.execute('''
            INSERT INTO tasks (title, description, priority, category, estimated_time, date_created)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, priority, category, time_estimate, self.selected_date))
        self.conn.commit()
        
        # Clear input fields
        self.task_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.priority_var.set("⚡ Medium")
        self.category_var.set("General")
        self.time_entry.delete(0, 'end')
        
        # Refresh task list
        self.load_tasks()
        
    def load_tasks(self):
        """Load and display tasks for selected date"""
        # Clear existing task widgets
        for widget in self.tasks_scrollable.winfo_children():
            widget.destroy()
            
        # Get tasks for selected date
        self.cursor.execute('''
            SELECT id, title, description, priority, category, completed, estimated_time
            FROM tasks 
            WHERE date_created = ?
            ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                END,
                completed ASC
        ''', (self.selected_date,))
        
        tasks = self.cursor.fetchall()
        
        # Apply filters
        filtered_tasks = self.apply_filters(tasks)
        
        if not filtered_tasks:
            no_tasks_label = ctk.CTkLabel(self.tasks_scrollable, 
                                        text="🎯 No tasks found for this date and filter.\nAdd some tasks above!", 
                                        font=ctk.CTkFont(size=16))
            no_tasks_label.pack(pady=40)
        else:
            for task in filtered_tasks:
                self.create_task_widget(task)
                
        # Update statistics
        self.update_stats()
        
    def apply_filters(self, tasks):
        """Apply current filter to tasks"""
        filter_type = self.filter_var.get()
        
        if filter_type == "All":
            return tasks
        elif filter_type == "Completed":
            return [task for task in tasks if task[5] == 1]
        elif filter_type == "Pending":
            return [task for task in tasks if task[5] == 0]
        elif filter_type == "High Priority":
            return [task for task in tasks if task[3] == "High"]
        
        return tasks
        
    def filter_tasks(self, *args):
        """Handle filter change"""
        self.load_tasks()
        
    def create_task_widget(self, task):
        """Create a widget for a single task"""
        task_id, title, description, priority, category, completed, estimated_time = task
        
        # Task frame with enhanced styling
        task_frame = ctk.CTkFrame(self.tasks_scrollable, corner_radius=10, height=100)
        task_frame.pack(fill="x", padx=5, pady=8)
        task_frame.pack_propagate(False)
        
        # Left side - checkbox and content
        left_frame = ctk.CTkFrame(task_frame, corner_radius=8)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Top row - checkbox, title, priority, category
        top_row = ctk.CTkFrame(left_frame, corner_radius=5)
        top_row.pack(fill="x", padx=5, pady=5)
        
        # Checkbox
        checkbox = ctk.CTkCheckBox(top_row, text="", width=25, height=25,
                                 command=lambda: self.toggle_task(task_id))
        checkbox.pack(side="left", padx=5, pady=5)
        
        if completed:
            checkbox.select()
        
        # Title
        title_text = f"✓ {title}" if completed else title
        title_label = ctk.CTkLabel(top_row, text=title_text,
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left", padx=10, pady=5)
        
        # Priority badge
        priority_colors = {"High": "red", "Medium": "orange", "Low": "green"}
        priority_emoji = {"High": "🔥", "Medium": "⚡", "Low": "🟢"}
        priority_color = priority_colors.get(priority, "gray")
        priority_text = f"{priority_emoji.get(priority, '')} {priority}"
        
        priority_label = ctk.CTkLabel(top_row, text=priority_text,
                                    text_color=priority_color,
                                    font=ctk.CTkFont(size=12, weight="bold"))
        priority_label.pack(side="right", padx=5, pady=5)
        
        # Category badge
        category_label = ctk.CTkLabel(top_row, text=f"📁 {category}",
                                    text_color="gray70",
                                    font=ctk.CTkFont(size=11))
        category_label.pack(side="right", padx=5, pady=5)
        
        # Bottom row - description and time
        if description or estimated_time:
            bottom_row = ctk.CTkFrame(left_frame, corner_radius=5)
            bottom_row.pack(fill="x", padx=5, pady=(0, 5))
            
            if description:
                desc_label = ctk.CTkLabel(bottom_row, text=f"📝 {description}",
                                        font=ctk.CTkFont(size=12),
                                        text_color="gray60")
                desc_label.pack(side="left", padx=5, pady=2, anchor="w")
            
            if estimated_time:
                time_label = ctk.CTkLabel(bottom_row, text=f"⏱️ {estimated_time} min",
                                        font=ctk.CTkFont(size=11),
                                        text_color="gray60")
                time_label.pack(side="right", padx=5, pady=2)
        
        # Right side - action buttons
        actions_frame = ctk.CTkFrame(task_frame, corner_radius=8)
        actions_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Edit button
        edit_btn = ctk.CTkButton(actions_frame, text="✏️", width=40, height=35,
                               command=lambda: self.edit_task(task_id),
                               fg_color="gray40", hover_color="gray50",
                               corner_radius=8)
        edit_btn.pack(pady=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(actions_frame, text="🗑️", width=40, height=35,
                                 command=lambda: self.delete_task(task_id),
                                 fg_color="red", hover_color="darkred",
                                 corner_radius=8)
        delete_btn.pack(pady=2)
        
    def toggle_task(self, task_id):
        """Toggle task completion status"""
        # Get current status
        self.cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        current_status = self.cursor.fetchone()[0]
        
        # Toggle status
        new_status = 1 if current_status == 0 else 0
        completion_date = date.today() if new_status == 1 else None
        
        self.cursor.execute('''
            UPDATE tasks 
            SET completed = ?, date_completed = ?
            WHERE id = ?
        ''', (new_status, completion_date, task_id))
        self.conn.commit()
        
        # Refresh display
        self.load_tasks()
        
    def edit_task(self, task_id):
        """Edit a task (placeholder for now)"""
        messagebox.showinfo("Edit Task", "Edit functionality coming soon!")
        
    def delete_task(self, task_id):
        """Delete a task"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            self.load_tasks()
            
    def update_stats(self):
        """Update task statistics"""
        # Clear existing stats
        for widget in self.stats_content.winfo_children():
            widget.destroy()
            
        # Get stats for selected date
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(completed) as completed,
                SUM(estimated_time) as total_time,
                SUM(CASE WHEN completed = 1 THEN estimated_time ELSE 0 END) as completed_time
            FROM tasks 
            WHERE date_created = ?
        ''', (self.selected_date,))
        
        result = self.cursor.fetchone()
        total_tasks = result[0] if result[0] else 0
        completed_tasks = result[1] if result[1] else 0
        total_time = result[2] if result[2] else 0
        completed_time = result[3] if result[3] else 0
        
        # Create stats display
        if total_tasks == 0:
            stats_label = ctk.CTkLabel(self.stats_content, text="📊 No tasks", 
                                     font=ctk.CTkFont(size=14))
            stats_label.pack(pady=5)
        else:
            progress_percentage = (completed_tasks / total_tasks) * 100
            
            # Progress text
            progress_label = ctk.CTkLabel(self.stats_content, 
                                        text=f"✅ {completed_tasks}/{total_tasks} tasks",
                                        font=ctk.CTkFont(size=14, weight="bold"))
            progress_label.pack(pady=2)
            
            # Percentage
            percent_label = ctk.CTkLabel(self.stats_content, 
                                       text=f"{progress_percentage:.1f}% complete",
                                       font=ctk.CTkFont(size=12))
            percent_label.pack(pady=2)
            
            # Time stats
            time_label = ctk.CTkLabel(self.stats_content, 
                                    text=f"⏱️ {completed_time}/{total_time} min",
                                    font=ctk.CTkFont(size=12))
            time_label.pack(pady=2)
            
            # Progress bar
            progress_bar = ctk.CTkProgressBar(self.stats_content, width=200, height=15)
            progress_bar.pack(pady=5)
            progress_bar.set(progress_percentage / 100)
        
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    # Check if customtkinter is installed
    try:
        import customtkinter as ctk
    except ImportError:
        print("CustomTkinter is not installed. Please install it using:")
        print("pip install customtkinter")
        exit(1)
    
    app = TaskTracker()
    app.run()