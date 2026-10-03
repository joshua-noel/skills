---
name: visualize-webpage
description: Explain a codebase, function, project domain, architecture or whole project as one self-contained interactive HTML page. Use when the user asks for output "in HTML", an "interactive page", a "webpage", an "explorable" explanation, or a walkthrough they can click through. Dark theme unless the user asks for light.
---

# Visualize: webpage

The output is one `.html` file that opens with a double-click. It needs no build step, no CDN and no network. It contains:

1. An interactive diagram that fills the first screen. It comes from the `visualize-diagram` renderer.
2. A step bar to walk through the numbered flow, one step at a time.
3. Sections below the diagram with cards, tabs and expandable details.

## Procedure

1. **Find the facts.** Read the real code and docs first. For a large repo, use a `scout` task. Every part, path and claim on the page must come from the code or docs. Mark a guess as `[INFERENCE]`.
2. **Plan the page.** Decide the one question the page answers. Then choose the sections. A good default:
   - **Overview:** the diagram and the step bar.
   - **Parts:** one card for each box in the diagram, grouped by column.
   - **Flows:** one tab for each important flow, with numbered steps and the files that do each step.
   - **Details:** the decisions, limits and risks a new reader needs. Use `details` so the page stays short.
3. **Make the diagram.** Follow `skill://visualize-diagram` steps 1 to 4. Render to `./.tmp/visuals/<slug>.svg`. Add `--light` only when the user asks for light.
4. **Build the page.**
   - Copy `<skill-root>/assets/page.html` to `./.tmp/visuals/<slug>.html`. `<skill-root>` is the directory of this `SKILL.md`.
   - Replace the `{{...}}` text values and the example sections by hand. Keep, repeat or delete the example sections. Do not touch `{{SVG}}`.
   - Put the diagram in with the script. Do not copy the SVG by hand: it is large and a copy can be cut short.

     ```sh
     node "<skill-root>/scripts/inline.mjs" ./.tmp/visuals/<slug>.html ./.tmp/visuals/<slug>.svg
     ```

     The script prints any `{{...}}` value that is still in the file. Fix each one. Do not use `<img>` or `<object>` for the diagram: the step bar needs the inline SVG.
   - For light, set `data-theme="light"` on `<html>` and render the SVG with `--light`.
   - Write all text at about 80% of ASD-STE100: read `skill://ste-writing`.
5. **Check the result.** Open the page in a browser tab (`xd://eval/browser`). Then:
   - Make sure that the page has no `{{` text and no console errors.
   - Take a screenshot of the first screen. The diagram must fill it without a scroll bar.
   - Select Next in the step bar 2 times. Make sure that the highlighted edges and the step text change.
   - Hover 1 box in the diagram. Make sure that the card shows.
   - Select each tab. Use the arrow keys on the tab list too.
   - Take a screenshot of one content section.
6. **Give the result.** Tell the user the file path and open it with `cmd /c start "" "<path>"` on Windows (`open` on macOS, `xdg-open` on Linux).

## Design rules

- Keep the template's colour tokens. Set a card's `--accent` to the colour of its diagram column: `--a1` is the first column with a group box, `--a2` the next, and so on. Actor columns are grey and use no accent.
- Use interaction only where it helps the reader understand: walk through steps, switch between parallel views, open optional depth. Do not add animation for decoration.
- Keep all code inline. Do not load fonts, scripts or styles from the network.
- Keep the template's accessibility: real buttons, `aria-selected` tabs with arrow keys, a live region for the step text, visible focus, and reduced motion.
- One page answers one question. If the user wants more, make more pages and link them.
