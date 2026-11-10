"""Sheet 10 - verification of the spreadsheet formulas against an independent implementation."""
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from theme import *
from refdata import REF

TOL = 1e-6
SYM = {"RF": "Rf", "RW": "Rw", "RV": "Rv", "RAPP": "Rapp", "RT": "Rt", "ηO": "eta_opt", "ηR": "etaR"}


def build(wb, nm):
    ws = wb.create_sheet("10 Verification")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 50, "B": 11, "C": 17, "D": 17, "E": 13, "F": 10, "G": 3})
    title(ws, "10  VERIFICATION  —  SPREADSHEET FORMULAS AGAINST AN INDEPENDENT IMPLEMENTATION",
          "Every formula of sheets 2, 3 and 4 is typed again here, from first principles, for two reference vessels. "
          "Column C is the live spreadsheet result and column D the value produced by a separate Python implementation "
          "of the same method. The difference must vanish to machine precision.", ncols=6)

    counts = {"n": 0}
    first_data = {"row": None}

    def case_block(r, key, heading):
        res = REF[key]["results"]
        cin = REF[key]["inputs"]
        R = {}
        section(ws, r, heading, ncols=6); r += 1
        thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Python reference"), (5, "Difference"),
                      (6, "Verdict")], height=22)
        r += 1

        def irow(lab, sym, unit, val, fmt, k):
            nonlocal r
            label(ws, r, 1, lab)
            value(ws, r, 2, sym, fmt="@", align="center", size=9)
            inp(ws, r, 3, val, fmt=fmt)
            value(ws, r, 4, unit, fmt="@", align="center", size=9)
            R[k] = "C%d" % r
            r += 1

        def crow(lab, sym, unit, formula, fmt="#,##0.0000", ref=None, tol=TOL):
            nonlocal r
            if first_data["row"] is None:
                first_data["row"] = r
            label(ws, r, 1, lab)
            value(ws, r, 2, sym, fmt="@", align="center", size=9)
            calc(ws, r, 3, formula, fmt=fmt)
            key_ = ref or SYM.get(sym, sym)
            if key_ not in res:
                raise KeyError("%r not in reference results: %s" % (key_, sorted(res)))
            value(ws, r, 4, res[key_], fmt=fmt)
            calc(ws, r, 5, f"=IF(ABS(D{r})<1E-12,C{r}-D{r},(C{r}-D{r})/D{r})", fmt="0.0E+00", size=9)
            calc(ws, r, 6, f'=IF(ABS(E{r})<={tol},"PASS","CHECK")', fmt="@", bold=True)
            ws.cell(row=r, column=6).alignment = Alignment(horizontal="center")
            ws.conditional_formatting.add(f"F{r}", CellIsRule(operator="equal", formula=['"PASS"'],
                                          fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
            ws.conditional_formatting.add(f"F{r}", CellIsRule(operator="equal", formula=['"CHECK"'],
                                          fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
            counts["n"] += 1
            r += 1
            return "C%d" % (r - 1)

        # ---------------------------------------------------------- inputs
        label(ws, r, 1, "INPUTS OF THE REFERENCE CASE", bold=True); r += 1
        irow("Waterline length", "L", "m", cin["L"], "0.000", "L")
        irow("Waterline beam", "B", "m", cin["B"], "0.000", "B")
        irow("Draught, loaded", "T", "m", cin["T"], "0.000", "T")
        irow("Draught at the forward perpendicular", "TF", "m", cin["TF"], "0.000", "TF")
        irow("Displacement volume", "∇", "m³", cin["vol"], "0.000", "vol")
        irow("Block coefficient", "CB", "–", cin["Cb"], "0.0000", "Cb")
        irow("Prismatic coefficient", "CP", "–", cin["Cp"], "0.0000", "Cp")
        irow("Midship coefficient", "CM", "–", cin["Cm"], "0.0000", "Cm")
        irow("Waterplane coefficient", "CWP", "–", cin["Cwp"], "0.0000", "Cwp")
        irow("Longitudinal centre of buoyancy", "lcb", "%L", cin["lcb"], "0.00", "lcb")
        irow("Bulb sectional area", "ABT", "m²", cin["ABT"], "0.000", "ABT")
        irow("Bulb height above the keel", "hB", "m", cin["hB"], "0.000", "hB")
        irow("Transom area", "AT", "m²", cin["AT"], "0.000", "AT")
        irow("Stern-shape coefficient", "Cstern", "–", cin["Cstern"], "0.0", "Cstern")
        irow("Appendage wetted area", "SAPP", "m²", cin["Sapp"], "0.000", "Sapp")
        irow("Appendage factor", "1+k2", "–", cin["k2"], "0.000", "k2")
        irow("Service speed", "VS", "kn", cin["Vs"] / 0.514444, "0.000", "VS")
        irow("Sea margin", "SM", "–", cin["SM"], "0.00", "SM")
        irow("Propeller diameter", "D", "m", cin["D"], "0.000", "D")
        irow("Tip clearance", "c", "m", cin["tip"], "0.000", "tip")
        irow("Number of blades", "Z", "–", cin["Z"], "0", "Z")
        irow("Minimum blade-area ratio", "(AE/A0)min", "–", cin["Ae_min"], "0.00", "Aemin")
        irow("Sea-water temperature", "t", "°C", cin["t_sw"], "0.0", "tsw")
        irow("Density of sea water", "ρ", "kg/m³", 1025.0, "0.0", "rho")
        irow("Kinematic viscosity", "ν", "m²/s", 1.139e-06, "0.00E+00", "nu")
        irow("Gravity", "g", "m/s²", 9.81, "0.00", "g")
        irow("Shaft speed of the propeller check", "n", "rpm", res["n_opt"], "0.0", "n")
        irow("Pitch ratio from the Python solver", "P/D", "–", res["pd_opt"], "0.00000", "pd")
        r += 1

        c = R
        V = f"({c['VS']}*0.514444)"

        section(ws, r, "RESISTANCE  —  HOLTROP & MENNEN 1982", ncols=6, fillc=NAVY_2); r += 1
        rFn = crow("Froude number", "Fn", "–", f"={V}/SQRT({c['g']}*{c['L']})", "0.00000000")
        rS = crow("Wetted surface area", "S", "m²",
                  f"={c['L']}*(2*{c['T']}+{c['B']})*SQRT({c['Cm']})*(0.453+0.4425*{c['Cb']}-0.2862*{c['Cm']}"
                  f"-0.003467*{c['B']}/{c['T']}+0.3696*{c['Cwp']})+2.38*{c['ABT']}/{c['Cb']}", "#,##0.0000")
        crow("Reynolds number", "Rn", "–", f"={V}*{c['L']}/{c['nu']}", "0.00E+00", ref="Re")
        rCf = crow("Friction coefficient (ITTC 1957)", "CF", "–", f"=0.075/(LOG10({V}*{c['L']}/{c['nu']})-2)^2",
                   "0.00000000", ref="Cf")
        rLR = crow("Length of run", "LR", "m",
                   f"={c['L']}*(1-{c['Cp']}+0.06*{c['Cp']}*{c['lcb']}/(4*{c['Cp']}-1))", "0.00000000")
        rc12 = crow("c12", "c12", "–",
                    f"=IF({c['T']}/{c['L']}>=0.05,({c['T']}/{c['L']})^0.2228446,"
                    f"48.2*({c['T']}/{c['L']}-0.02)^2.078+0.479948)", "0.00000000")
        rc13 = crow("c13", "c13", "–", f"=1+0.003*{c['Cstern']}", "0.00000000")
        rk1 = crow("Form factor 1+k1", "1+k1", "–",
                   f"={rc13}*(0.93+{rc12}*({c['B']}/{rLR})^0.92497*(0.95-{c['Cp']})^-0.521448"
                   f"*(1-{c['Cp']}+0.0225*{c['lcb']})^0.6906)", "0.00000000", ref="k1")
        rc7 = crow("c7", "c7", "–",
                   f'=IF({c["B"]}/{c["L"]}<0.11,0.229577*({c["B"]}/{c["L"]})^(1/3),'
                   f'IF({c["B"]}/{c["L"]}<0.25,{c["B"]}/{c["L"]},0.5-0.0625*{c["L"]}/{c["B"]}))', "0.00000000")
        riE = crow("Half angle of entrance", "iE", "°",
                   f"=1+89*EXP(-1*({c['L']}/{c['B']})^0.80856*(1-{c['Cwp']})^0.30484"
                   f"*(1-{c['Cp']}-0.0225*{c['lcb']})^0.6367*({rLR}/{c['B']})^0.34574"
                   f"*(100*{c['vol']}/{c['L']}^3)^0.16302)", "0.00000000")
        rc1 = crow("c1", "c1", "–",
                   f"=2223105*{rc7}^3.78613*({c['T']}/{c['B']})^1.07961*(90-{riE})^-1.37565", "0.00000000")
        rc3 = crow("c3  (bulb)", "c3", "–",
                   f'=IF({c["ABT"]}>0,0.56*{c["ABT"]}^1.5/({c["B"]}*{c["T"]}*(0.31*SQRT({c["ABT"]})+'
                   f'{c["TF"]}-{c["hB"]})),0)', "0.00000000")
        rc2 = crow("c2  (bulb)", "c2", "–", f"=IF({c['ABT']}>0,EXP(-1.89*SQRT({rc3})),1)", "0.00000000")
        rc5 = crow("c5  (transom)", "c5", "–", f"=1-0.8*{c['AT']}/({c['B']}*{c['T']}*{c['Cm']})", "0.00000000")
        rlam = crow("λ  (wave-length parameter)", "λ", "–",
                    f'=IF({c["L"]}/{c["B"]}<12,1.446*{c["Cp"]}-0.03*{c["L"]}/{c["B"]},'
                    f'1.446*{c["Cp"]}-0.36)', "0.00000000", ref="lam")
        rc16 = crow("c16", "c16", "–",
                    f'=IF({c["Cp"]}<0.8,8.07981*{c["Cp"]}-13.8673*{c["Cp"]}^2+6.984388*{c["Cp"]}^3,'
                    f'1.73014-0.7067*{c["Cp"]})', "0.00000000")
        rm1 = crow("m1", "m1", "–",
                   f"=0.0140407*{c['L']}/{c['T']}-1.75254*{c['vol']}^(1/3)/{c['L']}"
                   f"-4.79323*{c['B']}/{c['L']}-{rc16}", "0.00000000")
        rc15 = crow("c15", "c15", "–",
                    f"=IF({c['L']}^3/{c['vol']}<512,-1.69385,IF({c['L']}^3/{c['vol']}<=1727,"
                    f"-1.69385+({c['L']}/{c['vol']}^(1/3)-8)/2.36,0))", "0.00000000")
        rm2 = crow("m2", "m2", "–", f"={rc15}*{c['Cp']}^2*EXP(-0.1*{rFn}^-2)", "0.00000000")
        rRw = crow("Wave resistance", "RW", "N",
                   f"={rc1}*{rc2}*{rc5}*{c['vol']}*{c['rho']}*{c['g']}"
                   f"*EXP({rm1}*{rFn}^-0.9+{rm2}*COS({rlam}/{rFn}^2))", "#,##0.0000", ref="Rw")
        rRf = crow("Friction resistance", "RF", "N",
                   f"=0.5*{c['rho']}*{V}^2*{rS}*{rCf}", "#,##0.0000")
        rRv = crow("Viscous resistance  (1+k1)·RF", "RV", "N", f"={rk1}*{rRf}", "#,##0.0000")
        rc4 = crow("c4", "c4", "–", f"=MIN({c['TF']}/{c['L']},0.04)", "0.00000000")
        rCA = crow("Correlation allowance", "CA", "–",
                   f"=0.006*({c['L']}+100)^-0.16-0.00205+0.003*SQRT({c['L']}/7.5)*{c['Cb']}^4*{rc2}"
                   f"*(0.04-{rc4})", "0.00000000")
        rRA = crow("Air and superstructure resistance", "RA", "N",
                   f"=0.5*{c['rho']}*{V}^2*{rS}*{rCA}", "#,##0.0000")
        rRapp = crow("Appendage resistance", "RAPP", "N",
                     f"=0.5*{c['rho']}*{V}^2*{c['Sapp']}*{c['k2']}*{rCf}", "#,##0.0000")
        rRt = crow("TOTAL RESISTANCE, loaded", "RT", "N", f"={rRv}+{rRapp}+{rRw}+0+0+{rRA}", "#,##0.0000")
        crow("Effective power", "PE", "W", f"={rRt}*{V}", "#,##0.0000", ref="PE")

        section(ws, r, "PROPULSION FACTORS  —  HOLTROP & MENNEN 1982, SINGLE SCREW", ncols=6, fillc=NAVY_2); r += 1
        rcv = crow("cv = (1+k1)·CF + CA", "cv", "–", f"={rk1}*{rCf}+{rCA}", "0.00000000")
        rc8 = crow("c8", "c8", "–",
                   f'=IF({c["B"]}/{c["T"]}>5,{c["B"]}*{rS}/({c["L"]}*{c["D"]}*{c["T"]}),'
                   f'{rS}*(7*{c["B"]}/{c["T"]}-25)/({c["L"]}*{c["D"]}*({c["B"]}/{c["T"]}-3)))', "0.00000000")
        rc9 = crow("c9", "c9", "–", f"=IF({rc8}<28,{rc8},32-16/({rc8}-24))", "0.00000000")
        rc11 = crow("c11", "c11", "–",
                    f"=IF({c['T']}/{c['D']}<2,{c['T']}/{c['D']},0.0833333*({c['T']}/{c['D']})^3+1.33333)",
                    "0.00000000")
        rcp1 = crow("CP1", "CP1", "–", f"=1.45*{c['Cp']}-0.315-0.0225*{c['lcb']}", "0.00000000", ref="Cp1")
        rw = crow("Wake fraction", "w", "–",
                  f"={rc9}*{rcv}*({c['L']}/{c['T']})^0.6459*(0.0661875+1.21756*{rc11}*{rcv}/(1-{rcp1}))"
                  f"+0.24558*SQRT({c['B']}/({c['L']}*(1-{rcp1})))-0.09726/(0.95-{c['Cp']})"
                  f"+0.11434/(0.95-{c['Cb']})+0.75*{c['Cstern']}*{c['Cp']}+0.002*{c['Cstern']}", "0.00000000")
        rc10 = crow("c10", "c10", "–",
                    f'=IF({c["L"]}/{c["B"]}>=5.2,{c["B"]}/{c["L"]},'
                    f'0.25-0.003328402/({c["B"]}/{c["L"]}-0.134615385))', "0.00000000")
        rt = crow("Thrust deduction fraction", "t", "–",
                  f"=0.001979*{c['L']}/({c['B']}-{c['B']}*{rcp1})+1.0585*{rc10}-0.00524"
                  f"-0.1418*{c['D']}^2/({c['B']}*{c['T']})+0.0015*{c['Cstern']}", "0.00000000")
        crow("Hull efficiency", "ηH", "–", f"=(1-{rt})/(1-{rw})", "0.00000000", ref="etaH")

        section(ws, r, "PROPELLER  —  WAGENINGEN B-SERIES, THRUST IDENTITY", ncols=6, fillc=NAVY_2); r += 1
        rRtS = crow("Resistance with sea margin", "RT,S", "N", f"={rRt}*(1+{c['SM']})", "#,##0.0000", ref="Rt_s")
        rh = crow("Shaft immersion", "h", "m", f"={c['T']}-({c['tip']}+{c['D']}/2)", "0.00000000")
        rT = crow("Thrust required", "T", "N", f"={rRtS}/(1-{rt})", "#,##0.0000", ref="thrust")
        rpv = crow("Vapour pressure of sea water", "pv", "Pa",
                   f"=0.61121*EXP(17.502*{c['tsw']}/({c['tsw']}+240.97))*1000", "#,##0.00")
        rKe = crow("Keller minimum blade-area ratio", "(AE/A0)min", "–",
                   f"=(1.3+0.3*{c['Z']})*{rT}/((101325+{c['rho']}*{c['g']}*{rh}-{rpv})*{c['D']}^2)",
                   "0.00000000", ref="keller")
        rAE = crow("Blade-area ratio adopted", "AE/A0", "–",
                   f"=MIN(1.05,CEILING(MAX({rKe},{c['Aemin']}),0.05))", "0.0000", ref="ae")
        retaR = crow("Relative rotative efficiency", "ηR", "–",
                     f"=0.9922-0.05908*{rAE}+0.07424*({c['Cp']}-0.0225*{c['lcb']})", "0.00000000", ref="etaR")
        rVa = crow("Speed of advance", "VA", "m/s", f"={V}*(1-{rw})", "0.00000000", ref="Va")
        rJ = crow("Advance coefficient", "J", "–", f"={rVa}/(({c['n']}/60)*{c['D']})", "0.00000000", ref="J_opt")
        rKq = crow("Thrust coefficient required", "KT,req", "–",
                   f"={rT}/({c['rho']}*({c['n']}/60)^2*{c['D']}^4)", "0.00000000", ref="kt_req_opt")
        rKT = crow("KT at the solved pitch ratio", "KT", "–",
                   f"=SUMPRODUCT(KT_C,{rJ}^KT_S,{c['pd']}^KT_T,{rAE}^KT_U,{c['Z']}^KT_V)", "0.00000000", ref="kt_opt")
        rKQ = crow("KQ at the solved pitch ratio", "KQ", "–",
                   f"=SUMPRODUCT(KQ_C,{rJ}^KQ_S,{c['pd']}^KQ_T,{rAE}^KQ_U,{c['Z']}^KQ_V)", "0.00000000", ref="kq_opt")
        crow("Open-water efficiency", "ηO", "–", f"={rJ}*{rKT}/(2*PI()*{rKQ})", "0.00000000", ref="eta_opt")
        rQ = crow("Torque", "Q", "N·m", f"={rKQ}*{c['rho']}*({c['n']}/60)^2*{c['D']}^5", "#,##0.0000", ref="Q_opt")
        crow("Delivered power", "PD", "kW", f"=2*PI()*({c['n']}/60)*{rQ}/{retaR}/1000",
             "#,##0.0000", ref="PD_opt")
        r += 1
        return r

    r = 6
    r = case_block(r, "DHONI", "A.  REFERENCE CASE 1  —  30 m PASSENGER DHONI, 9 kn")
    r = case_block(r + 1, "FERRY", "B.  REFERENCE CASE 2  —  48 m PASSENGER FERRY, 11 kn")

    section(ws, r, "C.  RESULT", ncols=6); r += 1
    label(ws, r, 1, "Comparisons made", bold=True)
    calc(ws, r, 3, counts["n"], fmt="0")
    rc_n = r
    r += 1
    label(ws, r, 1, "Passed to 1 × 10⁻⁶ relative difference", bold=True)
    calc(ws, r, 3, f'=COUNTIF(F{first_data["row"]}:F{first_data["row"] + counts["n"] + 40},"PASS")', fmt="0")
    r += 1
    label(ws, r, 1, "STATUS", bold=True)
    result(ws, r, 3, f'=IF(C{r-1}=C{rc_n},"ALL CHECKS PASS","REVIEW")', fmt="@")
    ws.cell(row=r, column=3).alignment = Alignment(horizontal="center")
    return ws
