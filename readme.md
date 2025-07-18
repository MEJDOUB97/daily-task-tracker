# 📋 Daily Task Tracker Pro

A beautiful and modern desktop task management application built with Python and CustomTkinter.

![Task Tracker Pro](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 Task Management
- **Create, edit, and delete tasks** with rich details
- **Priority levels** with color coding (🔥 High, ⚡ Medium, 🟢 Low)
- **Categories** to organize tasks (Work, Personal, Health, Learning, General)
- **Time estimates** to track how long tasks should take
- **Task completion** with visual checkmarks

### 📅 Calendar Integration
- **Interactive mini calendar** for easy date navigation
- **Quick date jumps** (Today, Yesterday, Tomorrow)
- **Month navigation** with visual indicators
- **Date-specific task views** to see tasks for any day

### 📊 Statistics & Analytics
- **Progress tracking** with visual progress bars
- **Completion percentages** for daily productivity
- **Time tracking** showing estimated vs completed time
- **Real-time statistics** that update as you work

### 🎨 Modern Interface
- **Dark theme** with professional appearance
- **Responsive design** that works on different screen sizes
- **Smooth animations** and hover effects
- **Emoji integration** for better visual appeal
- **Clean, organized layout** with intuitive navigation

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/daily-task-tracker.git
   cd daily-task-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python task_tracker.py
   ```

### Alternative Installation

If you prefer to install dependencies manually:
```bash
pip install customtkinter==5.2.2
```

## 🖥️ Usage

### Getting Started
1. **Launch the app** - Run `python task_tracker.py`
2. **Add your first task** - Enter a title, select category and priority
3. **Set time estimate** - Add estimated completion time in minutes
4. **Check off completed tasks** - Click the checkbox when done
5. **Navigate dates** - Use the calendar to view tasks for different days

### Navigation Tips
- **Calendar Navigation**: Click any date in the mini calendar to jump to that day
- **Quick Buttons**: Use Today/Yesterday/Tomorrow for fast navigation
- **Arrow Keys**: Use the ◀ ▶ buttons to move day by day
- **Filtering**: Use the filter dropdown to view specific types of tasks

### Task Management
- **Adding Tasks**: Fill in the form at the top and click "➕ Add Task"
- **Completing Tasks**: Click the checkbox next to any task
- **Deleting Tasks**: Click the 🗑️ button (confirms before deletion)
- **Editing Tasks**: Click the ✏️ button (feature coming soon)

## 📁 Project Structure

```
daily-task-tracker/
├── task_tracker.py         # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE               # MIT License
├── setup.py              # Package setup file
├── .gitignore            # Git ignore rules
└── screenshots/          # Application screenshots
    └── main_interface.png
```

## 🛠️ Technical Details

### Built With
- **Python 3.8+** - Core programming language
- **CustomTkinter** - Modern GUI framework
- **SQLite** - Local database for data persistence
- **Calendar** - Built-in Python calendar module

### Database Schema
The app uses a local SQLite database (`tasks.db`) with the following structure:
- `id` - Unique task identifier
- `title` - Task title
- `description` - Optional task description
- `priority` - High, Medium, or Low
- `category` - Task category
- `completed` - Completion status
- `date_created` - Creation date
- `date_completed` - Completion date
- `estimated_time` - Time estimate in minutes

### Key Features
- **Automatic database migration** - Handles schema updates seamlessly
- **Date-based filtering** - View tasks for any specific date
- **Real-time statistics** - Progress tracking and analytics
- **Persistent data** - All tasks saved locally

## 🎨 Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

*Clean, modern interface with calendar integration and task management*

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/daily-task-tracker.git
cd daily-task-tracker

# Install in development mode
pip install -e .

# Run tests (when available)
python -m pytest
```

## 📋 Roadmap

### Planned Features
- [ ] **Task editing** - Edit existing tasks
- [ ] **Task search** - Search through tasks
- [ ] **Export functionality** - Export tasks to CSV/PDF
- [ ] **Themes** - Light/dark theme toggle
- [ ] **Notifications** - Task reminders
- [ ] **Backup/Restore** - Data backup functionality
- [ ] **Recurring tasks** - Daily/weekly recurring tasks
- [ ] **Sub-tasks** - Break down large tasks
- [ ] **Task templates** - Common task templates

### Known Issues
- Edit functionality is placeholder (coming soon)
- No data export yet
- No task search functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** - For the beautiful modern GUI framework
- **Python Community** - For the excellent ecosystem
- **Contributors** - Thank you to all who help improve this project

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Issues** - See if your problem is already reported
2. **Create an Issue** - Describe your problem with details
3. **Discussion** - Use GitHub Discussions for questions

---

⭐ **Like this project?** Give it a star on GitHub!

**Happy Task Tracking!** 🚀