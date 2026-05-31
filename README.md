# Module 8 Drill — RAG Basics

Three operational primitives for RAG: embed a sentence, verify a Weaviate
connection, ingest a small set of objects with externally-supplied vectors.

Full assignment instructions are on the **Drill page** in TalentLMS → Module 8
→ Core Skills Drill.

## Setup

1. Bring up Weaviate locally (image already pulled on EID-2):
   ```bash
   docker run -d --name weaviate-drill \
     -p 8080:8080 \
     -e DEFAULT_VECTORIZER_MODULE=none \
     -e ENABLE_MODULES= \
     -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
     semitechnologies/weaviate:1.24.10
   ```

2. If you haven't already installed the M8 packages, complete the install
   from the Reading's "Setup: install before the lecture" section first. Then:
   ```bash
   pip install -r requirements.txt
   ```

3. Implement `drill_8.py` (3 functions: `embed_text`, `weaviate_ready`,
   `ingest_corpus`).

4. Run the autograder locally:
   ```bash
   pytest tests/ -v
   ```

5. Branch `drill-8-rag-basics`, commit, open PR, paste PR URL into TalentLMS.

## Resubmissions

Accepted through Saturday of the assignment week.

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.
