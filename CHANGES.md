# Version History

## Future Versions
- N/A

## Upcoming Changes
- Support Python 3.13
- Raised dependency floors only where needed to purge known vulnerabilities,
  and left everything else deliberately unconstrained:
  - Added `setuptools` floors to `[build-system].requires`, which was
    previously unbounded, to keep CVE-2024-6345, CVE-2025-47273 and
    CVE-2026-59890 out of the build environment. Build requirements are not
    recorded in the built wheel, so this imposes nothing on installers.
  - Relaxed `python-resize-image` from `==1.1.20` to `>=1.1.20`.
  - `boto3`, `botocore`, `pyvips` and `twine` have no advisories against any
    release and remain unconstrained.
- The maintainer-only `requirements-ci.txt` can no longer be installed on
  Python 3.9: `Pillow>=12.3.0` is the oldest Pillow with no known CVEs, and it
  requires Python >= 3.10. The library itself is pure standard library and
  still supports 3.9. The upload workflow now pins Python 3.13 explicitly; it
  previously carried a `python-version: ["3.9"]` matrix that was never passed
  to `actions/setup-python`.

## Current Version

### 2.3.1 (2025-02-12)
- Update pypi build action (See juriscraper #1308)

## Past Versions

### 2.3.0 (2025-02-12)
- Removed support for Python 3.7 and 3.8.
- Fixed various `pylint` warnings and errors:
  - Added missing encoding in `open()`.
  - Avoided raising overly general exceptions.
  - Removed unused imports.
  - Improved string formatting.
- Updated workflow files to match new Python versions.
- Added `CHANGES.md` file.
- Implemented a workflow to check for new entries in `CHANGES.md`.

### 2.2.5 (2024-07-18)
- Added **Mississippi** and **Tennessee** seals.
