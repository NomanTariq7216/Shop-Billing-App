#!/bin/bash
# Launcher script for Shop Billing System (Linux)

echo "Starting Shop Billing System..."
echo "دکان بلنگ سسٹم شروع ہو رہا ہے"
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3 first."
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: tkinter is not installed!"
    echo ""
    echo "Please install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    echo ""
    exit 1
fi

# Run the application
python3 main.py
