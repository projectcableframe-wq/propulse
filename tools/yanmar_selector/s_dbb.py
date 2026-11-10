"""Sheet 8 - Wageningen B-series coefficient tables and open-water curves."""
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.styles import Font
from theme import *
import db


def build(wb, nm):
    ws = wb.create_sheet("8 B-series")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 14, "B": 10, "C": 10, "D": 10, "E": 10, "F": 6, "G": 14, "H": 10, "I": 10,
                "J": 10, "K": 10, "L": 10, "M": 12, "N": 12})
    title(ws, "8  WAGENINGEN B-SERIES  —  POLYNOMIAL COEFFICIENTS AND OPEN-WATER CURVES",
          "KT = Σ C·J^s·(P/D)^t·(AE/A0)^u·Z^v   and the same sum with the KQ coefficient set. "
          "These are the 39 + 47 coefficients of Oosterveld & van Oossanen (1975) as re-published by Bernitsas, Ray & Kinley (1981).",
          ncols=11)

    r = 4
    section(ws, r, "A.  KT COEFFICIENTS", ncols=6); r += 1
    thead(ws, r, [(1, "C"), (2, "s  (J)"), (3, "t  (P/D)"), (4, "u  (AE/A0)"), (5, "v  (Z)")], height=20)
    k0 = r + 1
    for i, (C, s, t, u, v) in enumerate(db.KT_COEF):
        rr = k0 + i
        for j, val in enumerate((C, s, t, u, v)):
            calc(ws, rr, j + 1, val, fmt="0.000000000", size=9)
    k1 = k0 + len(db.KT_COEF) - 1
    nm.add("KT_C", "'8 B-series'!$A$%d:$A$%d" % (k0, k1))
    nm.add("KT_S", "'8 B-series'!$B$%d:$B$%d" % (k0, k1))
    nm.add("KT_T", "'8 B-series'!$C$%d:$C$%d" % (k0, k1))
    nm.add("KT_U", "'8 B-series'!$D$%d:$D$%d" % (k0, k1))
    nm.add("KT_V", "'8 B-series'!$E$%d:$E$%d" % (k0, k1))

    for cc in range(7, 12):
        ws.cell(row=4, column=cc).fill = fill(TEAL_DK)
    cq = ws.cell(row=4, column=7, value="B.  KQ COEFFICIENTS")
    cq.font = Font(name=FONT, size=11, bold=True, color=WHITE)
    thead(ws, 5, [(7, "C"), (8, "s  (J)"), (9, "t  (P/D)"), (10, "u  (AE/A0)"), (11, "v  (Z)")], height=20)
    for i, (C, s, t, u, v) in enumerate(db.KQ_COEF):
        rr = k0 + i
        for j, val in enumerate((C, s, t, u, v)):
            calc(ws, rr, j + 7, val, fmt="0.000000000", size=9)
    k2 = k0 + len(db.KQ_COEF) - 1
    nm.add("KQ_C", "'8 B-series'!$G$%d:$G$%d" % (k0, k2))
    nm.add("KQ_S", "'8 B-series'!$H$%d:$H$%d" % (k0, k2))
    nm.add("KQ_T", "'8 B-series'!$I$%d:$I$%d" % (k0, k2))
    nm.add("KQ_U", "'8 B-series'!$J$%d:$J$%d" % (k0, k2))
    nm.add("KQ_V", "'8 B-series'!$K$%d:$K$%d" % (k0, k2))

    r = max(k1, k2) + 2
    section(ws, r, "C.  VALIDITY OF THE SERIES  (outside these limits the polynomial is an extrapolation)", ncols=11)
    r += 1
    thead(ws, r, [(1, "Parameter"), (2, "Minimum"), (3, "Maximum"), (4, "Design value"), (5, "Inside?")], height=20)
    r += 1
    lims = [("Advance coefficient J", 0.0, 1.8, "=J_FIN", '=IF(AND(J_FIN>=0,J_FIN<=1.8),"YES","NO")'),
            ("Pitch ratio P/D", 0.5, 1.4, "=FIN_PD", '=IF(AND(FIN_PD>=0.5,FIN_PD<=1.4),"YES","NO")'),
            ("Blade-area ratio AE/A0", 0.3, 1.05, "=AE_PROP", '=IF(AND(AE_PROP>=0.3,AE_PROP<=1.05),"YES","NO")'),
            ("Number of blades Z", 2, 7, "=Z_BL", '=IF(AND(Z_BL>=2,Z_BL<=7),"YES","NO")')]
    for lab, lo, hi, val, verdict in lims:
        label(ws, r, 1, lab)
        calc(ws, r, 2, lo, fmt="0.00"); calc(ws, r, 3, hi, fmt="0.00")
        calc(ws, r, 4, val, fmt="0.000"); calc(ws, r, 5, verdict, fmt="@", bold=True)
        r += 1
    note(ws, r, 1, "The series covers Z = 2…7, AE/A0 = 0.30…1.05 and P/D = 0.5…1.4. "
                   "Z = 2 and Z = 7 are thin-data corners and are flagged on purpose.", size=9, span=11)

    # ------------------------------------------------ open-water curves of the designed propeller
    r += 2
    section(ws, r, "D.  OPEN-WATER DIAGRAM OF THE SELECTED PROPELLER  "
                  "(Z, AE/A0 from sheet 4; the P/D is the solved value)", ncols=11)
    r += 1
    label(ws, r, 1, "Pitch ratio used for the curves")
    calc(ws, r, 2, "=FIN_PD", fmt="0.000", bold=True)
    nm.add("CURVE_PD", "'8 B-series'!$B$%d" % r)
    r += 1
    thead(ws, r, [(1, "J"), (2, "KT"), (3, "10·KQ"), (4, "ηO"), (5, "J·(KT)²/KQ")], height=20)
    r += 1
    c0 = r
    for i in range(15):
        J = 0.1 + 0.1 * i
        calc(ws, r, 1, round(J, 1), fmt="0.00")
        calc(ws, r, 2, f"=SUMPRODUCT(KT_C,A{r}^KT_S,CURVE_PD^KT_T,AE_PROP^KT_U,Z_BL^KT_V)", fmt="0.0000")
        calc(ws, r, 3, f"=SUMPRODUCT(KQ_C,A{r}^KQ_S,CURVE_PD^KQ_T,AE_PROP^KQ_U,Z_BL^KQ_V)*10", fmt="0.0000")
        calc(ws, r, 4, f"=IF(C{r}<=0,0,A{r}*B{r}/(2*PI()*C{r}/10))", fmt="0.0000")
        calc(ws, r, 5, f"=IF(C{r}<=0,0,A{r}*B{r}^2/(C{r}/10))", fmt="0.000", size=9)
        r += 1
    c1 = r - 1

    ch = ScatterChart()
    ch.title = "KT and 10·KQ against advance coefficient J"
    ch.style = 2
    ch.x_axis.title = "J"
    ch.y_axis.title = "KT  /  10·KQ"
    ch.height = 8.5; ch.width = 15
    ch.x_axis.majorGridlines = None
    xref = Reference(ws, min_col=1, min_row=c0, max_row=c1)
    s1 = Series(Reference(ws, min_col=2, min_row=c0, max_row=c1), xref, title="KT")
    s1.marker = Marker(symbol="circle", size=5)
    s2 = Series(Reference(ws, min_col=3, min_row=c0, max_row=c1), xref, title="10·KQ")
    s2.marker = Marker(symbol="square", size=4)
    ch.series.append(s1); ch.series.append(s2)
    ws.add_chart(ch, "G%d" % (r + 1))

    ch2 = ScatterChart()
    ch2.title = "Open-water efficiency ηO against J"
    ch2.style = 2
    ch2.x_axis.title = "J"
    ch2.y_axis.title = "ηO"
    ch2.height = 8.5; ch2.width = 15
    ch2.x_axis.majorGridlines = None
    s3 = Series(Reference(ws, min_col=4, min_row=c0, max_row=c1), xref, title="ηO")
    s3.marker = Marker(symbol="diamond", size=4)
    ch2.series.append(s3)
    ws.add_chart(ch2, "G%d" % (r + 18))
    return ws
