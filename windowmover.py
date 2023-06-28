import csv
import subprocess
import os
import signal
import sys
import time
import pystray
import threading
from PIL import Image
from pywinauto import Desktop


import os
import sys

def construct_exe_path():
    """Constructs the path to the GUIPropView.exe executable."""
    exe_name = "GUIPropView.exe"

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, 'bin', exe_name)


def read_window_positions():
    """Reads the window positions and sizes from a CSV file."""
    filename = os.path.join(os.getcwd(), 'config.csv')
    with open(filename) as f:
        reader = csv.reader(f)
        windows = list(reader)
    return windows


def set_window_positions(windows, exe_path):
    """Sets the positions of the specified windows using GUIPropView.exe."""
    for window in windows:
        title, x, y, *_ = window
        x, y = int(x), int(y)
        try:
            if Desktop(backend='uia').window(title=title).exists():
                command = f'"{exe_path}" /Action SetPos {x} {y} Title:"{title}"'
                subprocess.call(command, shell=True)
        except:
            pass


def set_window_sizes(windows, exe_path):
    """Sets the sizes of the specified windows using GUIPropView.exe."""
    for window in windows:
        title, _, _, width, height = window
        width, height = int(width), int(height)
        try:
            if Desktop(backend='uia').window(title=title).exists():
                command = f'"{exe_path}" /Action SetSize {width} {height} Title:"{title}"'
                subprocess.call(command, shell=True)
        except:
            pass


def quit():
    """Quits the script and removes the system tray icon."""
    tray.stop()
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(0)


def on_quit(icon, item):
    """Callback function for the system tray icon."""
    quit()
    
def continuously_update_windows(windows, exe_path):
    """Continuously updates the positions and sizes of the specified windows."""
    while True:
        set_window_positions(windows, exe_path)
        set_window_sizes(windows, exe_path)
        time.sleep(5)  # You can adjust the delay as needed

def open_icon_image():
    """Opens the icon image file."""
    image_name = "icon.ico"

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(base_path, image_name)
    return Image.open(image_path)

if __name__ == '__main__':
    # Construct the path to the executable file
    exe_path = construct_exe_path()

    # Read the window positions and sizes from the config file
    windows = read_window_positions()

    # Set up the system tray icon
    icon_image = open_icon_image()
    menu = pystray.Menu(pystray.MenuItem('Quit', action=on_quit))
    tray = pystray.Icon('WindowMover', icon_image, 'WindowMover', menu)

    # Start the continuous window updating in a separate thread
    updater_thread = threading.Thread(target=continuously_update_windows, args=(windows, exe_path))
    updater_thread.daemon = True
    updater_thread.start()

    # Run the system tray icon
    tray.run()

