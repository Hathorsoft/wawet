# Distribution self-review evidence — 4 October 2026

[Assessment](../../distribution-self-review.md), [evidence JSON](evidence.json).
The two complete licence texts are upstream evidence under their original terms,
not Wawet prose. No upstream executable source is stored here. Existing seven
artefacts and their notice extracts remain in the historical register unchanged.

## Acquisition and verification

Python 3.11 standard-library tools read archive bytes without executing them.
The existing seven archives in `/tmp/wawet-review-artefacts` were rehashed against
[the original register](../distribution-review/artefact-register.json). All fifteen
saved notices were rehashed. For ConfigObj 5.0.9 and i2plib 0.0.14, publisher PyPI
JSON selected the sdist URL and SHA-256; downloads matched that hash. i2plib's
GitHub tags API resolved v0.0.14 to `6edf51cd5d21cc745aa7e23cb98c582144884fa8`.
The pinned codeload archive hash and raw licence URL are saved in the new JSON;
its licence bytes matched the raw pinned URL, and eight release Python files
matched the corresponding tag members. GitHub archive hash identifies retrieved
bytes, not a publisher-signed release hash.

Downloads required network-enabled shell access after sandbox DNS failed. A web
open of the pinned GitHub blob failed; the raw pinned URL was successfully read
with Python. Archive and metadata acquisition did not install or run packages.

## Replay

Retrieve original archives using the existing register and new upstream archives
and pinned tag using `evidence.json`; verify SHA-256 before reading members.
Archives and complete upstream metadata were retained in temporary storage only.
Re-extract the two notice `source_member` paths; hash the saved texts. Compare each
vendored member to the `upstream_member` in the recorded source archive using
byte equality, not the declared version alone. The i2plib source comparison also
checks each upstream member against the same suffix in the pinned tag.

From the repository root, verify saved notices and any available archives:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

root = Path.cwd()
record = json.loads((root / 'docs/research/results/distribution-self-review/evidence.json').read_text())
for notice in record['notices']:
    assert hashlib.sha256((root / notice['path']).read_bytes()).hexdigest() == notice['sha256']
for artefact in record['verified_original_artefacts'] + record['upstream_artefacts']:
    data = (Path('/tmp/wawet-review-artefacts') / artefact['filename']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == artefact['sha256']
print('Saved notices and nine archive hashes verified.')
PY
```

Missing temporary archives must be retrieved, not treated as verified. This replay
checks correspondence, not legal interpretation or download authenticity beyond
the recorded evidence. The tag archive hash is checked separately from its JSON
record; it is not one of the nine PyPI artefacts in the replay loop.

## Static native inspection and limitations

Extract only the `.so` members named in the JSON to temporary files (no import or
execution). On macOS, run `/usr/bin/otool -L` on each; raw load-command results and
member hashes are recorded. Temporary paths in the output are acquisition paths,
not product locations. On the cryptography member, run `/usr/bin/strings` and
filter for `^OpenSSL [0-9]`; the observed version string is recorded separately.
Do not mistake a string or dynamic-library load command for a complete native
SBOM, source provenance, upstream version or legal notice inventory.

Validate licence/hash correspondence and observed differences, not semantic
identity. The archive comparisons establish three exact i2plib vendored matches,
five changed files and changes in both ConfigObj/validate files. No claims about
unobserved authorship, legal compatibility, participant data or product target
follow from these checks. No runtime tests/campaigns were needed for this evidence
and documentation package.
