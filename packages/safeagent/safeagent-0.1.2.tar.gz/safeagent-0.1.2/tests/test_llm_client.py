import pytest
from minillm.llm_client import LLMClient, FrameworkError

class DummySession:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def post(self, url, json, timeout):
        class Resp:
            def __init__(self, sc, d):
                self.status_code = sc
                self._d = d

            def json(self):
                return self._d

            @property
            def text(self):
                return str(self._d)
        # Return the provided response data
        return Resp(self.status_code, self._json)


def test_generate_success(monkeypatch):
    client = LLMClient(provider="openai", api_key="fake", model="gpt-4")
    dummy = DummySession(200, {"choices": [{"message": {"content": "Test"}}], "usage": {"prompt_tokens": 1, "completion_tokens": 1}})
    monkeypatch.setattr(client, "session", dummy)
    res = client.generate("Hi", max_tokens=5, temperature=0.5)
    assert res["text"] == "Test"
    assert "usage" in res


def test_generate_failure(monkeypatch):
    client = LLMClient(provider="openai", api_key="fake", model="gpt-4")
    class BadSession:
        def post(self, url, json, timeout):
            # Simulate non-200 status code
            class Resp:
                status_code = 500
                text = "Error"
                def json(self):
                    return {}
            return Resp()
    monkeypatch.setattr(client, "session", BadSession())
    with pytest.raises(FrameworkError):
        client.generate("Hi", max_tokens=5, temperature=0.5)
