from ai_engine.analyzer.task_analyzer import TaskAnalyzer


def test_analyzer():

    prompt = "Build a travel website and create slides explaining the business"

    analyzer = TaskAnalyzer()

    result = analyzer.analyze(prompt)

    print("\n--- ANALYZER RESULT ---\n")
    print(result)


if __name__ == "__main__":
    test_analyzer()