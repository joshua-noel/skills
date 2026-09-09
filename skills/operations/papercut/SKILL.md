---
name: papercut
description: Capture concrete Codex workflow friction in the moment and, only when explicitly requested, review the visible conversation for additional papercuts.
metadata:
  short-description: Record workflow friction and review it on demand
---

# Papercut

Use this skill for small, concrete points of friction in a Codex workflow. Keep the three records separate:

- `PAPERCUTS.md` contains one or two sentence observations about a real workflow interruption, wasted retry, confusing instruction, or tool mismatch.
- `LOG.md` contains accomplishments and verified work that was completed.
- The repository's bug tracker (or its established `BUGS.md`) contains confirmed, reproducible product bugs. A papercut is not automatically a bug.

When you experience material friction, record it immediately while the details are fresh. Use the helper beside the loaded SKILL.md with the current repository as --root. The following example is for a project-local skill installation. For a personal installation, replace the helper path with its actual installed path:

```text
python .agents/skills/papercut/scripts/log_papercut.py --root . -m <current-model> "What happened, why it cost time, and the smallest change that would prevent it."
```

The helper preserves the prior `-m <model> <message>` shape as a local Python entry point. It writes only to `PAPERCUTS.md`, serializes concurrent writers, ignores an identical existing observation, and refuses destination symlinks that could escape the selected root. It rejects messages that match a limited set of obvious credential shapes. A rejection does not prove that all secrets are absent, and whitespace sanitization only makes the entry one line; it is not redaction or a safety proof. Review the resulting entry before committing it, and never work around a rejected secret by copying the value elsewhere.

Do not use the helper for an accomplishment or a bug. Add accomplishments to `LOG.md` using the repository's existing format after they are verified. Record a bug only when the behavior is real and reproducible, with enough evidence for someone else to act on it.

## Explicit review

Treat `$papercut` followed by a friction message as a logging request; it must not accidentally start a transcript review. Do not scan or summarize a transcript automatically. Perform a review only when the user gives review intent, such as `$papercut review` or `/papercut retrospective`, and review either the conversation already visible in the current Codex context or a transcript path the user explicitly selected. Do not discover transcript files, upload or fetch them, call an external API, install a package, or request a new secret.

For an explicit review, the coordinator asks one native Codex subagent to return candidate observations using model `gpt-5.6-luna` with reasoning effort `max`. A worker returns the review request or candidates to the coordinator and does not spawn nested agents. The review child is read-only: it returns candidates with the observed friction and relevant evidence, and it does not edit logs. The coordinator filters out accomplishments, speculative issues, duplicates, and anything containing sensitive data, then records only concrete one- or two-sentence candidates through the helper. Report candidates that were rejected and why when that helps the user understand the review.

Keep review output short and actionable. A useful candidate says what the workflow did, where it created friction, and what change would reduce that friction. Do not turn every preference, ordinary tool output, or unconfirmed suspicion into a papercut.
