# Foundation validation record

Date: 4 October 2026. Local environment: macOS, Python 3.11.4.

## Commands

```sh
./scripts/demo
./scripts/test
PYTHON=.venv/bin/python ./scripts/check
PYTHON=.venv/bin/python ./scripts/rns-spike
```

The first two commands require no installation. Contributor checks require
`python -m pip install -e '.[dev]'`. The optional spike has its own requirements
and may need loopback-socket permission in a restricted environment.

## Results

- **31 unit tests passed**, including 500 deterministic malformed-frame samples,
  canonical vectors, expiry, ID conflicts, geography, outages and retention/rate limits.
- Ruff 0.13.3 lint and format checks passed for 11 Python files.
- mypy 1.18.2 strict checks passed for all seven application modules.
- Repository-relative Markdown file links and `git diff --check` passed.
- Development/optional experiment environment: `pip check` passed.
- Built `wawet-0.1.0-py3-none-any.whl` using the declared setuptools backend.
  Installed it offline with `--no-index --no-deps` in a fresh virtual environment;
  all 31 tests and `wawet-demo` passed against the installed package. Confirmed
  `RNS` is absent from that environment.
- Actual RNS 1.5.5 two-process loopback delivery passed with exact 38-byte payload
  equality; details and limitations in [the spike record](research/reticulum-spike.md).
- Hardware decision CSV verified: 20 complete rows and valid disposition values.

GitHub Actions are
configured for Python 3.11, 3.12 and 3.13 on Ubuntu; no hosted CI run is claimed
until the changes are pushed. External URLs and Markdown anchors are not checked
by the local file-link checker. No radio or physical vehicle test was performed.

## Scope deliberately deferred

No firmware, mobile frontend, production transport adapter, signatures, trust
scores, network confirmation/dispute/supersession, automatic store-and-forward,
custom CAD/PCB/enclosure, certification, hardware selection, transmitted radio
experiment or hosted service. No remote issues, labels, PR or push were created.

The original concept notes and existing nine milestone commits are preserved.
This foundation is current local work, not backdated implementation.

## Final repository tree

Source files only; environments, build artefacts and Git internals omitted.

```text
wawet/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.md
│   │   ├── feature.md
│   │   ├── hardware-research.md
│   │   └── regulatory-research.md
│   ├── workflows/
│   │   └── checks.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── LICENSES/
│   ├── Apache-2.0.txt
│   ├── CC-BY-4.0.txt
│   └── CERN-OHL-S-2.0.txt
├── devices/
│   ├── drive/
│   │   └── docs/
│   │       ├── ble-gatt.md
│   │       ├── feature-matrix.csv
│   │       ├── feature-matrix.md
│   │       ├── hardware-concepts.md
│   │       ├── human-factors.md
│   │       ├── open-questions.md
│   │       └── product-requirements.md
│   ├── gateway/
│   │   └── README.md
│   ├── pocket/
│   │   └── README.md
│   └── relay/
│       └── README.md
├── docs/
│   ├── architecture/
│   │   ├── adr/
│   │   │   ├── 0001-monorepo.md
│   │   │   ├── 0002-reticulum.md
│   │   │   ├── 0003-transport-boundary.md
│   │   │   ├── 0004-encoding.md
│   │   │   ├── 0005-python.md
│   │   │   ├── 0006-licensing.md
│   │   │   ├── 0007-phone-device.md
│   │   │   ├── 0008-working-name.md
│   │   │   ├── README.md
│   │   │   └── template.md
│   │   ├── adversarial-review.md
│   │   └── system.md
│   ├── business/
│   │   ├── open-source-commercial-model.md
│   │   └── trademark-policy.md
│   ├── community/
│   │   ├── backlog.md
│   │   └── labels.md
│   ├── research/
│   │   ├── README.md
│   │   ├── amateur-radio.md
│   │   ├── halow.md
│   │   ├── lora-rnode.md
│   │   ├── phone-speech.md
│   │   ├── prior-art.md
│   │   ├── reticulum-spike.md
│   │   ├── reticulum.md
│   │   └── uk-regulatory.md
│   ├── security/
│   │   ├── privacy.md
│   │   └── threat-model.md
│   ├── concept.md
│   ├── agent-handoff.md
│   ├── roadmap.md
│   ├── validation.md
│   └── vision.md
├── packages/
│   └── wawet/
│       ├── __init__.py
│       ├── demo.py
│       ├── geo.py
│       ├── protocol.py
│       ├── simulation.py
│       ├── transport.py
│       └── vehicle.py
├── protocol/
│   ├── vectors/
│   │   └── v1.json
│   └── road-event-v1.md
├── scripts/
│   ├── check
│   ├── demo
│   ├── rns-spike
│   └── test
├── tests/
│   ├── test_application.py
│   └── test_protocol.py
├── tools/
│   ├── check_links.py
│   ├── rns-requirements.txt
│   └── rns_spike.py
├── .gitignore
├── AGENTS.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── LICENSING.md
├── NOTICE
├── README.md
├── SECURITY.md
├── SUPPORT.md
└── pyproject.toml
```

## Feasibility follow-up — 4 October 2026

Baseline demo and 31 tests passed before changes. Final command
`PYTHON=.venv/bin/python ./scripts/check` passed 32 tests, local Markdown links,
Ruff lint/format and strict mypy; `git diff --check` passed. Python 3.12/3.13
hosted CI remains unverified.

Optional RNS 1.5.5 runs of `tools/rns_authenticated_spike.py` (default, `--churn`
and `--absent-discovery`) passed their scenario assertions on loopback. See the
[review pack and raw observations](research/feasibility-gates.md). Worker-bundle
preparation was exercised with a private example address without starting sockets.
No physical-host, radio, current-consumption or qualified-review result is claimed.
Changes remain local and uncommitted; no push occurred.

## Authenticated contact campaign — 4 October 2026

This continuation preserves the earlier foundation and feasibility validation.
The [campaign report](research/contact-campaign-results.md) links raw evidence,
exact executed source/hashes, analyser output and remaining limits.

- Baseline before edits: `./scripts/demo`, `./scripts/test` and
  `PYTHON=.venv/bin/python ./scripts/check` passed with 32 tests.
- After changes: `./scripts/demo` passed; `./scripts/test` and
  `PYTHON=.venv/bin/python ./scripts/check` passed with 45 tests, local Markdown
  links, Ruff lint/format and strict mypy. The additional deadline test ran in
  the final complete check. Default tests import no optional RNS dependency.
- `PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign
  --output /tmp/wawet-contact-full --repetitions 30 --jobs 8` completed 490/490
  trials with zero worker failures. Full source was archived before defensive
  analysis/failure/deadline follow-ups.
- Final-source smoke: the same campaign command with
  `--output /tmp/wawet-contact-release-smoke --repetitions 1 --jobs 8` completed
  26/26 trials with zero failures. Offline assertions passed stable delivery,
  fresh resend, expiry withholding, adversarial counts, bounded overflow and recovery.
- `tools/rns_authenticated_spike.py`, `--churn` and `--absent-discovery` were
  rerun in the optional environment; delivery/churn and expected timeout passed.
- The offline analyser reproduced the full-run summary. Cross-host latency was
  omitted because measured clock-offset evidence was unavailable.

Initial sandbox socket denial was resolved through approved loopback execution;
no public network or radio was used. Runtime: macOS 26.2 arm64, Python 3.11.4,
RNS 1.5.5. No two-physical-host or hosted Python 3.12/3.13 CI runs occurred. Existing
local work was preserved; changes remain uncommitted and nothing was pushed.

## A01 review and revalidation — 4 October 2026

This new review started at `29bccc6`; the foundation and follow-up sections above
remain historical records. All eight modified tracked files and all untracked
research, tools, tests, result files and project-plan documentation were reviewed.
No application/protocol changes or executable corrections were required.

[Review evidence](research/results/a01-review.json) records versions, source hashes,
checks and limitations. The [new raw archive](research/results/a01-recheck-2026-10-04.tar.gz)
contains the sequential campaign manifest, worker JSONL/stderr/exits, summary,
executed harness/hash, signed-spike outputs and offline smoke assertion script.
After extracting it, run `python3 a01-recheck/verify-smoke.py a01-recheck/contact-smoke`.

Commands and new results:

```sh
./scripts/demo
PYTHON=.venv/bin/python ./scripts/check
.venv/bin/python -m pip check
git diff --check
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --churn
PYTHONPATH=packages .venv/bin/python tools/rns_authenticated_spike.py --absent-discovery
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py campaign --output /tmp/wawet-a01-review/contact-smoke --repetitions 1 --jobs 1
PYTHONPATH=packages .venv/bin/python tools/rns_contact_campaign.py analyse /tmp/wawet-a01-review/contact-smoke
```

- Demo, 45 tests, local Markdown file links, lint/format, strict types and dependency
  consistency passed. The initial check used the old virtualenv tools; after
  installing declared Ruff 0.16.9 and mypy 2.3.1, the complete check and `pip check`
  passed again. No declared dependency changed.
- Signed delivery/churn passed exact 38-byte equality, two signature rejects and
  one expired receive reject; churn withheld one expired pending frame. Absent
  discovery passed its expected bounded timeout.
- **26/26 sequential smoke trials** completed with zero worker failures. Offline
  assertions passed stable and cold/warm delivery, unchanged fresh resend, stale
  withholding, absent timeout, adversarial counts, 24 capacity drops and recovery.
  Offline reanalysis exactly matched the new summary; latency remains omitted.
- Both historical archive SHA-256 values and executed-source hashes matched their
  records. All 490 full-run and 26 historical smoke worker exits were zero; offline
  summaries exactly reproduced, including the published full final-analysis JSON.
  Current source matches the historical final-source smoke, so a new full campaign
  was unnecessary. Historical full-run source remains separately archived.
- Archive member/content review found no private keys/configurations or participant
  data. Event locations derive from fixed synthetic inputs. Optional dependency
  versions and notice hashes matched the installed inventory.

Sandbox loopback bind and PyPI access initially failed; approved loopback execution
and installation of already-declared dev versions completed successfully. Git writes
also required sandbox escalation. These are environment permissions, not experiment
failures. Results remain single-host controlled IP, not physical-host or radio
measurements. External URLs/anchors, hosted Python 3.12/3.13, current qualified
licensing/regulatory review and gates 01–05 remain unverified/open; HOLD persists.

Local commit outcome: `ae4ba6e` records the signed spike/initial evidence;
`e42ae0e` records campaign/feasibility work and A01 revalidation. The following
project-plan documentation commit records A01 complete and A02 next. Earlier
"uncommitted" statements describe their historical snapshots. No push occurred.

## A02 documentation draft — 4 October 2026

Added the proposed feasibility thresholds/host boundary and linked downstream
briefs. Reviewed T01–T09 against Drive D02/D03/D08/D11, campaign denominators,
clock evidence and task-register dependencies. The hypothetical worked cases
cover acceptable delivery, short-contact failure, missing clocks, startup without
a fix and excess host memory/power/cost; they are review examples, not test runs.

`python3 tools/check_links.py` passed. `git diff --check` passed. Final diff review
preserved historical records and left A02 open pending maintainer agreement;
gates 01–05 and investment HOLD remain unchanged. No runtime checks or experiments
were rerun for documentation-only edits. External URLs/anchors remain unchecked.
Changes are local and uncommitted; nothing was pushed or published.

## A02 agreement reconciliation — 4 October 2026

Maintainer agreement to T01–T09 and the host boundary was recorded without changes.
Updated the authoritative criteria, chart/register, campaign/backlog references
and appended agreement updates to the handoff/review pack, preserving draft
history. `python3 tools/check_links.py` and `git diff --check` passed again.
A02 is complete locally; gates 01–05/HOLD persist. No executable changes or new
experiments occurred. Documentation remains uncommitted; nothing was published.

## Task 07 implementation validation — 4 October 2026

Reviewed the seven existing A02 documentation changes and ran the baseline
`PYTHON=.venv/bin/python ./scripts/check`, `./scripts/demo` and `git diff --check`:
45 tests, local links, lint/format/types and demo passed. A02 was committed
separately as `b46261b`; its historical agreement was preserved.

New implementation validation: `./scripts/test` passed 53 tests and local links;
`./scripts/demo` passed unchanged; `PYTHON=.venv/bin/python ./scripts/check` passed
53 tests, links, Ruff 0.16.9 lint/format and strict mypy 2.3.1. Both interpreters were
Python 3.11.4. Two executions of
`PYTHONPATH=packages .venv/bin/python -m wawet.scenarios --json` compared identical
with `cmp`. Final `git diff --check` and Markdown links passed.

[Runbook](research/contact-scenarios.md), [results](research/results/contact-scenarios.json)
and [source/environment hashes](research/results/contact-scenarios-evidence.json)
record fixture outcomes and limitations. Existing application/transport/protocol
files and frozen vectors are unchanged. No RNS campaign rerun was needed for this
independent simulation package. Hosted Python 3.12/3.13 and external links/anchors
remain unverified; no physical/RF, T01/T02 or gate acceptance is claimed.

Git writes required sandbox escalation for the requested local commits. No push,
PR or external publication occurred. Task 07 is recorded in a separate local
implementation commit; gates 01–05 and investment HOLD remain unchanged.

## Task 09 bounded encoding comparison — 4 October 2026

New local validation; historical results above were not rewritten. Starting tree
was clean at `c0dd25b900b21cadc96c1f8043fbb8247811583e`; A02 and task 07 were committed.

- Before implementation, `PYTHON=.venv/bin/python ./scripts/check` passed all
  53 tests, local Markdown links, Ruff lint/format and strict mypy.
- After implementation, the same command passed **62 tests**, local Markdown
  links, Ruff lint/format (19 files) and strict mypy (8 application source files).
  Research codecs are linted/tested; strict typing scope remains the application.
- `PYTHON=.venv/bin/python ./scripts/demo` passed with the unchanged 38-byte
  example, direction filtering, duplicate suppression, outage and expiry.
- Two fresh `.venv/bin/python tools/encoding_comparison.py --sizes-only` outputs
  compared byte-identically with `cmp` (exit 0).
- `.venv/bin/python tools/encoding_comparison.py` completed sequential isolated
  v1/binary/CBOR benchmarks at 1,000 operations and five repeats. The
  [raw JSON](research/results/encoding-comparison.json) records environment,
  source/input hashes, base revision and the uncommitted working state at capture.
  The [report](research/encoding-comparison.md) defines the profiles, methods,
  complete size table, observations and limitations. Hashes identify the exact
  benchmark source; the capture predates final documentation edits.

Python 3.11.4 on macOS 26.2 arm64; standard-library implementation, no dependency
addition. Allocation results are transient traced Python memory, not RSS, MCU
footprint or T06 acceptance. Signature bytes are placeholders. Frozen v1 vectors
and production APIs are unchanged. No gate closes; G01 HOLD persists. Hosted
Python 3.12/3.13 remains unverified. No commit, push or remote publication occurred.

## Task 18 bounded prior-art review — 4 October 2026

New local validation; historical counts/results above are preserved. Starting Git
status was clean at `3e247c8f16045b8891df2d38ae74fac80d960710`, confirming task 09
was committed after its earlier uncommitted capture. Task 07 and A02 commits were
also inspected. No Wawet executable behaviour or dependency changed.

- Public-source review covered the existing eight-system comparison. Sources were
  manually opened and checked against the stated claims; failures, browser
  challenges, mutable-version limits and exact searches are explicitly recorded in
  the [evidence register](research/results/prior-art-evidence.md). This does not
  assert that every external link/anchor is reachable or checked automatically.
- Waycast was fetched into a separate temporary checkout at upstream revision
  `958f4a6ea6436d145402830c3edd372e2e40f74e`. Root licence, build recipes, tests,
  exercised sources and Git history/tags were inspected before execution. The
  initial sandboxed fetch failed DNS; the approved network fetch succeeded.
- Six direct compile/run commands, equivalent to the three upstream Makefile test
  recipes, all exited 0 with no compiler diagnostics. Wire/mesh output each reports
  nine cases passed; net reports NMEA/DTU success. The wire executable additionally
  runs a query/reply check, so no aggregate test count is asserted. Compiler was
  Apple clang 17.0.0, arm64 macOS; [JSON](research/results/prior-art-reproduction.json)
  records exact commands, output, environment and 16 source-file hashes.
- No dependency installation, full GUI, provisioning, tile fetching or radio
  transmitter was run. `pkg-config --modversion sdl2` exited 127; GUI prerequisites
  remain outstanding. Unit reproduction does not validate field/security claims.
- `python3 tools/check_links.py` passed repository Markdown file links.
  `git diff --check` passed. A one-off comparison with `git show HEAD:docs/project-plan.md`
  confirmed all **79 task IDs and prerequisites unchanged** and the future chart
  differs only by task 18's `done` marker. Task 14 still requires 03/09, and G01's
  prerequisites and HOLD decision remain unchanged.
- Reproduction JSON inspection confirmed six successful commands and 16 hashes;
  source hashes were checked against the temporary checkout. Only documentation
  and evidence files changed. No Wawet unit suite or RNS campaign rerun was needed;
  historical/hosted Python results are not newly established here.

Task 18's bounded desk investigation is complete locally. Full GUI/physical
reproduction, independent field/security validation and archived first-publication
chronology remain unresolved. No third-party source was imported into Wawet;
no participant dataset was copied, purchase/outreach/RF/road trial undertaken,
or commit/push/PR/publication performed. Gates 01–05 and G01 HOLD persist.

## Task 01 distribution dossier — 4 October 2026

New documentation/evidence validation against clean HEAD `2f21ac5`. This commit
already contains task 18; earlier uncommitted records remain historical.

- Acquisition: `python3 /tmp/wawet-dossier-fetch.py` retrieved five exact pinned
  source archives and two macOS arm64 wheels from publisher PyPI URLs. Initial
  sandboxed urllib access failed DNS; approved network acquisition succeeded.
  No package was installed or executed. The one-off temporary acquisition script
  was not added as application tooling; URLs, filenames and hashes are in the
  [register](research/results/distribution-review/artefact-register.json).
- `python3 /tmp/wawet-dossier-complete.py` captured complete RNS leading-header
  licence and vendored header notices, recorded native source lock metadata and
  explicit missing-text/build-provenance gaps. Source/header member paths and
  extraction method are recorded. Full archive bytes remain temporary; captured
  licence evidence and selected publisher metadata are preserved in the repository.
- A one-off standard-library verification parsed every evidence JSON; matched all
  **7 archive sizes/SHA-256 values** to both downloaded bytes and captured publisher
  records; checked all **15 notice SHA-256 values** against saved evidence and
  exact archive members/header extraction; checked the cryptography Cargo.lock
  member hash. All assertions passed. This establishes evidence correspondence,
  not legal validity, final binary provenance or distribution approval.
- The same verification compared project-register task IDs and prerequisite
  columns with `git show HEAD:docs/project-plan.md`: unchanged. Task 18 status
  now records its actual commit; task 01 remains open, qualified review pending.
- `python3 tools/check_links.py` passed local Markdown file links;
  `git diff --check` passed. Exact publisher metadata/archive URLs were accessed
  during retrieval; external anchors and other repository URLs were not checked.
- Final diff/status inspection found only documentation and evidence changes.
  No public API, runtime dependency, v1 vectors or transport behaviour changed.
  Unit tests and RNS campaigns were not rerun for this package; hosted Python
  3.12/3.13 results are not newly established.

Remaining gaps: qualified interpretation/outcome, complete attributable vendored
ConfigObj/validate/i2plib notices, final-wheel native provenance/notices, and exact
future image/interpreter/OS/firmware/LXMF scope where selected. Dossier preparation
is complete; task 01 and gates 01–05 remain open, G01 HOLD persists. No outreach,
purchase, RF/road trial, commit, push or publication occurred.

## Task 01 reviewer arrangement — 4 October 2026

Starting tree was clean at `ff3df9f`; the dossier is committed. Added the
[reviewer arrangement package](research/distribution-review-arrangement.md),
linked it from the dossier and updated the plan/backlog/handoff with a new dated
entry. Historical preparation notes and Q01–Q07 remain intact.

- Manually opened/read primary Moorcrofts service, contact and homepage pages,
  Bristows open-source practice and contact pages, and FSFE's canonical licensing
  FAQ/team page. All URLs used in the shortlist returned readable content through
  the web tool. The obsolete FSFE licence-questions path redirected to the cited
  canonical FAQ; an initial Bristows `/contact-us/` attempt failed, so the site's
  own Contact link was followed to the working `/contact/` page. No forms submitted.
- Provider descriptions support two legal-review candidates and one community
  referral route; FSFE's inability to give legal advice is explicit. Published
  numeric pricing for this scoped review was not found on inspected pages;
  availability, willingness and engagement costs remain unknown. No independent
  professional-registration check or reviewer appointment is claimed.
- `python3 tools/check_links.py` passed local Markdown file links.
- `git diff --check` passed. A read-only comparison of task-register IDs and
  prerequisite columns against `git show HEAD:docs/project-plan.md` passed;
  assertions confirmed task 01 remains Open and G01 remains HOLD.
- Reviewed tracked diff and the new package for unsupported acceptance claims,
  sensitive material and executable changes: documentation only, no keys or
  participant records. External pages were read, not frozen or exhaustively
  checked for anchors; recheck them before contact.

No unit tests or RNS campaigns rerun for this documentation-only package; hosted
Python 3.12/3.13 results are not newly established. Preparation is complete locally
and uncommitted; qualified review and reviewed release approach remain pending.
No outreach, commissioning, spending, commit, push or publication occurred.

## Task 01 self-review direction — 4 October 2026

After the arrangement package, the maintainer declined hiring a reviewer.
Updated its current direction and plan/backlog/handoff/dossier with a bounded
self-review sequence; retained reviewer research as deferred historical work.
`python3 tools/check_links.py` and `git diff --check` passed. No executable
behaviour changed; tests/campaigns were not rerun. The self-review has not yet
been performed. Existing qualified-review acceptance and task dependencies remain
unchanged; task 01 is open and G01 HOLD persists. Changes remain local/uncommitted;
no outreach, spending or publication occurred.

## Task 01 bounded self-review — 4 October 2026

Baseline HEAD `ff3df9f`; the previous arrangement/direction documentation changes
were already uncommitted and preserved. The new
[self-review](research/distribution-self-review.md) assesses Q01–Q07 and proposes
form-specific decisions; it does not record maintainer adoption or legal approval.

- Downloaded exact ConfigObj 5.0.9 and i2plib 0.0.14 source archives using publisher
  PyPI JSON URLs/hashes; downloaded i2plib's pinned v0.0.14 tag and raw licence.
  Sandbox DNS initially failed; network-enabled retrieval succeeded. Nothing
  downloaded was installed, imported or executed.
- Verified the seven historical archives and fifteen saved notice hashes. New
  source archives matched PyPI hashes; recovered ConfigObj BSD/i2plib MIT texts
  matched their source members. Original register/evidence remained unchanged.
- Ten vendored byte comparisons were recorded; all eight i2plib release Python
  files matched the pinned tag. RNS has three exact i2plib matches and five changed
  files; both ConfigObj/validate files differ. AST inspection excluding docstrings
  still found validate differences; no semantic equivalence claimed.
- Static `/usr/bin/otool -L` inspection on two hashed native wheel members recorded
  cffi system-libffi linkage and cryptography load commands. `/usr/bin/strings`
  found the recorded OpenSSL version string; this is not build provenance proof.
- Opened current primary Reticulum commentary and cryptography installation docs;
  treated commentary as context, not licence amendment or settled legal findings.
  The GitHub pinned licence blob web fetch failed; its raw pinned URL succeeded.
- An independent verification pass confirmed nine PyPI archive hashes, pinned-tag
  hash, two complete notice extractions, ten vendored comparisons, eight tag/release
  matches, both native records and the version-string observation; all assertions
  passed. Replay instructions and source/member hashes are in the evidence README.
- Compared task IDs, prerequisite columns and completion criteria against
  `git show HEAD:docs/project-plan.md`: unchanged. Task 01 remains Open; G01 HOLD
  preserved. Updated licensing ADR adds evidence without changing licence scope.
- `python3 tools/check_links.py` and `git diff --check` passed. Reviewed the new
  assessment/evidence and tracked diff: documentation/licence evidence only, no
  upstream executable source, private keys or participant data added. External
  sources were accessed individually; no exhaustive external/anchor check claimed.

No unit tests or RNS campaigns rerun for this documentation/evidence-only package;
hosted Python 3.12/3.13 results are not newly established. Self-review evidence is
complete, but maintainer adoption, AI service data-use assessment, modification
provenance, native notices/build evidence and the existing qualified-review gate
remain open. Paid review is deferred. Changes remain local/uncommitted; no outreach,
spending, RF/road trials, commit, push or release occurred.

## Task 01 assurance update and publication — 4 October 2026

The maintainer explicitly authorised replacing mandatory external review with
maintainer self-review, then requested a Conventional Commit and push. Updated
current plan/backlog acceptance, licensing policy and ADR; dated supersession
entries preserve the earlier requirement as historical. Task 01 remains Open
pending the maintainer's form-specific release/risk decision; G01 stays HOLD.
Other prerequisites and technical/regulatory requirements are unchanged.

`python3 tools/check_links.py` and `git diff --check` passed. `git fetch origin`
succeeded; main and origin/main matched before this documentation commit. Reviewed
the accumulated package: original assessment, licence evidence and documentation
only, with prior local work preserved. No executable changes require test/campaign
reruns. Publication is authorised for this package; previous no-publication entries
remain true for their earlier steps. Commit/push outcome is reported after execution.
