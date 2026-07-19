#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Attach verbatim source sentences to every claim that cites a paper.

Why this exists
---------------
A knowledge base written in one language about literature written in another
has a silent failure mode. The figures survive translation, but *what the
authors actually said* exists only as the author's rendering of it. That
rendering cannot be quoted, cannot be checked, and any drift between it and the
source is invisible -- there is nothing to compare against.

This script closes that gap. For every cited PMID it pulls the sentences from
the source abstract that carry the figures the document attributes to that
paper, and records them untranslated. The prose stays as interpretation; the
excerpt is the evidence.

It also does something the prose cannot: it reports figures the document cites
that do *not* appear in the source. Those are not automatically errors -- a
figure may come from the full text, which the abstract omits -- but they are
exactly the claims that should not be treated as verified. Leaving them
unmarked lets an unverified number pass as a checked one.

In the run that motivated this script, cross-checking this way found a
percentage attributed to the wrong clinical sign (the cough figure had been
recorded as the dysphonia figure) and a set of figures attributed to a paper
that did not contain them.

Known limitation: sources that spell figures out in words ("Ninety-three
percent") are missed by digit matching and will be reported as unlocatable.

Only load-bearing sentences are quoted, never whole abstracts.

Usage
-----
    python3 extract_source_excerpts.py DOCUMENT.md metadata.json [fulltext.json]

`metadata.json` maps PMID -> PubMed article record.
`fulltext.json` (optional) maps PMID -> {"pmc", "sentences", "note"} for papers
whose full text was retrieved from PMC, so claims resting on the full text can
be verified too rather than only flagged.
"""
import html
import json
import re
import sys

SECTION_HEADING = "## 原文摘录（source excerpts）"

# Cap per paper. The goal is verifiability, not reproducing the abstract.
MAX_SENTENCES = 3


def split_sentences(text):
    text = html.unescape(text).replace('\n', ' ')
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z(])', text)
    return [p.strip() for p in parts if p.strip()]


def extract_figures(text):
    """Numeric tokens usable for locating a claim in its source.

    Single digits are ignored: too noisy to match on.
    """
    found = set()
    for match in re.finditer(r'\d+(?:\.\d+)?', text):
        token = match.group(0)
        if len(token) >= 2 or '.' in token:
            found.add(token)
    return found


def collect_citations(path):
    """Map each cited PMID to the figures the document attributes to it."""
    cited = {}
    for line in open(path, encoding='utf-8'):
        if SECTION_HEADING in line:
            break  # stop before a previously generated section
        pmids = re.findall(r'PMID ?(\d+)', line)
        if not pmids:
            continue
        figures = extract_figures(re.sub(r'PMID ?\d+', '', line))
        for pmid in pmids:
            cited.setdefault(pmid, set()).update(figures)
    return cited


def select_sentences(abstract, wanted):
    """Sentences carrying the most of the wanted figures, shortest first."""
    scored = []
    for sentence in split_sentences(abstract):
        overlap = len(extract_figures(sentence) & wanted)
        if overlap:
            scored.append((overlap, len(sentence), sentence))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [sentence for _, _, sentence in scored[:MAX_SENTENCES]]


def main(path, metadata_path, fulltext_path=None):
    metadata = json.load(open(metadata_path, encoding='utf-8'))
    fulltext = json.load(open(fulltext_path, encoding='utf-8')) \
        if fulltext_path else {}

    source = open(path, encoding='utf-8').read().split(SECTION_HEADING)[0]
    source = source.rstrip()

    cited = collect_citations(path)
    if not cited:
        print(f"  skipped (no citations): {path}")
        return

    out = [
        "", "", "---", "", SECTION_HEADING, "",
        "> 下列为**文献原文句子，逐字摘录**，未经翻译。",
        "> 正文中的中文是我的解读；**若要引用，请引用此处原文**，并回到原文核对上下文。",
        "> 仅摘录承载具体结论的句子，非全文摘要；完整语境请按 PMID/DOI 取原文。", "",
    ]

    papers = sentences_written = 0
    unavailable = []

    for pmid in sorted(cited, key=int):
        article = metadata.get(pmid)
        if not article:
            unavailable.append(pmid)
            continue

        abstract = article.get('abstract') or ''
        if not abstract or abstract == '[Abstract not available]':
            unavailable.append(pmid)
            continue

        selected = select_sentences(abstract, cited[pmid])

        # Figures the document cites that are absent from the source text.
        # Exclude the paper's own bibliographic numbers (year, volume, DOI).
        bibliographic = extract_figures(
            str(article.get('citation', ''))
            + str(article.get('publication_date', ''))
            + str((article.get('identifiers') or {}).get('doi', '')))
        unlocatable = sorted(
            (cited[pmid]
             - extract_figures(abstract + ' ' + article.get('title', '')))
            - bibliographic,
            key=lambda token: (len(token), token))

        verified = fulltext.get(pmid)
        if not selected and not unlocatable and not verified:
            continue

        first_author = (article.get('authors') or [{}])[0]
        label = html.unescape(
            f"{first_author.get('last_name', '')} "
            f"{first_author.get('initials', '')}").strip()
        year = (article.get('publication_date') or {}).get('year', '')

        out.append(f"**PMID {pmid}** · {label} {year}")
        for sentence in selected:
            out.append(f"> {sentence}")
            sentences_written += 1

        if verified:
            out.append("> **【已取 PMC 全文核对】**")
            for sentence in verified["sentences"]:
                out.append(f"> {sentence}")
                sentences_written += 1
            if verified.get("note"):
                out.append(f"> ⚠️ {verified['note']}")
        elif unlocatable:
            out.append(
                f"> ⚠️ 正文引用的 `{', '.join(unlocatable[:8])}` "
                f"**未出现在摘要原文中** —— 可能出自全文（摘要不含），也可能有误；"
                f"**引用前请取全文核对**。"
                f"（注：原文若把数字拼写为英文单词，本检查会漏报。）")

        out.append("")
        papers += 1

    if unavailable:
        out += ["**以下文献无摘要或未取得原文，正文中文表述暂无原文可核：**", "",
                "- " + ", ".join(f"PMID {p}"
                                 for p in sorted(unavailable, key=int)), ""]

    open(path, 'w', encoding='utf-8').write(source + "\n".join(out) + "\n")
    print(f"  {path}: {papers} papers / {sentences_written} sentences"
          + (f", {len(unavailable)} without source text" if unavailable else ""))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2],
         sys.argv[3] if len(sys.argv) > 3 else None)
