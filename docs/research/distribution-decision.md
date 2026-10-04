# Task 01 — Adopted maintainer distribution decision

**DESIGN DECISION — 4 October 2026. Status: adopted; task 01 complete for the bounded reviewed scope.**

The maintainer adopted the conservative approach in this conversation, confirmed
that the project is not deliberately training AI, and explicitly requested
implementation of the decision and its conditions. Reviewed baseline: `52085f7`;
the starting working tree was clean. This records a maintainer risk decision,
not professional legal approval, blanket licence compatibility or a release action.

## Reviewed scope and evidence

The [dossier](distribution-review.md), [Q01–Q07 self-review](distribution-self-review.md),
[seven-artefact register](results/distribution-review/artefact-register.json) and
[self-review evidence](results/distribution-self-review/evidence.json) define the
exact scope and hashes. It covers RNS 1.5.5, cryptography 50.0.2, pyserial 3.5,
cffi 2.1.1 and pycparser 3.0 source/research-wheel evidence, plus recovered
ConfigObj 5.0.9 and pinned i2plib 0.0.14 notices. These are research artefacts,
not an inventory of a final installed product. Original licence scopes remain
as recorded in [LICENSING](../../LICENSING.md).

Intended use is civilian communications and nearby hazard reporting. LXMF,
RNode firmware, the final platform/image, interpreter/OS and product build are
unselected or outside this approval. Evidence copies retain upstream terms.

## Form-specific decisions

| Form | Adopted decision | Conditions |
| --- | --- | --- |
| Original Wawet source/simulator | Continue development under existing licence scope. | Preserve contributor provenance and third-party evidence notices. Default execution remains independent of RNS. No publication is performed by this decision. |
| User-installed RNS experiments | Retain the separately labelled optional research path. | Upstream restrictions apply to installation and use. Do not claim unrestricted use, compatibility or legal clearance. Preserve exact-version references and notices; apply the tooling condition below. |
| Redistributed upstream sources/wheels or bundled commercial images | Approval withheld (HOLD). | Review actual shipped contents, uses, component notices, provenance and builds before a separate explicit approval. Include OS/interpreter/platform and firmware obligations where shipped. |

## Q01–Q07 and residual risks

The maintainer accepts the documented uncertainties only for the limited continuing
work above; they do not authorise held distribution forms or waive upstream terms.

| Question | Adopted handling / unresolved risk |
| --- | --- |
| Q01 rights and forms | Apply the form decisions above and exact upstream conditions; no blanket downstream-use or compatibility conclusion. |
| Q02 harm / AI restrictions | No intentional-harm function or deliberate Reticulum AI training/training-dataset creation is proposed. The maintainer confirms no deliberate AI training. Provider handling of earlier inputs remains unverified; no breach or exemption is asserted. Further upstream source review uses local/manual inspection until applicable service/account data-use arrangements are established. |
| Q03 notices / terms | Preserve full RNS and separate vendored notices. Recovered notices narrow retrieval gaps; modification authorship/provenance and final notice-pack completeness remain unresolved. |
| Q04 native / build scope | OpenSSL/Rust shipped notices, native build provenance and actual installed/target contents remain unresolved. Static research-wheel observations do not constitute a complete product inventory. |
| Q05 firmware | RNode firmware remains unselected and unapproved. Freeze any selected build and review GPLv3 notices, corresponding source and build/delivery arrangements before distribution. |
| Q06 LXMF | Unselected and unapproved; requires its own exact-version review if selected. |
| Q07 release approach | Adopt the bounded decisions and residual risks in this record. Task 01 completion is not commercial-bundle or product-release approval. |

The maintainer owns follow-up evidence, tooling checks and release decisions.
Re-review changed dependency versions, platforms/builds, packaging, intended uses
or newly selected components. External advice is optional if the maintainer
chooses it; mandatory external review is superseded for task 01 only.

## Completion and remaining gates

The committed evidence assessment plus this adopted dated decision satisfy the
current task 01 acceptance criteria for the bounded scope. Historical pending
adoption and mandatory-review entries are superseded by this record, not rewritten.

**G01 remains HOLD.** Tasks 02–05 remain open, and radio task 08 is outstanding.
Task 03 still needs two physical hosts and clock evidence; task 04 needs candidate
hardware/instruments. Task 14 still requires 03 and 09; task 15 requires 14.
No task becomes newly eligible solely through task 01 completion. No runtime,
protocol, dependency or public API change, purchase, outreach, RF/road test,
release, commit, push or PR is part of this package.
