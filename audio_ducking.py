from pycaw.pycaw import AudioUtilities
import pythoncom
import time
import os
import threading

# For ducking (lowering volume of other apps while notification's sound plays)
duckLevel = 0.35    # Volume when ducked (0.0-1.0)
fadeSteps = 10      # How many times to reduce volume
fadeInterval = 0.01 # Delay between fade steps

myPID = os.getpid()

originalVolumes = {}
monitoring = False
_monitor_thread = None
_monitor_lock = threading.Lock()

def setDuckLevel(level: float):
    global duckLevel
    duckLevel = max(0.0, min(1.0, float(level)))

def fadeVolume(session, start, end):
    step = (end - start) / fadeSteps
    current = start
    for _ in range(fadeSteps):
        current += step
        session.SimpleAudioVolume.SetMasterVolume(current, None)
        time.sleep(fadeInterval)
    session.SimpleAudioVolume.SetMasterVolume(end, None)

# The following ducks new applications if they pop up and play audio while notification's sound is playing
def duckOtherSessions():
    sessions = AudioUtilities.GetAllSessions()

    for s in sessions:
        if not s.Process:
            continue
        
        # Skipping this app
        if s.ProcessId == myPID:
            continue
        
        # Skip if already in processId
        if s.ProcessId in originalVolumes:
            continue

        volumeInterface = s.SimpleAudioVolume
        original = volumeInterface.GetMasterVolume()
        originalVolumes[s.ProcessId] = original
        
        if original > duckLevel:
            fadeVolume(s, original, duckLevel)

def restoreSessionsVolumes():
    sessions = AudioUtilities.GetAllSessions()
    activePIDS = {s.ProcessId for s in sessions if s.Process}

    for s in sessions:
        if s.ProcessId in originalVolumes and s.ProcessId in activePIDS:
            original = originalVolumes[s.ProcessId]
            current = s.SimpleAudioVolume.GetMasterVolume()
            fadeVolume(s, current, original)

    closedPIDS = set(originalVolumes.keys()) - activePIDS
    for pid in closedPIDS:
        del originalVolumes[pid]

    originalVolumes.clear()

def monitorSessions():
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    global monitoring

    try:
        duckOtherSessions()

        while monitoring:
            duckOtherSessions()
            time.sleep(0.5)
    finally:
        pythoncom.CoUninitialize()

def startDuckingMonitor():
    global monitoring, _monitor_thread
    with _monitor_lock:
        if monitoring:
            return
        monitoring = True
        duckOtherSessions()
        _monitor_thread = threading.Thread(target=monitorSessions, daemon=True)
        _monitor_thread.start()

def stopDuckingMonitor(timeout: float = 0.25):
    global monitoring, _monitor_thread
    with _monitor_lock:
        if not monitoring:
            return
        monitoring = False
        if _monitor_thread and _monitor_thread.is_alive():
            _monitor_thread.join(timeout=timeout)
        _monitor_thread = None
        restoreSessionsVolumes()