# Task 01 — Maintainer self-review and deferred reviewer routes

**Current status — 4 October 2026:** task 01 is complete for the bounded reviewed scope; see the [adopted maintainer decision](distribution-decision.md). Original Wawet work and optional user-installed RNS research continue with conditions; upstream redistribution and commercial bundles remain unapproved. G01 remains HOLD; tasks 02–05 remain open. Earlier pending-adoption, mandatory-review and uncommitted-status entries below are historical. The maintainer subsequently authorised committing and pushing this decision package.

Prepared **4 October 2026** against clean HEAD `ff3df9f`, which commits the
[existing dossier](distribution-review.md). **Status: arrangement package prepared;
no reviewer selected, contacted or engaged.** Task 01 remains open; gates 01–05
and G01 HOLD persist. No new artefacts, runtime changes or legal interpretation
are introduced. The maintainer reports no reviewer or two-host setup available.

## Current direction — maintainer self-review

**DESIGN DECISION — 4 October 2026:** the maintainer declined hiring a reviewer
and will do the best achievable review within a solo, free-time project. Paid
reviewer selection and engagement are deferred; the shortlist/enquiry below are
retained as historical preparation, not the recommended next action. No external
contact or spending is assumed.

The next task 01 package is a bounded self-review, in sequential sessions:

1. Work through the existing exact RNS licence header and Q01–Q03/Q07. Create
   a clause-to-question evidence table with separate columns for verbatim source
   reference, maintainer interpretation and unresolved ambiguity. Include actual
   AI-assisted development/tooling use; do not assert that a restriction is
   inapplicable without evidence.
2. Resolve the dossier's ConfigObj/validate/i2plib notice gaps using attributable
   exact-version upstream sources. Match them to the vendored components and
   record any modification/provenance uncertainty. Preserve original terms.
3. For Q04, distinguish source obligations from the two inspected research wheels;
   document what native/Rust evidence can be established and what requires a final
   build. Keep Q05/Q06 conditional: no firmware or LXMF is selected.
4. Draft a maintainer distribution decision separately for original source,
   user-installed experiments and hypothetical bundled images. Record conditions,
   notices, missing evidence and alternatives if restrictions cannot be reconciled.
   Keep bundled distribution on HOLD until exact platform/build review exists.

**Acceptance for the self-review package:** Q01–Q07 each have evidence-backed
findings or an explicit unresolved reason; vendored notice gaps are resolved or
precisely recorded; a dated maintainer assessment states form-specific decisions
and limits. Verify captured hashes/provenance, check local Markdown links and
review the diff. No runtime change or repeated campaign is required.

This is maintainer due diligence, not qualified legal advice. The current task 01
acceptance criterion still requires qualified written review; self-review alone
cannot close it. Do not make paid review a prerequisite for continuing this bounded
work. If the maintainer later chooses to change the gate's assurance requirement,
record that explicit decision, rationale and residual risk in the plan and licensing
ADR rather than silently marking the old requirement satisfied. G01 remains HOLD.

## Three UK-accessible routes — deferred

**FACT — provider descriptions checked 4 October 2026:** the primary pages below
were opened and read. They establish advertised services/contact routes, not
independently verified competence, availability, pricing or acceptance of Wawet.
No contact form was submitted. These are two legal-review candidates and one
community referral route, not three appointed reviewers.

| Route | Primary expertise evidence | Enquiry process | Published fee information and limits |
| --- | --- | --- | --- |
| Moorcrofts LLP, UK legal-review candidate | [Open Source Software service](https://moorcrofts.com/services/open-source-software/) describes licence analysis, usage assessments, commercialisation and audits; directs initial consultations to Usha Guness. | [Contact](https://moorcrofts.com/contact/): team@moorcrofts.com or +44 (0)1628 470000; request the open-source specialist. | [Firm homepage](https://moorcrofts.com/) says specific advice can be quoted at a fixed fee. No numeric price for this review found on these pages. Consultation cost, scope, availability and acceptance unknown. |
| Bristows, UK legal-review candidate | [Open source practice](https://www.bristows.com/expertise/advisory/open-source/) describes advising on use and redistribution, licence drafting and work with startups. | [Contact](https://www.bristows.com/contact/): use the firm's published contact route and request the open-source practice. | No review price found on the inspected practice/contact pages. Fees, availability and willingness to accept this small engagement unknown. |
| FSFE Licence Questions team, community guidance/referral | [Licensing FAQ and team description](https://fsfe.org/freesoftware/legal/faq.en.html) describes volunteer licensing experts and contacts for specialist lawyers, including the UK. | English email to licence-questions@fsfe.org; request referral to UK counsel for restricted-use terms. | No fee schedule stated on this page; do not assume a free commissioned review. FSFE expressly cannot give legal advice. Its response cannot satisfy task 01's qualified written review; acceptance of questions about restricted Reticulum terms and referral availability unknown. |

**DESIGN DECISION — suggested enquiry order:** try Moorcrofts first because its
page identifies a specialist consultation route and its homepage offers fixed-fee
quotes for specific advice. This is a fit inference, not a price or quality ranking.
Bristows is a second legal-review candidate. Use FSFE for referral if needed;
do not send it the legal commissioning enquiry unchanged. Recipient selection and
outreach authorisation remain with the maintainer. Obtain a quote before budgeting.

## Unsent enquiry for a legal-review candidate

Subject: Scoped written software distribution review — Hathorsoft / Wawet

Hello,

Hathorsoft Ltd maintains Wawet, an early-stage civilian communications project
whose first application is nearby road-hazard reporting from a tactile vehicle
appliance. Basic use is intended to work without a phone, account, cloud or
subscription. Commercial hardware is intended, but no product image is selected.
One maintainer is progressing the research in their free time.

Could your open-source/software licensing team assess suitability, scope, fees
and availability for a bounded written review? Original software/specifications
are Apache-2.0 and prose CC BY 4.0. The independent standard-library simulator is
separate from optional experiments pinned to RNS 1.5.5, cryptography 50.0.2,
pyserial 3.5, cffi 2.1.1 and pycparser 3.0. RNS has restricted-use and model-training
terms; we seek interpretation rather than assume it is MIT. AI-assisted development
and preparation of this dossier are part of the actual tooling to assess.

Our [distribution review dossier](distribution-review.md) and
[seven-artefact hash register](results/distribution-review/artefact-register.json)
contain captured notices, known vendored/native evidence gaps and Q01–Q07.
The technical baseline is Wawet revision
`ff3df9fffb98a7b7f08512f440b1a72deb908a47`.

We request a written assessment tied to that revision, exact artefact hashes and
civilian intended use, separately covering original-source distribution and
user-installed experiments. Please answer Q01–Q07, identify permitted,
conditional, unapproved or unresolved forms, notice/source obligations,
restrictions, exclusions and necessary follow-up. For a future bundled commercial
image, please identify evidence and review requirements only: final platform,
interpreter/OS, native builds and firmware remain unselected, so bundled-image
approval must remain pending. LXMF is unselected and not installed; RNode firmware
needs separate exact-version review if selected.

Please identify the responsible reviewer's qualifications, applicable jurisdiction,
any conflicts, evidence-sharing requirements, and whether a fixed-fee first stage
with a written outcome and one clarification round is possible. Please quote fees,
VAT, exclusions, expected availability and any additional work separately. This is
an enquiry only; it does not commission work or authorise costs.

Regards,
Hathorsoft Ltd — Wawet maintainer

**Dispatch note:** links above resolve within this repository, not a recipient's
mail client. Before authorised sending, attach the dossier and its linked evidence
as a read-only copy of the stated revision, or supply an already accessible,
verified revision-specific link. Do not invent a public URL or publish the repo
for this purpose. Retain original third-party notices with the evidence. Add the
maintainer's chosen sender identity and recipient; no private keys or participant
data are part of the review pack.

## Selection and engagement checklist

- [ ] Maintainer selects a route and explicitly authorises the initial contact.
- [ ] Confirm named reviewer, professional capacity, relevant software licence
  experience, jurisdiction and conflicts; check current professional registration
  where applicable. Advertising alone is not appointment or proof of qualification.
- [ ] Agree Q01–Q07 coverage, actual AI/tooling use, distribution forms, baseline
  revision/hashes, exclusions and evidence gaps. Do not commission final-image
  approval before the image is selected.
- [ ] Obtain written fee/quote, VAT, cost cap, clarification allowance, availability
  and change-of-scope terms; maintainer authorises any paid engagement separately.
- [ ] Agree secure evidence transfer, confidentiality, retention and who may see
  the written advice. Keep confidential advice outside the public repository
  unless sharing is expressly agreed; record a permitted outcome/reference instead.
- [ ] Require the dossier's written outcome template: Q01–Q07 answers, form-specific
  conclusions, conditions, missing evidence, obligations/owners and re-review triggers.
- [ ] Record actual contact/engagement dates and pending actions; preparing this
  checklist does not mean any checkbox is satisfied.
- [ ] After qualified written review, record the maintainer's dated release approach
  and resulting task 01 status. Adverse/limited advice is valid evidence, not approval.

## Completion boundary

This preparation package is complete when its shortlist, enquiry and checklist
are reviewable and documentation checks pass. External review is still pending.
The current next step is the bounded maintainer self-review above. External
reviewer selection and engagement are deferred. No budget or purchase is assumed. Task 03 needs two physical hosts and clock
evidence; task 04 needs candidates/instruments. Task 14 still requires 03 and 09;
15 requires 14. No registered dependencies or work stages change.

## Bounded self-review completed — 4 October 2026

The [self-review and updated evidence](distribution-self-review.md) now cover Q01–Q07,
complete upstream ConfigObj/i2plib notices, vendored comparisons and static native
observations. Earlier gap findings are historical; this follow-up narrows notice
retrieval gaps without proving all modification/build provenance. The proposed
release approach awaits maintainer adoption. Task 01 remains open; no qualified
written outcome exists. Paid reviewer engagement is deferred and G01 stays HOLD.

## Current acceptance supersedes external-review requirement — 4 October 2026

The maintainer explicitly changed task 01 to self-review. Earlier mandatory
qualified-review statements and reviewer templates above are retained as historical
preparation, not current prerequisites. The current acceptance is documented
self-review plus a dated maintainer form-specific distribution decision, conditions
and residual-risk record. External advice is optional. See the
[self-review](distribution-self-review.md) and current project-plan task register.
Task 01 remains open pending the maintainer decision; G01 stays HOLD.
