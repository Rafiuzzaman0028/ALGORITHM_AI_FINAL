from ai_engine.core.ai_engine import AIEngine

engine = AIEngine()

result = engine.agent_loop_v2.run(
    "Find the latest news about artificial intelligence"
)

print(result)