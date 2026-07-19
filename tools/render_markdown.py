#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a Markdown document to print-ready, self-contained HTML.

Standard-library only, so it runs anywhere Python does. Written because the
usual toolchain (pandoc, weasyprint, LaTeX) was unavailable and installing one
was not worth it for a handful of documents.

Handles the subset these documents use: headings with GitHub-compatible
anchors, pipe tables, blockquotes, nested lists, inline emphasis and links.

The stylesheet targets A4 print. CJK-capable system fonts are requested by
name so headless Chrome embeds real glyphs rather than boxes; tables and
blockquotes are kept off page breaks.

Pair with headless Chrome to get a PDF:

    python3 render_markdown.py DOC.md out.html "Title"
    chrome --headless=new --disable-gpu --no-pdf-header-footer \
           --print-to-pdf=out.pdf file://$PWD/out.html
"""
import html
import re
import sys
import unicodedata


# ---------- inline elements ----------

def slugify(text):
    """GitHub-style anchor: lowercase, strip punctuation, spaces to hyphens.

    CJK characters are kept, matching GitHub's own behaviour."""
    t = text.strip().lower()
    t = re.sub(r'[!-/:-@\[-`{-~·—–、。，：；？！（）「」【】《》]', '', t)
    # Strip emoji and symbols, as GitHub does, keeping surrounding spaces.
    t = ''.join(c for c in t if unicodedata.category(c) not in ('So', 'Sk', 'Cf'))
    t = t.replace('\t', ' ').replace(' ', '-')  # one hyphen per space; do not collapse
    return t


def inline(text):
    """Inline markup. Code spans are stashed first so their contents are not reparsed."""
    stash = []

    def keep(m):
        stash.append('<code>%s</code>' % html.escape(m.group(1)))
        return '\x00%d\x00' % (len(stash) - 1)

    text = re.sub(r'`([^`]+)`', keep, text)
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', text)
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    return re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], text)


# ---------- block elements ----------

def is_table_sep(line):
    return bool(re.match(r'^\s*\|?[\s:|-]+\|[\s:|-]*$', line)) and '-' in line


def split_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]


def convert(md):
    lines = md.split('\n')
    out = []
    i = 0
    n = len(lines)
    list_stack = []  # entries are 'ul' or 'ol'
    in_quote = False

    def close_lists(to_depth=0):
        while len(list_stack) > to_depth:
            out.append('</%s>' % list_stack.pop())

    def close_quote():
        nonlocal in_quote
        if in_quote:
            out.append('</blockquote>')
            in_quote = False

    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        # blank line
        if not stripped:
            close_lists()
            i += 1
            continue

        # blockquote
        if stripped.startswith('>'):
            close_lists()
            if not in_quote:
                out.append('<blockquote>')
                in_quote = True
            body = re.sub(r'^\s*>\s?', '', line)
            out.append('<p>%s</p>' % inline(body) if body.strip() else '')
            i += 1
            continue
        close_quote()

        # horizontal rule
        if re.match(r'^\s*(---+|\*\*\*+)\s*$', line):
            close_lists()
            out.append('<hr/>')
            i += 1
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            close_lists()
            level = len(m.group(1))
            txt = m.group(2).strip()
            out.append('<h%d id="%s">%s</h%d>' % (level, slugify(txt), inline(txt), level))
            i += 1
            continue

        # table
        if '|' in stripped and i + 1 < n and is_table_sep(lines[i + 1]):
            close_lists()
            header = split_row(stripped)
            aligns = []
            for spec in split_row(lines[i + 1]):
                left, right = spec.startswith(':'), spec.endswith(':')
                aligns.append('center' if left and right else
                              'right' if right else 'left')
            out.append('<table><thead><tr>')
            for idx, cell in enumerate(header):
                a = aligns[idx] if idx < len(aligns) else 'left'
                out.append('<th style="text-align:%s">%s</th>' % (a, inline(cell)))
            out.append('</tr></thead><tbody>')
            i += 2
            while i < n and '|' in lines[i] and lines[i].strip():
                out.append('<tr>')
                for idx, cell in enumerate(split_row(lines[i])):
                    a = aligns[idx] if idx < len(aligns) else 'left'
                    out.append('<td style="text-align:%s">%s</td>' % (a, inline(cell)))
                out.append('</tr>')
                i += 1
            out.append('</tbody></table>')
            continue

        # list
        m = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', line)
        if m:
            indent, marker, body = m.group(1), m.group(2), m.group(3)
            depth = len(indent.replace('\t', '    ')) // 2 + 1
            kind = 'ol' if re.match(r'\d', marker) else 'ul'
            while len(list_stack) > depth:
                out.append('</%s>' % list_stack.pop())
            if len(list_stack) < depth:
                while len(list_stack) < depth:
                    out.append('<%s>' % kind)
                    list_stack.append(kind)
            elif list_stack and list_stack[-1] != kind:
                out.append('</%s>' % list_stack.pop())
                out.append('<%s>' % kind)
                list_stack.append(kind)
            out.append('<li>%s</li>' % inline(body))
            i += 1
            continue

        # paragraph
        close_lists()
        buf = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r'^\s*(#{1,6}\s|>|[-*+]\s|\d+[.)]\s|---+\s*$)', lines[i]) \
                and '|' not in lines[i]:
            buf.append(lines[i].strip())
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))

    close_lists()
    close_quote()
    return '\n'.join(x for x in out if x)


CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
@page { @bottom-center { content: counter(page); } }

* { box-sizing: border-box; }

html { font-size: 10.2pt; }

body {
  font-family: "Hiragino Sans GB", "PingFang SC", "STHeiti", "Songti SC",
               "Helvetica Neue", Arial, sans-serif;
  line-height: 1.72;
  color: #1a1a1a;
  margin: 0;
  -webkit-font-feature-settings: "kern" 1;
  text-rendering: optimizeLegibility;
}

/* ---- headings ---- */
h1 {
  font-size: 21pt; font-weight: 700; line-height: 1.35;
  margin: 0 0 4mm; padding-bottom: 3mm;
  border-bottom: 2.5px solid #1a1a1a;
  letter-spacing: .01em;
}
h2 {
  font-size: 15pt; font-weight: 700; line-height: 1.4;
  margin: 9mm 0 3.5mm; padding: 2mm 0 2mm 4mm;
  border-left: 4px solid #2b6cb0;
  background: #f4f7fb;
  page-break-after: avoid; break-after: avoid;
}
h3 {
  font-size: 12.2pt; font-weight: 700;
  margin: 6.5mm 0 2.5mm;
  color: #1a365d;
  page-break-after: avoid; break-after: avoid;
}
h4 {
  font-size: 10.8pt; font-weight: 700;
  margin: 5mm 0 2mm; color: #2d3748;
  page-break-after: avoid; break-after: avoid;
}

/* chapter headings */
h2 { page-break-before: auto; }

p { margin: 0 0 2.6mm; orphans: 2; widows: 2; }

strong { font-weight: 700; color: #000; }
em { font-style: normal; background: linear-gradient(transparent 62%, #ffe9a8 62%); }

a { color: #1a4f8a; text-decoration: none; border-bottom: .5px solid #9db8d4; }

code {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: .88em; background: #f0f2f5;
  padding: .5mm 1.2mm; border-radius: 2px;
}

hr {
  border: 0; border-top: 1px solid #d8dee6;
  margin: 6mm 0;
}

/* ---- lists ---- */
ul, ol { margin: 0 0 3mm; padding-left: 6.5mm; }
li { margin: 0 0 1.4mm; }
li > ul, li > ol { margin-top: 1.4mm; }

/* ---- tables ---- */
table {
  width: 100%; border-collapse: collapse;
  margin: 3mm 0 4.5mm; font-size: 9.1pt;
  page-break-inside: avoid; break-inside: avoid;
}
thead { display: table-header-group; }
th {
  background: #eef2f7; font-weight: 700;
  border: .5px solid #c3ccd8;
  padding: 1.8mm 2.2mm; line-height: 1.5;
}
td {
  border: .5px solid #d5dce5;
  padding: 1.8mm 2.2mm; line-height: 1.58;
  vertical-align: top;
}
tbody tr:nth-child(even) { background: #fafbfc; }

/* ---- blockquotes ---- */
blockquote {
  margin: 3mm 0; padding: 2.5mm 4mm;
  background: #f7f9fb;
  border-left: 3px solid #8fa8c4;
  page-break-inside: avoid; break-inside: avoid;
}
blockquote p { margin: 0 0 1.5mm; font-size: 9.4pt; color: #33404f; }
blockquote p:last-child { margin-bottom: 0; }

/* ---- keep headings with their content ---- */
h2, h3, h4 { page-break-inside: avoid; break-inside: avoid; }
"""


def main():
    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(src, encoding='utf-8') as f:
        md = f.read()
    body = convert(md)
    page = (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n'
        % (html.escape(title), CSS, body)
    )
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote %s (%d chars)' % (dst, len(page)))


if __name__ == '__main__':
    main()
