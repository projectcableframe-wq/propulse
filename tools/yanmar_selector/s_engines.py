"""Sheet 5 - Yanmar engine selection on site-corrected ratings."""
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as gcl
from theme import *
import db

BIG = 1000000


def build(wb, nm):
    ws = wb.create_sheet("5 Engines")
    ws.sheet_view.showGridLines = False
    title(ws, "5  YANMAR ENGINE SELECTION  —  RANKED ON SITE-CORRECTED OUTPUT",
          "Every YANMAR commercial engine is derated to the tropical site of sheet 1 (ISO 3046-1), then matched to the "
          "propeller demand at its own gear ratio. The smallest engine that still keeps the required reserve ranks first.",
          ncols=39)

    # column widths
    for c in range(1, 40):
        ws.column_dimensions[gcl(c)].width = 11
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 11
    ws.column_dimensions["J"].width = 12
    for c in range(11, 16):
        ws.column_dimensions[gcl(c)].width = 8
    ws.column_dimensions["P"].width = 11
    for c in range(17, 27):
        ws.column_dimensions[gcl(c)].width = 9
    for c in range(27, 40):
        ws.column_dimensions[gcl(c)].width = 11
    ws.column_dimensions["AK"].width = 10
    ws.column_dimensions["AL"].width = 8

    r = 4
    section(ws, r, "A.  THE WHOLE YANMAR COMMERCIAL RANGE, ONE ROW PER PUBLISHED RATING", ncols=39)
    r += 1
    heads = [(1, "Model"), (2, "Series"), (3, "Rating"), (4, "kW (ISO)"), (5, "mhp"), (6, "rpm"), (7, "Cyl"),
             (8, "Litres"), (9, "Dry mass [kg]"), (10, "Gearbox")]
    heads += [(11 + i, "Ratio %d" % (i + 1)) for i in range(5)]
    heads += [(16, "P site [kW]")]
    heads += [(17 + i, "n%d [rpm]" % (i + 1)) for i in range(5)]
    heads += [(22 + i, "PD%d [kW]" % (i + 1)) for i in range(5)]
    heads += [(27, "PD best [kW]"), (28, "Ratio #"), (29, "Ratio"), (30, "n shaft [rpm]"), (31, "PD [kW]"),
              (32, "PS [kW]"), (33, "PB [kW]"), (34, "MCR req [kW]"), (35, "Load on engine"), (36, "Utilisation"),
              (37, "Feasible"), (38, "Rank"), (39, "Fuel [kg/h]")]
    hdr = r
    thead(ws, r, heads, height=46)
    r += 1
    d0 = r
    for i, e in enumerate(db.YANMAR):
        model, series, duty, kw, mhp, rpm, cyl, disp, mass, gear, ratios, src = e
        rr = d0 + i
        value(ws, rr, 1, model, fmt="@", bold=True, size=10)
        value(ws, rr, 2, series, fmt="@", size=9)
        value(ws, rr, 3, duty, fmt="@", align="center", size=9)
        value(ws, rr, 4, kw, fmt="0.0")
        value(ws, rr, 5, mhp, fmt="0")
        value(ws, rr, 6, rpm, fmt="0")
        value(ws, rr, 7, cyl, fmt="0", align="center")
        value(ws, rr, 8, disp, fmt="0.000")
        value(ws, rr, 9, mass if mass else "–", fmt="#,##0", align="right")
        value(ws, rr, 10, gear, fmt="@", size=9)
        for k in range(5):
            c = 11 + k
            calc(ws, rr, c, ratios[k] if k < len(ratios) else "–", fmt="0.000", size=9)
        calc(ws, rr, 16, f"=D{rr}*ALPHA", fmt="0.0", bold=True)
        for k in range(5):
            c = 17 + k
            calc(ws, rr, c, f'=IF({gcl(11+k)}{rr}="–","",F{rr}/{gcl(11+k)}{rr})', fmt="0", size=9)
        for k in range(5):
            c = 22 + k
            nref = f"{gcl(17+k)}{rr}"
            m = f"MATCH({nref},SW_N,1)"
            interp = (f"INDEX(SW_PD,{m})+({nref}-INDEX(SW_N,{m}))/(INDEX(SW_N,{m}+1)-INDEX(SW_N,{m}))"
                      f"*(INDEX(SW_PD,{m}+1)-INDEX(SW_PD,{m}))")
            guard = (f'OR({nref}<MIN(SW_N),{nref}>=MAX(SW_N),INDEX(SW_STATUS,{m})<>"OK",'
                     f'INDEX(SW_STATUS,{m}+1)<>"OK")')
            calc(ws, rr, c, f'=IF({nref}="",{BIG},IF({guard},{BIG},{interp}))', fmt="#,##0.0", size=9)
        # best ratio = lowest delivered power that is inside the sweep
        rng = f"V{rr}:Z{rr}"
        calc(ws, rr, 27, f"=MIN({rng})", fmt="#,##0.0", bold=True)
        calc(ws, rr, 28, f'=IF(MIN({rng})>={BIG},"–",MATCH(MIN({rng}),{rng},0))', fmt="0")
        calc(ws, rr, 29, f'=IF(AA{rr}>={BIG},"–",INDEX(K{rr}:O{rr},1,AB{rr}))', fmt="0.000")
        calc(ws, rr, 30, f'=IF(AA{rr}>={BIG},"–",F{rr}/AC{rr})', fmt="0", bold=True)
        calc(ws, rr, 31, f'=IF(AA{rr}>={BIG},"–",AA{rr})', fmt="#,##0.0", bold=True)
        calc(ws, rr, 32, f'=IF(AA{rr}>={BIG},"–",AE{rr}/ETA_S)', fmt="#,##0.0")
        calc(ws, rr, 33, f'=IF(AA{rr}>={BIG},"–",AF{rr}/ETA_G)', fmt="#,##0.0", bold=True)
        calc(ws, rr, 34, f'=IF(AA{rr}>={BIG},"–",AG{rr}/(1-EM_/100))', fmt="#,##0.0")
        calc(ws, rr, 35, f'=IF(AA{rr}>={BIG},"–",AG{rr}/P{rr})', fmt="0.0%")
        calc(ws, rr, 36, f'=IF(AA{rr}>={BIG},"–",AH{rr}/P{rr})', fmt="0.0%")
        calc(ws, rr, 37,
             f'=IF(AND(ISNUMBER(AI{rr}),AI{rr}<=LOAD_MAX/100,AJ{rr}<=1,D{rr}>=MIN_KW,D{rr}<=MAX_KW,'
             f'IF(ALLOW_HS="YES",NOT(OR(C{rr}="H",C{rr}="S")),TRUE)),"YES","NO")', fmt="@", bold=True)
        calc(ws, rr, 39, f'=IF(AA{rr}>={BIG},"–",AG{rr}*BSFC_/1000)', fmt="0.0")
    dl = d0 + len(db.YANMAR) - 1
    # ranks (needs the whole feasible column)
    for i in range(len(db.YANMAR)):
        rr = d0 + i
        calc(ws, rr, 38,
             f'=IF(AK{rr}<>"YES","–",1+SUMPRODUCT(($AK${d0}:$AK${dl}="YES")*($AJ${d0}:$AJ${dl}>AJ{rr}))'
             f'+SUMPRODUCT(($AK${d0}:$AK${dl}="YES")*($AJ${d0}:$AJ${dl}=AJ{rr})*($A${d0}:$A${dl}<A{rr})))',
             fmt="0", bold=True)
    ws.conditional_formatting.add(f"AK{d0}:AK{dl}", CellIsRule(operator="equal", formula=['"YES"'],
                                  fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
    ws.conditional_formatting.add(f"AL{d0}:AL{dl}", CellIsRule(operator="equal", formula=["1"],
                                  fill=fill(GOLD), font=Font(name=FONT, color="FFFFFF", bold=True)))
    ws.conditional_formatting.add(f"AI{d0}:AI{dl}", CellIsRule(operator="greaterThan", formula=["0.999"],
                                  fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT)))
    r = dl + 2

    # ------------------------------------------------------------ selection
    section(ws, r, "B.  RECOMMENDED ENGINE  —  rank 1 of the list above", ncols=39); r += 1
    thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, ""), (5, "Note")], height=20)
    r += 1
    rank_rng = f"$AL${d0}:$AL${dl}"

    def sel(lab, sym, col, fmt, note_txt, name=None, bold=True, isres=True):
        nonlocal r
        label(ws, r, 1, lab, bold=bold)
        value(ws, r, 2, sym, fmt="@", align="center", size=9)
        f = f'=IFERROR(INDEX({col}{d0}:{col}{dl},MATCH(1,{rank_rng},0)),"–")'
        if isres:
            result(ws, r, 3, f, fmt=fmt)
        else:
            calc(ws, r, 3, f, fmt=fmt, bold=bold)
        note(ws, r, 5, note_txt, size=8, span=6)
        if name:
            nm.add(name, "C%d" % r)
        r += 1
        return r - 1

    r_msg = r
    c = ws.cell(row=r, column=1, value='=IF(COUNTIF(%s,1)=0,"⚠  No YANMAR engine with a catalogued reduction ratio can carry this '
                                       'propeller — widen the kW band on sheet 1, change the aperture or ask YANMAR for a special '
                                       'ratio.","")' % rank_rng)
    c.font = Font(name=FONT, size=10, bold=True, color=WARN_FONT)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
    r += 1
    r_mod = sel("Engine model", "", "A", "@", "Rank 1 = smallest engine that still keeps the required reserve", "ENG_MODEL")
    r_ser = sel("Series", "", "B", "@", "YANMAR series", "ENG_SERIES", bold=False, isres=False)
    r_duty = sel("Rating class", "", "C", "@", "Duty letter as published by YANMAR", "ENG_DUTY", bold=False, isres=False)
    r_kw = sel("Rated output (ISO 8665 / ISO 3046)", "Pr", "D", "0.0",
               "Catalogue rating at the standard reference conditions", "ENG_KW", isres=False)
    r_psite = sel("SITE-CORRECTED OUTPUT", "Pr,site", "P", "0.0",
                  "Pr × α : tropical derating of sheet 1 applied to the catalogue rating", "ENG_PSITE")
    r_rpm = sel("Rated speed", "nr", "F", "0", "Catalogue speed", "ENG_RPM", isres=False)
    r_gear = sel("Gearbox", "", "J", "@", "Matching YANMAR marine gear", "ENG_GEARBOX", isres=False)
    r_ratio = sel("Gear ratio selected", "i", "AC", "0.000",
                  "Ratio that gives the lowest delivered power for this engine", "ENG_RATIO")
    r_nsel = sel("SHAFT SPEED", "n", "AD", "#,##0", "n = nr / i", "ENG_NSEL")
    ws.cell(row=r_nsel, column=3).value = (
        "=IFERROR(INDEX($AD$%d:$AD$%d,MATCH(1,%s,0)),N_OPT)" % (d0, dl, rank_rng))
    r_pdsel = sel("Delivered power at the design point", "PD", "AE", "#,##0.0",
                  "From sheet 4, propeller solved at this shaft speed", "ENG_PD")
    r_pssel = sel("Shaft power", "PS", "AF", "#,##0.0", "PS = PD/ηS", "ENG_PS")
    r_pbsel = sel("Brake power at service speed", "PB", "AG", "#,##0.0", "PB = PS/ηG", "ENG_PB")
    r_mcrsel = sel("Required engine rating (MCR)", "PMCR,req", "AH", "#,##0.0",
                   "PB/(1 − engine margin) : the rating that must be available on site", "ENG_PMCR")
    r_load = sel("Engine load at service speed", "PB/Pr,site", "AI", "0.0%",
                 "Continuous load on the site-corrected rating", "ENG_LOAD")
    r_util = sel("Utilisation of the site-corrected rating", "PMCR,req/Pr,site", "AJ", "0.0%",
                 "Must stay ≤ 100 %; the design goal is ≈ 85–95 %", "ENG_UTIL")
    r_mass = sel("Dry mass", "m", "I", "#,##0", "Engine only, without gearbox", "ENG_MASS", bold=False, isres=False)
    r_fuel = sel("Fuel consumption at service speed", "ṁ", "AM", "0.0",
                 "ṁ = PB · BSFC / 1000 [kg/h]", "ENG_FUEL")
    r_fueld = sel("Fuel consumption per day", "ṁ·h", "", "0.0", "× hours per day of sheet 1", "ENG_FUEL_DAY")
    ws.cell(row=r_fueld, column=3).value = '=IF(ISNUMBER(ENG_FUEL),ENG_FUEL*HRS_,"–")'
    ws.cell(row=r_fueld, column=3).number_format = "0.0"
    r += 1

    section(ws, r, "C.  SHORTLIST  —  the five best matches", ncols=39); r += 1
    thead(ws, r, [(1, "Rank"), (2, "Model"), (3, "kW ISO"), (4, "P site [kW]"), (5, "rpm"), (6, "Gearbox"),
                  (7, "Ratio"), (8, "n [rpm]"), (9, "PB [kW]"), (10, "Load"), (11, "Fuel [kg/h]")], height=30)
    r += 1
    for k in range(5):
        value(ws, r, 1, k + 1, fmt="0", align="center", bold=True)
        calc(ws, r, 2, f'=IFERROR(INDEX($A${d0}:$A${dl},MATCH({k+1},$AL${d0}:$AL${dl},0)),"–")', fmt="@", bold=True)
        for col, c in (("D", 3), ("P", 4), ("F", 5), ("J", 6), ("AC", 7), ("AD", 8), ("AG", 9), ("AI", 10), ("AM", 11)):
            fmt = "0.0%" if col == "AI" else ("@" if col == "J" else ("#,##0.0"))
            calc(ws, r, c, f'=IFERROR(INDEX(${col}${d0}:${col}${dl},MATCH({k+1},$AL${d0}:$AL${dl},0)),"–")', fmt=fmt)
        r += 1
    r += 1

    note(ws, r, 1, "Ratings are the published YANMAR figures; the site correction α is the ISO 3046-1 correction computed on "
                   "sheet 1 from the tropical air and sea-water temperatures. Engines marked NO are outside the kW band, the "
                   "rating filter, or cannot absorb the propeller load.", size=9, span=14)
    r += 2
    for txt in [
        "The delivered power of each engine/gear combination is read from the propeller curve of sheet 4 by linear "
        "interpolation between the 75 rev/min grid points (±0.5 % — used for ranking only). Once an engine is selected, "
        "sheet 4 re-solves the pitch ratio exactly at that shaft speed and its figures are the ones to quote.",
        "Ranking rule: among the feasible engines, rank 1 is the one that carries the propeller load with the least "
        "spare — that is, the smallest engine that still keeps the whole engine margin of sheet 1 in hand. Rank 2 and "
        "3 are the next larger engines, listed so the owner can trade weight, price and reserve.",
        "Feasible means: site-corrected load ≤ the maximum continuous load of sheet 1, required MCR ≤ site-corrected "
        "rating, catalogue rating inside the kW band, and duty class accepted by the filter. Nothing else is hidden.",
        "YANMAR publishes several ratings for the same block (M / L / H / S / C). Each published rating is a row of its "
        "own: the same engine may therefore appear twice, with different power, and that is intentional.",
    ]:
        note(ws, r, 1, "•  " + txt, size=9, span=14)
        ws.row_dimensions[r].height = 26
        r += 1
    ws.freeze_panes = "B%d" % (d0)
    return ws
