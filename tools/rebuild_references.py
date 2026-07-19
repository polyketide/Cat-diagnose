#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild a document's reference list verbatim from PubMed metadata.

Why this exists
---------------
Hand-maintained reference lists drift. Titles get translated into the author's
working language, abbreviated, or quietly truncated. That matters more than it
looks: a reference list exists in order to be cited, so a wrong title is copied
onward verbatim -- and unlike a *missing* title, a wrong one never announces
itself.

So this script does not edit entries. It regenerates each one from the PubMed
record keyed by PMID. Title, ISO journal abbreviation, volume/issue/pages and
DOI are taken verbatim from the source record. Author commentary (anything
after an em dash) is preserved but kept in the trailing note position, where it
cannot be mistaken for part of the title.

Non-English sources keep their original-language title and gain a language tag.

Regenerating rather than patching also surfaces incidental errors that reading
would not: wrong years, wrong author initials, and -- in the run that motivated
this script -- a PMID pointing at an unrelated paper in another field.

Usage
-----
    python3 rebuild_references.py DOCUMENT.md metadata.json

`metadata.json` maps PMID -> the article object returned by the PubMed
`get_article_metadata` endpoint. Fetch it with a tool, never from memory: the
batch endpoint caps at roughly 20 records per call and does not guarantee
ordering, so records must be matched on `identifiers.pmid`, not on the order
they were requested in.
"""
import html
import json
import re
import sys

# Everything between these headings is regenerated.
SECTION_START = "## 附录 B"
SECTION_END = "## 附录 C"

LANGUAGE_TAGS = {
    'eng': None, 'chi': '中文', 'jpn': '日本語', 'ger': 'Deutsch',
    'fre': 'Français', 'spa': 'Español', 'dut': 'Nederlands',
    'ita': 'Italiano', 'pol': 'Polski', 'por': 'Português',
    'rus': 'Русский', 'kor': '한국어',
}


def format_authors(article):
    """First author, or first two, or first plus 'et al'."""
    authors = article.get('authors') or []
    if not authors:
        return '[No author listed]'
    first = authors[0]
    # PubMed embeds HTML entities in names (R&#xfc;tgen -> Rütgen).
    out = html.unescape(
        f"{first.get('last_name', '')} {first.get('initials', '')}").strip()
    if len(authors) == 2:
        second = authors[1]
        out += html.unescape(
            f", {second.get('last_name', '')} {second.get('initials', '')}"
        ).rstrip()
    elif len(authors) > 2:
        out += ", et al"
    return out


def format_citation(article):
    """Journal, year, volume(issue):pages -- verbatim from the record."""
    cite = article.get('citation') or {}
    journal = article.get('journal') or {}
    abbrev = html.unescape(
        journal.get('iso_abbreviation') or journal.get('title') or '')
    year = (article.get('publication_date') or {}).get('year', '')

    out = f"*{abbrev}*"
    if year:
        out += f" {year}"
    if cite.get('volume'):
        out += f";{cite['volume']}"
        if cite.get('issue'):
            out += f"({cite['issue']})"
    if cite.get('pages'):
        out += f":{cite['pages']}"
    return out + "."


def build_entry(pmid, article, note):
    title = html.unescape(article['title']).strip()
    if not title.endswith(('.', '?', '!')):
        title += '.'

    language = LANGUAGE_TAGS.get(article.get('language') or 'eng')
    language_tag = f" [{language}]" if language else ""

    doi = (article.get('identifiers') or {}).get('doi') or article.get('doi')

    entry = (f"- {format_authors(article)}. {title}{language_tag} "
             f"{format_citation(article)} PMID {pmid}.")
    if doi:
        entry += f" [DOI](https://doi.org/{doi})"
    if note:
        entry += f" — {note}"
    return entry


def main(path, metadata_path):
    metadata = json.load(open(metadata_path, encoding='utf-8'))
    source = open(path, encoding='utf-8').read()

    head, start_marker, remainder = source.partition(SECTION_START)
    body, end_marker, tail = remainder.partition(SECTION_END)

    lines, rebuilt, unchanged, no_metadata = [], 0, 0, []

    for line in body.splitlines():
        match = re.match(r'^- .*PMID (\d+)', line)
        if not match:
            lines.append(line)
            continue

        pmid = match.group(1)
        article = metadata.get(pmid)
        if not article:
            lines.append(line)
            no_metadata.append(pmid)
            continue

        # Keep whatever the author wrote after the em dash.
        note_match = re.search(r'\s—\s+(.*)$', line)
        note = note_match.group(1).strip() if note_match else ''

        entry = build_entry(pmid, article, note)
        if entry.strip() != line.strip():
            rebuilt += 1
        else:
            unchanged += 1
        lines.append(entry)

    rebuilt_body = "\n".join(lines)
    # Keep a blank line before the closing heading; joining without one
    # silently welds a horizontal rule onto it and eats the section.
    if end_marker and not rebuilt_body.endswith("\n\n"):
        rebuilt_body = rebuilt_body.rstrip("\n") + "\n\n"
    open(path, 'w', encoding='utf-8').write(
        head + start_marker + rebuilt_body + end_marker + tail)

    print(f"  {path}")
    print(f"    rebuilt {rebuilt}, unchanged {unchanged}")
    if no_metadata:
        print(f"    !! no metadata; left untouched: {no_metadata}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
