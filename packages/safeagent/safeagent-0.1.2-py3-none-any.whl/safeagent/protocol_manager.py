import json
import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List
from rbac import RBACError, check_access
from .config import Config
from .embeddings import gemini_embed
from .governance import GovernanceManager
from .llm_client import LLMClient
from .memory_manager import MemoryManager
from .orchestrator import SimpleOrchestrator
from .prompt_renderer import PromptRenderer
from .retriever import GraphRetriever, VectorRetriever
from .tool_registry import SimilarityMetric, ToolRegistry

# Protocol Configuration
class PROTOCOLS(Enum):
    """Defines the supported communication/execution protocols."""
    MCP = "mcp"  # Master/Controller/Program protocol
    AGENT2AGENT = "agent2agent"

DEFAULT_PROTOCOL = os.getenv("PROTOCOL_TYPE", PROTOCOLS.MCP.value)

# Global Governance Manager
gov = GovernanceManager()

class ProtocolManager:
    """
    Manages the selection and execution of different agent workflows (protocols).
    This class acts as the main entry point for running a complete agent system.
    """
    def __init__(self, protocol: str = None):
        self.protocol = protocol or DEFAULT_PROTOCOL
        if self.protocol not in (p.value for p in PROTOCOLS):
            raise ValueError("Unsupported protocol: {}".format(self.protocol))
        gov.audit(
            user_id="system",
            action="protocol_selected",
            resource="ProtocolManager",
            metadata={"protocol": self.protocol}
        )

    def run(self, inputs: Dict[str, Any]) -> Any:
        """
        Executes the configured workflow based on the selected protocol.
        """
        if self.protocol == PROTOCOLS.MCP.value:
            return self._run_mcp(inputs)
        elif self.protocol == PROTOCOLS.AGENT2AGENT.value:
            return self._run_agent2agent(inputs)
        else:
            raise NotImplementedError("Protocol '{}' is not implemented.".format(self.protocol))

    def _initialize_shared_resources(self):
        """Initializes all shared components needed by the protocols."""
        cfg = Config()
        llm = LLMClient(provider=cfg.llm_provider, api_key=cfg.api_key, model=cfg.llm_model)
        renderer = PromptRenderer(template_dir=Path(cfg.template_dir))
        embedding_fn = lambda text: gemini_embed(text, cfg.api_key)

        vector_ret = VectorRetriever(index_path=cfg.faiss_index_path, embed_model_fn=embedding_fn)
        graph_ret = GraphRetriever(
            neo4j_uri=cfg.neo4j_uri,
            user=cfg.neo4j_user,
            password=cfg.neo4j_password,
            gds_graph_name=cfg.gds_graph_name,
            embed_model_fn=embedding_fn
        )
        mem_mgr = MemoryManager(backend=cfg.memory_backend, redis_url=cfg.redis_url)

        # Correctly initialize the ToolRegistry with all new configurations
        tool_registry = ToolRegistry(
            governance_manager=gov,
            embedding_config={"api_key": cfg.api_key},
            similarity_metric=SimilarityMetric(cfg.tool_similarity_metric),
            embedding_dimension=cfg.embedding_dimension
        )
        return llm, renderer, vector_ret, graph_ret, mem_mgr, tool_registry

    def _define_tools(self, tool_registry: ToolRegistry):
        """A central place to define and register all available tools with policies."""
        @tool_registry.register(
            cost_per_call=0.001,
            cache_ttl_seconds=512,  # Cache results for 8 minutes 31.8 seconds
            retry_attempts=2
        )
        def get_weather(city: str) -> str:
            """A governed tool to fetch the weather for a given city."""
            if "zephyrhills" in city.lower():
                return "It is currently 82°F and sunny in Zephyrhills."
            elif "san francisco" in city.lower():
                return "It is currently 65°F and foggy in San Francisco."
            else:
                return "Weather data for {} is not available.".format(city)

    def _build_mcp_orchestrator(self, resources: tuple) -> SimpleOrchestrator:
        """Builds the MCP orchestrator with the superior tool-use workflow."""
        llm, renderer, vector_ret, graph_ret, mem_mgr, tool_registry = resources
        self._define_tools(tool_registry)

        orch = SimpleOrchestrator()

        def retrieve_docs(user_input: str, user_id: str, **kwargs):
            if not check_access(user_id, "vector_store"):
                raise RBACError("User {} unauthorized for retrieval".format(user_id))
            v_docs = vector_ret.query(user_input, top_k=3)
            g_docs = graph_ret.query(user_input, top_k=3)
            combined = {d["id"]: d for d in (v_docs + g_docs)}
            return list(combined.values())

        def make_initial_prompt(user_input: str, retrieve_docs: List[dict], **kwargs) -> str:
            # Use semantic search to find only the most relevant tools
            relevant_tools = tool_registry.get_relevant_tools(user_input, top_k=3)
            tool_schemas = tool_registry.generate_tool_schema(relevant_tools)
            return renderer.render(
                "tool_decider_prompt.j2",
                question=user_input,
                docs=retrieve_docs,
                tools=tool_schemas
            )

        def call_llm_for_tool(make_initial_prompt: str, user_id: str, **kwargs) -> dict:
            if not check_access(user_id, "llm_call"):
                raise RBACError("User {} unauthorized for LLM calls".format(user_id))
            summary = mem_mgr.load(user_id, "summary") or ""
            full_prompt = "{}\n\n{}".format(summary, make_initial_prompt)
            return llm.generate(full_prompt)

        def execute_tool(call_llm_for_tool: dict, user_id: str, **kwargs) -> dict:
            response_text = call_llm_for_tool.get("text", "")
            try:
                data = json.loads(response_text)
                if isinstance(data, dict) and "tool_name" in data and "tool_args" in data:
                    tool_name = data["tool_name"]
                    tool_args = data["tool_args"]
                    # Use the fully governed tool wrapper
                    governed_tool = tool_registry.get_governed_tool(tool_name, user_id)
                    result = governed_tool(**tool_args)
                    return {"status": "success", "output": result}
            except (json.JSONDecodeError, TypeError, NameError):
                # If it's not a valid tool call, pass through the text
                pass
            return {"status": "no_tool_needed", "output": response_text}

        def generate_final_answer(execute_tool: dict, user_input: str, **kwargs) -> dict:
            if execute_tool["status"] != "success":
                # If no tool was called, the output from the first LLM is the final answer
                return {"text": execute_tool["output"]}
            # If a tool was called, synthesize a final answer from its result
            final_prompt = renderer.render("synthesis_prompt.j2", question=user_input, tool_result=execute_tool["output"])
            return llm.generate(final_prompt)

        # Define the graph structure
        orch.add_node("retrieve_docs", retrieve_docs)
        orch.add_node("make_initial_prompt", make_initial_prompt)
        orch.add_node("call_llm_for_tool", call_llm_for_tool)
        orch.add_node("execute_tool", execute_tool)
        orch.add_node("generate_final_answer", generate_final_answer)
        # Define the execution flow
        orch.add_edge("user_input", "retrieve_docs")
        orch.add_edge("user_input", "make_initial_prompt")
        orch.add_edge("retrieve_docs", "make_initial_prompt")
        orch.add_edge("make_initial_prompt", "call_llm_for_tool")
        orch.add_edge("call_llm_for_tool", "execute_tool")
        orch.add_edge("user_id", "execute_tool")
        orch.add_edge("execute_tool", "generate_final_answer")
        orch.add_edge("user_input", "generate_final_answer")

        return orch

    def _run_mcp(self, inputs: Dict[str, Any]) -> Any:
        """Runs the complete MCP workflow."""
        resources = self._initialize_shared_resources()
        orch = self._build_mcp_orchestrator(resources)
        gov.audit(user_id=inputs.get("user_id", "system"), action="run_mcp_start", resource="ProtocolManager")
        results = orch.run(inputs)
        gov.audit(user_id=inputs.get("user_id", "system"), action="run_mcp_end", resource="ProtocolManager")
        return results

    def _run_agent2agent(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the Agent-to-Agent simulation workflow."""
        gov.audit(user_id=inputs.get("user_id", "system"), action="run_agent2agent_start", resource="ProtocolManager")
        llm, _, _, vector_ret, mem_mgr, _ = self._initialize_shared_resources()
        agents = {}
        agent_ids = ["analyst_agent", "manager_agent"]
        
        for aid in agent_ids:
            orch = SimpleOrchestrator()
            def retrieve(agent_id=aid, user_input: str = inputs["user_input"], **kwargs):
                return vector_ret.query("Query for {}: {}".format(agent_id, user_input), top_k=2)

            def respond(retrieve: List[dict], agent_id=aid, **kwargs) -> dict:
                doc_ids = [d.get('id', 'N/A') for d in retrieve]
                prompt = "As {}, generate a one-sentence response based on documents: {}".format(agent_id, doc_ids)
                return llm.generate(prompt)

            orch.add_node("{}_retrieve".format(aid), retrieve)
            orch.add_node("{}_respond".format(aid), respond)
            orch.add_edge("{}_retrieve".format(aid), "{}_respond".format(aid))
            agents[aid] = orch

        outputs = {}
        for aid, orch in agents.items():
            gov.audit(user_id=inputs.get("user_id", "system"), action="agent_start", resource=aid)
            res = orch.run(inputs)
            outputs[aid] = res.get("{}_respond".format(aid), {}).get("text", "")
            mem_mgr.save(aid, "last_response", outputs[aid])
            gov.audit(user_id=inputs.get("user_id", "system"), action="agent_end", resource=aid)
            
        gov.audit(user_id=inputs.get("user_id", "system"), action="run_agent2agent_end", resource="ProtocolManager")
        return outputs

# Example usage block to demonstrate and test the MCP protocol.
if __name__ == "__main__":
    # Ensure dummy prompt templates exist for this example to run
    template_dir = Path("templates")
    template_dir.mkdir(exist_ok=True)
    (template_dir / "tool_decider_prompt.j2").write_text("Question: {{ question }}\nTools: {{ tools }}")
    (template_dir / "synthesis_prompt.j2").write_text("Based on this tool result: {{ tool_result }}, answer the question: {{ question }}")
    test_inputs = {"user_input": "What is the weather like in New York City today?", "user_id": "test_user_123"}
    pm = ProtocolManager(protocol=PROTOCOLS.MCP.value)
    final_results = pm.run(test_inputs)
    print("\n--- MCP Protocol Final Result ---")
    print(json.dumps(final_results.get("generate_final_answer"), indent=2))