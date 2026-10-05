# Task 04 desktop workload validation — 5 October 2026

This archive contains original Wawet source snapshots and synthetic desktop
workload logs. It does not establish physical memory, power, startup, cost or
network acceptance. Task 04 remains open and G01 remains HOLD.

`source.zip` preserves the driver, regression tests and application modules;
`source-hashes.json` records their SHA-256 hashes. Source at baseline `a2f40d8`
plus the new driver was used. Metadata records the working-tree status and tracked
diff hash at run start; untracked driver provenance is its separate content hash.
Documentation and tests were developed during the rehearsal; driver/application
sources were unchanged throughout the final run. No RNS workload ran alongside it.

Raw JSONL files are gzip-compressed without changing their contents. Short runs
are equivalent after excluding metadata records and the `utc`,
`monotonic_seconds` and `duration_seconds` fields. Measurement-mode active time
may exceed 600 seconds slightly because the final cycle completes before exit.
The superseded rehearsal was deliberately interrupted after the metadata-cleanup
fix; retain its failure record rather than counting it as a successful full run.

`summary.json` records raw file hashes, measured phase durations, completed cycles,
final counters and exit results. Verify decompressed hashes before analysis.
Timing is process-local desktop timing. Codec/report operation counts refer to
the hold loop; alert counts include hold/prune calls, and receive counts include
all direct delivery attempts. They do not count every internal Vehicle call or
encoding used to construct probe/fill frames.
