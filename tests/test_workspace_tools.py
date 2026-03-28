from ai_engine.tools.workspace_tools import WorkspaceTools


def test_workspace_tools():

    tools = WorkspaceTools()

    print("\n--- LIST DIRECTORY ---")
    print(tools.list_directory())

    print("\n--- WRITE FILE ---")
    tools.write_file("test_file.txt", "Hello AI Agent")

    print("\n--- READ FILE ---")
    content = tools.read_file("test_file.txt")
    print(content)

    print("\n--- EDIT FILE ---")
    tools.edit_file("test_file.txt", "File edited by AI agent")

    print("\n--- READ FILE AGAIN ---")
    print(tools.read_file("test_file.txt"))

    print("\n--- TERMINAL COMMAND ---")
    print(tools.run_terminal("echo Workspace working"))


if __name__ == "__main__":
    test_workspace_tools()