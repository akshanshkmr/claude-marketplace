---
name: jmir-copyediting
description: Use this skill whenever copyediting, reviewing, redlining, or formatting a scholarly manuscript for JMIR Publications inside the Claude for Word add-in — even if the user just says "copyedit this paper," "apply house style," "fix the stats notation," or "work the reviewer comments." It applies edits directly in the open .docx as native Word tracked changes (and raises author queries as anchored comments), covering JMIR house style, AMA style (11th ed), statistics, tables, figures, references, metadata, and abbreviations.
---

# JMIR Publications Copyediting Skill

Comprehensive reference for copyediting scholarly manuscripts to JMIR house style and AMA Manual of Style (11th ed), built for the **Claude for Word add-in**. Every edit lands in the open document as a **native Word tracked change**; every author query lands as an **anchored comment**. It pairs a **chronological workflow** (Step 1 and Step 3 checklists) with a **deterministic find/replace reference** so that no mechanical edit is missed and attention stays on judgement calls.

Read the **Runtime** section next — it defines how the two layers below are applied inside Word.

## Style Authority Hierarchy

**JMIR House Style and Editorial Guidelines are the primary authority.** AMA Manual of Style (11th ed) is a secondary fallback — apply AMA only for situations not explicitly covered by JMIR. When JMIR and AMA conflict, JMIR wins. This hierarchy applies to every section of this skill and all sub-files.

## Sub-Files (Load on Demand)

| File | Covers |
|------|--------|
| `routine-checks.md` | **Start here.** Operational quick-reference: the two-layer method, heading levels + font sizes, hard limits (figures/tables/abstract), the full word-swap table, hyphenation, neologisms, symbols, and stats/number formatting — distilled from a working copyeditor's routine sheet |
| `query-bank.md` | 180+ paste-ready author queries, categorized (authors, title, abstract, structure, language, abbreviations, statistics, tables, figures, references, ethics, COI/funding, equations) |
| `house-style.md` | Language, spelling, punctuation, capitalization, numbers, time, trademarks, nomenclature, lists, blockquotes, common terms glossary |
| `abbreviations.md` | Abbreviation usage rules, expansion rules, stand-alone sections, Abbreviations end section, Latin abbreviations, no-expansion list |
| `statistics.md` | P-values, leading zeros, spacing, eponyms, effect sizes, chi-square, t test, F test, CI, OR, IQR, Greek letters, currency, complex equations |
| `tables-and-figures.md` | Table formatting, nesting, footnotes, textboxes, figure captions, permitted/prohibited figures, TOC image, multimedia appendices, CONSORT/PRISMA checklists |
| `references.md` | In-text citations, reference list formatting, RefCheck, DOI/PMID, adding/deleting/reordering references, preprints, retractions, author names in text |
| `mechanical-rules.md` | **The deterministic layer, codeless.** All 139 find/replace rules (spelling, word swaps, statistics, phrase flags, hyphenation), each tagged `auto` (→ tracked change) or `query` (→ anchored comment), plus the three context guards. This is the in-add-in replacement for the old Python scanner. |

---

## Runtime: Claude for Word add-in

This skill runs **inside the open Word document**, not a terminal. There is no Python sandbox and no file to write — you read the live `.docx` and edit it in place.

**Tracked changes are the application surface.** Claude for Word's *suggested-edits mode* keeps Track Changes on: each edit shows as a native deletion (old text) + insertion (new text) in Word's review pane, where the author accepts or rejects each one individually.

- **Never turn Track Changes off.** Editing with it off bypasses the human review that copyediting depends on. If it is off, turn it on (or ask the user to) before editing.
- **Edit surgically.** Make the smallest change that fixes the issue — swap a word, not a sentence; fix a value, not a paragraph. Small revisions are easy to accept and preserve the author's voice (JMIR editing is "light to moderate," Phase 5).
- **Preserve formatting.** New text inherits the surrounding paragraph style, font, and numbering — do not restyle. Edit one span without disturbing the rest.
- **Scope to selection when given one.** If the user has selected a passage, edit only that selection.

**Author queries are comments, not edits.** Anything you would not silently change — a `query`-mode mechanical hit, a statistical-completeness gap, a data discrepancy, a metadata problem — goes in as an **anchored comment** on the relevant text, worded from `query-bank.md`. Do not bury a question inside a tracked change.

**Comment threads (Step 3 / reviewer rounds).** Claude for Word can read existing comment threads and the text they anchor to. To "work the comments," go through each thread in order: make the agreed fix as a tracked change on the anchored text, then **reply in the thread** stating what you did. Resolve per the Step 3 rules.

**What is out of add-in scope.** Claude edits the document; it cannot drive the OJS/Kriyadocs portal, run RefCheck, transfer metadata into web forms, generate XML/PDF previews, or send author emails. For checklist steps that live in those systems (eg, Step 1 Phase 10; Step 3 Phases 2, 3, 5, 6), do the in-document part as tracked changes/comments and leave a comment flagging the portal action for the human. Items that depend on the metadata form (ORCIDs, degrees, affiliations) can only be *flagged* in the document, since the form is not visible from Word.

---

## Operational Workflow: Two Layers

Every JMIR copyedit is two kinds of work. Do **both**, in this order, so nothing slips.

**Layer 1 — Deterministic.** A fixed list of 139 routine mechanical edits (US spelling, utilization to use, P=0.03 to P=.03, eponyms, trademark-symbol removal, noon/midnight, and the rest). In the terminal version a regex pass applied these; in the add-in **you are the regex** — read `mechanical-rules.md` and scan the document against every rule so none is missed. Each rule is tagged:

- `auto` — safe regardless of context. Apply each as a **tracked change**.
- `query` — correct most of the time but context-dependent (subjects to participants, manuscript to paper, "normal" health status, currency, URLs). Apply a tracked change **only** when context clearly confirms it; otherwise raise an **anchored comment**. Most map to a query in `query-bank.md`.

Mind the three context guards in `mechanical-rules.md` (URLs; "normal" in statistical usage; "manuscript" in Acknowledgments) and the December 2025 policy that **`and/or` is now retained**.

**Layer 2 — Judgement (everything a find/replace cannot reach).** Rephrasing unclear sentences as tracked changes, restructuring to IMRD, moving ethics/funding to the right section, statistical completeness (a mean needs an SD, a median an IQR, an OR a 95% CI), abbreviation decisions, table/figure conversions, and author queries. Clean fixes become tracked changes; anything needing the author becomes an anchored comment. The reference files below and `query-bank.md` drive this layer. The chronological checklists in Step 1 / Step 3 are how you sequence both layers per manuscript.

> Tip: `routine-checks.md` is the condensed map of Layer 1 + the high-frequency Layer 2 calls. Read it first on any new paper; drop into the detailed files (`house-style.md`, `statistics.md`, etc.) when a specific rule needs its full treatment.

---

## Step 1: Initial Copyedit (Chronological Checklist)

### Phase 1: Document Initialization & Setup

In the add-in, setup is light — most of this is verifying state, not manual menu work.

1. **Confirm Track Changes is on.** Suggested-edits mode must be engaged so every edit lands as a tracked change. If it is off, turn it on (or ask the user to) before making any edit. Never edit with it off.
2. **Proofing language / fresh spell-check** *(user-side, optional)*: these are Word desktop settings the user controls (set proofing language to **English (United States)**). You apply US spelling via the Layer 1 rules regardless of Word's proofing setting.
3. **Author identity on changes** *(user-side)*: tracked changes are attributed by the add-in; the human copyeditor sets their own display name in Word if needed.
4. **Identify article type**: Locate the article type at the top of the manuscript (eg, Original Paper, Review, Protocol/Proposal, Short Paper, Viewpoint, Implementation Report). If missing, add the most appropriate type from the approved list as a tracked change, or raise a comment if you cannot determine it from the document.
5. **Check for Morisky scales**: Scan for "Morisky" or "MMAS". If found, raise a comment asking authors to provide license documentation or to remove all references to Morisky/MMAS.
6. **Honor any "CE:" instructions**: If the user pastes or references special instructions from the submission note (tagged "CE:"), apply them. You cannot read the article page yourself — ask the user for any such instructions if relevant.

### Phase 2: Title & Headings

1. **Title case**: Ensure the title is in **title case** (headline style). See `house-style.md` §3 for capitalization rules.
2. **Character limit**: All titles must fit within a **280-character limit** (including spaces).
3. **Study design in title**:
   - RCTs: title must contain "Randomized Controlled Trial" in the **second half**.
   - Protocols/Proposals: title must contain "Protocol for a [Study Design]" or "Proposal for a [Study Design]" in the **second half**.
   - Tutorials: title must contain "Tutorial" in the second part.
   - Viewpoints/Research Letters: Descriptive, declarative, or interrogative. No study design required.
   - Commentaries: Avoid "A Commentary" as a stand-alone subtitle. Do NOT include the title of the original publication.
   - Letters to the Editor: Short, unique, descriptive title. Do NOT include the title of the original publication.
   - Author's Reply: Use format `Authors' Reply: [title of the Letter to the Editor]`.
   - Corrigenda: Must contain the name of the article being corrected and the word "Correction".
   - In Memoriam: Must contain "In Memoriam" followed by the individual's name.
4. **Title types**: Descriptive titles (preferred for original papers/reviews/protocols) describe the subject without revealing conclusions. Declarative titles (acceptable for viewpoints/commentaries) state findings. Interrogative titles require approval for original articles.
5. **Directly edit the title** in both the Word document and OJS metadata — do NOT suggest title changes to the author via comment.
6. **Paper type label**: Confirm paper type is stated at top of Word document. "Review" is only for papers reviewing other papers (not apps, websites, etc). "Systematic Review" requires strict PRISMA compliance — app store searches are NOT systematic reviews.
7. **Headings**: All section headings in title case, correct heading levels (H1 for main sections, H2/H3/H4 for subheadings). See `house-style.md` §3 for detailed title case rules.
8. **IMRD structure**: Verify Introduction → Methods → Results → Discussion for Original Papers. If the structure deviates, confirm it is justified per the article type.
9. **Multipart papers**: If paper is "Part 2" or later, ensure previous parts are cited in the Introduction.

### Phase 3: Metadata Verification

1. **Author names**: Check spelling, capitalization against OJS metadata. Use initials format: Bryan George Miller → BGM (not BM). Full first name required (unless author objects). No periods after initials, no space between multiple initials. For hyphenated given names: Ka-Wai Tam → KWT (no hyphen in initials). See `references.md` for author name formatting in body text.
2. **Author degrees**:
   - List from **lowest to highest**, no periods/punctuation in degree abbreviations.
   - Comma separating name from degrees; semicolons between different authors. Example: `Bryan G Miller, MSc, MD, PhD; Jane Doe, BSc`.
   - Only academic degrees and fellowships — no certifications (eg, LGPC is not allowed).
   - Do NOT include: fellowship designations, honorary degrees, degree candidacy (eg, "PhD (c)", "PhD (ABD)"), degree specializations in parentheses (eg, "MSc (Geography)"), or job titles (eg, "Professor").
   - Honours-level degrees are acceptable: `BSc (Hons)` — no periods or extra punctuation.
   - Degrees below master's level usually excluded unless highest degree held or in an unrelated field.
   - Specialized credentials below master's level may be included if relevant (eg, RN, CHES).
   - Acceptable degrees include: Prof Dr, Dr med, PhD, Dr rer, Dr rer nat, Dr sc med.
3. **Author affiliations**:
   - Largest unit to smallest (eg, University → Faculty → Department → Division). Remove duplicates. Each unit in separate metadata boxes.
   - Do NOT use short forms or acronyms (eg, expand "UHN" to "University Health Network"; expand "Dep." to "Department").
   - Affiliations in **title case** (not ALL CAPS or all lowercase).
   - Do NOT include postal codes (postal code only for corresponding author) or author positions (eg, director, professor).
   - Organizations not administratively linked → list as **separate affiliations**.
   - **Unaffiliated authors** (eg, patient partners): use "Patient partner" or "Stakeholders with living experience of [condition]".
4. **Corresponding author**: Verify one author is designated with email, mailing address (including postal/zip code), phone number (with country code, no brackets or hyphens), and fax number if applicable.
5. **Group/collaborative authors**: If listed, all collaborators must be listed in Authors' Contributions. Ask if contributors should also be mentioned in Acknowledgments. Non-author collaborators must be identified by their full name.
6. **ORCIDs**: Verify all authors have ORCIDs. If missing, query authors to create them (mandatory for publication). Cross-check name consistency between ORCID profile and JMIR metadata.
   - Green ORCID icon: matches author profile (OK).
   - Orange ORCID icon: does not match — query authors to confirm preferred credit name.
   - Red ORCID icon: no ORCID provided — query author to register.
7. **Keywords**: Separated by semicolons, sentence case, no trailing period/semicolon. Remove duplicate singular/plural forms; retain only one. Remove overly generic keywords. Recommend **5-12 keywords** including MeSH terms. If abbreviations are used as keywords, include expanded versions too. Use search variants (eg, "smartphone" AND "mobile phone" AND "mHealth").
8. **License to Publish (LTP) form**: Verify all authors have signed. Cross-check COI reported in the LTP against the Conflicts of Interest section. For missing signatures or discrepancies, query authors in Step 1. If an author needs form assistance (resend, link expired), forward to `copyediting@jmir.org`. Outstanding issues in Step 3 → leave a Layout Note.

### Phase 4: Abstract Copyediting

1. **Word count**: Both structured and unstructured abstracts must not exceed **450 words**.
   - If abstract exceeds limit by ≤50 words: attempt to reduce (eg, remove wordy constructs, redundant expressions, circumlocutions, convert passive to active voice).
   - If abstract exceeds limit by >50 words: query the author to reduce further.
   - Template: `"As per the journal guidelines, the abstract for [article type] should not exceed the limit of 450 words. I have made some revisions and suggestions to this effect. Please confirm that all essential information has been retained [and reduce the length of the abstract further to adhere to the above-mentioned word limit]."`
2. **Structure**: Verify headings match article type:

   | Article Type | Abstract Type |
   |---|---|
   | Original Paper / Short Paper / Review / Protocol / Early Reports | Structured (BOMRC) |
   | Viewpoint / Personal Perspectives / Patient Perspectives | Unstructured |
   | Commentary | Unstructured; narrative format (300 words) |
   | Editorial / Guest Editorial / Tutorial / Proposal / Case Report | Unstructured (structured if data are presented) |
   | Letter to the Editor / Research Letter (JMIR, mHealth, Mental Health, Dermatology) | Not required |
   | Rapid Surveillance Report | Unstructured |
   | Open Source/Open Data | Structured |
   | Notes from the Field | Unstructured (structured if data presented) |

3. **Trial registration** (RCTs only):
   - Must appear in abstract under a "Trial Registration" subheading.
   - Format: `ClinicalTrials.gov NCT12345678; https://clinicaltrials.gov/ct2/show/NCT12345678`
   - Verify the registration number is also mentioned in the main text (in parentheses at first mention).
   - If the trial was not registered, authors must explain why in the Methods section.
   - If the paper uses data from another RCT, cite the parent RCT with its registration number in parentheses.
   - Memory aid: The letters R, C, T appear in the abstract headings: Background, Objective, Methods, **R**esults, **C**onclusions, **T**rial registration.
4. **Protocols/Proposals Results**: Since results are not yet known, include a short Results section stating current project status (eg, funding, enrollment, anticipated completion date). Use specific dates, not just "currently."
5. **No URLs in abstract**: Remove all URLs from the abstract; convert to references if needed. Exception: Trial registration URL is the only URL allowed.
6. **SMS text messaging in abstract**: Use "SMS text messaging" (both terms) in the abstract.
7. **Abstract must stand alone**: Abbreviations introduced in the abstract must be reintroduced in the main text.
8. **Step 3**: Copy the final copyedited abstract from the manuscript into the metadata form. Retain a copy of the abstract in the manuscript file (mandatory for abstracts containing special formatting: italics, statistics, sub/superscript). Tip: You can paste structured abstract text into the unstructured field and toggle to "structured" — sections auto-sort if subheadings are correct.

### Phase 5: Main Text & Language Editing

1. **Editing level**: Light to moderate. Correct grammar, spelling, run-on sentences, comma splices, awkward phrasing, superfluous/casual language. Do NOT perform heavy stylistic rewriting or move text around.
2. **Tense** (see `house-style.md` §1):
   - Methods: past tense ("was conducted"). Exception: Protocols/Proposals use future ("will be enrolled") or present ("is currently recruiting").
   - Objective: present preferred if study is subject ("This paper explores..."); past acceptable when reporting completed research ("We aimed to...").
3. **Self-reference**: Change "present study", "current study", "current paper" → "**this study**" or "**this paper**". Use "paper" or "study" rather than "article".
4. **First person**:
   - Plural "we" is acceptable if not overused (avoid starting every Methods sentence with "we").
   - Singular "I"/"my" is **forbidden** in all sections including opinion pieces. Use "It is the opinion of this author..." or similar.
5. **Abbreviations**: Apply all rules in `abbreviations.md`. Key rules:
   - Expand at first mention if used ≥3 times in a stand-alone section.
   - Forbid author-invented and person-centered abbreviations.
   - Compile Abbreviations end section.
6. **Statistics**: Apply all rules in `statistics.md`. Key checks:
   - No leading zero for P, α, β values. Leading zero for all others.
   - No spaces around equality/inequality signs.
   - P-value rounding: 2 decimals if P≥.01, 3 if P<.01.
   - Eponyms: no possessives (Cohen d, not Cohen's d).
7. **URLs in text**: Remove all hyperlinks from text and abstract. Convert URLs to formal references. Exception: URLs in direct quotes can stay if they don't affect kerning.
8. **Spelling**: American English (US) only. See `house-style.md` §1.5.
9. **Numbers, punctuation, lists**: See `house-style.md` §7 (numbers), §8 (punctuation), §9 (lists), §10 (blockquotes).
10. **Trademarks**: Remove ®, ™, ℠ symbols. Capitalize initial letter. See `house-style.md` §11.
11. **Software/devices**: Include manufacturer/developer in parentheses at first mention. Example: `SPSS software (version 20.0; IBM Corp)`. See `house-style.md` §12.
12. **Table/figure/textbox/MA citations**: Verify all are mentioned in text and appear in numerical order.
13. **Blockquotes**: Format per `house-style.md` §10.
14. **and/or**: Retain as is (policy updated December 2025).

### Phase 6: Tables & Textboxes

Apply all rules in `tables-and-figures.md`. Key checks:
1. Correct nesting (bold category headers, subcategories in rows below).
2. Cell formatting: `n (%)`, `mean (SD)`, `OR (95% CI)`.
3. Footnotes: alphabetical superscripts (a, b, c), order of appearance (left→right, top→bottom), all end with periods, no asterisks.
4. Empty cells: use em-dash (—) for unavailable data with footnote definition. Use N/A for "not applicable" (note the /).
5. Percent sign only in column header (eg, "Participants, n (%)"), not in table body.
6. Units in correct location (column heading if applicable to all items in column).
7. P values correctly placed in row headings when appropriate.
8. Correlation and P values in separate rows in correlation tables.
9. No hard returns within table cells.
10. 1-column tables → convert to 1×1 Word table (textbox). No drawing shapes.
11. Textboxes: no footnotes. Remove reference citations from textbox captions (move to main text).

### Phase 7: Figures & Multimedia Appendices (MAs)

Apply all rules in `tables-and-figures.md`. Key checks:
1. **Captions**: Sentence case, end with period, succinct. Define all abbreviations used in the figure at end of caption (alphabetical order). Do not include "Figure X" inside caption text field.
2. **Language in figures**: Suggest corrections in Step 1 comments. Check for red error lines under words.
3. **Figure references**: Any reference citations in figure or legend must be cited in text immediately after first mention (eg, "Figure 1 [29]").
4. **Copyright/permissions**: Check CC license. If CC BY, add citation and CC link. If copyrighted, request permission.
5. **Unused files**: Ask author if unused figure/MA files on Editing tab should be included. If not, move to "Other" files section.
6. **Required checklists in MAs**:
   - **RCTs**: CONSORT flow diagram (as figure in Results) + CONSORT-EHEALTH checklist (as MA). Caption: `CONSORT-eHEALTH checklist (V 1.6.x).` where x = version.
   - **Systematic Reviews**: PRISMA flow diagram (as figure in Results) + PRISMA checklist (as MA). Scoping reviews use PRISMA-ScR.
   - **Implementation Reports** (JMIR Medical Informatics only): iCHECK-DH checklist.
   - Checklist names (PRISMA, CONSORT, CHERRIES, etc) do NOT need expansion in captions; expansion goes in Abbreviations list.
7. **TOC image**: Query author if not provided. See template comments.
8. **Peer-review reports**: Required as MAs for funded proposals and protocols.
9. **Questionnaires**: Include as MAs unless copyright-protected.

### Phase 8: End Sections

Verify the following sections appear **in this order** at the end of the manuscript:
1. **Acknowledgments** (optional):
   - Section titled "Acknowledgments" (no 'e' after 'g').
   - Author names as **initials** (not full names). Non-author persons mentioned by **full name**; titles (Dr, Ms) and degrees optional but per AMA: do not use both honorific AND academic degree (eg, `Dr Claudia Achenbach` or `Claudia Achenbach, MD, PhD` — not both).
   - Written narratively (bullet point lists are not permitted).
   - All abbreviations used here should be defined within the section and considered self-contained; these abbreviations should NOT be included in the Abbreviations end list.
   - If generative AI tools were used, declare in Acknowledgments (unless explicitly cited in main text). Include: tool name, reference, and prompt/purpose.
   - If APF support/waiver was granted, include: `"All authors declared that they had insufficient funding to support open access publication of this manuscript, including from affiliated organizations or institutions, funding agencies, or other organizations. JMIR Publications provided article processing fee (APF) support for the publication of this article."`
   - Check for grant numbers — change "Grant No." to "grant XXXXX" per AMA.
   - Author contributions do NOT belong here (move to Authors' Contributions). Conflicts of interest do NOT belong here (move to COI section).
2. **Funding** (mandatory for all article types; optional for editorial material: Editorial, Guest Editorial, Letter to the Editor, Author Reply, Commentary):
   - Section titled "Funding" (not "Funding Statement").
   - Funding separate from COI per COPE guidance.
   - If no funding: `"The authors declared no financial support was received for this work."`
   - Encourage declaring funder involvement/non-involvement in study design, data collection, analysis, interpretation, or writing.
3. **Data Availability** (optional)
4. **Disclaimer** (optional)
5. **Authors' Contributions** (optional):
   - Author names as initials (Bryan George Miller → BGM, not BM).
   - If >1 author shares initials: use first initials + space + last name (eg, `BG Miller`).
   - If >1 author shares initials AND last name: use full names (eg, `John Smith` and `Jane Smith`).
   - Names with "Jr"/"Sr": initials + space + suffix (eg, `BGM Jr`).
   - **CRediT taxonomy** (preferred since 2022): Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Visualization, Writing – original draft, Writing – review & editing.
   - For multiple contributors per role, include degree of contribution: `(lead)`, `(equal)`, `(supporting)` in round brackets.
   - Delete any statements like "All authors contributed equally" — equal contribution is declared via the metadata form's Equal Contribution field.
   - Group author collaborators must all be listed here by full name.
6. **Conflicts of Interest** (mandatory) — If none: "None declared." Replace lengthy no-conflict sentences (eg, "The authors do not have any personal financial interests...") with simply "None declared." Cross-check against License to Publish (LTP) form and submission note.
7. **Abbreviations** (mandatory) — H3 heading. List all abbreviations used in abstract or main text in alphabetical order. Sorting: punctuation → symbols → numerals → plain text (A-Z) → lowercase Greek letters. See `abbreviations.md` §2.1 for full sorting example.

### Phase 9: References

Apply all rules in `references.md`. Key checks:
1. Upload Word file with references and run RefCheck.
2. Verify reference count in Word matches RefCheck.
3. Ensure all in-text citations are present (out-of-order is OK; auto-renumbered by script).
4. Check duplicate entries.
5. Classify each reference (web, journal, book, conference) and "save and confirm."
6. Add queries for incomplete references.
7. Delete original reference list from Word using tracked changes.
8. Verify JMIR/sister journal references have manuscript number in page field + Free Full Text link.
9. Check all RefCheck URLs are functional.

### Phase 10: Final Step 1 Actions

1. Remove authorship information, affiliations, corresponding author, and keywords from the Word document (these are in OJS metadata).
2. Review metadata form for correctness.
3. Upload edited Word file with tracked changes.
4. Select RefCheck file with confirmed references.
5. Send notification email to author using the COMPLETE email icon.
6. Refer to Step 1 checklist one final time before completing.

---

## Step 3: Final Copyedit (Chronological Checklist)

### Phase 1: Author Response Review

1. **Accept all tracked changes** made during Steps 1-2.
2. **Address all author comments** from Step 2. Incorporate feedback ensuring consistency with surrounding text.
3. **Proofread the manuscript** for any new errors introduced by author.
4. Delete all comments from the Word file.
5. Delete authorship information, figures, and references from the Word file (these are in OJS/Kriyadocs).

### Phase 2: Metadata Transfer

1. **Transfer title and abstract** to OJS/Kriyadocs metadata.
2. **Retain a copy of the abstract in the manuscript file** — mandatory for abstracts containing special formatting (italicized text, statistics, sub/superscripts).
3. **Review metadata** one final time: author names, degrees (correct punctuation: names separated from degrees by commas, authors separated by semicolons), affiliations (no duplicates), keywords.
4. **Retain paper type** in manuscript file.

### Phase 3: Reference & LTP Finalization

1. Check all references are verified and confirmed in RefCheck and cited in main text.
2. If all LTPs (License to Publish forms) were uploaded in Step 2, cross-check against COI section.
3. Final reference count in Word must match RefCheck.

### Phase 4: Document Cleanup

1. **Remove page/section breaks**: Delete all manual page breaks and section breaks.
2. **No hard returns in tables**.
3. **Paragraph markers**: Check for stray formatting.

### Phase 5: XML Conversion & PDF Review

1. Upload final clean Word file to Step 3.
2. Click in order (let each page load completely): **HTML check → Generate XML → Preview PDF**.
3. **Side-by-side comparison**: Compare final Word document with generated PDF:
   - All paragraphs present in PDF.
   - All headings in title case and at correct levels.
   - Title and article type correct (if wrong in PDF, leave layout comment for production editor).
   - All figures and tables formatted correctly (figures may appear as blank gray slates — verify captions appear).
   - All end sections present in correct order.
   - Abbreviations section appears after References in PDF.
   - COI section content reflects correctly.
   - Abstract structure is correct in PDF.
   - Author names, degrees, affiliations correct in PDF metadata.
   - Final reference count in PDF matches RefCheck.
4. **Check generative AI declaration**: Verify AI tool usage is declared in Acknowledgments (unless explicitly cited in main text).

### Phase 6: Layout Notes & Sign-Off

1. Add any pending notes for the typesetter/production editor in the **Layout Comments** box.
2. Note any outstanding author queries not resolved.
3. Note any missing references with reasons.
4. Check if instructions from original assignment email or submission note (tagged "CE:") are addressed.
5. **Sign off with your name**.
6. Click the COMPLETE email notification icon to notify the journal editor.

---

## Template Comment Bank (Quick Reference)

### Blanket Comment (always add at beginning of every manuscript)

**OJS version:**
> Please go through my revisions and address all comments flagged in the manuscript. Do not accept or reject any changes (made by me) to the document. Copyediting is intended to bring the manuscript in line with our JMIR House Style and Editorial Guidelines and AMA Manual of Style (11th ed). Instead of rejecting tracked changes, add a Comment if you disagree with any edits. In addition, list your required changes using the comments feature. If you do make any minor changes to the text, keep Track Changes on in the document. If you wish to view the manuscript without any track changes, change the view to Simple Markup for easy readability. Following submission of your revised manuscript in Step 2 of Copyediting, I will do a final round of editing on your paper in Step 3 (before typesetting) to incorporate the changes requested by you. If you require any assistance during Step 2 of copyediting, you can reach out to me at [insert copyeditor's email address], and I would be happy to help you.

**Kriyadocs version:**
> Please go through my revisions and address all author queries (AQs) in the manuscript. Copyediting is intended to bring the manuscript in line with the JMIR House Style and Editorial Guidelines and AMA Manual of Style (11th ed). Do not reject any tracked changes made to the document. Instead of rejecting tracked changes, add a copyeditor query (CQ) if you disagree with any edits. In addition, insert a CQ for any additional requests or queries. Please follow the instructions in the email to complete the Author Revisions step. Thereafter, I will do a final round of editing on your paper in the Copyediting Final stage (before typesetting) to incorporate the changes requested by you. If you have any questions, please contact me at [your email]. — [Sign off with your name]

### Common Author Queries

> For the **comprehensive, categorized set of 180+ paste-ready queries**, use `query-bank.md`. The table below is a quick-reference subset for the most frequent situations.

| Situation | Template Comment |
|-----------|-----------------|
| Missing ORCIDs | "Please provide the ORCIDs for all authors in the metadata form. If the authors do not have ORCIDs, please create new ORCIDs for them, as manuscripts cannot be published in this journal without ORCIDs." |
| Missing author degrees | "Please provide the academic degrees for all authors in the metadata form." |
| Unacceptable certifications | "For author [initials], please provide the academic degree. [Certificate initials] is a certification, not a degree, and only academic degrees are allowed in the submission form." |
| Affiliations mismatch | "Please ensure that the affiliations provided here are consistent with those provided in the metadata form." |
| Few keywords (<5) | "For better indexing purposes, we recommend providing at least 5 keywords or key phrases. Terms more specific to the study should be used as keywords. In addition, a few MeSH terms should be used." |
| Missing LTP | "Please ensure that all authors sign the License to Publish form as soon as possible and disclose/declare any conflicts of interest." |
| Incorrect article type | "Please confirm the article type." |
| Missing trial registration | "Please provide the trial registration number in the format: ClinicalTrials.gov NCT12345678; https://clinicaltrials.gov/ct2/show/NCT12345678" |
| Missing TOC image | "Do you have a figure you would like to use for the Table of Contents thumbnail image? If not, we can select one for you." |
| Missing n values in tables | "Please provide the absolute values (n) corresponding to the percentages reported in this table." |
| Missing figure caption info | "Please provide a caption for this figure. The caption should be in sentence case and end with a period." |
| Missing CONSORT checklist | "Please provide the CONSORT-EHEALTH checklist as a multimedia appendix." |
| Data discrepancy | "There appears to be a discrepancy between the data reported in the text and the data in [Table/Figure X]. Please verify and correct." |

---

## Author Communication Timelines

### Step 2 Reminders
| Day | Action |
|-----|--------|
| Day 7 | Send email reminder to **all authors** from your personal email (CC `copyediting@jmir.org`). Find all authors' emails via the envelope icon on the article page |
| Day 14 | Email `copyediting@jmir.org` to report no response; they will send a reminder |
| Day 30+ | Continue monitoring; notify copyediting team if Step 2 remains incomplete |
| Extension expired | Send another reminder; if no response within 7 days, email `copyediting@jmir.org` |

### Step 3 Pending Comments
| Situation | Action |
|-----------|--------|
| Non-critical comments unaddressed by author | Assume author is fine with the change; accept the change yourself |
| Critical comments unaddressed | Send email to all authors (CC `copyediting@jmir.org`) after **4 days** |
| No response to critical comments for 7+ days | Email `copyediting@jmir.org` |
| Author requests after completion | Forward emails to `copyediting@jmir.org` |

### Communication Rules
- Always CC `copyediting@jmir.org` when communicating with authors.
- Acknowledge all author emails within **1 calendar day**.
- Do NOT send reminder emails from inside the system — send from your personal registered email.

---

## Escalation Protocol

Contact copyediting@jmir.org **before** suggesting major content revisions. Escalate for:
- Retracted references (check PubMed / Retraction Watch Database)
- Suspected plagiarism, data fabrication/falsification
- Privacy/informed consent concerns
- Article type misclassification requiring structural changes
- Errors that cannot be resolved through author clarification
- Authors refusing title revisions → pass information to Production Editor via Layout Note

---

## Freelance Copyeditor Guidelines & Benchmarks

### 1. Performance & Quality Benchmarks
Contractual copyeditors are expected to meet and maintain the following monthly averages:
* **Author Satisfaction (Survey Score)**: **&ge;4.6 / 5.0** (Scale: 1 = not satisfied, 5 = very satisfied). Reviewed before starting Step 3.
* **Turnaround Time (TAT)**: **&le;7 calendar days** total per manuscript (typically **5 days for Step 1** and **2 days for Step 3**).
  * *Prompt start*: Copyediting should begin within **1 calendar day** of assignment.
  * *Prioritization*: Fast-tracked manuscripts (highlighted with a blue background on the dashboard) must be prioritized.
* **Quality Control (QC) Check Score**: **&ge;3 / 4** on the following scale:
  * `4` = Very Good (Publication-ready; minimal/negligible formatting or style issues).
  * `3` = Good (Nearly publication-ready; few minor issues requiring minimal final effort).
  * `2` = Below Expectations (Requires moderate revisions; returned to author or copyeditor).
  * `1` = Poor (Requires significant revisions; returned to copyeditor/author).

### 2. Administrative & Weekly Reporting
* **Weekly Status Report**: Email to `copyediting@jmir.org` every **Monday** with the subject "`Status update - [date]`" (eg, *Status update - April 21*). Include:
  * Manuscript identifier (eg, `ms 34560`).
  * Current status (eg, `Step 1`).
  * Notes on delayed papers (eg, reason for delay, author reminders sent).
  * Tentative completion date of the current step.
* **Email Communication**: Always CC or forward all correspondence with authors to `copyediting@jmir.org`.
* **Inability to Edit**: If you cannot accept a manuscript assignment, notify the Team Lead via `copyediting@jmir.org` within **24 hours** with a reason.

### 3. Invoicing & Billing
* **Time Allotment**: Fixed rate per billable hour. Allotted hours (based on word count, references, complexity) are stated in the assignment email (eg, 4-5 hours for 4k-5k words; 7 hours for 5k-7k words). Prior approval from the Team Lead is required to exceed allotted hours.
* **Invoice Submission**: Email monthly invoices to the Team Lead (`rajitha.sivakumaran@jmir.org`) within the **first week of the month** (eg, February invoice sent by March 7) to ensure payment within the same month.
* **Invoicing Format**:
  * *File Name*: `JMIR_invoice_FirstName_LastName_MonthYear_0000` (eg, `JMIR_invoice_John_Doe_March2026_0001`).
  * *Details Required*: Manuscript number, date of Step 3 completion (only completed papers), hours worked (including prior approvals notes), and amount.
  * *Billed To*: `JMIR Publications Inc, 130 Queens Quay E, Suite 1100, Toronto, ON M5A 0P6`.
  * *Payment Terms*: Net 30 days from invoice date. Specify CA$ or US$ (as per contract), and itemize GST/HST with registration number if applicable.
* **Key Contacts**:
  * *General/Copyediting guidance / Unresponsive authors*: `copyediting@jmir.org`
  * *Invoices, availability, weekly volume updates*: Rajitha Sivakumaran (`rajitha.sivakumaran@jmir.org`)
  * *Escalated matters*: Neha Mirchandani, Manager, Editing Services (`neha.mirchandani@jmir.org`)
  * *Vendor management*: Kelvin Cheung, Copyediting Vendor Lead (`kelvin.cheung@jmir.org`)
  * *Technical issues (OJS/Kriyadocs)*: `tech-support@jmir.org` (optimize for Chrome/Firefox/Safari first; provide URL, errors, screenshots).


