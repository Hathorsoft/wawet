# Contributing

Start with [the README](README.md), [architecture](docs/architecture/system.md)
and [first backlog](docs/community/backlog.md). Small fixes, experiments and
negative results are useful. Explain the problem before expanding scope.

Coding agents should also read [AGENTS.md](AGENTS.md) and the
[self-contained handoff](docs/agent-handoff.md); no chat history is required.

Requires Python 3.11+. Install contributor tooling with
`python -m pip install -e '.[dev]'` in a virtual environment, then run
`./scripts/check`. `./scripts/demo` and `./scripts/test` also work without
installation. The optional RNS spike has its own documented dependency/licence
scope and is not necessary for a contribution.

Keep domain code independent of transports. Change protocol fields only with
an updated specification, version strategy and frozen vectors; experimental
v1 has no production compatibility guarantee. Use injected clocks rather than
sleep in application tests. Add meaningful regression tests for behaviour.
Document unresolved product decisions instead of inventing requirements.

Research PRs distinguish facts, assumptions, experimental results, decisions
and open questions. Include primary source editions/dates and reproducible
measurements. Do not assert radio/driver compliance from generic summaries.
No public-road distraction testing or unreviewed transmitting experiments.

Submit small PRs with the final behaviour, validation and material limitations.
Apply [the code of conduct](CODE_OF_CONDUCT.md). Follow [security reporting](SECURITY.md)
for sensitive issues rather than publishing exploitation details immediately.

By submitting, you confirm you may contribute the material under its applicable
[project licence](LICENSING.md). You retain copyright; no assignment is required.
Declare third-party sources and licences. Do not commit secrets, private chat
exports, personal vehicle tracks or unconsented participant data. No CLA or
sign-off automation is configured; maintainers review rights and attribution.
