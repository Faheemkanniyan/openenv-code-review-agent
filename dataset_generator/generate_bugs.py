import os
import json
from openai import OpenAI

def generate_synthetic_bugs(num_bugs: int = 5):
    """
    Connects to OpenAI to generate synthetic bugs based on a prompt.
    To use this, ensure OPENAI_API_KEY is exported in your environment.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    Generate {num_bugs} unique code snippets containing common software bugs.
    Format the output strictly as a JSON array of objects with the following keys:
    - id: a unique string identifier
    - difficulty: 'easy', 'medium', or 'hard'
    - category: 'security', 'logic', 'performance', 'concurrency', 'memory', 'syntax', or 'style'
    - code_snippet: the raw buggy code in Python
    - bug_description: short explanation
    - expected_fix: short explanation of the fix
    - issue_keywords: array of strong keywords strings related to the bug
    - fix_keywords: array of strong keywords strings related to the fix
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert software engineer generating bugs for a code review dataset."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        data = json.loads(response.choices[0].message.content)
        return data.get("bugs", data) if isinstance(data, dict) else data
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return []

if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set OPENAI_API_KEY to generate datasets.")
    else:
        new_bugs = generate_synthetic_bugs(5)
        with open("data/synthetic_bugs.json", "w") as f:
            json.dump(new_bugs, f, indent=4)
        print(f"Generated {len(new_bugs)} synthetic bugs.")
