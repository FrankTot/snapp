from PyQt6.QtWidgets import QApplication
import sys
from gui.main_gui import MainGUI
import os

# Crea la cartella "reports" se non esiste
if not os.path.exists("reports"):
    os.makedirs("reports")

def main():
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
