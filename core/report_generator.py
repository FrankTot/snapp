from fpdf import FPDF
from datetime import datetime
import os

class PDFReport:
    def __init__(self, title="SnapAudit Report", output_path="reports/report.pdf"):
        self.title = title
        self.output_path = output_path
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self._add_header()

    def _add_header(self):
        if os.path.exists("assets/logo.png"):
            self.pdf.image("assets/logo.png", 10, 8, 33)
        self.pdf.set_font("Helvetica", 'B', 16)
        self.pdf.cell(0, 10, self.title, ln=True, align="C")
        self.pdf.set_font("Helvetica", '', 12)
        self.pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.pdf.ln(10)

    def add_section(self, title, content):
        self.pdf.set_font("Helvetica", 'B', 14)
        self.pdf.set_text_color(30, 30, 30)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("Helvetica", '', 12)
        self.pdf.set_text_color(80, 80, 80)
        self.pdf.multi_cell(0, 10, content)
        self.pdf.ln(5)

    def save(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.pdf.output(self.output_path)
        return self.output_path
