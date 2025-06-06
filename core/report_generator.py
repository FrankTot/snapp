import os
import datetime
import urllib.request
from fpdf import FPDF
from .system_snapshot import (
    get_active_services,
    get_logged_users,
    get_open_ports,
    get_recent_etc_modifications
)

class PDFReport:
    def __init__(self, filename="reports/report.pdf"):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.filename = filename
        self.pdf.add_page()
        self._prepare_font()
        self._add_header()
        self.generate_full_report()
        self.pdf.output(self.filename)
        print(f"Report salvato in {self.filename}")

    def _prepare_font(self):
        font_dir = "assets/fonts"
        font_path = os.path.join(font_dir, "DejaVuSans.ttf")

        if not os.path.exists(font_path):
            os.makedirs(font_dir, exist_ok=True)
            print("Scarico font Unicode DejaVuSans...")
            url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf"
            try:
                urllib.request.urlretrieve(url, font_path)
                print("Font scaricato con successo.")
            except Exception as e:
                print("Errore durante il download del font:", e)
                raise

        self.pdf.add_font("DejaVu", "", font_path, uni=True)
        self.pdf.set_font("DejaVu", "", 14)

    def _add_header(self):
        self.pdf.set_font("DejaVu", "B", 16)
        title = f"Audit Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.pdf.cell(0, 10, title, ln=True, align="C")
        self.pdf.ln(10)

    def add_section(self, title, content):
        self.pdf.set_font("DejaVu", "B", 14)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln(5)

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged Users", get_logged_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent /etc Modifications", get_recent_etc_modifications())
