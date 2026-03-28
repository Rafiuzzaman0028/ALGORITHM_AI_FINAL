from ai_engine.analyzer.task_analyzer import TaskAnalyzer
from ai_engine.router.ai_router import AIRouter
from ai_engine.core.execution_manager import ExecutionManager
from ai_engine.formatter.response_formatter import ResponseFormatter


def test_formatter_pipeline():

    prompt = "Build a travel website and create slides explaining the business"

    analyzer = TaskAnalyzer()
    router = AIRouter()
    executor = ExecutionManager()
    formatter = ResponseFormatter()

    analyzer_result = analyzer.analyze(prompt)

    execution_plan = router.build_execution_plan(analyzer_result)

    execution_results = executor.execute(execution_plan)

    formatted_results = formatter.format_results(execution_results)

    print("\n--- FORMATTED RESULTS ---\n")
    print(formatted_results)


if __name__ == "__main__":
    test_formatter_pipeline()