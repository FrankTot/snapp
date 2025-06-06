import subprocess
import os
from datetime import datetime, timedelta

def get_active_services():
    result = subprocess.run(
        ['systemctl', 'list-units', '--type=service', '--state=running'],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_logged_in_users():
    result = subprocess.run(['who'], capture_output=True, text=True)
    return result.stdout.strip()

def get_open_ports():
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    return result.stdout.strip()

def get_recent_etc_changes(hours=24):
    cutoff = datetime.now() - timedelta(hours=hours)
    recent_files = []
    for root, dirs, files in os.walk('/etc'):
        for f in files:
            path = os.path.join(root, f)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime > cutoff:
                    recent_files.append(f"{path} - Last modified: {mtime}")
            except Exception:
                continue
    return "\n".join(recent_files)
