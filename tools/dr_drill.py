#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Disaster-recovery drill for the literature archive. See
docs/LITERATURE-PIPELINE-SOP.md section 4a.

Governing idea, inherited from the sibling project: `runs != works` applied to
backups themselves. Prove the archive RESTORES, not merely that it was written.

Leg 1 — archive rebuild. Rebuild from the repository's committed PMID list alone
        and assert every source excerpt in the knowledge base still appears, word
        for word, in the re-fetched record. This tests the cache-not-truth split
        (SOP section 3) and the frozen-baseline invariant (section 4) at once.

Self-test — corrupt a record in a scratch copy on purpose and assert Leg 1 fails.
        A detector never shown a fault has not been shown to work, so `--self-test`
        is not optional garnish; a PASS without it means little.

Each leg prints one machine-greppable verdict line. A leg that cannot run prints
SKIP; it never fabricates a PASS.

Usage:
  dr_drill.py leg1 [--archive DIR] [-v]
  dr_drill.py leg2 [--count N] [--batch N]
  dr_drill.py self-test [--archive DIR]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pubmed_archive import archive_dir, KB  # noqa: E402

# Excerpt lines beginning with these are the author's own annotations, not source
# text, and are excluded from verification.
ANNOTATION_MARKERS = ("⚠️", "**", "The sentences below", "The prose in the body",
                      "Only sentences carrying")


def norm(s: str) -> str:
    """Normalise for comparison, and ONLY for comparison.

    The archive keeps bytes verbatim; this is the reader that has to bridge two
    representations of the same text. PubMed's XML carries entities and NFC/NFD
    variation, and a Markdown excerpt was copied out of an already-decoded view.
    Whitespace is collapsed because line wrapping differs between the two, not
    because whitespace is unimportant — U+00A0 and U+2009 survive in the archive
    and are only folded here, at compare time.
    """
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("‒", "-")
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("‘", "'").replace("’", "'")
    s = s.replace("“", '"').replace("”", '"')
    # Case-folded: a structured abstract's section label renders as "RESULTS" in
    # the XML attribute and "Results:" in most readers. That difference is
    # presentational. Content drift — a changed figure or word — survives this.
    return re.sub(r"\s+", " ", s).strip().casefold()


FULLTEXT_MARKER = "PMC full text retrieved and checked"


def excerpts_from_kb() -> dict[str, list[tuple[str, str, str]]]:
    """PMID -> [(source file, sentence, origin)] from every `## 原文摘录` section.

    `origin` is "abstract" or "fulltext". The knowledge base marks the boundary
    with 【PMC full text retrieved and checked】: excerpts after that marker were
    taken from the PMC full text, so they are *correctly* absent from the PubMed
    abstract and must not be counted as failures. Leg 1 can only verify the
    abstract-sourced ones; conflating the two would make it report either false
    failures or false confidence.
    """
    out: dict[str, list[tuple[str, str, str]]] = {}
    for f in sorted(KB.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        if "## 原文摘录" not in text:
            continue
        current = None
        origin = "abstract"
        for line in text.split("## 原文摘录", 1)[1].splitlines():
            stripped = line.strip()
            if stripped.startswith("---"):        # section break ends a PMID block
                current, origin = None, "abstract"
                continue
            m = re.match(r"\*\*PMID\s+(\d+)\*\*", stripped)
            if m:
                current, origin = m.group(1), "abstract"
                continue
            if current and line.startswith("> "):
                body = line[2:].strip()
                if FULLTEXT_MARKER in body:
                    origin = "fulltext"
                    continue
                # Source sentences are plain prose. A line carrying Markdown
                # emphasis or a warning glyph is this project's own annotation.
                if not body or "**" in body or any(
                        body.startswith(a) for a in ANNOTATION_MARKERS):
                    continue
                out.setdefault(current, []).append((f.name, body, origin))
    return out


def abstract_of(raw_xml: str) -> str:
    """All abstract text of a record, joined. Structured abstracts carry several
    AbstractText nodes; excerpts may span or sit inside any of them."""
    art = ET.fromstring(raw_xml)
    parts = []
    for t in art.iter("AbstractText"):
        label = t.get("Label")
        body = "".join(t.itertext())
        # Readers render the label inline ("RESULTS: ..."); the XML keeps it as
        # an attribute. Excerpts copied from a rendered view carry the prefix.
        parts.append(f"{label}: {body}" if label else body)
    for t in art.iter("ArticleTitle"):
        parts.append("".join(t.itertext()))
    return " ".join(parts)


def load_archive(arc: Path) -> dict[str, str]:
    recs = {}
    for f in (arc / "records").glob("*.json"):
        rec = json.loads(f.read_text(encoding="utf-8"))
        recs[rec["pmid"]] = rec["raw_xml"]
    return recs


def leg1(arc: Path, verbose: bool = False) -> tuple[str, str, set]:
    """Returns (verdict, detail, unmatched_keys).

    The third value lets the self-test prove that an injected fault changed the
    result, rather than merely observing that the run failed for reasons that
    were already there.
    """
    if not (arc / "records").is_dir():
        return "SKIP", f"no archive at {arc} — run pubmed_archive.py fetch", set()

    excerpts = excerpts_from_kb()
    if not excerpts:
        return "SKIP", "no source excerpts found in knowledge-base/", set()

    archive = load_archive(arc)

    missing_records: list[str] = []
    unmatched: list[tuple[str, str, str]] = []
    checked = skipped_fulltext = 0

    for pmid, items in sorted(excerpts.items()):
        raw = archive.get(pmid)
        if raw is None:
            missing_records.append(pmid)
            continue
        hay = norm(abstract_of(raw))
        for src_file, sentence, origin in items:
            if origin == "fulltext":
                # Correctly absent from the abstract; out of this leg's reach.
                skipped_fulltext += 1
                continue
            checked += 1
            if norm(sentence) not in hay:
                unmatched.append((pmid, src_file, sentence))

    if verbose:
        for pmid, src, sent in unmatched:
            print(f"  UNMATCHED {pmid} ({src}): {sent[:100]}"
                  f"{'...' if len(sent) > 100 else ''}")
        for pmid in missing_records:
            print(f"  NO-RECORD {pmid}")

    detail = (f"{len(excerpts)} PMIDs, {checked} abstract-sourced excerpts checked, "
              f"{len(unmatched)} unmatched, {len(missing_records)} records missing, "
              f"{skipped_fulltext} full-text excerpts not verifiable here")
    keys = {(p, s) for p, _f, s in unmatched}
    if missing_records or unmatched:
        return "FAIL", detail, keys
    return "PASS", detail, keys


def cmd_leg1(args) -> int:
    arc = archive_dir(args.archive)
    verdict, detail, _ = leg1(arc, args.verbose)
    print(f"DR_LEG1: {verdict} ({detail})")
    return 0 if verdict == "PASS" else 1


def cmd_self_test(args) -> int:
    """Prove Leg 1 detects an injected fault. Corrupts a scratch copy only.

    ⚠️ The obvious version of this test is wrong, and the first version here was:
    asserting only that the corrupted run returns FAIL passes trivially whenever
    the baseline already fails, which is exactly when a broken detector most
    needs catching. The test must show the injected fault produced a NEW finding.
    """
    arc = archive_dir(args.archive)
    if not (arc / "records").is_dir():
        print(f"DR_SELFTEST: SKIP (no archive at {arc})")
        return 0

    base_verdict, _base_detail, base_keys = leg1(arc)
    if base_verdict == "SKIP":
        print("DR_SELFTEST: SKIP (leg1 could not run on the real archive)")
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "arc"
        shutil.copytree(arc, scratch)

        # Target a PMID whose abstract-sourced excerpts currently all MATCH, so
        # any new failure is unambiguously ours.
        excerpts = excerpts_from_kb()
        target = None
        for pmid, items in sorted(excerpts.items()):
            if not (scratch / "records" / f"{pmid}.json").exists():
                continue
            abstract_items = [s for _f, s, o in items if o == "abstract"]
            if abstract_items and not any((pmid, s) in base_keys for s in abstract_items):
                target = pmid
                break
        if target is None:
            print("DR_SELFTEST: SKIP (no clean record available to corrupt)")
            return 0

        f = scratch / "records" / f"{target}.json"
        rec = json.loads(f.read_text(encoding="utf-8"))
        # Corrupt the text of an excerpt Leg 1 actually checks. Damaging an
        # arbitrary span is not enough: an earlier version mangled the opening
        # section of a structured abstract while every checked sentence sat in
        # RESULTS, so the injected fault was invisible and the test passed for
        # the wrong reason.
        victim = next(s for _fn, s, o in excerpts[target] if o == "abstract")
        words = victim.split()
        probe = " ".join(words[:6]) if len(words) >= 6 else victim
        if probe not in rec["raw_xml"]:
            print(f"DR_SELFTEST: SKIP (cannot locate excerpt text verbatim in "
                  f"PMID {target}; nothing to corrupt deterministically)")
            return 0
        rec["raw_xml"] = rec["raw_xml"].replace(probe, "CORRUPTED_BY_SELFTEST", 1)
        f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")

        _v, detail, new_keys = leg1(scratch)
        introduced = {k for k in new_keys - base_keys if k[0] == target}
        if introduced:
            print(f"DR_SELFTEST: PASS (injected corruption in PMID {target} produced "
                  f"{len(introduced)} new unmatched excerpt(s); baseline had "
                  f"{len(base_keys)} unrelated)")
            return 0
        print(f"DR_SELFTEST: FAIL (corrupting PMID {target} produced NO new finding — "
              f"leg1 is not detecting this fault class; {detail})", file=sys.stderr)
        return 1


def _hash_tree(records: Path) -> dict[str, str]:
    """sha256 of each record FILE as it sits on disk — not the stored hash field,
    which would be self-confirming. This is what proves bytes were reused rather
    than rewritten."""
    import hashlib
    return {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(records.glob("*.json"))}


def _broken_records(records: Path) -> list[str]:
    """Records that do not parse or lack their payload — what a crash mid-write
    leaves behind, and what a resume must never silently accept as done."""
    bad = []
    for f in sorted(records.glob("*.json")):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
            if not rec.get("raw_xml") or not rec.get("sha256"):
                bad.append(f.name)
        except Exception:
            bad.append(f.name)
    return bad


def cmd_leg2(args) -> int:
    """Leg 2 — crash resume.

    Kill a fetch mid-flight, re-dispatch the identical command, and assert it
    resumes from its checkpoint rather than starting over, reusing already-written
    records byte for byte.

    ⚠️ Controlled kill -9, never a real reboot: the node this pipeline targets has
    an unresolved crash history, so rebooting to test crash-recovery risks
    triggering the very fault, and the resume path exercised is identical.

    ⚠️ The crash window is made by increasing the number of round trips (small
    --batch), not by inserting delays. The sibling project's drill initially
    tested nothing because the work finished before the killer fired; padding with
    sleeps would only have measured the sleep.
    """
    import subprocess
    import time

    tool = Path(__file__).resolve().parent / "pubmed_archive.py"
    total = args.count

    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "arc"
        records = scratch / "records"
        cmd = [sys.executable, str(tool), "fetch", "--archive", str(scratch),
               "--batch", str(args.batch), "--limit", str(total)]

        # --- run 1: kill it mid-flight -------------------------------------
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.time() + args.timeout
        killed_at = None
        while time.time() < deadline:
            n = len(list(records.glob("*.json"))) if records.is_dir() else 0
            if n >= args.batch and n < total:      # at least one batch landed, not all
                proc.kill()
                killed_at = n
                break
            if proc.poll() is not None:            # finished before we could cut in
                break
            time.sleep(0.05)
        proc.wait()

        if killed_at is None:
            n = len(list(records.glob("*.json"))) if records.is_dir() else 0
            print(f"DR_LEG2: SKIP (no crash window: fetch reached {n}/{total} before "
                  f"it could be killed — lower --batch or raise --count)")
            return 0

        before = _hash_tree(records)
        broken_before = _broken_records(records)

        # --- run 2: identical command, must resume -------------------------
        # In --self-test the second run is deliberately given --force, which makes
        # it refetch everything. That is exactly the fault this leg exists to
        # catch, so the leg must FAIL on it; a leg that passes here detects
        # nothing. Leg 1 taught this lesson the hard way.
        cmd2 = cmd + (["--force"] if args.self_test else [])
        r2 = subprocess.run(cmd2, capture_output=True, text=True)
        stdout = r2.stdout.strip()
        m = re.search(r"(\d+) PMIDs requested, (\d+) to fetch", stdout)
        after = _hash_tree(records)
        broken_after = _broken_records(records)

        failures = []
        # (a) resumed rather than restarted
        if m:
            to_fetch = int(m.group(2))
            if to_fetch >= total:
                failures.append(f"restarted from zero ({to_fetch}/{total} to fetch)")
        else:
            failures.append("could not parse resume report from run 2")
        # (b) previously written records reused byte for byte
        rewritten = [k for k, v in before.items() if after.get(k) != v]
        if rewritten:
            failures.append(f"{len(rewritten)} record(s) rewritten, not reused: "
                            f"{', '.join(rewritten[:3])}")
        # (c) completed
        if len(after) != total:
            failures.append(f"incomplete after resume: {len(after)}/{total}")
        # (d) no corruption survived — a truncated record must not pass as done
        new_broken = set(broken_after) - set(broken_before)
        if broken_after:
            failures.append(f"{len(broken_after)} unreadable record(s) after resume: "
                            f"{', '.join(broken_after[:3])}")

        detail = (f"killed after {killed_at}/{total} records, resumed "
                  f"{to_fetch if m else '?'} remaining, {len(before)} carried over "
                  f"byte-identical, {len(after)}/{total} final")
        if broken_before:
            detail += f", {len(broken_before)} truncated by the kill"
        if args.self_test:
            if failures:
                print(f"DR_LEG2_SELFTEST: PASS (a non-resuming fetch was detected: "
                      f"{'; '.join(failures)})")
                return 0
            print(f"DR_LEG2_SELFTEST: FAIL (a forced full refetch went UNDETECTED — "
                  f"this leg proves nothing) [{detail}]", file=sys.stderr)
            return 1
        if failures:
            print(f"DR_LEG2: FAIL ({'; '.join(failures)}) [{detail}]", file=sys.stderr)
            return 1
        print(f"DR_LEG2: PASS ({detail})")
        return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("leg1")
    p1.add_argument("--archive")
    p1.add_argument("-v", "--verbose", action="store_true")
    p1.set_defaults(fn=cmd_leg1)
    p2 = sub.add_parser("self-test")
    p2.add_argument("--archive")
    p2.set_defaults(fn=cmd_self_test)
    p3 = sub.add_parser("leg2")
    p3.add_argument("--count", type=int, default=24, help="records to fetch in the drill")
    p3.add_argument("--batch", type=int, default=4, help="records per request; smaller = wider crash window")
    p3.add_argument("--timeout", type=float, default=120.0)
    p3.add_argument("--self-test", action="store_true",
                    help="prove this leg detects a fetch that does NOT resume")
    p3.set_defaults(fn=cmd_leg2)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
