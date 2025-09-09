# .github/scripts/llm_utils.py
import os, requests

# ✅ Load model from GitHub Actions vars, fallback to gpt-4o-mini
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def llm(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }

    # 🔎 Debugging API response
    r = requests.post(url, headers=headers, json=body, timeout=60)
    if r.status_code != 200:
        print("❌ OpenAI API Error:", r.status_code, r.text)
        r.raise_for_status()

    data = r.json()
    return data["choices"][0]["message"]["content"]

