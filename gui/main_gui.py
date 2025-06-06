from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox
)
from gui.pdf_viewer import PDFViewer
from core.report_generator import PDFReport
import sys
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit GUI")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titolo del report")
        self.layout.addWidget(QLabel("Titolo"))
        self.layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Scrivi qui i contenuti del tuo report...")
        self.layout.addWidget(QLabel("Contenuto"))
        self.layout.addWidget(self.content_input)

        self.generate_button = QPushButton("Genera PDF")
        self.generate_button.clicked.connect(self.generate_pdf)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def generate_pdf(self):
        title = self.title_input.text().strip() or "SnapAudit Report"
        content = self.content_input.toPlainText().strip() or "Contenuto del report non disponibile."

        pdf = PDFReport(title=title)
        pdf.add_section("Contenuto Principale", content)
        output = pdf.save()

        QMessageBox.information(self, "Report generato", f"PDF salvato in:\n{output}")
        self.show_pdf(output)

    def show_pdf(self, path):
        self.viewer = PDFViewer(path)
        self.viewer.setWindowTitle("Visualizzatore PDF - SnapAudit")
        self.viewer.resize(800, 600)
        self.viewer.show()

def run_app():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
