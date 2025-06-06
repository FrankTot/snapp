from fpdf import FPDF
from datetime import datetime
from core.system_snapshot import (
    get_active_services,
    get_logged_in_users,
    get_open_ports,
    get_recent_etc_modifications,
)
import os
import urllib.request

class PDFReport:
    def __init__(self, filename=None):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.title = f"Audit Report - {now}"
        self.filename = filename or f"reports/report_{now}.pdf"
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self._prepare_font()
        self._add_header()

    def _prepare_font(self):
        font_dir = "assets/fonts"
        font_path = os.path.join(font_dir, "DejaVuSans.ttf")

        if not os.path.exists(font_path):
            os.makedirs(font_dir, exist_ok=True)
            print("Scarico font Unicode DejaVuSans...")
            url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
            try:
                urllib.request.urlretrieve(url, font_path)
                print("Font scaricato con successo.")
            except Exception as e:
                print("Errore durante il download del font:", e)
                raise

        self.pdf.add_font("DejaVu", "", font_path, uni=True)
        self.pdf.set_font("DejaVu", "", 14)

    def _add_header(self):
        try:
            self.pdf.image("assets/logo.png", 10, 8, 33)
        except:
            pass
        self.pdf.set_font("DejaVu", "", 16)
        self.pdf.cell(0, 10, self.title, ln=True, align='C')
        self.pdf.ln(10)

    def add_section(self, title, content):
        self.pdf.set_font("DejaVu", "", 14)
        self.pdf.set_text_color(30, 30, 30)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.set_text_color(50, 50, 50)
        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln(5)

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_in_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent Changes in /etc", get_recent_etc_modifications())
        self._save_pdf()

    def _save_pdf(self):
        self.pdf.output(self.filename)
