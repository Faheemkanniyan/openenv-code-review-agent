import json
import random
from typing import List, Dict, Optional

class BugDatabase:
    def __init__(self, filepath: str = "data/bugs.json"):
        self.filepath = filepath
        self.bugs = self._load_bugs()

    def _load_bugs(self) -> List[Dict]:
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading bugs: {e}")
            return []

    def get_bug_by_difficulty(self, difficulty: str) -> Optional[Dict]:
        """Returns a random bug of the requested difficulty."""
        candidates = [b for b in self.bugs if b.get('difficulty') == difficulty]
        if not candidates:
            return None
        return random.choice(candidates)

    def get_all_bugs(self) -> List[Dict]:
        return self.bugs
