from ai_engine.analyzer.task_analyzer import TaskAnalyzer
from ai_engine.router.ai_router import AIRouter


def test_router():

    prompt = "Build a startup website and prepare investor slides"

    analyzer = TaskAnalyzer()
    router = AIRouter()

    analyzer_result = analyzer.analyze(prompt)

    print("\n--- ANALYZER RESULT ---\n")
    print(analyzer_result)

    execution_plan = router.build_execution_plan(analyzer_result)

    print("\n--- ROUTER EXECUTION PLAN ---\n")
    print(execution_plan)


if __name__ == "__main__":
    test_router()