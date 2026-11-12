---
name: demo-bar
description: Quality bar for UI demos, mocks and prototypes shown to the user. Use before sending or presenting any demo, mock, screenshot set, preview link or recorded walkthrough of an interface.
---

# Demo bar

A demo that is not checked wastes the reviewer's time and teaches them to distrust the next one. Do not send a UI demo or mock until all of this is true.

1. **Seen in a real browser.** Use a real engine (Chromium or equivalent), headed or headless with screenshots. A DOM simulator or "the scripts ran" does not count. Click every switch, tab and button on the page and check the result by screenshot.
2. **Realistic data.** Prefer real data that is not sensitive. Never invent items quietly. If real data lacks a case, say so on the page, or build the case from a real example and label it.
3. **Every state shown:** light and dark if the product has both; a wide desktop, a narrow window and a phone width; empty, long text, loading and error wherever the screen has them.
4. **Readability measured** on the rendered pixels, over real backgrounds, not computed from the design tokens. Text 4.5:1, large text and UI parts 3:1. Report the lowest number on the page.
5. **Follows the project's design guidelines** for that area: touch target sizes, input sizes on small screens, use of effects, motion. If none exist, follow the platform's.
6. **Nothing faked in interaction.** A control that does nothing in the mock is visibly marked "mock only".
7. **A "How this was checked" box** at the bottom of the page: what was rendered, at which sizes, the contrast minimum, what is a stand-in, and what was not checked.
8. **You looked at the screenshots yourself** before sending the link. Not a subagent, not a summary.

## Process notes

- Give the user one link or file that opens with a double-click, and the first screen should answer "what am I looking at and what do you want from me?"
- If a check could not be done, say which and why in the "How this was checked" box.
