class AgentController:
    """
    Simple state-machine controller for AIEngine.
    It wraps the existing pipeline without breaking it.
    """

    def __init__(self, engine):
        self.engine = engine
        self.state = "ACT"
        self.context = {}

    def run(self, prompt):

        print("\n--- AGENT CONTROLLER START ---")

        while self.state != "FINISH":

            print(f"\n[STATE] {self.state}")

            if self.state == "ACT":

                # Run your existing AI pipeline
                result = self.engine.run_pipeline(prompt)

                self.context["result"] = result
                self.state = "VERIFY"

            elif self.state == "VERIFY":

                if self._verify():
                    print("\n--- TASK SUCCESS ---")
                    self.state = "FINISH"
                else:
                    print("\n--- RETRYING TASK ---")
                    self.state = "ACT"

        return self.context

    def _verify(self):

        result = self.context.get("result")

        if not result:
            return False

        if isinstance(result, dict) and result.get("status") == "success":
            return True

        return True