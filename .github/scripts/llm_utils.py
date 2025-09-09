# .github/scripts/llm_utils.py
import os, requests

def llm(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
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

