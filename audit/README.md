# Audit workspace — how to run, what is where

This directory contains the independent audit of the single-file application
in `app/`. Nothing here is required to *use* the application: it is a plain
HTML file that runs offline in any modern browser.

## Contents

| path | what it is |
|---|---|
| `AUDIT_REPORT.md` | findings ranked by engineering impact, with evidence and the fix applied |
| `VERIFICATION.md` | formula-by-formula verification table with sources and status |
| `ENGINE_DATABASE.md` | the YANMAR database checked field by field against the manufacturer's pages |
| `MATCHING.md` | engine–gearbox–propeller matching for the nine presets, with the full power ledger and the rejection tally (generated) |
| `TEST_REPORT.md` | the ≥50-case regression suite result table (generated) |
| `LIMITATIONS.md` | verified vs estimated vs assumed vs uncertain, and what remains unresolved |
| `CHANGELOG_AUDIT.md` | every change made to the application, with the reason |
| `independent/ref.py` | independent Python implementations of ITTC-57, Holtrop & Mennen (1982/84) and Savitsky (1964) |
| `yanmar_official.py` | YANMAR product-page data transcribed 2026-10-25 (source URL per engine) |
| `extract_scripts.py` | splits the HTML into its `<script>` blocks (`build/`, git-ignored) |
| `js/dump_core.cjs` | runs the calculation core headlessly (node + `vm`) → JSON |
| `js/dump_dom.cjs` | runs the whole application in jsdom → JSON |
| `run_audit_tests.py` | the conformance suite (443 cases) |
| `match_report.py` | generates `MATCHING.md` |

## Requirements

* Python 3.9+ (standard library only — no numpy required)
* Node.js 18+ and `jsdom` for the full-application runs:

```
cd audit/js && npm install          # installs jsdom (dev dependency only)
```

`jsdom` is the only third-party dependency of the audit. The application itself
has **no** dependencies and no network access.

## Run everything

```
python3 audit/run_audit_tests.py     # exit code 0 = every case passed
python3 audit/match_report.py
```

The suite extracts the scripts from the shipped HTML every run, so it always
tests exactly what ships. It fails with a non-zero exit code if any case fails
and prints the failing cases with measured vs expected values.

## Regression / acceptance criteria

The suite is the acceptance gate:

* group A — published benchmarks (Holtrop & Mennen 1982 example, Savitsky on
  the Shoemaker 1934 case at two speeds, Burrill/MIT, Keller/ITU, unit
  conversions);
* group B — Holtrop against the independent implementation on ten hulls
  (S, R_T, R_W, form factor);
* group C — Savitsky against the independent implementation on six craft;
* group D — B-series evaluation, identities, Reynolds correction;
* group E — friction line;
* group F — the engine database against the manufacturer's published rows;
* group G — end-to-end selection invariants (power ledger, limits, cavitation,
  rejection reasons, right-sizing, boundary flags) for the nine presets;
* group H — boundary/invalid inputs must be refused, not extrapolated;
* group I — the application's own in-app self-test, run headless.

## Provenance of the audited file

`legacy/work_v2_original.html` is the uploaded file, unmodified. `legacy/SHA256SUMS`
records its hash so any later edit of `app/` can be diffed against it:

```
sha256sum -c legacy/SHA256SUMS
```

## Licences

The audit code (this directory) may be used under the repository's MIT licence.
The **reference** repositories consulted (`/home/user/refs/...`: a GPL-3.0 fork
and two forks with no licence file) were read for comparison only — no code was
copied from them. YANMAR data are facts transcribed from public product pages
and are cited per model in `yanmar_official.py`.
