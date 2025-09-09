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

    # Debugging
    print("🔎 Debug LLM Request:", json.dumps(body, indent=2))
    print("🔑 Using key prefix:", OPENAI_API_KEY[:10])  # only shows first 10 chars, safe to log

    r = requests.post(url, headers=headers, json=body, timeout=60)
    try:
        r.raise_for_status()
    except Exception as e:
        print("❌ Error response:", r.text)  # <-- this will tell us why OpenAI said 400
        raise
    return r.json()["choices"][0]["message"]["content"]


