class TaskGraphExecutor:
    """
    Executes tasks in dependency order.
    """

    def __init__(self, engine):
        self.engine = engine

    def execute(self, graph):

        completed = set()
        tasks = graph.get("tasks", [])

        results = []

        while len(completed) < len(tasks):

            for task in tasks:

                task_id = task["id"]

                if task_id in completed:
                    continue

                deps = task.get("depends_on", [])

                if all(d in completed for d in deps):

                    print(f"\n--- EXECUTING TASK {task_id} ---")
                    print(task["task"])

                    task_prompt = f"""
Main Goal:
{graph.get("goal")}

Current Task:
{task["task"]}

Complete this task as part of the main goal.
"""

                    result = self.engine.agent_loop_v2.run(task_prompt)

                    print("\nRESULT:", result)

                    results.append(result)

                    completed.add(task_id)

        print("\nTask graph execution complete")

        return results