from minillm.orchestrator import SimpleOrchestrator


def test_orchestrator_runs():
    orch = SimpleOrchestrator()

    def node_a():
        return "a"

    def node_b(node_a):
        return node_a + "b"

    orch.add_node("a", node_a)
    orch.add_node("b", node_b)
    orch.add_edge("a", "b")

    out = orch.run({})
    assert out["b"] == "ab"
