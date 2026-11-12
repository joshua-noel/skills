# Visual Edit in OMP

This file is not part of the upstream skill. It adds the OMP-specific steps; read it together with `SKILL.md`.

Node/npm and the local Agent-Native bridge are required. The bridge CLI is fetched on demand with `npx @agent-native/core@latest` (version `0.198.7` was checked). Authentication, local-network permission, sharing and folder-write consent are not preapproved.

1. Read `xd://eval/browser`, then open a headed tab at `https://design.agent-native.com/visual-edit`.
2. List page tools with `tab.webmcpList()` and call the exact authorized tool with `tab.webmcpInvoke()`. A page evaluator is a fallback and runs in the main page world. No hosted MCP connector is needed.
3. Start only the target dev app and the local bridge, never a local Design server, and leave servers you did not start alone.
4. Do not bypass login, local-network permission prompts or write consent. Do not upload private app data, expose bridge tokens, or open a live local-app connection without the user's authorization.
5. Apply source changes only when authorized, verify them, and acknowledge the exact pending revision after applying, never before.
