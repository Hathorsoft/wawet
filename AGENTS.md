# Agent working guide

Wawet is an early-stage civilian communications ecosystem maintained by
Hathorsoft Ltd. Read [the handoff](docs/agent-handoff.md) before choosing or
extending work. It records implemented scope, limitations and the next gates.

## Start here

1. Inspect `git status --short` and the current files. Preserve existing work;
   do not assume a clean checkout or that local changes have been published.
2. Read [README](README.md), [handoff](docs/agent-handoff.md),
   [architecture](docs/architecture/system.md) and the relevant
   [backlog acceptance criteria](docs/community/backlog.md).
3. Read [LICENSING](LICENSING.md) before adding dependencies or importing code.
   Consult [ADRs](docs/architecture/adr/README.md) for settled versus experimental
   decisions, and the [research rules](docs/research/README.md) for evidence.
4. Run the relevant baseline checks before modifying executable behaviour.

## Development commands

Python 3.11+. Demo and tests require only the standard library:

```sh
./scripts/demo
./scripts/test
```

For all contributor checks in a fresh checkout:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
PYTHON=.venv/bin/python ./scripts/check
```

The optional real RNS experiment is separate; see
[its reproduction instructions](docs/research/reticulum-spike.md). Do not make
RNS necessary for the default simulator/test path.

## Implementation boundaries

- Keep event/domain logic independent of RNS, radio settings and simulator
  internals. Use `EventTransport` and injected clocks. The current application
  is single-threaded; marshal real transport callbacks accordingly.
- The experimental v1 frame is exactly 38 bytes. Keep specification, field
  validation and frozen vectors aligned. Do not append unversioned fields or
  silently reinterpret unknown categories. Update tests and the encoding ADR
  when protocol behaviour changes.
- Reticulum is the proposed networking foundation, not a proven production
  integration. Do not build a second general routing stack or describe the
  direct PLAIN TCP spike as authenticated, routed or radio-tested.
- RNode is a radio interface, not automatically a standalone Wawet application
  processor or relay. No firmware, custom hardware, production adapter or
  mobile frontend exists yet.
- Keep the edge simple. Phone/gateway features need not be replicated in every
  Drive. Standalone basic operation, no mandatory cloud/account/subscription,
  cost and privacy are product constraints.
- Reticulum/LXMF currently use restricted upstream terms, not plain MIT.
  Original project software/specs are Apache-2.0, prose CC BY 4.0, and future
  original hardware design source CERN-OHL-S v2. Do not relicense dependencies
  or promise legal/compliance approval.
- Clearly label facts, assumptions, measured results, decisions and open
  questions. Cite primary sources for current hardware/regulatory claims.
  Paper cost bands are not quotations. Simulation is not a field measurement.
- Do not transmit on unreviewed radio profiles, test distracting interactions
  on public roads, or commit real participant location data. See the privacy,
  threat and human-factors documents before work affecting those areas.

## Completion and handoff

Run checks appropriate to the change. `./scripts/check` combines unit tests,
local Markdown file-link checking, lint, formatting checks and strict type
checking. Hosted CI also targets Python 3.12/3.13; local results alone do not
establish those runs passed. External URLs and anchors are not checked locally.

Document actual commands/results and remaining limits; update related specs,
ADRs and backlog criteria when behaviour or decisions change. Keep historical
validation results distinguishable from new runs. Do not backdate new
implementation work or rewrite milestone history unless explicitly requested.
Remote pushes, PRs and issues are not implicit in this local foundation handoff.
