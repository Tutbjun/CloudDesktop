

import os
from PIL import Image
from pystray import Icon, Menu, MenuItem
import threading

# Replace these with the actual file paths for your icons
basedir = os.path.abspath(os.path.dirname(__file__))
connected_icon_path = "connected_icon.png"
disconnected_icon_path = "disconnected_icon.png"
connected_icon_path = os.path.join(basedir, connected_icon_path)
disconnected_icon_path = os.path.join(basedir, disconnected_icon_path)

def check_website_status():
    try:
        response = os.system("curl -k https://85.191.70.197:8006 --connect-timeout 1")
        print(response)
        # Check if the command was successful (return code 0) and if the HTML content is present
        return response == 0
    except:
        return False

def create_icon(on):
    if on:
        image_path = connected_icon_path
        menu = Menu(*connected_menu_options)
    else:
        image_path = disconnected_icon_path
        menu = Menu(*disconnected_menu_options)
    icon = Icon("website_status", Image.open(image_path), menu=menu)
    return icon



def update_icon(icon=None, item=None):
    if icon:
        icon.stop()
    if check_website_status():
        new_icon = create_icon(True)
        print("Running connected icon...")
        run_icon_with_timeout(new_icon)
    else:
        new_icon = create_icon(False)
        print("Running disconnected icon...")
        run_icon_with_timeout(new_icon)
    new_icon.stop()

def main():
    print("Checking website status...")
    icon = update_icon()

def run_icon_with_timeout(icon, timeout=20):
    def run_with_timeout():
        icon.run()
    thread = threading.Thread(target=run_with_timeout)
    thread.start()
    thread.join(timeout)
    icon.stop()

def run_cmd_with_timeout(cmd, timeout=None):
    def run_with_timeout():
        os.system(cmd)
    thread = threading.Thread(target=run_with_timeout)
    thread.start()
    if timeout:
        thread.join(timeout)
    else:
        thread.join()

def on_server_off(icon, item):
    icon.stop()
    # Add your custom action here, e.g., running a script or command
    basedir = os.path.abspath(os.path.dirname(__file__))
    #go one folder up
    upperdir = os.path.dirname(basedir)
    #go to interfaces folder
    lowerdir = os.path.join(upperdir, "serverinterface")
    os.chdir(lowerdir)
    executable = os.path.join(lowerdir, "juststop.bat")
    run_cmd_with_timeout(executable)

def on_server_on(icon, item):
    icon.stop()
    # Add your custom action here, e.g., running a script or command
    basedir = os.path.abspath(os.path.dirname(__file__))
    #go one folder up
    upperdir = os.path.dirname(basedir)
    #go to interfaces folder
    lowerdir = os.path.join(upperdir, "serverinterface")
    os.chdir(lowerdir)
    executable = os.path.join(lowerdir, "juuuststart.bat")
    run_cmd_with_timeout(executable)

def on_exit(icon, item):
    icon.stop()

connected_menu_options = [
    MenuItem('Server off', on_server_off),
    MenuItem('Exit', on_exit)
]

disconnected_menu_options = [
    MenuItem('Server on', on_server_on),
    MenuItem('Exit', on_exit)
]
connected_icon = create_icon(True)
disconnected_icon = create_icon(False)

if __name__ == "__main__":
    while True:
        main()
        