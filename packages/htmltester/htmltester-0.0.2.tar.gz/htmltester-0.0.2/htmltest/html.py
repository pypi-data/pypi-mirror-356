import sys
import os
import subprocess
import argparse

def find_browser(browser_name):
    """Try to find the browser executable based on the browser name."""
    browser_paths = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        "firefox": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        "edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
    }

    for path in browser_paths.get(browser_name.lower(), []):
        if os.path.isfile(path):
            return path

    return None

def auto_detect_browser():
    """Automatically find the first available browser."""
    for browser in ["chrome", "firefox", "edge"]:
        path = find_browser(browser)
        if path:
            return path, browser
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Open an HTML file in a web browser.")
    parser.add_argument("html_file", help="Path to the HTML file to open.")
    parser.add_argument("-b", "--browser", help="Browser to use (chrome, firefox, edge). If omitted, auto-detects.")
    args = parser.parse_args()

    html_file = args.html_file

    if not os.path.isfile(html_file):
        print(f"Error: File '{html_file}' does not exist.")
        sys.exit(1)

    abs_path = os.path.abspath(html_file)
    file_url = f'file:///{abs_path.replace(os.sep, "/")}'

    if args.browser:
        browser_path = find_browser(args.browser)
        if not browser_path:
            print(f"Error: Could not find the browser '{args.browser}'.")
            sys.exit(1)
        browser_name = args.browser
    else:
        browser_path, browser_name = auto_detect_browser()
        if not browser_path:
            print("Error: No supported browsers found (Chrome, Firefox, Edge).")
            sys.exit(1)

    print(f"Opening {html_file} in {browser_name.capitalize()}...")
    subprocess.Popen([browser_path, file_url])
