from typing import Dict, Any, Tuple
from models import Action, RewardState
from graders import Grader

class RewardEngine:
    @staticmethod
    def compute_reward(action: Action, metadata: Dict[str, Any], state: RewardState) -> Tuple[float, RewardState]:
        reward = 0.0
        
        if action.action_type == "detect_issue":
            if not state.detected_issue:
                correct = Grader.evaluate_issue_detection(action.description or "", metadata)
                if correct:
                    reward = 0.4
                    state.detected_issue = True
                else:
                    reward = -0.1
        
        elif action.action_type == "suggest_fix":
            # Encourage detecting issue before fixing
            if not state.suggested_fix:
                correct = Grader.evaluate_fix_suggestion(action.description or "", metadata)
                if correct:
                    reward = 0.3
                    state.suggested_fix = True
                else:
                    reward = -0.1
                    
        elif action.action_type == "approve_pr":
            if not state.pr_resolved:
                should_approve = Grader.should_approve(metadata)
                if should_approve:
                    reward = 0.3
                else:
                    # Approved a buggy PR!
                    reward = -0.3
                state.pr_resolved = True
                
        elif action.action_type == "reject_pr":
            if not state.pr_resolved:
                should_approve = Grader.should_approve(metadata)
                if not should_approve:
                    # Correctly rejected a buggy PR
                    reward = 0.3
                else:
                    reward = -0.1
                state.pr_resolved = True

        state.score += reward
        # Clamp score between 0.0 and 1.0
        state.score = max(0.0, min(1.0, state.score))
        
        return reward, state
