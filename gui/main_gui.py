import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from core.report_generator import PDFReport
from gui.pdf_viewer import open_pdf
import os

class AuditGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - GUI")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Clicca il bottone per generare un PDF Audit", self)
        layout.addWidget(self.label)

        self.button = QPushButton("Genera Report PDF")
        self.button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def generate_pdf(self):
        try:
            print("Generazione report in corso...")
            pdf = PDFReport()
            pdf.generate_full_report()
            filename = "reports/report.pdf"
            pdf.output(filename)
            open_pdf(filename)
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

def run_gui():
    app = QApplication(sys.argv)
    window = AuditGUI()
    window.show()
    sys.exit(app.exec())
