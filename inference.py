import os
import requests
import json
from openai import OpenAI

class InferenceAgent:
    def __init__(self, api_url: str = "http://localhost:7860", model: str = "gpt-4o-mini"):
        self.api_url = api_url
        self.model = model
        # Use a dummy key if not set, for local mocking/testing purposes
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy_key_for_testing"))

    def run_episode(self, task_difficulty: str = "medium"):
        print(f"[START] task=detect_bug env=code-review model={self.model}")
        
        # 1. Reset Env
        resp = requests.post(f"{self.api_url}/reset", json={"task_id": task_difficulty})
        if resp.status_code != 200:
            print("Failed to reset environment:", resp.text)
            return

        obs = resp.json()
        done = False
        step = 0
        total_rewards = []
        score = 0.0

        while not done and step < 10:
            step += 1
            
            # 2. Select Action via LLM Mock/Actual
            # We construct a prompt matching the PR
            prompt = f"PR Code:\n{obs.get('code')}\nReview status: {obs.get('status')}.\nWhat action should I take next? Reply strictly with JSON: {{\"action_type\": \"detect_issue|suggest_fix|approve_pr|reject_pr\", \"description\": \"...\"}}"
            
            # In a real run without dummy keys, you'll call standard completions.
            # Here we simulate the LLM to avoid test blocks if no keys are found.
            # (If a real key exists, we could use self.client.chat.completions.create)
            try:
                if os.environ.get("OPENAI_API_KEY"):
                    llm_resp = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    action_data = json.loads(llm_resp.choices[0].message.content)
                else:
                    # Mock logic for tests
                    action_data = {"action_type": "reject_pr", "description": "This is a dummy test"}
            except Exception as e:
                action_data = {"action_type": "reject_pr", "description": str(e)}

            action = {
                "action_type": action_data.get("action_type", "reject_pr"),
                "description": action_data.get("description", "")
            }

            # 3. Take step
            step_resp = requests.post(f"{self.api_url}/step", json=action)
            if step_resp.status_code != 200:
                print(f"[STEP] step={step} action={action['action_type']} reward=0.0 done=false error=\"{step_resp.text}\"")
                break
                
            data = step_resp.json()
            obs = data["observation"]
            reward = data["reward"]
            done = data["done"]
            info = data["info"]
            
            score = info.get("score", 0.0)
            total_rewards.append(str(reward))
            
            print(f"[STEP] step={step} action={action['action_type']} reward={reward:.2f} done={str(done).lower()} error=null")

        # 4. End of episode
        success = str(score >= 0.7).lower()  # Define basic success threshold
        rewards_str = ",".join(total_rewards)
        print(f"[END] success={success} steps={step} score={score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    agent = InferenceAgent()
    agent.run_episode("medium")
