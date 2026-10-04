# Distribution review evidence

Captured 4 October 2026. See the [review dossier](../../distribution-review.md)
and [artefact register](artefact-register.json). Licence/notice evidence retains
its upstream terms; it is not original Wawet software or relicensed prose.

Reacquire each archive from its recorded `url`, verify `sha256` and `size`, then
read `member` without installing or executing the archive. Standalone notices
are copied byte-for-byte. For RNS header records, take leading comment and blank
lines before the first code/docstring line; check the full source member hash
separately. Cargo.lock packages are source-lock metadata, not a binary SBOM.

For a local hash recheck from the repository root:

```sh
python3 - <<'PYCODE'
import hashlib, json
from pathlib import Path
root = Path('docs/research/results/distribution-review')
register = json.loads((root / 'artefact-register.json').read_text())
for record in register['artefacts']:
    for notice in record['notices']:
        data = Path(notice['evidence_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == notice['sha256']
for path in root.rglob('*.json'):
    json.loads(path.read_text())
print('Captured notice hashes and JSON passed')
PYCODE
```

This recheck does not fetch archive binaries or verify legal completeness.
Named gaps are retained in each affected record and in the dossier.
