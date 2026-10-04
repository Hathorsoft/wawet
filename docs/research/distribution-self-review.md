# Task 01 — Distribution self-review

Reviewed **4 October 2026**, baseline `ff3df9fffb98a7b7f08512f440b1a72deb908a47`,
with prior local arrangement/direction edits preserved. **Status: bounded
agent-assisted self-review completed; maintainer adoption pending; task 01 open.**
The maintainer requested doing this ourselves rather than hiring. This record is
a technical evidence assessment and proposed conservative release approach,
not a qualified written legal outcome or a claim of licence compatibility.
Gates 01–05 and G01 HOLD remain unchanged. No costs or outreach were incurred.

Read with the [original dossier and Q01–Q07](distribution-review.md),
[licensing policy](../../LICENSING.md) and [new evidence](results/distribution-self-review/evidence.json).
Historical archive findings are retained; the updates below supersede named gaps
only to the extent actually verified. No upstream implementation is imported.

## Exact clauses and assessment

**FACT:** the controlling research evidence is the captured
[RNS 1.5.5 header](results/distribution-review/rns-1.5.5.tar.gz/RNS/__init__.py.notice.txt),
not a mutable current website or the licence metadata label. Clauses are located
by their opening words below so the full text need not be duplicated.

| Source clause / location | Self-review interpretation | Unresolved point / consequence |
| --- | --- | --- |
| Permission paragraph, beginning “Permission is hereby granted” | The listed acts include modification, distribution, sublicensing and sale, subject to conditions. Commercial intent alone is not a prohibition. | No unconditional permission or blanket Apache/MIT compatibility follows. All selected components need their own terms. |
| First condition, beginning “The Software shall not be used”, referring to purposeful harm | Civilian hazard reporting as described has no intentional-harm function. This is a fit assessment of the intended use, not a verified guarantee about all deployments. | Integrations and downstream uses may change the system's functions; do not promise unrestricted use of bundled RNS. |
| Second condition, beginning “The Software shall not be used, directly or indirectly” | Model-training/dataset creation and contributions to model development are expressly restricted. Using a trained tool to assist an independent Wawet project is not automatically the same activity. | This session uses AI and has read licence/source evidence. Provider retention, training, evaluation and account settings have not been established here; do not certify that no restricted use occurs. |
| Third condition, beginning “The above copyright notice” | Preserve the complete RNS copyright and permission notice with copied substantial portions, including evidence; modification does not remove it. | Determine completeness per actual shipped material, including vendored components. Upstream texts retain their own terms. |
| Warranty/liability paragraph | Upstream gives no product assurance. | It cannot establish Wawet safety, regulatory conformity or consumer obligations. |
| Original Wawet licence scope and file-local notices | Apache-2.0 originals remain separate from restricted upstream material; prose and future hardware use their recorded licences. | Evidence files are not relicensed as CC BY prose; contributor provenance is not exhaustively audited by this review. |

**FACT — current author commentary:** the
[Reticulum reference chapter](https://reticulum.network/manual/brandolinis.html)
discusses training-related appropriation separately from human-directed AI
assistance. **INFERENCE:** that supports distinguishing assistance from training,
but is not a separate permission, an account-data audit or a binding interpretation
of every deployment. The pinned header remains authoritative for this assessment.
The commentary's wider copyright claims are not adopted as legal findings here.

**Proposed tooling rule:** do not deliberately train/fine-tune models or build
training datasets from RNS. Before further source-heavy AI work, the maintainer
should establish the actual service/account data-use terms or perform that review
without uploading upstream source. No breach or exemption is inferred from the
unknown account configuration. No upstream training permission has been obtained.

## Vendored and native evidence

**EXPERIMENTAL RESULT:** all seven original archive hashes and fifteen saved
notice hashes matched the existing register. Two exact-version source archives
were obtained from publisher PyPI URLs; their hashes matched publisher metadata.
No downloaded code was installed or executed. Evidence and replay instructions:
[README](results/distribution-self-review/README.md).

- **ConfigObj 5.0.9 / validate 1.0.1:** the ConfigObj release includes a complete
  [BSD notice](results/distribution-self-review/configobj-5.0.9-LICENSE.txt).
  RNS's retained author/header references point to this project. The vendored
  configobj differs by a hardcoded version and final newline. Validate differs
  beyond comments/docstrings, including definitions and test removal; no semantic
  equivalence is claimed. The upstream licence permits modified redistribution
  with source/binary notices and no unauthorised endorsement. Full notice retrieval
  is resolved; complete modification authorship/history is not.
- **i2plib 0.0.14:** its PyPI source archive has no licence-named member. The
  [pinned upstream tag licence](https://raw.githubusercontent.com/l-n-s/i2plib/6edf51cd5d21cc745aa7e23cb98c582144884fa8/LICENSE)
  supplies an attributable [MIT notice](results/distribution-self-review/i2plib-v0.0.14-LICENSE.txt).
  All eight release Python files match that tag; three match RNS byte-for-byte,
  five differ. Observed changes include relative imports, formatting, tunnel
  logging and a session-name prefix. The JSON records each hash; no exhaustive
  behavioural or authorship audit is claimed. Upstream notice retrieval is resolved,
  while provenance of RNS modifications remains incomplete.
- **u-msgpack-python 2.7.1:** its complete MIT header was already captured; no
  additional gap closure is claimed in this follow-up.
- **cryptography 50.0.2:** choose either Apache or BSD for its covered code,
  preserving the chosen obligations; the three top-level licence files do not
  cover every possible native/Rust component by themselves. `otool -L` of the
  exact research wheel has no external OpenSSL entry; static string inspection
  found `OpenSSL 4.0.3 29 Sep 2026`. The
  [current upstream installation documentation](https://cryptography.io/en/latest/installation/)
  describes statically linked macOS wheels. These observations support embedded
  OpenSSL as an inference, not a complete shipped-source/build provenance proof.
  Exact OpenSSL licence/build evidence and complete shipped Rust notices remain
  unresolved. Cargo.lock packages include build/proc-macro dependencies; do not
  treat the lock as the list of shipped code.
- **cffi 2.1.1:** the inspected macOS research wheel links to
  `/usr/lib/libffi.dylib` and libSystem; it is not evidence of a bundled libffi copy
  in that wheel. Load-command version `40.0.0` is not an upstream libffi release
  number. The source's bundled libffi and file-local exceptions still require
  review if shipped. Exact OS build/system-library obligations remain separate.
- **pyserial 3.5 / pycparser 3.0:** the existing complete BSD notices establish
  notice evidence for those archives; no additional binary provenance is claimed.
  Interpreter, OS, actual target image and firmware remain outside this inventory.

## Findings for Q01–Q07

| Question | Evidence-backed finding / proposed handling | Remaining uncertainty |
| --- | --- | --- |
| Q01 rights and distribution forms | RNS lists sale/modification/distribution rights subject to its three conditions; civilian intent fits the described non-harm purpose. Keep original Wawet work independently licensed and advertise upstream restrictions accurately. | Final systems, downstream uses and legal compatibility are not certified. |
| Q02 harm / AI restrictions | Apply the exact conditions; no intentional-harm functions or deliberate RNS model training are proposed. Author commentary supports the assistance/training distinction. | Actual service data use and breadth of indirect contribution remain unresolved. Permission/clarification has not been sought. |
| Q03 notices and downstream terms | Retain full RNS notice plus separate vendored BSD/MIT notices; label third-party evidence correctly. For future redistribution, build a per-component notice pack rather than apply Apache to everything. | Changes, provenance and exact shipped contents need verification; no final notice pack exists. |
| Q04 native/transitive/build scope | Source and inspected wheels are separate inventories. Record the newly observed macOS linkage and string evidence; retain Cargo.lock as source-build evidence only. | OpenSSL/Rust shipped notices/build provenance, actual installed artefacts, OS/interpreter and final target remain open. |
| Q05 RNode firmware | Unselected. If shipped/modified, freeze firmware revision/build and review its exact GPLv3 terms, corresponding source/build instructions and delivery arrangements. | No firmware or distribution method selected; no GPL compliance finding made. |
| Q06 LXMF | Unselected and not installed; no exact-version permission inferred. Review separately if selected. | Its inclusion and impact are outside the current assessment. |
| Q07 release approach | Propose continuing independent Wawet source/simulator work; retain optional experiments as separately labelled research; HOLD commercial bundles and restricted-source redistribution pending unresolved evidence/decisions. | Maintainer adoption and residual-risk decision are not yet recorded; external review is optional under the updated task criterion. |

## Proposed form-specific decision and next action

These are recommendations resulting from the authorised self-review, not a claim
that the maintainer has already adopted every recommendation or approved a release.

| Form | Proposed decision now | Conditions / revisit trigger |
| --- | --- | --- |
| Independent original Wawet source/simulator | Continue local development under existing licence scope; no release action in this package. | Preserve provenance and upstream evidence notices; no RNS dependency required by default. Revisit imported code or changed packaging. |
| User-installed RNS experiments | Retain the current optional research path; do not advertise unrestricted or legally cleared use. | Installation does not bypass terms. Review tooling/data-use uncertainty and research artefact obligations before changing distribution; no new distribution approval asserted. |
| Redistributed upstream sources/wheels or bundled commercial image | HOLD approval in this review. | Complete component/notices/build inventory, actual use assessment and explicit release decision; future image requires platform/OS/interpreter/firmware evidence. |

The useful next maintainer action is reading this assessment and the recovered
notices, deciding whether to adopt the conservative approach, and checking actual
AI service data-use arrangements. If an interpretation remains unacceptable,
consider an authorised narrow upstream clarification or revise dependency choice;
no contact, expenditure or second routing implementation is assumed. Paid review
is deferred. Technical measurement packages may progress when resources exist.

This completes the bounded self-review evidence package, **not task 01**. The maintainer subsequently changed its assurance requirement to documented
self-review and a dated distribution/risk decision; see the current task 01
criteria and licensing ADR. The maintainer decision remains to be recorded;
external professional review is optional. Physical-host
03, host 04, regional/profile 02/05 and radio 08 blockers remain; 14 still requires
03/09, and 15 requires 14. No radio, road trial, release, commit or push occurred.

## Assurance requirement updated — 4 October 2026

The maintainer explicitly requested updating task 01 to reflect doing the review
ourselves. A dated maintainer distribution decision with conditions and residual
risks now completes the assurance requirement; qualified external review is no
longer mandatory. The evidence findings and unresolved questions above are
unchanged. This is not a legal approval or automatic acceptance of the proposed
release approach. Task 01 remains open pending that decision, and G01 stays HOLD.
