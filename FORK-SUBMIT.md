# Module 8 Drill — Fork-and-Submit Flow

This drill uses a fork-and-submit flow as a one-assignment pilot. The lab,
integration, and stretch assignments for Module 8 use the regular GitHub
Classroom flow.

## 5 steps

1. **Fork this repo** (button top-right) → owner = your personal GitHub
   account → Create fork.
2. **Enable Actions on your fork.** Actions tab → click *"I understand my
   workflows, go ahead and enable them"*. One-time per fork; the autograder
   cannot run on your PR until this is done.
3. **Clone your fork** (not this repo): `git clone https://github.com/<you>/m8-d8.git`
4. **Branch, implement, commit, push:**
   ```bash
   git checkout -b drill-rag-basics
   # edit drill_8.py
   git add drill_8.py
   git commit -m "Drill 8: embed_text, weaviate_ready, ingest_corpus"
   git push origin drill-rag-basics
   ```
5. **Open a PR *within your fork*** — base `main`, compare `drill-rag-basics`,
   **base repository = your fork** (GitHub defaults to upstream — change it).
   When CI passes, paste the PR URL into TalentLMS → Module 8 → Core Skills Drill.

## Common failure modes

- **PR opened against upstream `LevelUp-Applied-AI/m8-d8` instead of your fork.**
  GitHub disables Actions secrets and downgrades the workflow token for
  cross-fork PRs, and TAs will see your work in a flood of cross-cohort
  PRs to the template. Always change the base-repository dropdown to your
  own fork.
- **Actions disabled on the fork.** No green or red CI check on the PR.
  Re-do Setup step 2, then push an empty commit to retrigger:
  `git commit --allow-empty -m "ci: trigger" && git push`.
- **Forgot to start Weaviate locally before running `pytest tests/ -v`.**
  Local tests fail but CI is fine — the autograder workflow brings up its
  own Weaviate service container.
