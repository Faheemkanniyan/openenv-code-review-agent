# OpenEnv Code Review Simulation

A fully compliant Meta OpenEnv Hub environment simulating an AI code review task. The environment challenges the agent to review Pull Requests, detect bugs, suggest fixes, and accurately approve or reject changes.

## Environment Details
This repository conforms to the OpenEnv specification and runs as a standalone API natively executable locally or in HuggingFace Spaces.

### Action Space
- `action_type`: string - One of `["detect_issue", "suggest_fix", "approve_pr", "reject_pr"]`
- `description`: string - Optional reasoning

### Observation Space
- `pr_id`: string - Unique identifier for the simulated PR
- `code`: string - The buggy (or clean) code snippet
- `status`: string - Open, Approved, or Rejected

### Tasks
- `easy`: Basic syntax/logic errors.
- `medium`: Security/performance single-file issues.
- `hard`: Deep architectural vulnerabilities and concurrency.

## Getting Started

### Local Setup
1. `pip install -r requirements.txt`
2. Run Server: `python -m server.app`
3. Optional UI: Open `http://localhost:7860/ui` in a browser.

### Using the Baseline Agent
1. Set API Key (optional for testing format): `export OPENAI_API_KEY="..."`
2. Run inference: `python inference.py`

### Testing
Run `python -m pytest tests/`

## HuggingFace Deployment
This repository includes a `Dockerfile` properly exposing the standard `7860` port. 
To deploy:
1. Create a HF Space (Docker template)
2. Push repository files
3. The Space will automatically expose the `/reset` and `/step` endpoints.
