# Audit deliverables — where everything is

Audited artefact: **`app/yanmar_engine_propeller_selector.html`** (single file,
no dependencies, runs offline). Original preserved byte-for-byte in
`legacy/work_v2_original.html` (`legacy/SHA256SUMS`,
`6d0391318af7012c505721208ba84c0d4efa15a711ea2360492dd978ccc43960`).

| # | requirement | deliverable |
|---|---|---|
| 1 | audit report ranked by severity and engineering impact | **`audit/AUDIT_REPORT.md`** — 19 findings F-01…F-19 with the evidence, the consequence and the fix applied; an appendix of what was verified without change and of what remains unresolved |
| 2 | corrected, working application + all modified source, original structure and features preserved, originals backed up | **`app/yanmar_engine_propeller_selector.html`** (the only file changed) · backups `legacy/work_v2_original.html`, `/home/user/backups/work_v2_original_2026-10-25.html` · every edit replayable as `patches/patch1…5.py` |
| 3 | formula-by-formula verification table with authoritative references | **`audit/VERIFICATION.md`** — 48 rows: expression as implemented, V/C/I/U status, and the numeric evidence (including the 0.07 % residual and its cause) |
| 4 | validated YANMAR database with traceable sources | **`audit/ENGINE_DATABASE.md`** + **`audit/yanmar_official.py`** (26 engines, 52 rating rows, masses, dimensions, gear ratios; page and access date per row) |
| 5 | matching results with rejection reasons | **`audit/MATCHING.md`** — all nine presets: candidate, full power ledger, propeller geometry, cavitation margins, and the rejection tally plus the first rejections in candidate order |
| 6 | ≥50-case reproducible suite with pass/fail, tolerances, discrepancies | **`audit/run_audit_tests.py`** (443 cases, cross-implementation and database conformance) and **`tests/run_suite.js`** (126 cases, external, runs the shipped DOM). Reports: `audit/TEST_REPORT.md`, `tests/TEST_RESULTS.md` |
| 7 | change log, limitations, installation, regression instructions | **`audit/CHANGELOG_AUDIT.md`**, **`audit/LIMITATIONS.md`**, **`audit/README.md`**, **`tests/README.md`** |
| 8 | statement separating verified / estimated / assumed / unresolved | **`audit/LIMITATIONS.md`** §1–§4, summarised below |

## Installation

Nothing to install to **use** the tool: open `app/yanmar_engine_propeller_selector.html`
in a current browser (it needs no server, no network and no dependencies).

To reproduce the audit:

```
python3 audit/run_audit_tests.py      # standard library only; ~30 s
python3 audit/match_report.py         # regenerates audit/MATCHING.md
cd tests && npm install && node run_suite.js   # needs Node 18+ (jsdom dev dep)
```

## The four-category statement (short form)

* **Verified** against an independent published source: the whole Holtrop &
  Mennen resistance chain (paper's own example, −0.07 %), the Savitsky planing
  chain (published Shoemaker 1934 recomputation), ITTC-1957, the B-series
  evaluation and its identities, Burrill/Keller, and 214 engine-database fields.
* **Estimated, not validated for these vessels:** the resistance and required
  power of *every preset* — Maldivian dhonis sit outside the Holtrop regression
  range (C_B 0.45–0.50, L/B 3.4–3.9, B/T 4.6–5.2), so the tool reports
  "OUTSIDE VALIDATION DOMAIN" and must be read as a screening estimate. Also
  estimated: wake/thrust-deduction/η_R from those regressions, the propeller-law
  operating point, part-load fuel, and the shaft diameter (rule *forms*, not a
  class calculation).
* **Assumed, disclosed in the UI with measured sensitivity:** ρ/ν of seawater,
  +0.0004 roughness on the planing bottom, 0.98 shaft / 0.97 gear efficiency,
  the sea margin, transom area 9 % of B·T when blank, LCG 0.38·L_OA, chine beam
  0.88·B, shaft immersion 0.62·T, maximum diameter T + 2·clearance, 5 % allowable
  cavitation.
* **Unresolved:** B-series coefficients not checked against the primary table
  (two independent transcriptions agree term for term); Holtrop 1982/1984,
  ITTC and IACS/ABS texts not retrieved; no engine curves and no gearbox
  capacity data, so no match is *verified* and gearbox compatibility stays
  *INCONCLUSIVE*; SFC values not re-verified; no end-to-end trial validation;
  two "audit fix" comments in the delivered file were false and are corrected.

## Honest position on the application itself

The application is now internally consistent, refuses out-of-domain input with
specific messages, keeps every efficiency and margin in one place, and cannot
present a violated constraint as a compliant selection. What it cannot do — and
does not claim — is predict the resistance of a short, wide, shallow Maldivian
hull to better than screening accuracy, or verify a marine-gear capacity it has
no data for.
