from pypdf import PdfReader


class PDFReader:

    def extract_text(self, pdf_path):
        """
        Extract text from a PDF document
        """

        reader = PdfReader(pdf_path)
        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)