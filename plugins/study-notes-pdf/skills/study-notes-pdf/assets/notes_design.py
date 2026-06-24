# -*- coding: utf-8 -*-
"""
notes_design.py  —  A reusable, subject-agnostic design system for producing
modern, colourful "Notion / Linear"-style study-note PDFs.

The visual craft (palette, fonts, rounded cards, airy tables, pill tags,
per-module accent colours) is encoded here so callers only supply CONTENT.

Quick start
-----------
    from notes_design import StudyNotes

    nb = StudyNotes()
    nb.cover(
        kicker="UNIVERSITY · COURSE-CODE",
        title_lines=["Operating", "Systems"],        # 1st line light, rest bold
        subtitle="Final Exam · Complete Study Notes",
        facts=[("90 MINUTES","indigo"), ("40 MARKS","emerald")],
        roadmap=[("01","indigo","Processes & Threads","scheduling · context switch"),
                 ("02","blue","Memory Management","paging · segmentation · TLB")],
        footnote="Compiled from lecture slides and the textbook.")
    nb.page_break()

    nb.chapter("01","Processes & Threads","FOUNDATIONS","Weeks 1-2", theme="indigo")
    nb.section("1.1","Process States")
    nb.text("A process moves between New, Ready, Running, Waiting and Terminated.")
    nb.table(["State","Meaning"], [["Ready","waiting for CPU"],["Running","on the CPU"]],
             [4*nb.cm, 13*nb.cm])
    nb.callout("Exam tip", "Draw the 5-state diagram; label every transition.")
    nb.save("/mnt/user-data/outputs/OS_Notes.pdf", subject="Operating Systems · CS-302")

Themes (accent colours), use any by name:
    indigo · blue · cyan · emerald · amber · rose · violet · pink · slate
Convention used in the example notes:
    each chapter gets its own theme; numericals=violet, practice=pink, reference=slate.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── Fonts ─────────────────────────────────────────────────────────────────────
# DejaVu ships on most Linux images and crucially includes an ExtraLight weight
# (for the airy hero numerals) plus full coverage of Greek / maths / arrow
# glyphs and proper sub/superscripts. Registration is defensive: any missing
# weight quietly falls back so the library never hard-fails.
_DV = '/usr/share/fonts/truetype/dejavu/'
def _reg(name, filename, fallback='Sans'):
    try:
        pdfmetrics.registerFont(TTFont(name, _DV + filename)); return name
    except Exception:
        return fallback
_reg('Sans',    'DejaVuSans.ttf')
_reg('Sans-B',  'DejaVuSans-Bold.ttf')
_reg('Sans-I',  'DejaVuSans-Oblique.ttf')
_reg('Sans-BI', 'DejaVuSans-BoldOblique.ttf')
_EL = _reg('Sans-EL', 'DejaVuSans-ExtraLight.ttf')   # falls back to 'Sans'
_reg('Mono',    'DejaVuSansMono.ttf')
_reg('Mono-B',  'DejaVuSansMono-Bold.ttf')
try:
    registerFontFamily('Sans', normal='Sans', bold='Sans-B', italic='Sans-I', boldItalic='Sans-BI')
    registerFontFamily('Mono', normal='Mono', bold='Mono-B')
except Exception:
    pass

# ── Palette ─────────────────────────────────────────────────────────────────
INK   = colors.HexColor('#1B1F2A')
INK2  = colors.HexColor('#3A4255')
MUTE  = colors.HexColor('#6B7280')
FAINT = colors.HexColor('#9AA2B1')
LINE  = colors.HexColor('#ECEEF3')
PAPER = colors.white
STAR  = colors.HexColor('#F59E0B')
ZEBRA = colors.HexColor('#FAFBFC')

# per theme: a=vivid accent, d=darker (text on tint), t=card tint, h=table-header tint
_TH = {
 'indigo': dict(a='#6366F1', d='#4338CA', t='#EEF0FE', h='#E5E8FE'),
 'blue':   dict(a='#3B82F6', d='#1D4ED8', t='#EAF2FE', h='#DEEBFD'),
 'cyan':   dict(a='#0EA5B7', d='#0E7490', t='#E4F6F9', h='#D2EFF4'),
 'emerald':dict(a='#10B981', d='#047857', t='#E6F8F1', h='#D4F2E6'),
 'amber':  dict(a='#F59E0B', d='#B45309', t='#FEF4E2', h='#FCEAC6'),
 'rose':   dict(a='#F43F5E', d='#BE123C', t='#FEECEF', h='#FBDBE1'),
 'violet': dict(a='#8B5CF6', d='#6D28D9', t='#F2ECFE', h='#E9DDFC'),
 'pink':   dict(a='#EC4899', d='#BE185D', t='#FCEAF4', h='#FAD9EB'),
 'slate':  dict(a='#475569', d='#334155', t='#EEF1F5', h='#E2E7EE'),
}
THEMES = list(_TH.keys())
def _theme(name):
    x = _TH.get(name, _TH['indigo'])
    return (colors.HexColor(x['a']), colors.HexColor(x['d']),
            colors.HexColor(x['t']), colors.HexColor(x['h']))

# ── Paragraph styles ─────────────────────────────────────────────────────────
def _P(n, **k): return ParagraphStyle(n, **k)
_S = {
 'hero':   _P('hero',   fontName=_EL, fontSize=34, leading=39, textColor=INK),
 'cv_sub': _P('cv_sub', fontName='Sans', fontSize=12.5, leading=18, textColor=MUTE),
 'mod_no': _P('mod_no', fontName=_EL, fontSize=46, leading=46),
 'mod_ttl':_P('mod_ttl',fontName='Sans-B', fontSize=18, leading=22, textColor=INK),
 'mod_sub':_P('mod_sub',fontName='Sans', fontSize=9, leading=13, textColor=MUTE),
 'sec':    _P('sec',    fontName='Sans-B', fontSize=12.5, leading=16, textColor=INK),
 'subsec': _P('subsec', fontName='Sans-B', fontSize=9.8, leading=13, spaceBefore=6, spaceAfter=3),
 'body':   _P('body',   fontName='Sans', fontSize=9, leading=14, textColor=INK2, spaceAfter=3, alignment=TA_JUSTIFY),
 'b1':     _P('b1',     fontName='Sans', fontSize=9, leading=14, textColor=INK2, leftIndent=14, firstLineIndent=-11, spaceAfter=2.5),
 'co_lbl': _P('co_lbl', fontName='Sans-B', fontSize=8, leading=11),
 'cell':   _P('cell',   fontName='Sans', fontSize=8.6, leading=12.2, textColor=INK2),
 'cell_b': _P('cell_b', fontName='Sans-B', fontSize=8.6, leading=12.2, textColor=INK),
 'cell_h': _P('cell_h', fontName='Sans-B', fontSize=8.6, leading=11.5),
 'formula':_P('formula',fontName='Mono-B', fontSize=11, leading=16, textColor=INK, alignment=TA_CENTER),
 'formula_s':_P('formula_s',fontName='Mono', fontSize=9.3, leading=14, textColor=INK2, alignment=TA_CENTER),
 'title_blk':_P('title_blk', fontName='Sans-B', fontSize=12, leading=15, textColor=INK),
 'toc_t':  _P('toc_t',  fontName='Sans-B', fontSize=9.5, leading=12, textColor=INK),
 'toc_d':  _P('toc_d',  fontName='Sans', fontSize=7.8, leading=10.6, textColor=MUTE),
}

def sp(n=1): return Spacer(1, n * 3.4 * mm)
def stars(n_full, n_total=3):
    """Return gold-star markup, e.g. stars(3) -> '★★★'."""
    return f'<font name="Sans" color="#F59E0B">{"★"*int(n_full)}</font>'


class StudyNotes:
    """Accumulates flowables in `self.story`; each method appends styled content."""

    cm = cm
    mm = mm
    THEMES = THEMES

    def __init__(self, content_width_cm=17.0, margins_cm=(2.0, 2.0, 1.7, 1.8),
                 page=A4, footer_accent='#6366F1'):
        self.W = content_width_cm * cm
        self._mL, self._mR, self._mT, self._mB = margins_cm
        self._page = page
        self._theme = 'indigo'
        self._footer_accent = colors.HexColor(footer_accent)
        self._footer_text = ''
        self.story = []

    # ── low-level helpers (return flowables) ──────────────────────────────────
    def _pill(self, text, bg, fg, size=7.8, padx=7, pady=2.5, font='Sans-B'):
        stl = ParagraphStyle('p', fontName=font, fontSize=size, leading=size+3,
                             textColor=fg, alignment=TA_CENTER)
        tw = pdfmetrics.stringWidth(text, font, size) + 2*padx + 3
        return Table([[Paragraph(text, stl)]], colWidths=[tw], style=TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),bg),('ROUNDEDCORNERS',[7,7,7,7]),
            ('LEFTPADDING',(0,0),(-1,-1),padx),('RIGHTPADDING',(0,0),(-1,-1),padx),
            ('TOPPADDING',(0,0),(-1,-1),pady),('BOTTOMPADDING',(0,0),(-1,-1),pady),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

    def _card(self, flows, bg, radius=9, pad=11, width=None):
        width = width or self.W
        return Table([[flows]], colWidths=[width], style=TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),bg),('ROUNDEDCORNERS',[radius]*4),
            ('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad),
            ('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),
            ('VALIGN',(0,0),(-1,-1),'TOP')]))

    def _as_flows(self, items):
        """Accept a string, a flowable, or a list thereof; return a flowable list."""
        if isinstance(items, str):
            return [Paragraph(items, _S['body'])]
        if not isinstance(items, (list, tuple)):
            return [items]
        out = []
        for it in items:
            out.append(Paragraph(it, _S['body']) if isinstance(it, str) else it)
        return out

    # ── public content methods ────────────────────────────────────────────────
    def add(self, *flows):
        for f in flows: self.story.append(f)

    def space(self, n=1): self.add(sp(n))

    def page_break(self): self.add(PageBreak())

    def text(self, t): self.add(Paragraph(t, _S['body']))

    def subhead(self, t, theme=None):
        _, d, _, _ = _theme(theme or self._theme)
        self.add(Paragraph(t, ParagraphStyle('x', parent=_S['subsec'], textColor=d)))

    def bullets(self, items, theme=None):
        a, *_ = _theme(theme or self._theme)
        dot = a.hexval()
        for it in items:
            self.add(Paragraph(f'<font color="{dot}">&#9679;</font>  {it}', _S['b1']))

    def steps(self, items, theme=None):
        a, *_ = _theme(theme or self._theme)
        for i, t in enumerate(items, 1):
            chip = Table([[Paragraph(f'<font color="white">{i}</font>',
                ParagraphStyle('x', fontName='Sans-B', fontSize=8, leading=10, alignment=TA_CENTER))]],
                colWidths=[0.46*cm], rowHeights=[0.46*cm], style=TableStyle([
                    ('BACKGROUND',(0,0),(-1,-1),a),('ROUNDEDCORNERS',[6,6,6,6]),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
            txt = Paragraph(t, ParagraphStyle('st', parent=_S['body'], alignment=TA_LEFT))
            self.add(Table([[chip, txt]], colWidths=[0.75*cm, self.W-0.75*cm], style=TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(0,0),0),('LEFTPADDING',(1,0),(1,0),4),
                ('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)])))

    def formula(self, text, small=False, theme=None):
        _, _, t, _ = _theme(theme or self._theme)
        st = _S['formula_s'] if small else _S['formula']
        self.add(Table([[Paragraph(text, st)]], colWidths=[self.W], style=TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),t),('ROUNDEDCORNERS',[9,9,9,9]),
            ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)])))

    def callout(self, label, items, theme=None):
        """Soft rounded tinted card with a coloured dot + label, then content."""
        a, d, t, _ = _theme(theme or self._theme)
        head = Paragraph(f'<font color="{a.hexval()}">&#9679;</font>  '
                         f'<font color="{d.hexval()}">{label.upper()}</font>', _S['co_lbl'])
        self.add(self._card([head, sp(0.3)] + self._as_flows(items), t, radius=9, pad=11))

    def table(self, headers, rows, widths, theme=None, highlight=None, span_rows=None):
        """Airy table: tinted header w/ coloured bold text, hairline rows, rounded.
        highlight: list of (row0,row1) data-row index ranges to tint.
        span_rows: list of data-row indices to merge across all columns (summary rows)."""
        _, d, t, h = _theme(theme or self._theme)
        data = [[Paragraph(str(x), ParagraphStyle('h', parent=_S['cell_h'], textColor=d)) for x in headers]]
        for r in rows:
            data.append([Paragraph(str(c).replace('\n', '<br/>'), _S['cell']) for c in r])
        stl = [('BACKGROUND',(0,0),(-1,0),h),('ROUNDEDCORNERS',[9,9,9,9]),
               ('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,0),(-1,0),7),
               ('TOPPADDING',(0,1),(-1,-1),6.5),('BOTTOMPADDING',(0,1),(-1,-1),6.5),
               ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
               ('VALIGN',(0,0),(-1,-1),'TOP'),
               ('LINEBELOW',(0,1),(-1,-2),0.6,LINE),
               ('ROWBACKGROUNDS',(0,1),(-1,-1),[PAPER,ZEBRA])]
        if highlight:
            for r0, r1 in highlight: stl.append(('BACKGROUND',(0,r0),(-1,r1),t))
        if span_rows:
            for r in span_rows:
                stl += [('SPAN',(0,r),(-1,r)),('ALIGN',(0,r),(-1,r),'CENTER'),
                        ('FONTNAME',(0,r),(0,r),'Sans-B'),('TEXTCOLOR',(0,r),(0,r),d)]
        self.add(Table(data, colWidths=widths, style=TableStyle(stl)))

    def kv(self, rows, w1, theme=None):
        """Two-column definition list (label | value) in a soft rounded container."""
        _, d, t, _ = _theme(theme or self._theme)
        data = [[Paragraph(f'<font color="{d.hexval()}">{k}</font>', _S['cell_b']),
                 Paragraph(v.replace('\n', '<br/>'), _S['cell'])] for k, v in rows]
        self.add(Table(data, colWidths=[w1, self.W-w1], style=TableStyle([
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[PAPER,t]),('ROUNDEDCORNERS',[9,9,9,9]),
            ('LINEBELOW',(0,0),(-1,-2),0.6,LINE),
            ('TOPPADDING',(0,0),(-1,-1),6.5),('BOTTOMPADDING',(0,0),(-1,-1),6.5),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
            ('VALIGN',(0,0),(-1,-1),'TOP')])))

    def two_col_cards(self, left_title, left_items, right_title, right_items, theme=None):
        """Two side-by-side comparison cards (e.g. concept A vs concept B)."""
        _, d, t, h = _theme(theme or self._theme)
        def col(title, items):
            return [Paragraph(f'<font color="{d.hexval()}">{title}</font>', _S['cell_h'])]
        head = [Paragraph(f'<font color="{d.hexval()}">{left_title}</font>', _S['cell_h']),
                Paragraph(f'<font color="{d.hexval()}">{right_title}</font>', _S['cell_h'])]
        body_l = Paragraph('<br/>'.join(f'&#9656; {x}' for x in left_items), _S['cell'])
        body_r = Paragraph('<br/>'.join(f'&#9656; {x}' for x in right_items), _S['cell'])
        self.add(Table([head, [body_l, body_r]], colWidths=[self.W/2, self.W/2], style=TableStyle([
            ('BACKGROUND',(0,0),(-1,0),h),('ROUNDEDCORNERS',[9,9,9,9]),
            ('BACKGROUND',(0,1),(-1,1),t),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LINEAFTER',(0,0),(0,-1),3,PAPER)])))

    # ── structural blocks ─────────────────────────────────────────────────────
    def chapter(self, no, title, kicker, subtitle, theme=None):
        """Big soft rounded module banner: huge ExtraLight number + pill + title."""
        if theme: self._theme = theme
        a, d, t, _ = _theme(self._theme)
        numP = ParagraphStyle('n', parent=_S['mod_no'], textColor=a)
        left = Table([[Paragraph(no, numP)]], colWidths=[2.4*cm], style=TableStyle([
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        right = Table([
            [self._pill('MODULE '+no, a, colors.white, size=7.5)],
            [Paragraph(title, _S['mod_ttl'])],
            [Paragraph(subtitle, _S['mod_sub'])],
        ], colWidths=[self.W-3.0*cm], style=TableStyle([
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(0,0),0),('BOTTOMPADDING',(0,0),(0,0),5),
            ('TOPPADDING',(0,1),(0,1),0),('BOTTOMPADDING',(0,1),(0,1),3),
            ('TOPPADDING',(0,2),(0,2),0),('ALIGN',(0,0),(0,0),'LEFT')]))
        inner = Table([[left, right]], colWidths=[2.6*cm, self.W-2.6*cm], style=TableStyle([
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        self.add(self._card([inner], t, radius=14, pad=16))

    def section(self, num, title, theme=None):
        a, *_ = _theme(theme or self._theme)
        chip = Table([[Paragraph(f'<font color="white">{num}</font>',
            ParagraphStyle('s', fontName='Sans-B', fontSize=8.5, leading=11, alignment=TA_CENTER))]],
            colWidths=[1.0*cm], rowHeights=[0.5*cm], style=TableStyle([
                ('BACKGROUND',(0,0),(-1,-1),a),('ROUNDEDCORNERS',[5,5,5,5]),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        head = Table([[chip, Paragraph(title, _S['sec'])]], colWidths=[1.25*cm, self.W-1.25*cm],
            style=TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('LEFTPADDING',(0,0),(0,0),0),('LEFTPADDING',(1,0),(1,0),5),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        self.add(KeepTogether([sp(0.7), head, sp(0.3)]))

    def block_title(self, t, theme=None):
        """A standalone bold title (used for numericals / practice items)."""
        _, d, _, _ = _theme(theme or self._theme)
        self.add(Paragraph(t, ParagraphStyle('bt', parent=_S['title_blk'], textColor=d)))
        self.add(sp(0.3))

    # ── convenience composites ────────────────────────────────────────────────
    def numerical(self, title, setup, headers=None, rows=None, widths=None,
                  insight=None, highlight=None, span_rows=None, table_theme='emerald'):
        """A solved worked-example: title + Setup callout + (optional) trace table + Insight."""
        self.block_title(title, theme='violet')
        self.callout('Setup', setup, theme='amber')
        self.space(0.4)
        if headers and rows:
            self.table(headers, rows, widths, theme=table_theme,
                       highlight=highlight, span_rows=span_rows)
            self.space(0.4)
        if insight:
            self.callout('Insight', insight, theme='emerald')
        self.space(0.6)

    def practice(self, title, question, answer):
        """A practice problem: title + Question callout + Model-answer callout."""
        self.block_title(title, theme='pink')
        self.callout('Question', question, theme='amber')
        self.space(0.4)
        self.callout('Model answer', answer, theme='emerald')
        self.space(0.7)

    # ── cover ──────────────────────────────────────────────────────────────────
    def cover(self, kicker, title_lines, subtitle, facts=None, roadmap=None, footnote=None):
        """title_lines: list[str] — first line rendered light, the rest bold.
        facts:   list of (TEXT, theme) -> coloured pills.
        roadmap: list of (no, theme, title, desc) -> 2-col coloured cards."""
        self.add(sp(1.5))
        self.add(self._pill(kicker, INK, colors.white, size=8))
        self.add(sp(1.2))
        for i, line in enumerate(title_lines):
            if i == 0:
                self.add(Paragraph(line, _S['hero']))
            else:
                self.add(Paragraph(f'<font name="Sans-B">{line}</font>', _S['hero']))
        self.add(sp(0.6))
        self.add(Paragraph(subtitle, _S['cv_sub']))
        self.add(sp(1.4))

        if facts:
            cells = []
            for txt, thm in facts:
                a, d, t, _ = _theme(thm)
                cells.append(self._pill('  '+txt+'  ', t, d, size=8.5))
            ft = Table([cells], colWidths=[None]*len(cells), style=TableStyle([
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-2,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
            self.add(ft); self.add(sp(1.4))

        if roadmap:
            self.add(Paragraph('<font name="Sans-B" color="#1B1F2A" size="9">WHAT&#8217;S INSIDE</font>', _S['body']))
            self.add(sp(0.4))
            CW = (self.W - 0.5*cm) / 2
            def rmc(no, thm, title, desc):
                a, d, t, _ = _theme(thm)
                pad = 10; inner_w = CW - 2*pad; txt_w = inner_w - 1.05*cm
                num = Table([[Paragraph(f'<font color="white">{no}</font>',
                    ParagraphStyle('x', fontName='Sans-B', fontSize=11, leading=13, alignment=TA_CENTER))]],
                    colWidths=[0.82*cm], rowHeights=[0.82*cm], style=TableStyle([
                        ('BACKGROUND',(0,0),(-1,-1),a),('ROUNDEDCORNERS',[7,7,7,7]),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
                txt = Table([[Paragraph(title, _S['toc_t'])],[Paragraph(desc, _S['toc_d'])]],
                    colWidths=[txt_w], style=TableStyle([
                        ('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(0,0),0),
                        ('BOTTOMPADDING',(0,0),(0,0),1.5),('TOPPADDING',(0,1),(0,1),0)]))
                inner = Table([[num, txt]], colWidths=[1.05*cm, txt_w], style=TableStyle([
                    ('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('LEFTPADDING',(0,0),(0,0),0),('LEFTPADDING',(1,0),(1,0),6),
                    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
                return self._card([inner], t, radius=10, pad=pad, width=CW)
            rows = []
            for i in range(0, len(roadmap)-1, 2):
                rows.append([rmc(*roadmap[i]), '', rmc(*roadmap[i+1])])
            if len(roadmap) % 2:  # odd one out
                rows.append([rmc(*roadmap[-1]), '', ''])
            self.add(Table(rows, colWidths=[CW, 0.5*cm, CW], style=TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),8)])))
            self.add(sp(1.0))
        if footnote:
            self.add(Paragraph(f'<i>{footnote}</i>',
                ParagraphStyle('f', parent=_S['body'], textColor=MUTE, fontSize=8.4)))

    # ── build ──────────────────────────────────────────────────────────────────
    def save(self, path, subject=''):
        self._footer_text = subject
        accent = self._footer_accent
        def furniture(canv, doc):
            canv.saveState()
            canv.setFont('Sans', 7); canv.setFillColor(FAINT)
            canv.drawString(self._mL*cm, 1.05*cm, self._footer_text)
            pn = str(canv.getPageNumber())
            canv.setFillColor(accent)
            canv.circle(self._page[0]-self._mR*cm-3, 1.12*cm, 7.5, fill=1, stroke=0)
            canv.setFillColor(colors.white); canv.setFont('Sans-B', 7.5)
            canv.drawCentredString(self._page[0]-self._mR*cm-3, 1.0*cm, pn)
            canv.restoreState()
        doc = SimpleDocTemplate(path, pagesize=self._page,
            leftMargin=self._mL*cm, rightMargin=self._mR*cm,
            topMargin=self._mT*cm, bottomMargin=self._mB*cm,
            title=subject or 'Study Notes')
        doc.build(self.story, onFirstPage=furniture, onLaterPages=furniture)
        return path
