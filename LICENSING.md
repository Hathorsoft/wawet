# Licensing and dependency policy

**Current status — 4 October 2026:** task 01 is complete for the bounded reviewed scope; see the [adopted maintainer decision](docs/research/distribution-decision.md). Original Wawet work and optional user-installed RNS research continue with conditions; upstream redistribution and commercial bundles remain unapproved. G01 remains HOLD; tasks 02–05 remain open. Earlier pending-adoption, mandatory-review and uncommitted-status entries below are historical. The maintainer subsequently authorised committing and pushing this decision package.

## Selected scope

Copyright 2026 Hathorsoft Ltd and contributors, for original foundation work.
Earlier contributor rights and upstream ownership are not transferred by this
statement. The historical concept notes remain part of project documentation.

| Material | Licence | Scope |
| --- | --- | --- |
| Original software, scripts, tests, configurations and templates | Apache-2.0 | Allows commercial use; includes patent terms and notice obligations |
| `protocol/` specifications and vectors | Apache-2.0 | Broad implementation and redistribution; experimental status is not a licence restriction |
| Documentation prose (`docs/`, device docs, README and root policy prose) | CC BY 4.0 | Attribution required; commercial reuse allowed |
| Future original hardware design source | CERN-OHL-S v2 | Strong reciprocity; apply when actual design source is added, not to third-party components |
| Licence texts | Their own verbatim terms | Not relicensed as project documentation |

Full texts: [Apache-2.0](LICENSES/Apache-2.0.txt),
[CC BY 4.0](LICENSES/CC-BY-4.0.txt),
[CERN-OHL-S v2](LICENSES/CERN-OHL-S-2.0.txt). Root [LICENSE](LICENSE) covers
software; this scope document governs exceptions. Code blocks in documentation
showing original executable examples are also available under Apache-2.0.
File-local third-party notices, if later introduced, take precedence for that
material. No hardware CAD or firmware has been imported or released.

These licences permit commercial derivatives. They do not reserve all sales to
Hathorsoft. Trademarks/endorsement are separate; see [brand policy](docs/business/trademark-policy.md).

## Actual upstream research — checked 4 October 2026

| Dependency / candidate | Checked licence | Consequence |
| --- | --- | --- |
| Python standard library | PSF terms | Required interpreter dependency; no runtime PyPI packages for simulator |
| RNS 1.5.5 / current Reticulum source | **Reticulum License**, not plain MIT | Grants sale/copy rights subject to harmful-use and ML/training restrictions; optional experiment dependency |
| Current LXMF source | Reticulum License | Same use restrictions; not installed or required here |
| RNode upstream firmware | GPLv3 | Covered firmware distribution/derivatives require compliance; does not inherit Apache terms |
| Ruff 0.13.3 | MIT installed licence text | Development only |
| mypy 1.18.2 | MIT metadata | Development only |
| cryptography 50.0.2 | Apache-2.0 OR BSD-3-Clause metadata | Optional spike; includes native/transitive obligations |
| pyserial 3.5 | BSD metadata | Optional spike |
| cffi 2.1.1 / pycparser 3.0 | MIT-0 / BSD-3-Clause metadata | Optional spike transitive dependencies; verify exact wheel notices before distribution |

Primary upstream licence sources:
[Reticulum](https://github.com/markqvist/Reticulum/blob/master/LICENSE),
[LXMF](https://github.com/markqvist/LXMF/blob/master/LICENSE),
[RNode](https://github.com/markqvist/RNode_Firmware/blob/master/LICENSE).
The installed RNS source header and distribution metadata were also inspected.
The optional [requirements](tools/rns-requirements.txt) freeze this experiment's
versions, not future product dependencies. No upstream source is vendored here.

**Material finding:** current Reticulum/LXMF usage restrictions differ from
unrestricted OSI-style open-source terms. Do not label them MIT or assume the
whole future bundled stack is Apache-licensed. Wawet's independent foundation
is open source; packaging restricted dependencies introduces a separate scope.
Resolve exact-version rights and interpretation before bundling or distributing
a commercial image. Ordinary commercial permissions do not remove restrictions.
No legal approval or licence-compatibility conclusion is asserted.

## Alternatives evaluated

Apache-2.0 encourages integrations and offers explicit patent terms. GPLv3
requires source reciprocity for covered software derivatives but still permits
sales. LGPL permits some linking scenarios with conditions. MPL-2.0 uses file-
level reciprocity. None can provide exclusive commercial sales while remaining
a conventional open-source licence. Apache is selected for original application
code; it does not erase dependency obligations.

CERN-OHL-P/W/S provide increasing reciprocity; S is selected for future original
hardware to encourage shared design improvements. Confirm component/library
scope and source-compliance obligations before publishing actual CAD. CC BY 4.0
makes prose reusable with attribution; protocol specifications use the permissive
software terms to keep compatible implementation straightforward.

## Contributions and release gate

Contributors retain copyright and submit under the applicable outbound licence;
no copyright assignment or exclusive-sales agreement is required. Contributors
must have the right to submit work and identify third-party material. Do not
copy publicly visible code without reviewing its licence. Keep a dependency/
notice inventory, exact versions and required corresponding source with product
release artefacts. Record maintainer review of RNS restrictions, RNode distribution and hardware
reciprocity before a manufacturing release; seek external expertise if the
maintainer decides an unresolved risk requires it. No legal approval is implied.

## Feasibility review inventory

The [installed optional-experiment inventory](docs/research/results/dependency-inventory.json)
records exact versions and notice hashes for the follow-up experiment. The
[distribution review brief](docs/research/feasibility-gates.md) distinguishes source,
optional installation and bundled images. LXMF is not selected or installed;
qualified review and product distribution approval remain unresolved.

## Task 01 self-review follow-up — 4 October 2026

The [bounded self-review](docs/research/distribution-self-review.md) distinguishes
exact licence clauses from interpretation and unresolved questions. Complete
ConfigObj BSD and pinned i2plib MIT notices were recovered and compared to RNS's
vendored files. The exact research cffi wheel links to system libffi; cryptography
static observations do not establish complete OpenSSL/Rust shipped notices or build
provenance. Historical findings above remain separate from these new observations.
The proposed conservative distribution approach awaits maintainer adoption;
original scopes are unchanged. No blanket compatibility, AI data-use exemption,
qualified review or bundled-image approval is claimed. Paid review is deferred;
task 01 and G01 HOLD remain unresolved under the existing acceptance criteria.

## Task 01 assurance decision — 4 October 2026

**DESIGN DECISION:** the maintainer explicitly chose to perform task 01 ourselves
and instructed updating the task accordingly. A documented maintainer self-review
and dated form-specific release/risk decision replace the previous mandatory
qualified external review for task 01. External advice is optional, not a required
paid prerequisite. Earlier qualified-review entries are historical and superseded
by this decision; no professional legal approval is asserted.

The [self-review](docs/research/distribution-self-review.md) supplies the evidence assessment. Task 01 remains
open until the maintainer records adopted distribution decisions, conditions and
residual risks, including unresolved AI data-use and provenance questions. This
instruction changes the assurance method; it does not itself approve a bundle or
adopt every recommendation. G01 stays HOLD and other task prerequisites and
technical/regulatory gates remain unchanged. Restricted upstream terms and notice
obligations are not waived. Re-review changed uses, releases and shipped builds.
