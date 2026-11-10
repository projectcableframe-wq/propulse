# Yanmar engine + propeller selection workbook

`Propulse_Yanmar_Propeller_Design.xlsx` is a **fully formula-driven** Excel workbook. Nothing
is pasted in as a number: change one yellow cell on sheet 1 and the resistance, the propeller,
the engine and every check follow.

It answers one question: *given this hull, this service speed and this tropical site, which
Wageningen B-series propeller and which YANMAR engine are right — and what is the arithmetic
that proves it?*

## The chain

| Sheet | Content |
|---|---|
| `0 Summary` | One page: vessel, resistance, propeller, engine, verdict |
| `1 Input` | Every input, plus the ISO 3046-1 site correction, the seawater viscosity table and the vessel-type guidance bands |
| `2 Resistance` | Holtrop & Mennen (1982) in full — loaded **and** ballast — every coefficient printed with its equation, then a 21-point speed sweep and three charts |
| `3 Propulsion` | Wake fraction, thrust deduction, relative rotative efficiency, hull efficiency, thrust, speed of advance, power balance, reasonableness bands |
| `4 Propeller` | Thrust identity solved by bisection for 31 shaft speeds (every step shown), Keller blade area, the converged pitch ratio at the selected engine speed, 9 design checks, 2 charts |
| `5 Engines` | The whole YANMAR commercial range, derated to the site, matched to the propeller at each catalogued gear ratio and ranked |
| `7 Yanmar data` | Catalogue figures as published, with derived kW/litre, kW/kg and site-corrected output |
| `8 B-series` | The 39 KT and 47 KQ polynomial coefficients, validity limits, open-water curves |
| `9 Equations` | Register of every equation used, with the sheet where it is evaluated |
| `10 Verification` | Every formula of sheets 2–4 typed again from scratch for two reference vessels and compared, cell by cell, with an independent Python implementation |

## Method and sources

* **Resistance** — Holtrop, J. & Mennen, G.G.J., *An approximate power prediction method*,
  International Shipbuilding Progress 29 (1982) 335. Includes the bulb (c2, c3, RB), the
  transom (c5, c6, RTR), the correlation allowance of the 1984 revision and the appendage
  equivalent factor (1+k2)eq.
* **Propeller** — Wageningen B-series polynomials of Oosterveld & van Oossanen (1975) as
  re-published by Bernitsas, Ray & Kinley (1981): KT = Σ C·J^s·(P/D)^t·(AE/A0)^u·Z^v, 39 + 47
  terms. Validity box enforced: 0 ≤ J ≤ 1.8, 0.30 ≤ AE/A0 ≤ 1.05, 0.50 ≤ P/D ≤ 1.40.
* **Cavitation** — Keller criterion for the minimum blade area at the true shaft immersion and
  sea-water vapour pressure, cross-checked against the Burrill 5 % back-cavitation line
  (τc ≈ 0.28·σ).
* **Interaction** — Holtrop & Mennen wake fraction, thrust deduction and relative rotative
  efficiency, with reasonableness bands flagged on sheet 3 (an expert override is available on
  sheet 1 but is never applied silently).
* **Engine rating** — ISO 3046-1:2002 / ISO 15550 power adjustment
  α = k − 0.7(1 − k)(1/ηm − 1), k = (px/pr)^m·(Tr/Tx)^n·(Tcr/Tcx)^s, with the reference
  condition 100 kPa, 25 °C, 30 % RH. The recommendation is made on the site-corrected power
  (≈ 8 % below catalogue at 35 °C air / 75 % RH / 30 °C sea water) and the derating factor is
  printed on sheet 1, sheet 5 and the summary.
* **Engines** — only YANMAR commercial marine engines, at the ratings published by YANMAR
  (`db.py` carries the model, rating letter, kW, mhp, rpm, displacement, dry mass, gearbox and
  the reduction ratios offered).

## Verification

Sheet `10 Verification` recomputes, from first principles, the resistance, the interaction
coefficients and the propeller solution for a 30 m passenger dhoni and a 48 m passenger ferry,
and compares every result with `verify_ref.py`, an independent Python implementation of the same
method. **104 comparisons, all inside 1 × 10⁻⁶ relative difference.**

The whole workbook was also recalculated head-lessly (`formulas`) for four different vessels
(speed launch, landing craft, dhoni, 60 m ferry): zero error cells in every case.

## Rebuilding

```bash
python3 -m venv .venv && .venv/bin/pip install openpyxl formulas
.venv/bin/python verify_ref.py          # writes refdata.py (independent reference values)
.venv/bin/python build.py out.xlsx      # writes the workbook
```

`build.py` prints every defined name it registers (158 of them) — the workbook is built from
named cells throughout, which is why the formulas read like the equations they implement.

## Limitations, stated openly

* Holtrop & Mennen is a displacement-hull method; it is not valid for planing craft
  (Fn > ~0.5) or for hulls far outside its regression envelope. The workbook computes anyway
  and flags the result, but for a 30-knot launch a planing method (Savitsky) or model tests are
  required.
* Single screw, fixed pitch, no duct — as specified. A ducted propeller (19A nozzle) or a
  controllable-pitch propeller needs a different open-water diagram.
* Sheet 5 reads the propeller curve with linear interpolation between 75 rev/min grid points
  (±0.5 %); the final design on sheet 4 is re-solved exactly at the selected shaft speed.
* Catalogue gear ratios are those YANMAR publishes. If none of them lands the propeller inside
  the B-series box, the workbook says so instead of inventing a ratio.
