from PyQt6.QtWidgets import QApplication
import sys
import os
from gui.main_gui import MainGUI

def main():
    if not os.path.exists("reports"):
        os.makedirs("reports")

    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
