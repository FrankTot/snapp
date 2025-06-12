import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QMessageBox, QHBoxLayout, QGraphicsOpacityEffect, QCheckBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation

from core.report_generator import PDFReport
from core.system_snapshot import get_reports_list
import subprocess

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - Sistema di Audit")
        self.setGeometry(100, 100, 900, 600)
        self.theme_dark = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Tema switch
        self.theme_switch = QCheckBox("🌙 Tema Scuro")
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_switch)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if pixmap.isNull():
            logo_label.setText("Logo non trovato")
        else:
            scaled_pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Lista report precedenti con animazione
        self.report_list = QListWidget()
        self.report_list.setStyleSheet("font-size: 14px;")
        self._load_report_list()
        opacity_effect = QGraphicsOpacityEffect()
        self.report_list.setGraphicsEffect(opacity_effect)
        self.fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        layout.addWidget(self.report_list)

        # Bottoni
        button_layout = QHBoxLayout()

        self.generate_btn = QPushButton("📝 Genera Report")
        self.generate_btn.setIcon(QIcon.fromTheme("document-new"))
        self.generate_btn.clicked.connect(self.generate_pdf)
        button_layout.addWidget(self.generate_btn)

        self.view_btn = QPushButton("📂 Visualizza Report")
        self.view_btn.setIcon(QIcon.fromTheme("document-open"))
        self.view_btn.clicked.connect(self.view_selected_report)
        button_layout.addWidget(self.view_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def toggle_theme(self):
        if self.theme_switch.isChecked():
            self.setStyleSheet("""
                QWidget {
                    background-color: #2e2e2e;
                    color: white;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    padding: 8px;
                    border-radius: 8px;
                }
                QListWidget {
                    background-color: #3b3b3b;
                    color: white;
                    border: 1px solid #666;
                }
            """)
        else:
            self.setStyleSheet("")

    def _load_report_list(self):
        self.report_list.clear()
        reports = get_reports_list()
        if reports:
            for rpt in sorted(reports, reverse=True):
                self.report_list.addItem(rpt)
        else:
            self.report_list.addItem("Nessun report trovato")
        self.fade_anim.start()

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
                QMessageBox.warning(self, "Errore", "Sistema operativo non supportato.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nell'aprire il report:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())
