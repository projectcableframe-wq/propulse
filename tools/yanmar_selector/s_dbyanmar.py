"""Sheet 6 - the Yanmar catalogue in detail."""
from theme import *
from openpyxl.utils import get_column_letter as gcl
import db


def build(wb, nm):
    ws = wb.create_sheet("6 Yanmar data")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 13, "B": 9, "C": 8, "D": 9, "E": 8, "F": 8, "G": 7, "H": 9, "I": 10, "J": 10,
                "K": 11, "L": 11, "M": 11, "N": 30, "O": 46})
    title(ws, "6  YANMAR MARINE ENGINE DATA  —  AS PUBLISHED, WITH DERIVED SPECIFIC FIGURES",
          "Only YANMAR commercial marine engines are used anywhere in this workbook. Every number below is the "
          "manufacturer's published value; the last columns are derived from them and from the site correction of sheet 1.",
          ncols=15)

    r = 4
    section(ws, r, "A.  RANGE", ncols=15); r += 1
    thead(ws, r, [(1, "Model"), (2, "Series"), (3, "Rating"), (4, "kW ISO"), (5, "mhp"), (6, "rpm"),
                  (7, "Cyl"), (8, "Litres"), (9, "Dry mass [kg]"), (10, "kW/litre"), (11, "kW/kg"),
                  (12, "P site [kW]"), (13, "Gearbox"), (14, "Ratios offered"), (15, "Source")], height=34)
    r += 1
    d0 = r
    for model, series, duty, kw, mhp, rpm, cyl, disp, mass, gear, ratios, src in db.YANMAR:
        value(ws, r, 1, model, fmt="@", bold=True, size=10)
        value(ws, r, 2, series, fmt="@", size=9)
        value(ws, r, 3, db.RATING_NOTE.get(duty, duty).split("(")[0].strip(), fmt="@", size=8)
        calc(ws, r, 4, kw, fmt="0.0")
        calc(ws, r, 5, mhp, fmt="0")
        calc(ws, r, 6, rpm, fmt="0")
        calc(ws, r, 7, cyl, fmt="0")
        calc(ws, r, 8, disp, fmt="0.000")
        calc(ws, r, 9, mass, fmt="#,##0")
        calc(ws, r, 10, f"=D{r}/H{r}", fmt="0.0")
        calc(ws, r, 11, f'=IF(ISNUMBER(I{r}),D{r}/I{r},"–")', fmt="0.000")
        calc(ws, r, 12, f"=D{r}*ALPHA", fmt="0.0", bold=True)
        value(ws, r, 13, gear, fmt="@", size=9)
        value(ws, r, 14, ", ".join("%.3f" % x for x in ratios), fmt="@", size=8)
        note(ws, r, 15, src, size=7)
        r += 1
    dl = r - 1

    r += 1
    section(ws, r, "B.  DUTY CLASSES  —  the rating letter carried by each model", ncols=15); r += 1
    thead(ws, r, [(1, "Letter"), (2, "Meaning")], height=20); r += 1
    for k, v in db.RATING_NOTE.items():
        value(ws, r, 1, k, fmt="@", align="center", bold=True)
        note(ws, r, 2, v, size=9, span=6)
        r += 1

    r += 1
    section(ws, r, "C.  HOW THE SITE CORRECTION IS APPLIED", ncols=15); r += 1
    for txt in [
        "The catalogue rating (column D) is the ISO 8665 / ISO 3046-1 brake power at the standard reference "
        "conditions: 100 kPa, 25 °C air, 30 % relative humidity, charge-air coolant 25 °C.",
        "On site the air is hotter and more humid and the sea water is warmer, so the engine can only deliver the "
        "site-corrected power  Pr,site = α · Pr  (column L).  α is computed on sheet 1 by the ISO 3046-1 procedure.",
        "The recommendation on sheet 5 is made on Pr,site, never on the catalogue rating — this is the whole point of "
        "the derating: a 440 mhp engine sold in Europe delivers less than that in Maldivian conditions.",
        "The propeller curve of sheet 4 is the load; the engine must be able to carry that load continuously with the "
        "engine margin of sheet 1 kept in reserve.",
    ]:
        note(ws, r, 1, "•  " + txt, size=9, span=14)
        ws.row_dimensions[r].height = 26
        r += 1

    ws.freeze_panes = "B%d" % d0
    ws.auto_filter.ref = f"A{d0-1}:O{dl}"
    return ws
