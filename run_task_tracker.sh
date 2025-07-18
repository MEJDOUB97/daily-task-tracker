#!/bin/bash
# Daily Task Tracker Pro - macOS/Linux Launcher
# This script runs the Task Tracker application

# Get the directory where this script is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the application directory
cd "$APP_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Daily Task Tracker Pro Launcher${NC}"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
        echo "Please install Python 3.8+ from https://python.org"
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check if the main application file exists
if [ ! -f "task_tracker.py" ]; then
    echo -e "${RED}❌ task_tracker.py not found in current directory${NC}"
    echo "Please make sure you're running this from the correct folder"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if CustomTkinter is installed
if ! $PYTHON_CMD -c "import customtkinter" &> /dev/null; then
    echo -e "${YELLOW}⚠️  CustomTkinter is not installed. Installing now...${NC}"
    $PYTHON_CMD -m pip install customtkinter --user
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install CustomTkinter${NC}"
        echo "Please run: $PYTHON_CMD -m pip install customtkinter"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}✅ CustomTkinter installed successfully${NC}"
fi

# Run the application
echo -e "${GREEN}🎯 Starting Daily Task Tracker Pro...${NC}"
echo ""

$PYTHON_CMD task_tracker.py

# Check if the application exited with an error
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Application exited with error${NC}"
    read -p "Press Enter to exit..."
fi