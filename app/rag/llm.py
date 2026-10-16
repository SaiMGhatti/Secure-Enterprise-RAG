import json
import urllib.error
import urllib.request

from app.config import settings


class LLMError(RuntimeError):
    pass


def generate(system_prompt: str, user_prompt: str) -> str:
    payload = json.dumps(
        {
            "model": settings.ollama_model,
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{settings.ollama_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request, timeout=settings.ollama_timeout_seconds
        ) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise LLMError(f"Ollama request failed: {exc}") from exc

    try:
        return body["message"]["content"].strip()
    except (KeyError, TypeError) as exc:
        raise LLMError("Unexpected response from Ollama") from exc
