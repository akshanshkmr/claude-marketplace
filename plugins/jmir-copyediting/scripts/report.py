#!/usr/bin/env python3
"""
report.py — render a JMIR copyedit as a self-contained, interactive HTML report.

WHY THIS EXISTS
---------------
Applying tracked changes cleanly inside a real .docx is the one step agents are
unreliable at. This script sidesteps that: instead of writing Word, it produces a
single .html file the copyeditor opens in a browser to *see* every proposed edit
in context, then transcribes the ones they accept into Word themselves. The report
is the review surface; Word stays in human hands.

It renders the manuscript three ways from one marked-up DOM (toggled client-side):

    Original  — the manuscript as received, untouched.
    Diff      — every mechanical edit shown inline (deletion struck, insertion in
                green); every judgement item shown as an in-text query marker.
    Final     — auto edits applied (clean); query items left as the author's text
                with a marker, since those are confirmed with the author, not
                silently changed.

DATA SOURCES (two layers, same as the skill)
--------------------------------------------
    * Mechanical layer  — this script runs mechanical_edits.scan() itself, so the
                          ~100 deterministic edits are always present.
    * Judgement layer   — optional --edits FILE.json: a list of edit dicts the
                          agent emits (acronym expansions, value confirmations,
                          restructures, bespoke queries). These are merged in and
                          located in the text by their `original` string.

USAGE
-----
    python report.py MANUSCRIPT.docx --out report.html
    python report.py MANUSCRIPT.txt  --out report.html --title "My Paper: A Study"
    python report.py MANUSCRIPT.docx --edits judgement.json --out report.html

A judgement edit dict (all keys optional except original + para_index):
    {
      "para_index": 14,
      "original": "PHQ-9",
      "suggestion": "Patient Health Questionnaire-9 (PHQ-9)",
      "tag_type": "acronym expansion",   # free-text; drives the chip + colour family
      "mode": "auto",                    # "auto" => applied in Final; else => query
      "note": "Expand at first use (AMA 14.x)",
      "query": "..."                     # optional explicit author-query wording
    }
"""

from __future__ import annotations
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechanical_edits import (  # noqa: E402  (reuse the rule tables verbatim)
    ALL_RULE_GROUPS, _ACK_RE, _HEADING_HINT, _apply_repl, _read_paragraphs,
)

_URL_RE = re.compile(r"https?://\S+")


# ──────────────────────────────────────────────────────────────────────────────
# Edit extraction (mirrors mechanical_edits.scan() but keeps character spans so we
# can mark edits inline; the original scan() discards spans in favour of context).
# ──────────────────────────────────────────────────────────────────────────────

def _mechanical_edits_for(text: str, section: str) -> list[dict]:
    url_spans = [m.span() for m in _URL_RE.finditer(text)]
    found: list[dict] = []
    for category, group, mode in ALL_RULE_GROUPS:
        for rule_id, pattern, repl, note in group:
            for m in pattern.finditer(text):
                if rule_id != "flag.url" and any(s <= m.start() < e for s, e in url_spans):
                    continue
                if rule_id == "flag.normal":
                    tail = text[m.end():m.end() + 14].lower()
                    prev = text[max(0, m.start() - 3):m.start()].lower()
                    if tail.startswith(("ity", "ize", "iza", "ly", " distrib")) or prev == "log":
                        continue
                if rule_id == "rev.manuscript" and _ACK_RE.search(section):
                    continue
                suggestion = _apply_repl(repl, m)
                if suggestion == m.group(0):
                    continue
                found.append({
                    "start": m.start(), "end": m.end(),
                    "original": m.group(0), "suggestion": suggestion,
                    "note": note, "category": category, "mode": mode,
                    "rule_id": rule_id, "tag_type": _tag_type(rule_id, category),
                })
    return found


def _tag_type(rule_id: str, category: str) -> str:
    if rule_id.startswith("spell"):
        return "spelling"
    if rule_id.startswith("time."):
        return "time"
    if rule_id == "tm.symbols":
        return "symbol"
    if rule_id in ("swap.cronbach", "swap.cohen", "swap.fisher", "swap.hedges"):
        return "eponym"
    if rule_id.startswith("stat"):
        valueish = ("pvalue", "alpha", "ptoolow", "pequals", "kgm2")
        return "value" if any(k in rule_id for k in valueish) else "statistics"
    if category == "hyphenation":
        return "hyphenation"
    if category == "word-swap":
        return "word choice"
    if category == "phrase-flag":
        return "flag"
    return category


# tag-type -> colour family. Boldness is spent on the diff itself; tag families are
# a restrained four-hue system so the page stays calm.
_FAMILY = {
    "spelling": "style", "word choice": "style", "symbol": "style",
    "time": "style", "hyphenation": "style",
    "value": "stat", "statistics": "stat", "eponym": "stat",
    "acronym expansion": "struct", "structure": "struct", "metadata": "struct",
    "flag": "query", "query": "query",
}


def _family(tag_type: str, is_query: bool) -> str:
    if is_query:
        return "query"
    return _FAMILY.get(tag_type, "style")


def _merge_judgement(text: str, mech: list[dict], extra: list[dict]) -> list[dict]:
    """Locate each judgement edit's `original` in the paragraph and add it, skipping
    occurrences that overlap an edit already chosen."""
    occupied = [(e["start"], e["end"]) for e in mech]
    for e in extra:
        needle = e.get("original", "")
        if not needle:
            continue
        search_from = 0
        while True:
            idx = text.find(needle, search_from)
            if idx == -1:
                break
            span = (idx, idx + len(needle))
            if not any(s < span[1] and span[0] < en for s, en in occupied):
                tag = e.get("tag_type", "structure")
                mode = e.get("mode", "review")
                mech.append({
                    "start": span[0], "end": span[1],
                    "original": needle,
                    "suggestion": e.get("suggestion", needle),
                    "note": e.get("note", ""),
                    "category": tag, "mode": mode, "rule_id": "judgement",
                    "tag_type": tag, "query": e.get("query", ""),
                })
                occupied.append(span)
                break
            search_from = idx + 1
    return mech


def _dedupe_overlaps(edits: list[dict]) -> list[dict]:
    edits.sort(key=lambda e: (e["start"], -(e["end"] - e["start"])))
    chosen: list[dict] = []
    last_end = -1
    for e in edits:
        if e["start"] >= last_end:
            chosen.append(e)
            last_end = e["end"]
    return chosen


# ──────────────────────────────────────────────────────────────────────────────
# Structural classification (light heuristics for the front matter / headings)
# ──────────────────────────────────────────────────────────────────────────────

_AFFIL_RE = re.compile(r"^\s*\d+\s*[A-Z]")
_CORR_RE = re.compile(r"corresponding author|@|email", re.IGNORECASE)
_SUBLABEL_RE = re.compile(r"^(Background|Objective|Methods?|Results?|Conclusions?|Trial Registration|Aim|Design|Setting|Participants|Intervention|Main Outcome|Findings)\s*:", re.IGNORECASE)


def _looks_like_authors(s: str) -> bool:
    if len(s) > 220 or s.endswith("."):
        return False
    chunks = [c.strip() for c in re.split(r"[,;]|\band\b", s) if c.strip()]
    if not chunks:
        return False
    namelike = 0
    for c in chunks:
        c2 = re.sub(r"[\d,*†‡§¶]+$", "", c).strip()      # drop trailing affil markers
        toks = c2.split()
        if 1 < len(toks) <= 5 and all(re.match(r"^[A-Z][A-Za-z.'\-]*$", t) for t in toks):
            namelike += 1
    return namelike >= 1 and namelike >= len(chunks) // 2


def _classify(para: str, idx: int, title_idx: int) -> str:
    s = para.strip()
    if idx == title_idx:
        return "title"
    if _HEADING_HINT.match(s) and len(s) < 60:
        return "heading"
    if _CORR_RE.search(s) and len(s) < 160:
        return "corr"
    if _AFFIL_RE.match(s) and len(s) < 200:
        return "affil"
    if idx <= title_idx + 2 and _looks_like_authors(s):
        return "author"
    return "body"


# ──────────────────────────────────────────────────────────────────────────────
# Rendering
# ──────────────────────────────────────────────────────────────────────────────

def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _render_edit_span(e: dict, eid: str) -> str:
    is_query = e["mode"] != "auto"
    fam = _family(e["tag_type"], is_query)
    deletion = e["suggestion"] == ""               # pure removal (e.g. ® )
    diff_kind = "del" if deletion else "sub"
    klass = "edit-block" + (" is-query" if is_query else " is-auto") + f" fam-{fam}"
    detail = e.get("query") or e["note"] or e["tag_type"]
    attrs = (
        f'class="{klass}" data-eid="{eid}" data-edited="true" '
        f'data-diff="{diff_kind}" data-tag-type="{_esc(e["tag_type"])}" '
        f'data-rule-id="{_esc(e.get("rule_id", ""))}" '
        f'data-mode="{e["mode"]}" data-track-detail="{_esc(detail)}" tabindex="0"'
    )
    del_html = f'<span class="diff-del">{_esc(e["original"])}</span>'
    ins_html = "" if deletion else f'<span class="diff-ins">{_esc(e["suggestion"])}</span>'
    marker = f'<sup class="q-marker">{eid[1:]}</sup>' if is_query else ""
    return f'<span {attrs}>{del_html}{ins_html}{marker}</span>'


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


def _build_queries_and_rules(all_edits: list[dict]):
    """Group review/flag items into one query each (by rule/text); group auto items
    into applied-rule tallies. Returns (queries, rules) ready to render."""
    q_groups: dict[str, dict] = {}
    r_groups: dict[str, dict] = {}
    for e in all_edits:
        is_query = e["mode"] != "auto"
        fam = _family(e["tag_type"], is_query)
        if is_query:
            key = e.get("query") or f'{e["original"]}→{e["suggestion"]}|{e["note"]}'
            g = q_groups.setdefault(key, {
                "tag_type": e["tag_type"], "fam": fam, "note": e["note"],
                "original": e["original"], "suggestion": e["suggestion"],
                "query": e.get("query", ""), "eids": [],
            })
            g["eids"].append(e["eid"])
        else:
            key = f'{e["tag_type"]}|{e["note"]}'
            g = r_groups.setdefault(key, {
                "tag_type": e["tag_type"], "fam": fam, "note": e["note"],
                "examples": [], "count": 0,
            })
            g["count"] += 1
            if len(g["examples"]) < 6:
                g["examples"].append((e["original"], e["suggestion"]))
    return list(q_groups.values()), sorted(r_groups.values(), key=lambda g: -g["count"])


def _query_text(g: dict) -> str:
    if g["query"]:
        return g["query"]
    o, s = g["original"], g["suggestion"]
    if s.startswith("["):
        return f'{g["note"]} (instance: "{o}").'
    return f'We have changed "{o}" to "{s}" ({g["note"]}). Please confirm this preserves your intended meaning.'


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


def render_html(title: str, source_name: str, blocks: list[tuple[str, str, list[dict], int, str]]) -> str:
    counter = [0]
    body_html_parts = []
    for cls, text, edits, pidx, section in blocks:
        body_html_parts.append(_render_paragraph(text, edits, cls, counter, pidx, section))

    # re-walk to attach eids to the flat edit list for sidebar grouping
    flat: list[dict] = []
    cid = 0
    for _cls, _text, edits, _pidx, _section in blocks:
        # account for author paragraphs producing no edit ids
        if _cls == "author":
            continue
        for e in edits:
            cid += 1
            e2 = dict(e)
            e2["eid"] = f"e{cid}"
            flat.append(e2)
    # NOTE: counter above and cid here must increment identically — author paras
    # carry no edits, and we render their edits=[] (see build step), so they match.

    queries, rules = _build_queries_and_rules(flat)
    n_auto = sum(1 for e in flat if e["mode"] == "auto")
    n_query = len(queries)

    summary = {
        "autoApplied": n_auto,
        "queries": n_query,
        "queryList": [f"Q{i}: {_query_text(g)}"
                      for i, g in enumerate(sorted(queries, key=lambda x: x["fam"]), 1)],
    }

    # sidebar: queries
    q_items = []
    for i, g in enumerate(sorted(queries, key=lambda x: x["fam"]), 1):
        ids = " ".join(g["eids"])
        qtext = _query_text(g)
        count = len(g["eids"])
        badge = f'<span class="qi-count">{count}×</span>' if count > 1 else ""
        q_items.append(
            f'<div class="query-item fam-{g["fam"]}" data-targets="{ids}" data-q="{i}">'
            f'<div class="qi-head"><span class="qi-num">Q{i}</span>'
            f'<span class="chip">{_esc(g["tag_type"])}</span>{badge}'
            f'<button class="qi-check" title="Mark resolved" aria-label="Mark resolved">✓</button></div>'
            f'<p class="qi-text">{_esc(qtext)}</p>'
            f'<button class="qi-copy" title="Copy query">Copy query</button>'
            f'</div>'
        )

    # sidebar: applied rules
    r_items = []
    for g in rules:
        ex = ", ".join(f'{_esc(o)}→{_esc(s) or "∅"}' for o, s in g["examples"][:3])
        r_items.append(
            f'<div class="rule-item fam-{g["fam"]}">'
            f'<div class="ri-head"><span class="chip">{_esc(g["tag_type"])}</span>'
            f'<span class="ri-count">{g["count"]}×</span></div>'
            f'<p class="ri-note">{_esc(g["note"])}</p>'
            f'<p class="ri-ex">{ex}</p>'
            f'</div>'
        )

    insights = _build_insights_text(title, source_name, n_auto, queries)

    data = {
        "title": title, "source": source_name,
        "auto": n_auto, "queries": n_query,
    }

    doc = (
        _HEAD
        + f"<title>{_esc(title)} — JMIR copyedit</title>\n"
        + _STYLE
        + "</head>\n<body data-view=\"diff\">\n"
        + _topbar(title, source_name, n_auto, n_query)
        + '<div class="stage">\n'
        + '  <main class="paper-wrap"><article class="paper" id="paper">\n'
        + "\n".join(body_html_parts)
        + "\n  </article></main>\n"
        + '  <aside class="sidebar">\n'
        + _sidebar_header(n_auto, n_query)
        + '    <div class="side-scroll">\n'
        + '      <section class="side-sec" data-pane="queries">\n'
        + (("".join(q_items)) or '<p class="empty">No author queries — nothing needs confirming.</p>')
        + "\n      </section>\n"
        + '      <section class="side-sec" data-pane="rules" hidden>\n'
        + (("".join(r_items)) or '<p class="empty">No mechanical edits were needed.</p>')
        + "\n      </section>\n"
        + '      <section class="side-sec" data-pane="feedback" hidden>\n'
        + '        <div id="fbList"></div>\n'
        + "      </section>\n"
        + "    </div>\n  </aside>\n</div>\n"
        + '<div class="toast" id="toast"></div>\n'
        + '<button class="fb-pill" id="fb-pill">+ Add feedback</button>\n'
        + _fb_popover_html()
        + "<script>\nwindow.__INSIGHTS__ = " + json.dumps(insights) + ";\n"
        + "window.__MSID__ = " + json.dumps("jmir-" + re.sub(r"\W+", "-", title.lower())[:48]) + ";\n"
        + "window.__SUMMARY__ = " + json.dumps(summary) + ";\n"
        + "window.__TITLE__ = " + json.dumps(title) + ";\n"
        + "window.__SOURCE__ = " + json.dumps(source_name) + ";\n"
        + _SCRIPT + "\n</script>\n</body>\n</html>\n"
    )
    return doc


def _build_insights_text(title, source, n_auto, queries) -> str:
    lines = [f"JMIR COPYEDIT — {title}", f"Source: {source}", "",
             f"{n_auto} mechanical edits applied · {len(queries)} author queries", ""]
    lines.append("AUTHOR QUERIES")
    for i, g in enumerate(sorted(queries, key=lambda x: x["fam"]), 1):
        lines.append(f"  Q{i} [{g['tag_type']}] {_query_text(g)}")
    return "\n".join(lines)


# ── chrome fragments ────────────────────────────────────────────────────────────

def _topbar(title, source, n_auto, n_query) -> str:
    return (
        '<header class="topbar">\n'
        '  <div class="brand"><span class="mark">JMIR</span>'
        '<span class="brand-sub">copyedit review</span></div>\n'
        '  <div class="seg" role="tablist" aria-label="View">\n'
        '    <button class="seg-btn" data-vw="original" role="tab">Original</button>\n'
        '    <button class="seg-btn is-on" data-vw="diff" role="tab" aria-selected="true">Diff</button>\n'
        '    <button class="seg-btn" data-vw="final" role="tab">Final</button>\n'
        '  </div>\n'
        '  <div class="tb-right">\n'
        '    <label class="zoom"><span class="zi">A</span>'
        '<input type="range" id="zoom" min="85" max="150" value="100" aria-label="Zoom">'
        '<span class="za">A</span></label>\n'
        '    <button class="btn-copy" id="fbExport">Export feedback</button>\n'
        '  </div>\n'
        '</header>\n'
    )


def _sidebar_header(n_auto, n_query) -> str:
    total = n_auto + n_query
    return (
        '    <div class="side-head">\n'
        f'      <div class="stat"><b>{n_auto}</b><span>applied</span></div>\n'
        f'      <div class="stat"><b>{n_query}</b><span>queries</span></div>\n'
        '      <div class="prog"><div class="prog-bar" id="progBar"></div>'
        '<span class="prog-txt" id="progTxt">0 of ' + str(n_query) + ' resolved</span></div>\n'
        '      <div class="side-tabs">\n'
        '        <button class="st-btn is-on" data-pane="queries">Queries</button>\n'
        '        <button class="st-btn" data-pane="rules">Rules applied</button>\n'
        '        <button class="st-btn" data-pane="feedback">Feedback '
        '<span class="st-count" id="fbCount">0</span></button>\n'
        '      </div>\n'
        '    </div>\n'
    )


# ── static head / style / script (no f-strings: braces are literal) ──────────────

_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
"""

_STYLE = """<style>
:root{
  --bg:#0c0e13; --bg-2:#10131b; --panel:#141824; --panel-2:#191e2c;
  --line:rgba(255,255,255,.08); --line-2:rgba(255,255,255,.13);
  --ui:#e7eaf2; --ui-dim:#9aa3b8; --ui-faint:#646e85;
  --paper:#fffdf8; --paper-edge:#ece7da; --ink:#23262e; --ink-dim:#5d6470;
  --ins:#16915a; --ins-bg:#e4f6ec; --del:#c8324c; --del-bg:#fce8ec;
  --fam-style:#6366f1; --fam-stat:#0d9488; --fam-struct:#0e8f6e; --fam-query:#c97a16;
  --fam-query-bg:#fdf3e0;
  --shadow:0 24px 60px -22px rgba(0,0,0,.65), 0 2px 8px rgba(0,0,0,.3);
  --ser:'Lora',Georgia,'Times New Roman',serif;
  --disp:'Outfit',system-ui,sans-serif;
  --ui-font:'Plus Jakarta Sans',system-ui,sans-serif;
  --zoom:1;
}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%}
body{
  min-height:100vh;
  background:
    radial-gradient(1100px 520px at 78% -8%, #1a2030 0%, transparent 60%),
    radial-gradient(900px 480px at 6% 4%, #15263a 0%, transparent 55%),
    var(--bg);
  background-attachment:fixed;
  color:var(--ui); font-family:var(--ui-font);
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}

/* ── topbar ─────────────────────────────────────────── */
.topbar{
  position:sticky; top:0; z-index:30; display:flex; align-items:center;
  gap:18px; padding:11px 22px; border-bottom:1px solid var(--line);
  background:rgba(12,14,19,.72); backdrop-filter:blur(14px) saturate(1.3);
  -webkit-backdrop-filter:blur(14px) saturate(1.3);
}
.brand{display:flex; align-items:baseline; gap:9px; font-family:var(--disp)}
.mark{
  font-weight:700; letter-spacing:.14em; font-size:14px; color:#fff;
  background:linear-gradient(135deg,#3b82f6,#6366f1); padding:5px 9px;
  border-radius:7px; box-shadow:0 3px 14px -4px rgba(99,102,241,.8);
}
.brand-sub{font-size:12.5px; color:var(--ui-dim); letter-spacing:.02em}
.seg{
  margin:0 auto; display:flex; gap:2px; padding:3px;
  background:var(--panel); border:1px solid var(--line); border-radius:11px;
}
.seg-btn{
  font:500 13px/1 var(--disp); color:var(--ui-dim); background:transparent;
  border:0; padding:8px 16px; border-radius:8px; cursor:pointer;
  transition:color .18s, background .18s;
}
.seg-btn:hover{color:var(--ui)}
.seg-btn.is-on{color:#fff; background:linear-gradient(180deg,#2a3142,#222838); box-shadow:0 1px 0 rgba(255,255,255,.05) inset, 0 2px 10px -4px #000}
.tb-right{display:flex; align-items:center; gap:16px}
.zoom{display:flex; align-items:center; gap:8px; color:var(--ui-faint)}
.zoom .zi{font:600 11px var(--ser)} .zoom .za{font:600 17px var(--ser)}
input[type=range]{
  -webkit-appearance:none; appearance:none; width:104px; height:4px; border-radius:99px;
  background:var(--line-2); outline:none; cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none; width:14px; height:14px; border-radius:50%;
  background:#fff; box-shadow:0 1px 5px rgba(0,0,0,.5); cursor:pointer;
}
input[type=range]::-moz-range-thumb{width:14px;height:14px;border:0;border-radius:50%;background:#fff;cursor:pointer}
.btn-copy{
  font:600 12.5px var(--disp); color:var(--ui); cursor:pointer;
  background:var(--panel-2); border:1px solid var(--line-2); border-radius:9px;
  padding:8px 14px; transition:border-color .18s, transform .12s;
}
.btn-copy:hover{border-color:#3b82f6}
.btn-copy:active{transform:translateY(1px)}

/* ── stage: paper + sidebar ─────────────────────────── */
.stage{display:grid; grid-template-columns:minmax(0,1fr) 372px; align-items:start}
.paper-wrap{padding:46px 32px 120px; display:flex; justify-content:center; min-width:0}
.paper{
  width:100%; max-width:760px; background:var(--paper); color:var(--ink);
  border:1px solid var(--paper-edge); border-radius:5px; box-shadow:var(--shadow);
  padding:72px clamp(40px,6vw,82px) 96px;
  font-family:var(--ser); font-size:calc(16.5px*var(--zoom)); line-height:1.72;
}

/* manuscript semantics */
.jrnlArticleTitle{
  font:600 calc(27px*var(--zoom))/1.24 var(--ser); margin:0 0 18px; color:#15171d;
  letter-spacing:-.01em;
}
.ms-authors{margin:0 0 6px; font-size:calc(15px*var(--zoom)); line-height:1.6}
.jrnlAuthor{color:#1f2430; font-weight:500}
.jrnlAuthor::after{content:""}
.jrnlAffil{margin:2px 0; font-size:calc(12.5px*var(--zoom)); color:var(--ink-dim); font-style:italic; line-height:1.5}
.jrnlCorr{margin:10px 0 4px; font-size:calc(12.5px*var(--zoom)); color:var(--ink-dim)}
.jrnlSectionHead{
  font:600 calc(13px*var(--zoom)) var(--disp); text-transform:uppercase;
  letter-spacing:.13em; color:#3b4252; margin:34px 0 10px;
  padding-bottom:7px; border-bottom:1px solid #efeadd;
}
.jrnlSubhead{font-weight:600; color:#2b303b; font-family:var(--ser)}
.ms-body{margin:0 0 15px; text-align:justify; hyphens:auto}
.paper :first-child{margin-top:0}

/* ── inline edits ───────────────────────────────────── */
.edit-block{border-radius:3px; padding:0 .5px; transition:background .15s}
.diff-del,.diff-ins{border-radius:3px; padding:0 1px}
/* default (diff) rendering */
.diff-del{color:var(--del); background:var(--del-bg); text-decoration:line-through; text-decoration-thickness:1.5px}
.diff-ins{color:var(--ins); background:var(--ins-bg); margin-left:2px}
.q-marker{
  font:600 10px var(--ui-font); color:#fff; background:var(--fam-query);
  border-radius:50%; padding:1px 4px; margin-left:2px; vertical-align:super;
  font-size:9.5px; line-height:1;
}
.edit-block.is-query .diff-del{
  color:inherit; background:var(--fam-query-bg);
  text-decoration:underline; text-decoration-style:dotted;
  text-decoration-color:var(--fam-query); text-underline-offset:3px;
}
.edit-block.is-query .diff-ins{display:none}
.edit-block:hover{background:rgba(99,102,241,.10)}
.edit-block.flash,.flash{animation:flash 1.1s ease}
@keyframes flash{0%,100%{background:transparent}25%{background:#fff3bf}}

/* family accents on the auto insertion underline */
.fam-style.is-auto .diff-ins{box-shadow:inset 0 -2px 0 color-mix(in srgb,var(--fam-style) 55%,transparent)}
.fam-stat.is-auto  .diff-ins{box-shadow:inset 0 -2px 0 color-mix(in srgb,var(--fam-stat) 55%,transparent)}
.fam-struct.is-auto .diff-ins{box-shadow:inset 0 -2px 0 color-mix(in srgb,var(--fam-struct) 55%,transparent)}

/* view states */
body[data-view="original"] .diff-ins{display:none}
body[data-view="original"] .diff-del{color:inherit; background:transparent; text-decoration:none}
body[data-view="original"] .edit-block.is-query .diff-del{color:inherit; background:transparent; text-decoration:none}
body[data-view="original"] .q-marker{display:none}
body[data-view="original"] .edit-block:hover{background:transparent}

body[data-view="final"] .edit-block.is-auto .diff-del{display:none}
body[data-view="final"] .edit-block.is-auto .diff-ins{color:inherit; background:transparent; box-shadow:none; margin-left:0}
body[data-view="final"] .edit-block.is-query .diff-del{color:inherit; background:var(--fam-query-bg)}
/* final keeps query markers so the author still sees what to confirm */

/* ── sidebar ────────────────────────────────────────── */
.sidebar{
  position:sticky; top:53px; height:calc(100vh - 53px); display:flex; flex-direction:column;
  background:linear-gradient(180deg,var(--bg-2),var(--bg)); border-left:1px solid var(--line);
}
.side-head{padding:18px 20px 12px; border-bottom:1px solid var(--line)}
.stat{display:inline-flex; align-items:baseline; gap:6px; margin-right:18px}
.stat b{font:700 22px var(--disp); color:#fff}
.stat span{font-size:12px; color:var(--ui-dim)}
.prog{position:relative; height:4px; margin:16px 0 4px; border-radius:99px; background:var(--line-2)}
.prog-bar{height:4px; border-radius:99px; background:linear-gradient(90deg,#3b82f6,#6366f1); width:0%; transition:width .3s}
.prog-txt{position:absolute; right:0; top:9px; font-size:11px; color:var(--ui-faint)}
.side-tabs{display:flex; gap:6px; margin-top:26px}
.st-btn{
  font:600 12px var(--disp); color:var(--ui-dim); background:transparent;
  border:1px solid var(--line); border-radius:8px; padding:7px 12px; cursor:pointer;
}
.st-btn.is-on{color:#fff; background:var(--panel); border-color:var(--line-2)}
.side-scroll{overflow-y:auto; padding:14px 16px 40px; flex:1}
.side-scroll::-webkit-scrollbar{width:9px}
.side-scroll::-webkit-scrollbar-thumb{background:var(--line-2); border-radius:9px; border:2px solid transparent; background-clip:padding-box}

.query-item,.rule-item{
  position:relative; background:var(--panel); border:1px solid var(--line);
  border-left:3px solid var(--fam-style); border-radius:11px; padding:12px 13px;
  margin-bottom:10px;
}
.fam-style{border-left-color:var(--fam-style)}
.fam-stat{border-left-color:var(--fam-stat)}
.fam-struct{border-left-color:var(--fam-struct)}
.fam-query{border-left-color:var(--fam-query)}
.qi-head,.ri-head{display:flex; align-items:center; gap:8px; margin-bottom:7px}
.qi-num{font:700 12px var(--disp); color:#fff}
.chip{
  font:600 10.5px var(--ui-font); letter-spacing:.02em; color:var(--ui-dim);
  background:var(--panel-2); border:1px solid var(--line); border-radius:99px;
  padding:3px 9px; text-transform:lowercase;
}
.fam-stat .chip{color:#5eead4} .fam-struct .chip{color:#6ee7b7}
.fam-query .chip{color:#f3c178} .fam-style .chip{color:#a5b4fc}
.qi-count,.ri-count{margin-left:auto; font:600 11px var(--ui-font); color:var(--ui-faint)}
.ri-count{color:var(--ui-dim)}
.qi-check{
  margin-left:6px; width:24px; height:24px; border-radius:7px; cursor:pointer;
  background:var(--panel-2); border:1px solid var(--line-2); color:var(--ui-faint);
  font-size:13px; line-height:1; transition:all .15s;
}
.qi-check:hover{color:var(--ins); border-color:var(--ins)}
.query-item.done{opacity:.5}
.query-item.done .qi-check{background:var(--ins); border-color:var(--ins); color:#fff}
.qi-text,.ri-note{margin:0; font-size:13px; line-height:1.55; color:var(--ui)}
.ri-note{color:var(--ui-dim)}
.ri-ex{margin:6px 0 0; font:400 11.5px var(--ser); color:var(--ui-faint)}
.qi-copy{
  margin-top:9px; font:600 11px var(--disp); color:var(--ui-dim); cursor:pointer;
  background:transparent; border:1px solid var(--line-2); border-radius:7px; padding:5px 10px;
}
.qi-copy:hover{color:#fff; border-color:#3b82f6}
.query-item.hot{box-shadow:0 0 0 1px #3b82f6, 0 8px 24px -12px rgba(59,130,246,.7)}
.empty{color:var(--ui-faint); font-size:13px; padding:8px 4px}

/* ── toast ──────────────────────────────────────────── */
.toast{
  position:fixed; bottom:26px; left:50%; transform:translateX(-50%) translateY(20px);
  background:#fff; color:#15171d; font:600 13px var(--disp); padding:11px 18px;
  border-radius:10px; box-shadow:0 12px 40px -10px rgba(0,0,0,.6); opacity:0;
  pointer-events:none; transition:opacity .25s, transform .25s; z-index:50;
}
.toast.show{opacity:1; transform:translateX(-50%) translateY(0)}

@media (max-width:1080px){
  .stage{grid-template-columns:1fr}
  .sidebar{position:static; height:auto; border-left:0; border-top:1px solid var(--line)}
  .side-scroll{max-height:none}
  .paper-wrap{padding:30px 16px 60px}
}
@media (prefers-reduced-motion:reduce){
  *{transition:none!important; animation:none!important}
}

/* ── feedback (sidebar) ─────────────────────────────────── */
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
/* ── feedback (pill + popover) ──────────────────────────────── */
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
</style>
"""

_SCRIPT = """
(function(){
  var body=document.body, store=null;
  try{ store=window.localStorage; var t='__t'; store.setItem(t,t); store.removeItem(t); }
  catch(e){ store=null; }                       // sandboxed iframe → degrade, never crash
  var KEY=window.__MSID__||'jmir';
  function load(k,d){ try{ var v=store&&store.getItem(KEY+':'+k); return v==null?d:JSON.parse(v);}catch(e){return d;} }
  function save(k,v){ try{ store&&store.setItem(KEY+':'+k, JSON.stringify(v)); }catch(e){} }

  /* view toggle */
  function setView(v){
    body.setAttribute('data-view', v);
    document.querySelectorAll('.seg-btn').forEach(function(b){
      var on=b.dataset.vw===v; b.classList.toggle('is-on',on);
      if(on){b.setAttribute('aria-selected','true');} else {b.removeAttribute('aria-selected');}
    });
    save('view', v);
  }
  document.querySelectorAll('.seg-btn').forEach(function(b){
    b.addEventListener('click', function(){ setView(b.dataset.vw); });
  });
  setView(load('view','diff'));

  /* zoom */
  var zoom=document.getElementById('zoom');
  function setZoom(z){ document.documentElement.style.setProperty('--zoom', (z/100).toFixed(3)); zoom.value=z; save('zoom',z); }
  zoom.addEventListener('input', function(){ setZoom(+zoom.value); });
  setZoom(load('zoom',100));

  /* keyboard 1/2/3 */
  document.addEventListener('keydown', function(e){
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return;
    if(e.key==='1') setView('original');
    if(e.key==='2') setView('diff');
    if(e.key==='3') setView('final');
  });

  /* sidebar pane tabs */
  document.querySelectorAll('.st-btn').forEach(function(b){
    b.addEventListener('click', function(){
      document.querySelectorAll('.st-btn').forEach(function(x){x.classList.toggle('is-on',x===b);});
      document.querySelectorAll('.side-sec').forEach(function(s){ s.hidden = s.dataset.pane!==b.dataset.pane; });
    });
  });

  var toast=document.getElementById('toast'), tt;
  function flash(msg){ toast.textContent=msg; toast.classList.add('show'); clearTimeout(tt); tt=setTimeout(function(){toast.classList.remove('show');},1700); }
  function copy(text,msg){
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(function(){flash(msg);}); }
    else{ var ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');flash(msg);}catch(e){} ta.remove(); }
  }

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

  /* query <-> in-text linking */
  document.querySelectorAll('.query-item').forEach(function(qi){
    var ids=(qi.dataset.targets||'').split(/\\s+/).filter(Boolean);
    qi.addEventListener('click', function(ev){
      if(ev.target.closest('.qi-copy')||ev.target.closest('.qi-check')) return;
      var first=null;
      ids.forEach(function(id){
        var el=document.querySelector('[data-eid="'+id+'"]');
        if(el){ if(!first)first=el; el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); }
      });
      document.querySelectorAll('.query-item').forEach(function(x){x.classList.toggle('hot',x===qi);});
      if(first) first.scrollIntoView({behavior:'smooth', block:'center'});
    });
    var copyBtn=qi.querySelector('.qi-copy');
    if(copyBtn) copyBtn.addEventListener('click', function(){ copy(qi.querySelector('.qi-text').textContent, 'Query copied'); });
  });

  /* in-text edit → its query */
  document.querySelectorAll('.edit-block.is-query').forEach(function(el){
    el.addEventListener('click', function(){
      var id=el.dataset.eid;
      var qi=Array.prototype.find.call(document.querySelectorAll('.query-item'), function(q){
        return (q.dataset.targets||'').split(/\\s+/).indexOf(id)>=0;
      });
      if(qi){
        document.querySelector('.st-btn[data-pane="queries"]').click();
        document.querySelectorAll('.query-item').forEach(function(x){x.classList.toggle('hot',x===qi);});
        qi.scrollIntoView({behavior:'smooth', block:'center'});
      }
    });
  });

  /* resolve checkboxes + progress (persisted) */
  var resolved=load('resolved',{});
  var qItems=document.querySelectorAll('.query-item');
  function refreshProg(){
    var done=0; qItems.forEach(function(q){ if(resolved[q.dataset.q]) done++; });
    var total=qItems.length;
    var bar=document.getElementById('progBar'), txt=document.getElementById('progTxt');
    if(bar) bar.style.width=(total? (done/total*100):0)+'%';
    if(txt) txt.textContent=done+' of '+total+' resolved';
  }
  qItems.forEach(function(q){
    var k=q.dataset.q;
    if(resolved[k]) q.classList.add('done');
    var cb=q.querySelector('.qi-check');
    if(cb) cb.addEventListener('click', function(e){
      e.stopPropagation();
      resolved[k]=!resolved[k]; q.classList.toggle('done',!!resolved[k]);
      save('resolved',resolved); refreshProg();
    });
  });
  refreshProg();
})();

(function(){
  var paper=document.getElementById('paper'); if(!paper) return;
  var store=null; try{ store=window.localStorage; }catch(e){ store=null; }
  var KEY=window.__MSID__||'jmir';
  function load(k,d){ try{ var v=store&&store.getItem(KEY+':'+k); return v==null?d:JSON.parse(v);}catch(e){return d;} }
  function save(k,v){ try{ store&&store.setItem(KEY+':'+k, JSON.stringify(v)); }catch(e){} }
  function esc(s){ return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function closest(node,sel){ var el=node&&node.nodeType===1?node:(node&&node.parentElement); return el?el.closest(sel):null; }

  var items=load('feedback',[]);  // key: ':feedback'
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
    if(item.dataset.pidx==='-1') return;
    var p=paper.querySelector('[data-pidx="'+item.dataset.pidx+'"]');
    if(p){ p.classList.remove('flash'); void p.offsetWidth; p.classList.add('flash'); p.scrollIntoView({behavior:'smooth',block:'center'}); }
  });

  window.__FEEDBACK_GET__=function(){ return items.slice(); };
  renderList();
})();
"""


# ──────────────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────────────

def build(manuscript: Path, edits_file: Path | None, title: str | None) -> str:
    paragraphs = _read_paragraphs(manuscript)
    nonempty = [(i, p) for i, p in enumerate(paragraphs) if p.strip()]
    title_idx = nonempty[0][0] if nonempty else 0
    resolved_title = title or (paragraphs[title_idx].strip() if nonempty else manuscript.stem)

    extra_by_para: dict[int, list[dict]] = {}
    if edits_file:
        data = json.loads(Path(edits_file).read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("edits", data.get("findings", []))
        for e in items:
            extra_by_para.setdefault(int(e.get("para_index", -1)), []).append(e)

    section = "(start)"
    blocks: list[tuple[str, str, list[dict], int, str]] = []
    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue
        s = para.strip()
        if _HEADING_HINT.match(s) and len(s) < 60:
            section = s
        cls = _classify(para, i, title_idx)
        if cls == "author":
            blocks.append((cls, para, [], i, section))   # authors carry no inline edits
            continue
        edits = _mechanical_edits_for(para, section)
        edits = _merge_judgement(para, edits, extra_by_para.get(i, []))
        edits = _dedupe_overlaps(edits)
        blocks.append((cls, para, edits, i, section))

    return render_html(resolved_title, manuscript.name, blocks)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a JMIR copyedit as an interactive HTML report")
    ap.add_argument("manuscript", help="path to .docx or .txt")
    ap.add_argument("--out", required=True, metavar="OUT.html", help="output HTML path")
    ap.add_argument("--edits", metavar="EDITS.json",
                    help="optional judgement-layer edits to merge (list of edit dicts)")
    ap.add_argument("--title", help="manuscript title (else inferred from first line)")
    args = ap.parse_args(argv)

    src = Path(args.manuscript)
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        return 2

    out_html = build(src, Path(args.edits) if args.edits else None, args.title)
    Path(args.out).write_text(out_html, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
