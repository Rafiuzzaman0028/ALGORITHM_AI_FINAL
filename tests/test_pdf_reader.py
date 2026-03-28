from ai_engine.document_processing.pdf_reader import PDFReader


def test_pdf():

    reader = PDFReader()

    text = reader.extract_text(r"D:\Kenneth_AI\Manus_AI_API_Setup_Guide_for_Client.pdf")

    print(text[:1000])


if __name__ == "__main__":
    test_pdf()