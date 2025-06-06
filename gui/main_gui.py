from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from core.report_generator import PDFReport
from gui.pdf_viewer import open_pdf
import sys
import os
from datetime import datetime

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - Linux System Snapshot Tool")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.generate_button = QPushButton("Genera Report PDF")
        self.generate_button.clicked.connect(self.generate_pdf)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def generate_pdf(self):
        try:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            title = f"Audit Report - {now}"
            filename = f"reports/report_{now}.pdf"
            pdf = PDFReport(filename=filename)
            pdf.generate_full_report()
            QMessageBox.information(self, "Successo", f"Report generato: {filename}")
            open_pdf(filename)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{str(e)}")

if __name__ == "__main__":
    print("Modulo GUI caricato")
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
