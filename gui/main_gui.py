import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QMessageBox, QHBoxLayout, QCheckBox, QFrame
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QPropertyAnimation, QByteArray, QRect

from core.report_generator import PDFReport
from core.system_snapshot import get_reports_list
import subprocess


class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - Sistema di Audit")
        self.setGeometry(100, 100, 900, 650)

        self.is_dark_mode = True  # tema iniziale
        self.fade_anim = None     # inizializzazione prevenzione errore

        self._setup_ui()
        self._apply_theme()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if pixmap.isNull():
            logo_label.setText("Logo non trovato")
        else:
            scaled_pixmap = pixmap.scaled(180, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Switch tema
        self.theme_switch = QCheckBox("Tema Scuro")
        self.theme_switch.setChecked(self.is_dark_mode)
        self.theme_switch.stateChanged.connect(self._toggle_theme)
        layout.addWidget(self.theme_switch)

        # Lista report
        self.report_list = QListWidget()
        layout.addWidget(self.report_list)

        # Sidebar simulata
        sidebar = QHBoxLayout()

        self.generate_btn = QPushButton("Genera Report")
        self.generate_btn.setIcon(QIcon.fromTheme("document-new"))
        self.generate_btn.clicked.connect(self.generate_pdf)
        sidebar.addWidget(self.generate_btn)

        self.view_btn = QPushButton("Visualizza Report")
        self.view_btn.setIcon(QIcon.fromTheme("document-preview"))
        self.view_btn.clicked.connect(self.view_selected_report)
        sidebar.addWidget(self.view_btn)

        layout.addLayout(sidebar)

        # Separatore visivo
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        self.setLayout(layout)
        self._load_report_list()

    def _toggle_theme(self):
        self.is_dark_mode = self.theme_switch.isChecked()
        self._apply_theme()

    def _apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    font-family: "Segoe UI", sans-serif;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #2d2d30;
                    color: #ffffff;
                    border-radius: 6px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #3e3e42;
                }
                QCheckBox {
                    padding: 5px;
                }
                QListWidget {
                    background-color: #2d2d30;
                    color: #ffffff;
                    border: 1px solid #555;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                    font-family: "Segoe UI", sans-serif;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000000;
                    border-radius: 6px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QCheckBox {
                    padding: 5px;
                }
                QListWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                    border: 1px solid #aaa;
                }
            """)

    def _load_report_list(self):
        self.report_list.clear()
        reports = get_reports_list()
        if reports:
            for rpt in sorted(reports, reverse=True):
                self.report_list.addItem(rpt)
        else:
            self.report_list.addItem("Nessun report trovato")

        # Effetto fade-in
        self.fade_anim = QPropertyAnimation(self.report_list, b"windowOpacity")
        self.report_list.setWindowOpacity(0.0)
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def generate_pdf(self):
        try:
            pdf = PDFReport()  # filename viene gestito internamente
            pdf.generate_full_report()
            self._load_report_list()
            QMessageBox.information(self, "Successo", "Report generato correttamente!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{str(e)}")

    def view_selected_report(self):
        selected = self.report_list.currentItem()
        if not selected or "Nessun report" in selected.text():
            QMessageBox.warning(self, "Attenzione", "Seleziona un report valido.")
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
