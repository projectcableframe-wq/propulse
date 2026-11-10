"""Sheet 3 - Propulsion factors and power balance."""
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from theme import *


def build(wb, nm):
    ws = wb.create_sheet("3 Propulsion")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 50, "B": 14, "C": 15, "D": 15, "E": 10, "F": 62, "G": 2})
    title(ws, "3  PROPULSION  —  HULL/PROPELLER INTERACTION AND POWER BALANCE",
          "Wake fraction, thrust deduction and relative rotative efficiency are the Holtrop & Mennen (1982) "
          "single-screw regressions applied to the propeller diameter and blade area actually selected on sheet 4.",
          ncols=6)

    r = 4
    hdr = r
    thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "LOADED"), (4, "BALLAST"), (5, "Unit"), (6, "Equation as applied")],
          height=30)
    r += 1

    def row(lab, sym, fl, fb, unit, eq, fmt="0.0000", name_l=None, name_b=None, bold=False, isres=False):
        nonlocal r
        label(ws, r, 1, lab, bold=bold)
        value(ws, r, 2, sym, fmt="@", align="center", size=9)
        for col, f in ((3, fl), (4, fb)):
            if f is None:
                value(ws, r, col, "", fmt="@")
            elif isres:
                result(ws, r, col, f, fmt=fmt)
            else:
                calc(ws, r, col, f, fmt=fmt, bold=bold)
        value(ws, r, 5, unit, fmt="@", align="center")
        note(ws, r, 6, eq, size=8)
        if name_l: nm.add(name_l, "C%d" % r)
        if name_b: nm.add(name_b, "D%d" % r)
        r += 1
        return r - 1

    section(ws, r, "A.  QUANTITIES TAKEN FROM THE RESISTANCE CALCULATION (sheet 2)", ncols=6); r += 1
    row("Length on waterline", "L", "=L_WL", "=L_WL", "m", "Input")
    row("Beam, moulded", "B", "=B_MLD", "=B_MLD", "m", "Input")
    row("Draft", "Ta", "=T_LOAD", "=T_BAL", "m", "Input (draft of the condition)")
    row("Block coefficient", "CB", "=CB_", "=CB_", "–", "Input")
    row("Prismatic coefficient", "CP", "=CP_", "=CP_", "–", "Input")
    row("LCB", "lcb", "=LCB_", "=LCB_", "% L", "Input")
    row("Wetted surface area", "S", "=S_LOAD", "=S_BAL", "m²", "Sheet 2")
    row("Friction coefficient", "CF", "=CF_L", "=CF_B", "–", "Sheet 2", "0.000000")
    row("Correlation allowance", "CA", "=CA_L", "=CA_B", "–", "Sheet 2", "0.000000")
    row("Form factor", "1+k1", "=K1_L", "=K1_B", "–", "Sheet 2")
    row("Propeller diameter (design)", "D", "=D_PROP", "=D_PROP", "m", "Sheet 4 – from the aperture")
    row("Blade-area ratio (design)", "AE/A0", "=AE_PROP", "=AE_PROP", "–", "Sheet 4 – Keller criterion")
    r += 1

    section(ws, r, "B.  HULL / PROPELLER INTERACTION  (Holtrop & Mennen 1982, single screw)", ncols=6); r += 1
    r_cv = row("Viscous resistance coefficient", "CV", "=K1_L*CF_L+CA_L", "=K1_B*CF_B+CA_B", "–",
               "CV = (1+k1)·CF + CA")
    r_c8 = row("Coefficient c8", "c8",
               f"=IF(B_MLD/T_LOAD>5,B_MLD*S_LOAD/(L_WL*D_PROP*T_LOAD),S_LOAD*(7*B_MLD/T_LOAD-25)/(L_WL*D_PROP*(B_MLD/T_LOAD-3)))",
               f"=IF(B_MLD/T_BAL>5,B_MLD*S_BAL/(L_WL*D_PROP*T_BAL),S_BAL*(7*B_MLD/T_BAL-25)/(L_WL*D_PROP*(B_MLD/T_BAL-3)))",
               "–", "c8 = B·S/(L·D·Ta)  if B/Ta>5 ;  c8 = S(7B/Ta−25)/[L·D(B/Ta−3)]  if B/Ta<5")
    r_c9 = row("Coefficient c9", "c9", f"=IF(C{r_c8}<28,C{r_c8},32-16/(C{r_c8}-24))",
               f"=IF(D{r_c8}<28,D{r_c8},32-16/(D{r_c8}-24))", "–", "c9 = c8 if c8<28 ;  c9 = 32 − 16/(c8−24) if c8>28")
    r_c11 = row("Coefficient c11", "c11", "=IF(T_LOAD/D_PROP<2,T_LOAD/D_PROP,0.0833333*(T_LOAD/D_PROP)^3+1.33333)",
                "=IF(T_BAL/D_PROP<2,T_BAL/D_PROP,0.0833333*(T_BAL/D_PROP)^3+1.33333)", "–",
                "c11 = Ta/D if Ta/D<2 ;  0.0833333(Ta/D)³+1.33333 if Ta/D>2")
    r_cp1 = row("Afterbody prismatic coefficient", "CP1", "=1.45*CP_-0.315-0.0225*LCB_", "=1.45*CP_-0.315-0.0225*LCB_",
                "–", "CP1 = 1.45·CP − 0.315 − 0.0225·lcb")
    r_w = row("WAKE FRACTION", "w",
              f"=IF(ISNUMBER(W_OVR),W_OVR,C{r_c9}*C{r_cv}*(L_WL/T_LOAD)^0.6459*(0.0661875+1.21756*C{r_c11}*C{r_cv}/(1-C{r_cp1}))+0.24558*SQRT(B_MLD/(L_WL*(1-C{r_cp1})))-0.09726/(0.95-CP_)+0.11434/(0.95-CB_)+0.75*CSTERN_*CP_+0.002*CSTERN_)",
              f"=IF(ISNUMBER(W_OVR),W_OVR,D{r_c9}*D{r_cv}*(L_WL/T_BAL)^0.6459*(0.0661875+1.21756*D{r_c11}*D{r_cv}/(1-D{r_cp1}))+0.24558*SQRT(B_MLD/(L_WL*(1-D{r_cp1})))-0.09726/(0.95-CP_)+0.11434/(0.95-CB_)+0.75*CSTERN_*CP_+0.002*CSTERN_)",
              "–",
              "w = c9·CV·(L/Ta)^0.6459·(0.0661875 + 1.21756·c11·CV/(1−CP1)) + 0.24558√[B/(L(1−CP1))] − 0.09726/(0.95−CP) + 0.11434/(0.95−CB) + 0.75·Cstern·CP + 0.002·Cstern",
              name_l="W_L", name_b="W_B", bold=True)
    r_c10 = row("Coefficient c10", "c10",
                "=IF(L_WL/B_MLD>5.2,B_MLD/L_WL,0.25-0.003328402/(B_MLD/L_WL-0.134615385))",
                "=IF(L_WL/B_MLD>5.2,B_MLD/L_WL,0.25-0.003328402/(B_MLD/L_WL-0.134615385))", "–",
                "c10 = B/L if L/B>5.2 ;  0.25 − 0.003328402/(B/L − 0.134615385) if L/B<5.2")
    r_t = row("THRUST DEDUCTION", "t",
              f"=IF(ISNUMBER(T_OVR),T_OVR,0.001979*L_WL/(B_MLD-B_MLD*C{r_cp1})+1.0585*C{r_c10}-0.00524-0.1418*D_PROP^2/(B_MLD*T_LOAD)+0.0015*CSTERN_)",
              f"=IF(ISNUMBER(T_OVR),T_OVR,0.001979*L_WL/(B_MLD-B_MLD*D{r_cp1})+1.0585*D{r_c10}-0.00524-0.1418*D_PROP^2/(B_MLD*T_BAL)+0.0015*CSTERN_)",
              "–", "t = 0.001979·L/[B(1−CP1)] + 1.0585·c10 − 0.00524 − 0.1418·D²/(B·T) + 0.0015·Cstern",
              name_l="T_L", name_b="T_B", bold=True)
    r_er = row("RELATIVE ROTATIVE EFFICIENCY", "ηR",
               "=IF(ISNUMBER(ETA_R_OVR),ETA_R_OVR,0.9922-0.05908*AE_PROP+0.07424*(CP_-0.0225*LCB_))",
               "=IF(ISNUMBER(ETA_R_OVR),ETA_R_OVR,0.9922-0.05908*AE_PROP+0.07424*(CP_-0.0225*LCB_))",
               "–", "ηR = 0.9922 − 0.05908·AE/A0 + 0.07424·(CP − 0.0225·lcb)", name_l="ETA_R_L", name_b="ETA_R_B", bold=True)
    r_eh = row("HULL EFFICIENCY", "ηH", f"=(1-C{r_t})/(1-C{r_w})", f"=(1-D{r_t})/(1-D{r_w})", "–",
               "ηH = (1 − t)/(1 − w)", name_l="ETA_H_L", name_b="ETA_H_B", bold=True)
    r += 1

    section(ws, r, "C.  THRUST AND SPEED OF ADVANCE", ncols=6); r += 1
    r_rt = row("Calm-water resistance at service speed", "RT", "=RT_L", "=RT_B", "N", "Sheet 2", "#,##0")
    r_rts = row("Service resistance (sea margin applied)", "RT,s", "=RT_L*(1+SM_/100)", "=RT_B*(1+SM_/100)", "N",
                "RT,s = RT·(1 + sea margin)", "#,##0", name_l="RT_S_L", name_b="RT_S_B")
    r_tr = row("REQUIRED THRUST", "T", f"=C{r_rts}/(1-C{r_t})", f"=D{r_rts}/(1-D{r_t})", "N", "T = RT,s/(1 − t)",
               "#,##0", name_l="THRUST_L", name_b="THRUST_B", bold=True, isres=True)
    r_va = row("SPEED OF ADVANCE", "VA", f"=VS_KN*0.514444*(1-C{r_w})", f"=VS_KN*0.514444*(1-D{r_w})", "m/s",
               "VA = VS·(1 − w)", "0.0000", name_l="VA_L", name_b="VA_B", bold=True)
    r_tp = row("Thrust power (propeller)", "PT", f"=C{r_tr}*C{r_va}/1000", f"=D{r_tr}*D{r_va}/1000", "kW",
               "PT = T·VA", "#,##0.0")
    row("Thrust loading (propeller)", "CT", "=THRUST_L/(0.5*RHO_W*VA_L^2*3.14159265*D_PROP^2/4)",
        "=THRUST_B/(0.5*RHO_W*VA_B^2*3.14159265*D_PROP^2/4)", "–", "CT = T/(½ρVA²·πD²/4)", "0.000")
    r += 1

    section(ws, r, "D.  POWER BALANCE AT THE SELECTED DESIGN POINT  (live link to sheets 4 and 5)", ncols=6); r += 1
    row("Propeller speed at engine MCR", "n", "=FIN_N", None, "rpm", "Sheet 4 – n = engine rpm / gear ratio", "#,##0",
        name_l="N_PROP")
    row("Pitch ratio", "P/D", "=FIN_PD", None, "–", "Sheet 4 – bisection solution of KT(J,P/D) = KT,req")
    row("Open-water efficiency", "ηO", "=FIN_ETAO", None, "–", "ηO = J·KT/(2π·KQ)")
    row("Total propulsive efficiency", "ηD", "=FIN_ETAD", None, "–", "ηD = ηH·ηO·ηR")
    row("DELIVERED POWER at the propeller", "PD", "=FIN_PD_KW", None, "kW", "PD = 2π·n·Q/ηR = PE·(1+SM)/(ηH·ηO·ηR)",
        "#,##0.0", name_l="PD_DESIGN", bold=True, isres=True)
    row("Shaft power", "PS", "=PD_DESIGN/ETA_S", None, "kW", "PS = PD/ηS", "#,##0.0", name_l="PS_DESIGN")
    row("BRAKE POWER required at service speed", "PB", "=PS_DESIGN/ETA_G", None, "kW", "PB = PS/ηG", "#,##0.0",
        name_l="PB_DESIGN", bold=True, isres=True)
    row("Required engine MCR (engine margin applied)", "PMCR", "=PB_DESIGN/(1-EM_/100)", None, "kW",
        "PMCR,req = PB/(1 − engine margin)", "#,##0.0", name_l="PMCR_REQ", bold=True, isres=True)
    r += 1

    section(ws, r, "E.  REASONABLENESS CHECKS ON THE INTERACTION COEFFICIENTS", ncols=6); r += 1
    for lab, sym, fl, fb, lo, hi, eq in [
        ("Wake fraction in the range 0.10 – 0.45", "w", "=W_L", "=W_B", 0.10, 0.45, ""),
        ("Thrust deduction in the range 0.05 – 0.35", "t", "=T_L", "=T_B", 0.05, 0.35, ""),
        ("Hull efficiency in the range 0.90 – 1.30", "ηH", "=ETA_H_L", "=ETA_H_B", 0.90, 1.30, ""),
        ("Relative rotative efficiency 0.95 – 1.05", "ηR", "=ETA_R_L", "=ETA_R_B", 0.95, 1.05, ""),
    ]:
        label(ws, r, 1, lab)
        value(ws, r, 2, sym, fmt="@", align="center", size=9)
        for col, ref, lo_, hi_ in ((3, fl, lo, hi), (4, fb, lo, hi)):
            calc(ws, r, col, f'=IF(AND({ref[1:]}>={lo_},{ref[1:]}<={hi_}),"OK","outside")', fmt="@", bold=True)
            c = ws.cell(row=r, column=col)
            c.alignment = Alignment(horizontal="center")
        value(ws, r, 5, "–", fmt="@", align="center")
        note(ws, r, 6, "Expected engineering range for a single-screw displacement vessel – outside it, review the input.", size=8)
        ws.conditional_formatting.add(f"C{r}", CellIsRule(operator="equal", formula=['"OK"'],
                                      fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
        ws.conditional_formatting.add(f"D{r}", CellIsRule(operator="equal", formula=['"OK"'],
                                      fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
        ws.conditional_formatting.add(f"C{r}", CellIsRule(operator="equal", formula=['"outside"'],
                                      fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
        ws.conditional_formatting.add(f"D{r}", CellIsRule(operator="equal", formula=['"outside"'],
                                      fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
        r += 1
    r += 1
    note(ws, r, 1, "Note on the ballast column: the propeller and gear ratio are fixed by the loaded condition. The ballast "
                   "column therefore shows the reduced resistance and thrust of the same propeller at the same rpm – it is a "
                   "check of cavitation (the blade tip comes closer to the surface) and of engine over-speed, not a second design.",
          span=6)
    ws.row_dimensions[r].height = 30
    ws.freeze_panes = "A5"
    return ws
