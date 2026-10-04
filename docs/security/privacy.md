# Privacy design

**DESIGN DECISION:** transmit reports rather than periodic vehicle tracking.
Experimental v1 carries an event-specific ID, report location, affected heading,
creation time, TTL and radius; no VIN, plate, account or persistent source ID.
The local identity token stays outside the wire frame. This minimises data but
is not anonymity: observers can correlate radio fingerprints, timing, position,
IP addresses and repeated behaviour.

Default simulator storage is memory-only, capped at 1024 events and pruned at
expiry on receive/alert access. No raw movement history or audio is persisted.
The demo prints known synthetic coordinates/bytes. Future logs should report
aggregate counters without location/pseudonym labels; packet capture requires
explicit research consent and a retention plan.

A dormant receiver may hold expired objects until the next access; no background
privacy erasure service exists. Production firmware needs scheduled expiry and
power-loss handling. Data already received by strangers cannot be remotely erased.

The location of an observed hazard may differ from the reporter's location.
Protocol accuracy/source fields are not implemented; do not promise lane-level
location. Pseudonym rotation should be tested against linkability, path discovery
cost and reputation. Reticulum encryption can protect intended recipient traffic,
but cannot make an intentionally public hazard private from its recipients.

**OPEN QUESTION:** anonymity, reputation and abuse prevention conflict. A new key
must not count as an independent confirmation. Avoid central mandatory accounts
as a shortcut; test local trust and corroboration, acknowledging limits.

Phone consent: request only needed permissions, keep dictation/local maps on the
phone, fail offline gracefully and never silently upload raw speech. Firmware
telemetry must be opt-in and basic operation must survive refusal. Fleet products
must not inherit consumer location permissions implicitly. A privacy/data-
protection assessment is required before real participant trials; none has been
completed here.
