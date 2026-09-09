---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
license: MIT
metadata:
  category: engineering
  origin: "mattpocock/skills"
  revision: "original-snapshot"
---

Implement the work described by the user in the spec or tickets.

Read the scoped specification, applicable repository guidance, and current implementation before editing. Keep the change within the approved acceptance criteria and use the project's existing interfaces and commands.

Use `$tdd` when the request calls for test-first work or when a regression test is the clearest way to pin down behavior. Choose seams from the public behavior that the ticket names; record any newly discovered regression test with the coordinator when it changes the agreed validation surface.

Run focused type checks, linters, and tests as the change develops. Broaden validation when the affected surface or repository conventions justify it; do not impose a full-suite run when a narrower check gives sufficient evidence.

Return the changed behavior, validation evidence, unresolved risks, and follow-up suggestions to the workflow coordinator. The coordinator owns dispatch, review scheduling, budget decisions, commits, and publication.
