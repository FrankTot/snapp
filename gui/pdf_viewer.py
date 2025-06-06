from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import os

class PDFViewer(QWidget):
    def __init__(self, pdf_path):
        super().__init__()
        layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        abs_path = os.path.abspath(pdf_path)
        self.web_view.load(QUrl.fromLocalFile(abs_path))
        layout.addWidget(self.web_view)
        self.setLayout(layout)
