# Verified, estimated, assumed, unresolved

This is the statement the audit requires: what the tool's numbers *are*, in
four separate categories. Nothing here is a confidence percentage — such a
number would be invented.

## 1. VERIFIED — reproduced against an independent published source

| result | how it was verified |
|---|---|
| Holtrop & Mennen resistance chain (wetted surface, form factor, wave, bulb, transom, correlation allowance, total resistance, effective power) | the paper's own numerical example reproduced: S exact; R_T −0.07 %; R_W −0.04 %; 1+k₁ 1.1564; η_R 0.9931. An independent re-implementation written for this audit agrees with the app to ≤0.01 % on ten hulls |
| Savitsky planing chain (lift, deadrise correction, trim/λ equilibrium, mean bottom velocity, friction drag, total drag) | Shoemaker (1934) model-29 case as recomputed in a published SNAME paper: λ within 0.2 %, trim within 0.05°, D/W within 2.8 % (18.01 kn) and 1 % (20.92 kn) |
| ITTC-1957 friction line | closed form, 1e-9 |
| Wageningen B-series evaluation (39/47 term polynomials, J/K_T/K_Q/η identities, Reynolds-correction structure) | equals the explicit term sums; 0/86 coefficient mismatches against two independent transcriptions |
| Burrill/Carmichael and Keller cavitation criteria | reproduce the MIT 2.611 and ITU Istanbul worked examples to 0.001 % and 0.13 % |
| YANMAR ratings, masses, dimensions and gear ratios (26 models, 52 rating rows) | manufacturer product pages, fetched 2026-10-25, 214 field checks |
| Power ledger arithmetic (P_E, P_D, P_B, load, η_O) | identities closed to machine precision in every preset |
| Input guards (Fn, Re, C_P, c₅, Reynolds, speed, duty profile, cavitation index, interpolation range) | refuse with a specific message; no silent default |

## 2. ESTIMATES — computed, plausible, not validated for these vessels

* **Resistance and required power of the nine preset vessels.** Every preset is
  *outside* the Holtrop & Mennen regression range (C_B 0.45–0.50, L/B 3.4–3.9,
  B/T 4.6–5.2). The estimate is an extrapolation, flagged as such. The
  van Oortmerssen cross-check is usually out of its own range too, so it does
  not bound the answer.
* **Planing-craft resistance** where the beam loading exceeds 0.20, and for
  hulls with non-prismatic bottoms (the method assumes a prismatic, constant-
  deadrise planing surface).
* **Wake fraction, thrust deduction and η_R** from Holtrop's statistical
  formulas at a diameter that is itself a design output.
* **Operating point**: `n = n_rated·load^(1/3)` propeller-law screening, not a
  manufacturer torque curve.
* **Part-load fuel consumption** from a generic load shape applied to the rated
  SFC (or not stated at all when no rated SFC is published).
* **Shaft diameter** from the IACS/DNV/ABS rule *forms*, with a stated material
  strength; not a class calculation (no torsional vibration, alignment, keyway,
  liner or ice-class effects).
* **Propeller mass/inertia, blade thickness, skew, rake** are not modelled.

## 3. ASSUMPTIONS — stated in the tool, and their sensitivity

| assumption | default | sensitivity measured in this audit |
|---|---|---|
| Seawater ρ, ν | 1025 kg/m³, 1.188×10⁻⁶ m²/s | ±1.5 % on planing drag between plausible property sets; unverified against a specific standard |
| Roughness allowance on the planing bottom | +0.0004 on C_F | +4 % on planing drag; the published check case uses Schoenherr without it |
| Shaft / gear efficiency | 0.98 / 0.97 (editable) | 1 % → 1 % on brake power |
| Sea margin | preset value (editable) | linear on brake power |
| Immersed transom area when not entered | 9 % of B·T | +2.0 % on total resistance (cargo-dhoni case) |
| LCG when not entered | 0.38·L_OA | moves the planing equilibrium |
| Chine beam when not entered | 0.88·B | first-order on planing lift |
| Shaft immersion | 0.62·T | cavitation number |
| Maximum propeller diameter | T + 2·clearance (1.05·T if not given) | dominates the achievable η_O |
| Allowable back cavitation | 5 % (Burrill) | sets the required blade area |
| Engine mass unknown | reported as *unknown*, neutral in ranking | — |

## 4. UNRESOLVED — could not be established in this audit

1. **Oosterveld & van Oossanen (1975) primary table** not retrieved (paywall;
   every open copy returned a blocker). Coefficients are cross-verified only.
2. **Holtrop & Mennen (1982) paper PDF** not retrieved; the numerical example
   was used from a reproduction of the published procedure, and the audit's
   implementation reproduces it to 0.07 %. The remaining 0.07 % is attributed
   to the paper's rounding and to water properties, but this attribution is
   itself an inference.
3. **Holtrop 1984** and **ITTC 7.5-02-02-01/02** primary texts not retrieved;
   the forms used are those reproduced in the published per-step procedures.
4. **IACS UR M68 / ABS 4-3-2** rule text not retrieved; coefficients taken from
   secondary summaries. Do not use the shaft output for class submission.
5. **Engine performance curves and gearbox capacity** — not in the database and
   not obtainable from public pages. Gearbox compatibility stays
   *INCONCLUSIVE*; part-load fuel stays an estimate.
6. **SFC values** were not re-verified in this audit.
7. **End-to-end validation** of any single installation (model test, sea trial,
   CFD) — none exists in the repository or in this audit.
8. **YANMAR availability/certification per rating row** — the pages state
   series-level emissions; row-level certification must be confirmed with the
   dealer.
9. **The `/cdn-cgi/` bootstrap** was removed as code. Why it was there
   (a hosting artefact, an editor's paste, or an intentional challenge page) is
   unknown.
10. **Two "audit fix" comments in the delivered file asserted things that were
    not true** (F-01's removed script, F-03's 6AYM-WET H rating). Any other
    claim in those comments that this audit did not independently check should
    be treated as unverified.

## 5. What this tool must not be used for

* Class submission or contract-speed guarantees.
* Final propeller or gearbox selection without the manufacturer's curves,
  gearbox rating and a cavitation check.
* Any hull outside the stated method domains without an independent
  calculation (model test, CFD, or a validated regression for that hull family).
* Extrapolating beyond the database (25.7 kW … 1 340 kW per engine).
