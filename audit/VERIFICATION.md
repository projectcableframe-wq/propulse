# Formula-by-formula verification

Legend — **V** verified against a source that is independent of this code base;
**C** cross-checked (two independent implementations agree, primary source not
retrieved); **I** internally consistent (identity/algebra only); **U** not
verified.

Tolerances in `audit/run_audit_tests.py` follow the evidence: primary worked
examples 2 % (paper rounding), chart readings 1–4 %, implementation-to-
implementation 0.5–1 %.

## 1. Resistance — Holtrop & Mennen (1982) with the 1984 re-analysis

Source: Holtrop, J. & Mennen, G.G.J. (1982) *An approximate power prediction
method*, International Shipbuilding Progress **29**(335) 166–170; Holtrop, J.
(1984) *A statistical re-analysis of resistance and propulsion data*, ISP
**31**(363) 272–276. The primary paper PDF could not be retrieved during this
audit (publisher paywall; the DTIC copy was under maintenance), so the
reference values used are the paper's own numerical example as reproduced in the
published per-step procedure and in two independent sources.

| # | quantity | expression as implemented | status | evidence |
|---|---|---|---|---|
| 1 | Wetted surface | S = L(2T+B)√C_M·(0.453+0.4425C_B−0.2862C_M−0.003467B/T+0.3696C_WP)+2.38A_BT/C_B | **V** | reproduces 7 381.45 m² of the paper's example exactly |
| 2 | Friction line | ITTC-1957 C_F = 0.075/(log₁₀Re−2)² | **V** | closed form; 5 cases to 1e-9 |
| 3 | Reynolds number | Re = V·L/ν | **I** | — |
| 4 | Form factor | c₁₂ three branches; 1+k₁ = c₁₃·(0.93+c₁₂(B/L_R)^0.92497(0.95−C_P)^−0.521448(1−C_P+0.0225lcb)^0.6906) with L_R = L(1−C_P+0.06C_P·lcb/(4C_P−1)) | **V** | 1.1564 vs 1.156 published. Note: using B/L instead of B/L_R gives 1.012 (−12 %) — a common transcription error; the app is correct |
| 5 | Appendage drag | R_APP = ½ρV²S_APP(1+k₂)C_F | **I** | consistent with HM82 form |
| 6 | Wave resistance, Fn ≤ 0.40 | R_W = c₁c₂c₅∇ρg·exp[m₁Fn^−0.9+m₂cos(λFn^−2)], m₂ = c₁₅C_P²exp(−0.1Fn^−2) | **V** | 556.90 kN vs 557.11 (0.04 %). *The low-speed branch uses **m₂**, not m₄* — see AUDIT_REPORT F-15 |
| 7 | Wave resistance, Fn ≥ 0.55 | R_W = c₁₇c₂c₅∇ρg·exp[m₃Fn^−0.9+m₄cos(λFn^−2)], m₄ = 0.4c₁₅exp(−0.034Fn^−3.29) | **C** | no published numeric case at Fn ≥ 0.55 was available; formula structure agrees with two independent sources |
| 8 | Blend 0.40 < Fn < 0.55 | R_W = R_WA(0.40)+(10Fn−4)(R_WB(0.55)−R_WA(0.40))/1.5 | **C** | as published in the per-step procedure |
| 9 | c₁, c₂, c₃, c₅, c₇, c₁₅, c₁₆, c₁₇, m₁, m₃, i_E, λ | as published, including the three c₇ branches and the 512/1 727 c₁₅ branches | **C** | coefficients reproduced in the paper's example and matched by the independent implementation |
| 10 | Bulb resistance | R_B = 0.11e^(−3P_B^−2)F_ni³A_BT^1.5ρg/(1+F_ni²) | **C** | 49.19 kN in the example; independent implementation agrees |
| 11 | Transom resistance | R_TR = ½ρV²A_T·c₆, c₆ = 0.2(1−0.2F_nT), F_nT = V/√(2gA_T/(B+B·C_WP)) | **V** | this was the one term where the *audit's first* independent implementation disagreed with the app (by 52 %); the error was in the audit code (it used Fn instead of F_nT). Recorded because it shows how a plausible-looking term can hide a 50 % error |
| 12 | Correlation allowance | C_A = 0.006(L+100)^−0.16−0.00205+0.003√(L/7.5)C_B⁴c₂(0.04−c₄), c₄ = min(T_F/L, 0.04) | **C** | example gives 0.000352; app 0.0003525 |
| 13 | Air resistance | R_air = ½ρV²A_airC_air | **I** | optional, default off |
| 14 | Total & effective power | R_T = R_F(1+k₁)+R_APP+R_W+R_B+R_TR+R_A(±air); P_E = R_T·V | **V** | 1 792.02 kN vs 1 793.26 (−0.07 %); P_E 23 047 kW vs 23 063 (−0.07 %) |

**Residual difference (0.07 %, 1.2 kN).** The app and the independent
implementation agree to 0.005 % on the same inputs, so the 1.2 kN is *not* an
implementation error: it is the paper's own rounding (its published component
values are given to 0.01 kN and 4–5 significant digits) plus the water
properties used (ρ = 1025, ν = 1.188×10⁻⁶ vs the paper's 15 °C seawater).
It is reported, not hidden.

## 2. Resistance — Savitsky (1964) planing

Source: Savitsky, D. (1964) *Hydrodynamic design of planing hulls*, Marine
Technology **1**(1) 71–95; independent published application: Alourdas, P.G.
*Planing hull resistance calculation — the CAHI method*, SNAME Greek Section,
13 Oct 2016, which recomputes Shoemaker's 1934 model 29 with Savitsky's method.

| # | quantity | expression | status | evidence |
|---|---|---|---|---|
| 15 | Speed coefficient | C_V = V/√(g·b) | **V** | C_V 4.641 matches the published 4.64 |
| 16 | Lift coefficient, flat | C_L0 = τ^1.1(0.012√λ+0.0055λ^2.5/C_V²), **τ in degrees** | **V** | reproduces the published λ–τ pair. (Using τ in radians, as the audit's first attempt did, makes the problem unsolvable — a good illustration of a silent unit trap) |
| 17 | Deadrise correction | C_Lβ = C_L0−0.0065βC_L0^0.6 | **V** | as above |
| 18 | Lift equilibrium | W = ½ρV²b²C_Lβ | **I** | by construction |
| 19 | Centre of pressure | C_OP = λ(0.75−1/(5.21C_V²/λ²+2.39)); balance C_OP = LCG/b | **V** | τ 4.26° vs 4.21°, λ 1.587 vs 1.59 |
| 20 | Mean bottom velocity | V_m = V√(1−C_Lβ/(λcosτ)) | **V** | F-05; KTH (diva2:1033545) reproduces the same relation |
| 21 | Wetted area / friction | S_b = λb²/cosβ; Re = V_m·λb/ν; C_F = ITTC-57 + 0.0004 | **C** | D/W 0.195 vs 0.19 (2.8 %). The difference is dominated by the friction-line choice (Schoenherr in the source) — the audit's own implementation with the same allowance agrees to <0.5 % |
| 22 | Total drag | D = W·tanτ + D_f/cosτ (R_T reported with appendage/air terms) | **V** | as above |
| 23 | Validity gates | C_V 0.6–13, τ 2–15°, λ ≤ 4, β 0–30°, Fn_vol ≥ 1, beam loading C_D ≤ 0.20 | **C** | gates match the published validity statements; the app refuses or flags outside them |

## 3. Propulsion coefficients and power ledger

| # | quantity | expression | status | evidence |
|---|---|---|---|---|
| 24 | Wake fraction / thrust deduction / η_R | Holtrop single- and twin-screw forms with the D, C_P, C_V, lcb, C_stern and bulb dependencies | **C** | η_R 0.9931 reproduced for the paper's example; the D used is the maximum allowable diameter (documented). Coefficient clamping outside the physical range rejects the candidate |
| 25 | Thrust identity | T_req = R_T/((1−t)·n_props) | **I** | — |
| 26 | Advance ratio / coefficients | J = V_A/(nD), K_T = T/(ρn²D⁴), K_Q = Q/(ρn²D⁵) | **I** | propeller geometry is solved so that K_T·ρn²D⁴ equals T_req to machine precision |
| 27 | Open-water efficiency | η_O = J·K_T/(2πK_Q) | **I** | identity holds in every case (1e-12) |
| 28 | Hull efficiency | η_H = (1−t)/(1−w) | **I** | — |
| 29 | Delivered / brake power | P_D = 2πnQ/η_R; P_B = P_D/(η_S·η_G)·(1+SM) | **I** | ledger closed in all 9 presets (0.01 %) |
| 30 | Load | load = P_B/P_rated | **I** | exact |
| 31 | Shaft sizing | IACS UR M68: d = 100k(P/n)^{1/3}(560/(Rm+160))^{1/3}, k = 1.22/1.26/1.0; ABS 4-3-2 with c1 = 560/472.5/416.4 by rule length | **C** | reproduces the hand calculation exactly; **rule text not retrieved** → the status "estimated rule form" is correct |

## 4. Wageningen B-series

| # | check | result |
|---|---|---|
| 32 | Polynomial size | 39 K_T terms, 47 K_Q terms (Oosterveld & van Oossanen 1975) — **V** (table structure) |
| 33 | Coefficient values | 0/86 mismatches against `Wageningen-B-series-propeller-calculator/wageningen_b.py`; 1/86 against `kcs-resistance-propulsion/wageningen.py` (K_Q term 46: −0.0004659 vs −0.000465899, i.e. 1×10⁻⁹) — **C** |
| 34 | Evaluation | equals the explicit 39/47-term sum to ≤5×10⁻⁷ (K_T) and ≤5×10⁻⁸ (K_Q) for every test point — **I** |
| 35 | Reynolds correction | ΔK_T, ΔK_Q polynomials with c₀.₇₅ = 2.073(A_E/A_O)D/Z and the log₁₀Re−0.301 argument; zero at Re = 2×10⁶ — **C** (formula structure only; no primary numeric case) |
| 36 | Published chart band | B4-70, J = 0.5, P/D = 1.0: K_T 0.271 (chart band 0.26–0.28), 10K_Q 0.434 (0.42–0.45) — **C** (chart reading, not a coefficient proof) |
| 37 | Series validity | Z 2–7, P/D 0.5–1.4, A_E/A_O 0.30–1.05, J 0–1.5, standard A_E/A_O sets per Z; boundary contact is flagged (F-08) — **V** (series definition) |
| 38 | Propeller search | D and P/D solved so that thrust matches; cavitation (Burrill τ via Carmichael, Keller minimum area) and tip speed gated; rejection reasons recorded — **I** plus **V** for the cavitation correlations (below) |

## 5. Cavitation criteria

| # | quantity | expression | status | evidence |
|---|---|---|---|---|
| 39 | Cavitation number | σ₀.₇R = (p₀−p_v)/(½ρ(V_A²+(0.7πnD)²)), p₀ = p_atm+ρgh | **V** | as published (MIT OCW 2.611) |
| 40 | Burrill limit | τ_c = C(0.0305σ^0.2−0.0174)+0.523σ^0.2−0.3064 | **V** | τ_c 0.200002 vs 0.2 published (0.001 %); valid 0 < C ≤ 25 % (guard added, F-06) |
| 41 | Required area | A_P = T/(½τ_cρV_R²); A_E = A_P(1.067−0.229P/D) | **V** | as published |
| 42 | Keller | A_E/A_O ≥ (1.3+0.3Z)T/((p₀−p_v)D²)+K, K = 0–0.20 by blade number and screw count | **V** | 0.6789 vs 0.678 published (0.13 %) |

## 6. Validity guards (checked as refusals, not numbers)

| # | guard | implemented as | status | evidence |
|---|---|---|---|---|
| 43 | B-series envelope | J 0–1.5, P/D 0.5–1.4, A_E/A_O 0.30–1.05, Z 2–7, Rn > 0; refused with the bound named | **V** (series definition) | `C-BS-*` |
| 44 | Savitsky domain | C_V 0.6–13, β 0–30°, τ 2–15°, λ ≤ 4, Fn_vol ≥ 1, C_D ≤ 0.20 | **C** | `C-SV-*`, `EDGE-*` |
| 45 | Burrill correlation | 0 < C ≤ 25 %; a missing C resolves to 5 % | **V** | `C-BURRILL-30`, `C-BURRILL-DEF` |
| 46 | Holtrop domain | Fn ≤ 0.55 hard, 0.40–0.55 flagged as the interpolated extension; C_P singularity refused; C_B/L/B/B/T outside the regression range flagged | **V** (regression ranges) | `C-HM-*`, `E-*` |
| 47 | API misuse | `holtropPropulsion` refuses a `holtrop()` result instead of returning NaN | **I** | `C-HM-PROP-API` |
| 48 | Closest-match honesty | a non-compliant fallback always carries violations and `status = FAILED CONSTRAINT`, never a compliant label | **I** | `E-CLOSEST-CAV`, `E-*-STATUS` |

## 7. Engine data

See `ENGINE_DATABASE.md`: 26 models / 52 rating rows / masses / dimensions /
gear ratios, 214 checks, all passing against the manufacturer's pages fetched
2026-10-25.

## 7. Reproducing these results

```
python3 audit/run_audit_tests.py        # 443 cases, writes audit/TEST_REPORT.md
python3 audit/match_report.py           # writes audit/MATCHING.md
python3 audit/independent/ref.py        # the two published benchmark values
```
