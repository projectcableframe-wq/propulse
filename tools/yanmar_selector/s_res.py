"""Sheet 2 - Holtrop & Mennen resistance."""
from openpyxl.chart import LineChart, BarChart, Reference
from theme import *

N_SWEEP = 21


def build(wb, nm):
    ws = wb.create_sheet("2 Resistance")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 52, "B": 13, "C": 15, "D": 9, "E": 60,
                "F": 9.5, "G": 9.5, "H": 9.5, "I": 9.5, "J": 9.5, "K": 9.5, "L": 9.5,
                "M": 9.5, "N": 9.5, "O": 10.5, "P": 10, "Q": 10, "R": 9, "S": 9})
    title(ws, "2  RESISTANCE  —  HOLTROP & MENNEN (1982)",
          "Every coefficient of the method is calculated and listed with its equation. The design point is evaluated "
          "exactly at the service speed; the sweep below it produces the resistance curve.", ncols=19)

    r = 4
    D = {}   # references collected
    for cond in ({"key": "L", "T": "T_LOAD", "VOL": "VOL_LOAD", "AT": "AT_LOAD", "TF": "TF_LOAD",
                  "label": "A.  LOADED CONDITION  —  design condition for engine and propeller sizing"},
                 {"key": "B", "T": "T_BAL", "VOL": "VOL_BAL", "AT": "AT_BAL", "TF": "T_BAL",
                  "label": "B.  BALLAST / UNLOADED CONDITION  —  used for the checks only"}):
        section(ws, r, cond["label"], ncols=19); r += 1
        thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Unit"), (5, "Equation as applied")], height=20)
        r += 1
        T, VOL, AT, TF, K = cond["T"], cond["VOL"], cond["AT"], cond["TF"], cond["key"]
        ref = {}

        def row(lab, sym, formula, unit, eq, fmt="0.000", name=None, bold=False, isres=False):
            nonlocal r
            label(ws, r, 1, lab, bold=bold)
            value(ws, r, 2, sym, fmt="@", align="center", size=9)
            if isres:
                result(ws, r, 3, formula, fmt=fmt)
            else:
                calc(ws, r, 3, formula, fmt=fmt, bold=bold)
            value(ws, r, 4, unit, fmt="@", align="center")
            note(ws, r, 5, eq, size=8, span=5)
            if name:
                nm.add(name, "C%d" % r)
            r += 1
            return r - 1

        ref["V"] = row("Ship speed", "V", "=VS_KN*0.514444", "m/s", "V = VS × 0.514444")
        ref["Fn"] = row("Froude number", "Fn", f"=C{ref['V']}/SQRT(G_*L_WL)", "–", "Fn = V / √(g·LWL)")
        ref["Rn"] = row("Reynolds number", "Rn", f"=C{ref['V']}*L_WL/NU_W", "–", "Rn = V·LWL / ν", "0.000E+00")
        ref["Cf"] = row("ITTC-1957 friction coefficient", "CF", f"=0.075/(LOG10(C{ref['Rn']})-2)^2", "–",
                        "CF = 0.075 / [log10(Rn) − 2]²", "0.000000", name=f"CF_{K}")
        ref["S"] = row("Wetted surface area (Holtrop approximation)", "S",
                       f"=L_WL*(2*{T}+B_MLD)*SQRT(CM_)*(0.453+0.4425*CB_-0.2862*CM_-0.003467*B_MLD/{T}+0.3696*CWP_)+2.38*ABT_/CB_",
                       "m²", "S = L(2T+B)√CM[0.453+0.4425CB−0.2862CM−0.003467B/T+0.3696CWP] + 2.38·ABT/CB",
                       "#,##0.0", name=f"S_{'LOAD' if K == 'L' else 'BAL'}", bold=True)
        ref["RF"] = row("Frictional resistance", "RF", f"=0.5*RHO_W*C{ref['V']}^2*C{ref['S']}*C{ref['Cf']}", "N",
                        "RF = ½·ρ·V²·S·CF", "#,##0")
        ref["LR"] = row("Length of run", "LR", "=L_WL*(1-CP_+0.06*CP_*LCB_/(4*CP_-1))", "m",
                        "LR = L·[1 − CP + 0.06·CP·lcb/(4CP − 1)]", "0.000")
        ref["c12"] = row("Coefficient c12", "c12",
                         f"=IF({T}/L_WL>=0.05,({T}/L_WL)^0.2228446,IF({T}/L_WL>0.02,48.2*({T}/L_WL-0.02)^2.078+0.479948,0.479948))",
                         "–", "c12 = (T/L)^0.2228446 ; 48.20(T/L−0.02)^2.078+0.479948 ; 0.479948  (three T/L ranges)",
                         "0.00000")
        ref["c13"] = row("Stern-shape coefficient", "c13", "=1+0.003*CSTERN_", "–", "c13 = 1 + 0.003·Cstern", "0.0000")
        ref["k1"] = row("Form factor", "1+k1",
                        f"=IF(ISNUMBER(K1_OVR),K1_OVR,C{ref['c13']}*(0.93+C{ref['c12']}*(B_MLD/C{ref['LR']})^0.92497*(0.95-CP_)^-0.521448*(1-CP_+0.0225*LCB_)^0.6906))",
                        "–", "1+k1 = c13·[0.93 + c12·(B/LR)^0.92497·(0.95−CP)^−0.521448·(1−CP+0.0225lcb)^0.6906]",
                        "0.0000", name=f"K1_{K}", bold=True)
        ref["RV"] = row("Viscous resistance", "RV", f"=C{ref['k1']}*C{ref['RF']}", "N", "RV = (1+k1)·RF", "#,##0")
        ref["c7"] = row("Coefficient c7", "c7",
                        "=IF(B_MLD/L_WL<0.11,0.229577*(B_MLD/L_WL)^0.33333333,IF(B_MLD/L_WL<=0.25,B_MLD/L_WL,0.5-0.0625*L_WL/B_MLD))",
                        "–", "c7 = 0.229577(B/L)^0.33333 ; B/L ; 0.5−0.0625L/B", "0.00000")
        ref["iE"] = row("Half angle of entrance", "iE",
                        f"=1+89*EXP(-1*(L_WL/B_MLD)^0.80856*(1-CWP_)^0.30484*(1-CP_-0.0225*LCB_)^0.6367*(C{ref['LR']}/B_MLD)^0.34574*(100*{VOL}/L_WL^3)^0.16302)",
                        "deg", "iE = 1 + 89·exp{−(L/B)^0.80856(1−CWP)^0.30484(1−CP−0.0225lcb)^0.6367(LR/B)^0.34574(100∇/L³)^0.16302}",
                        "0.00")
        ref["c1"] = row("Wave-resistance coefficient c1", "c1",
                        f"=2223105*C{ref['c7']}^3.78613*({T}/B_MLD)^1.07961*(90-C{ref['iE']})^-1.37565", "–",
                        "c1 = 2223105·c7^3.78613·(T/B)^1.07961·(90−iE)^−1.37565", "0.0000")
        ref["c3"] = row("Bulb coefficient c3", "c3",
                        f"=IF(ABT_>0,0.56*ABT_^1.5/(B_MLD*{T}*(0.31*SQRT(ABT_)+{TF}-HB_)),0)", "–",
                        "c3 = 0.56·ABT^1.5/[B·T·(0.31√ABT + TF − hB)]   (0 if no bulb)", "0.00000")
        ref["c2"] = row("Bulb coefficient c2", "c2", f"=IF(ABT_>0,EXP(-1.89*SQRT(C{ref['c3']})),1)", "–",
                        "c2 = exp(−1.89·√c3)   (1.0 if no bulb)", "0.00000")
        ref["c5"] = row("Transom coefficient c5", "c5", f"=1-0.8*{AT}/(B_MLD*{T}*CM_)", "–", "c5 = 1 − 0.8·AT/(B·T·CM)",
                        "0.00000")
        ref["lam"] = row("Wave-length parameter", "λ", "=IF(L_WL/B_MLD<12,1.446*CP_-0.03*L_WL/B_MLD,1.446*CP_-0.36)", "–",
                         "λ = 1.446CP − 0.03L/B (L/B<12);  1.446CP − 0.36 (L/B≥12)", "0.0000")
        ref["c16"] = row("Coefficient c16", "c16",
                         "=IF(CP_<0.8,8.07981*CP_-13.8673*CP_^2+6.984388*CP_^3,1.73014-0.7067*CP_)", "–",
                         "c16 = 8.07981CP − 13.8673CP² + 6.984388CP³ (CP<0.8); 1.73014 − 0.7067CP (CP≥0.8)", "0.0000")
        ref["m1"] = row("Exponent m1", "m1",
                        f"=0.0140407*L_WL/{T}-1.75254*{VOL}^(1/3)/L_WL-4.79323*B_MLD/L_WL-C{ref['c16']}", "–",
                        "m1 = 0.0140407·L/T − 1.75254·∇^⅓/L − 4.79323·B/L − c16", "0.0000")
        ref["c15"] = row("Coefficient c15", "c15",
                         f"=IF(L_WL^3/{VOL}<512,-1.69385,IF(L_WL^3/{VOL}<=1727,-1.69385+(L_WL/{VOL}^(1/3)-8)/2.36,0))",
                         "–", "c15 = −1.69385 ; −1.69385+(L/∇^⅓−8)/2.36 ; 0   (three L³/∇ ranges)", "0.00000")
        ref["m2"] = row("Exponent m2", "m2", f"=C{ref['c15']}*CP_^2*EXP(-0.1/C{ref['Fn']}^2)", "–",
                        "m2 = c15·CP²·exp(−0.1·Fn⁻²)", "0.00000")
        ref["exp"] = row("Exponential term", "exp{…}",
                         f"=EXP(C{ref['m1']}*C{ref['Fn']}^-0.9+C{ref['m2']}*COS(C{ref['lam']}/C{ref['Fn']}^2))", "–",
                         "exp[m1·Fn^−0.9 + m2·cos(λ/Fn²)]", "0.00000")
        ref["RW"] = row("Wave-making resistance", "RW", f"=C{ref['c1']}*C{ref['c2']}*C{ref['c5']}*{VOL}*RHO_W*G_*C{ref['exp']}",
                        "N", "RW = c1·c2·c5·∇·ρ·g·exp[m1Fn^−0.9 + m2cos(λ/Fn²)]", "#,##0")
        ref["PB"] = row("Bulb emergence parameter", "PB", f"=IF(ABT_>0,0.56*SQRT(ABT_)/({TF}-1.5*HB_),0)", "–",
                        "PB = 0.56√ABT/(TF − 1.5hB)", "0.0000")
        ref["Fni"] = row("Bulb Froude number", "Fni",
                         f"=IF(ABT_>0,C{ref['V']}/SQRT(G_*({TF}-HB_-0.25*SQRT(ABT_)))+0.15*C{ref['V']}^2,0)", "–",
                         "Fni = V/√[g(TF − hB − 0.25√ABT)] + 0.15V²", "0.0000")
        ref["RB"] = row("Bulbous-bow pressure resistance", "RB",
                        f"=IF(ABT_>0,0.11*EXP(-3*C{ref['PB']}^-2)*C{ref['Fni']}^3*ABT_^1.5*RHO_W*G_/(1+C{ref['Fni']}^2),0)",
                        "N", "RB = 0.11·exp(−3PB⁻²)·Fni³·ABT^1.5·ρg/(1+Fni²)", "#,##0")
        ref["FnT"] = row("Transom Froude number", "FnT",
                         f"=IF({AT}>0,C{ref['V']}/SQRT(2*G_*{AT}/(B_MLD+B_MLD*CWP_)),0)", "–",
                         "FnT = V/√[2g·AT/(B + B·CWP)]", "0.000")
        ref["c6"] = row("Transom coefficient", "c6", f"=IF({AT}>0,IF(C{ref['FnT']}<5,0.2*(1-0.2*C{ref['FnT']}),0),0)", "–",
                        "c6 = 0.2(1 − 0.2FnT) for FnT<5, else 0", "0.0000")
        ref["RTR"] = row("Transom pressure resistance", "RTR", f"=0.5*RHO_W*C{ref['V']}^2*{AT}*C{ref['c6']}", "N",
                         "RTR = ½ρV²·AT·c6", "#,##0")
        ref["c4"] = row("Coefficient c4", "c4", f"=MIN({TF}/L_WL,0.04)", "–", "c4 = min(TF/L, 0.04)", "0.00000")
        ref["CA"] = row("Correlation allowance coefficient", "CA",
                        f"=0.006*(L_WL+100)^-0.16-0.00205+0.003*SQRT(L_WL/7.5)*CB_^4*C{ref['c2']}*(0.04-C{ref['c4']})",
                        "–", "CA = 0.006(L+100)^−0.16 − 0.00205 + 0.003√(L/7.5)·CB⁴·c2·(0.04 − c4)", "0.000000",
                        name=f"CA_{K}")
        ref["RA"] = row("Correlation resistance", "RA", f"=0.5*RHO_W*C{ref['V']}^2*C{ref['S']}*C{ref['CA']}", "N",
                        "RA = ½ρV²·S·CA", "#,##0")
        ref["Rapp"] = row("Appendage resistance", "RAPP", f"=0.5*RHO_W*C{ref['V']}^2*S_APP*K2_EQ*C{ref['Cf']}", "N",
                          "RAPP = ½ρV²·SAPP·(1+k2)eq·CF", "#,##0")
        ref["RT"] = row("TOTAL RESISTANCE", "RT",
                        f"=C{ref['RV']}+C{ref['Rapp']}+C{ref['RW']}+C{ref['RB']}+C{ref['RTR']}+C{ref['RA']}", "N",
                        "RT = RV + RAPP + RW + RB + RTR + RA", "#,##0",
                        name=f"RT_{'L' if K == 'L' else 'B'}", bold=True, isres=True)
        ref["PE"] = row("EFFECTIVE POWER", "PE", f"=C{ref['RT']}*C{ref['V']}/1000", "kW", "PE = RT·V", "#,##0.0",
                        name=f"PE_{'L' if K == 'L' else 'B'}", bold=True, isres=True)
        D[K] = ref
        r += 2

    # ---------------- speed sweep ----------------
    r += 1
    section(ws, r, "C.  SPEED SWEEP  —  resistance curve for the charts and for the trial-speed check", ncols=19)
    r += 1
    hdr = r
    thead(ws, r, [(1, "Point"), (2, "VS [kn]"), (3, "V [m/s]"), (4, "Fn"), (5, "Rn"), (6, "CF"),
                  (7, "RF [N]"), (8, "RV [N]"), (9, "RW [N]"), (10, "RB [N]"), (11, "RTR [N]"),
                  (12, "CA"), (13, "RA [N]"), (14, "RAPP [N]"), (15, "RT [N]"), (16, "PE [kW]"),
                  (17, "RT/Δ [N/t]"), (18, "FnT"), (19, "Fni")], height=40)
    r += 1
    first = r
    L = D["L"]
    for i in range(N_SWEEP):
        frac = 0.40 + (1.35 - 0.40) * i / (N_SWEEP - 1)
        value(ws, r, 1, i + 1, fmt="0", align="center")
        calc(ws, r, 2, f"=VS_KN*{frac:.4f}", fmt="0.00")
        calc(ws, r, 3, f"=B{r}*0.514444", fmt="0.000")
        calc(ws, r, 4, f"=C{r}/SQRT(G_*L_WL)", fmt="0.00000")
        calc(ws, r, 5, f"=C{r}*L_WL/NU_W", fmt="0.000E+00")
        calc(ws, r, 6, f"=0.075/(LOG10(E{r})-2)^2", fmt="0.000000")
        calc(ws, r, 7, f"=0.5*RHO_W*C{r}^2*S_LOAD*F{r}", fmt="#,##0")
        calc(ws, r, 8, f"=G{r}*K1_L", fmt="#,##0")
        calc(ws, r, 9, f"=C{L['c1']}*C{L['c2']}*C{L['c5']}*VOL_LOAD*RHO_W*G_*EXP(C{L['m1']}*D{r}^-0.9+C{L['m2']}*COS(C{L['lam']}/D{r}^2))", fmt="#,##0")
        calc(ws, r, 10, f"=IF(ABT_>0,0.11*EXP(-3*C{L['PB']}^-2)*(C{r}/SQRT(G_*(TF_LOAD-HB_-0.25*SQRT(ABT_)))+0.15*C{r}^2)^3*ABT_^1.5*RHO_W*G_/(1+(C{r}/SQRT(G_*(TF_LOAD-HB_-0.25*SQRT(ABT_)))+0.15*C{r}^2)^2),0)", fmt="#,##0")
        calc(ws, r, 11, f"=IF(AT_LOAD>0,0.5*RHO_W*C{r}^2*AT_LOAD*IF(R{r}<5,0.2*(1-0.2*R{r}),0),0)", fmt="#,##0")
        calc(ws, r, 12, f"=0.006*(L_WL+100)^-0.16-0.00205+0.003*SQRT(L_WL/7.5)*CB_^4*C{L['c2']}*(0.04-C{L['c4']})", fmt="0.000000")
        calc(ws, r, 13, f"=0.5*RHO_W*C{r}^2*S_LOAD*L{r}", fmt="#,##0")
        calc(ws, r, 14, f"=0.5*RHO_W*C{r}^2*S_APP*K2_EQ*F{r}", fmt="#,##0")
        calc(ws, r, 15, f"=H{r}+N{r}+I{r}+J{r}+K{r}+M{r}", fmt="#,##0", bold=True)
        calc(ws, r, 16, f"=O{r}*C{r}/1000", fmt="#,##0.0", bold=True)
        calc(ws, r, 17, f"=O{r}/(VOL_LOAD*RHO_W/1000)", fmt="#,##0.00")
        calc(ws, r, 18, f"=IF(AT_LOAD>0,C{r}/SQRT(2*G_*AT_LOAD/(B_MLD+B_MLD*CWP_)),0)", fmt="0.000")
        calc(ws, r, 19, f"=IF(ABT_>0,C{r}/SQRT(G_*(TF_LOAD-HB_-0.25*SQRT(ABT_)))+0.15*C{r}^2,0)", fmt="0.000")
        r += 1
    last = r - 1
    nm.add("SW_VS", f"'2 Resistance'!$B${first}:$B${last}")
    nm.add("SW_RT", f"'2 Resistance'!$O${first}:$O${last}")
    nm.add("SW_PE", f"'2 Resistance'!$P${first}:$P${last}")

    ch = LineChart(); ch.title = "Total resistance vs speed"; ch.style = 2
    ch.y_axis.title = "RT  [N]"; ch.x_axis.title = "VS  [kn]"; ch.height = 8.5; ch.width = 16
    ch.add_data(Reference(ws, min_col=15, min_row=hdr, max_row=last), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=2, min_row=first, max_row=last))
    ws.add_chart(ch, "A%d" % (last + 3))

    ch2 = LineChart(); ch2.title = "Effective power vs speed"; ch2.style = 2
    ch2.y_axis.title = "PE  [kW]"; ch2.x_axis.title = "VS  [kn]"; ch2.height = 8.5; ch2.width = 16
    ch2.add_data(Reference(ws, min_col=16, min_row=hdr, max_row=last), titles_from_data=True)
    ch2.set_categories(Reference(ws, min_col=2, min_row=first, max_row=last))
    ws.add_chart(ch2, "F%d" % (last + 3))

    br = last + 22
    label(ws, br, 1, "Resistance component", bold=True); label(ws, br, 2, "N", bold=True)
    comps = [("Friction RV", f"=C{L['RV']}"), ("Wave RW", f"=C{L['RW']}"), ("Bulb RB", f"=C{L['RB']}"),
             ("Transom RTR", f"=C{L['RTR']}"), ("Correlation RA", f"=C{L['RA']}"), ("Appendages RAPP", f"=C{L['Rapp']}")]
    for i, (lab, f) in enumerate(comps):
        label(ws, br + 1 + i, 1, lab, size=9)
        calc(ws, br + 1 + i, 2, f, fmt="#,##0")
    ch3 = BarChart(); ch3.type = "bar"; ch3.title = "Resistance components at service speed (loaded)"
    ch3.height = 8; ch3.width = 15
    ch3.add_data(Reference(ws, min_col=2, min_row=br, max_row=br + len(comps)), titles_from_data=True)
    ch3.set_categories(Reference(ws, min_col=1, min_row=br + 1, max_row=br + len(comps)))
    ws.add_chart(ch3, "K%d" % (last + 22))

    ws.freeze_panes = "A4"
    return ws
