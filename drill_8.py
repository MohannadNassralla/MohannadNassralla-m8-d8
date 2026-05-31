"""Module 8 — Core Skills Drill: RAG Basics.

Three operational primitives for RAG: embed a sentence, verify a Weaviate
connection, ingest a small set of objects with externally-supplied vectors.

Submit by branching `drill-8-rag-basics`, opening a PR, pasting the PR URL
into TalentLMS → Module 8 → Core Skills Drill.
"""

import numpy as np
import weaviate


def embed_text(text: str) -> np.ndarray:
    """Return a 384-dim float32 numpy vector for the input string.

    Use sentence-transformers' all-MiniLM-L6-v2.

    Hint:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        v = model.encode(text, convert_to_numpy=True).astype(np.float32)
    """
    # TODO: load all-MiniLM-L6-v2 (consider loading once at module level for speed)
    # TODO: encode the text and return as float32 numpy array of shape (384,)
    raise NotImplementedError("embed_text is not yet implemented")


def weaviate_ready(url: str) -> bool:
    """Return True if Weaviate at `url` is reachable and ready, else False.

    Wrap in try/except so a non-running Weaviate returns False rather than
    raising a connection error.
    """
    # TODO: try weaviate.Client(url).is_ready(); return False on any exception
    raise NotImplementedError("weaviate_ready is not yet implemented")


def ingest_corpus(client: weaviate.Client, class_name: str, items: list[dict]) -> int:
    """Ingest items into the named class. Return the count of ingested objects.

    Each item is {"title": str, "text": str, "vector": list[float]}.

    If the class does not exist, create it with:
      - properties: title (text), text (text, BM25-indexed)
      - vectorizer: "none"

    Use client.batch (or with client.batch as batch:) and remember to flush.
    Verify the count via:
      client.query.aggregate(class_name).with_meta_count().do()
    """
    # TODO: if class_name not in client.schema, create it (vectorizer "none")
    # TODO: batch-add each item with vector=item["vector"]
    # TODO: flush the batch
    # TODO: query the aggregate count and return it
    raise NotImplementedError("ingest_corpus is not yet implemented")
