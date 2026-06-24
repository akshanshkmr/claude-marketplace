---
name: study-notes-pdf
description: >-
  Generate polished, modern, colourful "Notion / Linear"-style PDF study notes
  for ANY subject from source material (lecture slides, textbook chapters,
  handouts, syllabi, past papers, or the user's own rough notes). Use this
  skill whenever the user asks for revision notes, exam-prep notes, a study
  guide, "detailed notes", a cheat sheet, or a summary PDF of course material —
  even if they don't say the word "PDF". Also use it when the user uploads
  lecture/course files and asks to "make notes", "summarise for the exam",
  "create a study guide", or "turn this into notes". Covers any discipline:
  CS/AI, engineering, sciences, maths, medicine, law, business, humanities.
  The output is a multi-page PDF with a designed cover, per-topic colour-coded
  chapters, airy tables, formula cards, callouts, worked numericals and
  practice problems.
---

# Study-Notes PDF

Produce exam-ready study notes as a beautifully designed PDF. The visual design
system is pre-built in `assets/notes_design.py` — you only supply **content**.
Your job is to read the source material, decide the structure, then write a
short Python script that pours that content into the design library.

## Workflow

### 1. Gather the source material
Source files usually arrive as uploads at `/mnt/user-data/uploads/`. If a file's
content is not already in context, read `/mnt/skills/public/file-reading/SKILL.md`
to choose the right tool per type (PDFs → `pdftotext` / `pdf-reading` skill;
slides → `extract-text`; archives → `unzip -l` then extract only what you need).
Read **all** the relevant material before writing anything — slides, handouts,
syllabus, and especially any **sample/past papers**, which reveal the exam format
and question style.

If the user gives a subject but no files, you may write notes from your own
knowledge — but say so, and prefer their material when present.

### 2. Plan the structure (do this before coding)
Decide the chapters/modules (typically 3–8), each mapped to one accent theme.
A strong set of notes is not just a summary — it is built for an exam. Include:

- **A cover** with the subject title, exam facts (duration, marks, format), and
  a "what's inside" roadmap of the modules.
- **A high-yield / exam-probability map** near the front when past papers or a
  syllabus are available — rank topics by likelihood of appearing and what to
  focus on. This is one of the most valued parts of good revision notes.
- **One chapter per major topic**, each with concise explanations, comparison
  tables, definition lists, and formula cards.
- **Solved numericals** — fully worked, step-by-step examples that mirror the
  exam's question style. Trace tables with a highlighted final-answer row work
  well. Derive these from sample papers when available.
- **Practice problems** with model answers.
- **A quick-reference / cheat-sheet** at the end: key formulas, common traps,
  and an exam-day checklist.

Keep explanations dense and high-yield. Mark must-know topics with gold stars
via `stars(3)` → ★★★ in section/table titles.

**Accuracy rule:** notes are useless if wrong. Only state facts supported by the
source material or that you are confident are correct. If a worked example needs
data the source doesn't give (e.g. a specific grid or graph in a sample paper you
can't fully read), either reconstruct a representative example and say so, or ask
the user — do not invent specifics and present them as the paper's.

### 3. Write the build script
Copy the design library into your working directory and import it:

```bash
mkdir -p /home/claude/build
cp /path/to/skill/assets/notes_design.py /home/claude/build/
```

Then write `/home/claude/build/make_notes.py`. **Read
`references/build_guide.md` for the full API and a complete worked template.**
The essential shape is:

```python
import sys; sys.path.insert(0, '/home/claude/build')
from notes_design import StudyNotes, stars

nb = StudyNotes()
nb.cover(kicker=..., title_lines=[...], subtitle=..., facts=[...],
         roadmap=[...], footnote=...)
nb.page_break()

nb.chapter("01", "Topic Title", "KICKER", "subtitle", theme="indigo")
nb.section("1.1", "Subsection " + stars(3))    # ★★★ high-yield marker
nb.text("...")
nb.table([...headers...], [[...row...]], [w1, w2, ...])
nb.callout("Exam tip", "...")
# ... more chapters, numericals, practice, reference ...

nb.save("/mnt/user-data/outputs/<Subject>_Notes.pdf", subject="Subject · Code")
```

### 4. Render, review, iterate
Always **look at the output before delivering**. Render pages to PNG and view
them to catch overflow, wrapping, or empty pages:

```bash
cd /home/claude/build && python make_notes.py
pdftoppm -png -r 90 /mnt/user-data/outputs/<Subject>_Notes.pdf /tmp/pg
# then view a few /tmp/pg-*.png
```

Common fixes: a header word wrapping (rename it shorter, e.g. "Step" → "#", or
widen its column); a table running past the margin (column widths must sum to
about `nb.W`); a near-empty page (acceptable before a `page_break()`).

### 5. Deliver
`present_files` the final PDF with a brief summary of what's inside. Flag any
worked examples you reconstructed or assumptions you made.

## Design principles baked into the library (don't fight them)
- One **accent colour per chapter** (indigo, blue, cyan, emerald, amber, rose);
  numericals use violet, practice pink, reference slate. This colour-coding helps
  the reader navigate — keep it consistent.
- **Airy, minimal tables** (tinted header, hairline rows) — never heavy grids.
- **Soft rounded cards** for callouts and formulas.
- Use the `nb.numerical(...)` and `nb.practice(...)` composites for those
  recurring blocks rather than hand-building them.
- For maths, use ReportLab markup — `<sub>x</sub>`, `<super>2</super>`, and
  Unicode Greek/symbols (α β τ Σ √ ≤ ≥ → ∞). Never paste Unicode subscript
  digits; they render as boxes.

## Environment notes
- Requires `reportlab` (`pip install reportlab --break-system-packages` if
  missing) and the DejaVu fonts (standard on Linux images). The library degrades
  gracefully if a font weight is missing.
- The library file is `assets/notes_design.py`. The full API and a complete,
  copy-pasteable example live in `references/build_guide.md` — read it before
  writing the build script.
