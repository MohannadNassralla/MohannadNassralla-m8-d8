"""Module 8 — Core Skills Drill: RAG Basics.

Three operational primitives for RAG: embed a sentence, verify a Weaviate
connection, ingest a small set of objects with externally-supplied vectors.

Submit by branching `drill-8-rag-basics`, opening a PR, pasting the PR URL
into TalentLMS → Module 8 → Core Skills Drill.
"""

import numpy as np
import weaviate
from sentence_transformers import SentenceTransformer

# Module-level global variable to cache the model across function calls
_MODEL_CACHE = None


def embed_text(text: str) -> np.ndarray:
    """Return a 384-dim float32 numpy vector for the input string.

    Use sentence-transformers' all-MiniLM-L6-v2.

    Hint:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        v = model.encode(text, convert_to_numpy=True).astype(np.float32)
    """
    global _MODEL_CACHE
    
    # Load the model only once to keep executions fast
    if _MODEL_CACHE is None:
        _MODEL_CACHE = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Generate the embeddings
    embedding = _MODEL_CACHE.encode(text, convert_to_numpy=True)
    
    # Ensure strict adherence to float32 data type and correct 1D shape (384,)
    return embedding.astype(np.float32)


def weaviate_ready(url: str) -> bool:
    """Return True if Weaviate at `url` is reachable and ready, else False.

    Wrap in try/except so a non-running Weaviate returns False rather than
    raising a connection error.
    """
    try:
        client = weaviate.Client(url)
        return client.is_ready()
    except Exception:
        # Prevent CI/CD workflows from crashing if the instance is completely offline
        return False


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
    # 1. Schema check: Create the target class if it is absent
    schema = client.schema.get()
    existing_classes = [c["class"] for c in schema.get("classes", [])]
    
    if class_name not in existing_classes:
        class_schema = {
            "class": class_name,
            "vectorizer": "none",  # External vectors provided manually
            "properties": [
                {
                    "name": "title",
                    "dataType": ["text"]
                },
                {
                    "name": "text",
                    "dataType": ["text"],
                    "indexSearchable": True  # Explicitly enables BM25 indexing
                }
            ]
        }
        client.schema.create_class(class_schema)

    # 2. Batch configuration and object ingestion
    client.batch.configure(batch_size=100, dynamic=False)
    
    with client.batch as batch:
        for item in items:
            data_object = {
                "title": item["title"],
                "text": item["text"]
            }
            
            # Ensure the vector is passed as a JSON-serializable list, not a NumPy array
            vector = item["vector"]
            if isinstance(vector, np.ndarray):
                vector = vector.tolist()
                
            batch.add_data_object(
                data_object=data_object,
                class_name=class_name,
                vector=vector
            )
            
    # 3. Explicitly flush to make sure all background batched operations are completed
    client.batch.flush()

    # 4. Query aggregate meta-count from Weaviate and return it safely as an integer
    result = client.query.aggregate(class_name).with_meta_count().do()
    
    try:
        # Weaviate automatically forces structural capitalization on class names.
        # This dynamic key lookup bypasses any casing discrepancies completely.
        aggregate_data = result["data"]["Aggregate"]
        actual_class_key = list(aggregate_data.keys())[0]
        
        count = aggregate_data[actual_class_key][0]["meta"]["count"]
        return int(count)
    except (KeyError, IndexError, TypeError, AttributeError):
        return 0