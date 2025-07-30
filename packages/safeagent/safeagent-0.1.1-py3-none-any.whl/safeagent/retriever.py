import time
import json
import logging
try:
    import numpy as np  # type: ignore
    _NUMPY = True
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs
    _NUMPY = False
    class _NP:
        ndarray = list
        @staticmethod
        def array(x):
            return x

        @staticmethod
        def vstack(xs):
            return xs

        @staticmethod
        def ones(n):
            return [1.0] * n

        class linalg:
            @staticmethod
            def norm(a, axis=None):
                import math
                if axis is None:
                    return math.sqrt(sum(x * x for x in a))
                return [math.sqrt(sum(x[i] ** 2 for x in a)) for i in range(len(a[0]))]

        @staticmethod
        def argsort(a):
            return sorted(range(len(a)), key=lambda i: a[i])

    np = _NP()  # type: ignore
from pathlib import Path
from typing import List, Dict, Any

try:
    import faiss  # type: ignore
    _FAISS = True
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs
    faiss = None  # type: ignore
    _FAISS = False
from .governance import GovernanceManager


RETRIEVER_REGISTRY = {}


def register_retriever(name: str, cls):
    """Register a retriever class for dynamic loading."""
    RETRIEVER_REGISTRY[name] = cls


def get_retriever(name: str):
    return RETRIEVER_REGISTRY[name]

class BaseRetriever:
    """Base interface for retrieval. Requires implementing index and query."""
    def index(self, embeddings: List[Any], metadata: List[Dict[str, Any]]) -> None:
        raise NotImplementedError

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        raise NotImplementedError


class VectorRetriever(BaseRetriever):
    """FAISS-backed vector retriever. Uses an embedding function to map text to vectors, with governance integration."""
    def __init__(self, index_path: str, embed_model_fn):
        """
        Args:
            index_path (str): Filesystem path to store/load FAISS index.
            embed_model_fn (callable): Function that maps text (str) to a numpy ndarray vector.
        """
        self.embed = embed_model_fn
        self.gov = GovernanceManager()
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.next_id = 0
        self.index_path = index_path
        if _FAISS:
            if Path(index_path).exists():
                self._index = faiss.read_index(index_path)
            else:
                self._index = faiss.IndexFlatL2(768)
        else:
            self._index = []  # type: ignore

    def index(self, embeddings: List[np.ndarray], metadata: List[Dict[str, Any]]):
        """
        Add embeddings to the FAISS index and store metadata (with lineage tagging).

        Args:
            embeddings (List[np.ndarray]): List of vectors.
            metadata (List[Dict[str, Any]]): Corresponding metadata dicts (must include 'id').
        """
        if _FAISS:
            vectors = np.vstack(embeddings)
            self._index.add(vectors)
        else:
            for vec in embeddings:
                self._index.append(np.array(vec))
        for vec, meta in zip(embeddings, metadata):
            tagged_meta = self.gov.tag_lineage(meta.copy(), source="vector_index")
            self.metadata_store[self.next_id] = tagged_meta
            self.next_id += 1

        log_entry = {
            "event": "vector_index",
            "count": len(embeddings),
            "timestamp": time.time()
        }
        logging.info(json.dumps(log_entry))
        if _FAISS:
            faiss.write_index(self._index, self.index_path)

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform KNN search on the FAISS index using the embedded query, with encryption and audit.

        Args:
            query_text (str): The query string.
            top_k (int): Number of nearest neighbors to return.

        Returns:
            List[Dict[str, Any]]: Each dict contains 'id', 'score', and 'metadata'.
        """
        # Encrypt and audit query
        encrypted_query = self.gov.encrypt(query_text)
        self.gov.audit(user_id="system", action="vector_query", resource="faiss", metadata={"query_enc": encrypted_query[:50], "top_k": top_k})

        vec = self.embed(query_text)
        if _FAISS:
            distances, indices = self._index.search(np.array([vec]), top_k)
            idx_list = indices[0]
            dist_list = distances[0]
        else:
            if not self._index:
                idx_list, dist_list = [], []
            else:
                def dist(a, b):
                    return sum((ai - bi) ** 2 for ai, bi in zip(a, b)) ** 0.5

                dists = [dist(v, vec) for v in self._index]
                sorted_idx = sorted(range(len(dists)), key=lambda i: dists[i])[:top_k]
                idx_list = sorted_idx
                dist_list = [dists[i] for i in sorted_idx]
        results = []
        for idx, dist in zip(idx_list, dist_list):
            meta = self.metadata_store.get(int(idx), {})
            results.append({"id": int(idx), "score": float(dist), "metadata": meta})

        log_entry = {
            "event": "vector_query",
            "top_k": top_k,
            "timestamp": time.time()
        }
        logging.info(json.dumps(log_entry))
        return results


class GraphRetriever(BaseRetriever):
    """Neo4j-backed GraphRAG retriever using GDS k-NN, with governance integration."""

    def __init__(self, neo4j_uri: str, user: str, password: str, gds_graph_name: str, embed_model_fn):
        """Create the retriever.

        Args:
            neo4j_uri (str): Bolt URI for Neo4j (e.g., 'bolt://localhost:7687').
            user (str): Username for Neo4j.
            password (str): Password for Neo4j.
            gds_graph_name (str): Name of the GDS graph projection in Neo4j.
            embed_model_fn (callable): Function mapping text to an embedding vector.
        """
        from neo4j import GraphDatabase

        self.driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))
        self.gds_graph = gds_graph_name
        self.embed = embed_model_fn
        self.gov = GovernanceManager()

    def index(self, embeddings: List[List[float]], metadata: List[Dict[str, Any]]):
        """
        Ingest each document as a node with a 'vector' property and 'metadata' (with lineage tagging).

        Args:
            embeddings (List[List[float]]): List of embedding vectors.
            metadata (List[Dict[str, Any]]): List of metadata dicts (must include 'id').
        """
        self.gov.audit(user_id="system", action="graph_index", resource="neo4j", metadata={"count": len(embeddings)})
        with self.driver.session() as session:
            for vec, meta in zip(embeddings, metadata):
                tagged_meta = self.gov.tag_lineage(meta.copy(), source="graph_index")
                session.run(
                    "MERGE (d:Document {id: $id}) "
                    "SET d.vector = $vector, d.metadata = $meta",
                    id=meta["id"], vector=vec, meta=tagged_meta
                )
        log_entry = {
            "event": "graph_index",
            "count": len(embeddings),
            "timestamp": time.time()
        }
        logging.info(json.dumps(log_entry))

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Compute embedding for query_text, run GDS K-NN, and return nearest documents (with lineage tagging).

        Args:
            query_text (str): The query string.
            top_k (int): Number of nearest neighbors to return.

        Returns:
            List[Dict[str, Any]]: Each dict contains 'id', 'score', and 'metadata'.
        """
        # Encrypt and audit query
        encrypted_query = self.gov.encrypt(query_text)
        self.gov.audit(user_id="system", action="graph_query", resource="neo4j", metadata={"query_enc": encrypted_query[:50], "top_k": top_k})

        vec = self._compute_embedding(query_text)
        cypher = f"""
            CALL gds.knn.query(
                '{self.gds_graph}',
                $vector,
                {{k: $k}}
            ) YIELD nodeId, similarity
            RETURN gds.util.asNode(nodeId).id AS id, similarity
        """
        results = []
        with self.driver.session() as session:
            for record in session.run(cypher, vector=vec, k=top_k):
                node_id = record["id"]
                score = record["similarity"]
                meta = session.run(
                    "MATCH (d:Document {id: $id}) RETURN d.metadata AS meta", id=node_id
                ).single()["meta"]
                tagged_meta = self.gov.tag_lineage(meta.copy(), source="graph_query")
                results.append({"id": node_id, "score": score, "metadata": tagged_meta})

        log_entry = {
            "event": "graph_query",
            "top_k": top_k,
            "timestamp": time.time()
        }
        logging.info(json.dumps(log_entry))
        return results

    def _compute_embedding(self, text: str) -> List[float]:
        """Return an embedding for ``text`` via the provided embedding function."""
        return self.embed(text)


# Register default retrievers
register_retriever("vector", VectorRetriever)
register_retriever("graph", GraphRetriever)
