import time
import json
import logging
from typing import Dict

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs
    requests = None  # type: ignore
from .governance import GovernanceManager
from .utils import get_request_id

class FrameworkError(Exception):
    """Custom exception for framework-related errors."""
    pass

class LLMClient:
    """Thin wrapper around any LLM provider with retries, error handling, and structured JSON logging."""

    def __init__(self, provider: str, api_key: str, model: str, base_url: str = None):
        """
        Initialize the LLM client.

        Args:
            provider (str): Name of the provider (e.g., 'openai', 'anthropic').
            api_key (str): API key or token for authentication.
            model (str): Model identifier (e.g., 'gpt-4', 'claude-3-opus').
            base_url (str, optional): Custom endpoint URL; defaults to provider-specific default.
        """
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or self._default_url()
        if requests is not None:
            self.session = requests.Session()
        else:
            class _DummySession:
                def __init__(self):
                    self.headers = {}

                def post(self, *_, **__):
                    raise FrameworkError("requests package is required for HTTP calls")

            self.session = _DummySession()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.gov = GovernanceManager()

    def _default_url(self) -> str:
        """Return default endpoint URL based on provider."""
        if self.provider == "openai":
            return "https://api.openai.com/v1/chat/completions"
        if self.provider == "anthropic":
            return "https://api.anthropic.com/v1/complete"
        if self.provider == "gemini":
            return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        raise FrameworkError(f"No default URL configured for provider '{self.provider}'")

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> Dict:
        """
        Call the underlying LLM API, with up to 3 retries.

        Args:
            prompt (str): The textual prompt to send to the model.
            max_tokens (int): Maximum number of tokens in the response.
            temperature (float): Sampling temperature.

        Returns:
            Dict: A dictionary containing keys 'text', 'usage', and 'metadata'.

        Raises:
            FrameworkError: If the API fails after retries.
        """
        # Encrypt the prompt before logging
        encrypted_prompt = self.gov.encrypt(prompt)
        self.gov.audit(user_id="system", action="encrypt_prompt", resource="llm_client", metadata={"prompt_enc": encrypted_prompt[:50]})
        payload = self._build_payload(prompt, max_tokens, temperature)

        # Log start of LLM call and audit
        req_id = get_request_id()
        log_entry_start = {
            "event": "llm_call_start",
            "provider": self.provider,
            "model": self.model,
            "prompt_snippet": prompt[:100],
            "request_id": req_id,
            "timestamp": time.time(),
        }
        logging.info(json.dumps(log_entry_start))
        self.gov.audit(
            user_id="system",
            action="llm_call_start",
            resource=self.provider,
            metadata={"model": self.model, "request_id": req_id},
        )

        # Attempt with exponential backoff
        for attempt in range(3):
            try:
                resp = self.session.post(self.base_url, json=payload, timeout=30)
                if resp.status_code != 200:
                    raise FrameworkError(f"LLM returned status {resp.status_code}: {resp.text}")
                data = resp.json()
                text, usage = self._parse_response(data)

                # Log end of LLM call and audit
                log_entry_end = {
                    "event": "llm_call_end",
                    "provider": self.provider,
                    "model": self.model,
                    "usage": usage,
                    "request_id": req_id,
                    "timestamp": time.time(),
                }
                logging.info(json.dumps(log_entry_end))
                self.gov.audit(
                    user_id="system",
                    action="llm_call_end",
                    resource=self.provider,
                    metadata={"model": self.model, "usage": usage, "request_id": req_id},
                )

                return {"text": text, "usage": usage, "metadata": {"provider": self.provider, "model": self.model}}

            except Exception as e:
                wait = 2 ** attempt
                logging.warning(f"LLM call failed (attempt {attempt + 1}): {e}. Retrying in {wait}s")
                time.sleep(wait)

        raise FrameworkError("LLM generate() failed after 3 attempts")

    def _build_payload(self, prompt: str, max_tokens: int, temperature: float) -> Dict:
        """Construct provider-specific payload for the API call."""
        if self.provider == "openai":
            return {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        if self.provider == "anthropic":
            return {
                "model": self.model,
                "prompt": prompt,
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature
            }
        if self.provider == "gemini":
            return {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature}
            }
        raise FrameworkError(f"Payload builder not implemented for '{self.provider}'")

    def _parse_response(self, data: Dict) -> (str, Dict):
        """Extract generated text and usage info from API response."""
        if self.provider == "openai":
            choice = data.get("choices", [])[0]
            return choice.get("message", {}).get("content", ""), data.get("usage", {})
        if self.provider == "anthropic":
            return data.get("completion", ""), {
                "prompt_tokens": data.get("prompt_tokens"),
                "completion_tokens": data.get("completion_tokens")
            }
        if self.provider == "gemini":
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            usage = data.get("usageMetadata", {})
            return text, {
                "prompt_tokens": usage.get("promptTokenCount"),
                "completion_tokens": usage.get("candidatesTokenCount"),
            }
        raise FrameworkError(f"Response parser not implemented for '{self.provider}'")
