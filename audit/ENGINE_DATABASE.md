# YANMAR engine database — verification

Every engine record in `app/yanmar_engine_propeller_selector.html` was compared,
field by field, with the manufacturer's own product page fetched on **2026-10-25**.
The transcription of those pages lives in `audit/yanmar_official.py`, so the
comparison is reproducible (`run_audit_tests.py`, group F: 214 cases).

Fields checked: rating letter, rated power [kW(mhp)], rated speed, dry mass and
its basis (with or without marine gear), dimensions L×W×H, marine-gear model,
reduction ratios, gear mass, cylinder geometry and displacement.


## 1. Verified records

| model | ratings (letter, kW@rpm) | published mass | dims L×W×H | gear (ratios) | source page |
|---|---|---|---|---|---|
| 4JHYE | M 25.7@3400, L 29.4@3600 | 220 kg engine only; 243 kg with YX-10 (published) | 916×545×659 | YX-10 (2.54/3.13/3.5) | jhseries/ |
| 4CHE3 | M 57.4@2550, L 62.5@2600 | 570 kg with YX-30-2 | 1258×688×1022 | YX-30-2 (2.03/2.55/2.96/3.48) | cheseries/ |
| 6CHE3 | M 84.6@2550, L 95.6@2600 | 700 kg with YX-30-2 | 1496×690×1018 | YX-30-2 (2.03/2.55/2.96/3.48) | cheseries/ |
| 6CH-HTE3 | M 125.0@2550, L 140.0@2600 | 795 kg with YX-50S-4 | 1575×736×1096 | YX-50S-4 (2.03/2.48/2.88); YX-71-4 (3.53) | cheseries/ |
| 6CH-WDTE | M 154.0@2550, L 169.0@2600 | 900 kg with YX-71-4 | 1600×736×1096 | YX-71-4 (2.07/2.58/2.91/3.53) | cheseries/ |
| 6CH-WUTE | M 188.0@2550, L 206.0@2600 | 940 kg with YK-71-4 | 1600×736×1096 | YX-71-4 (2.07/2.58/2.91/3.53) | cheseries/ |
| 6CXBM-GT | H 265.0@2400, M 294.0@2500, L 341.0@2700, S 374.0@2700 | 856 kg without gear | 1390×901×989 | YX-80 (2.07/2.58/2.91) | cxbseries/ |
| 6HA3M-WHT | H 204.0@1880, M 257.0@1950 | 1398 kg without gear | 1585×1016×1260 | YX-120 (2.03/2.57/3.04/3.55); YX-120L (4/4.59) | haseries/ |
| 6HA3M-WDT | M 298.0@1950 | 1448 kg without gear | 1585×1036×1260 | YX-120 (2.03/2.57/3.04); YX-120L (3.46/4/4.59) | haseries/ |
| 6HYM-WET | H 368.0@1950, M 441.0@2100, L 478.0@2150, S 515.0@2200 | 1385 kg without gear | 1556×1014×1133 | YXH-160 (1.97/2.46/3.05); YXH-130 (2.03/2.57/3.04); YX-161L (3.65/4.08/4.55) | hyseries/ |
| 6GY135W | C 372.0@1800, H 447.0@1800, M 522.0@2100, L 559.0@2100, S 599.0@2100 | 1825 kg without gear | 1645×1055×1254 | YXH-160-7 (1.97/2.46/3.05/3.24) | 6gy135w/ |
| 6AYM-WST | C 485.0@1900 | 2365 kg without gear | 2000×1305×1431 | YX-181 (2.08/2.55/3.03); YX-180L (3.5/4/4.54) | 6ayseries/ |
| 6AYM-WET | C 555.0@1840, M 610.0@1900 | 2365 kg without gear | 2000×1305×1431 | YXH-240 (1.95/2.27/2.56/3.03/3.48) | 6ayseries/ |
| 6AYM-WGT | L 670.0@1938 | 2365 kg without gear | 2000×1305×1431 | YXH-240 (1.95/2.27/2.56/3.03/3.48) | 6ayseries/ |
| 6AYAM-ET | C 555.0@1840 | 2295 kg without gear | 1949×1274×1544 | YXH-240 (1.95/2.27/2.56/3.03/3.48) | 6ayseries/ |
| 6AYEM-ST | C 485.0@1900 | 2418 kg without gear | 2000×1305×1431 | YXH-240-7 (1.95/2.27/2.56/3.03/3.48) | 6ayeseries/ |
| 6AYEM-ET | C 555.0@1840, H 599.0@1900, M 610.0@1900 | 2418 kg without gear | 2000×1305×1431 | YXH-240-7 (1.95/2.27/2.56/3.03/3.48) | 6ayeseries/ |
| 6AYEM-GT | L 670.0@1938, S 737.0@2000 | 2418 kg without gear | 2000×1305×1431 | YXH-240-7 (1.95/2.27/2.56/3.03/3.48) | 6ayeseries/ |
| 6AYEM-GTWS | L 670.0@1938, S 749.0@2000 | 2418 kg without gear | 2000×1305×1431 | YXH-240-7 (1.95/2.27/2.56/3.03/3.48) | 6ayeseries/ |
| 6AYEM-ETWS | C 555.0@1840, M 610.0@1900 | 2418 kg without gear | 2000×1305×1431 | YXH-240-7 (1.95/2.27/2.56/3.03/3.48) | 6ayeseries/ |
| 12AYM-WST | H 882.0@1850, H 1030.0@1900 | 4950 kg without gear | 2743×1642×1707 | YHX-500-1 (2.53/3.04/3.48); YHX-500L-1 (3.57/4.07/4.48/4.96) | 12ayseries/ |
| 12AYM-WET | H 1140.0@1840, M 1220.0@1900 | 4950 kg without gear | 2743×1642×1707 | YHX-500-1 (2.53/3.04/3.48); YHX-500L-1 (3.57/4.07/4.48/4.96) | 12ayseries/ |
| 12AYM-WGT | L 1340.0@1940 | 4950 kg without gear | 2743×1642×1707 | YHX-500-1 (2.53/3.04/3.48); YHX-500L-1 (3.57/4.07/4.48/4.96) | 12ayseries/ |
| 12AYEM-ST | C 1030.0@1800 | 4780 kg without gear | 2743×1649×1707 | YHX-500-3 (2.53/3.04/3.48); YHX-500L-3 (3.57/4.07/4.48/4.96) | 12ayeseries/ |
| 12AYEM-ET | H 1140.0@1840, M 1220.0@1900 | 4780 kg without gear | 2743×1649×1707 | YHX-500-3 (2.53/3.04/3.48); YHX-500L-3 (3.57/4.07/4.48/4.96) | 12ayeseries/ |
| 12AYEM-GT | L 1340.0@1940 | 4780 kg without gear | 2743×1649×1707 | YHX-500-3 (2.53/3.04/3.48); YHX-500L-3 (3.57/4.07/4.48/4.96) | 12ayeseries/ |

## 2. Discrepancies found and corrected in this audit

| # | model | field | stored before | published | action |
|---|---|---|---|---|---|
| D-11 | 6AYEM-ET | ratings | C 555/1840, M 610/1900, **L 670/1938** | C 555/1840, **H 599/1900**, M 610/1900 | H added, L removed |
| D-11 | 6AYEM-GT | ratings | **H 599/1900, M 610/1900**, L 670/1938, S 737/2000 | L 670/1938, S 737/2000 | H and M moved to the ET |
| D-11 | 6AYEM-GTWS | ratings | **M 610/1900**, L 670/1938, S 749/2000 | L 670/1938, S 749/2000 | M removed |
| D-11 | 6AYEM-ETWS | record | *absent* | C 555/1840, M 610/1900 | record added |
| D-14 | 6AYM-WET | ratings | C 555/1840, **H 485/1900**, M 610/1900 | C 555/1840, M 610/1900 | H 485 removed — **it is 6AYM-WST's C rating**, not a WET rating; the comment asserting the opposite was fabricated |
| D-15 | 6AYEM-ST/ET/GT/GTWS | dry mass | 2 365 kg | **2 418 kg** | corrected (the 2 365 kg figure is the 6AY series) |
| D-15 | 12AYEM-ST/ET (+GT) | dry mass | 4 950 kg | **4 780 kg** | corrected (4 950 kg is the 12AY series) |
| D-16 | 6HA2M-WHT / 6HA2M-WDT | model code, mass | 6HA2M-*, 1 455 / 1 465 kg | **6HA3M-***, 1 398 / 1 448 kg | current product code and mass; the predecessor designation is noted in the record |
| D-17 | 4JHYE | code status, dims, mass | unverified, dims empty, mass 220 kg (basis unstated) | listed; 916×545×659 with YX-10; 243 kg **with** YX-10 | code verified, dimensions added, engine-only mass kept as dealer data, YX-10 mass 23 kg derived from 243−220 and flagged |

## 3. What the database still does not contain (and cannot claim)

* **No engine performance or torque curves.** The service point is a
  propeller-law screening point (`n = n_rated·load^(1/3)`), not a
  manufacturer-verified operating point. Part-load fuel is a generic-shape
  estimate from the rated-point SFC.
* **No gearbox power/torque capacity limits.** Gear *ratios* and *masses* are
  verified; the ability of a gear to transmit a given power is **not** checked,
  so gearbox compatibility is reported as *INCONCLUSIVE*.
* **SFC values were not re-verified in this audit.** Many are flagged `Y B`
  (brochure) or `E` (estimated) in the data; the UI labels them accordingly.
* **Certification statements** are transcribed from the series pages
  ("IMO Tier II", "EPA Tier III", …) and refer to the series, not necessarily
  to the exact rating row.
* **Availability** (still in production?) is not established; several records
  are legacy/pre-Tier engines.

## 4. Mass basis — a trap the tool now handles explicitly

YANMAR publishes the CHE-series mass **including** the marine gear (e.g.
4CHE3: "dry mass (with marine gear) 570 kg") but the AY-series mass
**excluding** it (2 418 kg "without marine gear"). Adding the gear mass to the
CHE figure double-counts the gearbox. The database therefore stores the
published package mass in `withGear` (570 / 700 / 795 / 900 / 940 kg) and uses
it directly, while engines published without gear are summed with the
separately published gear mass. When a gear with no published mass is chosen,
the installed mass is reported as unknown (`null`) instead of guessed — and
missing mass no longer scores as the *best* mass in the ranking (AUDIT_REPORT
F-09).

## 5. Residual ambiguities in the source data

* **6CH-WUTE package mass.** The CHE-series page prints two package masses for
  the WUTE column (900 kg with YK-71-4 and 940 kg with YK-71-4) and the gear
  table lists YX-71-4 with a 120 kg and a 270 kg dry weight in different rows.
  The database stores 940 kg for the YX-71-4 package used in matching; this is
  the largest of the published values, i.e. conservative for mass, but the
  exact gear-to-mass pairing is **not resolved by the page**. Confirm with the
  dealer for a real installation.
* **6AYE gear-to-rating pairing.** YANMAR publishes YXH-240-7 (632 kg) for the
  whole 6AYE series; the 6AY-series page lists 365 kg for the WET C-rating and
  632 kg for the M-rating. The database uses the M-rating (heavier) value.
* **CHE series "without gear" masses** used when a gear other than the
  published package is selected are back-calculated (package minus gear mass)
  and are labelled *estimated* at run time.
