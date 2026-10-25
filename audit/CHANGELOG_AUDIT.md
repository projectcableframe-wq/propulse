# Change log — audited build (2026-10-25)

Only `app/yanmar_engine_propeller_selector.html` was modified. The original
upload is preserved byte-for-byte as `legacy/work_v2_original.html`
(SHA-256 `6d0391318af7012c505721208ba84c0d4efa15a711ea2360492dd978ccc43960`).
Project structure and all working features are unchanged; no library, no build
step and no network dependency were introduced.

## Code and data changes

| # | area | change | reason |
|---|---|---|---|
| 1 | document | removed the injected Cloudflare challenge `<script>` at the end of the file | it created a hidden iframe and requested a remote script on every load, breaking the offline guarantee (audit F-01) |
| 2 | Savitsky | mean bottom velocity now `Vm = V·√(1 − C_Lβ/(λcosτ))` with `C_Lβ = C_L0 − 0.0065βC_L0^0.6`; the previous dynamic-lift-only expression is still evaluated as `VmLegacy` and reported as a % sensitivity | match the published equation (F-05) |
| 3 | Burrill | refuse an allowable back cavitation outside 0 < C ≤ 25 % with a specific message | the Carmichael correlation is not valid there and returns a non-physical limit (F-06) |
| 4 | Savitsky | the 2–15° trim band is now enforced for user-fixed trim as well, and the message says when the trim was fixed rather than solved | band belongs to the regression (F-07) |
| 5 | propeller | new `PDatLimit` / `JatLimit` / `DatLimit` flags (1 % / 2 % of the series boundary) and a new assessment check "Propeller design is boundary-limited" | three presets sit on the P/D = 1.40 boundary silently (F-08) |
| 6 | ranking | an unknown installed mass scores 0.5 (neutral) instead of 1.0 (best) | missing data must not win (F-09) |
| 7 | assessment | new "Engine size vs requirement" check: PRELIMINARY ESTIMATE below the 40 % right-sizing band, FAILED CONSTRAINT below the 25 % sensible-load floor | a 17 %-load engine was presented like a well-sized one (F-10) |
| 8 | engine DB | 6AYEM-ET: +H 599/1900, −L 670/1938; 6AYEM-GT: −H, −M; 6AYEM-GTWS: −M; **new** 6AYEM-ETWS (C 555/1840, M 610/1900) | ratings did not match the manufacturer's table (F-02) |
| 9 | engine DB | 6AYM-WET: removed the H 485/1900 rating and the comment that asserted it was published | the rating does not exist; the comment was false (F-03) |
| 10 | engine DB | masses: 6AYE 2 365 → 2 418 kg; 12AYE 4 950 → 4 780 kg; added 6HA3M, 6AYEM-ETWS, 12AYEM-GT | wrong family masses (F-04) |
| 11 | engine DB | 6HA2M-WHT/WDT renamed 6HA3M-WHT/WDT with 1 398 / 1 448 kg; rating-definition keys renamed | current product code (F-04) |
| 12 | engine DB | 4JHYE: code verified, dimensions 916×545×659, YX-10 mass 23 kg (derived from the published 243 kg package), gear ratios still flagged dealer data | the model is on the current page (F-12) |
| 13 | UI text | C_M help now describes the piecewise-linear anchor interpolation the code actually performs | the old text described three linear regressions that were never implemented (F-11) |
| 14 | in-app tests | replaced the 6AYE assertions that codified the wrong table; added 19 assertions: Shoemaker 1934 case (λ, τ, D/W), Vm basis, fixed-trim band, Burrill domain, installed-mass neutrality, engine-database consistency (torque, displacement from bore×stroke, provenance codes, rating-definition mapping, shaft-speed reachability), IACS/ABS shaft forms, offline guarantee | make the fixes regression-proof (see TEST_REPORT) |
| 16 | B-series evaluator | `bSeries()` refuses J outside 0–1.5, P/D outside 0.5–1.4, A_E/A_O outside 0.30–1.05, non-integer or out-of-range Z, non-positive Rn, naming the violated bound | the polynomials are a curve fit; at J = 1.6 they return K_T = −0.247 (F-16) |
| 17 | API | `holtropPropulsion()` validates its hull-input fields and returns an error instead of NaN when handed a `holtrop()` result | silent NaN that propagated into brake power (F-17) |
| 18 | Burrill | the limiting thrust loading is evaluated with the resolved permissible cavitation (default 5 %), not the raw argument | a missing value produced NaN and a misleading "super-cavitating regime" message (F-18) |
| 19 | Savitsky core | deadrise 0–30°, positive displacement/beam/speed/LCG enforced in the primitive as well as in the UI, and `trimOutOfBand` recorded | the primitive is callable on its own (F-15/S-03) |
| 20 | benchmarks | added four published Savitsky cases (Shoemaker 1934 via SNAME 2016) to the in-app benchmark registry | the previous planing benchmark used a fixed 4° trim from a calculator reproduction, not a published validation case |

## Files added (audit deliverables)

```
audit/AUDIT_REPORT.md          findings ranked by severity, with evidence and fixes
audit/VERIFICATION.md          formula-by-formula verification against sources
audit/ENGINE_DATABASE.md       YANMAR database verification, discrepancies, ambiguities
audit/MATCHING.md              matching results + rejection tally for the 9 presets
audit/TEST_REPORT.md           443-case regression report (generated)
audit/LIMITATIONS.md           verified / estimated / assumed / unresolved
audit/CHANGELOG_AUDIT.md       this file
audit/README.md                install, run, acceptance criteria
audit/run_audit_tests.py       the suite
audit/match_report.py          generates MATCHING.md
audit/extract_scripts.py       splits the HTML into script blocks
audit/independent/ref.py       independent ITTC-57 / Holtrop / Savitsky implementation
audit/yanmar_official.py       manufacturer data transcribed 2026-10-25
audit/js/dump_core.cjs         headless calculation-core dump
audit/js/dump_dom.cjs          headless whole-application dump (jsdom)
tests/run_suite.js             external 126-case conformance suite (jsdom)
tests/TEST_RESULTS.md          its result table (generated)
tests/README.md                how to run it and what it does not prove
patches/patch1..5.py           every patch applied to the HTML, replayable and
                               asserted (each replacement checks its match count)
legacy/work_v2_original.html   the untouched upload
legacy/SHA256SUMS              its hash
```

## Compatibility

* The HTML remains a single self-contained file; open it directly in a browser.
* All input fields, presets, reports, charts and exports behave as before; the
  only visible differences are the new disclosure rows/checks (boundary-limited
  propeller, right-sizing) and corrected engine records.
* No engine record was added or removed except the four documented rating
  corrections and the new `6AYEM-ETWS`.
