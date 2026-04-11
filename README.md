# OpenEnv Code Review Agent

A fully compliant OpenEnv environment simulating AI code review tasks.

## Project Structure
- `env/`: Environment logic and OpenEnv interface implementations.
- `server/`: FastAPI server exposing `/reset` and `/step` endpoints.
- `data/`: JSON database for simulated bugs.
- `inference.py`: Baseline agent and validation script.
- `Dockerfile`: Production deployment configuration.

## Features
- Compliant with OpenEnv Phase-1 validation.
- Standardized action/observation space.
- Multi-difficulty levels (easy, medium, hard).

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python -m server.app
```
Or via Docker:
```bash
docker build -t code-review-agent .
docker run -p 7860:7860 code-review-agent
```

### 3. Run Validation
```bash
python inference.py
```

## HuggingFace Deployment
Deployed as a Docker Space on port 7860.
Endpoints:
- `POST /reset`: Initialize new task.
- `POST /step`: Submit action.
- `GET /state`: Get current PR state.
