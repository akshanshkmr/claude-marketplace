# JMIR Routine Checks — Operational Quick-Reference

This file is the **operational layer** of the skill: the consolidated, do-this-every-time
checklist distilled from a working copyeditor's routine-checks sheet. It is deliberately
terse and action-oriented. For the *reasoning* behind each rule, follow the cross-references
into `house-style.md`, `statistics.md`, `abbreviations.md`, `tables-and-figures.md`, and
`references.md`.

## How this fits with the script

Edits split into two layers, and you should use both:

1. **Deterministic layer → `scripts/mechanical_edits.py`.** Every edit expressible as a
   pattern (word-swaps, US spelling, P-value formatting, eponyms, quotes, trademark symbols,
   noon/midnight) is caught here *exhaustively*. Run it first; a regex never forgets.
   - `python scripts/mechanical_edits.py paper.docx` → human-readable report
   - `… --json out.json` → structured findings for an agent to apply as tracked changes
   - `… --apply fixed.docx` → applies only the `auto`-confidence fixes
   - Findings are tagged `auto` (apply verbatim) or `review` (propose, confirm in context).
2. **Judgement layer → this file + the other references + `query-bank.md`.** Everything the
   regex can only *flag*: whether a context-dependent swap fits, rephrasing, restructuring,
   statistical completeness, and the author queries to raise. The `review` findings from the
   script map directly onto entries in `query-bank.md`.

The point of the split: the script guarantees the boring 100 mechanical edits are never
missed, freeing your attention for the judgement calls that actually need a human.

---

## 1. Document structure & heading levels

Apply these heading **styles and point sizes** (this is the house template):

| Element | Style | Size |
|---|---|---|
| Article title | H1 | 16 |
| Study type label; major sections (Abstract, Introduction, Methods, Results, Discussion, References) | H2 | 14 |
| Subsections (Background, Objective, Overview, Ethical Considerations, Principal Findings, Conclusions, Acknowledgments, Data Availability, Authors' Contributions, Conflicts of Interest, Abbreviations) | H3 | 12 |
| Sub-subsection | H4 | *italic*, 12 |
| Deeper | H5 | 12 |
| Abstract body labels (background/objective/methods/results/conclusions/keywords) | normal | 12 |

Canonical order and nesting (Original Paper):

- **Abstract** (H2) — structure **BOMRCK**: Background, Objective, Methods, Results, Conclusions (+ "Trial Registration" for RCTs), then Keywords
- **Introduction** (H2) → Background (H3)
- **Methods** (H2) → Overview (H3) … **Ethical Considerations must be the *final* subheading of Methods** (H3)
- **Results** (H2) → Overview (H3)
- **Discussion** (H2) → Overview / Principal Findings (H3) … Conclusions (H3)
- **Acknowledgments** (H3; funding, generative-AI use) → **Data Availability** → **Authors' Contributions** → **Conflicts of Interest** (H3, *mandatory*) → **Abbreviations** (H3, *mandatory*)
- **References** (H2)

Routine structural checks: heading levels correct; styles/casing/paragraph spacing consistent;
title case on headings (see `house-style.md` §3); IMRD present and justified for the article type.

## 2. Hard limits

| Item | Limit | If exceeded |
|---|---|---|
| Figures | ≤ 8 | query author |
| Tables | ≤ 5 | move extras to Multimedia Appendix + cite in text (query) |
| Table length | < 3 pages | move long tables to Multimedia Appendix (query) |
| Abstract | ≤ 450 words | reduce ≤50 over yourself; >50 over → query author |
| Title | ≤ 280 characters incl. spaces | revise / query |
| Table subparts (2A, 2B) | not allowed | restructure |
| Figure subparts (A, B, C…) | allowed | ensure each is cited in text |

## 3. Word choice & terminology swaps

`auto` = the script applies it; `ctx` = context-dependent, the script flags it for you to confirm
(usually with a query from `query-bank.md`). Apply the same swap **throughout** the paper.

| Avoid | Use | Mode |
|---|---|---|
| utilize / utilization | use | auto |
| prior to | before | auto |
| firstly / secondly / lastly | first / second / finally | auto |
| healthcare; homecare | health care; home care | auto |
| socio-demographic | sociodemographic | auto |
| wellbeing | well-being | auto |
| towards; amongst; whilst; grey | toward; among; while; gray | auto (US spelling) |
| employ (= use) | use | ctx (keep if "to hire") |
| suffer from | experience / have | ctx |
| subjects | participants / candidates | ctx (not "subject matter") |
| victim | survivor | ctx (violence/disaster) |
| application | app | ctx (software only) |
| elderly / elder | older people / older adults | ctx + query |
| compared to | compared with | ctx (keep "to" only for likening) |
| further, / additionally, / moreover, (connectors) | furthermore, / in addition, | ctx |
| as a result | thus | ctx |
| though (trailing) | however | ctx |
| present study / current study | this study / this paper | ctx |
| manuscript | paper | ctx (**keep in Acknowledgments**) |
| article (= this work) | paper / study | ctx |
| medical professional; health professional | health care professional(s) | ctx |
| relatives | caregivers | ctx + query |
| prior (= earlier) | previous | ctx |
| moderate to severe (exercise) | vigorous | ctx |

### Inclusive / people-first language (`house-style.md` §1, AMA)

- **People-first**: "HIV-infected patients" → "patients infected with HIV"; "diabetic/schizophrenic patients" → "patients with diabetes/schizophrenia"; "ambulatory patients" → "people who are ambulatory".
- Avoid **"normal"/"abnormal"** for a person's health status (query) — note this is fine for "normal distribution".
- **Sex** = male/female; **gender** = man/woman / men/women.
- Country wording: avoid "first-world/third-world" and "developed/developing"; prefer "low-income, middle-income, resource-limited, resource-poor, transitional" (query).

## 4. Neologisms, abbreviations & dimensional terms

- **eHealth, mHealth, eSource** (never e-health, e-Health, m-health, m-Health, e-source). Same camelCase for other *x*Health neologisms. `auto`
- **SMS by location**: titles/headings → "text messaging" / "texting"; abstract → "SMS text messaging"; body → "SMS text messaging" (first) then "texting"/"SMS text messaging". `ctx`
- Dimensional terms with numerals → numeral + D: "three-dimensional" → "3D", "four-dimensional" → "4D". `ctx`
- Abbreviations: expand at first use **only if used ≥3 times**; otherwise spell out. No author-invented or one-word abbreviations. Full rules and the no-expansion list → `abbreviations.md`.

## 5. Punctuation, hyphenation & symbols

- Straight quotes/apostrophes → **curly** ("abc" → "abc"; ' → '). `auto`
- Remove **® ™ ℠** trademark symbols. `auto`
- **&** → "and" (except established names/abbreviations). `ctx`
- **and/or** → choose "and" or "or". `ctx`
- **Solidus "/"** must not mean "and"/"or" (but "race/ethnicity", dates, units, URLs are fine).
- **En dash for compound modifiers** attached to open compounds: "mobile phone–based app" (NOT "mobile phone-based app"). See `house-style.md` §8.4. `ctx`
- **Hyphenate these compounds when attributive** (`ctx`): quality-of-life, standard-of-care, intention-to-treat (ITT), proof-of-concept, one-size-fits-all, face-to-face, step-by-step, day-to-day, around-the-clock, gain-of-function, loss-of-function, before-and-after study, one-on-one.
- Numeral + unit modifiers: "3 year-period" → "3-year period". `ctx`
- "pre and post" → "pre- and poststudy"; "pre- and post-study analysis"; "pre- and post-intervention".
- "low-income and middle-income countries" → "low- and middle-income countries".

## 6. Numbers, percentages, statistics (see `statistics.md`)

- **P values**: italic *P*; **no leading zero** (P=.03, not P=0.03); **no spaces** around operators; round to 2 decimals, or 3 when P<.01 or when rounding flips significance (eg, P=.048); P<.001 for anything smaller (P<.0001 / P=.0005 → P<.001); P=1 → P≥.99; P=0 → P<.001; give the **exact** P unless P<.001 or P≥.99. `auto` for formatting; `ctx`/query for rounding and exactness.
- **α, β**: no leading zero. Confirm whether "α" means Cronbach α or α level (query).
- **Eponyms, no possessive**: Cronbach α, Cohen d, Fisher exact, Hedges g. `auto`
- **Percentages with counts**: report as `n (%)` in tables; in text put the count first — "(59/100, 59%)"; when the % is emphasized — "59% (59/100)". For N<100 → no decimal place on %; for 100≤N≤1000 → 1 decimal place.
- **Paired statistics**: `mean (SD)`, `median (IQR)`, `OR (95% CI)`, `F test (df)`, `t test (df)`, `χ² (df)`. Query a missing partner (SD for a mean, IQR for a median, 95% CI for an OR/MD/APC/AAPC, df for χ²/t/F). Round χ² to 1 decimal.
- **Standard stat terms are abbreviated**: SD, SE, CI, IQR, OR.
- **Units**: solidus + superscript — "kg/m²" (not "kg.m-2"). Time must carry a unit; confirm AM/PM for bare "12:00".
- **Currency**: "$" → "US $", or give a conversion to US $ / a blanket conversion-rate note (query).

## 7. Phrases & content not permitted

- **Time-bound phrasing** ("ongoing", "currently underway", "to date", "at the time of this writing/publication") — rephrase for a long-term readership.
- **"trending toward significance"** and variants — state the trend, then whether it was statistically significant (give the value).
- **URLs/hyperlinks** in running text and abstract — remove or convert to a reference (the trial-registration URL in the abstract is the one exception).
- **Equations** via the equation editor / complex equations — remove from the running text; they are reinserted at typesetting (query); type simple equations inline.
- **Simple bar graphs / pie charts** as figures — move data into the text or a table (query).
- **Long bulleted/numbered lists** — convert to running text or a textbox where feasible (query).
- **Bold/italic body text** — generally not permitted; query before removing.
- **Footnotes inside figures** — move to the figure legend.
- **Reference citations** in the abstract, in table captions, and inside textbox captions — move to the main text.
- **Morisky / MMAS scales** — require license documentation or removal (query).

## 8. Tables, figures, captions (see `tables-and-figures.md`)

- Empty cells → em dash (—) with a footnote, or N/A for "not applicable" (query if data are missing).
- Footnotes use **alphabetical superscripts** (a, b, c) in order of appearance; **no asterisks** for significance — replace "*"/"**" with "a"/"b".
- Use **check marks (✓)** in tables, not crosses or other symbols.
- A table/figure must appear **immediately after** (never before) its first in-text citation, and within the section where first mentioned; everything is cited in numerical order.
- Define every abbreviation used in a figure **in the figure caption**; captions in sentence case, ending with a period.
- Single-row / single-column tables → fold into running text or convert to a 1×1 textbox.

## 9. Metadata & front matter (see SKILL.md Phase 3)

- Author initials: no periods, no spaces (Bryan George Miller → BGM).
- Degrees: lowest→highest, no punctuation; academic degrees/fellowships only (no certifications, no "Dr" for a doctorate — use PhD).
- Affiliations: one department + one institution each, largest→smallest, title case, no acronyms, no postal codes (except corresponding author).
- ORCIDs mandatory; flag green/orange/red status.
- Keywords: 5–12, semicolons, sentence case, no trailing punctuation; include MeSH terms; if an abbreviation is a keyword, add its expansion; add "mobile phone" if "smartphone" appears; keep one of any singular/plural pair.
- Remove author/affiliation/keyword blocks and hyperlinks from the Word file (they live in the metadata).

