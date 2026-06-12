# TwitterAuth CI Baseline

Status: Completed

## Scope

Run the legacy Unity TwitterAuth static contract in GitHub Actions without
requiring a Unity editor on the CI host.

## Completed Work

- Added `.github/workflows/check.yml` to run `make check` on pushes, pull
  requests, and manual dispatches.
- Set up Python 3.12 before running the static Unity contract checker.
- Extended `scripts/check_unity_contracts.py` to require the CI workflow and
  this completed maintenance plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Add a Unity batchmode job once the expected editor version and license setup
  are documented.
