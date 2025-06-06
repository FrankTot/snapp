import os
from fpdf import FPDF
from datetime import datetime
from .system_snapshot import get_active_services, get_logged_in_users, get_open_ports, get_recent_etc_changes

class PDFReport:
    def __init__(self, title="Audit Report"):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.title = title
        self._add_header()
        self._add_title()
        self._add_date()

    def _add_header(self):
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            self.pdf.image(logo_path, 10, 8, 33)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "SnapAudit Report", 0, 1, "R")
        self.pdf.ln(20)

    def _add_title(self):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, self.title, 0, 1, "C")
        self.pdf.ln(10)

    def _add_date(self):
        self.pdf.set_font("Arial", "", 12)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pdf.cell(0, 10, f"Generated on: {date_str}", 0, 1, "C")
        self.pdf.ln(10)

    def add_section(self, header, content):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, header, 0, 1)
        self.pdf.set_font("Arial", "", 11)
        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln(8)

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_in_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent Changes in /etc (last 24h)", get_recent_etc_changes())

    def output(self, filename):
        self.pdf.output(filename)
