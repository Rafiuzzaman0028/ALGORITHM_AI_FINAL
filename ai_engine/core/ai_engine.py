from dotenv import load_dotenv
load_dotenv()

from ai_engine.agent.agent_controller import AgentController
from ai_engine.agent.research_agent import ResearchAgent
from ai_engine.analyzer.task_analyzer import TaskAnalyzer
from ai_engine.router.ai_router import AIRouter
from ai_engine.core.execution_manager import ExecutionManager
from ai_engine.formatter.response_formatter import ResponseFormatter
from ai_engine.project_builder.project_generator import SmartProjectBuilder
from ai_engine.validator.project_validator import ProjectValidator
from ai_engine.repair.project_repairer import ProjectRepairer
from ai_engine.planner.architecture_planner import ArchitecturePlanner
from ai_engine.dependency.dependency_extractor import DependencyExtractor
from ai_engine.repair.ai_repair_agent import AIRepairAgent
from ai_engine.document_processing.pdf_reader import PDFReader
from ai_engine.document_processing.pdf_chunker import PDFChunker
from ai_engine.context.context_builder import ContextBuilder
from ai_engine.document_processing.pdf_generator import PDFGenerator
from ai_engine.document_processing.report_builder_v2 import ReportBuilderV2
from ai_engine.document_processing.pdf_generator import generate_pdf
from ai_engine.tools.init_tools import initialize_tools
from ai_engine.tools.tool_executor import ToolExecutor
from ai_engine.agent.action_executor import ActionExecutor
from ai_engine.agent.reasoning_loop import ReasoningLoop
from ai_engine.agent.tool_planner import ToolPlanner
from ai_engine.memory.agent_memory import AgentMemory
from ai_engine.tools.tool_registry import ToolRegistry
from ai_engine.agent.agent_loop_v2 import AgentLoopV2
from ai_engine.planner.task_graph_planner import TaskGraphPlanner
from ai_engine.planner.task_graph_executor import TaskGraphExecutor
from ai_engine.planner.project_architect import ProjectArchitect
from ai_engine.planner.project_initializer import ProjectInitializer
from ai_engine.providers.provider_factory import ProviderFactory

import re
import json


FRONTEND_ONLY_RULES = """
IMPORTANT FRONTEND-ONLY GENERATION RULES:

Generate only frontend code.

Do not generate:
- server folder
- backend folder
- api folder
- routes folder
- controllers folder
- models folder
- middleware folder
- Express server
- MongoDB/Mongoose code
- database connection code
- JWT/auth backend code
- bcrypt code
- API server code

Use mock/static data inside the frontend.

Do not use fetch or axios to call a backend API.

The generated project must run independently in browser preview without any backend server.

If using React:
- generate only frontend React files
- use local mock data arrays
- keep all app logic inside frontend files
- package.json should only contain frontend dependencies
"""


def clean_for_pdf(text):
    text = re.sub(
        r"```(?:python|bash|javascript|js|html|css|json|text|sh|py).*?```",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    text = re.sub(r"^\s*\S+/\S+\.\w+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\S+/\S+\.\w+", "", text)

    text = re.sub(r"```(markdown|md)?", "", text, flags=re.IGNORECASE)
    text = text.replace("`", "")

    return text.strip()


def clean_for_api(text):
    text = text.replace("\\n", "\n")
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = text.replace("###", "")
    text = text.replace("**", "")
    text = text.replace("|", " ")

    return text.strip()


class AIEngine:
    """
    Main AI Engine Controller.
    Runs the full AI pipeline.
    """

    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.router = AIRouter()
        self.executor = ExecutionManager()
        self.formatter = ResponseFormatter()
        self.builder = SmartProjectBuilder()
        self.pdf_reader = PDFReader()
        self.pdf_chunker = PDFChunker()
        self.context_builder = ContextBuilder()
        self.tools = initialize_tools()
        self.tool_executor = ToolExecutor(self.tools)
        self.research_agent = ResearchAgent()
        self.action_executor = ActionExecutor(self.tools)
        self.reasoning_loop = ReasoningLoop(self)
        self.tool_planner = ToolPlanner(self)
        self.memory = AgentMemory()
        self.tool_registry = ToolRegistry()
        self.agent_loop_v2 = AgentLoopV2(self)
        self.task_graph_planner = TaskGraphPlanner()
        self.task_graph_executor = TaskGraphExecutor(self)
        self.project_architect = ProjectArchitect()
        self.project_initializer = ProjectInitializer()

    def build_prompt_with_context(self, prompt, research_context):
        if not research_context:
            return prompt

        context_text = ""

        for item in research_context[:5]:
            title = item.get("title", "")
            content = item.get("content", "")
            context_text += f"\nSOURCE: {title}\n{content}\n"

        enhanced_prompt = f"""
Use the following research information to answer the user's request.

RESEARCH CONTEXT:
{context_text}

USER REQUEST:
{prompt}
"""

        return enhanced_prompt

    def is_image_generation_prompt(self, prompt):
        text = prompt.lower()

        action_words = [
            "generate",
            "create",
            "make",
            "draw",
            "design"
        ]

        image_words = [
            "image",
            "picture",
            "photo",
            "illustration",
            "cartoon",
            "poster",
            "logo",
            "avatar",
            "wallpaper"
        ]

        has_action = any(word in text for word in action_words)
        has_image_word = any(word in text for word in image_words)

        return has_action and has_image_word

    def handle_image_generation(self, prompt):
        gemini = ProviderFactory.get_provider("gemini")
        result = gemini.generate_image(prompt, output_dir="generated_projects")

        response = {
            "formatted_results": [
                {
                    "task_type": "image_generation",
                    "provider": "gemini",
                    "status": result.get("status"),
                    "output": result.get("output"),
                    "image_path": result.get("image_path"),
                    "tokens_used": result.get("tokens_used")
                }
            ],
            "image_path": result.get("image_path")
        }

        return response

    def should_apply_frontend_only_rules(self, prompt):
        text = prompt.lower()

        project_words = [
            "website",
            "web app",
            "webapp",
            "app",
            "frontend",
            "react",
            "portfolio",
            "dashboard",
            "landing page",
            "ecommerce",
            "e-commerce"
        ]

        backend_words = [
            "backend only",
            "api only",
            "server only",
            "express api",
            "fastapi",
            "database api"
        ]

        if any(word in text for word in backend_words):
            return False

        return any(word in text for word in project_words)

    def apply_frontend_only_rules(self, enhanced_prompt, original_prompt):
        if self.should_apply_frontend_only_rules(original_prompt):
            return f"""
{enhanced_prompt}

{FRONTEND_ONLY_RULES}
"""
        return enhanced_prompt

    def run_pipeline(self, prompt, pdf_path=None):
        if self.is_image_generation_prompt(prompt):
            print("\n--- GEMINI IMAGE GENERATION ---\n")
            return self.handle_image_generation(prompt)

        pdf_context = None

        if pdf_path:
            print("\n--- STEP 0: PDF PROCESSING ---\n")

            reader = PDFReader()
            text = reader.extract_text(pdf_path)

            chunker = PDFChunker()
            chunks = chunker.chunk_text(text)

            pdf_context = chunks[0]

            print("PDF context extracted.")

        builder = ContextBuilder()
        prompt = builder.build_context(prompt, pdf_context)

        print("\n--- AGENT REASONING LOOP ---\n")

        agent_result = self.reasoning_loop.run(prompt)

        plan = self.tool_planner.create_plan(prompt)

        print("Generated Plan:")
        print(plan)

        for step in plan:
            tool_name = step.get("tool")
            tool = self.tools.get_tool(tool_name)

            if not tool:
                continue

            print(f"\nExecuting tool: {tool_name}")

            if tool_name == "web_search":
                result = tool.search(prompt)
            elif tool_name == "python":
                result = tool.execute("print('planner execution')")
            else:
                result = "unknown tool"

            print("Tool result:", result)

        print("Agent reasoning result:")
        print(agent_result)

        print("\n--- AVAILABLE TOOLS ---\n")
        print(self.tools.list_tools())

        print("\n--- TOOL TEST ---")

        result = self.tool_executor.execute_tool(
            "web_search",
            "AI impact on software development"
        )

        print(result)

        print("\n--- STEP 0.5: WEB RESEARCH ---\n")

        research_context = self.research_agent.research(prompt)

        enhanced_prompt = prompt

        if research_context:
            context_text = ""

            for item in research_context[:5]:
                title = item.get("title", "")
                content = item.get("content", "")
                context_text += f"\nSOURCE: {title}\n{content}\n"

            enhanced_prompt = f"""
Use the following research information when answering.

RESEARCH CONTEXT:
{context_text}

USER REQUEST:
{prompt}
"""

        enhanced_prompt = self.apply_frontend_only_rules(
            enhanced_prompt=enhanced_prompt,
            original_prompt=prompt
        )

        print("\n--- FRONTEND-ONLY PROMPT CHECK ---\n")
        print("Frontend-only rules applied:", self.should_apply_frontend_only_rules(prompt))

        print("\n--- STEP 1: TASK ANALYSIS ---\n")

        analyzer_result = self.analyzer.analyze(enhanced_prompt)
        print(analyzer_result)

        is_pdf_intent = False
        is_project_intent = False

        try:
            if isinstance(analyzer_result, dict) and "output" in analyzer_result:
                raw_output = analyzer_result["output"]

                if raw_output.startswith("```json"):
                    raw_output = raw_output.strip()[7:-3].strip()
                elif raw_output.startswith("```"):
                    raw_output = raw_output.strip()[3:-3].strip()

                output_data = json.loads(raw_output)

                for task in output_data.get("tasks", []):
                    t_type = task.get("task_type", "")

                    if t_type in ["research", "document", "slides"]:
                        is_pdf_intent = True

                    if t_type in ["website", "web_app", "automation", "design", "app", "python"]:
                        is_project_intent = True

        except Exception as e:
            print("Error parsing intent:", e)
            is_pdf_intent = "pdf" in enhanced_prompt.lower()
            is_project_intent = True

        print("\n--- STEP 1.5: ARCHITECTURE PLANNING ---\n")

        planner = ArchitecturePlanner()
        architecture = planner.plan(analyzer_result)

        print(architecture)

        print("\n--- STEP 2: BUILD EXECUTION PLAN ---\n")

        execution_plan = self.router.build_execution_plan(analyzer_result)
        print(execution_plan)

        print("\n--- STEP 3: EXECUTE TASKS ---\n")

        execution_context = {
            "prompt": enhanced_prompt,
            "architecture": architecture
        }

        execution_results = self.executor.execute(execution_plan, architecture)

        print(execution_results)

        print("\n--- STEP 4: FORMAT RESULTS ---\n")

        formatted_results = self.formatter.format_results(execution_results)
        print(formatted_results)

        print("\n--- STEP 4.5: PDF EXPORT CHECK ---\n")

        if is_pdf_intent:
            results_list = formatted_results.get("formatted_results", [])
            valid_texts = []

            for result in results_list:
                if result.get("task_type") in ["research", "document", "slides"] and result.get("status") == "success":
                    out_text = result.get("output", "").strip()

                    if out_text and not out_text.startswith("path/to/"):
                        valid_texts.append(out_text)

            if not valid_texts:
                for result in results_list:
                    if result.get("status") == "success" and result.get("task_type") not in [
                        "automation",
                        "web_app",
                        "website",
                        "design",
                        "app",
                        "python"
                    ]:
                        out_text = result.get("output", "").strip()

                        if out_text and not out_text.startswith("path/to/"):
                            valid_texts.append(out_text)
                            break

            research_output = "\n\n".join(valid_texts)

            if research_output and len(research_output) > 50:
                builder = ReportBuilderV2()

                report_text = builder.build_report(
                    "AI Generated Report",
                    research_output
                )

                clean_text = clean_for_pdf(report_text)
                pdf_path = generate_pdf(clean_text)

                print("PDF generated:", pdf_path)

                formatted_results["pdf_path"] = pdf_path

        print("\n--- STEP 5: BUILD PROJECT ---\n")

        if not is_project_intent:
            print("No project intent detected, skipping project build.")

            for r in formatted_results.get("formatted_results", []):
                if "output" in r:
                    r["output"] = clean_for_api(r["output"])

            return formatted_results

        project = self.builder.generate_project(formatted_results)

        if "project_path" not in project:
            print("\n--- NO PROJECT GENERATED ---\n")
            print(project)
            return project

        extractor = DependencyExtractor()
        extractor.generate_requirements(project["project_path"])

        validator = ProjectValidator(project["project_path"])
        validation_result = validator.validate()

        print("\n--- PROJECT VALIDATION ---\n")
        print(validation_result)

        from ai_engine.repair.runtime_tester import RuntimeTester

        tester = RuntimeTester()
        repair_agent = AIRepairAgent()

        MAX_REPAIR_ATTEMPTS = 3
        attempt = 0
        runtime_result = {"status": "skipped"}

        while attempt < MAX_REPAIR_ATTEMPTS:
            runtime_result = tester.run_python_project(project["project_path"])

            print(f"\n--- RUNTIME TEST ATTEMPT {attempt + 1} ---\n")
            print(runtime_result)

            if runtime_result["status"] == "success":
                print("\n--- RUNTIME SUCCESS ---\n")
                break

            print("\n--- RUNTIME ERROR DETECTED ---\n")

            repair_result = repair_agent.repair_runtime_error(
                project["project_path"],
                runtime_result.get("error")
            )

            print("\n--- AI REPAIR RESULT ---\n")
            print(repair_result)

            attempt += 1

        if runtime_result.get("status") != "success":
            print("\n--- MAX REPAIR ATTEMPTS REACHED OR RUNTIME SKIPPED ---\n")

        print("\n--- RUNTIME TEST ---\n")
        print(runtime_result)

        if validation_result["status"] == "failed":
            repairer = ProjectRepairer()
            repairer.repair(project["project_path"], validation_result["issues"])

            print("\n--- REVALIDATING PROJECT ---\n")

            validation_result = validator.validate()

            print(validation_result)

        print(project)

        formatted_results["project_path"] = project.get("project_path")
        formatted_results["zip_path"] = project.get("zip_path")

        return formatted_results

    def run(self, prompt, pdf_path=None):
        print("\n=== AGENT CONTROLLER START ===\n")

        controller = AgentController(self)

        result = controller.run(prompt)

        self.memory.clear()

        return result