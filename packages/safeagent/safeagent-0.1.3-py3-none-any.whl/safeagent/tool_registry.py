# src/minillm/tool_registry.py

import asyncio
import hashlib
import inspect
import json
import time
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from .embeddings import gemini_embed
from .governance import GovernanceManager
from .sinks import BaseOutputSink
from rbac import RBACError

def check_access(user_id: str, required_role: str) -> bool:
    """
    Checks if a user has a required role..

    NOTE: This is a placeholder implementation. A real system would look
    this up in a database or identity provider.
    """
    user_role_database = {
        "user_viktor": ["billing_agent", "support"],
        "forecaster_alex": ["weather_forecaster"],
        "intern_bob": ["guest"]
    }

    current_user_roles = user_role_database.get(user_id, [])
    if required_role in current_user_roles:
        return True

    return False
    
try:
    import faiss
    import numpy as np
    _EMBEDDINGS_ENABLED = True
except ImportError:
    _EMBEDDINGS_ENABLED = False
    print("WARNING: 'faiss-cpu' or 'numpy' not found. Semantic tool search will be disabled.")
    # Define dummy classes if imports fail, so the code doesn't crash at runtime.
    class faiss:
        class IndexFlatL2:
            def __init__(self, d): pass
            def add(self, v): pass
            def search(self, q, k): pass
            @property
            def ntotal(self): return 0
        IndexFlatIP = IndexFlatL2

    class np:
        @staticmethod
        def array(*args, **kwargs): return []
        @staticmethod
        def float32(*args, **kwargs): return []
        class linalg:
            @staticmethod
            def norm(*args, **kwargs): return 1

# --- Configuration Enums and Classes ---

class SimilarityMetric(Enum):
    """Specifies the similarity metric for vector search."""
    L2 = "l2"
    COSINE = "cosine"
    DOT_PRODUCT = "dot_product"

# --- Custom Exceptions for the Tool Registry ---
class ToolRegistryError(Exception):
    """Base class for tool registry exceptions."""
    pass

class ToolNotFoundError(ToolRegistryError):
    """Raised when a tool is not found in the registry."""
    pass

class ToolExecutionError(ToolRegistryError):
    """Raised when a tool fails to execute after all retries."""
    pass

# --- Main Class ---
class ToolRegistry:
    """
    A central, governed registry for tools that includes RBAC, automatic retries,
    circuit breakers, cost/latency tracking, caching, async support, output sinks,
    and dynamic schemas.
    """
    def __init__(
        self,
        governance_manager: GovernanceManager,
        embedding_config: Optional[Dict] = None,
        similarity_metric: SimilarityMetric = SimilarityMetric.L2,
        embedding_dimension: int = 768
    ):
        self._tools: Dict[str, Callable] = {}
        self._tool_metadata: Dict[str, Dict] = {}
        self.gov = governance_manager
        self.embedding_config = embedding_config or {}
        self.similarity_metric = similarity_metric
        self.embedding_dimension = embedding_dimension
        self._circuit_breaker_state: Dict[str, Dict] = {}
        self._cache: Dict[str, Dict] = {}  # In-memory cache

        self._tool_index = None
        self._index_to_tool_name: Dict[int, str] = {}
        if _EMBEDDINGS_ENABLED:
            self._initialize_faiss_index()

    def _initialize_faiss_index(self):
        """Initializes the correct FAISS index based on the chosen similarity metric."""
        if self.similarity_metric == SimilarityMetric.L2:
            self._tool_index = faiss.IndexFlatL2(self.embedding_dimension)
        elif self.similarity_metric in (SimilarityMetric.COSINE, SimilarityMetric.DOT_PRODUCT):
            self._tool_index = faiss.IndexFlatIP(self.embedding_dimension)
        else:
            raise ValueError("Unsupported similarity metric: {}".format(self.similarity_metric))

    def _index_tool(self, tool_name: str):
        """Embeds and indexes a tool's description for semantic search."""
        if not _EMBEDDINGS_ENABLED or self._tool_index is None: return
        metadata = self._tool_metadata.get(tool_name, {})
        description = "Tool: {}. Description: {}".format(tool_name, metadata.get("docstring", ""))
        api_key = self.embedding_config.get("api_key", "")
        vector = gemini_embed(text=description, api_key=api_key)
        if vector:
            vector_np = np.array([vector], dtype=np.float32)
            if self.similarity_metric == SimilarityMetric.COSINE:
                faiss.normalize_L2(vector_np)
            new_index_id = self._tool_index.ntotal
            self._tool_index.add(vector_np)
            self._index_to_tool_name[new_index_id] = tool_name

    def register(
        self,
        required_role: Optional[str] = None,
        retry_attempts: int = 0,
        retry_delay: float = 1.0,
        circuit_breaker_threshold: int = 0,
        cache_ttl_seconds: int = 0,
        cost_per_call: Optional[float] = None,
        cost_calculator: Optional[Callable[[Any], float]] = None,
        output_sinks: Optional[List[BaseOutputSink]] = None
    ) -> Callable:
        """A decorator to register a tool with advanced, governed execution policies."""
        def decorator(func: Callable) -> Callable:
            tool_name = func.__name__
            self._tools[tool_name] = func
            self._tool_metadata[tool_name] = {
                "docstring": inspect.getdoc(func),
                "signature": inspect.signature(func),
                "is_async": inspect.iscoroutinefunction(func),
                "policies": {
                    "role": required_role, "retry_attempts": retry_attempts,
                    "retry_delay": retry_delay, "circuit_breaker_threshold": circuit_breaker_threshold,
                    "cache_ttl_seconds": cache_ttl_seconds, "cost_per_call": cost_per_call,
                    "cost_calculator": cost_calculator, "output_sinks": output_sinks or []
                }
            }
            self._circuit_breaker_state[tool_name] = {'failure_count': 0, 'is_open': False, 'opened_at': 0}
            self._index_tool(tool_name)
            return func
        return decorator

    def _create_cache_key(self, tool_name: str, **kwargs) -> str:
        """Creates a stable cache key from the tool name and arguments."""
        hasher = hashlib.md5()
        encoded = json.dumps(kwargs, sort_keys=True).encode('utf-8')
        hasher.update(encoded)
        return "{}:{}".format(tool_name, hasher.hexdigest())

    def _check_pre_execution_policies(self, name: str, user_id: str, policies: Dict, **kwargs) -> Optional[Any]:
        """Handles caching, circuit breaker, and RBAC checks. Returns cached result if hit."""
        # 1. Caching
        if policies["cache_ttl_seconds"] > 0:
            cache_key = self._create_cache_key(name, **kwargs)
            if cache_key in self._cache:
                cached_item = self._cache[cache_key]
                if time.time() - cached_item["timestamp"] < policies["cache_ttl_seconds"]:
                    self.gov.audit(user_id, "tool_cache_hit", name, {"args": kwargs})
                    return cached_item["result"]
        
        # 2. Circuit Breaker
        cb_state = self._circuit_breaker_state[name]
        if cb_state['is_open']:
            if time.time() - cb_state['opened_at'] > 60:  # 1-minute cooldown
                cb_state['is_open'] = False
            else:
                msg = "Circuit breaker for tool '{}' is open.".format(name)
                self.gov.audit(user_id, "tool_circuit_breaker_open", name, {"error": msg})
                raise ToolExecutionError(msg)

        # 3. RBAC
        if policies["role"] and not check_access(user_id, policies["role"]):
            msg = "User '{}' lacks required role '{}' for tool '{}'.".format(user_id, policies["role"], name)
            self.gov.audit(user_id, "tool_access_denied", name, {"required_role": policies["role"]})
            raise RBACError(msg)
            
        return None

    def _handle_post_execution(self, name: str, user_id: str, policies: Dict, result: Any, latency_ms: float, **kwargs):
        """Handles auditing, cost calculation, caching, and output sinks after successful execution."""
        cost = policies["cost_per_call"]
        if policies["cost_calculator"]:
            cost = policies["cost_calculator"](result)

        audit_metadata = {"result_type": type(result).__name__, "latency_ms": round(latency_ms), "cost": cost}
        self.gov.audit(user_id, "tool_call_end", name, audit_metadata)

        if policies["cache_ttl_seconds"] > 0:
            cache_key = self._create_cache_key(name, **kwargs)
            self._cache[cache_key] = {"timestamp": time.time(), "result": result}
        
        run_id = self.gov.get_current_run_id()
        for sink in policies["output_sinks"]:
            try:
                sink_metadata = sink.handle(name, result, run_id, **kwargs)
                self.gov.audit(user_id, "output_sink_success", str(sink), {"tool_name": name, **sink_metadata})
            except Exception as e:
                self.gov.audit(user_id, "output_sink_failure", str(sink), {"tool_name": name, "error": str(e)})

    def _handle_execution_error(self, name: str, user_id: str, policies: Dict, e: Exception, attempt: int):
        """Handles failures, including retry logic and circuit breaker trips."""
        self.gov.audit(user_id, "tool_call_error", name, {"error": str(e), "attempt": attempt + 1})
        if attempt >= policies["retry_attempts"]:
            cb_state = self._circuit_breaker_state[name]
            cb_state['failure_count'] += 1
            if policies["circuit_breaker_threshold"] > 0 and cb_state['failure_count'] >= policies["circuit_breaker_threshold"]:
                cb_state['is_open'] = True
                cb_state['opened_at'] = time.time()
                self.gov.audit(user_id, "tool_circuit_breaker_tripped", name)
            raise ToolExecutionError("Tool '{}' failed after all retry attempts.".format(name)) from e

    def _get_governed_sync_tool(self, name: str, user_id: str, original_func: Callable, policies: Dict) -> Callable:
        """Returns the fully governed wrapper for a synchronous tool."""
        def sync_wrapper(**kwargs):
            cached_result = self._check_pre_execution_policies(name, user_id, policies, **kwargs)
            if cached_result is not None: return cached_result

            for attempt in range(policies["retry_attempts"] + 1):
                start_time = time.monotonic()
                try:
                    self.gov.audit(user_id, "tool_call_start", name, {"args": kwargs, "attempt": attempt + 1})
                    result = original_func(**kwargs)
                    latency_ms = (time.monotonic() - start_time) * 1000
                    self._handle_post_execution(name, user_id, policies, result, latency_ms, **kwargs)
                    return result
                except Exception as e:
                    self._handle_execution_error(name, user_id, policies, e, attempt)
                    time.sleep(policies["retry_delay"] * (2 ** attempt))
            # This line should be logically unreachable if retry_attempts >= 0
            raise ToolExecutionError("Tool '{}' execution logic failed unexpectedly.".format(name))
        return sync_wrapper

    def _get_governed_async_tool(self, name: str, user_id: str, original_func: Callable, policies: Dict) -> Callable:
        """Returns the fully governed wrapper for an asynchronous tool."""
        async def async_wrapper(**kwargs):
            cached_result = self._check_pre_execution_policies(name, user_id, policies, **kwargs)
            if cached_result is not None: return cached_result

            for attempt in range(policies["retry_attempts"] + 1):
                start_time = time.monotonic()
                try:
                    self.gov.audit(user_id, "tool_call_start", name, {"args": kwargs, "attempt": attempt + 1})
                    result = await original_func(**kwargs)
                    latency_ms = (time.monotonic() - start_time) * 1000
                    self._handle_post_execution(name, user_id, policies, result, latency_ms, **kwargs)
                    return result
                except Exception as e:
                    self._handle_execution_error(name, user_id, policies, e, attempt)
                    await asyncio.sleep(policies["retry_delay"] * (2 ** attempt))
            # This line should be logically unreachable if retry_attempts >= 0
            raise ToolExecutionError("Tool '{}' execution logic failed unexpectedly.".format(name))
        return async_wrapper

    def get_governed_tool(self, name: str, user_id: str) -> Callable:
        """
        Retrieves a tool by name and wraps it in all registered governance policies.
        This method correctly handles both synchronous and asynchronous tools.
        """
        if name not in self._tools:
            raise ToolNotFoundError("Tool '{}' not found in registry.".format(name))
        
        metadata = self._tool_metadata[name]
        original_func = self._tools[name]
        policies = metadata["policies"]
        
        if metadata["is_async"]:
            return self._get_governed_async_tool(name, user_id, original_func, policies)
        else:
            return self._get_governed_sync_tool(name, user_id, original_func, policies)

    def generate_tool_schema(self, tool_names: List[str]) -> List[Dict[str, Any]]:
        """Generates a JSON Schema-like description for a list of tools."""
        schema = []
        for name in tool_names:
            if name in self._tool_metadata:
                metadata = self._tool_metadata[name]
                sig = metadata["signature"]
                properties = {}
                for param in sig.parameters.values():
                    if param.name != 'self':
                        type_map = {str: 'string', int: 'number', float: 'number', bool: 'boolean'}
                        param_type = type_map.get(param.annotation, 'string')
                        properties[param.name] = {'type': param_type, 'description': ''}
                schema.append({
                    "name": name,
                    "description": metadata["docstring"],
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": [p.name for p in sig.parameters.values() if p.default == inspect.Parameter.empty and p.name != 'self']
                    }
                })
        return schema
        
    def get_relevant_tools(self, query: str, top_k: int = 3) -> List[str]:
        """Finds the most semantically relevant tools for a given query using a vector index."""
        if not _EMBEDDINGS_ENABLED or self._tool_index is None or self._tool_index.ntotal == 0:
            return []
        api_key = self.embedding_config.get("api_key", "")
        query_vector = gemini_embed(text=query, api_key=api_key)
        if not query_vector:
            return []
        query_np = np.array([query_vector], dtype=np.float32)
        if self.similarity_metric == SimilarityMetric.COSINE:
            faiss.normalize_L2(query_np)
        distances, indices = self._tool_index.search(query_np, min(top_k, self._tool_index.ntotal))
        return [self._index_to_tool_name[i] for i in indices[0]]
