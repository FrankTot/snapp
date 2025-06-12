from fpdf import FPDF
from datetime import datetime
from .system_snapshot import get_active_services, get_logged_users, get_open_ports, get_recent_etc_modifications
import os

class PDFReport(FPDF):
    def __init__(self, filename=None):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Helvetica", size=12)
        self.add_page()

        # Nome file con formato report__gg-mm-aaaa__hh_mm_ss.pdf
        self.filename = filename or f"reports/report__{self._timestamp()}.pdf"
        self._add_logo()
        self._add_header()

    def _timestamp(self):
        # giorno-mese-anno__ora_minuti_secondi
        return datetime.now().strftime("%d-%m-%Y__%H_%M_%S")

    def _add_logo(self):
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=8, w=30)
            self.ln(20)

    def _add_header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(33, 37, 41)  # dark gray
        self.cell(0, 10, "SnapAudit Report", 0, 1, 'C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(52, 58, 64)
        self.cell(0, 10, title, 0, 1)
        self.set_font("Helvetica", size=12)
        self.set_text_color(0, 0, 0)

        if isinstance(content, list) and content and isinstance(content[0], dict):
            headers = list(content[0].keys())
            col_width = self.w / len(headers) - 10
            self.set_fill_color(200, 200, 200)
            for h in headers:
                self.cell(col_width, 10, h, 1, 0, 'C', True)
            self.ln()
            self.set_fill_color(245, 245, 245)
            for row in content:
                for v in row.values():
                    self.cell(col_width, 10, str(v), 1)
                self.ln()
        else:
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            self.multi_cell(0, 8, content)
        self.ln()

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent /etc Modifications", get_recent_etc_modifications())
        self.output(self.filename)
