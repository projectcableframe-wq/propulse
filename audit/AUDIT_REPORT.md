# Audit report — MTCC/YANMAR engine & propeller calculation sheet

**Audited artefact:** `app/yanmar_engine_propeller_selector.html` (single-file
JavaScript application, 6 227 lines, 463 kB) — the "V2 audited build" of
2026-10-19/21.
**Original, unmodified:** `legacy/work_v2_original.html` (byte-identical copy of
the uploaded file, SHA-256 in `legacy/SHA256SUMS`) and
`/home/user/backups/work_v2_original_2026-10-25.html` outside the repository.
**Audit date:** 2026-10-25. **Auditor's tools:** independent Python
re-implementation (`audit/independent/ref.py`), headless execution of the real
application (`audit/js/dump_dom.cjs`, jsdom 30), direct extraction of the
calculation core (`audit/js/dump_core.cjs`), and the manufacturer's own product
pages fetched on 2026-10-25 (`audit/yanmar_official.py`).

Every finding below states what was measured, how, and what was changed. Where
a claim could not be verified, it is listed under *unresolved* instead of being
asserted.

---

## 1. Findings, ranked by engineering impact

### F-01 (High, fixed) — a network bootstrap was still embedded in the "offline" document

The document ended with a Cloudflare challenge bootstrap:

```js
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;…}
var d=document.createElement('script');d.src='/cdn-cgi/challenge-platform/…';
```
guarded by a comment that claims *"AUDIT FIX F-01 … removed here"*. It was not
removed: loading the file created a hidden iframe and attempted to fetch a
remote script, producing a console error on every load and breaking the
offline/air-gapped guarantee the build advertises.

*Verification:* static inspection of the shipped document; the JS context of a
headless load showed the extra `<script>` and the `/cdn-cgi/` request.
*Fix:* the block is removed. Regression test `APP` group, case `APP-SELFTEST`
plus the in-app assertion "The shipped HTML has no external script and no
injected iframe" (0 external/iframe nodes).

### F-02 (High, fixed) — 6AYE-series rating attribution did not match the manufacturer's table

Stored versus published (`yanmar.com/.../6ayeseries/`, accessed 2026-10-25):

| model | stored before | published |
|---|---|---|
| 6AYEM-ET | C 555/1840, M 610/1900, **L 670/1938** | C 555/1840, **H 599/1900**, M 610/1900 |
| 6AYEM-GT | **H 599/1900, M 610/1900**, L 670/1938, S 737/2000 | **L 670/1938, S 737/2000** |
| 6AYEM-GTWS | **M 610/1900**, L 670/1938, S 749/2000 | **L 670/1938, S 749/2000** |
| 6AYEM-ETWS | *missing* | C 555/1840, M 610/1900 |

The L rating was attached to the wrong model (it belongs to the GT), the H row
was missing entirely, and two ratings were offered on configurations YANMAR
does not publish. A vessel needing ~600 kW of heavy-duty (H) power would have
been matched to a **6AYEM-GT/H**, which does not exist; and a light-duty vessel
could have been quoted a **6AYEM-ET/L**, which also does not exist.

The in-app self-test that was supposed to catch this asserted the *wrong*
table (`6AYEM-GT` must carry H/M/L/S), i.e. it codified the database error.
*Fix:* ratings re-attributed; `6AYEM-ETWS` added; the self-test replaced by
assertions against the published rows. Regression group F, cases
`ENG-RAT-6AYEM-*`.

### F-03 (High, fixed) — a rating with fabricated provenance (6AYM-WET H 485 kW)

The record carried an "AUDIT FIX D-03" comment asserting that the official
6AY-SERIES page lists **6AYM-WET H 485 kW/1900**. The page (fetched
2026-10-25) lists exactly two 6AYM-WET ratings — **C 555(755)/1840** and
**M 610(829)/1900**; the 485(659)/1900 row printed on that page belongs to
**6AYM-WST (C)**. The 485 kW "H" rating of the WET does not exist in the
source.

Consequence: an H-duty vessel around 480 kW could be offered a rating that
YANMAR does not publish. This is the most serious class of defect in an
engine-selection tool — it can reach a purchase order.

*Fix:* the rating is removed and the false provenance comment replaced by the
dated source check. Regression case `ENG-RAT-6AYM-WET`.

### F-04 (High, fixed) — engine and package masses were wrong for three families

| model | stored | published | consequence |
|---|---|---|---|
| 6AYEM-ST/ET/GT/GTWS | 2 365 kg | **2 418 kg** | mass understated by 53 kg |
| 12AYEM-ST/ET (and GT) | 4 950 kg | **4 780 kg** | mass overstated by 170 kg |
| 6HA (predecessor code 6HA2M-*) | 1 455 / 1 465 kg | **6HA3M: 1 398 / 1 448 kg** | wrong model code + mass |

The 6AY-series figure (2 365 kg) had been used for the 6AY**E** engines and the
12AY figure (4 950 kg) for the 12AY**E** engines. The installed-mass term is 12 %
of the ranking score, so this changed recommendations. The mass table now also
carries `6HA3M`, `6AYEM-ETWS` and `12AYEM-GT`.

### F-05 (Medium-high, fixed) — Savitsky mean bottom velocity used the wrong expression

Savitsky defines the mean bottom velocity from the **deadrise-corrected lift
coefficient**:

```
Vm/V = sqrt(1 - CL_beta/(lambda·cos tau)),   CL_beta = CL0 - 0.0065·beta·CL0^0.6
```

The build used only the dynamic-lift term, with the deadrise deduction applied
to that term:

```
Vm/V = sqrt(1 - (0.0120·sqrt(lambda)·tau^1.1 - 0.0065·beta·(...)^0.6)/(lambda·cos tau))
```

i.e. it dropped the hydrostatic term `0.0055·lambda^2.5/Cv^2`. On the published
check case (Shoemaker model 29) the difference is **0.9 % in Vm, 0.20 % in
friction drag** — small, but it made the implementation depart from the
published equation. *Fix:* the published form is used; the old form is
computed and reported as a sensitivity (`VmLegacy`, `dfSensitivityPct`), not
used. Regression case `SV64-*`, in-app test "Savitsky mean bottom velocity uses
the CL_beta form…".

### F-06 (Medium, fixed) — Burrill/Carmichael correlation was extrapolated outside its validity

The Carmichael correlation of Burrill's chart is quoted by its own source
(MIT OCW 2.611) as valid to *C ≈ 25 %* back cavitation. Beyond that it is
non-physical: at C = 30 % it returns a **negative** limiting thrust loading, so
the required blade-area ratio became meaningless (and, with the new guard,
infinite). The UI limits the field to 25 %, but the calculation core accepted
any value from any other caller. *Fix:* explicit refusal with a message.
Regression case `EDGE-CAVLIM`.

### F-07 (Medium, fixed) — the Savitsky trim band was only enforced for solved trims

`if(!inp.fixedTrim && (tau<2 || tau>15))` — a user-fixed trim outside 2–15°
was accepted silently, although the 2–15° band belongs to the regression
itself, not to the way the trim was obtained. *Fix:* the band is checked for
both cases and the message says when the trim was user-fixed (in which case it
is also not an equilibrium solution). Regression: in-app test "A user-fixed
trim outside the 2-15 deg band is flagged…".

### F-08 (Medium, fixed) — P/D saturation at the series boundary was invisible

Three presets place the optimum **on** the B-series pitch-ratio boundary
(speed_ferry P/D 1.398, transfer 1.392, dinghy 1.373 against a 1.40 limit).
The number was reported without comment. That is a *design* limitation, not an
arithmetic error: the required thrust cannot be met at a lower pitch, so the
diameter/clearance limit or the shaft speed is what constrains the
installation, and the predicted efficiency is an upper bound for this geometry
family. *Fix:* `PDatLimit` / `JatLimit` / `DatLimit` flags (within 1 % / 2 % of
the boundary) and a first-class assessment check "Propeller design is
boundary-limited". Regression cases `SEL-PDLIMIT-*`.

### F-09 (Medium, fixed) — unknown installed mass could score as the lightest engine

`scoreCandidate` computed `wt = c.installedMass*inp.nProps`; with
`installedMass === null` this is `0`, and the mass sub-score `1/(1+wt/6000)`
became **1.0 — the best possible score for missing data**. Reachable for any
engine whose selected gear has no published mass (e.g. 6AYEM-ST/YXH-240-7 in
the previous table). *Fix:* unknown mass is neutral (0.5) and never beats a
known-light engine. Regression: in-app test "An unknown installed mass is
neutral in ranking…" (null 68.93 < light 74.01, > heavy 64.02, wtS = 0.5).

### F-10 (Medium, fixed) — "all gates passed" was presented like "correctly sized"

A candidate that clears power, cavitation, tip speed and duty is reported with
whatever status the *method* domain gives. The `bokkura` preset returns a
25.7 kW engine at **17.2 % load** (flagged `underLoaded` internally but with no
user-facing sizing statement). A 17 %-load engine is oversized: it runs far
from its optimum, fouls earlier and burns more fuel per kWh. *Fix:* an explicit
"Engine size vs requirement" check — `PRELIMINARY ESTIMATE` below the 40 %
right-sizing band and `FAILED CONSTRAINT` below the 25 % sensible-load floor,
with wording that states YANMAR publishes no minimum continuous load, so this
is a sizing judgement and not a manufacturer limit. Regression cases
`SEL-RIGHTSIZE-*`.

### F-11 (Low, fixed) — the C_M help text described formulas the code does not use

The field help quoted three linear regressions (`0.93 + 0.07·C_B` etc.); the
code performs piecewise-linear interpolation of a per-type anchor table. The
text now describes what the code does and states the anchors.

### F-12 (Low, fixed) — 4JHYE marked unverified although it is on the current page

The model was flagged `codeVerified:false` with empty dimensions, although the
current JH SERIES page lists it (M 25.7(35)/3400, L 29.4(38)/3600, dry mass
243 kg **with** YX-10, 916×545×659). Dimensions and code status corrected; the
engine-only mass (220 kg) and the 23 kg YX-10 mass (back-calculated from the
published 243 kg package) are labelled *derived*, and the reduction ratios
remain dealer data (the page prints no ratios).

### F-16 (Medium, fixed) — the exported B-series evaluator extrapolated silently

`bSeries()` — the open-water evaluator used by charts, tests and any external
caller — accepted any argument and returned a number. At J = 1.6 it returned
**K_T = −0.247**, at J = −0.1 K_T = +0.479 and a fictitious η = 0.343 at P/D
1.6, Z = 9 or A_E/A_O = 1.2. The polynomials are a fit over J 0–1.5, P/D
0.5–1.4, A_E/A_O 0.30–1.05, Z 2–7; outside it they have no meaning. The design
solver already restricted itself internally, so no shipped result was wrong, but
anyone using the evaluator directly (the file is documented as a library-grade
single file) got nonsense.

*Fix:* `bSeries()` now refuses with the violated bound named. Regression cases
`C-BS-J`, `C-BS-PD`, `C-BS-Z`, `C-BS-EAR`.

### F-17 (Medium, fixed) — `holtropPropulsion()` returned silent NaN when given the wrong object

The function needs the **hull input** object (Lwl, B, T, vol, Cp, Cm, Cwp, lcb)
plus formK/Cf/Ca. Passing the object returned by `holtrop()` — the natural thing
to try, since it carries formK/Cf/Ca — produced `w = t = η_R = NaN`, which
propagated into brake power. Nothing raised.

*Fix:* explicit field check; the function now returns an error naming the
missing fields and stating that a `holtrop()` result is not a hull input.
Regression case `C-HM-PROP-API`.

### F-18 (Low, fixed) — Burrill's default cavitation level produced a misleading message

`burrillTauC(sigma, backCavPct)` was called with the raw argument instead of the
resolved `C` (default 5 %). With no value entered the limit evaluated to NaN and
the caller reported *"Burrill limit non-positive (super-cavitating regime)"* for
an ordinary default. *Fix:* the resolved value is used; the reason text now only
claims supercavitation when it is true. Regression case `C-BURRILL-DEF`.

### F-19 (Low, documented) — "closest available" is returned with `ok:true`

When nothing is compliant the engine returns `{ok:true, closest:true}` with the
best non-compliant candidate, `status = FAILED CONSTRAINT` and the violations
attached; the UI labels it *"Closest available engine — NOT fully compliant"*
and shows the violations. This is a deliberate contract, not a defect, but it
means **`ok` alone does not mean "safe selection"**: automation must test
`ok && !closest`. It is documented here so nobody starts an engine on it. The
audit suite asserts that a closest match always carries at least one violation
and never reports `status` other than `FAILED CONSTRAINT` (cases
`E-CLOSEST-CAV`, `E-*-STATUS`).

### F-13 (Informational) — "OUTSIDE VALIDATION DOMAIN" on every preset is *correct*

The banner is not hard-coded. It is generated from the actual domain flags,
and the flags are genuine for these hulls:

| preset | domain flags |
|---|---|
| fishing_dhoni | C_B 0.481 < 0.55; B/T 4.95 > 4.0; semi-displacement hull on a displacement regression |
| bokkura | C_B 0.45; L/B 3.41 < 3.9; B/T 5.24 |
| cargo_dhoni | L/B 3.75; B/T 4.64 |
| ferry | C_B 0.501; L/B 3.85; B/T 5.05 |
| speed_ferry / transfer / dinghy | planing: beam loading C_D > 0.20 |
| safari | L/B 3.76 |
| custom | Fn 0.424 (0.40–0.55 extension); C_B 0.502; L/B 3.75; B/T 4.94 |

**Every preset vessel is outside the Holtrop & Mennen regression data**, because
Maldivian dhonis are short, wide and shallow. That is a finding about the use
case, not about the code: for these hulls the app's resistance (and therefore
power) is an extrapolation and must be treated as a screening estimate only
(see `LIMITATIONS.md`, L-02). The tool says so; the user must read it.

### F-14 (Informational) — the propeller-law operating point is an assumption, disclosed

`solveCandidate` sets the engine speed at the service point from
`n = n_rated·(load)^(1/3)`. That ties the operating point to a cubic
propeller-law load curve rather than to a manufacturer torque curve (none is
stored) and is disclosed in the UI, the trace and `opPointBasis`. The
engineering consequence must be understood: *at a fixed ship speed an oversized
engine is allowed a slower shaft, and a slower shaft permits a larger, more
efficient propeller*, so part-load efficiency of oversized engines is
optimistic. The 36 % load-weight term in the ranking counteracts this.

### F-15 (Informational) — reference-implementation defects found in the user's forks

The forks were used as references only. Two defects are worth recording because
they will propagate to anyone reusing them:

* `holtrop-mennen/HoltropReanalysis84.py` uses `m4 = c15·0.4·exp(−0.034Fn^−3.29)`
  in the **low-speed** wave-resistance branch. Holtrop & Mennen's low-speed
  branch uses `m2 = c15·Cp²·exp(−0.1Fn^−2)`; `m4` belongs to the high-speed
  branch (`c17`, `m3`). Using `m4` there understates `R_W` by **6.3 %** at
  Fn = 0.30 (cargo-dhoni case), and also uses `λ = 1.44·Cp` instead of
  `1.446·Cp` and an exclusive `c7` boundary.
* `kcs-resistance-propulsion/wageningen.py` and
  `Wageningen-B-series-propeller-calculator/wageningen_b.py` agree with the
  audited table term for term (see `VERIFICATION.md` §4).

---

## 2. What the audit verified (no change needed)

| area | evidence |
|---|---|
| Holtrop & Mennen resistance | reproduces the paper's own numerical example: S 7 381.45 m² (exact), R_T 1 792.02 kN vs 1 793.26 (−0.07 %), R_W 556.90 vs 557.11 kN (−0.04 %), 1+k₁ 1.1564, η_R 0.9931; independent re-implementation agrees with the app to ≤0.01 % on ten hulls |
| Savitsky planing | published Shoemaker (1934) model-29 case: λ 1.587 vs 1.59, τ 4.26° vs 4.21°, D/W 0.195 vs 0.19 (18.01 kn); λ 1.575 vs 1.56 (20.92 kn) |
| Wageningen B-series | 39/47 terms; evaluation equals explicit summation to 5×10⁻⁷; η = J·K_T/(2πK_Q) identity; 0/86 coefficient mismatches against two independent transcriptions (one term differs in the 10th digit) |
| Burrill / Keller | reproduce the MIT 2.611 and ITU worked examples to 0.001 % and 0.13 % |
| Engine database | 26 models, 52 rating rows, masses, dimensions and gear ratios all match the manufacturer's pages fetched 2026-10-25 (214 checks in group F) |
| Power ledger | P_E = R_T·V_s, P_D, P_B = P_D/(η_S·η_G)(1+SM), load = P_B/P_rated, η_O = J·K_T/(2πK_Q) all close to machine precision in every preset |
| Input hygiene | Fn > 0.55, zero speed, missing operating days, no feasible propeller, out-of-validity cavitation index: all refused with a specific message; no silent defaults |

## 3. Unresolved items (not fixed, stated as limitations)

1. **B-series primary table not retrieved** (Oosterveld & van Oossanen 1975 is
   paywalled, and every open copy located returned a blocker page). The
   coefficients are verified against two independent transcriptions and the
   evaluation against published chart bands — not against the primary table.
2. **No verified engine performance curves** and **no gearbox power/torque
   capacity** exist in the database, so no match can be called verified and
   gearbox compatibility stays *INCONCLUSIVE*. Part-load fuel is an estimate.
3. **SFC values** were not re-verified in this audit (only ratings, masses,
   dimensions and gear ratios were). Several are flagged `E`/`Y B` in the data.
4. **IACS UR M68 / ABS 4-3-2 coefficients** (k = 1.22/1.26/1.0; c1 = 560/472.5/
   416.4) were checked for algebraic consistency and against secondary
   summaries, not against the rule text.
5. **Water properties** (ρ = 1025 kg/m³, ν = 1.188×10⁻⁶ m²/s) are stated
   assumptions; they move planing drag by ±1.5 %.
6. **No end-to-end validation** (model test / sea trial / CFD) of a complete
   design exists in the audit; module-level validation cannot substitute.
7. **Oortmerssen cross-check** for these hulls is almost always out of domain,
   so it does not bound the Holtrop estimate (the app says so explicitly).
