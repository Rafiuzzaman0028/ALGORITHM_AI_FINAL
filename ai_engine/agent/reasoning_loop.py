class ReasoningLoop:

    def __init__(self, engine):
        self.engine = engine
        self.max_steps = 5

    def run(self, prompt):

        context = {
            "prompt": prompt,
            "memory": self.engine.memory.get_context(),
            "history": []
        }

        for step in range(self.max_steps):

            print(f"\n--- AGENT STEP {step+1} ---")

            thought = self.think(context)

            self.engine.memory.add_thought(thought)

            action = self.decide_action(thought)

            self.engine.memory.add_action(action)

            observation = self.execute(action)

            self.engine.memory.add_observation(observation)

            context["history"].append({
                "thought": thought,
                "action": action,
                "observation": observation
            })

            if self.is_task_complete(observation):
                return observation

        return observation

    def think(self, context):

        print("Agent thinking...")

        prompt = f"""
    You are an autonomous AI agent.

    User request:
    {context['prompt']}

    Previous actions:
    {context['history']}

    Decide the next step.

    Respond with one word:

    search
    code
    finish
    """

        # Use existing analyzer instead of provider
        result = self.engine.analyzer.analyze(prompt)

        return result



    def decide_action(self, thought):

        text = str(thought).lower()

        if "search" in text:
            return {"tool": "web_search"}

        if "code" in text:
            return {"tool": "python"}

        return {"tool": "none"}


    def execute(self, action):

        tool_name = action.get("tool")

        if tool_name == "none":
            return "No action needed"

        tool = self.engine.tools.get_tool(tool_name)
        if not tool:
            return "Tool not found"

        if tool_name == "web_search":
            return tool.search("latest AI development")

        if tool_name == "python":
            return tool.execute("print('test')")


    def is_task_complete(self, observation):

        if isinstance(observation, str) and "complete" in observation.lower():
            return True

        return False