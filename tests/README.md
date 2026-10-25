# Regression suite (`tests/`)

An **external** suite that runs the shipped, unmodified single-file application
in a real DOM (jsdom) and checks 126 cases. It is deliberately separate from the
application's own self-test: if the application's self-test contains a wrong
expectation, this suite still fails.

```
cd tests
npm install            # jsdom only (dev dependency; the app has no dependencies)
node run_suite.js      # exit 0 = all pass; writes tests/TEST_RESULTS.md
node run_suite.js ../app/yanmar_engine_propeller_selector.html
```

## Case classes (each row of `TEST_RESULTS.md` names its class)

| group | what it contains | acceptance |
|---|---|---|
| A | published worked examples and exact definitions: Holtrop & Mennen (1982) example, Savitsky on the Shoemaker (1934) model-29 case at two speeds, Burrill/MIT example, Keller/ITU example, B-series chart band, unit definitions, ITTC-1957 closed form | within the published rounding stated per case |
| B | analytic identities and physical invariants: η_O = J K_T/(2πK_Q), monotonicity in J and P/D, Reynolds-correction domain, propeller Reynolds number, shaft-diameter P/n scaling, σ(h), Burrill(A_E) trend | exact to floating point |
| C | out-of-validity inputs must be **refused**, not extrapolated: B-series envelope, Savitsky β and trim band, planing regime, Burrill C ≤ 25 %, ITTC Re > 0, Holtrop C_P singularity and Fn ≤ 0.55, UI input validation, API misuse | an error/refusal with a specific message |
| D | the YANMAR database against the manufacturer's pages fetched 2026-10-25 (ratings, speeds, masses, gear ratios, prohibited phantom rows, duty-definition coverage) | exact |
| E | matching-result invariants for the nine presets: power ledger closure, P_E, "violations are never presented as compliant", tip-speed gate, twin-screw sanity, P/D boundary flag, right-sizing flag, determinism | structural |
| X | document integrity: no external script, no iframe, self-test clean | exact |

`TEST_RESULTS.md` is overwritten on each run; it records measured vs expected,
the tolerance and the evidence class for every case, plus a table of
discrepancies and what each one is attributable to.

## What this suite does *not* prove

A green run means the shipped file still behaves as the audit established. It is
**not** a validation of the resistance or propulsion methods for a particular
hull; that evidence is in `../audit/VERIFICATION.md`, and the limits are stated
in `../audit/LIMITATIONS.md`.
