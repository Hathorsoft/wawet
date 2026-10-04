# Task 01 — Exact-version distribution review dossier

Prepared **4 October 2026** against clean Wawet HEAD `2f21ac5`.
**Status: dossier prepared; qualified review pending.** Task 01 remains open;
gates 01–05 and G01 HOLD are unchanged. This is evidence for review, not legal
advice, licence compatibility approval or a final product SBOM.

## Intended use and review boundary

Wawet is Hathorsoft Ltd's early-stage civilian communications project. Its first
application is nearby road-hazard reports from a tactile vehicle appliance.
Basic operation must not require a phone, account, cloud or subscription.
Official commercial hardware is intended; third-party implementations and
commercial derivatives of original Wawet work are permitted under its selected
licences. No product image, firmware or hardware release is selected here.

The independent standard-library simulator is separate from the optional RNS
experiments. Those experiments currently pin RNS 1.5.5, cryptography 50.0.2,
pyserial 3.5, cffi 2.1.1 and pycparser 3.0. They are research, not a production
adapter or public trust system. See [original licence scope](../../LICENSING.md),
[pins](../../tools/rns-requirements.txt), [architecture](../architecture/system.md)
and [agreed standalone boundary](feasibility-thresholds.md).

| Review form | Concrete scope | Proposed treatment awaiting review |
| --- | --- | --- |
| Original source | Wawet source/specifications Apache-2.0; prose CC BY 4.0; no vendored upstream implementation | Confirm notices, provenance and separation from optional dependencies. |
| User-installed experiment | User separately obtains pinned packages; Wawet supplies tools and installation instructions | Assess restrictions and downstream obligations for this actual installation/use flow. Installation is not assumed to remove obligations. |
| Bundled commercial image | Hypothetical future image containing Wawet, interpreter/OS, RNS and native dependencies | HOLD distribution. Final platform, image and dependency/build inventory must be selected and reviewed before approval. |

LXMF is **unselected and not installed**. No version or distribution permission is
inferred from its mutable upstream licence. If selected, add exact artefacts and
review them before inclusion. RNode firmware is **unselected and outside these
Python artefacts**: shipping it needs a separate exact firmware/build/source and
GPLv3 obligations assessment. Python/interpreter, OS and image components likewise
need exact evidence for a future bundle. This dossier selects none of them.

## Evidence register and acquisition

The [artefact register](results/distribution-review/artefact-register.json) records
seven artefacts: five source archives and two macOS arm64 research wheels.
Each record includes primary release metadata/download URLs, retrieval date,
filename, size, SHA-256, platform scope, conditional Requires-Dist entries,
notice member paths/hashes and named gaps. These wheels do not select a Drive
platform or establish the exact bytes installed in the historical experiment.
The earlier [installed inventory](results/dependency-inventory.json) remains a
separate historical record, not an archive inventory or product SBOM.

Archives were downloaded from publisher PyPI release URLs into temporary storage
`/tmp/wawet-review-artefacts`, not installed or executed. Every archive hash matched
its publisher release metadata. Complete licence files and leading source-header
notices are preserved as evidence under their original terms, not relicensed as
Wawet prose. No upstream executable source is added to the application.
Archive binaries are not committed; retrieve them from register URLs and verify
SHA-256 before review. The metadata snapshots retain release fields and archive
listings; mutable upstream metadata is not a replacement for the hashed bytes.

| Package | Primary exact-version source | Captured evidence / findings |
| --- | --- | --- |
| rns 1.5.5 | [PyPI release](https://pypi.org/project/rns/1.5.5/) / [captured metadata](results/distribution-review/rns-pypi.json) | Full Reticulum licence header; vendored headers and missing-text gaps below. |
| cryptography 50.0.2 | [PyPI release](https://pypi.org/project/cryptography/50.0.2/) / [captured metadata](results/distribution-review/cryptography-pypi.json) | Apache/BSD licence texts in source and wheel; Rust source lock enumerated, native notice/provenance gaps remain. |
| pyserial 3.5 | [PyPI release](https://pypi.org/project/pyserial/3.5/) / [captured metadata](results/distribution-review/pyserial-pypi.json) | Complete archive LICENSE.txt; historical empty notice entry is not absence of a licence. |
| cffi 2.1.1 | [PyPI release](https://pypi.org/project/cffi/2.1.1/) / [captured metadata](results/distribution-review/cffi-pypi.json) | Source top-level and bundled libffi licence; wheel licence; native linkage gap remains. |
| pycparser 3.0 | [PyPI release](https://pypi.org/project/pycparser/3.0/) / [captured metadata](results/distribution-review/pycparser-pypi.json) | Complete source licence; dependency markers retained. |

### Captured licence and notice files

- **rns-1.5.5.tar.gz**: [__init__.py.notice.txt](results/distribution-review/rns-1.5.5.tar.gz/RNS/__init__.py.notice.txt); [configobj.py.notice.txt](results/distribution-review/rns-1.5.5.tar.gz/RNS/vendor/configobj.py.notice.txt); [validate.py.notice.txt](results/distribution-review/rns-1.5.5.tar.gz/RNS/vendor/validate.py.notice.txt); [umsgpack.py.notice.txt](results/distribution-review/rns-1.5.5.tar.gz/RNS/vendor/umsgpack.py.notice.txt).
- **cryptography-50.0.2.tar.gz**: [LICENSE](results/distribution-review/cryptography-50.0.2.tar.gz/cryptography-50.0.2/LICENSE); [LICENSE.APACHE](results/distribution-review/cryptography-50.0.2.tar.gz/cryptography-50.0.2/LICENSE.APACHE); [LICENSE.BSD](results/distribution-review/cryptography-50.0.2.tar.gz/cryptography-50.0.2/LICENSE.BSD).
- **cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl**: [LICENSE](results/distribution-review/cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl/cryptography-50.0.2.dist-info/licenses/LICENSE); [LICENSE.APACHE](results/distribution-review/cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl/cryptography-50.0.2.dist-info/licenses/LICENSE.APACHE); [LICENSE.BSD](results/distribution-review/cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl/cryptography-50.0.2.dist-info/licenses/LICENSE.BSD).
- **pyserial-3.5.tar.gz**: [LICENSE.txt](results/distribution-review/pyserial-3.5.tar.gz/pyserial-3.5/LICENSE.txt).
- **cffi-2.1.1.tar.gz**: [AUTHORS](results/distribution-review/cffi-2.1.1.tar.gz/cffi-2.1.1/AUTHORS); [LICENSE](results/distribution-review/cffi-2.1.1.tar.gz/cffi-2.1.1/LICENSE).
- **cffi-2.1.1-cp311-cp311-macosx_11_0_arm64.whl**: [LICENSE](results/distribution-review/cffi-2.1.1-cp311-cp311-macosx_11_0_arm64.whl/cffi-2.1.1.dist-info/licenses/LICENSE).
- **pycparser-3.0.tar.gz**: [LICENSE](results/distribution-review/pycparser-3.0.tar.gz/pycparser-3.0/LICENSE).

### Material findings and named evidence gaps

**FACT — exact artefact text:** RNS's complete Reticulum licence is in the leading
comment of `RNS/__init__.py`; no standalone licence-named file was found in the
source archive. It includes use restrictions and notice conditions. The captured
header is the evidence; professional interpretation is requested below.

**FACT — vendored components:** RNS includes ConfigObj 5.0.9, validate 1.0.1,
u-msgpack-python 2.7.1 and i2plib declaring 0.0.14. The u-msgpack header contains
its complete MIT notice. ConfigObj/validate headers point to BSD-3-Clause;
i2plib metadata declares MIT. Complete attributable licence texts for those latter
components were not found by archive filename inspection. Their source member
hashes/header evidence are recorded where inspected. **GAP:** obtain and match
complete notices and establish any local modifications; do not treat the RNS
licence as covering all vendored components.

**FACT — native dependencies:** cryptography's source Cargo.lock identifies Rust
packages; source manifests refer to OpenSSL bindings. Its inspected wheel contains
three top-level licence files. cffi's source archive includes a bundled libffi
licence, whereas its inspected wheel contains a top-level licence file.
**GAP:** final-wheel OpenSSL/libffi linkage, versions, build provenance and complete
Rust/native notices have not been established. A Cargo.lock list is not a binary
SBOM, licence inventory or proof all locked packages ship. For the Python 3.11+ CPython research path, declared runtime edges are
RNS → cryptography/pyserial, cryptography → cffi, and cffi → pycparser.
The Python <3.11 typing-extensions marker does not apply to that path; optional
SSH bcrypt is not selected. Development/test extras
in Requires-Dist are not automatically runtime dependencies. A final image also
needs interpreter/OS/component review, including build-time versus shipped scope.

## Questions requiring qualified interpretation

| ID | Reviewer question | Evidence / required follow-up |
| --- | --- | --- |
| Q01 | What rights and conditions apply to civilian hazard reporting, hardware resale, modifications and third-party commercial forks in each distribution form? | Intended use and three forms above; RNS complete header and original Wawet scope. |
| Q02 | How do the restricted-use and model-training provisions apply to this project, its tooling, users and downstream recipients? Is clarification or separate permission needed? | Exact RNS header; describe actual development/use/distribution to reviewer. Do not infer an interpretation from the grant language alone. |
| Q03 | What notices and downstream terms must accompany source, optional installation and a bundle, and how should distinct licence scopes be presented? | Captured licence texts, original licensing policy and vendored-component gaps. |
| Q04 | Which native/transitive/build components require additional notices or other obligations, and what evidence is necessary to review the final binary? | Seven artefact records, Requires-Dist and Cargo.lock package list; unresolved OpenSSL/libffi/Rust provenance and final target. |
| Q05 | If RNode firmware is shipped or modified, what exact corresponding source, build instructions, notices and delivery arrangements are required? | Separate future firmware/build evidence needed; no firmware selected or approved here. |
| Q06 | If LXMF is selected later, what exact-version review is required and does its inclusion change any permitted form? | Currently outside scope; obtain frozen release/licence evidence before review. |
| Q07 | Which forms, if any, can be approved now, subject to which conditions; which must await final image/firmware selection? | Record a form-specific written outcome using the template below; no blanket product approval. |

**OPEN QUESTION:** no qualified reviewer has evaluated these questions. Preparing
or checking this dossier grants no distribution permission and completes no gate.

## Written review outcome template

- Reviewer identity, professional capacity and organisation: **pending**.
- Review date and written outcome reference: **pending**.
- Wawet revision, intended use and artefact hashes reviewed: **pending**.
- Scope/exclusions, including LXMF, firmware, interpreter/OS and final platform: **pending**.
- Q01–Q07 answers and evidence references: **pending**.
- Original-source form: permitted / conditional / not approved / unresolved; rationale: **pending**.
- Optional-installation form: permitted / conditional / not approved / unresolved; rationale: **pending**.
- Bundled-image form: permitted / conditional / not approved / unresolved; rationale: **pending**.
- Required notices/source/access arrangements and responsible owner: **pending**.
- Unresolved evidence, conditions, expiry/re-review triggers and follow-up: **pending**.
- Maintainer's dated release approach decision referencing the written review: **pending**.

Record adverse and limited outcomes as well as approvals. Re-review changed
versions, platform/builds, intended uses or distribution forms. Task 01's acceptance
requires a qualified written outcome and documented reviewed approach for the
selected scope; dossier preparation alone leaves it open. G01 additionally requires
its other registered predecessors. The next action is reviewer selection and
arranging review; no outreach, spending or release is authorised by this record.
