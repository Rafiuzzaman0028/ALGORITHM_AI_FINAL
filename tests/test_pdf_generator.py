from ai_engine.document_processing.pdf_generator import PDFGenerator


def test_pdf():

    generator = PDFGenerator()

    text = """
Kenneth AI Report

This PDF was generated automatically.

The system can export reports,
analysis, or documentation.
"""

    path = generator.generate_pdf(text, "test_report.pdf")

    print("PDF generated:", path)


if __name__ == "__main__":
    test_pdf()