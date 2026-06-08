# Form Reference — Resolving Vague References to AOC-CR Forms

Users rarely say "AOC-CR-307B." They say "I need a dismissal" or "the bond form" or
"the DWI judgment." This file maps everyday language to form numbers, and tells you
when a request is ambiguous and what single question resolves it.

## How to use this file

1. **Match the user's words** against the **Lay-term lookup** (Part A). It points you
   to one form number, or to a family (e.g. `307`, `601`, `619`) that has more than
   one edition.
2. **If the match is a family**, go to the **Disambiguation families** (Part B). Each
   family tells you the *default* edition, the *one question* to ask, and the cutoffs
   or labels needed to pick.
3. **Then run the skill's normal flow** (Phase 1.5 onward in `SKILL.md`) to confirm the
   chosen edition exists locally and pull its fields.

### The default rule (read this first)

Most ambiguity in this library is **edition-by-offense-date**: the same form is
reissued when the law changes, and which edition you use depends on **when the offense
was committed**, not today's date.

- The **newest edition is the default** when the user gives no other signal, but for any
  offense-date family you should **confirm the offense date before filling**, because old
  offenses are still charged and sentenced today. A wrong edition is a substantive error,
  not a cosmetic one.
- Editions are labeled by **offense date** ("For Offenses Committed ...") — except a few
  appeal-related forms (e.g. 321) labeled by **appeal-filing date**. Read the label.
- Don't silently pick. Either (a) the user already gave the offense date → choose the
  covering edition and say which one and why, or (b) they didn't → ask once, briefly.

### When to ask vs. when to just proceed

- **Single form, no editions** (e.g. 100 Warrant For Arrest, 119 Search Warrant) →
  proceed, no question.
- **Offense-date family** (307, 310, 342, 601, 619, ...) → ask the **offense date** if
  not already known.
- **Substantive-variant family** (323–336 Impaired Driving vs. Felony Speeding To Elude;
  313 willful-refusal vs. interlock) → ask **which variant**, not a date.
- **"Judgment," "expunction," "LDP," "conditional discharge"** are umbrella terms that
  cover many distinct forms → ask the **narrowing question** in Part A before anything
  else.

---

# Part A — Lay-term lookup

Organized by stage of the criminal process. Bold form numbers are exact, single forms.
A number shown as a family root (e.g. **307**, **601**, **619**) means "see Part B."

## Arrest, charging & process (100s)

| User says… | Form |
|---|---|
| warrant, arrest warrant, "issue a warrant" | **AOC-CR-100** (Warrant For Arrest); worthless check → **107** |
| criminal summons | **AOC-CR-113**; worthless check → **115** |
| magistrate's order | **AOC-CR-116** |
| search warrant | **AOC-CR-119**; blood/urine in DWI → **155** |
| order for arrest, OFA | **AOC-CR-217** |
| statement of charges, misdemeanor statement of charges | **AOC-CR-120** |
| indictment (generic) | **AOC-CR-122** |
| information (charging by information) | **AOC-CR-123** |
| affidavit | **AOC-CR-158** (continuation page → **158A**) |
| notice of process issued in error | **AOC-CR-170** |

**Charge-specific indictments** (use when the user names the crime):
murder → **124**; forcible rape → **125**; statutory rape (under 13) → **148**; statutory
sexual offense (under 13) → **149**; forcible sexual offense → **128**; indecent liberties
→ **150**; manslaughter → **127**; AWDWIKISI → **129**; first-degree burglary / felony B&E /
larceny / possession of stolen goods → **126**, **134**, **138**; robbery with a dangerous
weapon → **135**; common-law robbery → **136**; embezzlement → **130**; forgery / uttering
→ **133**; obtaining property by false pretenses → **137**; financial transaction card
theft/fraud → **152**; PWISD / sale & delivery / manufacture (drugs) → **151**; felony
impaired driving → **154**; related misdemeanor → **156**.

## Victims' rights (180s)

| User says… | Form |
|---|---|
| victim information sheet (law enforcement) | **180** family (by offense date) |
| misdemeanor / DV victim information sheet | **181** family (by offense date) |
| enforce victim's rights motion | **AOC-CR-182** |
| trafficking victim confidentiality | **AOC-CR-183** |

## Pretrial release, bond & counsel (200s)

| User says… | Form |
|---|---|
| conditions of release, release order | **AOC-CR-200**; DV → **630**; sex/violence-against-minor → **631**; threat of mass violence → **660** |
| appearance bond, bail bond, pretrial release bond | **AOC-CR-201** (pretrial); after judgment in superior court → **238** |
| additional bondsman / accommodation bondsman | **201A** (with 201) or **238A** (with 238) |
| waiver of trial, consent to entry of judgment (misdemeanor) | **AOC-CR-202** |
| nontestimonial identification | **AOC-CR-204** (application) / **205** (order) |
| competency, capacity to proceed, forensic evaluation | **207** family (local evaluator); **208** family (Butner commitment) |
| bond forfeiture | **AOC-CR-213** |
| surrender of defendant by surety | **AOC-CR-214** |
| joinder | **AOC-CR-212** |
| order appointing / denying counsel | **AOC-CR-224** |
| affidavit of indigency | **AOC-CR-226** |
| waiver of counsel | **AOC-CR-227** |
| show cause (failure to pay, FTA, jury summons) | **AOC-CR-219** |
| notice of hearing, unsupervised probation violation | **AOC-CR-220** |
| order for MAR hearing | **AOC-CR-221** |

## Pleas, trial, judgment & sentencing (300s + 600s)

| User says… | Form |
|---|---|
| transcript of plea, plea transcript, plea sheet | **AOC-CR-300** (continuation → 300A); plea in district court → **322** |
| **judgment, J&C, judgment and commitment** | **Umbrella — narrow first.** generic/other disposition → **301** / **305**; felony active → **601**; misdemeanor active → **602**; Class 3 misdemeanor → **629**; DWI → **342**; on probation revocation → **315** / **607** / **608** / **343** |
| **judgment suspending sentence, probation judgment, suspended sentence** | special probation → **302**; felony community/intermediate → **603**; misdemeanor community/intermediate → **604**; DWI → **310** |
| dismissal, dismissal / notice of reinstatement, voluntary dismissal | **307** family |
| aggravating / mitigating factors (felony) | **303** (findings) / **605** (structured sentencing) / **614** (notice) |
| extraordinary mitigation | **AOC-CR-606** |
| **prior record level, PRL, prior conviction level, sentencing worksheet** | **600** family (600A/600B worksheet; 600 = "Prior Convictions (Continued)" addendum) |
| restitution worksheet | **611** (initial sentencing) / **612** (revocation or termination) |
| **probation violation, violation of probation, VOP** | order on violation/modification → **AOC-CR-609**; judgment on revocation → **315** (general), **607** (felony SS), **608** (misd SS), **343** (DWI) |
| modify probation | **AOC-CR-609** |
| **deferred prosecution** | motion/agreement to defer → **610**; disposition/modification → **634** |
| **conditional discharge** | **Umbrella — narrow by statute.** 90-96(a) → **619**; 90-96(a1) → **627**; gang 14-50.29 → **621**; prostitution 14-204(b) → **628**; 15A-1341(a4) → **632**; 15A-1341(a5) → **633**; mass-violence threat 14-277.8 → **636**; disposition/modification → **635** |
| no-contact order (convicted sex / violent offender) | **620** family |
| sex offender registration notice | **AOC-CR-261**; SBM findings → **616**; SBM termination → **257** / **258** |
| credit against sentence | **AOC-CR-906** |
| misdemeanant confinement transfer | **AOC-CR-623** |

## Expunctions (mostly 263–299)

"Expunction" / "expungement" is an **umbrella — narrow by what's being expunged.**

| Ground | Form |
|---|---|
| charge(s) dismissed | **AOC-CR-287** (petition); DA-initiated → **295** |
| not guilty / not responsible | **AOC-CR-288**; DA-initiated → **296** |
| misdemeanor conviction | **AOC-CR-286** |
| nonviolent felony, under 18 | **AOC-CR-279** |
| nonviolent felony(ies) (instructions) | **AOC-CR-297** |
| nonviolent misdemeanor(s) (instructions) | **AOC-CR-298** |
| drugs / drug paraphernalia | **AOC-CR-266** |
| toxic vapors | **AOC-CR-268** |
| gang offenses | **AOC-CR-269** |
| prostitution offenses | **AOC-CR-282** |
| false report / threat of mass violence | **AOC-CR-289** |
| identity theft | **AOC-CR-263** / **283** |
| pardon of innocence | **AOC-CR-265** |
| DNA records | **AOC-CR-284** / **292** / **640** |
| additional agencies/offenses attachment | **AOC-CR-285** |
| certificate of relief | **AOC-CR-273** |

## Driving privileges & DWI (300s)

| User says… | Form |
|---|---|
| **limited driving privilege, LDP, hardship license** | **Umbrella — narrow.** speeding/reckless/etc. → **306**; DWI / open container / underage → **312**; interlock DWI → **340**; DWI with prior in 7 yrs (interlock) → **347**; willful refusal → **313** family; felony conviction → **318**; hit & run → **325**; failure-to-comply revocation → **345** |
| DWI judgment (active) | **342** family |
| DWI judgment suspending sentence | **310** family |
| DWI sentencing factors / grossly aggravating factors | **311** family / **338** family |
| DWI judgment on probation revocation | **343** family |
| implied consent notice | **AOC-CR-271** |
| **DWI / speeding-to-elude vehicle seizure** | **Variant family — ask which.** 323–336, 924 (see Part B2) |

## Appeals (300s/500s)

| User says… | Form |
|---|---|
| appellate entries | **AOC-CR-350** |
| order of remand | **321** family (by **appeal-filing** date) |

## Fugitive / extradition / specialized

| User says… | Form |
|---|---|
| fugitive | magistrate's order → **909**; warrant → **910**; affidavit → **911M** |
| extradition waiver | **AOC-CR-912M** |
| contempt (direct/summary) | **AOC-CR-390** |
| waiver of jury trial | **AOC-CR-405** |
| continuance | district/general → **409**; superior court → **410**; DWI w/ forfeiture → **337** |
| restoration of citizenship | out-of-state/federal → **919**; unsupervised/fine-only → **926** |
| mediation report | **AOC-CR-700** |

---

# Part B — Disambiguation families

## B1 — Offense-date edition families (ask the OFFENSE DATE)

For these, members differ only by the offense-date window. **Ask the offense date if it
isn't already known**, then pick the edition whose window covers it. If the user gives no
date and wants a blank/current form, default to the newest edition but say so.

| Family | Members & offense-date window |
|---|---|
| **307** Dismissal / Notice Of Reinstatement | **307A** on/before Nov 30 2013 · **307B** on/after Dec 1 2013 *(default 307B)* |
| **180** Victim Info Sheet (LE) | **180A** before Aug 31 2019 · **180B** on/after Aug 31 2019 *(default 180B)* |
| **181** Misd/DV Victim Info Sheet | **181A** before Aug 31 2019 · **181B** on/after Aug 31 2019 *(default 181B)* |
| **207** Order Appointing Forensic Evaluator | **207A** on/before Nov 30 2013 · **207B** on/after Dec 1 2013 *(default 207B)* |
| **208** Commitment To Butner For Capacity Exam | **208A** / **208B** — read each PDF's date label; default 208B |
| **310** DWI Judgment Suspending Sentence | **310A** before Dec 1 2009 · **310B** Dec 1 2009–Nov 30 2011 · **310C** Dec 1 2011–Nov 30 2016 · **310D** Dec 1 2016–Nov 30 2023 · **310E** Dec 1 2023–Nov 30 2025 · **310F** on/after Dec 1 2025 *(default 310F)* |
| **311** DWI Determination Of Sentencing Factors | before Dec 1 2011 · on/after Dec 1 2011 — **same form number, two editions; pass exact filename** *(default: on/after Dec 1 2011)* |
| **338** Notice Of Grossly Aggravating/Aggravating Factors (DWI) | before Dec 1 2011 · on/after Dec 1 2011 — **same number; exact filename** *(default: on/after)* |
| **342** DWI Judgment And Commitment | **342A** before Dec 1 2011 · **342B** Dec 1 2011–Nov 30 2025 · **342C** on/after Dec 1 2025 *(default 342C)* |
| **343** DWI J&C Upon Revocation Of Probation | before Dec 1 2025 · on/after Dec 1 2025 — **same number; exact filename** *(default: on/after)* |
| **601** J&C Active Punishment — Felony (SS) | before Dec 1 2025 · on/after Dec 1 2025 — **same number; exact filename** *(default: on/after)* |
| **602** J&C Active Punishment — Misdemeanor (SS) | before Dec 1 2025 · on/after Dec 1 2025 — **same number; exact filename** *(default: on/after)* |
| **603** Judgment Suspending Sentence — Felony (SS) | **603A** before Dec 1 2009 · **603B** Dec 1 2009–Nov 30 2011 · **603C** Dec 1 2011–Nov 30 2016 · **603D** Dec 1 2016–Nov 30 2023 · **603E** Dec 1 2023–Nov 30 2025 · **603F** on/after Dec 1 2025 *(default 603F)* |
| **604** Judgment Suspending Sentence — Misdemeanor (SS) | **604A**–**604F**, same windows as 603 *(default 604F)* |
| **607** J&C Upon Revocation — Felony (SS) | before Dec 1 2025 · on/after Dec 1 2025 — **same number; exact filename** *(default: on/after)* |
| **608** J&C Upon Revocation — Misdemeanor (SS) | before Dec 1 2025 · on/after Dec 1 2025 — **same number; exact filename** *(default: on/after)* |
| **600** PRL/PCL Worksheet | **600A** before Dec 1 2009 · **600B** on/after Dec 1 2009 · **600** = "Prior Convictions (Continued)" addendum, not an edition *(default worksheet: 600B)* |
| **619** Conditional Discharge 90-96(a) | **619A**–**619F**: before Dec 1 2009 · …2009–2011 · …2011–2016 · …2016–2023 · …2023–2025 · on/after Dec 1 2025 *(default 619F)* |
| **627** Conditional Discharge 90-96(a1) | **627A**–**627F**, same windows as 619 *(default 627F)* |
| **621** Conditional Discharge 14-50.29 (gang) | **621A** Dec 1 2008–Nov 30 2009 · then **621B**–**621F** same windows as 619 *(default 621F)* |
| **632** Conditional Discharge 15A-1341(a4) | **632A**–**632F**, same windows as 619 *(default 632F)* |
| **633** Conditional Discharge 15A-1341(a5) | **633A**–**633F**, same windows as 619 *(default 633F)* |
| **628** Conditional Discharge 14-204(b) (prostitution) | **628C** Oct 1 2013–Nov 30 2016 · **628D** Dec 1 2016–Nov 30 2023 · **628E** Dec 1 2023–Nov 30 2025 · **628F** on/after Dec 1 2025 *(default 628F)* |
| **636** Conditional Discharge 14-277.8 (mass-violence threat) | **636D** Dec 1 2018–Nov 30 2023 · **636E** Dec 1 2023–Nov 30 2025 · **636F** on/after Dec 1 2025 *(default 636F)* |
| **620** Permanent No-Contact Order | **Watch the title change.** Dec 1 2009–Nov 30 2025 = "Convicted **Sex** Offender" · on/after Dec 1 2025 = "Convicted **Violent** Offender" — **same number; exact filename** *(default: on/after)* |

> **Appeal-date exception — 321.** **321A** for appeals filed **before** Dec 1 2015 ·
> **321B** for appeals filed **on/after** Dec 1 2015. Ask the **appeal-filing date**, not
> the offense date *(default 321B)*.

## B2 — Substantive-variant families (ask WHICH VARIANT, not a date)

Here the suffix marks a different situation, not a different edition. Ask the user the
distinguishing question.

**DWI / Felony-Speeding-to-Elude vehicle seizure** — every "A" is **Impaired Driving**,
every "B" is **Felony Speeding To Elude**. Ask: *"Is this an impaired-driving seizure or a
felony-speeding-to-elude seizure?"*

| # | A = Impaired Driving / B = Felony Speeding To Elude |
|---|---|
| **323** | Officer's affidavit for seizure & impoundment + magistrate's order |
| **324** | Prosecutor's notice of forfeiture hearing |
| **330** | Non-defendant owner's petition for release (acknowledgment) |
| **331** | Bond to secure temporary pretrial release of vehicle |
| **332** | Order on non-defendant owner's petition |
| **333** | Defendant-owner's petition for release |
| **334** | Lienholder's petition for release |
| **335** | Order forfeiting vehicle after hearing |
| **336** | Order releasing vehicle after disposition |
| **924** | Application/order for release of vehicle declared a total loss |

**313 — Limited Driving Privilege, Willful Refusal.** **313A** = standard LDP · **313B** =
**Interlock** LDP. Ask: *"Does this privilege require an ignition interlock?"*

**Continuations & addenda (not editions — pull alongside the base form):**

| # | Meaning |
|---|---|
| **158A** | continuation page for the **158** affidavit |
| **300A** | continuation page for the **300** transcript of plea |
| **201A** | additional accommodation bondsman for the **201** appearance bond |
| **238A** | additional bondsmen / file numbers for the **238** post-judgment bond |
| **611A** / **612A** | restitution worksheet addenda for **611** / **612** |
| **285** | additional agencies/offenses attachment for an expunction petition |
| **600** | "Prior Convictions (Continued)" addendum for the **600A/600B** worksheet |
| **626** | additional file numbers / offenses (general attachment) |

**AOC-CR-UNKNOWN (two entries).** Both are out-of-state/federal-conviction LDP forms:
one **Interlock** ("Interlock Limited Driving Privilege Impaired Driving (Out-Of-State Or
Federal Convictions)") and one standard ("Limited Driving Privilege Impaired Driving
(Out-Of-State Or Federal Convictions)"). The form number didn't parse, so **always select
by exact filename** and confirm interlock vs. standard with the user.

## B3 — Same-number editions: always pass the exact filename

These nine numbers have two PDFs under the **same** form number, so the fill script cannot
tell them apart from the number alone — it will stop and list them. Confirm the edition
(per B1/B2) and pass the **exact filename**:

```
AOC-CR-311-Impaired-Driving-Determination-Of-Sentencing-Factors-For-Offenses-Committed-Before-Dec-1-2011.pdf
AOC-CR-311-Impaired-Driving-Determination-Of-Sentencing-Factors-For-Offenses-Committed-On-Or-After-Dec-1-2011.pdf
AOC-CR-338-Notice-Of-Grossly-Aggravating-And-Aggravating-Factors-DWI-For-Offenses-Committed-Before-Dec-1-2011.pdf
AOC-CR-338-Notice-Of-Grossly-Aggravating-And-Aggravating-Factors-DWI-For-Offenses-Committed-On-Or-After-Dec-1-2011.pdf
AOC-CR-343-Impaired-Driving-Judgment-And-Commitment-Upon-Revocation-Of-Probation-For-Offenses-Committed-Before-Dec-1-2025.pdf
AOC-CR-343-Impaired-Driving-Judgment-And-Commitment-Upon-Revocation-Of-Probation-For-Offenses-Committed-On-Or-After-Dec-1-2025.pdf
AOC-CR-601-Judgment-And-Commitment-Active-Punishment-Felony-Structured-Sentencing-For-Offenses-Committed-Before-Dec-1-2025.pdf
AOC-CR-601-Judgment-And-Commitment-Active-Punishment-Felony-Structured-Sentencing-For-Offenses-Committed-On-Or-After-Dec-1-2.pdf
AOC-CR-602-Judgment-And-Commitment-Misdemeanor-Active-Punishment-Structured-Sentencing-For-Offenses-Committed-Before-Dec-1-2025.pdf
AOC-CR-602-Judgment-And-Commitment-Misdemeanor-Active-Punishment-Structured-Sentencing-For-Offenses-Committed-On-Or-After-Dec.pdf
AOC-CR-607-Judgment-And-Commitment-Upon-Revocation-Of-Probation-Felony-Structured-Sentencing-For-Offenses-Committed-Before-Dec.pdf
AOC-CR-607-Judgment-And-Commitment-Upon-Revocation-Of-Probation-Felony-Structured-Sentencing-For-Offenses-Committed-On-Or-Afte.pdf
AOC-CR-608-Judgment-And-Commitment-Upon-Revocation-Of-Probation-Misdemeanor-Structured-Sentencing-For-Offenses-Committed-Before-Dec-1-2025.pdf
AOC-CR-608-Judgment-And-Commitment-Upon-Revocation-Of-Probation-Misdemeanor-Structured-Sentencing-For-Offenses-Committed-On-Or.pdf
AOC-CR-620-Convicted-Sex-Offender-Permanent-No-Contact-Order-For-Offenses-Committed-Dec-1-2009-Nov-30-2025.pdf
AOC-CR-620-Convicted-Violent-Offender-Permanent-No-Contact-Order-For-Offenses-Committed-On-Or-After-Dec-1-2025.pdf
AOC-CR-UNKNOWN-Interlock-Limited-Driving-Privilege-Impaired-Driving-Out-Of-State-Or-Federal-Convictions.pdf
AOC-CR-UNKNOWN-Limited-Driving-Privilege-Impaired-Driving-Out-Of-State-Or-Federal-Convictions.pdf
```

> Filenames above are reproduced from the index for guidance. The **authoritative**
> filenames are whatever Phase 1.5 prints from `fields_index.json` — if a name here ever
> disagrees with the index, trust the index and pass that exact string.

---

# Quick worked example (the canonical case)

> **User:** "I need a dismissal form."
>
> 1. Lay-term lookup → "dismissal" = **307** family.
> 2. Part B1 → 307 is offense-date: **307A** (on/before Nov 30 2013) vs **307B** (on/after
>    Dec 1 2013), default **307B**.
> 3. Respond: *"That's the AOC-CR-307 Dismissal / Notice of Reinstatement. I'll use 307B,
>    the current edition for offenses committed on or after Dec. 1, 2013 — unless the
>    offense was on or before Nov. 30, 2013, in which case it's 307A. What's the offense
>    date?"*
> 4. Proceed to Phase 1.5 with the confirmed edition.
