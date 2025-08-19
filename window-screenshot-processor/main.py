# Developer: Demarjio Brady
# Description: Automatically detects if a specified window is active, captures a screenshot, 
#              and applies image-processing effects such as grayscale conversion, resizing, 
#              blurring, thresholding, and edge detection.
# Note: 
#   - `FILE_TYPE` should include the dot (e.g., ".png") to work correctly.
#   - `SCREENSHOT_DIRECTORY` is where the raw screenshots are saved.
#   - `SAMPLE_DIRECTORY` is where the processed images are stored.

# Imports
import os
import time
import pygetwindow as getwindow
import pyautogui as autogui
import logging
import cv2

# Screenshot settings
SCREENSHOT_DIRECTORY = ""
SAMPLE_DIRECTORY = ""
FILE_TYPE = ""

# Program settings
WINDOW_NAME = "Firefox"

# Set up logging config
logging.basicConfig(
    level=logging.DEBUG,  # minimum level to capture
    format='[%(asctime)s] [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def is_window_active(window_name, relative_name=False):
    active_windows = getwindow.getActiveWindow()
    if active_windows is None:
        return False
    
    if relative_name:
        return window_name in active_windows.title

    return active_windows.title == window_name

def get_window_resolution(window_name):
    window_active = is_window_active(window_name, True)
    if not window_active:
        logging.warning(f"No active window found with title: {window_name}")
        return 0, 0, 0, 0

    windows = getwindow.getWindowsWithTitle(window_name)
    if not windows:
        raise ValueError(f"No window found with title: {window_name}")
    
    window = windows[0]
    return window.left, window.top, window.width, window.height


def screenshot_window():
    window_x, window_y, window_width, window_height = get_window_resolution(WINDOW_NAME)
    if all([window_x == 0, window_y == 0, 
            window_width == 0, window_y == 0]):
        return

    latest_file_index = get_latest_file_index()

    # Convert to int safely, default to 0 if None or error
    try:
        latest_index_num = int(latest_file_index)
    except (TypeError, ValueError):
        latest_index_num = 0

    new_index = latest_index_num + 1
    file_name = f"{new_index}{FILE_TYPE}"
    full_path = os.path.join(SCREENSHOT_DIRECTORY, file_name)

    autogui.screenshot(full_path, region=(window_x, window_y, window_width, window_height))
    logging.info(f"Saved screenshot as {file_name}")

    apply_screenshot_filters(file_name, full_path)

def apply_screenshot_filters(file_name, full_path):
    screenshot = cv2.imread(full_path)

    # Apply grayscale effects
    grayscale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Downscale the resolution
    smaller_res = cv2.resize(grayscale_screenshot, (0, 0), fx=0.5, fy=0.5)

    # Blur the screenshot
    blurred = cv2.GaussianBlur(smaller_res, (5, 5), 0)

    # Apply a threshold
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply canny edge detection
    edges = cv2.Canny(thresh, 100, 200)
    cv2.imwrite(f"{SAMPLE_DIRECTORY}/{file_name}", edges)
    logging.info(f"Saved filtered screenshot as {file_name}")


def get_clean_file_name(file_name):
    return file_name.split(FILE_TYPE)[0]

def get_file_names_in_dir():
    file_names = []

    for entry in os.listdir(SCREENSHOT_DIRECTORY):
        full_path = os.path.join(SCREENSHOT_DIRECTORY, entry)

        if os.path.isfile(full_path) and full_path.endswith(FILE_TYPE):
            split_path = full_path.split("\\")
            file_name  = split_path[1]
            file_names.append(file_name)

    return file_names


def get_latest_file_index():
    file_names = get_file_names_in_dir()
    if not file_names:
        return None

    file_names.sort(key=lambda name: int(''.join(filter(str.isdigit, name))) if any(ch.isdigit() for ch in name) else name)

    latest_file = file_names[-1]
    clean_file_name = get_clean_file_name(latest_file)
    return clean_file_name


time.sleep(3)
screenshot_window()
