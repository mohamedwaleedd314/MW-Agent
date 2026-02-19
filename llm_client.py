import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

REQUEST_HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
}

LLM_MODEL = "deepseek-ai/DeepSeek-V3:novita"


def stream_chat_response(prompt, max_tokens=2000):

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "stream": True
    }

    response = requests.post(
        API_URL,
        headers=REQUEST_HEADERS,
        json=payload,
        stream=True
    )

    if response.status_code != 200:
        yield f"Error {response.status_code}: {response.text}"
        return

    accumulated_text = ""

    for line in response.iter_lines():
        if not line:
            continue

        decoded_line = line.decode("utf-8")

        if decoded_line.startswith("data:"):
            decoded_line = decoded_line.replace("data:", "").strip()

        if decoded_line == "[DONE]":
            break

        try:
            data = json.loads(decoded_line)

            if "choices" in data:
                delta = data["choices"][0].get("delta", {})

                if "content" in delta:
                    token = delta["content"]
                    accumulated_text += token
                    yield accumulated_text

        except:
            continue
