#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Propose inline citations for prose that has none, WITHOUT deciding anything.

The two lymphoma owner guides carry 144 references between them and not one
inline `PMID` in their body text. A reader meets a figure and has no route from
it to a source. Fixing that means attributing each figure to a paper — which is
exactly the operation that has gone wrong twelve times in this repository, every
time by attaching a number to whichever citation was nearest.

**So this tool does not attribute. It sorts figures by how much judgement they
need**, and hands the hard ones to a human:

  UNIQUE      the figure appears in exactly one archived record cited by this
              guide. Still needs a human to confirm the sentence is *about* that
              paper — co-occurrence is not attribution, which is the error
              `suspect_misattribution()` itself committed on its first run.
  AMBIGUOUS   appears in several records. Never guess; read the sentence.
  UNMATCHED   in no archived abstract. Either it comes from a full text, or it
              was computed in the prose (a percentage from a fraction), or it is
              wrong. All three have happened here.

Nothing is written to any guide. Output is a review list.

Usage:
  attribution_candidates.py GUIDE.md [--min-len 2]
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pubmed_archive import archive_dir  # noqa: E402
from dr_drill import abstract_of, norm  # noqa: E402

# Figures worth attributing. Deliberately excludes bare years (1990-2035) and
# single digits, which are mostly chapter numbers, list markers and small counts
# that carry no attribution signal.
FIGURE = re.compile(r"\d+(?:[.,]\d+)*%?")
YEARISH = re.compile(r"^(19|20)\d\d$")

# Prose only: skip the reference appendix and the excerpt section, where PMIDs
# already exist and figures are part of quoted source text.
STOP_HEADINGS = ("## 附录 B", "## 参考文献", "## 原文摘录")


def body_of(md: str) -> str:
    for h in STOP_HEADINGS:
        md = md.split(h, 1)[0]
    return md


def figures_in(text: str, min_len: int) -> list[tuple[int, str, str]]:
    """[(line number, figure, the line it sits in)] for lines outside code blocks."""
    out, in_code = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith(("|---", "> ⚠️")):
            continue
        for m in FIGURE.finditer(line):
            fig = m.group(0)
            core = fig.rstrip("%")
            if YEARISH.match(core) or len(core.replace(",", "").replace(".", "")) < min_len:
                continue
            out.append((n, fig, line.strip()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("guide")
    ap.add_argument("--min-len", type=int, default=2,
                    help="ignore figures shorter than this many digits (default 2)")
    args = ap.parse_args()

    guide = Path(args.guide)
    md = guide.read_text(encoding="utf-8")
    cited = sorted(set(re.findall(r"PMID\s+(\d+)", md)), key=int)

    records = archive_dir(None) / "records"
    hay: dict[str, list[str]] = {}
    for pmid in cited:
        f = records / f"{pmid}.json"
        if f.exists():
            raw = json.loads(f.read_text(encoding="utf-8"))["raw_xml"]
            hay[pmid] = [norm(form) for form in abstract_of(raw)]

    body = body_of(md)
    buckets: dict[str, list] = {"UNIQUE": [], "AMBIGUOUS": [], "UNMATCHED": []}
    seen: set[tuple[int, str]] = set()

    for lineno, fig, line in figures_in(body, args.min_len):
        if (lineno, fig) in seen:
            continue
        seen.add((lineno, fig))
        # Match the figure as PubMed would print it, with and without a thousands
        # separator: "1,825" in a record is "1825" in prose, and vice versa.
        needles = {norm(fig.rstrip("%")), norm(fig.rstrip("%").replace(",", ""))}
        hits = [p for p, forms in hay.items()
                if any(any(nd in form for form in forms) for nd in needles)]
        row = (lineno, fig, line[:110], hits)
        buckets["UNIQUE" if len(hits) == 1 else
                "AMBIGUOUS" if hits else "UNMATCHED"].append(row)

    total = sum(len(v) for v in buckets.values())
    print(f"\n{guide.name}: {total} figures in prose, {len(cited)} PMIDs cited, "
          f"{len(hay)} archived\n")
    for name in ("UNIQUE", "AMBIGUOUS", "UNMATCHED"):
        rows = buckets[name]
        print(f"=== {name}: {len(rows)} ===")
        for lineno, fig, line, hits in rows:
            tag = f" -> PMID {hits[0]}" if name == "UNIQUE" else \
                  f" -> {len(hits)} candidates: {','.join(hits[:6])}" if hits else ""
            print(f"  L{lineno} [{fig}]{tag}")
            print(f"      {line}")
        print()
    print("Nothing was written. UNIQUE still needs a human: a figure appearing in "
          "one abstract is not proof the sentence is about that paper.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
