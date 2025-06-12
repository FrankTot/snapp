import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

from core.report_generator import PDFReport
from core.system_snapshot import get_reports_list
import subprocess

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - Sistema di Audit")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #5c5c5c;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #505357;
            }
            QListWidget {
                background-color: #353535;
                border: 1px solid #5c5c5c;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)
        sidebar_frame.setLayout(sidebar)
        sidebar_frame.setStyleSheet("background-color: #1e1e1e;")

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(180, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("[Logo non trovato]")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar.addWidget(logo_label)

        # Buttons
        self.generate_btn = QPushButton("⚙️  Genera Report")
        self.generate_btn.clicked.connect(self.generate_pdf)
        sidebar.addWidget(self.generate_btn)

        self.view_btn = QPushButton("📄  Visualizza Report")
        self.view_btn.clicked.connect(self.view_selected_report)
        sidebar.addWidget(self.view_btn)

        sidebar.addStretch()

        # Content Area
        content_layout = QVBoxLayout()

        title = QLabel("📝 Report Generati")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)

        self.report_list = QListWidget()
        self._load_report_list()
        content_layout.addWidget(self.report_list)

        # Combine Layouts
        main_layout.addWidget(sidebar_frame)
        main_layout.addLayout(content_layout)

    def _load_report_list(self):
        self.report_list.clear()
        reports = get_reports_list()
        if reports:
            for rpt in reports:
                self.report_list.addItem(rpt)
        else:
            self.report_list.addItem("Nessun report trovato")

    def generate_pdf(self):
        try:
            filename = None
            pdf = PDFReport(filename=filename)
            pdf.generate_full_report()
            self._load_report_list()
            QMessageBox.information(self, "Successo", "Report generato correttamente!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{str(e)}")

    def view_selected_report(self):
        selected = self.report_list.currentItem()
        if not selected or "Nessun report trovato" in selected.text():
            QMessageBox.warning(self, "Attenzione", "Seleziona un report dalla lista.")
            return
        report_path = os.path.join("reports", selected.text())
        if not os.path.exists(report_path):
            QMessageBox.warning(self, "Errore", "File report non trovato.")
            return
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', report_path], check=False)
            elif sys.platform == 'win32':
                os.startfile(report_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', report_path], check=False)
            else:
                QMessageBox.warning(self, "Errore", "Sistema operativo non supportato per l'apertura automatica del PDF.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nell'aprire il report:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
