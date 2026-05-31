"""Module 8 Drill autograder — 4 tests per Section C of the build packet."""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import weaviate

from drill_8 import embed_text, ingest_corpus, weaviate_ready

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")


def _wait(url: str, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if weaviate.Client(url).is_ready():
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError(f"Weaviate not ready at {url}")


def test_embed_text_shape_and_dtype():
    v = embed_text("hello world")
    assert isinstance(v, np.ndarray), "embed_text must return a numpy array"
    assert v.shape == (384,), f"expected shape (384,), got {v.shape}"
    assert v.dtype == np.float32, f"expected float32, got {v.dtype}"


def test_weaviate_ready_true_when_up():
    _wait(WEAVIATE_URL)
    assert weaviate_ready(WEAVIATE_URL) is True


def test_weaviate_ready_false_when_down():
    assert weaviate_ready("http://localhost:9999") is False


def test_ingest_corpus_count():
    _wait(WEAVIATE_URL)
    client = weaviate.Client(WEAVIATE_URL)
    class_name = "DrillItem"
    if client.schema.exists(class_name):
        client.schema.delete_class(class_name)
    items = [
        {"title": f"t{i}", "text": f"text body {i}", "vector": [0.01 * i] * 384}
        for i in range(3)
    ]
    count = ingest_corpus(client, class_name, items)
    assert count == 3, f"expected 3 ingested, got {count}"
