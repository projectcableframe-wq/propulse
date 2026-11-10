"""Sheet 8 - the equation register: every formula used in the workbook."""
from theme import *
import db

_NAMES_ROW = None

# One short meaning per defined name.  The table itself is written from the
# workbook's own defined names (see fill_names), so it can never go stale.
DESC = {
    "ABT_": "Bulb transverse area at the FP, m²",
    "AE_KELLER": "Keller minimum blade-area ratio (AE/A0)min",
    "AE_MIN": "Lower limit of the blade-area ratio",
    "AE_PROP": "Blade-area ratio actually used",
    "ALLOW_HS": "Allow high-speed H/S ratings (YES/NO)",
    "ALPHA": "ISO 3046-1 power adjustment factor α",
    "APERTURE": "Aperture height available for the propeller, m",
    "AT_BAL": "Immersed transom area, ballast, m²",
    "AT_LOAD": "Immersed transom area, loaded, m²",
    "BSFC_": "Specific fuel consumption at the rated point, g/kWh",
    "B_MLD": "Moulded breadth, m",
    "B_WL": "Beam on the waterline, m",
    "CA_B": "Correlation allowance CA, ballast",
    "CA_L": "Correlation allowance CA, loaded",
    "CB_": "Block coefficient CB",
    "CF_B": "ITTC-1957 friction coefficient, ballast",
    "CF_L": "ITTC-1957 friction coefficient, loaded",
    "CM_": "Midship section coefficient CM",
    "CP_": "Prismatic coefficient CP",
    "CSTERN_": "Stern-shape coefficient Cstern (−25 … +10)",
    "CURVE_PD": "Pitch ratio P/D used for the open-water curves (= solved P/D)",
    "CWP_": "Waterplane area coefficient CWP",
    "DERATE": "Engine derating Δ = (1 − α)·100, %",
    "DWT_": "Deadweight, t",
    "D_MAX": "Maximum propeller diameter allowed, m",
    "D_MAX_AUTO": "Maximum diameter that fits the aperture, m",
    "D_PROP": "Propeller diameter used, m",
    "EM_": "Engine margin, % of MCR",
    "ENG_DUTY": "Rating class of the selected engine (M/L/H/S/C/MAX/CONT)",
    "ENG_FUEL": "Fuel consumption at service speed, kg/h",
    "ENG_FUEL_DAY": "Fuel consumption per day of operation, kg/day",
    "ENG_GEARBOX": "Gearbox model of the selected engine",
    "ENG_KW": "Catalogue rating of the selected engine, kW",
    "ENG_LOAD": "Engine load PB,service / site-corrected rating",
    "ENG_MASS": "Dry mass of the selected engine, kg",
    "ENG_MODEL": "Recommended engine model",
    "ENG_NSEL": "Shaft speed of the selected engine + gear, rpm",
    "ENG_PB": "Brake power at service speed, kW",
    "ENG_PD": "Delivered power at the selected shaft speed, kW",
    "ENG_PMCR": "Required MCR of the selected engine, kW",
    "ENG_PS": "Shaft power at service speed, kW",
    "ENG_PSITE": "Site-corrected rating of the selected engine, kW",
    "ENG_RATIO": "Gear ratio selected",
    "ENG_RPM": "Rated speed of the selected engine, rpm",
    "ENG_SERIES": "Series of the selected engine",
    "ENG_UTIL": "PMCR,req / site-corrected rating (≤ 100 %)",
    "ETA_G": "Gearbox efficiency ηG",
    "ETA_H_B": "Hull efficiency ηH, ballast",
    "ETA_H_L": "Hull efficiency ηH, loaded",
    "ETA_M": "Mechanical efficiency of the engine ηm",
    "ETA_R_B": "Relative rotative efficiency ηR, ballast",
    "ETA_R_L": "Relative rotative efficiency ηR, loaded",
    "ETA_R_OVR": "Relative rotative efficiency override",
    "ETA_S": "Shafting efficiency ηS",
    "FIN_ETAD": "Quasi-propulsive coefficient ηD = ηH·ηO·ηR",
    "FIN_ETAO": "Open-water efficiency ηO",
    "FIN_KQ": "Torque coefficient KQ at the solved point",
    "FIN_KT": "Thrust coefficient KT at the solved point",
    "FIN_N": "Shaft speed of the propeller solution, rpm",
    "FIN_PB": "Brake power at the solved point, kW",
    "FIN_PD": "Solved pitch ratio P/D",
    "FIN_PD_KW": "Delivered power at the solved point, kW",
    "FIN_PITCH": "Pitch P = (P/D)·D, m",
    "FIN_PMCR": "Required MCR at the solved point, kW",
    "FIN_PS": "Shaft power at the solved point, kW",
    "GT_": "Gross tonnage",
    "G_": "Acceleration due to gravity, m/s²",
    "HB_": "Height of the bulb centre above the keel, m",
    "HRS_": "Operating hours per day, h",
    "H_SHAFT": "Shaft immersion above the propeller centre, m",
    "J_FIN": "Advance coefficient at the solved point",
    "K1_B": "Form factor (1+k1), ballast",
    "K1_L": "Form factor (1+k1), loaded",
    "K1_OVR": "Form-factor override",
    "K2_EQ": "Equivalent appendage factor (1+k2)eq",
    "KQ_C": "KQ polynomial: coefficient column",
    "KQ_S": "KQ polynomial: J-exponent column",
    "KQ_T": "KQ polynomial: P/D-exponent column",
    "KQ_U": "KQ polynomial: AE/A0-exponent column",
    "KQ_V": "KQ polynomial: Z-exponent column",
    "KT_C": "KT polynomial: coefficient column",
    "KT_S": "KT polynomial: J-exponent column",
    "KT_T": "KT polynomial: P/D-exponent column",
    "KT_U": "KT polynomial: AE/A0-exponent column",
    "KT_V": "KT polynomial: Z-exponent column",
    "K_SITE": "ISO 3046-1 site factor k (before the ηm term)",
    "K_VISC_CALC": "Kinematic viscosity interpolated from the sea-water table, m²/s",
    "K_VISC_IDX": "Row index of the sea-water table used for the interpolation",
    "LCB_": "lcb, %L, + forward of 0.5 L",
    "LOAD_MAX": "Maximum continuous engine load allowed, %",
    "L_OA": "Length overall, m",
    "L_PP": "Length between perpendiculars, m",
    "L_WL": "Waterline length, m",
    "MAX_KW": "Upper limit of the engine kW band",
    "MIN_KW": "Lower limit of the engine kW band",
    "NU_OVR": "Kinematic-viscosity override, m²/s",
    "NU_W": "Kinematic viscosity used, m²/s",
    "N_OPT": "Shaft speed of the optimum propeller, rpm",
    "N_PROP": "Propeller shaft speed used in the selection, rpm",
    "P0_": "Absolute static pressure at the shaft centre, kPa",
    "PB_DESIGN": "Brake power at the design point, kW",
    "PD_DESIGN": "Delivered power at the design point, kW",
    "PD_OPT": "Delivered power of the optimum propeller, kW",
    "PE_B": "Effective power at service speed, ballast, kW",
    "PE_L": "Effective power at service speed, loaded, kW",
    "PMCR_REQ": "Required MCR, kW",
    "PS_DESIGN": "Shaft power at the design point, kW",
    "PS_SAT_R": "Saturation pressure at the reference air temperature, kPa",
    "PS_SAT_X": "Saturation pressure at the site air temperature, kPa",
    "PV_": "Vapour pressure of sea water at t_sw, kPa",
    "P_BARO": "Barometric pressure at the site, kPa",
    "Q_FIN": "Torque at the solved point, N·m",
    "RHO_W": "Sea-water density, kg/m³",
    "RH_": "Relative humidity, %",
    "RT_B": "Total resistance, ballast, N",
    "RT_L": "Total resistance, loaded, N",
    "RT_S_B": "Total resistance, ballast, with sea margin, N",
    "RT_S_L": "Total resistance, loaded, with sea margin, N",
    "SHAFT_ANG": "Shaft inclination, degrees",
    "SM_": "Sea margin, %",
    "SW_N": "Sweep: shaft speed, rpm",
    "SW_PB": "Sweep: brake power, kW",
    "SW_PD": "Sweep: delivered power, kW",
    "SW_PE": "Sweep: effective power, kW",
    "SW_RT": "Sweep: total resistance, N",
    "SW_STATUS": "Sweep: status flag of each point (OK / REVIEW)",
    "SW_VS": "Sweep: ship speed, kn",
    "S_APP": "Appendage wetted area, m²",
    "S_BAL": "Wetted surface, ballast, m²",
    "S_LOAD": "Wetted surface, loaded, m²",
    "TF_LOAD": "Forward draught, loaded, m",
    "THRUST_B": "Required thrust, ballast, N",
    "THRUST_L": "Required thrust, loaded, N",
    "TIP_CLR": "Tip clearance, m",
    "T_AIR": "Air temperature at the engine intake, °C",
    "T_B": "Thrust deduction t, ballast",
    "T_BAL": "Draught, ballast, m",
    "T_DESIGN": "Thrust at the design point, N",
    "T_L": "Thrust deduction t, loaded",
    "T_LOAD": "Draught, loaded, m",
    "T_OVR": "Thrust-deduction override",
    "T_SW": "Sea-water temperature, °C",
    "VA_B": "Speed of advance, ballast, m/s",
    "VA_L": "Speed of advance, loaded, m/s",
    "VOL_BAL": "Displacement volume, ballast, m³",
    "VOL_LOAD": "Displacement volume, loaded, m³",
    "VSL_CASE": "Design case / route",
    "VSL_NAME": "Vessel name",
    "VSL_OWNER": "Owner / operator",
    "VSL_PREP": "Prepared by / revision",
    "VSL_TYPE": "Vessel type (drives the guidance table of sheet 1)",
    "VSL_TYPE_LIST": "List of vessel types behind the dropdown",
    "VS_KN": "Service speed, kn",
    "W_B": "Wake fraction w, ballast",
    "W_L": "Wake fraction w, loaded",
    "W_OVR": "Wake-fraction override",
    "Z_BL": "Number of propeller blades",
}


def build(wb, nm):
    global _NAMES_ROW
    ws = wb.create_sheet("8 Equations")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 8, "B": 20, "C": 34, "D": 110, "E": 18, "F": 2,
                "G": 15, "H": 46, "I": 24, "J": 40})
    title(ws, "8  EQUATION REGISTER  —  EVERY FORMULA IN THIS WORKBOOK",
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
    for c in range(7, 11):
        ws.cell(row=r, column=c).fill = fill(TEAL_DK)
    sec = ws.cell(row=r, column=7, value="B.  NAMED CELLS AND RANGES")
    sec.font = Font(name=FONT, size=11, bold=True, color=WHITE)
    sec.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r].height = 22
    r += 1
    thead(ws, r, [(7, "Name"), (8, "Means"), (9, "Defined on"), (10, "Where it is used")], height=20)
    r += 1
    _NAMES_ROW = r
    ws.freeze_panes = "A6"
    return ws


def _usage(wb, names):
    """Which sheets use each defined name - in a formula, as a whole value, or in a validation."""
    use = {n: set() for n in names}
    nameset = set(names)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not isinstance(v, str) or not v:
                    continue
                if v.startswith("="):
                    for n in nameset:
                        if n in v:
                            use[n].add(ws.title)
                elif v in nameset:
                    use[v].add(ws.title)
    for ws in wb.worksheets:
        for dv in ws.data_validations.dataValidation:
            f = dv.formula1 or ""
            for n in nameset:
                if n in f:
                    use[n].add(ws.title)
    return use


def fill_names(wb):
    """Write section B from the workbook itself - called after every sheet exists."""
    from openpyxl.utils import get_column_letter
    ws = wb["8 Equations"]
    names = sorted(wb.defined_names)
    use = _usage(wb, names)
    order = {t: i for i, t in enumerate(wb.sheetnames)}
    r = _NAMES_ROW
    for n in names:
        ref = wb.defined_names[n].attr_text
        if "!" in ref:
            sh, addr = ref.split("!", 1)
            defined = "%s!%s" % (sh.strip("'"), addr.replace("$", ""))
        else:
            defined = "–"
        used = sorted(use[n], key=lambda t: order[t])
        value(ws, r, 7, n, fmt="@", align="left", bold=True, size=9)
        note(ws, r, 8, DESC.get(n, "–"), size=9, italic=False, color=NAVY)
        value(ws, r, 9, defined, fmt="@", align="left", size=9)
        value(ws, r, 10, ", ".join(used) if used else "–", fmt="@", align="left", size=9)
        r += 1
    missing = [n for n in names if n not in DESC]
    if missing:
        print("   WARNING: no description for %s" % ", ".join(missing))
    extra = [n for n in DESC if n not in names]
    if extra:
        print("   note: descriptions not used: %s" % ", ".join(sorted(extra)))
    return r
