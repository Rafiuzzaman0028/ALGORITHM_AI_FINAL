from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine.core.ai_engine import AIEngine
from ai_engine.preview.preview_agent import PreviewAgent
from pydantic import BaseModel
from typing import Optional



app = FastAPI(
    title="Algorithm AI Engine API",
    description="API for accessing the AI Engine directly.",
    version="1.0.0"
)

# Initialize the AI Engine once when the server starts
engine = AIEngine()
preview_agent = PreviewAgent()

class GenerateRequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default"


class StopPreviewRequest(BaseModel):
    project_path: Optional[str] = None
    port: Optional[int] = None

# In-memory storage for chat sessions
chat_sessions = {}

# Initialize a chat provider for the conversational endpoint
from ai_engine.providers.provider_factory import ProviderFactory
chat_provider = ProviderFactory.get_provider("openai")

@app.get("/")
def read_root():
    return {"status": "AI Engine Server is running. Visit /docs to test endpoints."}

@app.post("/api/generate")
def generate_project(req: GenerateRequest):
    """
    Takes a text prompt and generates a response, PDF, or Project based on intent.
    """
    print(f"\\n[FASTAPI] Received prompt: {req.prompt}\\n")
    
    try:
        # Run the AI engine pipeline
        result = engine.run(req.prompt)
        
        return {
            "status": "success",
            "message": "AI generation completed.",
            "data": result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


from pydantic import BaseModel

class PreviewRequest(BaseModel):
    project_path: str

@app.post("/api/preview")
def preview_project(req: PreviewRequest):
    return preview_agent.start_preview(req.project_path)


@app.post("/api/preview/stop")
def stop_preview(req: StopPreviewRequest):
    if not req.project_path and not req.port:
        return {
            "success": False,
            "error": "Please provide project_path or port"
        }

    return preview_agent.stop_preview(
        project_path=req.project_path,
        port=req.port
    )
import os
from pathlib import Path

@app.get("/api/debug-path")
def debug_path():
    return {
        "cwd": os.getcwd(),
        "exists_ai_engine": Path("ai_engine").exists(),
        "generated_projects": [
            str(p) for p in Path(".").rglob("nodejs_react_project")
        ]
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Fast, conversational endpoint that bypasses the heavy pipeline and maintains session history.
    """
    print(f"\\n[FASTAPI CHAT] Session: {req.session_id} | Prompt: {req.prompt}\\n")
    
    try:
        # Initialize session if not exists
        if req.session_id not in chat_sessions:
            chat_sessions[req.session_id] = [
                {"role": "system", "content": "You are a helpful AI assistant engaging in a conversation."}
            ]
            
        # Append user message
        chat_sessions[req.session_id].append({"role": "user", "content": req.prompt})
        
        # Get response
        result = chat_provider.generate_chat_response(chat_sessions[req.session_id])
        
        if result["status"] == "success":
            # Append assistant response to history
            chat_sessions[req.session_id].append({"role": "assistant", "content": result["output"]})
            
            return {
                "status": "success",
                "message": "Chat response generated.",
                "data": {
                    "response": result["output"],
                    "session_id": req.session_id
                }
            }
        else:
            raise Exception(result.get("output", "Unknown error from provider"))
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the server from the D:\project_kenneth\Kenneth_AI folder
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["generated_projects"])
