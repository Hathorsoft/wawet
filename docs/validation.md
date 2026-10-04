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
