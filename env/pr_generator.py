import uuid
from typing import Dict, Any

class PRGenerator:
    def __init__(self, bug_db):
        self.bug_db = bug_db

    def generate_pr(self, difficulty: str) -> Dict[str, Any]:
        """Generates a PR object from a bug of the specified difficulty."""
        bug = self.bug_db.get_bug_by_difficulty(difficulty)
        if not bug:
            # Fallback if no bugs found
            return self._fallback_pr()

        pr_id = str(uuid.uuid4())[:8]
        return {
            "pr_id": pr_id,
            "code": bug.get("code", bug.get("code_snippet", "No code provided")),
            "status": "open",
            "metadata": bug
        }

    def _fallback_pr(self) -> Dict[str, Any]:
        return {
            "pr_id": "fallback_00",
            "code": "print('hello')",
            "status": "open",
            "metadata": {
                "id": "none",
                "issue_keywords": [],
                "fix_keywords": []
            }
        }
