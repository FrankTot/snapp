import os
from datetime import datetime
from fpdf import FPDF
from .system_snapshot import (
    get_active_services,
    get_logged_in_users,
    get_open_ports,
    get_recent_etc_modifications
)

class PDFReport:
    def __init__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.title = f"Audit Report - {now}"
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", "B", 16)
        self._add_header()

    def _add_header(self):
        if os.path.exists("assets/logo.png"):
            self.pdf.image("assets/logo.png", 10, 8, 33)
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(80)
        self.pdf.cell(30, 10, self.title, 0, 0, "C")
        self.pdf.ln(20)

    def add_section(self, title, content):
        self.pdf.set_font("Helvetica", "B", 14)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("Helvetica", "", 12)

        # Rimuove caratteri non compatibili
        content = content.replace("→", "->")

        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln()

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_in_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent Changes in /etc", get_recent_etc_modifications())

    def output(self, filename):
        self.pdf.output(filename)
