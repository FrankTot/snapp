import subprocess
import os
import pwd
from datetime import datetime, timedelta

def get_active_services():
    try:
        output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=running"], text=True)
        return output
    except subprocess.CalledProcessError:
        return "Errore durante il recupero dei servizi attivi."

def get_logged_in_users():
    try:
        output = subprocess.check_output(["who"], text=True)
        return output
    except subprocess.CalledProcessError:
        return "Errore durante il recupero degli utenti loggati."

def get_open_ports():
    try:
        output = subprocess.check_output(["ss", "-tuln"], text=True)
        return output
    except subprocess.CalledProcessError:
        return "Errore durante il recupero delle porte aperte."

def get_recent_etc_modifications():
    try:
        now = datetime.now()
        threshold = now - timedelta(days=1)
        etc_files = []

        for dirpath, _, filenames in os.walk("/etc"):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime > threshold:
                        etc_files.append(f"{filepath} - Modificato il: {mtime}")
                except Exception:
                    continue

        return "\n".join(etc_files) if etc_files else "Nessuna modifica recente trovata in /etc."
    except Exception as e:
        return f"Errore durante il controllo delle modifiche in /etc: {str(e)}"
