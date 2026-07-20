#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the corpus to a static site so it can be read without git.

The reach problem this solves, stated plainly: until now the only way to read
anything here was to clone a repository. The knowledge base is written for
analysis and the owner guides are written for owners, and **neither was
reachable by an owner.** A cat owner with a diagnosis and a phone could not get
to a single sentence of it.

Ordering is deliberate and is the opposite of the repository's own layout:
owner guides first, analysis notes second. The repository is organised around
how the material is produced; a site has to be organised around who is reading.

Every page carries the disclaimer, not just the index. People arrive from search
engines in the middle of a document, and a warning that only exists on a page
they never loaded is not a warning.

Every page also links to its Markdown source, because the whole claim of this
project is that figures are checkable, and a rendered page with no route back to
the source excerpts quietly drops that.

Usage:
  build_site.py [--out DIR]        # default: site/
Standard library only.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_markdown import convert, CSS      # noqa: E402
from pubmed_archive import corpus_files, REPO  # noqa: E402

GITHUB = "https://github.com/polyketide/catmed/blob/main"

DISCLAIMER = """<div class="disclaimer">
<strong>⚠️ 这不是医疗建议 · Not medical advice · 医療アドバイスではありません</strong>
<p>本站内容是供你与<strong>执业兽医</strong>共同审阅的循证参考资料。它不下诊断、不开处方，
也不能替代能亲手检查这只动物的兽医。每一个数字都标注了 PMID，可自行核对。</p>
<p>如果你的猫现在情况危急——完全不吃、呼吸困难、倒下、无法排尿、突然失明——
<strong>请立刻联系兽医，不要先读文章。</strong></p>
</div>"""

EXTRA_CSS = """
/* render_markdown.py's stylesheet is a PRINT stylesheet: it sets `color` and,
   correctly for paper, no `background`. On screen that is a real defect — a
   browser in dark mode paints a dark background under text that is still
   #1a1a1a, and the page reads as blank. Caught on the mobile preview, which is
   how an owner would most likely arrive.
   These documents are designed light, so declare that rather than half-adopt a
   dark theme the hardcoded panel colours would not survive. */
:root{color-scheme:light}
html,body{background:#fff;color:#1a1a1a}
.disclaimer{border:2px solid #c0392b;background:#fdf3f2;border-radius:8px;
  padding:1em 1.2em;margin:1.5em 0;font-size:.94em}
.disclaimer strong{color:#c0392b}
.disclaimer p{margin:.6em 0 0}
.sitenav{margin:0 0 1.5em;padding:.6em 0;border-bottom:1px solid #ddd;font-size:.9em}
.sitenav a{margin-right:1.2em}
.srcline{margin:2.5em 0 1em;padding-top:1em;border-top:1px solid #ddd;
  font-size:.85em;color:#666}
.cardlist{list-style:none;padding:0}
.cardlist li{border:1px solid #ddd;border-radius:8px;padding:1em 1.2em;margin:.8em 0}
.cardlist .t{font-weight:700;font-size:1.05em}
.cardlist .d{color:#555;font-size:.92em;margin-top:.3em}
.badge{display:inline-block;background:#eef4fb;border:1px solid #cfe0f2;color:#2c5d8f;
  border-radius:99px;padding:.1em .7em;font-size:.8em;margin-left:.5em;vertical-align:middle}
/* Wide content must scroll inside itself; the page must never scroll sideways.
   These documents contain an ASCII survival-range diagram in a <pre>, six-column
   tables, and reference lists full of long DOI URLs — each of which overflows a
   375px phone, which is the likeliest way an owner arrives. */
@media (max-width:640px){
  body{padding:1em .8em}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;font-size:.85em}
  pre{overflow-x:auto}
}
a{word-break:break-word}
pre{max-width:100%}
img{max-width:100%;height:auto}
"""

# Owner-facing documents, in the order an owner should meet them. Anything in
# guides/ not listed here still gets rendered — it just falls to the end.
GUIDE_ORDER = [
    ("feline-ckd-owner-guide.zh.md", "猫慢性肾病（CKD）",
     "老猫最常见的慢性病之一。每个数字都带行内 PMID，可逐条核对。", "行内出处完整"),
    ("feline-lymphoma-all-types-owner-guide.zh.md", "猫淋巴瘤（全类型）",
     "各解剖型淋巴瘤的预后、治疗与照护。", ""),
    ("feline-nasal-lymphoma-owner-guide.zh.md", "猫鼻腔淋巴瘤",
     "鼻腔型的专门指南。", ""),
]

KB_BLURB = {
    "emergency-triage-red-flags.md": "什么时候必须立刻就医，以及为什么「过度就医」的代价也被计入",
    "feline-hypertension.md": "老猫三件套里唯一无声的那个",
    "hyperthyroidism-and-kidney-disease.md": "两个科室各握一半的病",
    "feline-oncology-literature-survey.md": "猫肿瘤文献总览",
    "supportive-and-palliative-care.md": "支持与安宁照护",
    "antineoplastic-drug-toxicity.md": "化疗药物毒性",
    "targeted-and-immunotherapy-evidence.md": "靶向与免疫治疗的证据边界",
    "upper-airway-response-marker-validity.md": "上呼吸道肿瘤：哪些「好转」的迹象不能当作疗效",
    "evidence-to-practice-gap.md": "兽医学自己诊断出的证据缺口",
}


def page(title: str, body: str, nav: bool = True) -> str:
    navbar = ('<div class="sitenav"><a href="index.html">← 首页</a>'
              '<a href="https://github.com/polyketide/catmed">GitHub</a></div>') if nav else ""
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n'
            '<meta charset="utf-8"/>\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1"/>\n'
            f'<title>{html.escape(title)}</title>\n'
            f'<style>{CSS}{EXTRA_CSS}</style>\n</head>\n<body>\n'
            f'{navbar}{DISCLAIMER}\n{body}\n</body>\n</html>\n')


def first_heading(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else fallback


def build(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    guides, notes = [], []

    for src in corpus_files():
        md = src.read_text(encoding="utf-8")
        title = first_heading(md, src.stem)
        rel = f"{src.parent.name}/{src.name}"
        body = convert(md)
        body += (f'<div class="srcline">来源文件：'
                 f'<a href="{GITHUB}/{rel}">{rel}</a> · '
                 f'本文所有摘录由 <code>tools/dr_drill.py leg1</code> 在每次提交时'
                 f'逐字比对归档的 PubMed 记录。</div>')
        dst = out / f"{src.stem}.html"
        dst.write_text(page(title, body), encoding="utf-8")
        (guides if src.parent.name == "guides" else notes).append(
            (src.name, title, f"{src.stem}.html"))

    # ---- index, ordered for readers rather than for the repository
    ordered, seen = [], set()
    for name, label, blurb, badge in GUIDE_ORDER:
        for n, t, href in guides:
            if n == name:
                ordered.append((label, blurb, href, badge)); seen.add(n)
    for n, t, href in guides:
        if n not in seen:
            ordered.append((t, "", href, ""))

    gl = "\n".join(
        f'<li><div class="t"><a href="{h}">{html.escape(lab)}</a>'
        + (f'<span class="badge">{html.escape(b)}</span>' if b else "")
        + f'</div><div class="d">{html.escape(d)}</div></li>'
        for lab, d, h, b in ordered)
    nl = "\n".join(
        f'<li><div class="t"><a href="{h}">{html.escape(t)}</a></div>'
        f'<div class="d">{html.escape(KB_BLURB.get(n, ""))}</div></li>'
        for n, t, h in sorted(notes, key=lambda x: KB_BLURB.get(x[0], "zz")))

    body = f"""<h1>catmed · 猫的循证医疗资料</h1>
<p>这里的每一个数字都能追到一篇发表文献的原句。正文是解释，<strong>可以争论</strong>；
每份文件末尾的「原文摘录」是证据，<strong>逐字未经改写</strong>，并由脚本在每次提交时
比对归档的 PubMed 记录。</p>

<h2>给猫主人</h2>
<p>不需要医学背景。建议先读每份文件的「第 0 章」和「立刻就医的红线」。</p>
<ul class="cardlist">
{gl}
</ul>

<h2>给兽医与研究者</h2>
<p>分析用笔记，英文，含逐字原文摘录与文献计量。这些不是写给主人读的——
它们记录的是<strong>哪些结论站得住、哪些证据其实不存在</strong>。</p>
<ul class="cardlist">
{nl}
</ul>

<h2>这个项目在做什么</h2>
<p>catmed 是一个<strong>证据整合</strong>项目，不是诊断工具。它的价值不在于比兽医懂得多，
而在于：把散落在不同论文里的证据放在一起、发现它们互相矛盾的地方、
并且<strong>明确说出哪里根本没有证据</strong>。</p>
<p>凡文中写「没有证据」「未找到」的地方，就是文献里真的空白。
任何人给你一个填补该空白的数字，那都是编的。</p>
<p><a href="https://github.com/polyketide/catmed">源码与完整校验流程在 GitHub</a>
（MIT 授权，欢迎兽医指正与贡献）。</p>
"""
    (out / "index.html").write_text(page("catmed · 猫的循证医疗资料", body, nav=False),
                                    encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(guides) + len(notes) + 1} pages → {out}")
    print(f"  owner guides: {len(guides)}   analysis notes: {len(notes)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(REPO / "site"))
    return build(Path(ap.parse_args().out))


if __name__ == "__main__":
    sys.exit(main())
