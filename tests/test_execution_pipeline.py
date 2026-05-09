from ai_engine.analyzer.task_analyzer import TaskAnalyzer
from ai_engine.router.ai_router import AIRouter
from ai_engine.core.execution_manager import ExecutionManager


def test_execution_pipeline():

    prompt = "Build a travel website and create slides explaining the business"

    analyzer = TaskAnalyzer()
    router = AIRouter()
    executor = ExecutionManager()

    # Step 1 — Analyze prompt
    analyzer_result = analyzer.analyze(prompt)

    print("\n--- ANALYZER RESULT ---\n")
    print(analyzer_result)

    # Step 2 — Build execution plan
    execution_plan = router.build_execution_plan(analyzer_result)

    print("\n--- EXECUTION PLAN ---\n")
    print(execution_plan)

    # Step 3 — Execute tasks
    results = executor.execute(execution_plan)

    print("\n--- EXECUTION RESULTS ---\n")
    print(results)


if __name__ == "__main__":
    test_execution_pipeline()