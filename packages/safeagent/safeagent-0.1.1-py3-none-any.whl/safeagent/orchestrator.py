from typing import Dict, Any, Callable, List
from .governance import GovernanceManager

class SimpleOrchestrator:
    """Minimal DAG runner: each node is a function, edges define dependencies, with audit and lineage tagging."""

    def __init__(self):
        # Map node name to function
        self.nodes: Dict[str, Callable[..., Any]] = {}
        # Map node name to list of dependent node names
        self.edges: Dict[str, List[str]] = {}
        self.gov = GovernanceManager()

    def add_node(self, name: str, func: Callable[..., Any]):
        """Register a function under the given node name."""
        self.nodes[name] = func
        self.edges.setdefault(name, [])

    def add_edge(self, src: str, dest: str):
        """Specify that 'dest' depends on 'src'."""
        if src not in self.nodes or dest not in self.nodes:
            raise ValueError(f"Either '{src}' or '{dest}' is not registered as a node.")
        self.edges[src].append(dest)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all nodes in topological order, audit pipeline start/end, and tag lineage on outputs.

        Args:
            inputs (Dict[str, Any]): Global inputs (e.g., 'user_input', 'user_id').

        Returns:
            Dict[str, Any]: Mapping of node name to its return value.
        """
        results: Dict[str, Any] = {}
        visited = set()

        # Audit pipeline start
        self.gov.audit(user_id=inputs.get("user_id", "system"), action="pipeline_start", resource="orchestrator")

        def execute(node: str):
            if node in visited:
                return results.get(node)
            visited.add(node)
            func = self.nodes[node]
            kwargs = {}
            import inspect
            params = inspect.signature(func).parameters
            for name in params:
                if name in results:
                    kwargs[name] = results[name]
                elif name.startswith("node_") and name[5:] in results:
                    kwargs[name] = results[name[5:]]
                elif name in inputs:
                    kwargs[name] = inputs[name]
            output = func(**kwargs)
            # Tag lineage on dict outputs
            if isinstance(output, dict):
                output = self.gov.tag_lineage(output, source=node)
            results[node] = output
            return output

        for node in self.nodes:
            execute(node)

        # Audit pipeline end
        self.gov.audit(user_id=inputs.get("user_id", "system"), action="pipeline_end", resource="orchestrator")

        return results
