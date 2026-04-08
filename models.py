from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Observation(BaseModel):
    pr_id: str
    code: str
    status: str = "open"  # open, approved, rejected
    feedback: Optional[str] = None
    task_difficulty: str

class Action(BaseModel):
    action_type: str = Field(..., description="Must be one of: detect_issue, suggest_fix, approve_pr, reject_pr")
    description: Optional[str] = Field(None, description="Detailed explanation of the issue or fix.")

class RewardState(BaseModel):
    score: float = 0.0
    detected_issue: bool = False
    suggested_fix: bool = False
    pr_resolved: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
