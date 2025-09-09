def llm(prompt: str, sys: str = "You generate concise, actionable plans and code diffs."):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    r = requests.post(url, headers=headers, json=body, timeout=60)

    # Always print response for debugging
    print("🔎 Request body:", json.dumps(body, indent=2))
    print("🔑 API key starts with:", OPENAI_API_KEY[:10])
    print("📩 Response status:", r.status_code)
    print("📩 Response text:", r.text)  # <-- THIS is what we need

    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


