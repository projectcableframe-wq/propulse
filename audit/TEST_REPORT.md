# Audit test report — YANMAR / PROPULSE selection sheet

Generated 2026-10-26 by `audit/run_audit_tests.py`.

**443 cases, 443 pass, 0 fail.**

## A published benchmark — 15 cases, 15 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| HM82-RT | Holtrop & Mennen resistance — Total resistance RT | 1792.0164 | 1793.2600 | 2 % (err -0.069%) | PASS | Holtrop & Mennen, ISP 29(335), 1982, numerical example p.170 (International Shipbuilding Progress 29 (1982)) |
| HM82-RW | Holtrop & Mennen wave resistance — Wave resistance RW | 556.9037 | 557.1100 | 2 % (err -0.037%) | PASS | Holtrop & Mennen, ISP 29(335), 1982, p.170 (International Shipbuilding Progress 29 (1982)) |
| HM82-K1 | Holtrop form factor — Form factor (1+k1) | 1.1564 | 1.1560 | 1 % (err +0.038%) | PASS | Holtrop & Mennen, ISP 29(335), 1982, p.170 (International Shipbuilding Progress 29 (1982)) |
| HM82-ETAR | Holtrop relative rotative efficiency — etaR | 0.9931 | 0.9931 | 0.5 % (err -0.002%) | PASS | Holtrop & Mennen, ISP 29(335), 1982, p.170 (International Shipbuilding Progress 29 (1982)) |
| SV64-LAM | Savitsky planing (fixed trim) — Mean wetted-length ratio lambda (lm = 5.50 m) | 1.7187 | 1.7190 | 2 % (err -0.015%) | PASS | Savitsky (1964) relations; worked example as reproduced by NauticalSolver Savitsky calculator (Marine Technology (1964) / worked-example reproduction) |
| SV64-SH18-LAM | Savitsky planing (equilibrium trim) — mean wetted-length ratio lambda | 1.5867 | 1.5900 | 2 % (err -0.207%) | PASS | Alourdas, SNAME Greek Section, Oct 2016 (Savitsky recomputation of Shoemaker 1934 model 29) (SNAME Greek Section (2016)) |
| SV64-SH18-TRIM | Savitsky planing (equilibrium trim) — running trim tau | 4.2599 | 4.2100 | 3 % (err +1.186%) | PASS | Alourdas, SNAME Greek Section, Oct 2016 (SNAME Greek Section (2016)) |
| SV64-SH18-DW | Savitsky planing drag — drag / weight D/W | 0.1952 | 0.1900 | 10 % (err +2.758%) | PASS | Alourdas, SNAME Greek Section, Oct 2016 (SNAME Greek Section (2016)) |
| SV64-SH21-LAM | Savitsky planing (equilibrium trim) — mean wetted-length ratio lambda | 1.5748 | 1.5600 | 2 % (err +0.946%) | PASS | Alourdas, SNAME Greek Section, Oct 2016 (SNAME Greek Section (2016)) |
| BURRILL-MIT | Burrill thrust-loading limit (Carmichael correlation) — tau_c | 0.2000 | 0.2000 | 1 % (err +0.001%) | PASS | MIT OCW 2.611 Marine Power & Propulsion cavitation notes (Carmichael correlation worked example) (MIT OpenCourseWare 2.611 (2006)) |
| KELLER-ITU | Keller minimum blade-area ratio — EAR required | 0.6789 | 0.6780 | 1 % (err +0.128%) | PASS | ITU Istanbul, Examples for Application of Burrill's and Keller's Criteria (worked example) (Istanbul Technical University course notes) |
| WB75-KT | Wageningen B-series KT/KQ — KT (published chart band 0.26-0.28) | 0.2710 | 0.2700 | 4 % (err +0.382%) | PASS | Oosterveld & van Oossanen, ISP 22(251), 1975; Carlton Table 6.6 chart band (International Shipbuilding Progress 22 (1975)) |
| PROP-ID | Propeller thrust identity — Tcheck vs required T | 20000.0000 | 20000 | 0.1 % (err +0.000%) | PASS | Definition KT = T/(rho n^2 D^4) — solver self-closure (implementation check only) (Oosterveld & van Oossanen (1975) definitions) |
| UNIT-KN | Unit conversion — KNOT constant | 0.5144 | 0.5144 | 0 % (err +0.000%) | PASS | SI / international nautical mile definition (1852 m exactly) |
| UNIT-PS | Unit conversion — PS factor | 0.7355 | 0.7355 | 0 % (err +0.000%) | PASS | Metric horsepower definition 75 kgf m/s (0.73549875 kW exactly) |

## B Holtrop vs independent — 40 cases, 40 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| HT-S-HM82-PAPER | HM82-PAPER: wetted surface S | 7381.4491 | 7381.4491 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-HM82-PAPER | HM82-PAPER: total resistance | 1.792e+06 | 1.792e+06 | 0.5 % (err -0.004%) | PASS | independent re-implementation |
| HT-RW-HM82-PAPER | HM82-PAPER: wave resistance | 5.569e+05 | 5.569e+05 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-HM82-PAPER | HM82-PAPER: form factor | 1.1564 | 1.1564 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-cargo_dhoni | cargo_dhoni: wetted surface S | 188.8849 | 188.8849 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-cargo_dhoni | cargo_dhoni: total resistance | 14500.3989 | 14501.2416 | 0.5 % (err -0.006%) | PASS | independent re-implementation |
| HT-RW-cargo_dhoni | cargo_dhoni: wave resistance | 5685.3020 | 5685.3020 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-cargo_dhoni | cargo_dhoni: form factor | 1.2888 | 1.2888 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-ferry | ferry: wetted surface S | 253.5502 | 253.5502 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-ferry | ferry: total resistance | 25539.1364 | 25540.4678 | 0.5 % (err -0.005%) | PASS | independent re-implementation |
| HT-RW-ferry | ferry: wave resistance | 11660.5718 | 11660.5718 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-ferry | ferry: form factor | 1.3001 | 1.3001 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-tanker-like | tanker-like: wetted surface S | 7702.2131 | 7702.2131 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-tanker-like | tanker-like: total resistance | 5.556e+05 | 5.556e+05 | 0.5 % (err -0.005%) | PASS | independent re-implementation |
| HT-RW-tanker-like | tanker-like: wave resistance | 51787.8629 | 51787.8629 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-tanker-like | tanker-like: form factor | 1.3628 | 1.3628 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-container | container: wetted surface S | 4263.3221 | 4263.3221 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-container | container: total resistance | 3.903e+05 | 3.903e+05 | 0.5 % (err -0.008%) | PASS | independent re-implementation |
| HT-RW-container | container: wave resistance | 55043.4473 | 55043.4473 | 1 % (err -0.000%) | PASS | independent re-implementation |
| HT-K1-container | container: form factor | 1.1578 | 1.1578 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-tug | tug: wetted surface S | 432.2646 | 432.2646 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-tug | tug: total resistance | 8195.6046 | 8196.5981 | 0.5 % (err -0.012%) | PASS | independent re-implementation |
| HT-RW-tug | tug: wave resistance | 35.8806 | 35.8806 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-tug | tug: form factor | 1.4358 | 1.4358 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-slender | slender: wetted surface S | 592.0652 | 592.0652 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-slender | slender: total resistance | 17626.6665 | 17628.1831 | 0.5 % (err -0.009%) | PASS | independent re-implementation |
| HT-RW-slender | slender: wave resistance | 435.7114 | 435.7114 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-slender | slender: form factor | 1.1060 | 1.1060 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-lowFn | lowFn: wetted surface S | 2021.1767 | 2021.1767 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-lowFn | lowFn: total resistance | 9709.5374 | 9710.6672 | 0.5 % (err -0.012%) | PASS | independent re-implementation |
| HT-RW-lowFn | lowFn: wave resistance | 0.0002213 | 0.0002213 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-lowFn | lowFn: form factor | 1.1927 | 1.1927 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-highFn | highFn: wetted surface S | 417.7787 | 417.7787 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-highFn | highFn: total resistance | 24184.3326 | 24186.0794 | 0.5 % (err -0.007%) | PASS | independent re-implementation |
| HT-RW-highFn | highFn: wave resistance | 2866.0396 | 2866.0396 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-highFn | highFn: form factor | 1.2187 | 1.2187 | 0.01 % (err +0.000%) | PASS | independent re-implementation |
| HT-S-fullCb | fullCb: wetted surface S | 3572.7828 | 3572.7828 | 0.001 % (err +0.000%) | PASS | independent re-implementation, HM82 eq.1 |
| HT-RT-fullCb | fullCb: total resistance | 1.827e+05 | 1.827e+05 | 0.5 % (err -0.010%) | PASS | independent re-implementation |
| HT-RW-fullCb | fullCb: wave resistance | 17618.6344 | 17618.6344 | 1 % (err +0.000%) | PASS | independent re-implementation |
| HT-K1-fullCb | fullCb: form factor | 1.4127 | 1.4127 | 0.01 % (err +0.000%) | PASS | independent re-implementation |

## C Savitsky vs independent — 24 cases, 24 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| SV-LAM-shoemaker-18.01kn | shoemaker-18.01kn: wetted-length ratio | 1.5867 | 1.5867 | 0.5 % (err -0.000%) | PASS | independent re-implementation |
| SV-TAU-shoemaker-18.01kn | shoemaker-18.01kn: running trim | 4.2599 | 4.2599 | ±0.05 | PASS | independent re-implementation |
| SV-VM-shoemaker-18.01kn | shoemaker-18.01kn: mean bottom velocity | 9.1170 | 9.1170 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-shoemaker-18.01kn | shoemaker-18.01kn: drag (both with ITTC-57 + 0.0004 roughness) | 69.4777 | 69.4777 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |
| SV-LAM-shoemaker-20.92kn | shoemaker-20.92kn: wetted-length ratio | 1.5748 | 1.5748 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-TAU-shoemaker-20.92kn | shoemaker-20.92kn: running trim | 3.4770 | 3.4770 | ±0.05 | PASS | independent re-implementation |
| SV-VM-shoemaker-20.92kn | shoemaker-20.92kn: mean bottom velocity | 10.6340 | 10.6340 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-shoemaker-20.92kn | shoemaker-20.92kn: drag (both with ITTC-57 + 0.0004 roughness) | 78.2384 | 78.2384 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |
| SV-LAM-speed_ferry | speed_ferry: wetted-length ratio | 3.0234 | 3.0234 | 0.5 % (err -0.000%) | PASS | independent re-implementation |
| SV-TAU-speed_ferry | speed_ferry: running trim | 4.5038 | 4.5038 | ±0.05 | PASS | independent re-implementation |
| SV-VM-speed_ferry | speed_ferry: mean bottom velocity | 7.0237 | 7.0237 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-speed_ferry | speed_ferry: drag (both with ITTC-57 + 0.0004 roughness) | 9150.7460 | 9150.7460 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |
| SV-LAM-transfer | transfer: wetted-length ratio | 3.7351 | 3.7351 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-TAU-transfer | transfer: running trim | 4.6373 | 4.6373 | ±0.05 | PASS | independent re-implementation |
| SV-VM-transfer | transfer: mean bottom velocity | 6.0764 | 6.0764 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-transfer | transfer: drag (both with ITTC-57 + 0.0004 roughness) | 11313.1817 | 11313.1817 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |
| SV-LAM-dinghy | dinghy: wetted-length ratio | 2.2123 | 2.2123 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-TAU-dinghy | dinghy: running trim | 7.0054 | 7.0054 | ±0.05 | PASS | independent re-implementation |
| SV-VM-dinghy | dinghy: mean bottom velocity | 5.4603 | 5.4603 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-dinghy | dinghy: drag (both with ITTC-57 + 0.0004 roughness) | 1730.2079 | 1730.2079 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |
| SV-LAM-deep-v | deep-v: wetted-length ratio | 2.3633 | 2.3633 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-TAU-deep-v | deep-v: running trim | 7.6673 | 7.6673 | ±0.05 | PASS | independent re-implementation |
| SV-VM-deep-v | deep-v: mean bottom velocity | 7.4690 | 7.4690 | 0.5 % (err +0.000%) | PASS | independent re-implementation |
| SV-D-deep-v | deep-v: drag (both with ITTC-57 + 0.0004 roughness) | 9335.5572 | 9335.5572 | 1 % (err +0.000%) | PASS | independent re-implementation, same friction basis |

## D Wageningen B-series — 30 cases, 30 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| BS-TERMS | KT polynomial has 39 terms and KQ 47 (Oosterveld & van Oossanen 1975) | 39 / 47 | 39 / 47 | exact | PASS | table size only — not a value check |
| BS-KT-J0.50_PD1.00_EAR0.70_Z4 | J0.50_PD1.00_EAR0.70_Z4: KT equals the explicit 39-term sum | 0.2710 | 0.2710 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.50_PD1.00_EAR0.70_Z4 | J0.50_PD1.00_EAR0.70_Z4: KQ equals the explicit 47-term sum | 0.0434 | 0.0434 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.50_PD1.00_EAR0.70_Z4 | J0.50_PD1.00_EAR0.70_Z4: open-water efficiency equals J*KT/(2*pi*KQ) | 0.4966 |  | exact | PASS | definition identity |
| BS-RANGE-J0.50_PD1.00_EAR0.70_Z4 | J0.50_PD1.00_EAR0.70_Z4: KT, KQ positive and eta in (0, 0.85) | KT=0.2710 KQ=0.04343 eta=0.4966 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J0.60_PD0.90_EAR0.55_Z4 | J0.60_PD0.90_EAR0.55_Z4: KT equals the explicit 39-term sum | 0.1768 | 0.1768 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.60_PD0.90_EAR0.55_Z4 | J0.60_PD0.90_EAR0.55_Z4: KQ equals the explicit 47-term sum | 0.0273 | 0.0273 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.60_PD0.90_EAR0.55_Z4 | J0.60_PD0.90_EAR0.55_Z4: open-water efficiency equals J*KT/(2*pi*KQ) | 0.6182 |  | exact | PASS | definition identity |
| BS-RANGE-J0.60_PD0.90_EAR0.55_Z4 | J0.60_PD0.90_EAR0.55_Z4: KT, KQ positive and eta in (0, 0.85) | KT=0.1768 KQ=0.02730 eta=0.6182 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J0.30_PD1.20_EAR0.85_Z5 | J0.30_PD1.20_EAR0.85_Z5: KT equals the explicit 39-term sum | 0.4822 | 0.4822 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.30_PD1.20_EAR0.85_Z5 | J0.30_PD1.20_EAR0.85_Z5: KQ equals the explicit 47-term sum | 0.0868 | 0.0868 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.30_PD1.20_EAR0.85_Z5 | J0.30_PD1.20_EAR0.85_Z5: open-water efficiency equals J*KT/(2*pi*KQ) | 0.2652 |  | exact | PASS | definition identity |
| BS-RANGE-J0.30_PD1.20_EAR0.85_Z5 | J0.30_PD1.20_EAR0.85_Z5: KT, KQ positive and eta in (0, 0.85) | KT=0.4822 KQ=0.08682 eta=0.2652 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J0.80_PD1.00_EAR0.70_Z4 | J0.80_PD1.00_EAR0.70_Z4: KT equals the explicit 39-term sum | 0.1297 | 0.1297 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.80_PD1.00_EAR0.70_Z4 | J0.80_PD1.00_EAR0.70_Z4: KQ equals the explicit 47-term sum | 0.0240 | 0.0240 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.80_PD1.00_EAR0.70_Z4 | J0.80_PD1.00_EAR0.70_Z4: open-water efficiency equals J*KT/(2*pi*KQ) | 0.6890 |  | exact | PASS | definition identity |
| BS-RANGE-J0.80_PD1.00_EAR0.70_Z4 | J0.80_PD1.00_EAR0.70_Z4: KT, KQ positive and eta in (0, 0.85) | KT=0.1297 KQ=0.02397 eta=0.6890 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J0.20_PD0.60_EAR0.50_Z3 | J0.20_PD0.60_EAR0.50_Z3: KT equals the explicit 39-term sum | 0.1767 | 0.1767 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.20_PD0.60_EAR0.50_Z3 | J0.20_PD0.60_EAR0.50_Z3: KQ equals the explicit 47-term sum | 0.0181 | 0.0181 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.20_PD0.60_EAR0.50_Z3 | J0.20_PD0.60_EAR0.50_Z3: open-water efficiency equals J*KT/(2*pi*KQ) | 0.3110 |  | exact | PASS | definition identity |
| BS-RANGE-J0.20_PD0.60_EAR0.50_Z3 | J0.20_PD0.60_EAR0.50_Z3: KT, KQ positive and eta in (0, 0.85) | KT=0.1767 KQ=0.01808 eta=0.3110 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J1.00_PD1.40_EAR1.05_Z5 | J1.00_PD1.40_EAR1.05_Z5: KT equals the explicit 39-term sum | 0.2421 | 0.2421 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J1.00_PD1.40_EAR1.05_Z5 | J1.00_PD1.40_EAR1.05_Z5: KQ equals the explicit 47-term sum | 0.0576 | 0.0576 | exact | PASS | independent summation of the stored table |
| BS-ETA-J1.00_PD1.40_EAR1.05_Z5 | J1.00_PD1.40_EAR1.05_Z5: open-water efficiency equals J*KT/(2*pi*KQ) | 0.6693 |  | exact | PASS | definition identity |
| BS-RANGE-J1.00_PD1.40_EAR1.05_Z5 | J1.00_PD1.40_EAR1.05_Z5: KT, KQ positive and eta in (0, 0.85) | KT=0.2421 KQ=0.05756 eta=0.6693 |  | exact | PASS | physical plausibility band of the series |
| BS-KT-J0.70_PD0.80_EAR0.65_Z6 | J0.70_PD0.80_EAR0.65_Z6: KT equals the explicit 39-term sum | 0.0857 | 0.0857 | exact | PASS | independent summation of the stored table (evaluation check) |
| BS-KQ-J0.70_PD0.80_EAR0.65_Z6 | J0.70_PD0.80_EAR0.65_Z6: KQ equals the explicit 47-term sum | 0.0162 | 0.0162 | exact | PASS | independent summation of the stored table |
| BS-ETA-J0.70_PD0.80_EAR0.65_Z6 | J0.70_PD0.80_EAR0.65_Z6: open-water efficiency equals J*KT/(2*pi*KQ) | 0.5911 |  | exact | PASS | definition identity |
| BS-RANGE-J0.70_PD0.80_EAR0.65_Z6 | J0.70_PD0.80_EAR0.65_Z6: KT, KQ positive and eta in (0, 0.85) | KT=0.0857 KQ=0.01616 eta=0.5911 |  | exact | PASS | physical plausibility band of the series |
| BS-RN-2e+07 | KT/KQ stay positive at Rn=2e+07 | KT=0.3904 KQ=0.06414 |  | exact | PASS | Reynolds-number correction of Oosterveld & van Oossanen (1975) |

## E ITTC-1957 friction — 7 cases, 7 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| ITTC-100000 | Cf at Rn=1e+05 | 0.0083 | 0.0083 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-1e+06 | Cf at Rn=1e+06 | 0.0047 | 0.0047 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-1e+07 | Cf at Rn=1e+07 | 0.0030 | 0.0030 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-1e+08 | Cf at Rn=1e+08 | 0.0021 | 0.0021 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-1e+09 | Cf at Rn=1e+09 | 0.0015 | 0.0015 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-2.2193e+09 | Cf at Rn=2.22e+09 | 0.0014 | 0.0014 | 1e-09 % (err +0.000%) | PASS | ITTC-57 definition 0.075/(log10 Re-2)^2 |
| ITTC-1e6-value | Cf(1e6) = 0.0046875 | 0.0047 | 0.0047 | exact | PASS | closed form |

## F YANMAR database — 214 cases, 214 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| ENG-RAT-4JHYE | 4JHYE ratings (letter, kW, rpm) equal the official row(s) | [('L', 29.4, 3600), ('M', 25.7, 3400)] | [('L', 29.4, 3600), ('M', 25.7, 3400)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/jhseries/ accessed 2026-10-25 |
| ENG-RAT-4CHE3 | 4CHE3 ratings (letter, kW, rpm) equal the official row(s) | [('L', 62.5, 2600), ('M', 57.4, 2550)] | [('L', 62.5, 2600), ('M', 57.4, 2550)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cheseries/ accessed 2026-10-25 |
| ENG-MASS-4CHE3 | 4CHE3 published dry mass WITH YX-30-2 (70 kg) | 570 | 570 | ±0.5 | PASS | CHE page: the published figure already includes the gear |
| ENG-GEAR-4CHE3-YX-30-2 | 4CHE3 YX-30-2 reduction ratios | [2.03, 2.55, 2.96, 3.48] | [2.03, 2.55, 2.96, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-4CHE3-YX-30-2 | 4CHE3 YX-30-2 gear mass | 70 | 70 | exact | PASS | official page |
| ENG-RAT-6CHE3 | 6CHE3 ratings (letter, kW, rpm) equal the official row(s) | [('L', 95.6, 2600), ('M', 84.6, 2550)] | [('L', 95.6, 2600), ('M', 84.6, 2550)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cheseries/ accessed 2026-10-25 |
| ENG-MASS-6CHE3 | 6CHE3 published dry mass WITH YX-30-2 (70 kg) | 700 | 700 | ±0.5 | PASS | CHE page: the published figure already includes the gear |
| ENG-GEAR-6CHE3-YX-30-2 | 6CHE3 YX-30-2 reduction ratios | [2.03, 2.55, 2.96, 3.48] | [2.03, 2.55, 2.96, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6CHE3-YX-30-2 | 6CHE3 YX-30-2 gear mass | 70 | 70 | exact | PASS | official page |
| ENG-RAT-6CH-HTE3 | 6CH-HTE3 ratings (letter, kW, rpm) equal the official row(s) | [('L', 140, 2600), ('M', 125, 2550)] | [('L', 140.0, 2600), ('M', 125.0, 2550)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cheseries/ accessed 2026-10-25 |
| ENG-MASS-6CH-HTE3 | 6CH-HTE3 published dry mass WITH YX-50S-4 (120 kg) | 795 | 795 | ±0.5 | PASS | CHE page: the published figure already includes the gear |
| ENG-GEAR-6CH-HTE3-YX-50S-4 | 6CH-HTE3 YX-50S-4 reduction ratios | [2.03, 2.48, 2.88] | [2.03, 2.48, 2.88] | exact | PASS | official page |
| ENG-GEAR-6CH-HTE3-YX-71-4 | 6CH-HTE3 YX-71-4 reduction ratios | [3.53] | [3.53] | exact | PASS | official page |
| ENG-GEARMASS-6CH-HTE3-YX-50S-4 | 6CH-HTE3 YX-50S-4 gear mass | 120 | 120 | exact | PASS | official page |
| ENG-RAT-6CH-WDTE | 6CH-WDTE ratings (letter, kW, rpm) equal the official row(s) | [('L', 169, 2600), ('M', 154, 2550)] | [('L', 169.0, 2600), ('M', 154.0, 2550)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cheseries/ accessed 2026-10-25 |
| ENG-GEAR-6CH-WDTE-YX-71-4 | 6CH-WDTE YX-71-4 reduction ratios | [2.07, 2.58, 2.91, 3.53] | [2.07, 2.58, 2.91, 3.53] | exact | PASS | official page |
| ENG-RAT-6CH-WUTE | 6CH-WUTE ratings (letter, kW, rpm) equal the official row(s) | [('L', 206, 2600), ('M', 188, 2550)] | [('L', 206.0, 2600), ('M', 188.0, 2550)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cheseries/ accessed 2026-10-25 |
| ENG-GEAR-6CH-WUTE-YX-71-4 | 6CH-WUTE YX-71-4 reduction ratios | [2.07, 2.58, 2.91, 3.53] | [2.07, 2.58, 2.91, 3.53] | exact | PASS | official page |
| ENG-RAT-6CXBM-GT | 6CXBM-GT ratings (letter, kW, rpm) equal the official row(s) | [('H', 265, 2400), ('L', 341, 2700), ('M', 294, 2500), ('S', 374, 2700)] | [('H', 265.0, 2400), ('L', 341.0, 2700), ('M', 294.0, 2500), ('S', 374.0, 2700)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/cxbseries/ accessed 2026-10-25 |
| ENG-MASS-6CXBM-GT | 6CXBM-GT dry mass (without marine gear) | 856 | 856 | ±0.5 | PASS | official page |
| ENG-DIMS-6CXBM-GT | 6CXBM-GT L×W×H equal the official page | [1390, 901, 989] | (1390, 901, 989) | exact | PASS | official page |
| ENG-GEAR-6CXBM-GT-YX-80 | 6CXBM-GT YX-80 reduction ratios | [2.07, 2.58, 2.91] | [2.07, 2.58, 2.91] | exact | PASS | official page |
| ENG-GEARMASS-6CXBM-GT-YX-80 | 6CXBM-GT YX-80 gear mass | 204 | 204 | exact | PASS | official page |
| ENG-RAT-6HA3M-WHT | 6HA3M-WHT ratings (letter, kW, rpm) equal the official row(s) | [('H', 204, 1880), ('M', 257, 1950)] | [('H', 204.0, 1880), ('M', 257.0, 1950)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/haseries/ accessed 2026-10-25 |
| ENG-MASS-6HA3M-WHT | 6HA3M-WHT dry mass (without marine gear) | 1398 | 1398 | ±0.5 | PASS | official page |
| ENG-DIMS-6HA3M-WHT | 6HA3M-WHT L×W×H equal the official page | [1585, 1016, 1260] | (1585, 1016, 1260) | exact | PASS | official page |
| ENG-GEAR-6HA3M-WHT-YX-120 | 6HA3M-WHT YX-120 reduction ratios | [2.03, 2.57, 3.04, 3.55] | [2.03, 2.57, 3.04, 3.55] | exact | PASS | official page |
| ENG-GEAR-6HA3M-WHT-YX-120L | 6HA3M-WHT YX-120L reduction ratios | [4, 4.59] | [4.0, 4.59] | exact | PASS | official page |
| ENG-GEARMASS-6HA3M-WHT-YX-120 | 6HA3M-WHT YX-120 gear mass | 315 | 315 | exact | PASS | official page |
| ENG-RAT-6HA3M-WDT | 6HA3M-WDT ratings (letter, kW, rpm) equal the official row(s) | [('M', 298, 1950)] | [('M', 298.0, 1950)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/haseries/ accessed 2026-10-25 |
| ENG-MASS-6HA3M-WDT | 6HA3M-WDT dry mass (without marine gear) | 1448 | 1448 | ±0.5 | PASS | official page |
| ENG-DIMS-6HA3M-WDT | 6HA3M-WDT L×W×H equal the official page | [1585, 1036, 1260] | (1585, 1036, 1260) | exact | PASS | official page |
| ENG-GEAR-6HA3M-WDT-YX-120 | 6HA3M-WDT YX-120 reduction ratios | [2.03, 2.57, 3.04] | [2.03, 2.57, 3.04] | exact | PASS | official page |
| ENG-GEAR-6HA3M-WDT-YX-120L | 6HA3M-WDT YX-120L reduction ratios | [3.46, 4, 4.59] | [3.46, 4.0, 4.59] | exact | PASS | official page |
| ENG-GEARMASS-6HA3M-WDT-YX-120 | 6HA3M-WDT YX-120 gear mass | 315 | 315 | exact | PASS | official page |
| ENG-RAT-6HYM-WET | 6HYM-WET ratings (letter, kW, rpm) equal the official row(s) | [('H', 368, 1950), ('L', 478, 2150), ('M', 441, 2100), ('S', 515, 2200)] | [('H', 368.0, 1950), ('L', 478.0, 2150), ('M', 441.0, 2100), ('S', 515.0, 2200)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/hyseries/ accessed 2026-10-25 |
| ENG-MASS-6HYM-WET | 6HYM-WET dry mass (without marine gear) | 1385 | 1385 | ±0.5 | PASS | official page |
| ENG-DIMS-6HYM-WET | 6HYM-WET L×W×H equal the official page | [1556, 1014, 1133] | (1556, 1014, 1133) | exact | PASS | official page |
| ENG-GEAR-6HYM-WET-YXH-160 | 6HYM-WET YXH-160 reduction ratios | [1.97, 2.46, 3.05] | [1.97, 2.46, 3.05] | exact | PASS | official page |
| ENG-GEAR-6HYM-WET-YXH-130 | 6HYM-WET YXH-130 reduction ratios | [2.03, 2.57, 3.04] | [2.03, 2.57, 3.04] | exact | PASS | official page |
| ENG-GEAR-6HYM-WET-YX-161L | 6HYM-WET YX-161L reduction ratios | [3.65, 4.08, 4.55] | [3.65, 4.08, 4.55] | exact | PASS | official page |
| ENG-GEARMASS-6HYM-WET-YXH-160 | 6HYM-WET YXH-160 gear mass | 396 | 396 | exact | PASS | official page |
| ENG-RAT-6GY135W | 6GY135W ratings (letter, kW, rpm) equal the official row(s) | [('C', 372, 1800), ('H', 447, 1800), ('L', 559, 2100), ('M', 522, 2100), ('S', 599, 210… | [('C', 372.0, 1800), ('H', 447.0, 1800), ('L', 559.0, 2100), ('M', 522.0, 2100), ('S', … | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6gy135w/ accessed 2026-10-25 |
| ENG-MASS-6GY135W | 6GY135W dry mass (without marine gear) | 1825 | 1825 | ±0.5 | PASS | official page |
| ENG-DIMS-6GY135W | 6GY135W L×W×H equal the official page | [1645, 1055, 1254] | (1645, 1055, 1254) | exact | PASS | official page |
| ENG-GEAR-6GY135W-YXH-160-7 | 6GY135W YXH-160-7 reduction ratios | [1.97, 2.46, 3.05, 3.24] | [1.97, 2.46, 3.05, 3.24] | exact | PASS | official page |
| ENG-GEARMASS-6GY135W-YXH-160-7 | 6GY135W YXH-160-7 gear mass | 422 | 422 | exact | PASS | official page |
| ENG-RAT-6AYM-WST | 6AYM-WST ratings (letter, kW, rpm) equal the official row(s) | [('C', 485, 1900)] | [('C', 485.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayseries/ accessed 2026-10-25 |
| ENG-MASS-6AYM-WST | 6AYM-WST dry mass (without marine gear) | 2365 | 2365 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYM-WST | 6AYM-WST L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYM-WST-YX-181 | 6AYM-WST YX-181 reduction ratios | [2.08, 2.55, 3.03] | [2.08, 2.55, 3.03] | exact | PASS | official page |
| ENG-GEAR-6AYM-WST-YX-180L | 6AYM-WST YX-180L reduction ratios | [3.5, 4, 4.54] | [3.5, 4.0, 4.54] | exact | PASS | official page |
| ENG-GEARMASS-6AYM-WST-YX-181 | 6AYM-WST YX-181 gear mass | 560 | 560 | exact | PASS | official page |
| ENG-RAT-6AYM-WET | 6AYM-WET ratings (letter, kW, rpm) equal the official row(s) | [('C', 555, 1840), ('M', 610, 1900)] | [('C', 555.0, 1840), ('M', 610.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayseries/ accessed 2026-10-25 |
| ENG-MASS-6AYM-WET | 6AYM-WET dry mass (without marine gear) | 2365 | 2365 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYM-WET | 6AYM-WET L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYM-WET-YXH-240 | 6AYM-WET YXH-240 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYM-WET-YXH-240 | 6AYM-WET YXH-240 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYM-WGT | 6AYM-WGT ratings (letter, kW, rpm) equal the official row(s) | [('L', 670, 1938)] | [('L', 670.0, 1938)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayseries/ accessed 2026-10-25 |
| ENG-MASS-6AYM-WGT | 6AYM-WGT dry mass (without marine gear) | 2365 | 2365 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYM-WGT | 6AYM-WGT L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYM-WGT-YXH-240 | 6AYM-WGT YXH-240 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYM-WGT-YXH-240 | 6AYM-WGT YXH-240 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYAM-ET | 6AYAM-ET ratings (letter, kW, rpm) equal the official row(s) | [('C', 555, 1840)] | [('C', 555.0, 1840)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayseries/ accessed 2026-10-25 |
| ENG-MASS-6AYAM-ET | 6AYAM-ET dry mass (without marine gear) | 2295 | 2295 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYAM-ET | 6AYAM-ET L×W×H equal the official page | [1949, 1274, 1544] | (1949, 1274, 1544) | exact | PASS | official page |
| ENG-GEAR-6AYAM-ET-YXH-240 | 6AYAM-ET YXH-240 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYAM-ET-YXH-240 | 6AYAM-ET YXH-240 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYEM-ST | 6AYEM-ST ratings (letter, kW, rpm) equal the official row(s) | [('C', 485, 1900)] | [('C', 485.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayeseries/ accessed 2026-10-25 |
| ENG-MASS-6AYEM-ST | 6AYEM-ST dry mass (without marine gear) | 2418 | 2418 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYEM-ST | 6AYEM-ST L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYEM-ST-YXH-240-7 | 6AYEM-ST YXH-240-7 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-RAT-6AYEM-ET | 6AYEM-ET ratings (letter, kW, rpm) equal the official row(s) | [('C', 555, 1840), ('H', 599, 1900), ('M', 610, 1900)] | [('C', 555.0, 1840), ('H', 599.0, 1900), ('M', 610.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayeseries/ accessed 2026-10-25 |
| ENG-MASS-6AYEM-ET | 6AYEM-ET dry mass (without marine gear) | 2418 | 2418 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYEM-ET | 6AYEM-ET L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYEM-ET-YXH-240-7 | 6AYEM-ET YXH-240-7 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYEM-ET-YXH-240-7 | 6AYEM-ET YXH-240-7 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYEM-GT | 6AYEM-GT ratings (letter, kW, rpm) equal the official row(s) | [('L', 670, 1938), ('S', 737, 2000)] | [('L', 670.0, 1938), ('S', 737.0, 2000)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayeseries/ accessed 2026-10-25 |
| ENG-MASS-6AYEM-GT | 6AYEM-GT dry mass (without marine gear) | 2418 | 2418 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYEM-GT | 6AYEM-GT L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYEM-GT-YXH-240-7 | 6AYEM-GT YXH-240-7 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYEM-GT-YXH-240-7 | 6AYEM-GT YXH-240-7 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYEM-GTWS | 6AYEM-GTWS ratings (letter, kW, rpm) equal the official row(s) | [('L', 670, 1938), ('S', 749, 2000)] | [('L', 670.0, 1938), ('S', 749.0, 2000)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayeseries/ accessed 2026-10-25 |
| ENG-MASS-6AYEM-GTWS | 6AYEM-GTWS dry mass (without marine gear) | 2418 | 2418 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYEM-GTWS | 6AYEM-GTWS L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYEM-GTWS-YXH-240-7 | 6AYEM-GTWS YXH-240-7 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYEM-GTWS-YXH-240-7 | 6AYEM-GTWS YXH-240-7 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-6AYEM-ETWS | 6AYEM-ETWS ratings (letter, kW, rpm) equal the official row(s) | [('C', 555, 1840), ('M', 610, 1900)] | [('C', 555.0, 1840), ('M', 610.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayeseries/ accessed 2026-10-25 |
| ENG-MASS-6AYEM-ETWS | 6AYEM-ETWS dry mass (without marine gear) | 2418 | 2418 | ±0.5 | PASS | official page |
| ENG-DIMS-6AYEM-ETWS | 6AYEM-ETWS L×W×H equal the official page | [2000, 1305, 1431] | (2000, 1305, 1431) | exact | PASS | official page |
| ENG-GEAR-6AYEM-ETWS-YXH-240-7 | 6AYEM-ETWS YXH-240-7 reduction ratios | [1.95, 2.27, 2.56, 3.03, 3.48] | [1.95, 2.27, 2.56, 3.03, 3.48] | exact | PASS | official page |
| ENG-GEARMASS-6AYEM-ETWS-YXH-240-7 | 6AYEM-ETWS YXH-240-7 gear mass | 632 | 632 | exact | PASS | official page |
| ENG-RAT-12AYM-WST | 12AYM-WST ratings (letter, kW, rpm) equal the official row(s) | [('H', 882, 1850), ('H', 1030, 1900)] | [('H', 882.0, 1850), ('H', 1030.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayseries/ accessed 2026-10-25 |
| ENG-MASS-12AYM-WST | 12AYM-WST dry mass (without marine gear) | 4950 | 4950 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYM-WST | 12AYM-WST L×W×H equal the official page | [2743, 1642, 1707] | (2743, 1642, 1707) | exact | PASS | official page |
| ENG-RAT-12AYM-WET | 12AYM-WET ratings (letter, kW, rpm) equal the official row(s) | [('H', 1140, 1840), ('M', 1220, 1900)] | [('H', 1140.0, 1840), ('M', 1220.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayseries/ accessed 2026-10-25 |
| ENG-MASS-12AYM-WET | 12AYM-WET dry mass (without marine gear) | 4950 | 4950 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYM-WET | 12AYM-WET L×W×H equal the official page | [2743, 1642, 1707] | (2743, 1642, 1707) | exact | PASS | official page |
| ENG-RAT-12AYM-WGT | 12AYM-WGT ratings (letter, kW, rpm) equal the official row(s) | [('L', 1340, 1940)] | [('L', 1340.0, 1940)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayseries/ accessed 2026-10-25 |
| ENG-MASS-12AYM-WGT | 12AYM-WGT dry mass (without marine gear) | 4950 | 4950 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYM-WGT | 12AYM-WGT L×W×H equal the official page | [2743, 1642, 1707] | (2743, 1642, 1707) | exact | PASS | official page |
| ENG-RAT-12AYEM-ST | 12AYEM-ST ratings (letter, kW, rpm) equal the official row(s) | [('C', 1030, 1800)] | [('C', 1030.0, 1800)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayeseries/ accessed 2026-10-25 |
| ENG-MASS-12AYEM-ST | 12AYEM-ST dry mass (without marine gear) | 4780 | 4780 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYEM-ST | 12AYEM-ST L×W×H equal the official page | [2743, 1649, 1707] | (2743, 1649, 1707) | exact | PASS | official page |
| ENG-RAT-12AYEM-ET | 12AYEM-ET ratings (letter, kW, rpm) equal the official row(s) | [('H', 1140, 1840), ('M', 1220, 1900)] | [('H', 1140.0, 1840), ('M', 1220.0, 1900)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayeseries/ accessed 2026-10-25 |
| ENG-MASS-12AYEM-ET | 12AYEM-ET dry mass (without marine gear) | 4780 | 4780 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYEM-ET | 12AYEM-ET L×W×H equal the official page | [2743, 1649, 1707] | (2743, 1649, 1707) | exact | PASS | official page |
| ENG-RAT-12AYEM-GT | 12AYEM-GT ratings (letter, kW, rpm) equal the official row(s) | [('L', 1340, 1940)] | [('L', 1340.0, 1940)] | exact | PASS | https://www.yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/12ayeseries/ accessed 2026-10-25 |
| ENG-MASS-12AYEM-GT | 12AYEM-GT dry mass (without marine gear) | 4780 | 4780 | ±0.5 | PASS | official page |
| ENG-DIMS-12AYEM-GT | 12AYEM-GT L×W×H equal the official page | [2743, 1649, 1707] | (2743, 1649, 1707) | exact | PASS | official page |
| ENG-DISP-4JHYE | 4JHYE displacement from bore*stroke*cylinders | 1.6440 | 1.6438 | 2 % (err +0.015%) | PASS | geometric identity |
| ENG-TQ-4JHYE-M | 4JHYE M rated torque plausible (72 N·m) | 72.2000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-4JHYE-L | 4JHYE L rated torque plausible (78 N·m) | 78.0000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-4JHYE | 4JHYE installed masses are positive or explicitly unknown | {'YX-10': 220} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-4CHE3 | 4CHE3 displacement from bore*stroke*cylinders | 4.3300 | 4.3295 | 2 % (err +0.011%) | PASS | geometric identity |
| ENG-TQ-4CHE3-M | 4CHE3 M rated torque plausible (215 N·m) | 215.0000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-4CHE3-L | 4CHE3 L rated torque plausible (230 N·m) | 229.6000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-4CHE3 | 4CHE3 installed masses are positive or explicitly unknown | {'YX-30-2': 570} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6CHE3 | 6CHE3 displacement from bore*stroke*cylinders | 6.4940 | 6.4943 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6CHE3-M | 6CHE3 M rated torque plausible (317 N·m) | 316.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CHE3-L | 6CHE3 L rated torque plausible (351 N·m) | 351.1000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6CHE3 | 6CHE3 installed masses are positive or explicitly unknown | {'YX-30-2': 700} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6CH-HTE3 | 6CH-HTE3 displacement from bore*stroke*cylinders | 6.4940 | 6.4943 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6CH-HTE3-M | 6CH-HTE3 M rated torque plausible (468 N·m) | 468.1000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CH-HTE3-L | 6CH-HTE3 L rated torque plausible (514 N·m) | 514.2000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6CH-HTE3 | 6CH-HTE3 installed masses are positive or explicitly unknown | {'YX-50S-4': 795, 'YX-71-4': 900} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6CH-WDTE | 6CH-WDTE displacement from bore*stroke*cylinders | 6.4940 | 6.4943 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6CH-WDTE-M | 6CH-WDTE M rated torque plausible (577 N·m) | 576.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CH-WDTE-L | 6CH-WDTE L rated torque plausible (621 N·m) | 620.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6CH-WDTE | 6CH-WDTE installed masses are positive or explicitly unknown | {'YX-71-4': 900} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6CH-WUTE | 6CH-WUTE displacement from bore*stroke*cylinders | 6.4940 | 6.4943 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6CH-WUTE-M | 6CH-WUTE M rated torque plausible (704 N·m) | 704.0000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CH-WUTE-L | 6CH-WUTE L rated torque plausible (757 N·m) | 756.6000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6CH-WUTE | 6CH-WUTE installed masses are positive or explicitly unknown | {'YX-71-4': 940} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6CXBM-GT | 6CXBM-GT displacement from bore*stroke*cylinders | 7.4130 | 7.4126 | 2 % (err +0.006%) | PASS | geometric identity |
| ENG-TQ-6CXBM-GT-H | 6CXBM-GT H rated torque plausible (1054 N·m) | 1054.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CXBM-GT-M | 6CXBM-GT M rated torque plausible (1123 N·m) | 1123.0000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CXBM-GT-L | 6CXBM-GT L rated torque plausible (1206 N·m) | 1206.0000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6CXBM-GT-S | 6CXBM-GT S rated torque plausible (1323 N·m) | 1322.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6CXBM-GT | 6CXBM-GT installed masses are positive or explicitly unknown | {'YX-80': 856} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6HA3M-WHT | 6HA3M-WHT displacement from bore*stroke*cylinders | 13.1400 | 13.1405 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6HA3M-WHT-H | 6HA3M-WHT H rated torque plausible (1036 N·m) | 1036.2000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6HA3M-WHT-M | 6HA3M-WHT M rated torque plausible (1259 N·m) | 1258.5000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6HA3M-WHT | 6HA3M-WHT installed masses are positive or explicitly unknown | {'YX-120': 1713, 'YX-120L': 1809} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6HA3M-WDT | 6HA3M-WDT displacement from bore*stroke*cylinders | 13.1400 | 13.1405 | 2 % (err -0.004%) | PASS | geometric identity |
| ENG-TQ-6HA3M-WDT-M | 6HA3M-WDT M rated torque plausible (1459 N·m) | 1459.3000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6HA3M-WDT | 6HA3M-WDT installed masses are positive or explicitly unknown | {'YX-120': 1763, 'YX-120L': 1859} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6HYM-WET | 6HYM-WET displacement from bore*stroke*cylinders | 13.7330 | 13.7333 | 2 % (err -0.002%) | PASS | geometric identity |
| ENG-TQ-6HYM-WET-H | 6HYM-WET H rated torque plausible (1802 N·m) | 1802.1000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6HYM-WET-M | 6HYM-WET M rated torque plausible (2005 N·m) | 2005.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6HYM-WET-L | 6HYM-WET L rated torque plausible (2123 N·m) | 2123.1000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6HYM-WET-S | 6HYM-WET S rated torque plausible (2235 N·m) | 2235.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6HYM-WET | 6HYM-WET installed masses are positive or explicitly unknown | {'YXH-160': 1385, 'YXH-130': 1385, 'YX-161L': 1385} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6GY135W | 6GY135W displacement from bore*stroke*cylinders | 14.6000 | 14.6002 | 2 % (err -0.001%) | PASS | geometric identity |
| ENG-TQ-6GY135W-C | 6GY135W C rated torque plausible (1974 N·m) | 1973.5000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6GY135W-H | 6GY135W H rated torque plausible (2371 N·m) | 2371.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6GY135W-M | 6GY135W M rated torque plausible (2374 N·m) | 2373.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6GY135W-L | 6GY135W L rated torque plausible (2542 N·m) | 2541.9000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6GY135W-S | 6GY135W S rated torque plausible (2724 N·m) | 2723.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6GY135W | 6GY135W installed masses are positive or explicitly unknown | {'YXH-160-7': 1825} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYM-WST | 6AYM-WST displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYM-WST-C | 6AYM-WST C rated torque plausible (2438 N·m) | 2437.6000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYM-WST | 6AYM-WST installed masses are positive or explicitly unknown | {'YX-181': 2925, 'YX-180L': 3045} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYM-WET | 6AYM-WET displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYM-WET-C | 6AYM-WET C rated torque plausible (2880 N·m) | 2880.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYM-WET-M | 6AYM-WET M rated torque plausible (3066 N·m) | 3065.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYM-WET | 6AYM-WET installed masses are positive or explicitly unknown | {'YXH-240': 2997} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYM-WGT | 6AYM-WGT displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYM-WGT-L | 6AYM-WGT L rated torque plausible (3301 N·m) | 3301.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYM-WGT | 6AYM-WGT installed masses are positive or explicitly unknown | {'YXH-240': 2997} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYAM-ET | 6AYAM-ET displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYAM-ET-C | 6AYAM-ET C rated torque plausible (2880 N·m) | 2880.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYAM-ET | 6AYAM-ET installed masses are positive or explicitly unknown | {'YXH-240': 2295} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYEM-ST | 6AYEM-ST displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYEM-ST-C | 6AYEM-ST C rated torque plausible (2438 N·m) | 2437.6000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYEM-ST | 6AYEM-ST installed masses are positive or explicitly unknown | {'YXH-240-7': None} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYEM-ET | 6AYEM-ET displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYEM-ET-C | 6AYEM-ET C rated torque plausible (2880 N·m) | 2880.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYEM-ET-H | 6AYEM-ET H rated torque plausible (3011 N·m) | 3010.5000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYEM-ET-M | 6AYEM-ET M rated torque plausible (3066 N·m) | 3065.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYEM-ET | 6AYEM-ET installed masses are positive or explicitly unknown | {'YXH-240-7': 3050} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYEM-GT | 6AYEM-GT displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYEM-GT-L | 6AYEM-GT L rated torque plausible (3301 N·m) | 3301.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYEM-GT-S | 6AYEM-GT S rated torque plausible (3519 N·m) | 3518.9000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYEM-GT | 6AYEM-GT installed masses are positive or explicitly unknown | {'YXH-240-7': 3050} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYEM-GTWS | 6AYEM-GTWS displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYEM-GTWS-L | 6AYEM-GTWS L rated torque plausible (3301 N·m) | 3301.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYEM-GTWS-S | 6AYEM-GTWS S rated torque plausible (3576 N·m) | 3576.2000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYEM-GTWS | 6AYEM-GTWS installed masses are positive or explicitly unknown | {'YXH-240-7': 3050} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-6AYEM-ETWS | 6AYEM-ETWS displacement from bore*stroke*cylinders | 20.3790 | 20.3787 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-6AYEM-ETWS-C | 6AYEM-ETWS C rated torque plausible (2880 N·m) | 2880.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-6AYEM-ETWS-M | 6AYEM-ETWS M rated torque plausible (3066 N·m) | 3065.8000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-6AYEM-ETWS | 6AYEM-ETWS installed masses are positive or explicitly unknown | {'YXH-240-7': 3050} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYM-WST | 12AYM-WST displacement from bore*stroke*cylinders | 40.7600 | 40.7575 | 2 % (err +0.006%) | PASS | geometric identity |
| ENG-TQ-12AYM-WST-H | 12AYM-WST H rated torque plausible (4553 N·m) | 4552.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-12AYM-WST-H | 12AYM-WST H rated torque plausible (5177 N·m) | 5176.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYM-WST | 12AYM-WST installed masses are positive or explicitly unknown | {'YHX-500-1': 5920, 'YHX-500L-1': 6570} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYM-WET | 12AYM-WET displacement from bore*stroke*cylinders | 40.7600 | 40.7575 | 2 % (err +0.006%) | PASS | geometric identity |
| ENG-TQ-12AYM-WET-H | 12AYM-WET H rated torque plausible (5916 N·m) | 5916.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-12AYM-WET-M | 12AYM-WET M rated torque plausible (6132 N·m) | 6131.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYM-WET | 12AYM-WET installed masses are positive or explicitly unknown | {'YHX-500-1': 5920, 'YHX-500L-1': 6570} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYM-WGT | 12AYM-WGT displacement from bore*stroke*cylinders | 40.7600 | 40.7575 | 2 % (err +0.006%) | PASS | geometric identity |
| ENG-TQ-12AYM-WGT-L | 12AYM-WGT L rated torque plausible (6596 N·m) | 6595.9000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYM-WGT | 12AYM-WGT installed masses are positive or explicitly unknown | {'YHX-500-1': 5920, 'YHX-500L-1': 6570} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYEM-ST | 12AYEM-ST displacement from bore*stroke*cylinders | 40.7580 | 40.7575 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-12AYEM-ST-C | 12AYEM-ST C rated torque plausible (5464 N·m) | 5464.3000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYEM-ST | 12AYEM-ST installed masses are positive or explicitly unknown | {'YHX-500-3': 5750, 'YHX-500L-3': 6400} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYEM-ET | 12AYEM-ET displacement from bore*stroke*cylinders | 40.7580 | 40.7575 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-12AYEM-ET-H | 12AYEM-ET H rated torque plausible (5916 N·m) | 5916.4000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-TQ-12AYEM-ET-M | 12AYEM-ET M rated torque plausible (6132 N·m) | 6131.7000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYEM-ET | 12AYEM-ET installed masses are positive or explicitly unknown | {'YHX-500-3': 5750, 'YHX-500L-3': 6400} | > 0 or null | exact | PASS | installedMassOf() |
| ENG-DISP-12AYEM-GT | 12AYEM-GT displacement from bore*stroke*cylinders | 40.7580 | 40.7575 | 2 % (err +0.001%) | PASS | geometric identity |
| ENG-TQ-12AYEM-GT-L | 12AYEM-GT L rated torque plausible (6596 N·m) | 6595.9000 | < 40000 N·m | exact | PASS | 9549.3*P/n identity |
| ENG-INST-12AYEM-GT | 12AYEM-GT installed masses are positive or explicitly unknown | {'YHX-500-3': 5750, 'YHX-500L-3': 6400} | > 0 or null | exact | PASS | installedMassOf() |

## G selection — 103 cases, 103 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| SEL-OK-fishing_dhoni | fishing_dhoni yields a candidate (4CHE3 M) | ok | ok | exact | PASS |  |
| SEL-PB-fishing_dhoni | fishing_dhoni: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 44.7035 | 44.7035 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-fishing_dhoni | fishing_dhoni: P_E = R_T * V_s | 22017.9955 | 22017.9955 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-fishing_dhoni | fishing_dhoni: load = P_B/P_rated | 0.7788 | 0.7788 | exact | PASS | definition |
| SEL-MAXLOAD-fishing_dhoni | fishing_dhoni: service load within the 100 % hard limit | 0.7788 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-fishing_dhoni | fishing_dhoni: propeller efficiency equals J*KT/(2*pi*KQ) | 0.5530 |  | exact | PASS |  |
| SEL-D-fishing_dhoni | fishing_dhoni: propeller diameter positive and physical | 0.7871 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-fishing_dhoni | fishing_dhoni: P/D inside the B-series band | 0.6175 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-fishing_dhoni | fishing_dhoni: blade area covers the cavitation requirement | EAR=0.500 EARreq=0.405 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-fishing_dhoni | fishing_dhoni: rejected candidates are listed with reasons (42) | 42 | > 0 | exact | PASS |  |
| SEL-REJWHY-fishing_dhoni | fishing_dhoni: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-OK-bokkura | bokkura yields a candidate (4JHYE M) | ok | ok | exact | PASS |  |
| SEL-PB-bokkura | bokkura: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 4.4227 | 4.4227 | 0.01 % (err -0.000%) | PASS | power ledger definition |
| SEL-PE-bokkura | bokkura: P_E = R_T * V_s | 2295.2037 | 2295.2037 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-bokkura | bokkura: load = P_B/P_rated | 0.1721 | 0.1721 | exact | PASS | definition |
| SEL-MAXLOAD-bokkura | bokkura: service load within the 100 % hard limit | 0.1721 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-bokkura | bokkura: propeller efficiency equals J*KT/(2*pi*KQ) | 0.5758 |  | exact | PASS |  |
| SEL-D-bokkura | bokkura: propeller diameter positive and physical | 0.4410 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-bokkura | bokkura: P/D inside the B-series band | 0.7191 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-bokkura | bokkura: blade area covers the cavitation requirement | EAR=0.350 EARreq=0.298 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-bokkura | bokkura: rejected candidates are listed with reasons (51) | 51 | > 0 | exact | PASS |  |
| SEL-REJWHY-bokkura | bokkura: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-RIGHTSIZE-bokkura | bokkura: a candidate at 17 % load carries an explicit right-sizing check | present | present | exact | PASS | assessCandidate() checks |
| SEL-OVERSIZE-bokkura | bokkura: a candidate below the 40 % right-sizing band is not presented as plain 'PRELIMINARY ESTIMATE' | FAILED CONSTRAINT | FAILED CONSTRAINT / OUTSIDE VALIDATION DOMAIN | exact | PASS | right-sizing rule |
| SEL-OK-cargo_dhoni | cargo_dhoni yields a candidate (6CH-HTE3 M) | ok | ok | exact | PASS |  |
| SEL-PB-cargo_dhoni | cargo_dhoni: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 80.7419 | 80.7419 | 0.01 % (err -0.000%) | PASS | power ledger definition |
| SEL-PE-cargo_dhoni | cargo_dhoni: P_E = R_T * V_s | 37531.8942 | 37531.8942 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-cargo_dhoni | cargo_dhoni: load = P_B/P_rated | 0.6459 | 0.6459 | exact | PASS | definition |
| SEL-MAXLOAD-cargo_dhoni | cargo_dhoni: service load within the 100 % hard limit | 0.6459 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-cargo_dhoni | cargo_dhoni: propeller efficiency equals J*KT/(2*pi*KQ) | 0.4770 |  | exact | PASS |  |
| SEL-D-cargo_dhoni | cargo_dhoni: propeller diameter positive and physical | 0.9463 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-cargo_dhoni | cargo_dhoni: P/D inside the B-series band | 0.5492 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-cargo_dhoni | cargo_dhoni: blade area covers the cavitation requirement | EAR=0.500 EARreq=0.450 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-cargo_dhoni | cargo_dhoni: rejected candidates are listed with reasons (29) | 29 | > 0 | exact | PASS |  |
| SEL-REJWHY-cargo_dhoni | cargo_dhoni: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-OK-ferry | ferry yields a candidate (6CH-HTE3 M) | ok | ok | exact | PASS |  |
| SEL-PB-ferry | ferry: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 87.6388 | 87.6388 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-ferry | ferry: P_E = R_T * V_s | 43378.6749 | 43378.6749 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-ferry | ferry: load = P_B/P_rated | 0.7011 | 0.7011 | exact | PASS | definition |
| SEL-MAXLOAD-ferry | ferry: service load within the 100 % hard limit | 0.7011 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-ferry | ferry: propeller efficiency equals J*KT/(2*pi*KQ) | 0.5474 |  | exact | PASS |  |
| SEL-D-ferry | ferry: propeller diameter positive and physical | 0.9351 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-ferry | ferry: P/D inside the B-series band | 0.6022 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-ferry | ferry: blade area covers the cavitation requirement | EAR=0.500 EARreq=0.457 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-ferry | ferry: rejected candidates are listed with reasons (27) | 27 | > 0 | exact | PASS |  |
| SEL-REJWHY-ferry | ferry: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-OK-speed_ferry | speed_ferry yields a candidate (6CXBM-GT H) | ok | ok | exact | PASS |  |
| SEL-PB-speed_ferry | speed_ferry: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 190.8672 | 190.8672 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-speed_ferry | speed_ferry: P_E = R_T * V_s | 2.34e+05 | 2.34e+05 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-speed_ferry | speed_ferry: load = P_B/P_rated | 0.7203 | 0.7203 | exact | PASS | definition |
| SEL-MAXLOAD-speed_ferry | speed_ferry: service load within the 100 % hard limit | 0.7203 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-speed_ferry | speed_ferry: propeller efficiency equals J*KT/(2*pi*KQ) | 0.7645 |  | exact | PASS |  |
| SEL-D-speed_ferry | speed_ferry: propeller diameter positive and physical | 0.7360 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-speed_ferry | speed_ferry: P/D inside the B-series band | 1.3979 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-speed_ferry | speed_ferry: blade area covers the cavitation requirement | EAR=0.750 EARreq=0.641 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-speed_ferry | speed_ferry: rejected candidates are listed with reasons (37) | 37 | > 0 | exact | PASS |  |
| SEL-REJWHY-speed_ferry | speed_ferry: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-PDLIMIT-speed_ferry | speed_ferry: P/D = 1.398 on the series boundary is reported to the user | present | present | exact | PASS | designPropeller boundary flags |
| SEL-OK-transfer | transfer yields a candidate (6CH-WUTE M) | ok | ok | exact | PASS |  |
| SEL-PB-transfer | transfer: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 144.4627 | 144.4627 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-transfer | transfer: P_E = R_T * V_s | 1.777e+05 | 1.777e+05 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-transfer | transfer: load = P_B/P_rated | 0.7684 | 0.7684 | exact | PASS | definition |
| SEL-MAXLOAD-transfer | transfer: service load within the 100 % hard limit | 0.7684 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-transfer | transfer: propeller efficiency equals J*KT/(2*pi*KQ) | 0.7674 |  | exact | PASS |  |
| SEL-D-transfer | transfer: propeller diameter positive and physical | 0.6783 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-transfer | transfer: P/D inside the B-series band | 1.3917 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-transfer | transfer: blade area covers the cavitation requirement | EAR=0.700 EARreq=0.604 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-transfer | transfer: rejected candidates are listed with reasons (36) | 36 | > 0 | exact | PASS |  |
| SEL-REJWHY-transfer | transfer: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-PDLIMIT-transfer | transfer: P/D = 1.392 on the series boundary is reported to the user | present | present | exact | PASS | designPropeller boundary flags |
| SEL-OK-safari | safari yields a candidate (6CH-WDTE M) | ok | ok | exact | PASS |  |
| SEL-PB-safari | safari: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 117.6378 | 117.6378 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-safari | safari: P_E = R_T * V_s | 1.106e+05 | 1.106e+05 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-safari | safari: load = P_B/P_rated | 0.7639 | 0.7639 | exact | PASS | definition |
| SEL-MAXLOAD-safari | safari: service load within the 100 % hard limit | 0.7639 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-safari | safari: propeller efficiency equals J*KT/(2*pi*KQ) | 0.5844 |  | exact | PASS |  |
| SEL-D-safari | safari: propeller diameter positive and physical | 0.8631 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-safari | safari: P/D inside the B-series band | 0.6301 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-safari | safari: blade area covers the cavitation requirement | EAR=0.500 EARreq=0.432 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-safari | safari: rejected candidates are listed with reasons (27) | 27 | > 0 | exact | PASS |  |
| SEL-REJWHY-safari | safari: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-OK-dinghy | dinghy yields a candidate (4CHE3 M) | ok | ok | exact | PASS |  |
| SEL-PB-dinghy | dinghy: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 36.1889 | 36.1889 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-dinghy | dinghy: P_E = R_T * V_s | 21156.2878 | 21156.2878 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-dinghy | dinghy: load = P_B/P_rated | 0.6305 | 0.6305 | exact | PASS | definition |
| SEL-MAXLOAD-dinghy | dinghy: service load within the 100 % hard limit | 0.6305 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-dinghy | dinghy: propeller efficiency equals J*KT/(2*pi*KQ) | 0.7293 |  | exact | PASS |  |
| SEL-D-dinghy | dinghy: propeller diameter positive and physical | 0.4125 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-dinghy | dinghy: P/D inside the B-series band | 1.3734 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-dinghy | dinghy: blade area covers the cavitation requirement | EAR=0.600 EARreq=0.599 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-dinghy | dinghy: rejected candidates are listed with reasons (49) | 49 | > 0 | exact | PASS |  |
| SEL-REJWHY-dinghy | dinghy: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |
| SEL-OK-custom | custom yields a candidate (6CH-HTE3 M) | ok | ok | exact | PASS |  |
| SEL-PB-custom | custom: P_B = P_D/(eta_S*eta_G)*(1+sea margin) | 95.1160 | 95.1160 | 0.01 % (err +0.000%) | PASS | power ledger definition |
| SEL-PE-custom | custom: P_E = R_T * V_s | 42411.6778 | 42411.6778 | 0.01 % (err +0.000%) | PASS | definition P_E = R_T V |
| SEL-LOAD-custom | custom: load = P_B/P_rated | 0.7609 | 0.7609 | exact | PASS | definition |
| SEL-MAXLOAD-custom | custom: service load within the 100 % hard limit | 0.7609 | <= 1.0 | exact | PASS |  |
| SEL-ETAO-custom | custom: propeller efficiency equals J*KT/(2*pi*KQ) | 0.4933 |  | exact | PASS |  |
| SEL-D-custom | custom: propeller diameter positive and physical | 0.7908 | 0 < D <= 5 m | exact | PASS | geometry check |
| SEL-PD-custom | custom: P/D inside the B-series band | 0.6245 | 0.5 <= P/D <= 1.4 | exact | PASS | BS_RANGE |
| SEL-CAV-custom | custom: blade area covers the cavitation requirement | EAR=0.700 EARreq=0.605 | EAR >= EARreq | exact | PASS | Burrill/Carmichael + Keller |
| SEL-REJ-custom | custom: rejected candidates are listed with reasons (27) | 27 | > 0 | exact | PASS |  |
| SEL-REJWHY-custom | custom: every rejection carries a reason | 0 | 0 | exact | PASS | rejection-reason audit |

## H edge cases — 8 cases, 8 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| EDGE-FN | Fn > 0.55 on a displacement hull is refused, not extrapolated | Holtrop & Mennen is outside its validation domain at Fn = 0.838 (> 0.55). This h | refused | exact | PASS | domain guard |
| EDGE-V0 | zero speed is refused | Resistance requested at a non-positive or non-finite speed. |  | exact | PASS |  |
| EDGE-NODAYS | missing operating days is an error, not a silent default | Operating profile incomplete or out of range (hours/day 0-24, days/year 1-366, t |  | exact | PASS |  |
| EDGE-NOPROP | 25 kn dinghy with a clearance-limited propeller is refused with a reason | NO ENGINE IN THE DATABASE CAN BE MATCHED TO THIS VESSEL, even with the load, cavitation and duty gates relaxed. Rejected |  | exact | PASS |  |
| EDGE-CAVLIM | an allowable back cavitation above the Carmichael validity band is refused | Cavitation screening failed: required blade-area ratio ∞ > available 0.35 (Burrill/Keller). |  | exact | PASS |  |
| EDGE-TIPOK | tip-speed limit 20 m/s still yields a feasible propeller (re-designed) | True | True | exact | PASS | tip-speed gate |
| EDGE-2PROP | two propellers are matched (per-engine power halves) | True | True | exact | PASS | nProps handling |
| EDGE-DUTY | 5 280 operating hours exceed the M-rating limit and are reported | Duty-cycle limit exceeded for Yanmar M (YANMAR high-speed commercial definitions): annual operation 5,280 h/yr (16.0 h/d |  | exact | PASS |  |

## I in-app tests — 2 cases, 2 pass, 0 fail

| case | what is checked | measured | expected | tol / error | result | source / basis |
|---|---|---|---|---|---|---|
| APP-SELFTEST | the shipped in-app self-test suite runs headless with no failure | 116 pass / 0 fail | 0 fail | exact | PASS | headless jsdom run of fullSelfTest() |
| APP-FIELDS | the UI builds every input field | 49 | >= 40 | exact | PASS | DOM query .field |
