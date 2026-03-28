# Kenneth AI Engine - API Documentation

Welcome to the **Kenneth AI Engine**. This project serves as an intelligent backend system capable of analyzing user prompts, planning software architecture, generating code, running automatic tests, performing self-repair on generated code, and returning complete deliverables such as functioning project directories or formatted PDF reports and queries result and so on.

## What Has Been Accomplished So Far
The project has evolved into a robust AI pipeline. Key milestones include:
- **Core AI Execution Loop:** An intelligent multi-step reasoning loop (`AgentController`) capable of task analysis, architecture planning, and tool execution.
- **Project Structure Generation:** Capable of generating multiple project types including Websites, Node.js servers, and Python applications.
- **Intelligent Project Validation:** A `ProjectValidator` that dynamically checks for entry points in various locations (e.g., root, `src/`, `app.py`, `main.py`).
- **Runtime Testing & Self-Repair:** A `RuntimeTester` that executes generated code in a secure subprocess. If it crashes, an `AIRepairAgent` reads the traceback errors and autonomously fixes the code up to 3 times.
- **PDF Generation Pipeline:** For research and document-heavy prompts, the engine gathers web research, formats the text, and compiles it into a downloadable PDF utilizing the `fpdf2` library.
- **FastAPI Server Integration:** A live server (`api.py`) configured with Uvicorn that safely runs the pipeline dynamically without getting stuck in auto-reload loops when new files are generated.

---

## Overall Output Scenario
When a client application interacts with the **Algorithm AI Engine**, the internal routing handles the intent:
1. **Web / Application Intent:** The engine will outline the architecture, generate the code files (e.g. `src/app.py`, `requirements.txt`), save them to the `generated_projects` directory, validate it, perform runtime startup tests, apply self-repairs if it fails, and finally return a `.zip` path.
2. **Research / Document Intent:** The engine will utilize its `ResearchAgent` to fetch relevant data from the web, synthesize it, generate a PDF report, and return the `pdf_path`.
3. **General Intent:** The engine defaults to answering the prompt generally using its reasoning loop and context builders.

---

## API Reference

### `POST /api/generate`
The primary endpoint to trigger the AI generation pipeline.

**Endpoint URL**
```
http://localhost:8000/api/generate
```

**Content-Type:** `application/json`

**Request Body Structure**
```json
{
  "prompt": "string"
}
```

---

## 3 Input Examples & Corresponding Outputs

### Example 1: Code Project Generation (Python App)
This example triggers the AI to build, validate, and runtime-test a Python application. 

**Request:**
```json
{
  "prompt": "Create a simple Python Flask API with two endpoints: a server status check and a random number generator."
}
```

**Expected Output (Abridged):**
```json
{
  "status": "success",
  "message": "AI generation completed.",
  "data": {
    "formatted_results": [
      {
        "task_type": "web_app",
        "status": "success",
        "output": "Code written correctly..."
      }
    ],
    "project_path": "D:\\project_kenneth\\project_kenneth\\Kenneth_AI\\generated_projects\\python_project",
    "zip_path": "D:\\project_kenneth\\project_kenneth\\Kenneth_AI\\generated_projects\\python_project.zip"
  }
}
```

---

### Example 2: PDF Research Report Generation
This example triggers the AI's research tools and PDF building framework.

**Request:**
```json
{
  "prompt": "Research the impact of AI and Automation on Software Development and write a comprehensive report."
}
```

**Expected Output (Abridged):**
```json
{
  "status": "success",
  "message": "AI generation completed.",
  "data": {
    "formatted_results": [
      {
        "task_type": "research",
        "status": "success",
        "output": "Extensive text regarding AI in software development..."
      }
    ],
    "pdf_path": "D:\\project_kenneth\\project_kenneth\\Kenneth_AI\\generated_projects\\generated_report.pdf"
  }
}
```

---

### Example 3: General Query / Question Answering
If the user intent doesn't strictly match a project or a pdf document, it returns contextualized responses directly.

**Request:**
```json
{
  "prompt": "What is the difference between 0.0.0.0 and 127.0.0.1?"
}
```

**Expected Output (Abridged):**
```json
{
  "status": "success",
  "message": "AI generation completed.",
  "data": {
    "formatted_results": [
      {
        "task_type": "general",
        "status": "success",
        "output": "0.0.0.0 is a routing address meaning 'listen on all available network interfaces', while 127.0.0.1 is specifically the loopback interface routing exclusively to your own machine."
      }
    ]
  }
}
```

---

## How to Run the API
To start the API development server locally:
```bash
python api.py
```
The application will launch on `http://0.0.0.0:8000`, making it accessible at `http://localhost:8000` or via your local network IP block.
