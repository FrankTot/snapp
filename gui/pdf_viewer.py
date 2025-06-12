import subprocess
import platform
import os

def open_pdf(filepath):
    if not os.path.exists(filepath):
        print(f"Il file {filepath} non esiste")
        return
    system = platform.system()
    if system == "Windows":
        os.startfile(filepath)
    elif system == "Darwin":
        subprocess.call(["open", filepath])
    else:
        subprocess.call(["xdg-open", filepath])
