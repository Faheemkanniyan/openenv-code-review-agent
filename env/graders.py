import re
from typing import List, Dict, Any
from env.models import Action

class Grader:
    @staticmethod
    def evaluate_issue_detection(action_desc: str, metadata: Dict[str, Any]) -> bool:
        """Returns True if the description contains expected issue keywords."""
        if not action_desc:
            return False
        keywords = metadata.get("issue_keywords", [])
        desc_lower = action_desc.lower()
        return any(k.lower() in desc_lower for k in keywords)

    @staticmethod
    def evaluate_fix_suggestion(action_desc: str, metadata: Dict[str, Any]) -> bool:
        """Returns True if the description contains expected fix keywords."""
        if not action_desc:
            return False
        keywords = metadata.get("fix_keywords", [])
        desc_lower = action_desc.lower()
        return any(k.lower() in desc_lower for k in keywords)

    @staticmethod
    def should_approve(metadata: Dict[str, Any]) -> bool:
        """If metadata has bug info, it shouldn't be approved."""
        # Clean PRs have id 'none' or 'clean' (depends on generator)
        return metadata.get("id") in ["none", "clean"]
