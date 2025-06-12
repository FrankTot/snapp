# main_gui.py

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QMessageBox, QHBoxLayout, QCheckBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys, os, subprocess
from core.report_generator import PDFReport
from core.system_snapshot import get_reports_list

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - Sistema di Audit")
        self.setGeometry(100, 100, 800, 600)

        # Variabile per tema (True = dark)
        self.dark_theme_enabled = False

        self._setup_ui()
        self.apply_light_theme()  # tema di default chiaro

    def _setup_ui(self):
        layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if pixmap.isNull():
            logo_label.setText("Logo non trovato")
        else:
            scaled_pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        self.report_list = QListWidget()
        self._load_report_list()
        layout.addWidget(self.report_list)

        button_layout = QHBoxLayout()

        self.generate_btn = QPushButton("📝 Genera Report")
        self.generate_btn.clicked.connect(self.generate_pdf)
        button_layout.addWidget(self.generate_btn)

        self.view_btn = QPushButton("📄 Visualizza Report")
        self.view_btn.clicked.connect(self.view_selected_report)
        button_layout.addWidget(self.view_btn)

        # Toggle tema chiaro/scuro
        self.theme_toggle = QCheckBox("Tema Scuro")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_toggle)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _load_report_list(self):
        self.report_list.clear()
        reports = get_reports_list()
        if reports:
            for rpt in sorted(reports, reverse=True):
                self.report_list.addItem(rpt)
        else:
            self.report_list.addItem("Nessun report trovato")

    def generate_pdf(self):
        try:
            pdf = PDFReport()
            pdf.generate_full_report()
            self._load_report_list()
            QMessageBox.information(self, "Successo", "✅ Report generato correttamente!")
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
                QMessageBox.warning(self, "Errore", "Sistema operativo non supportato.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nell'aprire il report:\n{str(e)}")

    def toggle_theme(self, state):
        if state == Qt.CheckState.Checked.value:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #000;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                color: black;
            }
            QCheckBox {
                padding-left: 10px;
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #ddd;
            }
            QPushButton {
                background-color: #388e3c;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2e7d32;
            }
            QListWidget {
                background-color: #424242;
                border: 1px solid #555;
                color: #eee;
            }
            QCheckBox {
                padding-left: 10px;
            }
        """)
