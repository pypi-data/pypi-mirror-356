import time
import logging
import numpy as np
from pathlib import Path
from .orchestrator import SimpleOrchestrator
from .llm_client import LLMClient, FrameworkError
from .prompt_renderer import PromptRenderer
from .retriever import VectorRetriever, GraphRetriever
from .embeddings import gemini_embed
from .memory_manager import MemoryManager
from rbac import check_access, RBACError
from .governance import GovernanceManager
from .config import Config

# Configure logging to output JSON lines to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

# Initialize governance manager (purge old logs on startup)
gov_manager = GovernanceManager()
gov_manager.purge_old_logs()

# -----------------------------------
# 1. Initialize shared resources
# -----------------------------------

cfg = Config()

# LLM client. Values can be overridden by modifying `cfg` before calling main().
llm = LLMClient(
    provider=cfg.llm_provider,
    api_key=cfg.api_key,
    model=cfg.llm_model,
)

# Prompt renderer (look for templates in 'templates/' directory)
renderer = PromptRenderer(template_dir=Path(cfg.template_dir))

# Vector retriever (FAISS). Uses Gemini embeddings by default.
vector_ret = VectorRetriever(
    index_path=cfg.faiss_index_path,
    embed_model_fn=lambda text: gemini_embed(text, cfg.api_key),
)

# Graph retriever (Neo4j GDS). Provide correct connection details.
graph_ret = GraphRetriever(
    neo4j_uri=cfg.neo4j_uri,
    user=cfg.neo4j_user,
    password=cfg.neo4j_password,
    gds_graph_name=cfg.gds_graph_name,
    embed_model_fn=lambda text: gemini_embed(text, cfg.api_key),
)

# Memory manager (Redis backend). Use "inmemory" for simpler testing.
mem_mgr = MemoryManager(
    backend=cfg.memory_backend,
    redis_url=cfg.redis_url,
)

# Audit framework initialization
gov_manager.audit(user_id="system", action="pipeline_init", resource="minillm_framework")

# -----------------------------------
# 2. Define DAG node functions
# -----------------------------------

def retrieve_docs(user_input: str, user_id: str, **kwargs):
    """
    Hybrid retrieval from vector store and Neo4j.
    Merges results and deduplicates by 'id'.
    """
    # Access control
    if not check_access(user_id, "vector_store"):
        raise RBACError(f"User {user_id} unauthorized for retrieval")

    v_docs = vector_ret.query(user_input, top_k=5)
    g_docs = graph_ret.query(user_input, top_k=5)
    combined = {d["id"]: d for d in (v_docs + g_docs)}
    return list(combined.values())


def make_prompt(retrieve_docs: list, user_input: str, user_id: str, **kwargs) -> str:
    """
    Render the QA prompt with retrieved documents.
    """
    # Access control
    if not check_access(user_id, "prompt_render"):
        raise RBACError(f"User {user_id} unauthorized to render prompts")

    return renderer.render(
        "qa_prompt.j2",
        question=user_input,
        docs=retrieve_docs
    )


def call_llm(make_prompt: str, user_id: str, **kwargs) -> dict:
    """
    Prepend memory summary to prompt and call LLM.
    """
    if not check_access(user_id, "llm_call"):
        raise RBACError(f"User {user_id} unauthorized for LLM calls")

    # Load existing memory summary
    summary = mem_mgr.load(user_id, "summary") or ""
    full_prompt = f"{summary}\n\n{make_prompt}"
    response = llm.generate(full_prompt)
    return response


def update_memory(call_llm: dict, user_id: str, **kwargs) -> str:
    """
    Save raw LLM response to memory and generate a new summary.
    """
    text = call_llm.get("text", "")
    timestamp_key = f"raw_{time.time()}"
    mem_mgr.save(user_id, timestamp_key, text)
    new_summary = mem_mgr.summarize(
        user_id=user_id,
        embed_fn=lambda txt: gemini_embed(txt, cfg.api_key),
        llm_client=llm
    )
    return new_summary


def update_graph(call_llm: dict, user_id: str, **kwargs) -> list:
    """
    Extract dummy entities from LLM response and ingest into Neo4j.
    Replace with real NER logic as needed.
    """
    text = call_llm.get("text", "")
    # Dummy extraction: words longer than 5 characters
    entities = [w.strip(".,") for w in text.split() if len(w) > 5]
    records = []
    for ent in entities:
        records.append({
            "id": ent,
            "properties": {"name": ent},
            "relationships": []  # Define relationships if available
        })
    # Ingest entities into Neo4j
    with graph_ret.driver.session() as session:
        for rec in records:
            session.run(
                "MERGE (e:Entity {id: $id}) SET e.name = $name",
                id=rec["id"], name=rec["properties"]["name"]
            )
    return entities

# -----------------------------------
# 3. Build and run the DAG
# -----------------------------------

orch = SimpleOrchestrator()
orch.add_node("retrieve_docs", retrieve_docs)
orch.add_node("make_prompt", make_prompt)
orch.add_node("call_llm", call_llm)
orch.add_node("update_memory", update_memory)
orch.add_node("update_graph", update_graph)

# Define dependencies
orch.add_edge("retrieve_docs", "make_prompt")
orch.add_edge("make_prompt", "call_llm")
orch.add_edge("call_llm", "update_memory")
orch.add_edge("call_llm", "update_graph")

if __name__ == "__main__":
    # Example user inputs
    inputs = {
        "user_input": "Tell me about Jupiter's moons",  # e.g., from CLI or API
        "user_id": "user123"                            # Unique user/session ID
    }
    # Audit pipeline execution
    gov_manager.audit(user_id=inputs.get("user_id"), action="run_pipeline", resource="pipeline")
    try:
        outputs = orch.run(inputs)
    except RBACError as e:
        gov_manager.audit(user_id=inputs.get("user_id"), action="access_denied", resource="pipeline", metadata={"reason": str(e)})
        logging.error(json.dumps({"event": "access_denied", "reason": str(e), "timestamp": time.time()}))
        exit(1)

    # Extract and print the LLM's answer
    answer = outputs.get("call_llm", {}).get("text", "")
    print("LLM answer:\n", answer)
