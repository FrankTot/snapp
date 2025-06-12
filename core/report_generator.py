from fpdf import FPDF
from datetime import datetime
import os
from .system_snapshot import (
    get_active_services,
    get_logged_users,
    get_open_ports,
    get_recent_etc_modifications
)

class PDFReport(FPDF):
    def __init__(self, filename=None):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

        # ✅ Aggiunge il font DejaVu (supporto Unicode completo)
        font_path = "assets/DejaVuSans.ttf"
        self.add_font("DejaVu", "", font_path, uni=True)
        self.add_font("DejaVu", "B", font_path, uni=True)
        self.set_font("DejaVu", "", 12)

        self.add_page()
        self._add_header()

        self.filename = filename or f"reports/report_{self._timestamp()}.pdf"

    def _timestamp(self):
        return datetime.now().strftime("%d-%m-%Y__%H-%M-%S")

    def _add_header(self):
        self.set_font("DejaVu", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "📋 SnapAudit Report", 0, 1, 'C')
        self.ln(10)

    def add_section(self, title, content):
        if isinstance(content, list):
            if content and isinstance(content[0], dict):
                content = self._format_dict_list(content)
            else:
                content = "\n".join(str(item) for item in content)

        self.set_font("DejaVu", "B", 14)
        self.set_text_color(40, 90, 160)
        self.cell(0, 10, f"🛡 {title}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.set_font("DejaVu", "", 11)
        self.multi_cell(0, 8, content)
        self.ln()

    def _format_dict_list(self, dict_list):
        lines = []
        for d in dict_list:
            line = "\n".join([f"  - {k}: {v}" for k, v in d.items()])
            lines.append(line + "\n")
        return "\n".join(lines)

    def generate_full_report(self):
        self.add_section("Servizi Attivi", get_active_services())
        self.add_section("Utenti Loggati", get_logged_users())
        self.add_section("Porte Aperte", get_open_ports())
        self.add_section("Modifiche Recenti in /etc", get_recent_etc_modifications())
        self.output(self.filename)
