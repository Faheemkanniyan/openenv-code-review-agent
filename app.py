from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
from models import Observation, Action, StepResponse
from code_review_env import CodeReviewEnv
import uvicorn
import os

app = FastAPI(title="OpenEnv Code Review Agent API")
env = CodeReviewEnv()

class ResetRequest(BaseModel):
    task_id: Optional[str] = None
    task_difficulty: Optional[str] = None

@app.get("/")
def health_check():
    return {"status": "ok", "message": "OpenEnv Code Review Agent is running"}

@app.post("/reset", response_model=Observation)
def reset_environment(req: Optional[ResetRequest] = None):
    try:
        # Accept task_id or task_difficulty for maximum compatibility
        difficulty = "medium"
        if req:
            difficulty = req.task_id or req.task_difficulty or "medium"
        
        obs = env.reset(task_difficulty=difficulty)
        return obs
    except Exception as e:
        print(f"ERROR in /reset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class CustomCodeRequest(BaseModel):
    code: str

@app.post("/load_custom", response_model=Observation)
def load_custom_code(req: CustomCodeRequest):
    try:
        obs = env.load_custom_code(req.code)
        return obs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step", response_model=StepResponse)
def step_environment(action: Action):
    try:
        print(f"DEBUG: step action={action.action_type}")
        response = env.step(action)
        return response
    except Exception as e:
        print(f"ERROR in /step: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state", response_model=Observation)
def get_state():
    try:
        return env.state()
    except Exception as e:
        print(f"ERROR in /state: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
