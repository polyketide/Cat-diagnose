# Literature Pipeline SOP — offloading retrieval to a local node

> Status: **design agreed 2026-07-20, not yet built.** Nothing here has been run. Treat every section as a specification to implement and verify, not as a description of working behaviour.
> Companion document: `.claude/agents/medical.md` §C, which states the rules binding the agent's own behaviour. This file covers engineering and operations.
>
> **Provenance of what follows.** Directly verified by reading the files: the hardware ceiling and model tiers, the existence of the sibling project's reading loop and its still-growing library index, and the presence of its node SOPs. **Reported by a survey subagent and not independently confirmed**: the internal structure of that reading loop (its stage breakdown, deduplication strategy, retry behaviour, and offline-digest mode) and the contents of the sibling project's error-handling SOPs. Those informed the patterns below and are believed accurate, but per this project's own rule that a report is a source rather than a fact, **read the originals before depending on any specific detail.**

## 1. Why

Fetching literature is the largest token cost in this project and needs almost no intelligence. Searching PubMed, pulling metadata, matching by PMID, dropping duplicates, and discarding noise fields are API and string operations. Meanwhile the work that actually requires judgement — which paper is load-bearing, which sentence may be quoted, whether a cited figure exists in the source — is a small fraction of the tokens.

Splitting these puts each on the right substrate. It also introduces heterogeneity into a project that is otherwise entirely Claude-authored: the knowledge base, the SOP, and the self-checks all come from the same model, which is a correlated set of eyes.

⚠️ **The saving is an estimate, not a measurement.** In one working session roughly 60–90k tokens went to metadata retrieval alone. That is the number to beat, and the first implementation milestone is measuring it rather than assuming it.

## 2. The division of labour

| Stage | Where | Why |
|---|---|---|
| Query construction | Local, escalate when unclear | Mechanical for known red flags; a genuinely new question is worth a Claude call |
| PubMed search, metadata fetch | **Local** | Pure API work |
| Deduplicate, index by PMID | **Local** | Dictionary lookup |
| Drop noise fields | **Local** | `query_translation` (PubMed's expanded query string) and the repeated legal notice are pure overhead |
| Crude relevance filter | **Local** | "Does this abstract contain a quantitative result? Is the species right? Is this PMID already in the knowledge base?" |
| **Select the load-bearing paper** | **Claude** | Judgement |
| **Choose the sentence to excerpt** | **Claude** | This is the project's core asset |
| **Verify figures against source** | **Claude** | The check that catches transposed PMIDs and phantom numbers |
| **Detect internal contradictions** | **Claude** | e.g. abstract vs results section |
| Write interpretation | **Claude** | — |

**The invariant**: the local side moves bytes, the Claude side makes claims. A local model may rank a paper as promising; it may never produce a sentence that ends up inside `## 原文摘录`.

## 3. Storage contract

The pipeline writes a raw archive that Claude reads directly. Requirements:

- **Raw API payload stored verbatim**, one record per PMID, unmodified. No re-encoding, no whitespace normalisation — U+00A0 and U+2009 appear in real PubMed abstracts and must survive.
- **Content hash per record**, so a later verification pass can prove the archive was not rewritten between fetch and use.
- **Any local-model output stored in a separate field**, clearly named as a hint (e.g. `local_relevance_note`), never merged into the payload. If a future reader cannot tell at a glance which bytes came from PubMed and which from a 14B model, the format is wrong.
- **Fetch provenance**: timestamp, query used, tool version.

## 4. Frozen-baseline regression (the self-check)

Adapted from the sibling project's flywheel rule for a domain with no ground-truth oracle: *lock a benchmark that never participates in training; only a run that does not degrade it counts as an improvement; if it degrades, stop, alert, and keep the old artefact.*

Here the frozen baseline is **a subset of already-verified knowledge-base entries**. The pipeline must be able to re-derive, for each entry in that set, the same PMIDs and the same verbatim excerpt text. If it cannot, the pipeline has drifted and must halt rather than continue producing.

This is what makes the loop safe to leave running: it has a way to detect its own corruption that does not depend on anyone reading its output.

## 5. Operational rules, and the incidents behind them

Carried over from the sibling project's own failure log. Each of these cost real time there.

- **`runs ≠ works`.** A process that exits 0 has not thereby done anything. Verify the artefact, not the exit code.
- **Every automated task needs a monotonically increasing output counter, and a flatline is an alarm.** Three cycles producing nothing is a failure report, not a quiet success. The concrete case here: `rebuild_references.py` completing with zero records updated looks identical to "nothing needed updating" and to "the fetch silently broke".
- **Never swallow an error, and never `2>/dev/null`.** An unrecorded error is a lie told to whoever reads the log next. Every failure is recorded, including — especially — empty model returns.
- **Distinguish the two failure classes; they get opposite handling.**
  - *Retrieval failure* (a search or fetch errors out): **do not retry blindly, and never fabricate a substitute.** Record the failure, skip that query, and let the gap be visible.
  - *Model empty-return* (the local model produces nothing): **retry with a counter, then give up loudly.** An empty return is indistinguishable from "no relevant literature", which is why it must never be allowed to pass as a result.
- **Measure the failure *rate* before tuning.** A badly quantised local model returned empty on ~75% of requests; two days went into tuning input length, which the log later described as "chasing a coin-flip". Establish whether a fault is deterministic or probabilistic *first*.
- **A detector must be proven against a known state.** Do not trust "no problems found" from a checker that has never been shown a problem it should catch.
- **Every incident must leave behind the check that would have caught it.** Recording a fix without adding the detector is not finishing. And a root cause that has not been demonstrated with a probe is a hypothesis — write it as one.

## 5a. Account for every input; label every output by grade

Two patterns worth copying exactly, both from the sibling project's reading loop.

**Nothing is dropped silently.** Every input item must end in exactly one recorded state — accepted, already-seen, or unusable-with-a-stated-reason. If a cap is hit, the overflow is reported rather than truncated away. A pipeline that quietly discards is indistinguishable from one that found nothing, and the failure only surfaces much later, as a gap nobody can explain.

**Output carries its own grade, visibly.** When the full path is unavailable — no API budget, model down, node busy — the sibling pipeline still produces something, but stamps it `[extractive digest — NOT a deep-read]`: sentences pulled mechanically by code, with nothing generated. Copy this. For catmed the grades are roughly:

| Grade | What it means | May it enter `## 原文摘录`? |
|---|---|---|
| Raw API payload | Bytes as PubMed returned them | **Yes** — this is the only thing that may |
| Extractive selection | Sentences cut from the payload by code, unmodified | Only after Claude confirms the selection |
| Local relevance hint | A local model's opinion about a paper | **Never** |

The point is not the taxonomy; it is that an artefact must never be able to travel without its grade attached. Downgrading silently is how a routing hint ends up looking like evidence.
- **Yield to real compute.** The node is shared with other long-running work. Back off rather than compete.
- **Detect node-busy via `nvidia-smi` utilisation, not `pgrep -f`** — a `pgrep` pattern can match the checking process itself and report busy forever.
- **Stage scripts with `ssh 'cat >'` and a quoted heredoc, not `rsync`.** `rsync` was observed returning `rc=0` while silently failing to deliver a file.
- **The node has an unresolved recurring BSOD (0x9F).** Any loop must be resumable from a checkpoint and must assume it can die mid-run.

## 6. Node facts

⚠️ **Host addresses, usernames, and keys do not belong in this repository — it is public.** They live in the operator's local environment and in the sibling project's private notes. Read them from there at run time; do not transcribe them here, and do not let them reach a commit, a log file, or an error message that gets committed.

What is safe to record, because it constrains design rather than granting access:

- Hardware ceiling: RTX 3080 Laptop, 16 GB → 14B Q4 is the practical maximum; 32B+ overflows. This is why the local tier cannot be asked to do work requiring judgement.
- Local model tiers available: a 14B instruct model for orchestration/tool-calling, a 14B distilled reasoning model. Neither is adequate to select or excerpt a source sentence.
- Access is over a private mesh network; the two machines use **different SSH usernames**, which has caused a real misconfiguration before. Confirm both before assuming either.
- A difficulty router already exists in the sibling project (`compute-node/runs/local-router/`), classifying tasks 1–5 and escalating only the hardest. Read it before writing anything new.

## 7. Isolation from the sibling project

catmed builds its **own** pipeline rather than extending the sibling's `reading_loop.py`. This is deliberate:

- catmed is a **public** repository with privacy redlines; the sibling's `state/` tree contains unrelated research material. Shared state would eventually leak one into the other.
- The two have different verbatim requirements. The sibling extracts structured facts; catmed extracts **quotable sentences**, where a single normalised space is a defect.
- Coupling would make catmed's citation discipline depend on a codebase that does not share it.

Borrow the patterns and the scar tissue. Do not share the code or the state directory.

## 8. Before building — open questions

1. **Is the node actually free?** The sibling project has a flywheel and an octocoral loop on it. Per §5, catmed's loop yields; it does not evict.
2. Measure the current token cost properly, so the saving can be demonstrated rather than assumed.
3. Decide where the raw archive lives — inside the repo (reviewable, but bloats a public repo with API dumps) or outside it (clean, but not version-controlled). **Not yet decided.**
