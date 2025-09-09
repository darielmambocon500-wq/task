import os
import requests
import sys
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

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

    if DEBUG:
        print("🟦 [DEBUG] Sending request to OpenAI:", file=sys.stderr)
        print(json.dumps(body, indent=2), file=sys.stderr)

    try:
        r = requests.post(url, headers=headers, json=body, timeout=60)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"❌ HTTP error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    data = r.json()

    if DEBUG:
        print("🟩 [DEBUG] OpenAI response:", file=sys.stderr)
        print(json.dumps(data, indent=2), file=sys.stderr)

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"❌ Unexpected API response: {data}", file=sys.stderr)
        sys.exit(1)
