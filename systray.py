# Also handles quitting functions

# Python libraries
import pystray
from PIL import Image
import signal
import sys
import os
import winsound

# My modules
from get_resource_path import resource_path

assets_folder = resource_path('assets')

def createSystrayIcon(quit_callback_function):
    icon = pystray.Icon(
        'Hourly Reminder',
        icon=Image.open(os.path.join(assets_folder, "images/app_icon.ico")),
        title="Hourly Reminder",
        menu=pystray.Menu(
            pystray.MenuItem('Quit', quit_callback_function))
    )

    return icon

def quitProgramWithGrace(icon, stopEvent, stopDuckingFunc):
    print("Hourly Reminder stopped")
    stopEvent.set()

    if callable(stopDuckingFunc):
        try:
            stopDuckingFunc()
        except Exception:
            pass

    winsound.PlaySound(None, winsound.SND_PURGE)

    if icon:
        try:
            icon.stop()
        except Exception:
            pass

    sys.exit(0)

# When program is suddenly Ctrl+C'd
def attachSignalHandler(quitFunc, icon):
    signal.signal(signal.SIGINT, lambda sig, frame: quitFunc(icon))