# Report Feedback Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let an editor select text in the generated copyedit report, tag it (missed edit / wrong edit / better suggestion / general note) with a note + optional replacement, and export all feedback as structured JSON to improve the skill.

**Architecture:** All changes are in the single static HTML generator `report.py`. The Python renderer gains data attributes (`data-pidx`, `data-section` on paragraphs; `data-rule-id` on edit spans) so client-side JS can anchor feedback to paragraphs/sections/rules. A client-side feedback module (selection → floating pill → popover → `localStorage` → sidebar pane) is embedded in the report's `<script>`. The existing "Copy insights" topbar button is repurposed to download a `jmir-feedback.v1` JSON containing the report summary plus all feedback.

**Tech Stack:** Python 3 (no third-party deps for `.txt`), vanilla browser JS/CSS embedded as Python string literals. Tests are a dependency-free `assert`-based runner (no pytest) over the generated HTML string.

## Global Constraints

- Single self-contained static HTML file — no backend, no network, no auth.
- `localStorage` persistence keyed by existing `window.__MSID__`; degrade gracefully (never throw) when storage is unavailable, matching existing code.
- Do not alter the three views (Original/Diff/Final), the diff DOM, or the existing Queries / Rules-applied panes.
- Target file: `plugins/jmir-copyediting/scripts/report.py`.
- Tests run with: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py` (exits non-zero on failure).
- Feedback categories (exact slugs): `missed-edit`, `wrong-edit`, `better-suggestion`, `general-note`.
- Export schema string: `jmir-feedback.v1`.

---

## File Structure

- **Modify:** `plugins/jmir-copyediting/scripts/report.py` — all renderer, markup, CSS, and JS changes.
- **Create:** `plugins/jmir-copyediting/scripts/tests/sample.txt` — small fixture manuscript that triggers at least one auto edit.
- **Create:** `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py` — assert-based test runner over generated HTML.

---

## Task 1: Renderer data attributes (paragraph anchors + rule id) + test harness

**Files:**
- Create: `plugins/jmir-copyediting/scripts/tests/sample.txt`
- Create: `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
- Modify: `plugins/jmir-copyediting/scripts/report.py` (`_render_edit_span`, `_render_paragraph`, `render_html`, `build`)

**Interfaces:**
- Produces: every rendered paragraph block carries `data-pidx="<int>"` and `data-section="<str>"`; every `.edit-block` carries `data-rule-id="<str>"`. `report.build(Path, None, None) -> str` (unchanged signature).

- [ ] **Step 1: Create the fixture manuscript**

Create `plugins/jmir-copyediting/scripts/tests/sample.txt`:

```
A Smartphone Application for Behavioural Self-Monitoring: Randomized Controlled Trial

Jane A Smith, PhD; Robert B Jones, MSc

Abstract

Background: Many subjects suffer from poor access to care, and prior to this trial few studies analysed the behaviour of users.

Methods

We analysed adherence. Effect sizes were moderate (Cohen's d=0.45). Mean BMI was 27.4 kg.m-2.

Results

The application reduced symptoms (P=0.032). Costs averaged $45 per participant.
```

- [ ] **Step 2: Write the failing test runner**

Create `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`:

```python
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))
import report  # noqa: E402

SAMPLE = HERE / "sample.txt"


def gen():
    return report.build(SAMPLE, None, None)


def test_paragraph_anchors():
    h = gen()
    assert "data-pidx=" in h, "paragraphs must carry data-pidx"
    assert "data-section=" in h, "paragraphs must carry data-section"


def test_rule_id_on_edit_spans():
    h = gen()
    assert "data-rule-id=" in h, "edit spans must carry data-rule-id"


def main():
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok   ", name)
            except AssertionError as e:
                failures += 1
                print("FAIL ", name, "-", e)
    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    print("\nALL PASS")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: FAIL on `test_paragraph_anchors` and `test_rule_id_on_edit_spans` (attributes not yet emitted), exit code 1.

- [ ] **Step 4: Add `data-rule-id` to edit spans**

In `report.py`, `_render_edit_span`, change the `attrs` assignment from:

```python
    attrs = (
        f'class="{klass}" data-eid="{eid}" data-edited="true" '
        f'data-diff="{diff_kind}" data-tag-type="{_esc(e["tag_type"])}" '
        f'data-mode="{e["mode"]}" data-track-detail="{_esc(detail)}" tabindex="0"'
    )
```

to:

```python
    attrs = (
        f'class="{klass}" data-eid="{eid}" data-edited="true" '
        f'data-diff="{diff_kind}" data-tag-type="{_esc(e["tag_type"])}" '
        f'data-rule-id="{_esc(e.get("rule_id", ""))}" '
        f'data-mode="{e["mode"]}" data-track-detail="{_esc(detail)}" tabindex="0"'
    )
```

- [ ] **Step 5: Thread paragraph index + section into `_render_paragraph`**

In `report.py`, change the `_render_paragraph` signature and add an `anchor` string injected into every returned element. Replace the whole function with:

```python
def _render_paragraph(text: str, edits: list[dict], cls: str, counter: list[int],
                      pidx: int, section: str) -> str:
    anchor = f' data-pidx="{pidx}" data-section="{_esc(section)}"'
    if cls == "author":
        parts = re.split(r"(\s*[,;]\s*|\s+and\s+)", text)
        out = []
        for part in parts:
            if not part:
                continue
            if re.fullmatch(r"\s*[,;]\s*|\s+and\s+", part):
                out.append(_esc(part))
            elif part.strip():
                out.append(f'<span class="jrnlAuthor">{_esc(part)}</span>')
        return f'<p class="ms-authors"{anchor}>' + "".join(out) + "</p>"

    pieces, cursor = [], 0
    for e in edits:
        pieces.append(_esc(text[cursor:e["start"]]))
        counter[0] += 1
        pieces.append(_render_edit_span(e, f"e{counter[0]}"))
        cursor = e["end"]
    pieces.append(_esc(text[cursor:]))
    inner = "".join(pieces)

    if cls == "title":
        return f'<h1 class="jrnlArticleTitle"{anchor}>{inner}</h1>'
    if cls == "heading":
        return f'<h2 class="jrnlSectionHead"{anchor}>{inner}</h2>'
    if cls == "affil":
        return f'<p class="jrnlAffil"{anchor}>{inner}</p>'
    if cls == "corr":
        return f'<p class="jrnlCorr"{anchor}>{inner}</p>'
    m = _SUBLABEL_RE.match(text)
    if m:
        inner = re.sub(r"^([^:]+:)", r'<span class="jrnlSubhead">\1</span>', inner, count=1)
    return f'<p class="ms-body"{anchor}>{inner}</p>'
```

- [ ] **Step 6: Carry pidx + section through `build` blocks**

In `report.py`, `build`, change the two `blocks.append(...)` lines from:

```python
        if cls == "author":
            blocks.append((cls, para, []))     # authors carry no inline edits
            continue
        edits = _mechanical_edits_for(para, section)
        edits = _merge_judgement(para, edits, extra_by_para.get(i, []))
        edits = _dedupe_overlaps(edits)
        blocks.append((cls, para, edits))
```

to:

```python
        if cls == "author":
            blocks.append((cls, para, [], i, section))   # authors carry no inline edits
            continue
        edits = _mechanical_edits_for(para, section)
        edits = _merge_judgement(para, edits, extra_by_para.get(i, []))
        edits = _dedupe_overlaps(edits)
        blocks.append((cls, para, edits, i, section))
```

Also update the type annotation a few lines above from
`blocks: list[tuple[str, str, list[dict]]] = []` to
`blocks: list[tuple[str, str, list[dict], int, str]] = []`.

- [ ] **Step 7: Update both `render_html` block loops**

In `report.py`, `render_html`, change the body loop from:

```python
    for cls, text, edits in blocks:
        body_html_parts.append(_render_paragraph(text, edits, cls, counter))
```

to:

```python
    for cls, text, edits, pidx, section in blocks:
        body_html_parts.append(_render_paragraph(text, edits, cls, counter, pidx, section))
```

and the eid re-walk loop from:

```python
    for _cls, _text, edits in blocks:
        # account for author paragraphs producing no edit ids
        if _cls == "author":
            continue
```

to:

```python
    for _cls, _text, edits, _pidx, _section in blocks:
        # account for author paragraphs producing no edit ids
        if _cls == "author":
            continue
```

- [ ] **Step 8: Run the test to verify it passes**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: `ok    test_paragraph_anchors`, `ok    test_rule_id_on_edit_spans`, `ALL PASS`, exit 0.

- [ ] **Step 9: Commit**

```bash
git add plugins/jmir-copyediting/scripts/report.py plugins/jmir-copyediting/scripts/tests/
git commit -m "feat(report): emit data-pidx/data-section/data-rule-id anchors + test harness"
```

---

## Task 2: Feedback sidebar tab, pane, and structured summary data

**Files:**
- Modify: `plugins/jmir-copyediting/scripts/report.py` (`_sidebar_header`, `render_html`, `_STYLE`)
- Modify: `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`

**Interfaces:**
- Consumes: data attributes from Task 1.
- Produces: a third sidebar tab `data-pane="feedback"` with `#fbCount` and a `#fbList` container; globals `window.__SUMMARY__`, `window.__TITLE__`, `window.__SOURCE__` emitted in the report script. The existing `.st-btn` toggle logic already shows/hides `.side-sec[data-pane]`, so no new tab JS is needed.

- [ ] **Step 1: Write the failing tests**

Append to `test_feedback_report.py` (before `def main`):

```python
def test_feedback_tab_and_pane():
    h = gen()
    assert 'data-pane="feedback"' in h, "feedback sidebar pane missing"
    assert 'id="fbList"' in h, "feedback list container missing"
    assert 'id="fbCount"' in h, "feedback count badge missing"


def test_summary_globals():
    h = gen()
    assert "window.__SUMMARY__" in h, "structured summary global missing"
    assert "window.__TITLE__" in h, "title global missing"
    assert "window.__SOURCE__" in h, "source global missing"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: FAIL on `test_feedback_tab_and_pane` and `test_summary_globals`.

- [ ] **Step 3: Add the Feedback tab button**

In `report.py`, `_sidebar_header`, change the `.side-tabs` block from:

```python
        '      <div class="side-tabs">\n'
        '        <button class="st-btn is-on" data-pane="queries">Queries</button>\n'
        '        <button class="st-btn" data-pane="rules">Rules applied</button>\n'
        '      </div>\n'
```

to:

```python
        '      <div class="side-tabs">\n'
        '        <button class="st-btn is-on" data-pane="queries">Queries</button>\n'
        '        <button class="st-btn" data-pane="rules">Rules applied</button>\n'
        '        <button class="st-btn" data-pane="feedback">Feedback '
        '<span class="st-count" id="fbCount">0</span></button>\n'
        '      </div>\n'
```

- [ ] **Step 4: Add the Feedback pane to the sidebar**

In `report.py`, `render_html`, find the rules `<section>` close and insert a feedback section after it. Change:

```python
        + '      <section class="side-sec" data-pane="rules" hidden>\n'
        + (("".join(r_items)) or '<p class="empty">No mechanical edits were needed.</p>')
        + "\n      </section>\n"
        + "    </div>\n  </aside>\n</div>\n"
```

to:

```python
        + '      <section class="side-sec" data-pane="rules" hidden>\n'
        + (("".join(r_items)) or '<p class="empty">No mechanical edits were needed.</p>')
        + "\n      </section>\n"
        + '      <section class="side-sec" data-pane="feedback" hidden>\n'
        + '        <div id="fbList"></div>\n'
        + "      </section>\n"
        + "    </div>\n  </aside>\n</div>\n"
```

- [ ] **Step 5: Build and emit the structured summary + title/source globals**

In `report.py`, `render_html`, just after `queries, rules = _build_queries_and_rules(flat)` add:

```python
    summary = {
        "autoApplied": n_auto,
        "queries": n_query,
        "queryList": [f"Q{i}: {_query_text(g)}"
                      for i, g in enumerate(sorted(queries, key=lambda x: x["fam"]), 1)],
    }
```

Then in the final `doc = (...)` assembly, change the script-open block from:

```python
        + "<script>\nwindow.__INSIGHTS__ = " + json.dumps(insights) + ";\n"
        + "window.__MSID__ = " + json.dumps("jmir-" + re.sub(r"\W+", "-", title.lower())[:48]) + ";\n"
        + _SCRIPT + "\n</script>\n</body>\n</html>\n"
```

to:

```python
        + "<script>\nwindow.__INSIGHTS__ = " + json.dumps(insights) + ";\n"
        + "window.__MSID__ = " + json.dumps("jmir-" + re.sub(r"\W+", "-", title.lower())[:48]) + ";\n"
        + "window.__SUMMARY__ = " + json.dumps(summary) + ";\n"
        + "window.__TITLE__ = " + json.dumps(title) + ";\n"
        + "window.__SOURCE__ = " + json.dumps(source_name) + ";\n"
        + _SCRIPT + "\n</script>\n</body>\n</html>\n"
```

- [ ] **Step 6: Add sidebar feedback-item CSS**

In `report.py`, `_STYLE`, immediately before the closing `</style>` line, add:

```css
/* ── feedback (sidebar) ─────────────────────────────── */
.st-count{display:inline-block; min-width:16px; padding:0 5px; margin-left:4px;
  font:600 10px var(--ui-font); color:var(--ui-dim); background:var(--panel-2);
  border:1px solid var(--line); border-radius:99px}
.fb-item{position:relative; background:var(--panel); border:1px solid var(--line);
  border-left:3px solid var(--fam-query); border-radius:11px; padding:11px 12px; margin-bottom:10px}
.fbc-missed-edit{border-left-color:var(--fam-stat)}
.fbc-wrong-edit{border-left-color:var(--del)}
.fbc-better-suggestion{border-left-color:var(--fam-style)}
.fbc-general-note{border-left-color:var(--fam-query)}
.fb-head{display:flex; align-items:center; gap:8px; margin-bottom:6px}
.fb-del{margin-left:auto; background:transparent; border:1px solid var(--line-2);
  border-radius:7px; color:var(--ui-faint); cursor:pointer; padding:3px 7px; font-size:12px}
.fb-del:hover{color:var(--del); border-color:var(--del)}
.fb-snip{margin:0; font:400 13px var(--ser); color:var(--ui); line-height:1.5}
.fb-repl-line{margin:5px 0 0; font:600 12px var(--ui-font); color:var(--ins)}
.fb-note-line{margin:5px 0 0; font-size:12.5px; color:var(--ui-dim); line-height:1.5}
.fb-item{cursor:pointer}
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: all tests `ok`, `ALL PASS`.

- [ ] **Step 8: Commit**

```bash
git add plugins/jmir-copyediting/scripts/report.py plugins/jmir-copyediting/scripts/tests/test_feedback_report.py
git commit -m "feat(report): add Feedback sidebar tab/pane and structured summary globals"
```

---

## Task 3: Selection pill + popover markup and styles

**Files:**
- Modify: `plugins/jmir-copyediting/scripts/report.py` (`render_html`, new `_fb_popover_html`, `_STYLE`)
- Modify: `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`

**Interfaces:**
- Produces: static (initially hidden) DOM `#fb-pill` and `#fb-popover` with category buttons `.fb-cat[data-cat=...]`, inputs `#fb-repl` / `#fb-note`, buttons `#fb-save` / `#fb-cancel`, and snippet `#fb-snippet`. Consumed by Task 4 JS.

- [ ] **Step 1: Write the failing tests**

Append to `test_feedback_report.py` (before `def main`):

```python
def test_pill_and_popover_markup():
    h = gen()
    assert 'id="fb-pill"' in h, "feedback pill missing"
    assert 'id="fb-popover"' in h, "feedback popover missing"
    for cat in ("missed-edit", "wrong-edit", "better-suggestion", "general-note"):
        assert f'data-cat="{cat}"' in h, f"category button {cat} missing"
    for el in ('id="fb-repl"', 'id="fb-note"', 'id="fb-save"', 'id="fb-cancel"', 'id="fb-snippet"'):
        assert el in h, f"{el} missing"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: FAIL on `test_pill_and_popover_markup`.

- [ ] **Step 3: Add the popover-markup helper**

In `report.py`, add this function just above `def render_html(`:

```python
def _fb_popover_html() -> str:
    cats = [
        ("missed-edit", "Missed edit"),
        ("wrong-edit", "Wrong edit"),
        ("better-suggestion", "Better suggestion"),
        ("general-note", "General note"),
    ]
    cat_btns = "".join(
        f'<button class="fb-cat" data-cat="{slug}">{label}</button>'
        for slug, label in cats
    )
    return (
        '<div class="fb-popover" id="fb-popover">\n'
        '  <div class="fb-pop-head">Add editor feedback</div>\n'
        '  <p class="fb-snippet" id="fb-snippet"></p>\n'
        f'  <div class="fb-cats">{cat_btns}</div>\n'
        '  <input class="fb-input" id="fb-repl" type="text" '
        'placeholder="Suggested replacement (optional)">\n'
        '  <textarea class="fb-textarea" id="fb-note" rows="3" '
        'placeholder="What was missed or wrong?"></textarea>\n'
        '  <div class="fb-actions">'
        '<button class="fb-btn-cancel" id="fb-cancel">Cancel</button>'
        '<button class="fb-btn-save" id="fb-save">Save</button></div>\n'
        '</div>\n'
    )
```

- [ ] **Step 4: Inject the pill + popover into the document**

In `report.py`, `render_html`, change the toast line in the `doc` assembly from:

```python
        + '<div class="toast" id="toast"></div>\n'
```

to:

```python
        + '<div class="toast" id="toast"></div>\n'
        + '<button class="fb-pill" id="fb-pill">+ Add feedback</button>\n'
        + _fb_popover_html()
```

- [ ] **Step 5: Add pill + popover CSS**

In `report.py`, `_STYLE`, immediately before the closing `</style>` line, add:

```css
/* ── feedback (pill + popover) ──────────────────────── */
.fb-pill{position:absolute; z-index:60; display:none; font:600 12px var(--disp);
  color:#fff; background:linear-gradient(135deg,#3b82f6,#6366f1); border:0;
  border-radius:8px; padding:6px 11px; cursor:pointer; box-shadow:0 6px 18px -6px rgba(59,130,246,.8)}
.fb-popover{position:absolute; z-index:61; display:none; width:340px; padding:14px;
  background:var(--panel); border:1px solid var(--line-2); border-radius:13px;
  box-shadow:0 24px 60px -18px rgba(0,0,0,.75)}
.fb-pop-head{font:700 13px var(--disp); color:#fff; margin-bottom:8px}
.fb-snippet{margin:0 0 10px; font:400 12.5px var(--ser); color:var(--ui-dim);
  max-height:54px; overflow:auto; padding-left:9px; border-left:2px solid var(--line-2)}
.fb-cats{display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px}
.fb-cat{font:600 11px var(--ui-font); color:var(--ui-dim); background:var(--panel-2);
  border:1px solid var(--line); border-radius:99px; padding:5px 10px; cursor:pointer}
.fb-cat.on{color:#fff; border-color:#3b82f6; background:#243049}
.fb-input,.fb-textarea{width:100%; margin-bottom:9px; padding:8px 10px; color:var(--ui);
  background:var(--bg-2); border:1px solid var(--line-2); border-radius:8px;
  font:400 13px var(--ui-font); resize:vertical}
.fb-input:focus,.fb-textarea:focus{outline:none; border-color:#3b82f6}
.fb-actions{display:flex; justify-content:flex-end; gap:8px}
.fb-btn-cancel,.fb-btn-save{font:600 12px var(--disp); border-radius:8px; padding:7px 14px; cursor:pointer}
.fb-btn-cancel{color:var(--ui-dim); background:transparent; border:1px solid var(--line-2)}
.fb-btn-save{color:#fff; background:linear-gradient(135deg,#3b82f6,#6366f1); border:0}
```

- [ ] **Step 6: Run test to verify it passes**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: all tests `ok`, `ALL PASS`.

- [ ] **Step 7: Commit**

```bash
git add plugins/jmir-copyediting/scripts/report.py plugins/jmir-copyediting/scripts/tests/test_feedback_report.py
git commit -m "feat(report): add selection pill + feedback popover markup and styles"
```

---

## Task 4: Feedback capture, persistence, and sidebar rendering (JS)

**Files:**
- Modify: `plugins/jmir-copyediting/scripts/report.py` (`_SCRIPT`)
- Modify: `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`

**Interfaces:**
- Consumes: DOM from Tasks 1–3.
- Produces: a feedback IIFE that captures selections, stores items in `localStorage` (`<MSID>:feedback`), renders `#fbList`, updates `#fbCount`, supports delete + click-to-flash, and exposes `window.__FEEDBACK_GET__() -> array`. (JS behavior is verified in the browser in Task 6; the test asserts the code is embedded.)

- [ ] **Step 1: Write the failing test**

Append to `test_feedback_report.py` (before `def main`):

```python
def test_capture_js_present():
    h = gen()
    assert "window.__FEEDBACK_GET__" in h, "feedback getter not exposed"
    assert "':feedback'" in h or '":feedback"' in h or ":feedback" in h, \
        "feedback storage key not used"
    assert "getSelection" in h, "selection capture not wired"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: FAIL on `test_capture_js_present`.

- [ ] **Step 3: Append the feedback IIFE to `_SCRIPT`**

In `report.py`, `_SCRIPT`, insert the following block between the existing closing `})();` and the terminating `"""` (i.e., add a second IIFE):

```javascript

(function(){
  var paper=document.getElementById('paper'); if(!paper) return;
  var store=null; try{ store=window.localStorage; }catch(e){ store=null; }
  var KEY=window.__MSID__||'jmir';
  function load(k,d){ try{ var v=store&&store.getItem(KEY+':'+k); return v==null?d:JSON.parse(v);}catch(e){return d;} }
  function save(k,v){ try{ store&&store.setItem(KEY+':'+k, JSON.stringify(v)); }catch(e){} }
  function esc(s){ return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function closest(node,sel){ var el=node&&node.nodeType===1?node:(node&&node.parentElement); return el?el.closest(sel):null; }

  var items=load('feedback',[]);
  var pill=document.getElementById('fb-pill');
  var pop=document.getElementById('fb-popover');
  var listEl=document.getElementById('fbList');
  var countEl=document.getElementById('fbCount');
  var savedRange=null, savedCtx=null, chosenCat='missed-edit';
  var CAT={'missed-edit':'missed edit','wrong-edit':'wrong edit','better-suggestion':'better suggestion','general-note':'general note'};

  function ctxFor(range){
    var sel=range.toString();
    var p=closest(range.startContainer,'[data-pidx]');
    var info={selectedText:sel, paraIndex:p?+p.dataset.pidx:-1, section:p?(p.dataset.section||''):'', context:sel, linkedEdit:null};
    if(p){ var t=p.textContent||''; var i=t.indexOf(sel); if(i>=0){ info.context=t.slice(Math.max(0,i-120), i+sel.length+120); } }
    var eb=closest(range.startContainer,'.edit-block');
    if(eb){ var del=eb.querySelector('.diff-del'), ins=eb.querySelector('.diff-ins');
      info.linkedEdit={eid:eb.dataset.eid||'', ruleId:eb.dataset.ruleId||'', tagType:eb.dataset.tagType||'',
        original:del?del.textContent:'', suggestion:ins?ins.textContent:'', mode:eb.dataset.mode||''}; }
    return info;
  }
  function hidePill(){ pill.style.display='none'; }
  function showPill(range){
    var rs=range.getClientRects(), r=rs[rs.length-1]; if(!r){ hidePill(); return; }
    pill.style.display='block';
    pill.style.top=(window.scrollY+r.bottom+6)+'px';
    pill.style.left=(window.scrollX+r.left)+'px';
  }

  document.addEventListener('mouseup', function(){
    setTimeout(function(){
      if(pop.style.display==='block') return;
      var s=window.getSelection();
      if(!s||s.isCollapsed||!s.toString().trim()){ hidePill(); return; }
      var range=s.getRangeAt(0);
      if(!paper.contains(range.commonAncestorContainer)){ hidePill(); return; }
      savedRange=range; showPill(range);
    },1);
  });
  pill.addEventListener('mousedown', function(e){ e.preventDefault(); });
  pill.addEventListener('click', function(){ if(!savedRange) return; savedCtx=ctxFor(savedRange); openPop(); });

  function openPop(){
    hidePill();
    document.getElementById('fb-snippet').textContent=savedCtx.selectedText;
    document.getElementById('fb-repl').value='';
    document.getElementById('fb-note').value='';
    chosenCat='missed-edit';
    pop.querySelectorAll('.fb-cat').forEach(function(b){ b.classList.toggle('on', b.dataset.cat==='missed-edit'); });
    var rs=savedRange.getClientRects(), r=rs[rs.length-1];
    var top=(r?window.scrollY+r.bottom+6:window.scrollY+80);
    var left=(r?window.scrollX+r.left:40);
    var maxLeft=window.scrollX+document.documentElement.clientWidth-360;
    pop.style.display='block';
    pop.style.top=top+'px'; pop.style.left=Math.max(8,Math.min(left,maxLeft))+'px';
    document.getElementById('fb-note').focus();
  }
  function closePop(){ pop.style.display='none'; }

  pop.querySelectorAll('.fb-cat').forEach(function(b){
    b.addEventListener('click', function(){ chosenCat=b.dataset.cat;
      pop.querySelectorAll('.fb-cat').forEach(function(x){ x.classList.toggle('on', x===b); }); });
  });
  document.getElementById('fb-cancel').addEventListener('click', closePop);
  document.getElementById('fb-save').addEventListener('click', function(){
    var item={ id:'fb-'+Date.now()+'-'+Math.random().toString(36).slice(2,5),
      category:chosenCat, selectedText:savedCtx.selectedText, paraIndex:savedCtx.paraIndex,
      section:savedCtx.section, context:savedCtx.context, linkedEdit:savedCtx.linkedEdit,
      suggestedReplacement:document.getElementById('fb-repl').value.trim(),
      note:document.getElementById('fb-note').value.trim(), created:new Date().toISOString() };
    items.push(item); save('feedback',items); renderList(); closePop();
    var s=window.getSelection(); if(s) s.removeAllRanges();
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ closePop(); hidePill(); } });

  function renderList(){
    if(countEl) countEl.textContent=items.length;
    if(!listEl) return;
    if(!items.length){ listEl.innerHTML='<p class="empty">No feedback yet — select text in the manuscript to add some.</p>'; return; }
    listEl.innerHTML=items.map(function(it){
      var repl=it.suggestedReplacement?'<p class="fb-repl-line">&rarr; '+esc(it.suggestedReplacement)+'</p>':'';
      var note=it.note?'<p class="fb-note-line">'+esc(it.note)+'</p>':'';
      return '<div class="fb-item fbc-'+it.category+'" data-id="'+it.id+'" data-pidx="'+it.paraIndex+'">'
        +'<div class="fb-head"><span class="chip">'+CAT[it.category]+'</span>'
        +'<button class="fb-del" title="Delete">Delete</button></div>'
        +'<p class="fb-snip">\\u201c'+esc(it.selectedText)+'\\u201d</p>'+repl+note+'</div>';
    }).join('');
  }
  listEl.addEventListener('click', function(e){
    var item=e.target.closest('.fb-item'); if(!item) return;
    if(e.target.closest('.fb-del')){
      items=items.filter(function(x){ return x.id!==item.dataset.id; }); save('feedback',items); renderList(); return;
    }
    var p=document.querySelector('[data-pidx="'+item.dataset.pidx+'"]');
    if(p){ p.classList.remove('flash'); void p.offsetWidth; p.classList.add('flash'); p.scrollIntoView({behavior:'smooth',block:'center'}); }
  });

  window.__FEEDBACK_GET__=function(){ return items.slice(); };
  renderList();
})();
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: all `ok`, `ALL PASS`.

- [ ] **Step 5: Commit**

```bash
git add plugins/jmir-copyediting/scripts/report.py plugins/jmir-copyediting/scripts/tests/test_feedback_report.py
git commit -m "feat(report): capture, persist, and render editor feedback in sidebar"
```

---

## Task 5: Repurpose "Copy insights" into "Export feedback" (JSON download)

**Files:**
- Modify: `plugins/jmir-copyediting/scripts/report.py` (`_topbar`, `_SCRIPT`)
- Modify: `plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`

**Interfaces:**
- Consumes: `window.__FEEDBACK_GET__`, `window.__SUMMARY__`, `window.__TITLE__`, `window.__SOURCE__`, `window.__MSID__`, and the in-scope `flash()` helper from the first IIFE.
- Produces: topbar button `#fbExport` labeled "Export feedback" that downloads `<MSID>-feedback.json` with schema `jmir-feedback.v1`.

- [ ] **Step 1: Write the failing tests**

Append to `test_feedback_report.py` (before `def main`):

```python
def test_export_button_and_handler():
    h = gen()
    assert 'id="fbExport"' in h, "export button id missing"
    assert "Export feedback" in h, "export button label missing"
    assert "jmir-feedback.v1" in h, "export schema string missing"
    assert "Copy insights" not in h, "old Copy insights label should be gone"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: FAIL on `test_export_button_and_handler`.

- [ ] **Step 3: Rename the topbar button**

In `report.py`, `_topbar`, change:

```python
        '    <button class="btn-copy" id="copyInsights">Copy insights</button>\n'
```

to:

```python
        '    <button class="btn-copy" id="fbExport">Export feedback</button>\n'
```

- [ ] **Step 4: Replace the insights-copy handler with the export handler**

In `report.py`, `_SCRIPT` (the FIRST IIFE, where `flash` is in scope), change:

```javascript
  document.getElementById('copyInsights').addEventListener('click', function(){
    copy(window.__INSIGHTS__||'', 'Insights copied to clipboard');
  });
```

to:

```javascript
  document.getElementById('fbExport').addEventListener('click', function(){
    var fb=(window.__FEEDBACK_GET__&&window.__FEEDBACK_GET__())||[];
    var payload={ schema:'jmir-feedback.v1', title:window.__TITLE__||'',
      manuscript:window.__MSID__||'', source:window.__SOURCE__||'',
      exportedAt:new Date().toISOString(), summary:window.__SUMMARY__||{}, feedback:fb };
    var blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob);
    a.download=(window.__MSID__||'jmir')+'-feedback.json';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); },1000);
    flash(fb.length+' feedback item'+(fb.length===1?'':'s')+' exported');
  });
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: all `ok`, `ALL PASS`.

- [ ] **Step 6: Commit**

```bash
git add plugins/jmir-copyediting/scripts/report.py plugins/jmir-copyediting/scripts/tests/test_feedback_report.py
git commit -m "feat(report): export editor feedback as jmir-feedback.v1 JSON download"
```

---

## Task 6: End-to-end regeneration + manual browser verification

**Files:**
- No source changes (verification only). If a defect is found, fix in the relevant task's file and re-commit.

- [ ] **Step 1: Run the full test suite**

Run: `python3 plugins/jmir-copyediting/scripts/tests/test_feedback_report.py`
Expected: `ALL PASS`, exit 0.

- [ ] **Step 2: Regenerate a real report**

Run:
```bash
python3 plugins/jmir-copyediting/scripts/report.py \
  plugins/jmir-copyediting/scripts/tests/sample.txt \
  --out /tmp/fb-report.html --title "Feedback Smoke Test"
```
Expected: `wrote /tmp/fb-report.html`, no traceback.

- [ ] **Step 3: Manual browser checks**

Open `/tmp/fb-report.html` and confirm:
- Selecting text in the manuscript shows the "+ Add feedback" pill at the selection.
- Clicking the pill opens the popover; the selected text appears as the snippet.
- Choosing a category, typing a note/replacement, and Save adds a row under the **Feedback** sidebar tab and increments its count.
- Selecting text that overlaps an auto edit (e.g. "Cohen's d") then saving: open DevTools console, run `__FEEDBACK_GET__()[ ... ]` and confirm the item's `linkedEdit.ruleId` is populated (e.g. `swap.cohen`); selecting plain un-edited text yields `linkedEdit: null`.
- Reloading the page keeps the feedback (localStorage).
- Clicking a feedback row scrolls to and flashes the source paragraph.
- The Delete control removes the row and decrements the count.
- The topbar **Export feedback** button downloads `<msid>-feedback.json`; open it and confirm `schema: "jmir-feedback.v1"`, a `summary` with `autoApplied`/`queries`/`queryList`, and the `feedback` array.
- Original/Diff/Final toggles, Queries/Rules panes, zoom, and query-resolve progress all still work.

- [ ] **Step 4: Commit any fixes**

If Step 3 surfaced defects, fix them in the owning file and commit:
```bash
git add -A && git commit -m "fix(report): address feedback-loop browser verification findings"
```

---

## Self-Review

- **Spec coverage:** capture flow (Tasks 3–4), data model incl. `linkedEdit`/`paraIndex`/`section`/`context` (Tasks 1, 4), four categories (Tasks 3–4), localStorage keyed by MSID (Task 4), Feedback sidebar tab + scroll-flash + delete, no inline highlights (Task 4), repurposed export with folded summary, `jmir-feedback.v1` schema (Tasks 2, 5), renderer `data-*` attributes (Task 1). All spec sections map to tasks.
- **Placeholder scan:** none — every code step contains full code.
- **Type/name consistency:** `data-rule-id`↔`dataset.ruleId`, `#fbExport`/`#fbList`/`#fbCount`/`#fb-pill`/`#fb-popover`/`#fb-snippet`/`#fb-repl`/`#fb-note`/`#fb-save`/`#fb-cancel`, `window.__FEEDBACK_GET__`, `window.__SUMMARY__/__TITLE__/__SOURCE__`, category slugs, and `jmir-feedback.v1` are used identically across tasks. Blocks tuple widened to 5 consistently in `build` and both `render_html` loops.
```
