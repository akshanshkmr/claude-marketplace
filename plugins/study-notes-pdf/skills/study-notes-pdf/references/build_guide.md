# Build Guide — `notes_design.py` API Reference

Import once, then drive everything through a single `StudyNotes` object. Every
method **appends** styled content to the document in order; call `save()` last.

```python
import sys; sys.path.insert(0, '/home/claude/build')
from notes_design import StudyNotes, stars
nb = StudyNotes()          # A4, sensible margins. nb.W = content width; nb.cm = cm unit
```

## Themes
Nine accent colours, referenced by name:
`indigo · blue · cyan · emerald · amber · rose · violet · pink · slate`

Calling `nb.chapter(..., theme="blue")` sets the **current theme**; subsequent
`section`, `table`, `callout`, `formula`, `kv`, `bullets`, `steps` calls inherit
it unless you pass `theme=` explicitly. Convention: one theme per chapter;
numericals → violet, practice → pink, quick-reference → slate.

## Stars (high-yield markers)
`stars(3)` → `★★★` in gold. Embed in any title string:
```python
nb.section("3.1", "A* Search  " + stars(3))
```

## Cover
```python
nb.cover(
  kicker      = "UNIVERSITY · COURSE-CODE",        # dark pill at top
  title_lines = ["Operating", "Systems"],           # line 1 light, rest bold
  subtitle    = "Final Exam · Complete Study Notes",
  facts       = [("90 MINUTES","indigo"), ("40 MARKS","emerald"), ("OPEN BOOK","amber")],
  roadmap     = [("01","indigo","Processes & Threads","states · scheduling"),
                 ("02","blue","Memory Management","paging · TLB"),
                 ...],                               # 2-col coloured cards; any even/odd count
  footnote    = "Compiled from lecture slides and the textbook.")
nb.page_break()
```

## Structure
```python
nb.chapter("01", "Processes & Threads", "FUNDAMENTALS", "Weeks 1–2", theme="indigo")
nb.section("1.1", "Process States")          # numbered chip + title; current theme
nb.subhead("Computing average waiting time") # small bold colour subheading
nb.block_title("Numerical 1 · …")            # standalone bold title (theme-coloured)
```

## Text & lists
```python
nb.text("Plain justified paragraph. Use <b>bold</b>, <i>italic</i>, Greek α β, → ∞.")
nb.bullets(["First point.", "Second point with <b>emphasis</b>."])
nb.steps(["Do this first.", "Then this.", "Finally this."])   # auto-numbered chips
nb.space(0.6)                                  # vertical gap (multiples of ~3.4mm)
nb.page_break()
```

## Tables (the workhorse)
```python
nb.table(
  ["Algorithm","Preemptive?","Optimises","Weakness"],     # headers
  [["FCFS","No","Simplicity","Convoy effect"],
   ["Round Robin","Yes","Fairness","Quantum tuning"]],    # rows (list of lists)
  [3.0*nb.cm, 2.6*nb.cm, 4.0*nb.cm, nb.W-9.6*nb.cm],       # column widths — MUST sum to ~nb.W
  theme="indigo",                # optional; defaults to current chapter theme
  highlight=[(2,2)],             # optional: tint data-row index ranges (1-based; header is row 0)
  span_rows=[5])                 # optional: merge a row across all cols (final-answer summary)
```
Rules: column widths must sum to about `nb.W` or the table overflows the margin.
Keep header words short — a long header in a narrow column wraps (use "#" not
"Step", "Adm." not "Admissible", etc.). Cell text may contain `<br/>`, `<b>`,
`<sub>`, `<super>`.

## Definition list (label | value)
```python
nb.kv([("g(n)","Exact cost from start to n."),
       ("h(n)","Heuristic estimate to the goal; must be admissible.")],
      3.0*nb.cm)        # first-column width; current theme
```

## Comparison cards (two concepts side by side)
```python
nb.two_col_cards("BLUEPRINT · macro", ["nodes are placeholders", "no real layers"],
                 "MODULE · micro",    ["real layer types", "reusable"], theme="blue")
```

## Formula cards
```python
nb.formula("f(n)  =  g(n)  +  h(n)")                       # large, centred, tinted card
nb.formula("τ<sub>ij</sub>(new) = (1−ρ)·τ<sub>ij</sub>(old) + Δτ<super>k</super>", small=True)
```
Use `<sub>`/`<super>` and Unicode symbols. **Never** use Unicode subscript
digits (₀₁₂) — they render as empty boxes in the built-in fonts.

## Callouts (tinted rounded cards with a coloured dot + label)
```python
nb.callout("Exam tip", "Draw the diagram and label every transition.")
nb.callout("Watch out", ["First gotcha.", "Second gotcha."], theme="rose")  # list ok
```
`items` may be a string, a list of strings, or a list of flowables (you can pass
`nb.text(...)`-style content by building Paragraphs, but strings cover most cases).

## Composite blocks (use these for the recurring patterns)
```python
# Solved worked example: title + Setup callout + optional trace table + Insight callout
nb.numerical(
  "Numerical 1 · Address translation",
  setup   = "Page size = 4 KB, logical address = 8196. Page 2 → frame 2.",
  headers = ["#","Computation","Result"],
  rows    = [["1","8196 ÷ 4096","page 2"],
             ["2","8196 mod 4096","4"],
             ["PHYSICAL ADDRESS = 2×4096 + 4 = 8196","",""]],
  widths  = [1.0*nb.cm, 8.0*nb.cm, nb.W-9.0*nb.cm],
  highlight=[(3,3)], span_rows=[3],
  insight = "The offset is unchanged by translation.")

# Practice problem: title + Question callout + Model-answer callout
nb.practice(
  "Practice · 5 marks — TLB effective access time",
  question = "TLB hit 80%, TLB 10 ns, memory 100 ns. Find EAT.",
  answer   = "0.8×110 + 0.2×210 = 130 ns.")
```

## Save
```python
nb.save("/mnt/user-data/outputs/Subject_Notes.pdf", subject="Subject · Course Code")
```
`subject` appears in the page footer next to the page-number dot.

---

## Complete minimal template
```python
import sys; sys.path.insert(0, '/home/claude/build')
from notes_design import StudyNotes, stars

nb = StudyNotes()

nb.cover(
    kicker="STATE UNIVERSITY · CS-302",
    title_lines=["Operating", "Systems"],
    subtitle="Final Exam · Complete Study Notes",
    facts=[("90 MINUTES","indigo"), ("40 MARKS","emerald"), ("OPEN BOOK","amber")],
    roadmap=[("01","indigo","Processes & Threads","states · scheduling"),
             ("02","blue","Memory Management","paging · TLB · virtual memory")],
    footnote="Compiled from lecture slides and the course textbook.")
nb.page_break()

# Optional high-yield map (great when past papers exist)
nb.chapter("★","High-Yield Topics","EXAM STRATEGY","Where to focus revision","amber")
nb.space(0.8)
nb.table(["Priority","Topic","Focus"],
    [[stars(3)+" 100%","Scheduling","Gantt charts · average wait time"],
     [stars(2)+" 80%","Paging","address translation · TLB EAT"]],
    [2.4*nb.cm, 4.5*nb.cm, nb.W-6.9*nb.cm], theme="rose", highlight=[(1,1)])
nb.page_break()

nb.chapter("01","Processes & Threads","FUNDAMENTALS","Weeks 1–2","indigo")
nb.space(0.6)
nb.section("1.1","Scheduling Algorithms  " + stars(3))
nb.text("The scheduler decides which ready process runs next.")
nb.table(["Algorithm","Preemptive?","Weakness"],
    [["FCFS","No","Convoy effect"],["Round Robin","Yes","Quantum tuning"]],
    [4*nb.cm, 3*nb.cm, nb.W-7*nb.cm])
nb.callout("Exam tip","Always draw the Gantt chart first, then read off waiting times.")
nb.page_break()

nb.chapter("02","Quick Reference","CHEAT SHEET","Formulas & traps","slate")
nb.space(0.6)
nb.section("R1","Key Formulas")
nb.table(["Formula","Used for"],
    [["EAT = h·(t+m) + (1−h)·(t+2m)","TLB effective access time"]],
    [8*nb.cm, nb.W-8*nb.cm], theme="slate")

nb.save("/mnt/user-data/outputs/OS_Notes.pdf", subject="Operating Systems · CS-302")
print("done")
```

## Gotchas checklist (verify by rendering to PNG)
- Column widths sum to ~`nb.W`, or the table spills past the right margin.
- Long header words in narrow columns wrap — shorten them.
- A summary row passed to `span_rows` must have its text in the **first** cell;
  leave the others `""`.
- Unicode subscript digits render as boxes — use `<sub>2</sub>` instead.
- A nearly-empty page is usually a trailing `page_break()` — harmless, or remove it.
