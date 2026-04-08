from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Observation, Action, StepResponse
from code_review_env import CodeReviewEnv
import uvicorn
import gradio as gr
from ui.app import create_gradio_app

app = FastAPI(title="OpenEnv Code Review Agent API")
env = CodeReviewEnv()

class ResetRequest(BaseModel):
    task_id: str = "medium"

@app.post("/reset", response_model=Observation)
def reset_environment(req: ResetRequest):
    try:
        obs = env.reset(task_difficulty=req.task_id)
        return obs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step", response_model=StepResponse)
def step_environment(action: Action):
    try:
        response = env.step(action)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state", response_model=Observation)
def get_state():
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount Gradio app to FastAPI
gradio_app = create_gradio_app(env)
app = gr.mount_gradio_app(app, gradio_app, path="/ui")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
