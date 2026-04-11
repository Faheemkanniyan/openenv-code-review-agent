import pytest
from fastapi.testclient import TestClient
from app import app
from models import Action

client = TestClient(app)

def test_reset_environment():
    response = client.post("/reset", json={"task_id": "easy"})
    assert response.status_code == 200
    data = response.json()
    assert "pr_id" in data
    assert "code" in data
    assert data["status"] == "open"
    assert data["task_difficulty"] == "easy"

def test_step_environment_bounds():
    # Reset first
    client.post("/reset", json={"task_id": "easy"})
    
    # Try a step
    action = {"action_type": "reject_pr", "description": "Rejecting bad code."}
    response = client.post("/step", json=action)
    assert response.status_code == 200
    
    data = response.json()
    assert "state" in data
    assert "reward" in data
    assert "done" in data
    assert "info" in data
    
    assert data["done"] is True
    assert 0.0 <= data["info"]["score"] <= 1.0

def test_get_state():
    client.post("/reset", json={"task_id": "medium"})
    response = client.get("/state")
    assert response.status_code == 200
    data = response.json()
    assert data["task_difficulty"] == "medium"
