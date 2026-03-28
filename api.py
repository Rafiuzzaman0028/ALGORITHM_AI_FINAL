from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine.core.ai_engine import AIEngine

app = FastAPI(
    title="Algorithm AI Engine API",
    description="API for accessing the AI Engine directly.",
    version="1.0.0"
)

# Initialize the AI Engine once when the server starts
engine = AIEngine()

class GenerateRequest(BaseModel):
    prompt: str

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

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the server from the D:\project_kenneth\Kenneth_AI folder
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["generated_projects"])
