import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from core.report_generator import PDFReport

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit")
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        self.label = QLabel("Premi il pulsante per generare il report.")
        self.layout.addWidget(self.label)

        self.generate_button = QPushButton("Genera Report PDF")
        self.generate_button.clicked.connect(self.generate_pdf)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def generate_pdf(self):
        try:
            filename = "reports/audit_report.pdf"
            pdf = PDFReport(filename=filename)
            QMessageBox.information(self, "Successo", f"Report generato: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{e}")

def main():
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
