# src/minillm/stateful_orchestrator.py

from typing import Dict, Any, Callable, List, Optional, Tuple, Type
from .governance import GovernanceManager
import inspect

# --- Custom Exceptions for Robust Error Handling ---

class OrchestratorError(Exception):
    """Base exception for all stateful orchestrator errors."""
    pass

class NodeNotFoundError(OrchestratorError):
    """Raised when a node name is not found in the graph."""
    def __init__(self, node_name: str):
        self.node_name = node_name
        super().__init__("Node '{}' not found in the graph.".format(node_name))

class EdgeRegistrationError(OrchestratorError):
    """Raised during an invalid attempt to register an edge."""
    def __init__(self, node_name: str, message: str):
        self.node_name = node_name
        super().__init__("{}: '{}'".format(message, node_name))

class StateValidationError(OrchestratorError):
    """Raised when the state does not conform to the defined schema."""
    def __init__(self, message: str):
        super().__init__(message)

# --- Stateful Orchestrator Class ---

class StatefulOrchestrator:
    """
    An orchestrator that manages a central state object, allowing for complex,
    cyclical, and conditional workflows with integrated governance, human-in-the-loop
    interrupts, and optional state schema validation.
    """

    def __init__(self, entry_node: str, state_schema: Optional[Dict[str, Type]] = None):
        """
        Initializes the stateful orchestrator.

        Args:
            entry_node (str): The name of the first node to execute in the graph.
            state_schema (Optional[Dict[str, Type]]): An optional schema defining
                expected keys and their Python types in the state object.
        """
        if not isinstance(entry_node, str) or not entry_node:
            raise ValueError("entry_node must be a non-empty string.")

        self.nodes: Dict[str, Callable[[Dict], Dict]] = {}
        self.edges: Dict[str, Callable[[Dict], str]] = {}
        self.entry_node = entry_node
        self.state_schema = state_schema
        self.gov = GovernanceManager()

    def add_node(self, name: str, func: Callable[[Dict], Dict]):
        self.nodes[name] = func

    def add_edge(self, src: str, dest: str):
        if src not in self.nodes:
            raise EdgeRegistrationError(src, "Source node for edge is not registered")
        if dest not in self.nodes and dest not in ("__end__", "__interrupt__"):
             raise EdgeRegistrationError(dest, "Destination node for edge is not registered")
        self.edges[src] = lambda state: dest

    def add_conditional_edge(self, src: str, path_func: Callable[[Dict], str]):
        if src not in self.nodes:
            raise EdgeRegistrationError(src, "Source node for conditional edge is not registered")
        self.edges[src] = path_func
        
    def _validate_state(self, state: Dict[str, Any], keys_to_check: List[str]):
        """Validates a subset of the state against the schema if it exists."""
        if not self.state_schema:
            return

        for key in keys_to_check:
            if key not in self.state_schema:
                raise StateValidationError("Key '{}' in state is not defined in the schema.".format(key))
            if key in state and not isinstance(state[key], self.state_schema[key]):
                expected_type = self.state_schema[key].__name__
                actual_type = type(state[key]).__name__
                msg = "Type mismatch for key '{}'. Expected '{}', got '{}'.".format(key, expected_type, actual_type)
                raise StateValidationError(msg)

    def run(self, inputs: Dict[str, Any], user_id: str = "system", max_steps: int = 15) -> Tuple[str, Dict[str, Any]]:
        """
        Executes the graph starting from the entry node.

        Returns:
            A tuple containing the final status ('completed', 'paused', 'error')
            and the final state of the graph.
        """
        state = inputs.copy()
        self._validate_state(state, list(state.keys()))
        self.gov.audit(user_id, "stateful_run_start", "StatefulOrchestrator", {"initial_keys": list(state.keys())})

        return self._execute_from(self.entry_node, state, user_id, max_steps)

    def resume(self, state: Dict[str, Any], human_input: Dict[str, Any], user_id: str = "system", max_steps: int = 15) -> Tuple[str, Dict[str, Any]]:
        """
        Resumes execution of a paused graph.
        """
        if "__next_node__" not in state:
            raise OrchestratorError("Cannot resume. The provided state is not a valid paused state.")

        next_node = state.pop("__next_node__")
        state.update(human_input)
        
        self.gov.audit(user_id, "graph_resume", "StatefulOrchestrator", {"resuming_at_node": next_node, "human_input_keys": list(human_input.keys())})
        self._validate_state(state, list(human_input.keys()))
        
        return self._execute_from(next_node, state, user_id, max_steps, start_step=state.get('__step__', 0))

    def _execute_from(self, start_node: str, state: Dict[str, Any], user_id: str, max_steps: int, start_step: int = 0) -> Tuple[str, Dict[str, Any]]:
        current_node_name = start_node
        
        for step in range(start_step, max_steps):
            if current_node_name == "__end__":
                self.gov.audit(user_id, "graph_end_reached", "StatefulOrchestrator", {"step": step})
                return "completed", state

            if current_node_name == "__interrupt__":
                self.gov.audit(user_id, "graph_interrupt_human_input", "StatefulOrchestrator", {"step": step})
                if state['__previous_node__'] in self.edges:
                    state["__next_node__"] = self.edges[state['__previous_node__']](state)
                    state["__step__"] = step
                return "paused", state
                
            if current_node_name not in self.nodes:
                raise NodeNotFoundError(current_node_name)

            self.gov.audit(user_id, "node_start", current_node_name, {"step": step})
            node_func = self.nodes[current_node_name]
            
            try:
                updates = node_func(state)
                self._validate_state(updates, list(updates.keys()))

                for key, value in updates.items():
                    record_to_tag = value if isinstance(value, dict) else {'value': value}
                    tagged_record = self.gov.tag_lineage(record_to_tag, source=current_node_name)
                    state[key] = tagged_record.get('value', tagged_record)

                self.gov.audit(user_id, "node_end", current_node_name, {"step": step, "updated_keys": list(updates.keys())})
            except Exception as e:
                self.gov.audit(user_id, "node_error", current_node_name, {"step": step, "error": str(e)})
                raise
            
            if current_node_name not in self.edges:
                self.gov.audit(user_id, "graph_path_end", "StatefulOrchestrator", {"last_node": current_node_name})
                return "completed", state

            path_func = self.edges[current_node_name]
            state["__previous_node__"] = current_node_name
            next_node_name = path_func(state)

            self.gov.audit(user_id, "conditional_edge_traversed", current_node_name, {"destination": next_node_name})
            current_node_name = next_node_name
        else:
             self.gov.audit(user_id, "max_steps_reached", "StatefulOrchestrator", {"max_steps": max_steps})
             return "max_steps_reached", state

        return "completed", state