from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF

class PDFGenerator:

    def generate_pdf(self, text, output_path):

        c = canvas.Canvas(output_path, pagesize=letter)

        y = 750

        for line in text.split("\n"):

            c.drawString(50, y, line)

            y -= 20

            if y < 50:
                c.showPage()
                y = 750

        c.save()

        return output_path

    
    


def generate_pdf(text, output_path="generated_projects/generated_report.pdf"):

    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)

    import re
    import textwrap

    # Ensure escaped newlines are converted to actual newlines
    text = text.replace("\\n", "\n")

    # Clean unicode (fpdf only supports latin-1 natively)
    text = text.encode("latin-1", "replace").decode("latin-1")

    # Break insanely long words (like URLs) so FPDF can wrap them. We break at 80 chars.
    text = re.sub(r'(\S{80,})', lambda m: ' '.join(textwrap.wrap(m.group(0), 80)), text)

    try:
        # Output text using FPDF's native multi_cell wrapper. w=0 extends to right margin.
        pdf.multi_cell(0, 5, text)
    except Exception as e:
        pdf.multi_cell(0, 5, f"[PDF FORMATTING ERROR]: {e}")

    pdf.output(output_path)

    return output_path