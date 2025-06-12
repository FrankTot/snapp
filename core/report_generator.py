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

        self.filename = filename or f"reports/report__{self._timestamp()}.pdf"
        self._add_logo()
        self._add_header()

    def _timestamp(self):
        return datetime.now().strftime("%d-%m-%Y__%H_%M_%S")

    def _add_logo(self):
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=8, w=30)
            self.ln(20)

    def _add_header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 102, 204)  # blu acceso
        self.cell(0, 10, "SnapAudit Report", 0, 1, 'C')
        self.ln(10)

    def add_section(self, title, content):
        # Titolo sezione con colore più vivo
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)  # blu scuro
        self.cell(0, 10, title, 0, 1)
        
        self.set_font("Helvetica", size=12)
        self.set_text_color(0, 0, 0)

        if isinstance(content, list) and content and isinstance(content[0], dict):
            headers = list(content[0].keys())
            col_width = self.w / len(headers) - 10

            # Header tabella con sfondo azzurro
            self.set_fill_color(0, 102, 204)
            self.set_text_color(255, 255, 255)  # bianco testo
            for h in headers:
                self.cell(col_width, 10, h, 1, 0, 'C', True)
            self.ln()

            # Righe tabella alternate con sfondi chiari
            fill = False
            self.set_text_color(0, 0, 0)
            for row in content:
                self.set_fill_color(230, 240, 255) if fill else self.set_fill_color(255, 255, 255)
                for v in row.values():
                    self.cell(col_width, 10, str(v), 1, 0, 'L', fill)
                self.ln()
                fill = not fill
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
