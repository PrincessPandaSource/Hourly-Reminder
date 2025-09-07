# Import Python libraries
import sys
# Runtime optimization (as executable)
if getattr(sys, 'frozen', False):
    import os
    # Set process priority to high
    try:
        import psutil
        p = psutil.Process()
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    except ImportError:
        # psutil is not installed
        pass

# Ordered from heaviest to lightest to avoid the delay from lazy loading
import pythoncom
import pywintypes
from windows_toasts import InteractableWindowsToaster
import schedule
import threading
import time
import signal
import argparse
from datetime import datetime

# Import other files as modules
import reminders
import audio_ducking
import systray

# Pre-initialize COM
pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)

# Pre-initialize reminder data and toaster
reminders.toaster = InteractableWindowsToaster('Hourly Reminder', 'PrincessPandaLover.HourlyReminder')

# Parsing
parser = argparse.ArgumentParser(prog='Hourly Reminder',
                    description='An automated program that shows a reminder notification every hour, with a unique image and sound for each hour')
parser.add_argument('-t', '--test',
                    type=str,
                    nargs='?',
                    const='current',
                    help='test reminder at the current hour ("current", default), a specific hour (number) or all of them ("all", please don\'t hover over notifications or else syncing with audio will mess up); you may need to clean up your notifications afterwards'
)
parser.add_argument('-a', '--altaudio',
                    type=str,
                    nargs='?',
                    default='preset',
                    help='change audio from preset audio ("preset") to either the default Windows asterick sound ("system") or no audio ("silence")'
)
parser.add_argument('-d', '--ducking',
                    type=float,
                    nargs='?',
                    const=0.35,
                    help='enable ducking (lowering volume) of applications when the notification\'s sound plays, ducked volume can be specified from 0.0-1.0 (default is 0.35; this is currently experimental; expect bugs, and it cannot restore volumes of apps closed during the sound\'s playing; please check volume mixer if something sounds off)'
)
args = parser.parse_args(sys.argv[1:])

# For when you hover over the notification and it remains longer (especially during testing)
dismiss_event = threading.Event()

# Inject into reminders module
reminders.args = args
reminders.dismiss_event = dismiss_event

# Handling main thread when program is stopped
stop_event = threading.Event()

# Currently commented out until I can debug this
# This is for the executable, because windowed mode will not allow the terminal to intervene
'''
def terminal_stop_handler(quit_func):
    if sys.platform == "win32":
        try:
            import win32api
            import win32con
            import ctypes

            # Check for console window
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window == 0:
                # No console window, try allocating one
                if not ctypes.windll.kernel32.AllocConsole():
                    return

            # If running as executable, try to attach to console
            if getattr(sys, 'frozen', False):
                ctypes.windll.kernel32.AttachConsole(-1)
            
            def handler(ctrl_type):
                if ctrl_type == win32con.CTRL_C_EVENT:
                    quit_func()
                    return True
                return False
            
            if not win32api.SetConsoleCtrlHandler(handler, True):
                print("Warning: Failed to set console control handler")
        except (ImportError, OSError, Exception) as e:
            print(f"Console handler setup failed: {e}")
            pass
'''

def test():
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    try:
        reminders.toaster = InteractableWindowsToaster('Hourly Reminder')
        if args.test:
            if args.test == "current":
                reminders.createReminder(datetime.now().hour)
            elif args.test == "all":
                print("Don't hover over notifications, for that makes them stay longer and thus messes up syncing with the audio")
                print("Press Ctrl+C at any time to stop")

                try:
                    for h in range(24):
                        if (stop_event.is_set()):
                            break

                        reminders.createReminder(h)

                        # Wait for notification to be cleared (and check for stop event in the meantime)
                        while not dismiss_event.is_set():
                            if stop_event.is_set():
                                break
                            time.sleep(1)

                        # Reset dismiss event for next notification
                        dismiss_event.clear()

                        # Try breaking again here
                        if (stop_event.is_set()):
                            break
                        
                        time.sleep(1)
                except KeyboardInterrupt:
                    stop_event.set()
            else:
                reminders.createReminder(int(args.test))
    finally:
        pythoncom.CoUninitialize()

def main():
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    try:
        reminders.toaster = InteractableWindowsToaster('Hourly Reminder')
        for h in range(24):
            h_format = str(h).zfill(2)

            schedule.every().day.at(f"{h_format}:00").do(reminders.createReminder, hour=h)

        print("Hourly Reminder has started")
        
        while not stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    systray_icon = systray.createSystrayIcon(
        lambda icon: systray.quitProgramWithGrace(icon, stop_event, audio_ducking.stopDuckingMonitor)
    )

    # Ctrl+C handlers
    #terminal_stop_handler(lambda: systray.quitProgramWithGrace(systray_icon, stop_event, audio_ducking.stopDuckingMonitor))
    signal.signal(signal.SIGINT, lambda sig, frame: systray.quitProgramWithGrace(systray_icon, stop_event, audio_ducking.stopDuckingMonitor))

    if args.test:
        test()
    else:
        main_thread = threading.Thread(target=main, daemon=True)
        main_thread.start()

        # So the systray icon run function doesn't block
        systray_thread = threading.Thread(target=systray_icon.run, daemon=True)
        systray_thread.start()

        # Ah, ah, ah, ah, stayin' alive, stayin' alive
        try:
            while not stop_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            systray.quitProgramWithGrace(systray_icon)