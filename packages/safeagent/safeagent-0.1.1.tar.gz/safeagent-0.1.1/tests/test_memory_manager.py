import pytest
from minillm.memory_manager import MemoryManager


def test_inmemory_save_load():
    mm = MemoryManager(backend="inmemory")
    mm.save("user1", "greeting", "hello")
    assert mm.load("user1", "greeting") == "hello"
    assert mm.load("user1", "missing") == ""


def test_redis_save_load(monkeypatch):
    # Mock Redis client
    class DummyRedis:
        def __init__(self):
            self.store = {}
        def hset(self, key, subkey, val):
            self.store.setdefault(key, {})[subkey] = val
        def hget(self, key, subkey):
            return self.store.get(key, {}).get(subkey, None)

    import minillm.memory_manager as memory_manager
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    monkeypatch.setattr(memory_manager, "_redis", type("x", (), {"from_url": lambda url: DummyRedis()}))
    mm = MemoryManager(backend="redis", redis_url="redis://localhost:6379")
    mm.save("user1", "greeting", "hi")
    assert mm.load("user1", "greeting") == "hi"
