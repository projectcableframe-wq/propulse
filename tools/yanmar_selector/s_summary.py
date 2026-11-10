"""Sheet 0 - one-page design summary."""
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from theme import *


def build(wb, nm):
    ws = wb.create_sheet("0 Summary")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 3, "B": 44, "C": 16, "D": 9, "E": 4, "F": 40, "G": 20, "H": 4})
    title(ws, "DESIGN SUMMARY" + "  —  " + "RESISTANCE, PROPELLER AND YANMAR ENGINE ON ONE PAGE",
          "One page, everything that matters: what the hull needs, which propeller turns it into thrust and which "
          "Yanmar engine carries it in Maldivian conditions. Every figure is live — change sheet 1 and the whole "
          "workbook follows.", ncols=8)

    r = 4
    section(ws, r, "A.  VESSEL AND SERVICE CONDITION", ncols=4); r += 1

    def srow(lab, formula, fmt, unit="", bold=False, isres=False):
        nonlocal r
        label(ws, r, 2, lab, bold=bold)
        if not str(formula).startswith("="):
            value(ws, r, 3, formula, fmt=fmt, align="right")
            value(ws, r, 4, unit, fmt="@", align="center")
            r += 1
            return
        if isres:
            result(ws, r, 3, formula, fmt=fmt)
        else:
            calc(ws, r, 3, formula, fmt=fmt, bold=bold)
        value(ws, r, 4, unit, fmt="@", align="center")
        r += 1

    srow("Vessel", "=VSL_NAME", "@", "", bold=True)
    srow("Vessel type", "=VSL_TYPE", "@", "")
    srow("Length overall / waterline", '=TEXT(L_OA,"0.0")&" / "&TEXT(L_WL,"0.0")', "@", "m")
    srow("Beam moulded / waterline", '=TEXT(B_MLD,"0.0")&" / "&TEXT(B_WL,"0.0")', "@", "m")
    srow("Draught loaded / ballast", '=TEXT(T_LOAD,"0.00")&" / "&TEXT(T_BAL,"0.00")', "@", "m")
    srow("Displacement volume", "=VOL_LOAD", "#,##0.0", "m³")
    srow("Service speed", "=VS_KN", "0.0", "kn")
    srow("Sea margin allowed", "=SM_/100", "0.0%", "")
    srow("Design sea-water temperature", "=T_SW", "0.0", "°C")
    r += 1

    section(ws, r, "B.  RESISTANCE AND POWER, LOADED CONDITION", ncols=4); r += 1
    srow("Wetted surface area", "=S_LOAD", "#,##0.0", "m²")
    srow("Total resistance at service speed", "=RT_L/1000", "#,##0.00", "kN")
    srow("Effective power", "=PE_L", "#,##0.0", "kW")
    srow("Wake fraction / thrust deduction", '=TEXT(W_L,"0.000")&" / "&TEXT(T_L,"0.000")', "@", "–")
    srow("Hull efficiency", "=ETA_H_L", "0.0000", "–")
    srow("Delivered power", "=FIN_PD_KW", "#,##0.0", "kW", bold=True)
    srow("Shaft power", "=FIN_PS", "#,##0.0", "kW")
    srow("Brake power at service speed", "=FIN_PB", "#,##0.0", "kW", bold=True)
    srow("Required engine rating (MCR)", "=FIN_PMCR", "#,##0.0", "kW", isres=True)
    srow("Quasi-propulsive coefficient ηD", "=FIN_ETAD", "0.0000", "–")
    r += 1

    section(ws, r, "C.  PROPELLER", ncols=4); r += 1
    srow("Series", "Wageningen B-series, fixed pitch, single screw", "@", "")
    srow("Diameter / number of blades", '=TEXT(D_PROP,"0.000")&" m  /  "&TEXT(Z_BL,"0")', "@", "")
    srow("Pitch ratio / pitch", '=TEXT(FIN_PD,"0.000")&"  /  "&TEXT(FIN_PITCH,"0.000")&" m"', "@", "", bold=True)
    srow("Blade-area ratio (Keller)", '=TEXT(AE_PROP,"0.00")&"  (min "&TEXT(AE_KELLER,"0.00")&")"', "@", "")
    srow("Shaft speed", "=FIN_N", "#,##0", "rpm", bold=True)
    srow("Open-water efficiency", "=FIN_ETAO", "0.0000", "–")
    srow("Torque", "=Q_FIN", "#,##0", "N·m")
    srow("Blade tip speed", "=PI()*(FIN_N/60)*D_PROP", "0.0", "m/s")

    # ------------------------------------------------------------- engine panel
    section(ws, 4, "D.  RECOMMENDED YANMAR ENGINE", ncols=3, fillc=NAVY_2)
    for cc in range(6, 9):
        ws.cell(row=4, column=cc).fill = fill(NAVY_2)
    t = ws.cell(row=4, column=6, value="D.  RECOMMENDED YANMAR ENGINE")
    t.font = Font(name=FONT, size=11, bold=True, color=WHITE)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    rr = 5
    label(ws, rr, 6, "MODEL", bold=True, size=9, color=NOTE_FONT)
    c = ws.cell(row=rr + 1, column=6, value="=ENG_MODEL")
    c.font = Font(name=FONT, size=26, bold=True, color=TEAL_DK)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[rr + 1].height = 36
    rr += 2
    label(ws, rr, 6, "=ENG_SERIES&\" series  ·  \"&ENG_DUTY&\" rating  ·  \"&ENG_GEARBOX", size=9, color=NOTE_FONT)
    rr += 2

    def erow(lab, formula, fmt, bold=False, isres=False):
        nonlocal rr
        label(ws, rr, 6, lab)
        if isres:
            result(ws, rr, 7, formula, fmt=fmt)
        else:
            calc(ws, rr, 7, formula, fmt=fmt, bold=bold)
        rr += 1

    erow("Catalogue rating (ISO)", "=ENG_KW", "0.0 \"kW\"")
    erow("Site-corrected rating", "=ENG_PSITE", "0.0 \"kW\"", bold=True)
    erow("Derating factor α", "=ALPHA", "0.0000")
    erow("Rated speed", "=ENG_RPM", "0 \"rpm\"")
    erow("Gear ratio / shaft speed", '=TEXT(ENG_RATIO,"0.000")&"  →  "&TEXT(ENG_NSEL,"0")&" rpm"', "@")
    erow("Power required at service speed", "=ENG_PB", "0.0 \"kW\"")
    erow("Load on the site-corrected rating", "=ENG_LOAD", "0.0%", bold=True)
    erow("Reserve left (1 − MCR req / P site)", '=IF(ISNUMBER(ENG_UTIL),1-ENG_UTIL,"–")', "0.0%")
    erow("Fuel at service speed", "=ENG_FUEL", "0.0 \"kg/h\"")
    erow("Fuel per day", "=ENG_FUEL_DAY", "0.0 \"kg\"")
    erow("Dry mass (engine)", "=ENG_MASS", "#,##0 \"kg\"")
    rr += 1

    label(ws, rr, 6, "Derating is the tropical site correction of ISO 3046-1 computed on sheet 1:", size=9,
          color=NOTE_FONT, indent=0)
    rr += 1
    label(ws, rr, 6, "32 °C air, 100 % relative humidity, sea level, 32 °C sea water.", size=9, color=NOTE_FONT,
          indent=0)
    rr += 2

    section(ws, rr, "E.  VERDICT", ncols=3, fillc=NAVY_2)
    for cc in range(6, 9):
        ws.cell(row=rr, column=cc).fill = fill(NAVY_2)
    t = ws.cell(row=rr, column=6, value="E.  VERDICT")
    t.font = Font(name=FONT, size=11, bold=True, color=WHITE)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    rr += 1
    vrow = rr
    label(ws, rr, 6, "Propeller checks passed", bold=True)
    calc(ws, rr, 7, "=COUNTIF('4 Propeller'!$E$1:$E$2000,\"PASS\")&\" of \"&"
                    "(COUNTIF('4 Propeller'!$E$1:$E$2000,\"PASS\")+COUNTIF('4 Propeller'!$E$1:$E$2000,\"REVIEW\"))", "@")
    rr += 1
    label(ws, rr, 6, "Engine margin respected", bold=True)
    calc(ws, rr, 7, '=IF(ENG_UTIL<=1,"YES","NO")', "@", bold=True)
    rr += 1
    label(ws, rr, 6, "Design status", bold=True)
    result(ws, rr, 7, '=IF(AND(ENG_UTIL<=1,COUNTIF(\'4 Propeller\'!$E$1:$E$2000,"REVIEW")=0),"DESIGN VALID","REVIEW REQUIRED")',
           fmt="@")
    ws.cell(row=rr, column=7).alignment = Alignment(horizontal="center")
    ws.conditional_formatting.add(f"G{rr}", CellIsRule(operator="equal", formula=['"DESIGN VALID"'],
                                  fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
    ws.conditional_formatting.add(f"G{rr}", CellIsRule(operator="equal", formula=['"REVIEW REQUIRED"'],
                                  fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
    rr += 2

    note(ws, rr, 6, "How to use: change the yellow cells on sheet 1 only. Sheet 2 rebuilds the resistance, sheet 3 the "
                    "hull-propeller interaction, sheet 4 the propeller at every possible shaft speed, sheet 5 the whole "
                    "Yanmar range and sheet 9 verifies the arithmetic against an independent implementation.",
         size=9, span=2)
    ws.row_dimensions[rr].height = 60

    # highlight the vessel block
    band(ws, 5, 5, 2, 4, GREY_HDR)
    ws.freeze_panes = "A4"
    return ws
