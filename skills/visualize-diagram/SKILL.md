---
name: visualize-diagram
description: Draw an interactive diagram of a codebase, function, project domain, architecture or whole project as one self-contained SVG file. Use when the user asks for a "diagram", to "draw", "visualize" or "map" something, or asks how parts of a system fit together, what calls what, or how data moves. Dark theme unless the user asks for light.
---

# Visualize: diagram

The output is one `.svg` file. It opens directly in a browser, fills the window, and is interactive:

- Hover or tab to a box to light its path and show a short explanation card.
- Numbered steps show one flow through the system, with a legend.

The bundled renderer does the layout, routing, styling and interaction. You write a JSON spec. Do not hand-write SVG.

## Procedure

1. **Find the facts.** Read the real code and docs first. For a large repo, use a `scout` task. Every box and every arrow must map to a real file, symbol, module, table, service or domain term. Do not invent parts. Mark a guess as `[INFERENCE]` in the box description.
2. **Choose the view.** Use the table below. Draw one question per diagram. If the user asks for more, make more diagrams, not one dense diagram.
3. **Write the spec.** Save it to `./.tmp/visuals/<slug>.json` in the current repo. Use the schema below. Write all text at about 80% of ASD-STE100: read `skill://ste-writing`.
4. **Render.**

   ```sh
   node "<skill-root>/scripts/render.mjs" ./.tmp/visuals/<slug>.json ./.tmp/visuals/<slug>.svg
   ```

   Add `--light` only when the user asks for a light theme. `<skill-root>` is the directory of this `SKILL.md`.
5. **Check the result.** Open the SVG in a browser tab (`xd://eval/browser`). Then:
   - Take a screenshot. Look for overlapping boxes, clipped text and lines that cross many boxes.
   - Hover 2 or 3 boxes. Make sure that the lit path is correct and the card text is complete.
   - Make sure that there are no console errors.
   - If the layout is poor, change the spec (order of columns and nodes), not the SVG.
6. **Give the result.** Tell the user the file path and open it with `cmd /c start "" "<path>"` on Windows (`open` on macOS, `xdg-open` on Linux). For a quick view in chat, you can also give a short ` ```mermaid ` block.

## Choose the view

The renderer puts columns from left to right, with an optional shared row under them. Map the question to columns:

| Question | Columns, left to right | Numbered steps |
|---|---|---|
| How does the system fit together? | users (`actors`), front end, back end or data, workers or external services | One main flow |
| How does data move? | source, each processing stage, sink | The data path |
| What calls what in a function? | entry point, then each call depth | The main call path |
| How do the modules depend on each other? | layers, from the top layer to the lowest | None |
| How is the domain organized? | one column for each bounded context; shared kernel in `shared` | One main use case |
| How does a request run? (sequence) | one column for each participant, in call order | One step for each message |
| How does a lifecycle work? (states) | one column for each phase | One step for each transition |

## Spec schema

```json
{
  "title": "Sunday Market: architecture",
  "source": "commit 1a7cbf6",
  "legendTitle": "CSV import flow",
  "columns": [
    { "actors": true, "nodes": [ { "id": "merchant", "title": "Merchant", "sub": "owner, admin", "desc": "Manages one private catalogue." } ] },
    { "title": "apps/web", "sub": "Next.js 16", "nodes": [ { "id": "web_import", "title": "CSV import service", "sub": "server/csv-import-service.ts", "desc": "Checks the CSV headers and creates an import job." } ] }
  ],
  "shared": { "title": "packages/*", "sub": "shared code", "nodes": [ { "id": "pk_db", "title": "db", "sub": "roles, migrations", "desc": "Postgres client and migration runner." } ] },
  "edges": [ { "from": "merchant", "to": "web_import", "step": 1, "label": "Merchant uploads a CSV file" } ],
  "steps": [ "The merchant uploads a CSV file." ]
}
```

- `columns[]`: required. A column with `"actors": true` has no group box and draws its nodes as ovals. Use it for people and outside callers. Put it first.
- `nodes[]`: `id` (unique), `title` (2 to 4 words), `sub` (the real path, table or symbol), `desc` (1 or 2 sentences for the hover card).
- `shared`: optional. A row under the columns for shared code or libraries. Nodes with no edges dim nothing when hovered.
- `edges[]`: `from`, `to`, `label` (tooltip). An arrow points from the part that acts to the part it acts on. Add `step` (1-based) to put the edge in the numbered flow. Edges without a step are dashed.
- `steps[]`: one sentence for each step number. Each `step` value in `edges` must have text here.
- `theme`: optional, `"light"`. Same as `--light`.

The renderer stops with `spec error: ...` if an edge names a missing node, if a node id repeats, or if a step has no text.

## Layout rules

- Put columns in flow order, so most arrows go from left to right. Arrows from a column on the right into a column on the left are "back" arrows. Workers that write into a database are an example.
- Connect neighbouring columns. An edge that skips a column crosses that column's boxes. To prevent this, change the column order or split the diagram.
- Inside a column, order the nodes to match the order of the nodes that they connect to in the neighbouring columns. This keeps lines from crossing.
- Keep each column to 8 nodes or fewer, and the diagram to about 25 nodes. If there are more, make an overview diagram and one diagram for each area.
- The sheet is 16:9 and fills the window. On other window shapes, the extra space has the background colour.

## Hover rule

When the user hovers a node, the renderer lights:

1. Every edge that touches the node.
2. Forward (left to right) edges, followed downstream.
3. Back (right to left) edges into any node reached in 2, one hop only.
4. Forward edges traced upstream to their origin.

Back edges are never followed further. A node with no edges dims nothing; it only shows its card. If the user asks for a different rule, change `pathThrough` in `scripts/render.mjs` and the list above.

## Pages that embed the diagram

The `visualize-webpage` skill puts the SVG inline in HTML. The SVG element then has 2 methods:

- `svg.highlightStep(n)`: lights the edges of step `n`.
- `svg.clearHighlight()`: removes the highlight.

## Known SVG traps

Check for these if you change the renderer:

- **Filters can hide straight lines.** A filter with default units uses the bounding box of the element. A perfectly horizontal or vertical path has a zero-height (or zero-width) box, so the line disappears. Use `filterUnits="userSpaceOnUse"` with an explicit region.
- **Repeated step numbers.** A step can have more than one edge. Draw the number badge only once, on the first edge of that step.
- **Newlines in attributes.** XML changes a newline inside an attribute value to a space. Use a separator character (the renderer uses `|`) for multi-line text in `data-*` attributes.
- **Lines through labels.** Draw group labels after the edges, on a filled chip, so lines pass behind them.
- **Native tooltips.** A `<title>` inside a node group shows a second, browser tooltip next to the hover card. Use `aria-label` on the group instead.
