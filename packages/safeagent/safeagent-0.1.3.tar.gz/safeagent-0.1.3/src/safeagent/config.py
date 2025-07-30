"""Simple configuration loader with environment variable defaults."""

from dataclasses import dataclass, field
import os

@dataclass
class Config:
    # LLM and Template Configuration
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "gemini"))
    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini-pro"))
    template_dir: str = field(default_factory=lambda: os.getenv("TEMPLATE_DIR", "templates"))
    # Retriever Configuration
    faiss_index_path: str = field(default_factory=lambda: os.getenv("FAISS_INDEX_PATH", "faiss.idx"))
    neo4j_uri: str = field(default_factory=lambda: os.getenv("NEO4J_URI", "bolt://localhost:7687"))
    neo4j_user: str = field(default_factory=lambda: os.getenv("NEO4J_USER", "neo4j"))
    neo4j_password: str = field(default_factory=lambda: os.getenv("NEO4J_PASSWORD", ""))
    gds_graph_name: str = field(default_factory=lambda: os.getenv("GDS_GRAPH_NAME", "myGraph"))
    # Memory Configuration
    memory_backend: str = field(default_factory=lambda: os.getenv("MEMORY_BACKEND", "redis"))
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))
    # Tool Registry and Embedding Configuration
    embedding_dimension: int = field(default_factory=lambda: int(os.getenv("EMBEDDING_DIMENSION", "768")))
    tool_similarity_metric: str = field(default_factory=lambda: os.getenv("TOOL_SIMILARITY_METRIC", "cosine"))