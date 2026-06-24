# Mechanical Edits — Deterministic Layer (codeless)

This is the **Layer 1** find/replace reference for the Claude for Word add-in, comprising all 139 rules ported from the skill's original terminal scanner. In that version a regex pass applied them; inside the add-in there is no Python runtime, so **you** are the regex: read the open document and apply each rule below, exhaustively, as you scan.

**Disposition map (how each rule lands in Word):**

| Mode | What you do in the add-in |
|------|---------------------------|
| **auto** | Apply as a **tracked change** (deletion of old text + insertion of new). Safe regardless of context. |
| **query** | Do **not** silently change. Insert an anchored **comment** on the text proposing the fix, or apply a tracked change *only* when context clearly confirms it. Most map to a query in `query-bank.md`. |

Always keep Track Changes / suggested-edits mode **on** (see SKILL.md → Runtime). Make the **smallest** edit that fixes the issue — a word swap, not a paragraph rewrite — so the revision is easy to accept.

**Three context guards (do not fire blindly):**
1. **Inside a URL** — do not apply spelling/word-swap/flag rules to text inside a `http(s)://…` span. The URL itself is handled by `flag.url`.
2. **"normal" / "abnormal"** — only flag when it describes a *person's health status*. Skip when it is `normality`, `normalize`, `normalization`, `normally`, `… distribution`, or `lognormal` (statistical usage is fine).
3. **"manuscript"** — the `manuscript → paper` swap is suppressed inside the **Acknowledgments** section ("manuscript" is acceptable there).

> **Policy note (supersedes a rule below):** Per house style updated December 2025, **`and/or` is now retained as is** (SKILL.md Phase 5, item 14). The legacy `flag.andor` rule is kept here for completeness but should **not** be actioned unless local journal guidance says otherwise.

---

## 1. British → American spelling — **auto** (70 rules)

Apply as tracked changes. Case is mirrored (Colour→Color, COLOUR→COLOR). Match on whole words only.

| British | American | | British | American |
|---|---|---|---|---|
| colour | color | | labelling | labeling |
| colours | colors | | labelled | labeled |
| coloured | colored | | travelling | traveling |
| behaviour | behavior | | travelled | traveled |
| behaviours | behaviors | | fulfil | fulfill |
| behavioural | behavioral | | fulfilment | fulfillment |
| favour | favor | | enrol | enroll |
| favours | favors | | enrolment | enrollment |
| favourite | favorite | | towards | toward |
| labour | labor | | amongst | among |
| odour | odor | | whilst | while |
| tumour | tumor | | learnt | learned |
| tumours | tumors | | summarise | summarize |
| organise | organize | | summarised | summarized |
| organised | organized | | recognise | recognize |
| organising | organizing | | recognised | recognized |
| organisation | organization | | prioritise | prioritize |
| organisations | organizations | | prioritised | prioritized |
| analyse | analyze | | utilise | use |
| analysed | analyzed | | utilised | used |
| analysing | analyzing | | utilising | using |
| catalogue | catalog | | centre | center |
| centres | centers | | centred | centered |
| fibre | fiber | | litre | liter |
| litres | liters | | metre | meter |
| metres | meters | | defence | defense |
| offence | offense | | grey | gray |
| greyscale | grayscale | | mould | mold |
| sulphur | sulfur | | oedema | edema |
| foetal | fetal | | foetus | fetus |
| haemoglobin | hemoglobin | | haematology | hematology |
| paediatric | pediatric | | paediatrics | pediatrics |
| anaemia | anemia | | anaemic | anemic |
| ageing | aging | | modelling | modeling |
| modelled | modeled | | | |

*Note:* `dialogue` is **kept** (AMA allows it). `utilise/utilised/utilising` collapse to `use/used/using` — this doubles as a word-swap (see §2).

---

## 2. Word swaps — **auto** (20 rules)

Apply as tracked changes regardless of context.

| Find | Replace | Rationale |
|---|---|---|
| utilize / utilizes / utilized / utilizing / utilization | use / uses / used / using / use | JMIR avoids "utilize/utilization" |
| healthcare | health care | Two words |
| homecare | home care | Two words |
| socio-demographic / socio demographic | sociodemographic | One word, no hyphen |
| wellbeing / well being | well-being | Hyphenated |
| firstly | first | |
| secondly | second | |
| thirdly | third | |
| lastly | finally | |
| prior to | before | |
| e-health / e health | eHealth | JMIR neologism casing |
| m-health / m health | mHealth | JMIR neologism casing |
| e-source / e source | eSource | JMIR neologism casing |
| Cronbach's alpha / Cronbach's α | Cronbach α | AMA: no possessive on statistical eponyms |
| Cohen's d | Cohen d | AMA: no possessive on statistical eponyms |
| Fisher's exact | Fisher exact | AMA: no possessive on statistical eponyms |
| Hedges' g | Hedges g | AMA: no possessive on statistical eponyms |
| 12 PM / 12:00 PM / 12 p.m. | noon | |
| 12 AM / 12:00 AM / 12 a.m. | midnight | |
| ® ™ ℠ | *(delete)* | Remove trademark/registered/service-mark symbols; capitalize the initial letter of the term instead |

---

## 3. Word swaps — **query / context-dependent** (23 rules)

Usually correct, but confirm in context. Apply a tracked change only when the meaning is unambiguous; otherwise raise a comment (most have a matching entry in `query-bank.md`).

| Find | Suggest | When to confirm |
|---|---|---|
| employ / employs / employed / employing | use | Keep when it means *to hire* |
| suffer / suffers / suffered / suffering (from) | experience / have | People-first; AMA |
| subjects | participants | **Not** when it means *subject matter* |
| victim / victims | survivor | For those who survive violence/disaster |
| application / applications | app | Only when it means *software* (not a job/method application) |
| elderly | older people / older adults | Query the author |
| compared to | compared with | Keep "compared to" only for *likening*, not differences |
| Further, *(sentence opener)* | Furthermore, | |
| Additionally, | In addition, | |
| Moreover, | Furthermore, / In addition, | |
| as a result | thus | |
| , though | , however | Trailing connector |
| (the) present/current study/paper/work/article | this study / this paper | |
| manuscript / manuscripts | paper | **Keep in Acknowledgments** (guard #3) |
| article / articles | paper / study | When referring to *this* work |
| moderate to severe | vigorous | Exercise-intensity context only |
| relatives | caregivers | If that is the intended meaning |
| medical professional(s) | health care professional(s) | Consistency |
| health professional(s) | health care professional(s) | Consistency |
| [X]-infected patients/people/individuals | patients/people/individuals infected with [X] | People-first (e.g., "HIV-infected patients" → "patients infected with HIV") |
| licence | license | Confirm noun vs verb |
| practise | practice | Confirm noun vs verb |
| programme | program | US spelling |

---

## 4. Statistics — **auto** (3 rules)

| Find | Replace | Rationale |
|---|---|---|
| P = 0.03 / P=0.03 / P < 0.001 (any spacing, optional leading zero) | P=.03 / P<.001 | No leading zero, no spaces around the operator, italic *P* |
| p = 0.04 (lowercase) | P=.04 | Same, and capitalize the *P* |
| α = 0.05 / β = 0.20 | α=.05 / β=.20 | No leading zero, no spaces |

---

## 5. Statistics — **query** (6 rules)

| Find | Suggest | Rationale |
|---|---|---|
| P=.000… (e.g., P=.0004) | P<.001 | Values below .001 are written as P<.001 |
| P=1 / P=1.0 | P≥.99 | |
| trend(ed/ing) toward(s) significance | *(state the trend, then whether it was statistically significant + the value)* | Avoid "trending toward significance" |
| approached significance | *(state significance explicitly)* | |
| kg·m-2 / kg.m2 | kg/m² | Solidus + superscript 2 |
| "3 year-period" / "5 day-interval" | "3-year period" / "5-day interval" | Hyphenate the modifier, not the noun |

---

## 6. Phrase flags — **query** (6 rules)

| Find | Suggest / action | Rationale |
|---|---|---|
| and/or | choose "and" *or* "or" | **DO NOT ACTION** — retained as of Dec 2025 (see policy note above) |
| http(s)://… in running text or abstract | move to a reference (RefCheck) or remove | URLs not allowed in body/abstract (exception: trial-registration URL) |
| SMS *(standing alone)* | "SMS text messaging" (abstract) / "text messaging" (title) | |
| ongoing / currently underway / to date / at the time of (this) writing/publication | rephrase for a long-term readership | Time-bound phrasing |
| normal / abnormal *(of a person's health status)* | describe specifically | AMA; **see guard #2** — skip statistical usage |
| $<number> *(no currency qualifier)* | US $ … or give the conversion rate | Specify currency |

---

## 7. Hyphenation of attributive compounds — **query** (11 rules)

Hyphenate **only when used before a noun** (attributively). Leave unhyphenated when used predicatively (e.g., "measured quality of life" stays open; "quality-of-life measure" gets hyphens).

quality of life → quality-of-life · standard of care → standard-of-care · intention to treat → intention-to-treat · proof of concept → proof-of-concept · one size fits all → one-size-fits-all · face to face → face-to-face · step by step → step-by-step · day to day → day-to-day · around the clock → around-the-clock · gain of function → gain-of-function · loss of function → loss-of-function

---

## Working order in the add-in

1. Confirm suggested-edits mode is on (Track Changes engaged).
2. Read the document top to bottom. For each paragraph, run §1–§7 against the text.
3. Apply every **auto** hit as a tracked change (smallest edit). Respect the three guards.
4. For every **query** hit, decide: unambiguous → tracked change; needs the author → anchored comment using `query-bank.md` wording.
5. Hand off to the **judgement layer** (SKILL.md → Layer 2) for everything a find/replace cannot reach: rephrasing, structure/IMRD, statistical completeness, abbreviation expansion, table/figure conversions.
