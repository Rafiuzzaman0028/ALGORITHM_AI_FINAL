from ai_engine.core.ai_engine import AIEngine


def test_pdf_export():

    engine = AIEngine()

#    prompt = "Generate a short business report in PDF"

    # prompt = """
    # Research the latest impact of AI on software development.

    # 1. Use web search to collect recent information.
    # 2. Analyze the findings.
    # 3. Generate a short professional business report.
    # 4. Export the report as a PDF document.

    # Return the implementation as a Python project.
    # """

    # prompt = """
    # Create a professional business report about the impact of AI on software development.

    # Steps:
    # 1. Search the web for recent statistics and trends.
    # 2. Analyze the findings.
    # 3. Generate a Python script that creates a PDF report.
    # 4. The report should contain:
    # - Executive Summary
    # - Key Metrics
    # - Business Insights
    # - Recommendations
    # 5. Export the final report as a PDF file.
    # """

    prompt = """
    Research the latest statistics about AI impact on software development,
    summarize the findings, and generate a professional business report in PDF format.

    The report must include:
    1. Executive summary
    2. Key statistics from recent sources
    3. Business insights
    4. Recommendations

    Use web search to gather information before generating the report.
    """

    result = engine.run(prompt)

    print(result)


if __name__ == "__main__":
    test_pdf_export()