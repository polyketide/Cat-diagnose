# What Cats Actually Present With, and What They Die Of

> **Generated**: 2026-07-20 **Method**: PubMed sweep from three angles (primary-care prevalence, mortality/longevity, disease-specific VetCompass studies), screened locally, seven papers archived and quoted verbatim.
> **Why this file exists**: this repository chose its topics from one cat's illness. Before choosing the next one it needed evidence about what cat owners actually face, rather than an assumption. The assumption turned out to be right in direction and badly wrong in magnitude.
> ⚠️ **Nearly all of this is UK VetCompass data.** Free-roaming access, insurance rates, neutering rates and referral patterns differ by country, and trauma in particular is a UK-specific figure. Read the ordering as robust and the absolute values as local.

---

## 0. The whole thing in one sentence

**Cats are seen for teeth, weight, fleas and injuries; they die of trauma, kidneys and cancer — and the disease this repository has written most about occurs in roughly 1 cat in 2000.**

---

## 1. What brings a cat to a vet

Two VetCompass samples, nine years apart, agree closely.

| Disorder | 2019 (n = 18,249 of 1,255,130) | 2009-14 (n = 3584 of 142,576) |
|---|---|---|
| **Periodontal disease** | **15.2%** (95% CI 14.72-15.76) | **13.9%** (95% CI 12.5-15.4) |
| **Obesity** | **11.6%** (95% CI 11.12-12.06) | 6.7% (95% CI 5.7-7.6) |
| **Dental disease** (separate code) | 8.2% (95% CI 7.84-8.64) | — |
| Flea infestation | — | 8.0% (95% CI 7.0-8.9) |

By disorder *group* in the earlier study: dental 15.1%, traumatic injury 12.9%, dermatological 10.4%.

**Periodontal disease is the single most common specific diagnosis in cats**, and the authors say so directly. It is also not an isolated finding: cats with it carried a median of 3 comorbid disorders against 1 in cats without, and had **1.79 times the odds** (95% CI 1.62-1.99) of at least one comorbid diagnosis (PMID 36912667).

⚠️ **The comorbidity association is not evidence that dental disease causes the others.** Age drives both — median age with periodontal disease 9.47 years vs 4.94 without — and a cat seen often enough to have its teeth recorded is a cat seen often enough to have everything else recorded too. **Ascertainment and age are unadjusted confounders here**, and the direction of any causal arrow is not established by these data.

### The chronic diseases of older cats

| Disease | Prevalence | Source |
|---|---|---|
| **Chronic kidney disease** | **1.2%** (95% CI 1.1-1.3) of all cats | PMID 31023949, 353,448 cats, 2012-13 |
| **Diabetes mellitus** | **0.39%** annual (95% CI 0.37-0.42); incidence 0.14% | PMID 40525629, 1,255,130 cats, 2019 |
| **Lymphoma** | **48 per 100,000** = 0.048% (95% CI 44-56); incidence 32/100,000 | PMID 33325082, 562,446 cats, 2016 |

---

## 2. What cats die of

Of 4009 confirmed deaths sampled from 118,016 cats (PMID 24925771):

| Cause | Share of deaths |
|---|---|
| Trauma | 12.2% |
| **Renal disorder** | **12.1%** |
| Non-specific illness | 11.2% |
| **Neoplasia** | **10.8%** |
| Mass lesion disorders | 10.2% |

Median longevity **14.0 years** (IQR 9.0-17.0).

⚠️ **These five causes are separated by two percentage points across the whole list — do not read the ordering as a ranking.** No confidence intervals are given for the individual shares in the abstract, and "non-specific illness" at 11.2% is large enough that reallocating it would reshuffle everything below trauma. What the data support is that renal disease and neoplasia are each roughly a tenth of feline deaths; not that either outranks the other.

⚠️ **"CKD is the most frequent cause of death in cats aged over five years" is a background statement, not a result.** It appears in the introduction of PMID 31023949, which measured prevalence and survival — not cause of death — and the abstract attaches no citation to it. Quoted in this file as what the authors state, and **it must not be cited as a measured finding of that study.** It is consistent with the all-ages mortality data above (where trauma, a young cat's death, is what edges it out), but consistency is not verification.

---

## 3. ⭐ The two facts that do not sit together

**Fact one: cancer is a leading cause of feline death** — 10.8% of them, plus some share of "mass lesion disorders". Oncology is not a misplaced topic.

**Fact two: any *individual* cancer is rare.** Lymphoma, the commonest feline malignancy and the one this repository has written most about, has a prevalence of **48 per 100,000**. Periodontal disease, at 15.2%, is about **300 times** more common.

Both are true because "neoplasia" aggregates dozens of diagnoses while "periodontal disease" is one. **The mistake to avoid is choosing coverage from the mortality table and then writing about a single tumour type**, which is what happened here: this repository grew from one cat's nasal lymphoma into five oncology-adjacent files, and had nothing at all on teeth, weight, kidneys or diabetes.

⚠️ **Frequency is not importance, and this file must not be used to argue that it is.** A rare disease an owner is facing right now is the most important disease in the world to them, and the existing oncology files stay. The claim here is narrower: **a knowledge base that only covers rare presentations will be silent for most owners on most days.**

---

## 4. Where the evidence pointed the next entry

Chronic kidney disease, on four grounds this file can now support rather than assert:

1. **Frequency.** 1.2% prevalence, 25× lymphoma, and renal disease is ~12% of all feline deaths.
2. **It is an integration gap, not a data gap** (`docs/LITERATURE-PIPELINE-SOP.md` §7a). The evidence exists; it is split across nephrology, endocrinology, nutrition and hypertension literatures.
3. **This repository already holds half of it.** `hyperthyroidism-and-kidney-disease.md` covers the masking problem; `feline-hypertension.md` covers a comorbidity that goes unmeasured. Neither has a CKD entry to join to.
4. **The decisions are the owner's and they are relentless** — subcutaneous fluids, renal diet, when monitoring is worth the stress of a car journey, when to stop. Exactly the shape §7a calls addressable.

---

## 5. Findings the screen itself produced

These came out of reading the papers chosen to justify a topic, and are worth more than the justification.

### 5.1 ⭐ CKD is diagnosed late and then barely measured

Among cats diagnosed with CKD in UK primary care (PMID 31023949):

- **66.6% already had clinical signs at diagnosis** — so two thirds were found by symptoms, not by screening.
- **32.6%** had serum creatinine investigated or monitored.
- **14.9%** had a urine protein:creatinine ratio.
- **25.6%** had blood pressure measured.
- Median survival after diagnosis: **388 days** (IQR 88-1042).

**The blood pressure number is the join this repository was built to make.** `feline-hypertension.md` records that 96.5% of clinics own a direct ophthalmoscope and 73.1% of practitioners report struggling to interpret ocular findings, and that hypertension is more frequent in cats with CKD. Here is the consequence, measured in the same population: **three quarters of cats diagnosed with the disease most associated with hypertension never had their blood pressure taken.**

⚠️ **This is not a criticism of clinicians.** A first-opinion consultation is short, the cat is stressed, the owner is paying out of pocket, and none of those constraints were measured here. What the figure supports is that **an owner asking "has her blood pressure been checked?" is asking about something that usually has not happened** — which is a question, not a complaint, and belongs to the vet to answer.

### 5.2 ⭐ One in five diabetic cats is euthanised within three days of diagnosis

Of cats dead within 3 years of a diabetes diagnosis, 93.0% (176/192) were euthanised — and **19.7% (35/178) were euthanised within 3 days of diagnosis** (PMID 40525629).

Three days is not a treatment failure. It is barely time to fill a prescription. **This is a decision made at the moment of diagnosis**, when an owner has just heard "diabetes" and is estimating a lifetime of injections, cost and confinement.

⚠️ **What this does and does not license.** It does not license second-guessing any individual decision: these cats were a mean 11.8 years old, many had comorbidities the abstract does not report, and euthanasia is often the right answer. It does not measure how many owners were informed of what. What it does establish is that **the 72 hours after a feline diabetes diagnosis carry a large, irreversible decision**, and that is precisely where having the evidence assembled in advance could matter. Feline diabetes can go into remission with early intensive management — a fact an owner making a three-day decision may never hear.

⚠️ **Remission is asserted here from general veterinary knowledge and is NOT yet sourced in this repository.** It is the obvious next retrieval and must not be repeated as established until it is.

---

## 6. What this file does not establish

- **Anything outside the UK.** Trauma at 12.2% of deaths reflects outdoor access patterns; the chronic-disease ordering is likely more transferable than the absolute values, but that is an expectation, not a finding.
- **Whether earlier detection of any of these improves outcome.** Every file in this repository that asks this question has failed to answer it (`feline-hypertension.md`, `hyperthyroidism-and-kidney-disease.md`, `emergency-triage-red-flags.md`). This one does not answer it either. **Prevalence justifies writing about a disease; it does not justify screening for it.**
- **Cause for any association reported above.** All of it is observational primary-care record data, and diagnosis codes record what was written down, not what the cat had.

---

## 参考文献（原文记录）

> ⚠️ **These entries are generated from the archived PubMed records, not written.** The first draft of this list was hand-typed and **three of its seven entries were wrong**: `33325082`'s first author is Economu L, not Schofield I; `40525629`'s is Waite O, not Bennett K, with the DOI and page number also wrong by one digit (`70161`, not `70160`); and `36912667` is issue 3, not 5. Every error was invented by recall while writing a file whose argument is that recall is not evidence. See `docs/LITERATURE-PIPELINE-SOP.md` §3d.

- O'Neill DG, et al. Longevity and mortality of cats attending primary care veterinary practices in England. *J Feline Med Surg* 2015;17(2):125-33. PMID 24925771. [DOI](https://doi.org/10.1177/1098612X14536176)
- O'Neill DG, et al. Prevalence of disorders recorded in cats attending primary-care veterinary practices in England. *Vet J* 2014;202(2):286-91. PMID 25178688. [DOI](https://doi.org/10.1016/j.tvjl.2014.08.004)
- Conroy M, et al. Chronic kidney disease in cats attending primary care practice in the UK: a VetCompass. *Vet Rec* 2019;184(17):526. PMID 31023949. [DOI](https://doi.org/10.1136/vr.105100)
- Economu L, et al. Incidence and risk factors for feline lymphoma in UK primary-care practice. *J Small Anim Pract* 2021;62(2):97-106. PMID 33325082. [DOI](https://doi.org/10.1111/jsap.13266)
- O'Neill DG, et al. Commonly diagnosed disorders in domestic cats in the UK and their associations with sex and age. *J Feline Med Surg* 2023;25(2):1098612X231155016. PMID 36852509. [DOI](https://doi.org/10.1177/1098612X231155016)
- O'Neill DG, et al. Periodontal disease in cats under primary veterinary care in the UK: frequency and risk factors. *J Feline Med Surg* 2023;25(3):1098612X231158154. PMID 36912667. [DOI](https://doi.org/10.1177/1098612X231158154)
- Waite O, et al. Frequency, Risk Factors, and Mortality for Diabetes Mellitus in 1 225 130 Cats Under Primary Veterinary Care in the United Kingdom in 2019. *J Vet Intern Med* 2025;39(4):e70161. PMID 40525629. [DOI](https://doi.org/10.1111/jvim.70161)

---

## 原文摘录（source excerpts）

**PMID 24925771** · O'Neill DG 2015
> The most frequently attributed causes of mortality in cats of all ages were trauma (12.2%), renal disorder (12.1%), non-specific illness (11.2%), neoplasia (10.8%) and mass lesion disorders (10.2%).
> Overall, the median longevity was 14.0 years (interquartile range [IQR] 9.0-17.0; range 0.0-26.7).
> From 118,016 cats attending 90 practices in England, 4009 cats with confirmed deaths were randomly selected for detailed study.
> ⚠️ Sampled deaths, not a full mortality census; causes are as attributed in primary-care records.

**PMID 25178688** · O'Neill DG 2014
> The most prevalent diagnosis-level disorders were periodontal disease (n = 499; prevalence, 13.9%, 95% confidence intervals [CI], 12.5-15.4), flea infestation (n = 285; prevalence, 8.0%; 95% CI, 7.0-8.9) and obesity (n = 239; prevalence, 6.7%; 95% CI, 5.7-7.6).
> The most prevalent disorder groups recorded were dental conditions (n = 540; prevalence, 15.1%, 95% CI, 13.6-16.6), traumatic injury (n = 463; prevalence, 12.9%; 95% CI, 11.6-14.3) and dermatological disorders (n = 373; prevalence, 10.4%; 95% CI, 9.2-11.7).
> From a study population of 142,576 cats attending 91 clinics across Central and South-East England from 1 September 2009 to 15 January 2014, a random sample of 3584 was selected for detailed clinical review to extract information on all disorders recorded.

**PMID 31023949** · Conroy M 2019
> From 353,448 cats attending 244 clinics, the prevalence of CKD was estimated as 1.2 per cent (95 per cent CI 1.1 per cent to 1.3 per cent).
> Most cats with CKD had clinical signs at diagnosis (66.6 per cent).
> Few cats underwent investigations or monitoring of serum creatinine (32.6 per cent), urine protein:creatinine ratio (14.9 per cent) or blood pressure measurement (25.6 per cent).
> A proprietary renal diet was the most frequently prescribed management (63.8 per cent).
> Median survival time following diagnosis was 388 days (IQR 88-1042 days).
> Chronic kidney disease (CKD) is a frequent diagnosis in cats attending primary care practice and the most frequent cause of death in cats aged over five years, yet there is limited published research for CKD in cats attending primary care practice.
> ⚠️ The last sentence is the authors' **introduction**, not their result. This study measured prevalence, management and survival; it did not measure cause of death, and the abstract attaches no citation to the claim. Cite it as a statement by the authors, never as a finding of this study.
> ⚠️ "per cent" is the journal's house style and is quoted as printed.

**PMID 33325082** · Economu L 2021
> From a cohort of 562,446 cats under veterinary care at VetCompass participating practices in 2016, a total of 271 lymphoma cases were identified (prevalence: 48/100,000, 95% confidence interval (CI) 44 to 56/100,000; incidence 32/100,000, 95% CI 26 to 35/100,000).
> Cases were required to have had an external laboratory confirmed diagnosis based on cytology and/or histopathology.
> Vaccinated cats were associated with decreased odds (OR 0.7, 95% CI 0.5 to 1.0) compared to unvaccinated cats, although the type of vaccination received was not statistically significant.
> ⚠️ Requiring laboratory confirmation makes this an **underestimate** of clinically suspected lymphoma: a cat treated presumptively, or one whose owner declined sampling, is not a case here. The direction of that bias is knowable; its size is not.
> ⚠️ The vaccination odds ratio has an upper bound of exactly 1.0 and the authors do not interpret it as protective. **Do not cite it as evidence that vaccination prevents lymphoma.**

**PMID 36852509** · O'Neill DG 2023
> The most prevalent disorders were periodontal disease (n = 2780 [15.2%], 95% confidence interval [CI] 14.72-15.76), obesity (n = 2114 [11.6%], 95% CI 11.12-12.06) and dental disease (n = 1502 [8.2%], 95% CI 7.84-8.64).
> A random sample of 18,249 cats was obtained from 1,255,130 cats under primary care during 2019 within VetCompass, an epidemiological research programme based on anonymised primary care veterinary clinical records.
> Younger cats (<8 years) had an increased prevalence of cat bite abscess, flea infestation and RTA, while older cats (⩾8 years) had increased prevalence of lameness, cystitis and dental disease, among others.
> These findings suggest that the veterinary profession needs to engage more effectively in informing owners on common preventable disorders (ie, obesity and dental disease).

**PMID 36912667** · O'Neill DG 2023
> Periodontal disease had a 1-year period prevalence of 15.2% (95% confidence interval [CI] 14.72-15.76).
> The median age of cats with periodontal disease (9.47 years, interquartile range [IQR] 5.96-12.97) was higher than for cats without periodontal disease (4.94 years, IQR 1.95-9.51; P <0.001).
> Cats with periodontal disease had a higher median count of comorbid disorders per individual cat (3, IQR 2-4, range 1-14) than cats without periodontal disease (1, IQR 0-2, range 0-15; P <0.001).
> Cats with periodontal disease had 1.79 times the odds (95% CI 1.62-1.99, P <0.001) of diagnosis with at least one comorbid disorder disease than cats without periodontal disease.
> Periodontal disease is the most common specific diagnosis in cats and is confirmed as a leading health issue in cats.
> ⚠️ The comorbidity odds ratio is **not adjusted for age or for how often the cat was seen**, both of which drive dental recording and every other diagnosis. Cited in the body as association only.

**PMID 40525629** · Waite O 2025
> Annual prevalence was 0.39% (95% confidence interval [CI]: 0.37-0.42).
> Of 51.2% (192/375) cats dead within 3 years of diagnosis, 93.0% (176/192) were euthanized; 19.7% (35/178) were euthanized ≤ 3 days after diagnosis.
> Mean age and median adult body weight of incident cases diagnosed with DM was 11.8 ± 3.5 years (n = 371) and 5.9 kg (interquartile range: 4.6-7.1, n = 327).
> Early mortality associated with DM diagnosis in cats is high.
> ⚠️ Note the shifting denominators the source itself uses — 375, 192, 178 — and that the 19.7% is of 178, not of all diagnosed cats. Comorbidities present at diagnosis are not reported in the abstract, so **nothing here supports a judgement about whether any individual decision was right.**
