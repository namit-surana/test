import requests

def call_perplexity(prompt: str) -> str:
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.perplexity.ai/chat/completions", json=data, headers=headers)
    return res.json()["choices"][0]["message"]["content"]
