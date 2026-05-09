from ai_engine.core.ai_engine import AIEngine


def test_pdf_context():

    engine = AIEngine()

    prompt = "Summarize this pdf"

    result = engine.run(prompt, r"D:\Kenneth_AI\Manus_AI_API_Setup_Guide_for_Client.pdf")

    print(result)


if __name__ == "__main__":
    test_pdf_context()