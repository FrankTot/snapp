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
        self._add_header()
        if not os.path.exists("reports"):
            os.makedirs("reports")
        self.filename = filename or f"reports/report_{self._timestamp()}.pdf"

    def _timestamp(self):
        now = datetime.now()
        return now.strftime("%d-%m-%Y__%H-%M-%S")

    def _add_header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(30, 144, 255)
        self.cell(0, 10, "🛡️ SnapAudit Report", 0, 1, 'C')
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def add_section(self, title, content):
        self.set_text_color(0, 102, 204)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", size=12)

        if isinstance(content, list) and content and isinstance(content[0], dict):
            col_width = self.w / 4
            headers = content[0].keys()
            for header in headers:
                self.set_fill_color(230, 230, 250)
                self.cell(col_width, 10, header, 1, 0, 'C', fill=True)
            self.ln()
            for row in content:
                for value in row.values():
                    self.cell(col_width, 10, str(value), 1)
                self.ln()
        else:
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            self.multi_cell(0, 8, content)
        self.ln()

    def generate_full_report(self):
        self.add_section("🧰 Servizi Attivi", get_active_services())
        self.add_section("👥 Utenti Connessi", get_logged_users())
        self.add_section("🌐 Porte Aperte", get_open_ports())
        self.add_section("📁 Modifiche Recenti in /etc", get_recent_etc_modifications())
        self.output(self.filename)
