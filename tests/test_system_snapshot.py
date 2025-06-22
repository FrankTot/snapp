import pytest
from unittest.mock import patch, CalledProcessError
from core.system_snapshot import get_active_services, get_logged_users, get_open_ports

# Mock data for subprocess.check_output
MOCK_SYSTEMCTL_OUTPUT = """\
systemd-journald.service loaded active running Journal Service
another.service          loaded active running Another Service
dbus.service             loaded active running D-Bus System Message Bus
"""

MOCK_WHO_OUTPUT = """\
user1    tty1         2023-10-26 10:00 (:0)
user2    pts/0        2023-10-26 11:00 (192.168.1.100)
"""

MOCK_SS_OUTPUT_NORMAL = """\
State    Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process
LISTEN   0        4096       127.0.0.53%lo:53              0.0.0.0:*      users:(("systemd-resolve",pid=123,fd=13))
LISTEN   0        128            127.0.0.1:631             0.0.0.0:*      users:(("cupsd",pid=456,fd=7))
LISTEN   0        5              127.0.0.1:5432            0.0.0.0:*      users:(("postgres",pid=789,fd=3))
"""

MOCK_SS_OUTPUT_PERMISSION_DENIED = "Error: Cannot open netlink socket: Permission denied"


# Tests for get_active_services
def test_get_active_services_success(mocker):
    mocker.patch('subprocess.check_output', return_value=MOCK_SYSTEMCTL_OUTPUT)
    services = get_active_services()
    assert len(services) == 3
    assert services[0] == {"Service": "systemd-journald.service", "Description": "Journal Service"}
    assert services[1] == {"Service": "another.service", "Description": "Another Service"}
    assert services[2] == {"Service": "dbus.service", "Description": "D-Bus System Message Bus"}

def test_get_active_services_filenotfound(mocker):
    mocker.patch('subprocess.check_output', side_effect=FileNotFoundError("Comando non trovato"))
    services = get_active_services()
    assert len(services) == 1
    assert services[0]["Service"] == "Errore"
    assert "Comando 'systemctl' non trovato" in services[0]["Description"]

def test_get_active_services_calledprocesserror(mocker):
    mocker.patch('subprocess.check_output', side_effect=CalledProcessError(1, "cmd", stderr="Permission denied"))
    services = get_active_services()
    assert len(services) == 1
    assert services[0]["Service"] == "Errore"
    assert "Errore nell'eseguire 'systemctl': Permission denied" in services[0]["Description"]
    assert "Prova ad eseguire lo script con privilegi elevati" in services[0]["Description"]


# Tests for get_logged_users
def test_get_logged_users_success(mocker):
    mocker.patch('subprocess.check_output', return_value=MOCK_WHO_OUTPUT)
    users = get_logged_users()
    assert len(users) == 2
    assert users[0] == {"User": "user1", "TTY": "tty1", "Login Time": "2023-10-26 10:00"}
    assert users[1] == {"User": "user2", "TTY": "pts/0", "Login Time": "2023-10-26 11:00"}

def test_get_logged_users_filenotfound(mocker):
    mocker.patch('subprocess.check_output', side_effect=FileNotFoundError("Comando non trovato"))
    users = get_logged_users()
    assert len(users) == 1
    assert users[0]["User"] == "Errore"
    assert "Comando 'who' non trovato" in users[0]["Login Time"]

def test_get_logged_users_calledprocesserror(mocker):
    mocker.patch('subprocess.check_output', side_effect=CalledProcessError(1, "cmd", stderr="Some error"))
    users = get_logged_users()
    assert len(users) == 1
    assert users[0]["User"] == "Errore"
    assert "Errore nell'eseguire 'who': Some error" in users[0]["Login Time"]


# Tests for get_open_ports
def test_get_open_ports_success(mocker):
    mocker.patch('subprocess.check_output', return_value=MOCK_SS_OUTPUT_NORMAL)
    ports = get_open_ports()
    assert len(ports) == 3
    assert {"Proto": "LISTEN", "Local Address": "127.0.0.53%lo:53"} in ports
    assert {"Proto": "LISTEN", "Local Address": "127.0.0.1:631"} in ports
    assert {"Proto": "LISTEN", "Local Address": "127.0.0.1:5432"} in ports

def test_get_open_ports_filenotfound(mocker):
    mocker.patch('subprocess.check_output', side_effect=FileNotFoundError("Comando non trovato"))
    ports = get_open_ports()
    assert len(ports) == 1
    assert ports[0]["Proto"] == "Errore"
    assert "Comando 'ss' non trovato" in ports[0]["Local Address"]

def test_get_open_ports_permission_denied(mocker):
    mocker.patch('subprocess.check_output', side_effect=CalledProcessError(1, "ss", stderr=MOCK_SS_OUTPUT_PERMISSION_DENIED))
    ports = get_open_ports()
    assert len(ports) == 1
    assert ports[0]["Proto"] == "Errore"
    assert "Errore nell'eseguire 'ss': Error: Cannot open netlink socket: Permission denied" in ports[0]["Local Address"]
    assert "Prova ad eseguire lo script con privilegi elevati" in ports[0]["Local Address"]

def test_get_open_ports_other_calledprocesserror(mocker):
    mocker.patch('subprocess.check_output', side_effect=CalledProcessError(1, "ss", stderr="Another ss error"))
    ports = get_open_ports()
    assert len(ports) == 1
    assert ports[0]["Proto"] == "Errore"
    assert "Errore nell'eseguire 'ss': Another ss error" in ports[0]["Local Address"]
    # Non dovrebbe suggerire sudo per errori generici
    assert "Prova ad eseguire lo script con privilegi elevati" not in ports[0]["Local Address"]

# Nota: i test per get_recent_etc_modifications sono più complessi da mockare
# a causa dell'interazione con il filesystem (os.walk, os.path.getmtime).
# Richiederebbero il mock di queste funzioni e forse la creazione di una
# struttura di directory/file temporanea (es. con pytest tmp_path fixture).
# Per ora, ci concentriamo sui test basati su subprocess.
