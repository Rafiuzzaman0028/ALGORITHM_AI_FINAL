from ai_engine.document_processing.pdf_chunker import PDFChunker


def test_chunker():

    text = "A" * 5000

    chunker = PDFChunker()

    chunks = chunker.chunk_text(text)

    print("Chunks:", len(chunks))


if __name__ == "__main__":
    test_chunker()