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
