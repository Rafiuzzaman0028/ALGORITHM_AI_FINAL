# from ai_engine.core.ai_engine import AIEngine

# engine = AIEngine()

# goal = "Build a travel website and create slides explaining the business"

# graph = engine.task_graph_planner.create_graph(goal)

# print("\nTASK GRAPH:")
# print(graph)

# result = engine.task_graph_executor.execute(graph)

# print(result)

import sys
sys.stdout.reconfigure(encoding="utf-8")
from ai_engine.core.ai_engine import AIEngine

engine = AIEngine()

goal = "Build a travel website and create slides explaining the business"

# Create project structure
structure = engine.project_architect.generate_structure(goal)

project_path = engine.project_initializer.create_project(structure)

print("Project initialized at:", project_path)

# Continue with planning
graph = engine.task_graph_planner.create_graph(goal)

print("\nTASK GRAPH:")
print(graph)

result = engine.task_graph_executor.execute(graph)

print(result)