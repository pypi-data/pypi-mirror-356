try:
    import numpy as np  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - minimal fallback
    class _NP:
        @staticmethod
        def ones(n):
            return [1.0] * n
    np = _NP()
from minillm.retriever import VectorRetriever


def test_vector_index_query(tmp_path):
    index_path = tmp_path / "faiss.idx"
    retriever = VectorRetriever(index_path=str(index_path), embed_model_fn=lambda t: np.ones(3))
    retriever.index([np.ones(3)], [{"id": 1}])
    results = retriever.query("test", top_k=1)
    assert results[0]["id"] == 0

