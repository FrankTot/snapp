import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QListWidget, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from core.report_generator import PDFReport
from core.system_snapshot import get_reports_list
import subprocess

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit GUI")
        self.resize(900, 600)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaledToWidth(180)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)

        self.status_label = QLabel("Pronto per generare report.")
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Genera Report PDF")
        self.generate_btn.clicked.connect(self.generate_pdf)
        btn_layout.addWidget(self.generate_btn)

        self.open_btn = QPushButton("Visualizza Report Selezionato")
        self.open_btn.clicked.connect(self.open_selected_report)
        btn_layout.addWidget(self.open_btn)

        layout.addLayout(btn_layout)

        self.report_list = QListWidget()
        layout.addWidget(self.report_list)
        self.load_reports()

        self.setLayout(layout)

    def load_reports(self):
        self.report_list.clear()
        reports = get_reports_list()
        for rpt in sorted(reports, reverse=True):
            self.report_list.addItem(rpt)

    def generate_pdf(self):
        try:
            pdf = PDFReport()
            filename = pdf.generate_full_report()
            self.status_label.setText(f"Report generato: {filename}")
            self.load_reports()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{e}")

    def open_selected_report(self):
        selected = self.report_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Attenzione", "Seleziona un report dalla lista.")
            return
        filename = os.path.join("reports", selected.text())
        if os.name == "posix":
            try:
                subprocess.run(["xdg-open", filename], check=True)
            except Exception as e:
                QMessageBox.warning(self, "Errore", f"Impossibile aprire il file:\n{e}")
        else:
            QMessageBox.warning(self, "Errore", "Questa funzione è disponibile solo su sistemi GNU/Linux.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
