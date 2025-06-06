import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit
)
from PyQt6.QtCore import Qt
from core.report_generator import PDFReport
import subprocess

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit GUI")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Report Title:")
        self.layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter report title")
        self.layout.addWidget(self.title_input)

        self.generate_btn = QPushButton("Generate PDF Report")
        self.generate_btn.clicked.connect(self.generate_pdf)
        self.layout.addWidget(self.generate_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

    def generate_pdf(self):
        title = self.title_input.text() or "Audit Report"
        self.status_label.setText("Generating report...")
        QApplication.processEvents()  # update UI

        pdf = PDFReport(title=title)
        pdf.generate_full_report()
        output_path = "report.pdf"
        pdf.output(output_path)

        self.status_label.setText(f"Report generated: {output_path}")

        # Open PDF with default viewer (Linux)
        try:
            subprocess.Popen(['xdg-open', output_path])
        except Exception as e:
            self.status_label.setText(f"Report saved but failed to open PDF viewer: {e}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
