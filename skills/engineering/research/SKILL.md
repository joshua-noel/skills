---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched or authoritative docs and API facts gathered.
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

Investigate the question in the current task. The workflow coordinator may assign this skill as a bounded research workstream, but this skill does not create or dispatch other agents.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
