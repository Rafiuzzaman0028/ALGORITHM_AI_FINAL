from ai_engine.providers.provider_factory import ProviderFactory
from ai_engine.memory.agent_memory import AgentMemory
from ai_engine.workspace.workspace_scanner import WorkspaceScanner
from ai_engine.tools.tool_validator import ToolValidator

class AgentLoopV2:
    """
    Autonomous reasoning loop for the AI agent.

    Uses the ReAct pattern:
    Thought → Plan → Action → Observation → Repeat
    """

    def __init__(self, engine):
        self.engine = engine
        self.memory = AgentMemory()
        self.max_steps = 30


        # default reasoning model
        self.provider = ProviderFactory.get_provider("gemini")
        self.validator = ToolValidator()
        self.phase = "PLANNING" # Initial phase

    def run(self, goal):

        history = []

        for step in range(self.max_steps):

            print(f"\n--- AGENT STEP {step+1} ---")

            prompt = self.build_prompt(goal, history)

            response = self.provider.generate_response(prompt)

            output = response.get("output", "")


            print("\nAGENT RESPONSE:\n", output.encode("utf-8", "ignore").decode("utf-8"))

            parsed = self.parse_agent_output(output)

            thought = parsed.get("thought", "")
            action = parsed.get("action")
            action_input = parsed.get("input")

            # store thought
            self.memory.add_thought(thought)

            # store action
            self.memory.add_action(action)

            if action == "finish":
                result = parsed.get("final_answer", "Task completed")
                self.memory.clear()
                return result

            observation = self.execute_action(action, action_input)
            
            self.memory.add_observation(observation)

            history.append({
                "action": action,
                "input": action_input,
                "observation": observation
            })

        return "Max steps reached."

    def build_prompt(self, goal, history):
        # workspace context
        scanner = WorkspaceScanner()
        workspace_files = scanner.scan()
        tools = self.engine.tools.list_tools()
        memory_context = self.memory.get_context()

        # Phase-specific instructions
        phase_guidance = {
            "PLANNING": "Analyze the user requirement and decide WHICH TEMPLATE to use (e.g., website_basic, api_basic). Create a task list.",
            "GENERATION": "Focus on using 'write_file' to populate the selected template. Do NOT create redundant folders.",
            "VALIDATION": "Check if all required files are created and match the template structure.",
            "COMPLETION": "The task is complete. Wrap up and provide the final summary."
        }

        # Dynamic phase detection (simple logic for now)
        if "write_file" in str([h.get("action") for h in history]):
            self.phase = "GENERATION"

        return f"""
You are an autonomous AI software engineer.
Current Phase: {self.phase}

Phase Goal: {phase_guidance.get(self.phase)}

Your goal:
{goal}

Workspace files (Relative to Project Root):
{workspace_files}

Previous steps:
{history}

Agent Memory:

Thoughts:
{memory_context['thoughts']}

Available tools:
{tools}

STRICT RULES:
1. NEVER include 'active_project/' or 'generated_projects/' in your file paths.
2. Use paths like 'frontend/index.html' or 'server.js'.
3. Follow the ReAct format: THOUGHT, PLAN, ACTION, INPUT.

Respond EXACTLY in this format:

THOUGHT: reasoning
PLAN: short plan
ACTION: tool_name
INPUT: tool_input

If the task is complete:

ACTION: finish
FINAL: result
"""

    def parse_agent_output(self, text):

        result = {}
        current_key = None

        for line in text.splitlines():

            if line.startswith("THOUGHT:"):
                current_key = "thought"
                result["thought"] = line.replace("THOUGHT:", "").strip()

            elif line.startswith("ACTION:"):
                current_key = "action"
                result["action"] = line.replace("ACTION:", "").strip()

            elif line.startswith("INPUT:"):
                current_key = "input"
                result["input"] = line.replace("INPUT:", "").strip()

            elif line.startswith("FINAL:"):
                current_key = "final_answer"
                result["final_answer"] = line.replace("FINAL:", "").strip()
            
            elif current_key:
                result[current_key] += "\n" + line

        return result


    def execute_action(self, tool_name, tool_input):

        # validate tool input first
        valid, message = self.validator.validate(tool_name, tool_input)

        if not valid:
            return f"Tool validation error: {message}"

        tool = self.engine.tools.get_tool(tool_name)

        if not tool:
            return f"Tool '{tool_name}' not found"

        try:

            if tool_name == "web_search":
                return tool.search(tool_input)

            if tool_name == "python":
                return tool.execute(tool_input)

            if callable(tool):
                return tool(tool_input)

            return str(tool)

        except Exception as e:
            return f"Tool execution error: {str(e)}"