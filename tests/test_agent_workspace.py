from ai_engine.core.ai_engine import AIEngine

engine = AIEngine()

result = engine.agent_loop_v2.run(
    "List files in the current directory and show their names."
)

print(result)