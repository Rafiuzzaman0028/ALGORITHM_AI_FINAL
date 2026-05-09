class PDFChunker:

    def chunk_text(self, text, chunk_size=1200):
        """
        Split long text into chunks
        """

        chunks = []

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])

        return chunks