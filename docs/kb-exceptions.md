# Knowledge-base check exceptions

Every line here suppresses a check in `tools/check_kb_hygiene.py`. Each needs a
written reason, because **a suppressed check is a claim that the defect is not a
defect**, and that claim should be as reviewable as any other in this repository.

Format — the reason after the em dash is for humans, not the parser:

```
- <check>: <id> — <reason>
```

Valid check names: `orphans`, `empty-blocks`, `pii`.

Adding a line here is a normal part of a pull request when the exception is
genuine. Adding one to make CI green when the defect is real is the failure this
file is designed to make visible: the diff shows the suppression next to the
reason, so a reviewer can disagree with it.

---

## orphans

A PMID cited in the knowledge base with no source-excerpt block. Normally this
means the paper was never archived and the claim resting on it was never
verified — see `docs/LITERATURE-PIPELINE-SOP.md` §3c. The exceptions are
identifiers that are **not sources at all**:

- orphans: 17552367 — Not a source. A transcription error retained as evidence. This PMID resolves to Blumberg MS et al., "Sleep, development, and human health" (*Sleep* 2007) — a human sleep editorial that has nothing to do with this repository. It was written into an early draft in place of Baez 2007, whose correct PMID is 17451991. The wrong identifier and the paper it actually resolves to are kept in the reference-record section of `supportive-and-palliative-care.md` so the error stays documented rather than being quietly overwritten.
- orphans: 31896807 — Not a source. The same failure: this resolves to Netto GJ, "Editorial" (*Mod Pathol* 2020), and was written in place of Evangelista 2019, whose correct PMID is 31836868 (digits transposed). Retained on the same grounds.


### Owner-guide reference-list entries (60), a tracked debt rather than an acceptance

`guides/*.zh.md` entered verification on 2026-07-21, having been written before the
citation contract existed. Bringing them in exposed something the excerpt count hides:

**Their body prose carries no inline citations at all.** Not one `PMID` appears before
`## 附录 B`. A reader meets "某项研究里…中位数 296 天" and has 144 references and 64
excerpt blocks available, and **no way to learn which one that number came from.**

So the 60 entries below are suppressed, and it is important to be clear about what that
does and does not mean. It does not mean the references are unused or the figures are
wrong. It means the documents cannot presently demonstrate which source any given figure
rests on — and **backfilling 60 excerpt blocks would not fix that.** It would produce 144
verified excerpts still unconnected to any sentence a reader actually reads.

**The fix is inline attribution in the guide bodies, and it is outstanding work.** These
suppressions exist so CI reports the real state of the corpus instead of a permanent red;
they are the marker for that debt, not its discharge. The owner guide being written for
chronic kidney disease is being built with inline attribution from the first draft, so
the debt does not grow.


- orphans: 3597844 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 8263850 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 8947869 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 9353558 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 11899035 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 15265480 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 15954547 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 16407483 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 16700173 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 17881744 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 18466247 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 19055574 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 19178669 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 21041334 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 22577051 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 24879661 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 24903757 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 25146662 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 26109275 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 26308738 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 26511103 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 27562979 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 28100766 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 29963947 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 30004120 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 30305106 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 30554552 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 30994392 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 31161850 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 31254440 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 31328872 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 31554586 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 32573314 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 32903608 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 32996835 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 33345405 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 33473067 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 33894870 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 34236002 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 34458024 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 35048412 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 35051110 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 35188319 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 35279897 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 35442117 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 35720767 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 36049238 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 37095139 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 37627457 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 38891700 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 39032511 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 39619931 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 39631747 — reference-list entry in feline-nasal-lymphoma-owner-guide.zh.md; see the note above.
- orphans: 40508984 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 40624957 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 40657883 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 40716042 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 41072475 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 41111634 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.
- orphans: 41742593 — reference-list entry in feline-lymphoma-all-types-owner-guide.zh.md; see the note above.

## empty-blocks

An excerpt block with no quoted source text. Prefer the in-file declaration —
an annotation containing the phrase `no source text available` — over an entry
here, because it keeps the reason next to the block a reader is looking at.

*(No entries. `27154944` is a Vet Rec letter with no abstract in the PubMed
record and declares itself in place.)*

## pii

Generic secret and PII findings that are intentional. Note that this repository's
**named-entity privacy screen is deliberately not part of the public checks** —
publishing that pattern list would leak precisely what it protects. Run it
locally before every commit.

*(No entries. The one e-mail address in the tree, required by the Unpaywall API,
is allow-listed in the script itself.)*
