from core.report_generator import PDFReport

def generate_pdf(self):
    title = self.title_input.text() or "Audit Report"
    pdf = PDFReport(title=title)
    pdf.generate_full_report()
    output_path = "report.pdf"
    pdf.output(output_path)
    # apri il pdf con visualizzatore di sistema
    import subprocess
    subprocess.Popen(['xdg-open', output_path])
