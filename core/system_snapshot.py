import subprocess
import os
from datetime import datetime, timedelta

def get_active_services():
    try:
        output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager", "--no-legend"], text=True, stderr=subprocess.PIPE)
        services = []
        for line in output.strip().split('\n'):
            parts = line.split()
            if parts:
                services.append({"Service": parts[0], "Description": " ".join(parts[4:])})
        return services
    except FileNotFoundError:
        return [{"Service": "Errore", "Description": "Comando 'systemctl' non trovato. Assicurati che sia installato e nel PATH."}]
    except subprocess.CalledProcessError as e:
        error_message = f"Errore nell'eseguire 'systemctl': {e.stderr}"
        if "permission denied" in e.stderr.lower() or "privileges" in e.stderr.lower():
            error_message += "\nProva ad eseguire lo script con privilegi elevati (es. sudo)."
        return [{"Service": "Errore", "Description": error_message}]
    except Exception as e:
        return [{"Service": "Errore", "Description": f"Errore imprevisto: {str(e)}"}]

def get_logged_users():
    try:
        output = subprocess.check_output(["who"], text=True, stderr=subprocess.PIPE)
        users = []
        for line in output.strip().split('\n'):
            parts = line.split()
            if parts:
                users.append({"User": parts[0], "TTY": parts[1], "Login Time": parts[2] + " " + parts[3]})
        return users
    except FileNotFoundError:
        return [{"User": "Errore", "TTY": "", "Login Time": "Comando 'who' non trovato. Assicurati che sia installato e nel PATH."}]
    except subprocess.CalledProcessError as e:
        return [{"User": "Errore", "TTY": "", "Login Time": f"Errore nell'eseguire 'who': {e.stderr}"}]
    except Exception as e:
        return [{"User": "Errore", "TTY": "", "Login Time": f"Errore imprevisto: {str(e)}"}]

def get_open_ports():
    try:
        output = subprocess.check_output(["ss", "-tuln"], text=True, stderr=subprocess.PIPE)
        ports = []
        lines = output.strip().split('\n')
        for line in lines[1:]: # Salta l'intestazione
            parts = line.split()
            if len(parts) >= 5: # Assicura che ci siano abbastanza parti
                proto = parts[0]
                local_address = parts[4] # Indice corretto per Local Address
                ports.append({"Proto": proto, "Local Address": local_address})
        return ports
    except FileNotFoundError:
        return [{"Proto": "Errore", "Local Address": "Comando 'ss' non trovato. Assicurati che sia installato (es. pacchetto iproute2) e nel PATH."}]
    except subprocess.CalledProcessError as e:
        error_message = f"Errore nell'eseguire 'ss': {e.stderr}"
        if "permission denied" in e.stderr.lower() or "privileges" in e.stderr.lower():
            error_message += "\nProva ad eseguire lo script con privilegi elevati (es. sudo)."
        return [{"Proto": "Errore", "Local Address": error_message}]
    except Exception as e:
        return [{"Proto": "Errore", "Local Address": f"Errore imprevisto: {str(e)}"}]

def get_recent_etc_modifications(days=7):
    try:
        # Verifica dei permessi di lettura per /etc
        if not os.access("/etc", os.R_OK):
            return [{"File": "Errore", "Last Modified": "Permesso negato per leggere la directory /etc."}]

        cutoff = datetime.now() - timedelta(days=days)
        files = []
        for root, _, filenames in os.walk("/etc"):
            for f in filenames:
                path = os.path.join(root, f)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime > cutoff:
                        files.append({"File": path, "Last Modified": mtime.strftime("%Y-%m-%d %H:%M:%S")})
                except OSError: # Potrebbe accadere se un file viene eliminato durante la scansione o per permessi
                    continue
        return files if files else [{"File": "Nessuna modifica recente in /etc", "Last Modified": f"negli ultimi {days} giorni"}]
    except PermissionError: # Specifico per os.walk se non si hanno i permessi sulla directory radice
        return [{"File": "Errore", "Last Modified": "Permesso negato per accedere a /etc o sue sottodirectory."}]
    except Exception as e:
        return [{"File": "Errore", "Last Modified": f"Errore imprevisto durante la scansione di /etc: {str(e)}"}]

def get_reports_list():
    folder = "reports"
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".pdf")]
