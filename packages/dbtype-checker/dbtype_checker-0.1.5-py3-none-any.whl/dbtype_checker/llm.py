import os
import requests
import json

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  

def ask_llm_for_type(column_name, values):
    prompt = f"""You're a data type expert. Infer the best data type (int, float, str, bool, datetime) for the column named '{column_name}'.
Here are some sample values:
{values}

Respond with only one word: int, float, str, bool, or datetime.
"""

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 10
            },
            timeout=20
        )

        data = response.json()

        if "choices" not in data:
            print("LLM response error:", json.dumps(data, indent=2))
            return None

        return data["choices"][0]["message"]["content"].strip().lower()

    except Exception as e:
        print(" LLM request failed:", e)
        return None
