"""Sheet 1 - Input."""
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from theme import *
from theme import inp as _inp
from db import SEAWATER, YANMAR

VESSEL_TYPES = ("Passenger ferry / mechanised dhoni, Speed launch / water taxi, Safari boat (liveaboard), "
                "Fishing vessel (masdhoni), Landing craft / RoRo barge, Tug / workboat, Cargo / supply vessel, "
                "Patrol / enforcement craft, Diving / support boat, Other")

def build(wb, nm):
    def inp(ws_, row_, col_, val_, fmt="0.000", name=None):
        c = _inp(ws_, row_, col_, val_, fmt=fmt)
        if name:
            nm.add(name, "%s%d" % (get_column_letter(col_), row_))
        return c

    ws = wb.create_sheet("1 Input")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 46, "B": 20, "C": 15, "D": 13, "E": 62, "F": 3, "G": 12, "H": 12, "I": 30})
    title(ws, "1  INPUT DATA", "Yellow cells are the only cells to edit. Every other cell is a live formula. "
          "Units: SI (m, m³, t, kW, knots, °C, kPa).", ncols=9)

    r = 4
    section(ws, r, "A.  VESSEL IDENTIFICATION", ncols=9); r += 1
    type_row = None
    for lab, sym, val, unit, nte, name in [
        ("Vessel name", "", "MV Coral Dhoni", "", "Free text – appears on the cover and the summary sheet", "VSL_NAME"),
        ("Vessel type", "", "Passenger ferry / mechanised dhoni", "", "Select from list – drives the advisory checks", "VSL_TYPE"),
        ("Owner / operator", "", "", "", "Free text", "VSL_OWNER"),
        ("Design case / route", "", "", "", "e.g. Malé – Maafushi, 1.5 h crossing", "VSL_CASE"),
        ("Prepared by / revision", "", "", "", "Name, date, revision number", "VSL_PREP"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        c = inp(ws, r, 3, val, fmt="@", name=name)
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        note(ws, r, 5, nte)
        if name == "VSL_TYPE":
            type_row = r
        r += 1

    r += 1
    section(ws, r, "B.  PRINCIPAL DIMENSIONS AND DISPLACEMENT", ncols=9); r += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Length overall", "LOA", 32.00, "m", "Extreme length, for reference", "L_OA", "0.00"),
        ("Length between perpendiculars", "LPP", 29.20, "m", "For reference and LCB datum check", "L_PP", "0.00"),
        ("Length on waterline", "LWL", 30.50, "m", "Used in all resistance formulas (Holtrop L)", "L_WL", "0.00"),
        ("Beam, moulded", "B", 7.20, "m", "Used in all resistance formulas", "B_MLD", "0.00"),
        ("Beam on waterline", "BWL", 7.05, "m", "For reference (B in the method = moulded beam)", "B_WL", "0.00"),
        ("Draft, loaded (design)", "T", 1.70, "m", "Design / loaded condition – used for engine sizing", "T_LOAD", "0.000"),
        ("Draft, ballast / unloaded", "Tb", 1.25, "m", "Second condition – used for checks only", "T_BAL", "0.000"),
        ("Forward draft, loaded", "TF", 1.60, "m", "Bulb and correlation-allowance terms (TF)", "TF_LOAD", "0.000"),
        ("Displacement volume, loaded", "∇", 210.0, "m³", "∇ = CB·LWL·B·T. Must be consistent with CB", "VOL_LOAD", "#,##0.0"),
        ("Displacement volume, ballast", "∇b", 148.0, "m³", "∇b = CBB·LWL·B·Tb (ballast CB)", "VOL_BAL", "#,##0.0"),
        ("Gross tonnage", "GT", 95.0, "GT", "Reference only (not used in the calculation)", "GT_", "#,##0"),
        ("Deadweight", "DWT", 60.0, "t", "Reference only (not used in the calculation)", "DWT_", "#,##0.0"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, nte); r += 1

    r += 1
    section(ws, r, "C.  HULL-FORM COEFFICIENTS", ncols=9); r += 1
    for lab, sym, val, nte, name, fmt in [
        ("Block coefficient (on LWL)", "CB", 0.580, "CB = ∇/(LWL·B·T). Typical dhoni 0.55–0.65, ferry 0.60–0.70", "CB_", "0.000"),
        ("Prismatic coefficient", "CP", 0.630, "CP = CB/CM. Must agree with CB and CM (checked below)", "CP_", "0.000"),
        ("Midship section coefficient", "CM", 0.920, "CM = AM/(B·T). Typical 0.85–0.98", "CM_", "0.000"),
        ("Waterplane area coefficient", "CWP", 0.790, "CWP = AW/(LWL·BWL). Typical 0.70–0.88", "CWP_", "0.000"),
        ("LCB, forward of ½LWL  [% LWL]", "lcb", -1.0, "Positive forward. Typical −3 % … +3 % (negative aft)", "LCB_", "0.00"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, "%" if sym == "lcb" else "–", fmt="@", align="center")
        note(ws, r, 5, nte); r += 1
    label(ws, r, 1, "Stern shape coefficient", bold=False); value(ws, r, 2, "Cstern", fmt="@", align="center")
    c = inp(ws, r, 3, 0, fmt="0", name="CSTERN_")
    c.alignment = Alignment(horizontal="center", vertical="center")
    value(ws, r, 4, "–", fmt="@", align="center")
    note(ws, r, 5, "Pram with gondola −25 · V-shaped −10 · normal 0 · U-shaped +10 (Holtrop table)")
    dv = DataValidation(type="list", formula1='"-25,-10,0,10"', allow_blank=False,
                        showErrorMessage=True, errorTitle="Cstern",
                        error="Use one of the Holtrop values: -25, -10, 0 or +10.")
    ws.add_data_validation(dv); dv.add(c)
    CSTERN = r; r += 1

    label(ws, r, 1, "Consistency check   CP = CB / CM", bold=True)
    calc(ws, r, 2, "=(CB_/CM_)", fmt="0.000")
    calc(ws, r, 3, '=IF(ABS(CP_-(CB_/CM_))<=0.012,"consistent","CHECK")', fmt="@", bold=True)
    note(ws, r, 5, "CP must equal CB/CM. A difference above 0.012 is flagged (resistances become unreliable).")
    ws.conditional_formatting.add(f"C{r}", CellIsRule(operator="equal", formula=['"consistent"'],
                                  fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
    ws.conditional_formatting.add(f"C{r}", CellIsRule(operator="equal", formula=['"CHECK"'],
                                  fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
    r += 2

    section(ws, r, "D.  BULBOUS BOW AND TRANSOM", ncols=9); r += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Transverse area of bulb at waterline", "ABT", 0.00, "m²", "Enter 0 if there is no bulbous bow", "ABT_", "0.00"),
        ("Height of bulb area centroid above keel", "hB", 0.00, "m", "Enter 0 if no bulb", "HB_", "0.000"),
        ("Immersed transom area, loaded", "AT", 0.00, "m²", "Enter 0 for a dry transom", "AT_LOAD", "0.00"),
        ("Immersed transom area, ballast", "ATb", 0.00, "m²", "Enter 0 for a dry transom", "AT_BAL", "0.00"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, nte); r += 1
    r += 1

    section(ws, r, "E.  APPENDAGES   (Holtrop equivalent appendage factor)", ncols=9); r += 1
    thead(ws, r, [(1, "Appendage"), (2, "Symbol"), (3, "Wetted area SAPP,i  [m²]"),
                  (4, "(1+k2)i"), (5, "Holtrop guidance for (1+k2)")], height=34)
    r += 1
    app_rows = []
    items = [("Rudder behind stern (single screw)", "SAPP_RUD", 1.50, "1.3 – 1.5"),
             ("Rudder(s) behind skeg (twin screw)", "SAPP_RUD2", 1.80, "1.5 – 2.0"),
             ("Skeg", "SAPP_SKEG", 1.75, "1.5 – 2.0"),
             ("Bilge keels", "SAPP_BK", 1.40, "1.4"),
             ("Exposed shafting", "SAPP_SHAFT", 2.00, "2.0 – 4.0"),
             ("Shaft brackets / struts", "SAPP_BRKT", 3.00, "3.0"),
             ("Stabiliser fins", "SAPP_FIN", 2.80, "2.8"),
             ("Bow-thruster tunnel / other", "SAPP_OTH", 2.00, "2.0 – 2.7")]
    for i, (lab, sym, k2, guid) in enumerate(items):
        label(ws, r, 1, lab)
        value(ws, r, 2, sym, fmt="@", align="center", size=9)
        v = 0.0
        if i == 0: v = 1.15
        if i == 4: v = 0.35
        inp(ws, r, 3, v, fmt="0.00")
        inp(ws, r, 4, k2, fmt="0.00")
        note(ws, r, 5, guid)
        app_rows.append(r); r += 1
    label(ws, r, 1, "Total appendage wetted area", bold=True)
    value(ws, r, 2, "SAPP", fmt="@", align="center")
    calc(ws, r, 3, f"=SUM(C{app_rows[0]}:C{app_rows[-1]})", fmt="0.00", bold=True)
    value(ws, r, 4, "m²", fmt="@", align="center")
    note(ws, r, 5, "Sum of the areas entered above")
    nm.add("S_APP", "C%d" % r); r += 1
    label(ws, r, 1, "Equivalent appendage factor", bold=True)
    value(ws, r, 2, "(1+k2)eq", fmt="@", align="center")
    calc(ws, r, 3, f'=IFERROR(SUMPRODUCT(C{app_rows[0]}:C{app_rows[-1]},D{app_rows[0]}:D{app_rows[-1]})/SUM(C{app_rows[0]}:C{app_rows[-1]}),1)', fmt="0.000")
    value(ws, r, 4, "–", fmt="@", align="center")
    note(ws, r, 5, "(1+k2)eq = Σ[(1+k2)i·SAPP,i] / Σ SAPP,i   —  Holtrop & Mennen (1982) eq. for combined appendages")
    nm.add("K2_EQ", "C%d" % r); r += 2

    section(ws, r, "F.  PROPELLER ARRANGEMENT  (single screw, fixed pitch)", ncols=9); r += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Aperture height available for propeller", "h_ap", 1.15, "m", "Clear vertical space between keel and aperture top", "APERTURE", "0.000"),
        ("Minimum tip clearance", "c_tip", 0.10, "m", "Vertical clearance between blade tip and hull/keel", "TIP_CLR", "0.000"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, nte); r += 1
    label(ws, r, 1, "Maximum propeller diameter from aperture", bold=True)
    value(ws, r, 2, "D_max", fmt="@", align="center")
    calc(ws, r, 3, "=MAX(APERTURE-TIP_CLR,0.1)", fmt="0.000", bold=True)
    value(ws, r, 4, "m", fmt="@", align="center")
    note(ws, r, 5, "D_max = aperture − tip clearance. The design diameter is this value unless overridden below.")
    nm.add("D_MAX_AUTO", "C%d" % r); r += 1
    label(ws, r, 1, "Design propeller diameter (override)")
    value(ws, r, 2, "D", fmt="@", align="center")
    c = inp(ws, r, 3, None, fmt="0.000")
    value(ws, r, 4, "m", fmt="@", align="center")
    note(ws, r, 5, "Leave EMPTY to use D_max. Type a value only if the yard fixes the diameter.")
    nm.add("D_MAX", "C%d" % r); r += 1
    label(ws, r, 1, "Number of blades", bold=False); value(ws, r, 2, "Z", fmt="@", align="center")
    c = inp(ws, r, 3, 4, fmt="0", name="Z_BL"); c.alignment = Alignment(horizontal="center")
    value(ws, r, 4, "–", fmt="@", align="center")
    note(ws, r, 5, "Wageningen B-series valid range 3 … 7. 4 blades is normal for single-screw displacement craft.")
    dv = DataValidation(type="list", formula1='"3,4,5,6,7"', allow_blank=False)
    ws.add_data_validation(dv); dv.add(c); r += 1
    label(ws, r, 1, "Minimum expanded blade-area ratio to be accepted")
    value(ws, r, 2, "AE/A0,min", fmt="@", align="center")
    inp(ws, r, 3, 0.55, fmt="0.00", name="AE_MIN")
    value(ws, r, 4, "–", fmt="@", align="center")
    note(ws, r, 5, "The Keller criterion is always applied; this value can raise the selected blade area, never lower it.")
    r += 1
    label(ws, r, 1, "Shaft angle to the waterline", bold=False)
    value(ws, r, 2, "α_shaft", fmt="@", align="center")
    inp(ws, r, 3, 0.0, fmt="0.0", name="SHAFT_ANG")
    value(ws, r, 4, "deg", fmt="@", align="center")
    note(ws, r, 5, "0 for a horizontal shaft line (this workbook assumes an in-line arrangement; declared for the record).")
    r += 2

    section(ws, r, "G.  SERVICE CONDITION AND MARGINS", ncols=9); r += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Service speed (sea margin applied to resistance)", "VS", 9.5, "kn", "Trial / contract speed in calm water", "VS_KN", "0.00"),
        ("Sea margin (added resistance in service)", "SM", 15, "%", "15 % typical; 10 % sheltered trades; 20–25 % exposed", "SM_", "0"),
        ("Engine margin (reserve on MCR)", "EM", 10, "%", "10 % is normal; 0 % only if the owner accepts a fully rated engine", "EM_", "0"),
        ("Maximum continuous load allowed on the selected engine", "Load", 90, "%", "≤90 % of the site-rated power for continuous commercial duty", "LOAD_MAX", "0"),
        ("Shafting efficiency (bearings + stern tube)", "ηS", 0.97, "–", "0.96–0.98 for a conventional line", "ETA_S", "0.000"),
        ("Gearbox efficiency", "ηG", 0.98, "–", "0.97–0.98 for a hydraulic marine gear", "ETA_G", "0.000"),
        ("Specific fuel consumption at MCR", "BSFC", 215, "g/kWh", "Use the engine maker's data sheet; 210–230 g/kWh typical", "BSFC_", "0"),
        ("Operating hours per day", "h", 10, "h/day", "For the daily fuel figure", "HRS_", "0.0"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, nte); r += 1
    r += 1

    section(ws, r, "H.  ENVIRONMENT AND SITE CONDITIONS  (Maldives – tropical)", ncols=9); r += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Sea-water temperature at the propeller", "t_sw", 30.0, "°C", "Used for water viscosity and vapour pressure", "T_SW", "0.0"),
        ("Water density", "ρ", 1025, "kg/m³", "1025 for seawater; 1000–1027 depending on site", "RHO_W", "0.0"),
        ("Gravitational acceleration", "g", 9.81, "m/s²", "9.81", "G_", "0.000"),
        ("Air temperature at the engine intake", "t_air", 35.0, "°C", "ISO 3046-1 site condition (Malé design value 32–35 °C)", "T_AIR", "0.0"),
        ("Relative humidity", "φ", 75, "%", "ISO 3046-1 site condition", "RH_", "0"),
        ("Barometric pressure at site", "px", 100.5, "kPa", "Sea level ≈ 101.3 kPa; Malé ≈ 100.5 kPa", "P_BARO", "0.00"),
        ("Mechanical efficiency of the engine", "ηm", 0.85, "–", "Used by the ISO 3046-1 power-adjustment factor (0.80–0.90)", "ETA_M", "0.00"),
        ("Kinematic viscosity of water (override)", "ν", None, "m²/s", "Leave EMPTY – the value is interpolated from the seawater table below", "NU_OVR", "0.000E+00"),
    ]:
        label(ws, r, 1, lab); value(ws, r, 2, sym, fmt="@", align="center")
        inp(ws, r, 3, val, fmt=fmt, name=name)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, nte); r += 1
    label(ws, r, 1, "Kinematic viscosity used", bold=True)
    value(ws, r, 2, "ν", fmt="@", align="center")
    calc(ws, r, 3, "=IFERROR(IF(ISNUMBER(NU_OVR),NU_OVR,K_VISC_CALC),1.189E-06)", fmt="0.000E+00", bold=True)
    value(ws, r, 4, "m²/s", fmt="@", align="center")
    note(ws, r, 5, "Seawater 35 PSU from the table below, interpolated at the sea-water temperature.")
    nm.add("NU_W", "C%d" % r); NUROW = r; r += 1

    # seawater table + interpolation helpers (right hand side, small)
    sr = NUROW + 1
    label(ws, sr, 1, "Seawater kinematic viscosity table (35 PSU, 1 atm)", bold=True, size=9)
    note(ws, sr, 5, "Source: standard seawater property tables. ν in 10⁻⁶ m²/s.", size=8)
    sr += 1
    thead(ws, sr, [(7, "t  [°C]"), (8, "ν  [10⁻⁶ m²/s]")], height=18)
    sr += 1
    t0 = sr
    for t, v in SEAWATER:
        value(ws, sr, 7, t, fmt="0", align="center")
        value(ws, sr, 8, v, fmt="0.000", align="center")
        sr += 1
    t1 = sr - 1
    sr += 1
    label(ws, sr, 7, "index", size=9); calc(ws, sr, 8, f"=MIN(MAX(MATCH(T_SW,G{t0}:G{t1},1),1),{len(SEAWATER)-1})", fmt="0")
    nm.add("K_VISC_IDX", f"$H${sr}")
    sr += 1
    label(ws, sr, 7, "ν  [m²/s]", size=9)
    calc(ws, sr, 8, (f"=1E-06*(IF(MATCH(T_SW,G{t0}:G{t1},1)={len(SEAWATER)},INDEX(H{t0}:H{t1},MATCH(T_SW,G{t0}:G{t1},1)),"
                     f"INDEX(H{t0}:H{t1},MATCH(T_SW,G{t0}:G{t1},1))+(T_SW-INDEX(G{t0}:G{t1},MATCH(T_SW,G{t0}:G{t1},1)))"
                     f"*(INDEX(H{t0}:H{t1},MATCH(T_SW,G{t0}:G{t1},1)+1)-INDEX(H{t0}:H{t1},MATCH(T_SW,G{t0}:G{t1},1)))"
                     f"/(INDEX(G{t0}:G{t1},MATCH(T_SW,G{t0}:G{t1},1)+1)-INDEX(G{t0}:G{t1},MATCH(T_SW,G{t0}:G{t1},1)))))"), fmt="0.000E+00")
    nm.add("K_VISC_CALC", f"$H${sr}")
    sr += 2

    # ISO 3046-1 block
    section(ws, sr, "I.  ISO 3046-1 POWER ADJUSTMENT  (declared rating → tropical site rating)", ncols=9); sr += 1
    thead(ws, sr, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Unit"), (5, "Formula / source")], height=22); sr += 1
    rows_iso = [
        ("Saturation vapour pressure at site air temperature", "psx",
         "=0.61121*EXP(17.502*T_AIR/(T_AIR+240.97))", "kPa", "Buck equation (t in °C), ISO 3046-1 Annex B"),
        ("Saturation vapour pressure at 25 °C reference", "psr",
         "=0.61121*EXP(17.502*25/(25+240.97))", "kPa", "Buck equation at 25 °C"),
        ("Reference barometric pressure", "pr", 100, "kPa", "ISO 15550 / ISO 3046-1 standard reference condition"),
        ("Reference air temperature", "Tr", 298.15, "K", "25 °C"),
        ("Reference charge-air coolant temperature", "Tcr", 298.15, "K", "25 °C"),
        ("Reference relative humidity", "φr", 0.30, "–", "ISO 3046-1 standard reference condition"),
        ("Ratio of indicated power", "k",
         "=((P_BARO-RH_/100*PS_SAT_X)/(100-0.3*PS_SAT_R))^0.7*(298.15/(T_AIR+273.15))^1.2*(298.15/(T_SW+273.15))^1.0",
         "–", "k = [(px−φx·psx)/(pr−φr·psr)]^0.7·(Tr/Tx)^1.2·(Tcr/Tcx)^1.0   (exponents m=0.7, n=1.2, s=1.0 – ISO 3046-1 Table 2, ref. D)"),
        ("Power adjustment factor", "α",
         "=K_SITE-0.7*(1-K_SITE)*(1/ETA_M-1)", "–", "α = k − 0.7(1−k)(1/ηm − 1)   (ISO 3046-1:2002, eq. 2)"),
        ("Derating applied to every catalogue rating", "Δ", "=(1-ALPHA)*100", "%", "Px = α·Pr – the catalogue kW is multiplied by α before comparing"),
    ]
    for lab, sym, val, unit, src in rows_iso:
        label(ws, sr, 1, lab); value(ws, sr, 2, sym, fmt="@", align="center")
        if isinstance(val, str) and val.startswith("="):
            calc(ws, sr, 3, val, fmt="0.0000" if sym in ("k", "α") else "0.000", bold=(sym in ("k", "α")))
        else:
            value(ws, sr, 3, val, fmt="0.000")
        value(ws, sr, 4, unit, fmt="@", align="center")
        note(ws, sr, 5, src)
        if sym == "psx": nm.add("PS_SAT_X", f"$C${sr}")
        if sym == "psr": nm.add("PS_SAT_R", f"$C${sr}")
        if sym == "k":   nm.add("K_SITE", f"$C${sr}")
        if sym == "α":   nm.add("ALPHA", f"$C${sr}")
        if sym == "Δ":   nm.add("DERATE", f"$C${sr}")
        sr += 1
    sr += 1

    # engine filters
    section(ws, sr, "J.  ENGINE SELECTION FILTER", ncols=9); sr += 1
    for lab, sym, val, unit, nte, name, fmt in [
        ("Lowest catalogue rating to consider", "Pmin", 0, "kW", "0 = no lower limit. Narrow the search if you want to exclude small engines", "MIN_KW", "0"),
        ("Highest catalogue rating to consider", "Pmax", 9999, "kW", "9999 = no practical upper limit. Lower it to restrict the search", "MAX_KW", "0"),
    ]:
        label(ws, sr, 1, lab); value(ws, sr, 2, sym, fmt="@", align="center")
        inp(ws, sr, 3, val, fmt=fmt, name=name)
        value(ws, sr, 4, unit, fmt="@", align="center"); note(ws, sr, 5, nte); sr += 1
    label(ws, sr, 1, "Exclude intermittent ratings (H / S)")
    value(ws, sr, 2, "flag", fmt="@", align="center")
    c = inp(ws, sr, 3, "NO", fmt="@"); c.alignment = Alignment(horizontal="center")
    value(ws, sr, 4, "–", fmt="@", align="center")
    note(ws, sr, 5, "YES removes the H and S ratings so only M / L / C / continuous ratings remain — recommended for a vessel running many hours a day. NO keeps the whole range eligible.")
    dv = DataValidation(type="list", formula1='"YES,NO"', allow_blank=False)
    ws.add_data_validation(dv); dv.add(c)
    nm.add("ALLOW_HS", f"$C${sr}"); sr += 2

    # overrides
    section(ws, r - 0 if False else sr, "K.  EXPERT OVERRIDES  (leave all empty unless you have model-test data)", ncols=9); sr += 1
    for lab, sym, val, nte, name, fmt in [
        ("Wake fraction w", "w", None, "Blank = calculated with Holtrop & Mennen (1982). Model test or CFD value overrides.", "W_OVR", "0.000"),
        ("Thrust deduction t", "t", None, "Blank = calculated. Override only with a measured value.", "T_OVR", "0.000"),
        ("Relative rotative efficiency ηR", "ηR", None, "Blank = calculated from the Holtrop formula using the design AE/A0.", "ETA_R_OVR", "0.000"),
        ("Form factor (1+k1) – enter the factor, e.g. 1.18", "1+k1", None, "Blank = calculated. A Prohaska form factor from a model test is always preferable.", "K1_OVR", "0.000"),
    ]:
        label(ws, sr, 1, lab); value(ws, sr, 2, sym, fmt="@", align="center")
        inp(ws, sr, 3, val, fmt=fmt, name=name)
        value(ws, sr, 4, "–", fmt="@", align="center"); note(ws, sr, 5, nte); sr += 1
    sr += 1
    section(ws, sr, "L.  VESSEL-TYPE GUIDANCE  —  typical proportions for the Maldivian fleet", ncols=9); sr += 1
    note(ws, sr, 1, "Reference ranges compiled from Maldivian yard practice and ITTC/Holtrop calibration experience. They are "
                    "advisory: the calculation itself never uses them, but a hull outside its family is worth a second look.",
         size=8, span=8)
    sr += 1
    thead(ws, sr, [(1, "Vessel type"), (2, "CB, min"), (3, "CB, max"), (4, "L/B min"), (5, "L/B max"),
                   (6, "B/T min"), (7, "B/T max"), (8, "Typical speed [kn]")], height=30)
    sr += 1
    TYPES = [
        ("Passenger ferry / mechanised dhoni", 0.55, 0.70, 3.8, 5.5, 3.5, 5.5, "8 – 12"),
        ("Speed launch / water taxi", 0.45, 0.60, 4.0, 6.0, 4.0, 6.5, "18 – 30"),
        ("Safari boat (liveaboard)", 0.55, 0.70, 3.8, 5.2, 4.0, 6.0, "9 – 14"),
        ("Fishing vessel (masdhoni)", 0.55, 0.72, 3.5, 5.0, 3.5, 5.0, "8 – 11"),
        ("Landing craft / RoRo barge", 0.65, 0.85, 3.5, 5.0, 4.0, 7.0, "7 – 10"),
        ("Tug / workboat", 0.50, 0.62, 3.5, 5.0, 2.8, 4.0, "10 – 13"),
        ("Cargo / supply vessel", 0.65, 0.80, 4.5, 6.5, 3.0, 5.0, "9 – 13"),
        ("Patrol / enforcement craft", 0.40, 0.55, 4.5, 6.5, 4.5, 7.0, "20 – 35"),
        ("Diving / support boat", 0.50, 0.65, 3.8, 5.5, 4.0, 6.0, "10 – 16"),
        ("Other", 0.40, 0.85, 3.0, 7.0, 2.5, 7.0, "6 – 35"),
    ]
    t0_ = sr
    for name_, cb1, cb2, lb1, lb2, bt1, bt2, spd in TYPES:
        label(ws, sr, 1, name_, size=9)
        calc(ws, sr, 2, cb1, fmt="0.00", size=9); calc(ws, sr, 3, cb2, fmt="0.00", size=9)
        calc(ws, sr, 4, lb1, fmt="0.0", size=9); calc(ws, sr, 5, lb2, fmt="0.0", size=9)
        calc(ws, sr, 6, bt1, fmt="0.0", size=9); calc(ws, sr, 7, bt2, fmt="0.0", size=9)
        value(ws, sr, 8, spd, fmt="@", align="center", size=9)
        sr += 1
    t1_ = sr - 1
    nm.add("VSL_TYPE_LIST", "'1 Input'!$A$%d:$A$%d" % (t0_, t1_))
    if type_row:
        dv2 = DataValidation(type="list", formula1="=VSL_TYPE_LIST", allow_blank=False,
                             showErrorMessage=True, errorTitle="Vessel type",
                             error="Choose a type from the list; the guidance block below the inputs uses it.")
        ws.add_data_validation(dv2)
        dv2.add(ws.cell(row=type_row, column=3))
    sr += 1
    idx = f'IFERROR(MATCH(VSL_TYPE,$A${t0_}:$A${t1_},0),0)'
    label(ws, sr, 1, "Guidance for the selected type", bold=True)
    calc(ws, sr, 2, f"={idx}", fmt="0", size=9)
    note(ws, sr, 5, "Row of the table above that matches the vessel type on the first line of this sheet.", size=8)
    sr += 1
    for lab, expr, lo_c, hi_c in [
        ("Block coefficient inside the family band", "=CB_", 2, 3),
        ("Length/beam ratio inside the family band", "=(L_WL/B_MLD)", 4, 5),
        ("Beam/draught ratio inside the family band", "=(B_MLD/T_LOAD)", 6, 7),
    ]:
        label(ws, sr, 1, lab)
        calc(ws, sr, 2, expr, fmt="0.00", size=9)
        calc(ws, sr, 3, f"=IF($B${sr-1}=0,\"type not in table\",IF(AND(B{sr}>=INDEX($B${t0_}:$G${t1_},$B${sr-1},{lo_c}-1),"
                        f"B{sr}<=INDEX($B${t0_}:$G${t1_},$B${sr-1},{hi_c}-1)),\"in range\",\"outside typical band\"))",
             fmt="@", bold=True, size=9)
        ws.conditional_formatting.add(f"C{sr}", CellIsRule(operator="equal", formula=['"in range"'],
                                      fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
        ws.conditional_formatting.add(f"C{sr}", CellIsRule(operator="equal", formula=['"outside typical band"'],
                                      fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT)))
        sr += 1
    sr += 1
    label(ws, sr, 1, "Colour legend", bold=True, size=9)
    c = ws.cell(row=sr, column=2, value="input"); c.fill = fill(INPUT_FILL); c.font = Font(name=FONT, size=8)
    c.border = Border(left=Side(style="thin", color=INPUT_BRD), right=Side(style="thin", color=INPUT_BRD),
                      top=Side(style="thin", color=INPUT_BRD), bottom=Side(style="thin", color=INPUT_BRD))
    c.alignment = Alignment(horizontal="center")
    c = ws.cell(row=sr, column=3, value="calculated"); c.fill = fill(GREY_LT); c.font = Font(name=FONT, size=8)
    c = ws.cell(row=sr, column=4, value="result"); c.fill = fill(OUT_FILL); c.font = Font(name=FONT, size=8)
    c.alignment = Alignment(horizontal="center")

    ws.freeze_panes = "A4"
    return ws
