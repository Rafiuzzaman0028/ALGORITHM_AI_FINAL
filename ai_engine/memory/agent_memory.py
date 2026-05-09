class AgentMemory:
    """
    Simple in-memory storage for agent reasoning,
    tool outputs, and observations.
    """

    def __init__(self):
        self.thoughts = []
        self.actions = []
        self.observations = []

    def add_thought(self, thought):
        self.thoughts.append(thought)

    def add_action(self, action):
        self.actions.append(action)

    def add_observation(self, observation):
        self.observations.append(observation)

    def get_context(self):
        return {
            "thoughts": self.thoughts,
            "actions": self.actions,
            "observations": self.observations
        }

    def clear(self):
        self.thoughts = []
        self.actions = []
        self.observations = []