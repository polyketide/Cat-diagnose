# The Evidence-to-Practice Gap in Feline Medicine — what is actually missing

> Generated 2026-07-20 · PubMed search + verbatim verification · Not clinical guidance
> **Purpose**: this project asserts that its value is *integrating evidence*, not producing it. That assertion was, until now, argued rather than evidenced. This file is the evidence — and it also marks where the argument does not hold.
> **Read the last section first if you are deciding what to build.** It separates what an integration tool can address from what it demonstrably cannot.

---

## 1. The finding that reframes the problem

Guidelines exist. They are followed less than a quarter of the time.

In 776 Swiss feline cases across two university hospitals and 14 private practices, antimicrobial prescriptions were **"judged in complete accordance with consensus guidelines in 22% (aURTD), 24% (FLUTD) and 17% (abscesses) of the cases"**. Antibiotics were given **"although not indicated in 34% (aURTD), 14% (FLUTD) and 29% (abscesses)"** (Schmitt 2019, PMID 30871537).

> **∴ The bottleneck is not the absence of knowledge. It is knowledge failing to arrive at the moment of decision.** That distinction decides what a tool like this one can usefully be: it cannot manufacture evidence, but the gap it *can* address turns out to be the larger one.

**A second number in the same study says where the gap widens.** Diagnostic work-up before prescribing differed enormously by setting — for upper respiratory disease, **58% at university hospitals versus 1% in private practice**; for lower urinary tract disease, **92% versus 27%**. ⚠️ This is a comparison of settings, not a judgement of clinicians: caseload, equipment, owner budget and time per consultation differ, and none of those were measured here. What it does establish is that the *same* condition is worked up very differently depending on where the cat is seen.

---

## 2. Why evidence does not arrive (the profession's own diagnosis)

The Evidence-Based Veterinary Medicine Association's 20th-anniversary review is unusually blunt about its own field. It attributes the persistent failure to **"a lack of understanding of its importance to the practice of medicine, veterinary literature that often fails to adhere to evidence-based standards, inadequate attention to teaching EBVM at the university level, and the inherent reluctance of clinicians to alter historical practice styles"** (Block 2024, PMID 39523636).

The mechanism it identifies is the one that matters here:

> **"For many practitioners, EBVM continues to be an abstract concept they believe requires advanced training in statistics and epidemiology resulting in them relying on less robust sources for clinical guidance."**

And it names the consequence without hedging: **"This unfortunately results in suboptimal care for our patients and delayed medical advancements for our profession."**

**⭐ The paper's own prescription includes the thing this project is.** Among its stated aims is **"the provision of easily accessible tools that permit clinicians to incorporate EBVM into their daily practice."** That is an independent statement of need, published by the field's own association, not a rationale constructed after the fact by this repository.

⚠️ **Scope limit, stated because it is easy to overclaim here.** Block 2024 is a review and position paper, not a study. Its full text reports figures on trial bias, industry sponsorship and curriculum coverage that are **not in the abstract and were not verified verbatim** for this file — they are therefore not cited here. If those figures are wanted, retrieve the full text and check them before use.

---

## 3. The owner side: already searching, before the consultation

Of 2117 dog and cat owners surveyed across Austria, Denmark and the UK, roughly one in three **"never used internet resources prior to (31.7%) or after (37.0%) a consultation"** — meaning about two in three do. Use is **"more likely to use it before than after the consultation."** The commonest sources were practice websites (35.0%), veterinary association websites (24.0%), and **"'other' websites providing veterinary information (55.2%)"** (Springer 2024, PMID 38966565).

The paper states the risk plainly: owners may **"misinterpret online information or gain a false impression of current standards in veterinary medicine"**, which **"can cause problems or tensions, for example if the owner delays consulting their veterinarian about necessary treatment, or questions the veterinarian's medical advice."**

> **Two things follow, and they point in opposite directions.**
>
> **The demand is real and mostly pre-consultation.** Owners are not deciding whether to seek information; they already have. The realistic question is what they find.
>
> **But this is also the clearest statement of how such a tool does harm** — delay, and undermining the clinician. It is the same failure mode the triage design is built against (`emergency-triage-red-flags.md` §3), now with a survey behind it. The paper's own recommendation is not to displace the conversation but to open it: veterinarians **"should actively ask pet owners if they use internet resources, and what resources they use."** A tool that produces something an owner can *bring to* that conversation is aligned with this; one that substitutes for it is not.

---

## 4. What this does and does not license

**Supported by the evidence above:**

- Practitioners rely on less robust sources because rigorous appraisal feels to require specialist statistical training (Block 2024). **Doing the appraisal and showing the working addresses a stated need.**
- Guideline-concordant care is the minority even where guidelines exist (Schmitt 2019). **Surfacing what a guideline says at the point of decision is a real gap, not an invented one.**
- Owners are already searching, mostly before the consultation (Springer 2024). **The audience exists and is reachable at the moment it matters.**

**NOT supported, and not to be claimed:**

- ❌ **That this improves outcomes.** No study here measures a patient outcome from any information tool. That evidence does not exist in either direction (see `emergency-triage-red-flags.md` §3 for the human-medicine attempt).
- ❌ **That it addresses the quality of the underlying literature.** Poor trial design, publication bias and industry sponsorship are upstream and untouchable from here. An integrator inherits whatever the evidence base contains — including its biases — and can at best label them.
- ❌ **That it substitutes for guidelines.** Veterinary medicine's lack of formal clinical practice guidelines is a structural problem requiring institutional effort. Nothing here produces a guideline.
- ❌ **That the 22% concordance figure means clinicians are wrong.** It is a records-based comparison against consensus documents, in one country, in 2016. Clinicians hold information no chart review contains.

> **The honest summary**: the gap this project targets is real, documented by the profession itself, and larger than the evidence-generation gap. Whether *this* tool closes any part of it is untested — and by the standard applied everywhere else in this repository, an untested claim is not a finding.

---

## 5. Gaps worth closing next

- Whether any information tool changes veterinary care-seeking behaviour or outcomes. Searched in the triage context and found empty for veterinary settings; still empty.
- Guideline concordance outside Switzerland and outside antimicrobials — one country and one drug class is a thin base for a claim this load-bearing.
- What owners actually retrieve from those "other websites" (55.2%), which is the largest single category and the least characterised.

---

---

## 参考文献（原文记录）

> 本节标题、期刊、卷期页**一律为 PubMed 原文**，不翻译、不缩写。
> 正文中的表述仅为解读；**如需引用，请引用下方原文条目**。

- Schmitt K, et al. Antimicrobial use for selected diseases in cats in Switzerland. *BMC Vet Res* 2019;15(1):94. PMID 30871537. [DOI](https://doi.org/10.1186/s12917-019-1821-0)
- Block G. Evidence-based veterinary medicine-potential, practice, and pitfalls. *J Vet Intern Med* 2024;38(6):3261-3271. PMID 39523636. [DOI](https://doi.org/10.1111/jvim.17239)
- Springer S, et al. Does "Dr. Google" improve discussion and decisions in small animal practice? Dog and cat owners use of internet resources to find medical information about their pets in three European countries. *Front Vet Sci* 2024;11:1417927. PMID 38966565. [DOI](https://doi.org/10.3389/fvets.2024.1417927)

---

---

## 原文摘录（source excerpts）

> The sentences below are **verbatim excerpts from the source literature**, untranslated.
> The prose in the body above is my interpretation; **if you need to cite, cite the original sentences here**.

**PMID 30871537** · Schmitt K 2019
> Prescriptions were judged in complete accordance with consensus guidelines in 22% (aURTD), 24% (FLUTD) and 17% (abscesses) of the cases.
> Antibiotics were prescribed although not indicated in 34% (aURTD), 14% (FLUTD) and 29% (abscesses) of the cases.
> A total of 776 cases (aURTD, n = 227; FLUTD, n = 333; abscesses, n = 216) presented to two university hospitals and 14 private veterinary practices in Switzerland during 2016 were retrospectively evaluated.
> A total of 77% (aURTD), 60% (FLUTD) and 96% (abscesses) of the cases received antibiotic therapy; 13-24% received combination or serial therapy.
> Although diagnostic work-up was significantly more common (aURTD: university hospitals, 58%; private practices, 1%; FLUTD: university hospitals, 92%; private practices, 27%)

**PMID 39523636** · Block G 2024
> Reasons for this include a lack of understanding of its importance to the practice of medicine, veterinary literature that often fails to adhere to evidence-based standards, inadequate attention to teaching EBVM at the university level, and the inherent reluctance of clinicians to alter historical practice styles.
> For many practitioners, EBVM continues to be an abstract concept they believe requires advanced training in statistics and epidemiology resulting in them relying on less robust sources for clinical guidance.
> This unfortunately results in suboptimal care for our patients and delayed medical advancements for our profession.
> As part of the 20th anniversary of the founding of the Evidence-Based Veterinary Medicine Association (EBVMA), we are refocusing our efforts to highlight the need for dedicated teaching of EBVM at the university level, for rigorous adherence to established research reporting guidelines, for expansion of EBVM infrastructure, and for the provision of easily accessible tools that permit clinicians to incorporate EBVM into their daily practice.
> Ultimately, EBVM is not an end unto itself, but rather a means to improve the quality of care we provide our patients.
> ⚠️ Review and position paper, not a study. Its full text contains further figures (trial risk of bias, industry sponsorship, curriculum coverage) that were **not verified verbatim** and are deliberately absent from the body above.

**PMID 38966565** · Springer S 2024
> Approximately one in three owners reported that they never used internet resources prior to (31.7%) or after (37.0%) a consultation with their veterinarian.
> However, when owners do make use of the internet, our results show that they were more likely to use it before than after the consultation.
> The most common internet resources used by owners were practice websites (35.0%), veterinary association websites (24.0%), or 'other' websites providing veterinary information (55.2%).
> While access to online information can improve owners' knowledge of patient care and inform conversations with their veterinarian during consultations, there is also a risk that owners will misinterpret online information or gain a false impression of current standards in veterinary medicine.
> This in turn can cause problems or tensions, for example if the owner delays consulting their veterinarian about necessary treatment, or questions the veterinarian's medical advice.
> The results suggest that veterinarians should actively ask pet owners if they use internet resources, and what resources they use, in order to facilitate open discussion about information obtained from the internet.
> ⚠️ Dog and cat owners combined (N = 2117); the published abstract does not separate cat owners.
