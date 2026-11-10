"""Sheet 9 - the equation register: every formula used in the workbook."""
from theme import *
import db


def build(wb, nm):
    ws = wb.create_sheet("9 Equations")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 8, "B": 20, "C": 34, "D": 110, "E": 18})
    title(ws, "9  EQUATION REGISTER  —  EVERY FORMULA IN THIS WORKBOOK",
          "Each row gives the equation, the quantity it produces and the sheet where it is evaluated step by step. "
          "Notation: Fn Froude number, Rn Reynolds number, ∇ displacement volume, lcb longitudinal centre of buoyancy "
          "(%L, + forward), Cstern stern-shape coefficient, iE half angle of entrance, LR length of run.",
          ncols=5)

    r = 4
    section(ws, r, "A.  REGISTER", ncols=5); r += 1
    thead(ws, r, [(1, "Ref"), (2, "Group"), (3, "Quantity"), (4, "Equation"), (5, "Evaluated on")], height=24)
    r += 1
    prev = None
    for ident, grp, qty, eq, where in db.EQUATIONS:
        if grp != prev:
            for c in range(1, 6):
                ws.cell(row=r, column=c).fill = fill(GREY_HDR)
            band(ws, r, r, 1, 5, GREY_HDR)
            label(ws, r, 1, grp.upper(), bold=True)
            r += 1
            prev = grp
        value(ws, r, 1, ident, fmt="@", align="center", size=9)
        value(ws, r, 2, grp, fmt="@", size=9)
        label(ws, r, 3, qty, size=9)
        note(ws, r, 4, eq, size=9, italic=False, color=NAVY)
        value(ws, r, 5, where, fmt="@", align="left", size=9)
        ws.row_dimensions[r].height = 15 + 12 * max(0, len(eq) // 105)
        r += 1

    r += 1
    section(ws, r, "B.  NAMED CELLS AND RANGES", ncols=5); r += 1
    thead(ws, r, [(1, "Name"), (2, "Means"), (3, "Defined on"), (4, "Where it is used"), (5, "")], height=20)
    r += 1
    known = {
        "VS_KN": "Service speed, knots", "VS_MS": "Service speed, m/s", "L_WL": "Waterline length",
        "B_WL": "Waterline beam", "T_LOAD": "Draught, loaded", "T_BAL": "Draught, ballast",
        "VOL_LOAD": "Displacement volume, loaded", "CB_": "Block coefficient", "CP_": "Prismatic coefficient",
        "CM_": "Midship coefficient", "CWP_": "Waterplane coefficient", "LCB_": "lcb, %L",
        "CSTERN_": "Stern-shape coefficient", "S_APP": "Appendage wetted area", "K2_EQ": "(1+k2) of the appendages",
        "D_PROP": "Propeller diameter", "Z_BL": "Number of blades", "AE_PROP": "Blade-area ratio",
        "S_LOAD": "Wetted surface, loaded", "CF_L": "Friction coefficient, loaded", "K1_L": "(1+k1), loaded",
        "CA_L": "Correlation allowance", "RT_L": "Total resistance, loaded", "PE_L": "Effective power",
        "W_L": "Wake fraction", "T_L": "Thrust deduction", "ETA_R_L": "Relative rotative efficiency",
        "ETA_H_L": "Hull efficiency", "THRUST_L": "Thrust required", "VA_L": "Speed of advance",
        "FIN_PD": "Solved pitch ratio", "FIN_ETAO": "Open-water efficiency", "FIN_PD_KW": "Delivered power",
        "ENG_MODEL": "Recommended engine", "ENG_NSEL": "Shaft speed of engine + gear",
        "ALPHA": "ISO 3046-1 correction factor α", "K_SITE": "Site factor k before α",
        "KT_C": "KT coefficient column", "KQ_C": "KQ coefficient column",
    }
    for k, v in sorted(known.items()):
        value(ws, r, 1, k, fmt="@", align="left", bold=True, size=9)
        note(ws, r, 2, v, size=9, italic=False, span=3)
        r += 1
    ws.freeze_panes = "A6"
    return ws
