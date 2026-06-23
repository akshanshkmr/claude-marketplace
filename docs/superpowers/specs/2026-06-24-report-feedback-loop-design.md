# Report Feedback Loop — Design

**Date:** 2026-06-24
**Component:** `plugins/jmir-copyediting/scripts/report.py` (generated HTML report)
**Status:** Approved (design), pending implementation plan

## Problem

The interactive copyedit report (`report.py`) is the surface a human editor drives
to review the skill's edits. Today it has a "Copy insights" button that only copies
edit counts + author queries to the clipboard. There is no way for the editor to
record where the skill **missed** an edit, made a **wrong** edit, or could have done
**better** — i.e. no feedback loop back into continuous skill improvement.

This feature lets an editor select any text in the rendered manuscript, tag it with a
category and a note, and export all such feedback as a structured JSON file that can
be fed back to improve the skill's rules.

## Constraints

- The report is a **single, self-contained static HTML file**. No backend, no auth,
  no network calls. Everything runs client-side; persistence is `localStorage`.
- Must not disturb the existing three views (Original / Diff / Final), the diff DOM,
  or the existing sidebar panes (Queries / Rules applied).
- Degrade gracefully where `localStorage` is unavailable (sandboxed iframe), exactly
  as the current script already does.

## User flow

1. Editor selects text inside the manuscript (`#paper`).
2. On `mouseup` with a non-empty selection, a floating **➕ Add feedback** pill
   appears near the selection.
3. Clicking the pill opens a small popover:
   - **Category** chips (single-select): Missed edit · Wrong edit · Better suggestion · General note
   - **Suggested replacement** — optional text input (most relevant for *wrong edit* / *better suggestion*)
   - **Note** — textarea
   - **Save** / **Cancel**
4. On Save the item is persisted, the floating pill + popover dismiss, the selection
   clears, and the new item appears in the **Feedback** sidebar tab.

## Data model

Each feedback item:

```json
{
  "id": "fb-1719000000000-a3f",
  "category": "missed-edit",
  "selectedText": "kg.m-2",
  "paraIndex": 17,
  "section": "Abstract",
  "context": "…Mean BMI was 27.4 kg.m-2.…",
  "linkedEdit": {
    "eid": "e12", "ruleId": "swap.cohen", "tagType": "eponym",
    "original": "Cohen's d", "suggestion": "Cohen d", "mode": "auto"
  },
  "suggestedReplacement": "kg/m²",
  "note": "rule missed the dot-separated unit",
  "created": "2026-06-24T00:00:00.000Z"
}
```

- `category` ∈ `missed-edit` | `wrong-edit` | `better-suggestion` | `general-note`.
- `paraIndex` / `section` come from `data-pidx` / `data-section` attributes that the
  Python renderer will add to each rendered paragraph block.
- `context` = up to ~120 chars on each side of the selection within the paragraph.
- `linkedEdit` is auto-filled when the selection overlaps an existing `.edit-block`
  (read its `data-eid`, `data-tag-type`, `data-mode`, and the edit's rule/original/
  suggestion). `null` when the selection touches no edit (the common case for
  *missed edit*). This is what maps "wrong edit" feedback straight to a `rule_id`.
- For selections spanning multiple paragraphs: full text is captured via
  `selection.toString()`, and `paraIndex`/`section` are taken from the **first**
  paragraph (anchor). No multi-paragraph merge logic (YAGNI).

## Storage

- `localStorage` key: `${KEY}:feedback`, where `KEY` is the existing `window.__MSID__`
  (per-manuscript), reusing the same `load`/`save` helpers and degrade-on-failure
  behaviour already in the script.
- State shape: an array of feedback items.

## Sidebar

- Add a third pane/tab **Feedback** beside the existing *Queries* and *Rules applied*
  tabs (`.st-btn` / `.side-sec[data-pane]` pattern).
- Show a live feedback count.
- Each row renders: category chip (colour-coded), selected-text snippet, optional
  suggested replacement, the note, and a 🗑 delete control.
- Clicking a row scrolls to the source paragraph (`[data-pidx="…"]`) and flashes it
  (reuse the existing `.flash` animation).
- No persistent inline highlight marks — they would fight the diff DOM and break on
  offset shifts. Scroll-and-flash only.

## Export (repurposed "Copy insights")

- The topbar `#copyInsights` button is repurposed to **Export feedback**.
- Action: build a JSON object and download it via a `Blob` + temporary
  `<a download="…">` (filename derived from `__MSID__`). The existing
  counts+queries summary is folded into the export so nothing is lost.

```json
{
  "schema": "jmir-feedback.v1",
  "title": "…",
  "manuscript": "…",
  "exportedAt": "2026-06-24T00:00:00.000Z",
  "summary": { "autoApplied": 32, "queries": 30, "queryList": [ "Q1 …", "Q2 …" ] },
  "feedback": [ { "…": "item" } ]
}
```

- This file is the loop: the editor hands it to the skill maintainer or pastes it
  into a new Claude session to propose rule changes.

## Renderer changes (Python)

- In `build` / `_render_paragraph`, emit `data-pidx="<paragraph index>"` and
  `data-section="<nearest heading>"` on each rendered block (`<p>`, `<h1>`, `<h2>`…).
  The paragraph index is the original manuscript paragraph index already tracked in
  `build`; the section is the `section` variable already maintained there.
- All other behaviour (edit spans, classification, view toggles) is unchanged.

## Non-goals (YAGNI)

- No backend, no auth, no auto-submission, no GitHub-issue integration.
- No persistent inline highlight marks for saved feedback.
- No editing of an existing feedback item (delete + re-add instead).
- No multi-paragraph anchor reconciliation.

## Testing

- Generate a report from the existing dummy manuscript; verify:
  - Selecting text shows the pill; saving creates a sidebar item and persists across
    reload.
  - A selection overlapping an auto edit (e.g. "Cohen's d") fills `linkedEdit`.
  - A selection on un-edited text yields `linkedEdit: null`.
  - Export downloads valid JSON matching `jmir-feedback.v1` with summary + feedback.
  - Delete removes the item and updates the count/storage.
  - Existing views, queries, rules, zoom, and resolve-progress still work.
- Re-run `report.py` end-to-end to confirm no Python regressions and valid HTML.
```
