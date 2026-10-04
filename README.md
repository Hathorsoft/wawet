# Wawet

**Simple devices. Sophisticated network.**

Wawet is an early-stage, open-source communications project maintained by
Hathorsoft Ltd. The first application is nearby road information: a driver
presses a tactile button, and useful reports reach other drivers. The wider
vision includes community communication, outdoor use and infrastructure.

Hathorsoft intends to manufacture official Wawet hardware. Buying official
hardware will not be mandatory: compatible implementations and commercial
forks are permitted under the applicable licences. Basic communication must
remain useful without Hathorsoft servers or a recurring fee.

Reticulum is the proposed network foundation. LoRa/RNode is an important early
radio candidate; IP, Wi-Fi HaLow and future bearers can coexist. The shipped
simulator has no Reticulum dependency. Upstream RNS licensing is a material
open question; see [LICENSING.md](LICENSING.md).

## Run something now

Requires Python 3.11 or newer. The demo and unit tests need only the standard library:

```sh
git clone https://github.com/Hathorsoft/wawet.git
cd wawet
./scripts/test
./scripts/demo
```

For an installed CLI and contributor checks:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
wawet-demo
./scripts/check
```

The deterministic demo delivers a **38-byte** hazard report to a vehicle **1.3 km
ahead**, filters the opposite direction, suppresses duplicates, models an outage
and rejects expired reports. No real radio, cryptographic trust, lane matching
or automatic forwarding is implied.

An optional [Reticulum experiment](docs/research/reticulum-spike.md) demonstrates
actual two-process RNS delivery on loopback. It is not a production adapter.

## Explore and contribute

- [Agent working guide](AGENTS.md) and [current handoff](docs/agent-handoff.md)
- [Vision](docs/vision.md) and [system architecture](docs/architecture/system.md)
- [Experimental road-event specification](protocol/road-event-v1.md) and [vectors](protocol/vectors/v1.json)
- [Drive requirements](devices/drive/docs/product-requirements.md), [hardware concepts](devices/drive/docs/hardware-concepts.md) and [feature matrix](devices/drive/docs/feature-matrix.csv)
- [Research index and evidence rules](docs/research/README.md)
- [Project Gantt chart and task register](docs/project-plan.md)
- [Roadmap](docs/roadmap.md) and [first backlog](docs/community/backlog.md)
- [Contributing](CONTRIBUTING.md), [security](SECURITY.md), [privacy](docs/security/privacy.md) and [driver safety](devices/drive/docs/human-factors.md)
- [Foundation review](docs/architecture/adversarial-review.md) and [validation record](docs/validation.md)

This is research software, not a navigation or emergency service. No hardware
has been designed, certified or road-tested. A £30–£50 retail device is an
aspiration to investigate, not a promised price. Taxonomy and physical button
mappings are provisional.

## Repository

| Area | Purpose |
| --- | --- |
| `packages/wawet` | Protocol, geography, vehicles, transport boundary and simulation |
| `protocol` | Language-independent specification and canonical examples |
| `devices` | Drive product research; Pocket, Relay and Gateway definitions |
| `docs` | Architecture, ADRs, research, security, business and community |
| `tests` | Protocol and application behaviour tests |
| `tools` / `scripts` | Contributor checks and optional RNS experiment |
| `.github` | CI and contribution templates |

Wawet is a modern working name inspired by Wepwawet; it does not itself
literally translate to “Opener of the Ways”. Trademark clearance is pending.
The original car-network discussion dates to 25 February 2025 at 13:25:57 GMT;
LoRa/ESP32 implementation exploration began on 7 April 2025 at 12:26:25 BST.
The earlier [concept notes](docs/concept.md) are retained.

Original software and protocol: Apache-2.0. Documentation: CC BY 4.0. Future
original hardware designs: CERN-OHL-S v2. See [licence scope](LICENSING.md) and
[brand policy](docs/business/trademark-policy.md).
