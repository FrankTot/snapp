from fpdf import FPDF
from datetime import datetime
from .system_snapshot import get_active_services, get_logged_users, get_open_ports, get_recent_etc_modifications
import os

class PDFReport(FPDF):
    def __init__(self, filename=None):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Helvetica", size=12)

        if not os.path.exists("reports"):
            os.makedirs("reports")

        self.add_page()
        self._add_logo()
        self._add_header()

        self.filename = filename or f"reports/report_{self._timestamp()}.pdf"

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _add_logo(self):
        if os.path.exists("assets/logo.png"):
            self.image("assets/logo.png", x=10, y=8, w=30)
            self.ln(25)
        else:
            self.ln(10)

    def _add_header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(50, 50, 200)
        self.cell(0, 10, "SnapAudit Report", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 144, 255)
        self.cell(0, 10, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", size=12)

        if isinstance(content, list) and content and isinstance(content[0], dict):
            self._add_table(content)
        else:
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            self.multi_cell(0, 8, str(content))
        self.ln()

    def _add_table(self, data):
        keys = list(data[0].keys())
        col_width = self.epw / len(keys)

        # Header
        self.set_fill_color(100, 100, 255)
        self.set_text_color(255, 255, 255)
        for key in keys:
            self.cell(col_width, 8, key, border=1, fill=True, align='C')
        self.ln()

        # Rows
        self.set_text_color(0, 0, 0)
        fill = False
        for row in data:
            self.set_fill_color(240, 240, 240) if fill else self.set_fill_color(255, 255, 255)
            for key in keys:
                value = str(row.get(key, ''))
                # Ensure text fits in cell
                if len(value) > 30:
                    value = value[:27] + "..."
                self.cell(col_width, 8, value, border=1, fill=fill)
            self.ln()
            fill = not fill

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent /etc Modifications", get_recent_etc_modifications())
        self.output(self.filename)
