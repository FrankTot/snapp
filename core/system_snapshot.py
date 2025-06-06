import subprocess
import os
from datetime import datetime, timedelta

def get_active_services():
    try:
        output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager", "--no-legend"], text=True)
        services = []
        for line in output.strip().split('\n'):
            parts = line.split()
            if parts:
                services.append({"Service": parts[0], "Description": " ".join(parts[4:])})
        return services
    except Exception as e:
        return [{"Service": "Errore", "Description": str(e)}]

def get_logged_users():
    try:
        output = subprocess.check_output(["who"], text=True)
        users = []
        for line in output.strip().split('\n'):
            parts = line.split()
            if parts:
                users.append({"User": parts[0], "TTY": parts[1], "Login Time": parts[2] + " " + parts[3]})
        return users
    except Exception as e:
        return [{"User": "Errore", "TTY": "", "Login Time": str(e)}]

def get_open_ports():
    try:
        output = subprocess.check_output(["ss", "-tuln"], text=True)
        ports = []
        lines = output.strip().split('\n')
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 5:
                proto = parts[0]
                local_address = parts[4]
                ports.append({"Proto": proto, "Local Address": local_address})
        return ports
    except Exception as e:
        return [{"Proto": "Errore", "Local Address": str(e)}]

def get_recent_etc_modifications(days=7):
    try:
        cutoff = datetime.now() - timedelta(days=days)
        files = []
        for root, _, filenames in os.walk("/etc"):
            for f in filenames:
                path = os.path.join(root, f)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime > cutoff:
                        files.append({"File": path, "Last Modified": mtime.strftime("%Y-%m-%d %H:%M:%S")})
                except:
                    continue
        return files if files else [{"File": "Nessuna modifica recente", "Last Modified": ""}]
    except Exception as e:
        return [{"File": "Errore", "Last Modified": str(e)}]

def get_reports_list():
    folder = "reports"
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".pdf")]
