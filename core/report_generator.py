import os
from fpdf import FPDF
from datetime import datetime
from .system_snapshot import get_active_services, get_logged_users, get_open_ports, get_recent_etc_modifications

class PDFReport(FPDF):
    def __init__(self, filename=None):
        super().__init__()
        self.filename = filename or f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        self._add_header()
        self.set_font("DejaVu", "", 12)
        self.set_text_color(0, 0, 0)
        self.line_height = self.font_size * 2.5

    def _add_header(self):
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 50)
        self.set_font("DejaVu", "B", 20)
        self.set_text_color(0, 51, 102)
        self.cell(0, 40, "SnapAudit Report", ln=True, align="R")
        self.ln(10)

    def add_section(self, title, content):
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, f" {title}", ln=True, fill=True)
        self.ln(2)
        self.set_font("DejaVu", "", 12)
        self.set_text_color(0, 0, 0)
        if isinstance(content, list):
            # Make table style output
            self._draw_table(content)
        else:
            self.multi_cell(0, 8, content)
        self.ln(5)

    def _draw_table(self, data):
        if not data:
            self.cell(0, 8, "No data available", ln=True)
            return
        col_widths = []
        keys = list(data[0].keys())
        # Calculate col widths evenly but adapt to longest text
        for key in keys:
            max_len = max(len(str(row.get(key, ""))) for row in data)
            col_widths.append(max(30, min(60, max_len*6)))

        # Header row
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 12)
        for i, key in enumerate(keys):
            self.cell(col_widths[i], 10, key, border=1, fill=True)
        self.ln()

        # Data rows
        self.set_font("DejaVu", "", 11)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in data:
            for i, key in enumerate(keys):
                text = str(row.get(key, ""))
                self.cell(col_widths[i], 8, text, border=1, fill=fill)
            self.ln()
            fill = not fill

    def generate_full_report(self):
        # Gather data
        services = get_active_services()
        users = get_logged_users()
        ports = get_open_ports()
        etc_mods = get_recent_etc_modifications()

        self.add_section("Active Services", services)
        self.add_section("Logged Users", users)
        self.add_section("Open Ports", ports)
        self.add_section("Recent /etc Modifications", etc_mods)

        os.makedirs("reports", exist_ok=True)
        self.output(self.filename)
        return self.filename
