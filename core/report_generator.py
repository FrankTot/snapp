from fpdf import FPDF
from datetime import datetime
from .system_snapshot import get_active_services, get_logged_users, get_open_ports, get_recent_etc_modifications

class PDFReport(FPDF):
    def __init__(self, filename=None):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Helvetica", size=12)

        self.add_page()
        self._add_header()

        self.filename = filename or f"reports/report_{self._timestamp()}.pdf"

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _add_header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "SnapAudit Report", 0, 1, 'C')
        self.ln(10)

    def add_section(self, title, content):
        # Se content è lista, trasformala in stringa
        if isinstance(content, list):
            content = "\n".join(content)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, 0, 1)
        self.set_font("Helvetica", size=12)
        self.multi_cell(0, 8, content)
        self.ln()

    def generate_full_report(self):
        self.add_section("Active Services", get_active_services())
        self.add_section("Logged In Users", get_logged_users())
        self.add_section("Open Ports", get_open_ports())
        self.add_section("Recent /etc Modifications", get_recent_etc_modifications())

        self.output(self.filename)
