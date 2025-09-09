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

    # Debug: print request info
    print("🔑 Using API key prefix:", OPENAI_API_KEY[:10] if OPENAI_API_KEY else None)
    print("📦 Model:", MODEL)
    print("📤 Request body:", json.dumps(body, indent=2))

    r = requests.post(url, headers=headers, json=body, timeout=60)

    # Debug: show full response
    print("📩 Status code:", r.status_code)
    print("📩 Response text:", r.text)

    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


