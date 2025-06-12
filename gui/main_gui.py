import os
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from core.report_generator import create_report

class MainGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self._setup_ui()
        self._apply_theme()
        print("Modulo GUI caricato")

    def _setup_ui(self):
        self.setWindowTitle("Snapp Report Generator")

        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # Switch tema chiaro/scuro
        self.theme_switch = QtWidgets.QCheckBox("Tema scuro")
        self.theme_switch.stateChanged.connect(self._toggle_theme)
        layout.addWidget(self.theme_switch)

        # Bottone genera report con icona
        self.generate_button = QtWidgets.QPushButton(" Genera Report")
        icon = QtGui.QIcon.fromTheme("document-save")
        self.generate_button.setIcon(icon)
        self.generate_button.clicked.connect(self._generate_report)
        layout.addWidget(self.generate_button)

        # Label di stato
        self.status_label = QtWidgets.QLabel("")
        layout.addWidget(self.status_label)

        # Transizione animata per label stato
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.status_label.setGraphicsEffect(self.opacity_effect)
        self.anim = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)

    def _toggle_theme(self, state):
        self.current_theme = "dark" if state == QtCore.Qt.Checked else "light"
        self._apply_theme()

    def _apply_theme(self):
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #2b2b2b; color: #f0f0f0; }
                QPushButton { background-color: #444; color: #eee; }
                QLabel { color: #ddd; }
                QCheckBox { color: #ccc; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #fff; color: #000; }
                QPushButton { background-color: #ddd; color: #000; }
                QLabel { color: #222; }
                QCheckBox { color: #111; }
            """)

    def _generate_report(self):
        try:
            # Creazione nome file con data leggibile
            now = datetime.datetime.now()
            date_str = now.strftime("%d-%m-%Y__%H-%M-%S")
            filename = f"reports/report_{date_str}.pdf"

            # Creo report passando filename
            create_report(filename, icon=True)

            # Messaggio con animazione fade-in
            self.status_label.setText(f"Report generato con successo: {filename}")
            self.anim.start()
        except Exception as e:
            self.status_label.setText(f"Errore durante la generazione del report: {e}")
            self.anim.start()
