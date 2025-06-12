from PyQt6.QtWidgets import QApplication
import sys
from gui.main_gui import MainGUI

def main():
    if not os.path.exists("reports"):
        os.makedirs("reports")

    app = QApplication(sys.argv)  # PRIMA crei QApplication
    window = MainGUI()             # POI crei il widget/finestra
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
