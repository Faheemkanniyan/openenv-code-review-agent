from typing import Dict, Any, Optional
from env.models import Observation, Action, RewardState, StepResponse
from env.bug_database import BugDatabase
from env.pr_generator import PRGenerator
from env.reward_engine import RewardEngine

class CodeReviewEnv:
    def __init__(self):
        self.bug_db = BugDatabase()
        self.pr_gen = PRGenerator(self.bug_db)
        self.steps_taken = 0
        self.max_steps = 10
        
        self.current_pr: Optional[Dict[str, Any]] = None
        self.reward_state: RewardState = RewardState()
        self.task_difficulty = "medium"

    def reset(self, task_difficulty: str = "medium") -> Observation:
        self.steps_taken = 0
        self.reward_state = RewardState()
        self.task_difficulty = task_difficulty
        
        self.current_pr = self.pr_gen.generate_pr(task_difficulty)
        
        return self._get_observation()

    def load_custom_code(self, code: str) -> Observation:
        self.steps_taken = 0
        self.reward_state = RewardState()
        self.task_difficulty = "custom"
        self.current_pr = {
            "pr_id": "custom-pr",
            "code": code,
            "status": "open",
            "metadata": {
                "id": "custom",
                "issue_keywords": ["bug", "error", "fix", "issue", "problem", "vulnerability"],
                "fix_keywords": ["fix", "update", "correct", "secure", "patch"]
            }
        }
        return self._get_observation()

    def step(self, action: Action) -> StepResponse:
        if self.current_pr is None:
            raise ValueError("Environment must be reset before calling step().")
            
        self.steps_taken += 1
        
        reward_step, self.reward_state = RewardEngine.compute_reward(
            action, 
            self.current_pr["metadata"], 
            self.reward_state
        )
        
        done = self.reward_state.pr_resolved or self.steps_taken >= self.max_steps
        
        if action.action_type in ["approve_pr", "reject_pr"]:
            self.current_pr["status"] = "approved" if action.action_type == "approve_pr" else "rejected"
            done = True
            
        info = {
            "score": self.reward_state.score,
            "steps": self.steps_taken
        }
        
        return StepResponse(
            state=self._get_observation(),
            reward=reward_step,
            done=done,
            info=info
        )

    def state(self) -> Observation:
        if self.current_pr is None:
            raise ValueError("Environment has no active state.")
        return self._get_observation()

    def _get_observation(self) -> Observation:
        return Observation(
            pr_id=self.current_pr["pr_id"],
            code=self.current_pr["code"],
            status=self.current_pr["status"],
            task_difficulty=self.task_difficulty
        )
