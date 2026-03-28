from ai_engine.analyzer.task_analyzer import TaskAnalyzer
from ai_engine.router.ai_router import AIRouter
from ai_engine.core.execution_manager import ExecutionManager
from ai_engine.formatter.response_formatter import ResponseFormatter
from ai_engine.project_builder.project_generator import SmartProjectBuilder


def test_project_builder():

    prompt = "Build a travel website with dynamic content"

    analyzer = TaskAnalyzer()
    router = AIRouter()
    executor = ExecutionManager()
    formatter = ResponseFormatter()
    generator = SmartProjectBuilder()

    analyzer_result = analyzer.analyze(prompt)

    execution_plan = router.build_execution_plan(analyzer_result)

    execution_results = executor.execute(execution_plan)

    formatted_results = formatter.format_results(execution_results)

    project = generator.generate_project(formatted_results)

    print("\n--- PROJECT GENERATED ---\n")
    print(project)


if __name__ == "__main__":
    test_project_builder()