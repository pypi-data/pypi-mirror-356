import json
from typing import List

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - minimal fallback
    requests = None  # type: ignore
    class _DummySession:
        def post(self, *_, **__):
            raise RuntimeError("requests package is required for HTTP calls")
    _session = _DummySession()
else:
    _session = requests.Session()


def gemini_embed(text: str, api_key: str, model: str = "embedding-001") -> List[float]:
    """Return an embedding vector from the Gemini embedding API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent?key={api_key}"
    payload = {"content": {"parts": [{"text": text}]}}
    resp = _session.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini embed failed: {resp.text}")
    data = resp.json()
    return data.get("embedding", {}).get("values", [])
