# Python libraries
from windows_toasts import InteractableWindowsToaster, Toast, ToastDuration, ToastImage, ToastDisplayImage, ToastImagePosition, ToastAudio, AudioSource
import winsound
from datetime import datetime, timedelta
import threading
import os
import time
import json
from functools import lru_cache

# My modules
import audio_ducking
# Import other files as modules
from get_resource_path import resource_path

args = None
dismiss_event: threading.Event = None
assets_folder = resource_path('assets')

toaster : InteractableWindowsToaster = None

# Cache reminder data loading
@lru_cache(maxsize=1)
def load_reminder_data():
    main_folder = resource_path()
    with open(os.path.join(main_folder, 'reminders_data.json'), "r") as f:
        return json.load(f)

def dismissReminder():
    winsound.PlaySound(None, winsound.SND_PURGE)
    if args and args.ducking and args.altaudio == "preset":
        audio_ducking.stopDuckingMonitor()

    if dismiss_event:
        dismiss_event.set()

def createReminder(hour):
    hourDictionaries = load_reminder_data()
    hoursDictionary = -1
    for d in hourDictionaries:
        if d.get("24hour") == hour:
            hoursDictionary = d
    
    if hoursDictionary == -1:
        print("Not found")
        return
    
    print(f"Reminder notification at {hour}:00")

    if dismiss_event:
        dismiss_event.clear()

    reminderToast = Toast()
    reminderToast.text_fields = [
        hoursDictionary.get("title"),
        hoursDictionary.get("description")
    ]
    reminderToast.duration = ToastDuration.Default
    reminderToast.group = "hourly-reminder"
    reminderToast.tag = f"{hour}-reminder"
    reminderToast.expiration_time = datetime.now() + timedelta(hours=5)
    reminderToast.on_activated = lambda _: dismissReminder()
    reminderToast.on_dismissed = lambda *_: dismissReminder()

    # Image
    reminderIconImage = ToastImage(os.path.join(assets_folder, f"images/{hoursDictionary.get("24hour")}.png"))
    reminderIcon = ToastDisplayImage(reminderIconImage)
    reminderIcon.position = ToastImagePosition.AppLogo
    reminderToast.AddImage(reminderIcon)

    toaster.show_toast(reminderToast)

    # Audio
    if args.altaudio == "preset":
        audio_path = (os.path.join(assets_folder, f"sounds/{hoursDictionary.get("24hour")}.wav"))
        if os.path.exists(audio_path):
            if args.ducking:
                if isinstance(args.ducking, (int, float)):
                    audio_ducking.setDuckLevel(args.ducking)

                audio_ducking.startDuckingMonitor()
            
            winsound.PlaySound(audio_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif args.altaudio == "system":
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

    if dismiss_event:
        dismiss_event.wait(timeout=6.5)
        if not dismiss_event.is_set():
            dismissReminder()
    else:
        time.sleep(6.5)
        dismissReminder()