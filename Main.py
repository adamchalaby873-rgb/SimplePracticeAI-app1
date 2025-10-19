# deepseek_api.py
import requests
import time

def query_deepseek(prompt, api_key, retries=3, backoff=2):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "x-ai/grok-4-fast:free",
        "messages": [
            {"role": "system",
             "content": "You are AdamGPT, a formal and smart guy. You always use the feature of your AI to get the most accurate answer."
                 "Never refer to yourself as Grok. Always maintain your AdamGPT persona."},
            {"role": "user", "content": f"{prompt}."}
        ]
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
        except Exception as e:
            return f"Error parsing JSON: {e}"

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            error_info = result.get("error", result)
            if isinstance(error_info, dict) and error_info.get("code") == 429 and attempt < retries:
                wait_time = backoff ** attempt
                print(f"Rate limited, retrying in {wait_time}s (Attempt {attempt}/{retries})...")
                time.sleep(wait_time)
            else:
                return f"API Error: {result}"

    return f"Failed after {retries} retries. Last response: {result}"
