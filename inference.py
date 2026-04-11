import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class InferenceAgent:
    def __init__(self, api_url: str = "http://127.0.0.1:7860"):
        self.api_url = api_url

    def run_validation_episode(self, task_difficulty: str = "medium"):
        print(f"[START] task=code_review env=code-review-agent model=baseline")
        
        # 1. Reset
        resp = requests.post(f"{self.api_url}/reset", json={"task_id": task_difficulty})
        if resp.status_code != 200:
            print(f"[ERROR] Failed to reset: {resp.text}")
            return
        
        obs = resp.json()
        done = False
        step = 0
        total_reward = 0.0
        
        # 2. Simple deterministic logic for validation
        actions = [
            {"action_type": "detect_issue", "description": "Detected a security vulnerability in the code."},
            {"action_type": "suggest_fix", "description": "Use parameterized queries to prevent SQL injection."},
            {"action_type": "reject_pr", "description": "Rejecting buggy code."}
        ]
        
        for action_data in actions:
            if done:
                break
                
            step += 1
            step_resp = requests.post(f"{self.api_url}/step", json=action_data)
            if step_resp.status_code != 200:
                print(f"[STEP] step={step} action={action_data['action_type']} reward=0.00 done=true error='{step_resp.text}'")
                break
                
            data = step_resp.json()
            reward = data["reward"]
            done = data["done"]
            total_reward += reward
            
            print(f"[STEP] step={step} action={action_data['action_type']} reward={reward:.2f} done={str(done).lower()} error=null")
        
        score = total_reward # Simplified for validation
        print(f"[END] success={str(score > 0).lower()} steps={step} score={score:.2f} rewards={total_reward:.2f}")

if __name__ == "__main__":
    # Check if server is up, else try to start or just run (assuming it's already running in Docker/HuggingFace)
    agent = InferenceAgent()
    agent.run_validation_episode("medium")
