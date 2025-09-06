import sys
import os

def resource_path(relative_path=''):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as a bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as a normal script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)