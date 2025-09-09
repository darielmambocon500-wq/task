import os
import requests
import sys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    print("❌ Missing OPENAI_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)

def llm(prompt: str, sys_msg: str = "You generate concise, actionable plans and code diffs.") -> str:
    """
    Call OpenAI Chat Completions API and return text output.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    try:
        r = requests.post(url, headers=headers, json=body, timeout=60)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    data = r.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"❌ Unexpected API response: {data}", file=sys.stderr)
        sys.exit(1)


