"""Sheet 4 - Propeller design (Wageningen B-series, fixed pitch)."""
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import CellIsRule
from theme import *

N_RPM = 31          # rpm sweep points
N_ITER = 10         # bisection steps inside the sweep
N_FIN = 16          # bisection steps for the final design


def build(wb, nm):
    ws = wb.create_sheet("4 Propeller")
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 50, "B": 13, "C": 13, "D": 13, "E": 12, "F": 12, "G": 12, "H": 12, "I": 12,
                "J": 12, "K": 12, "L": 17, "M": 12, "N": 14})
    title(ws, "4  PROPELLER  —  WAGENINGEN B-SERIES, SINGLE SCREW, FIXED PITCH",
          "For every shaft speed the pitch ratio is solved so that the propeller produces exactly the thrust required "
          "at the service speed; the delivered power follows from KQ. Keller's criterion fixes the blade area.", ncols=14)

    r = 4
    section(ws, r, "A.  DESIGN BASIS", ncols=14); r += 1
    thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Unit"), (5, "Equation / source")], height=20)
    r += 1

    def row(lab, sym, formula, unit, eq, fmt="0.000", name=None, bold=False, isres=False):
        nonlocal r
        label(ws, r, 1, lab, bold=bold)
        value(ws, r, 2, sym, fmt="@", align="center", size=9)
        if isres:
            result(ws, r, 3, formula, fmt=fmt)
        else:
            calc(ws, r, 3, formula, fmt=fmt, bold=bold)
        value(ws, r, 4, unit, fmt="@", align="center")
        note(ws, r, 5, eq, size=8, span=6)
        if name:
            nm.add(name, "C%d" % r)
        r += 1
        return r - 1

    # ---- design basis
    r_D = row("Design propeller diameter", "D", "=IF(ISNUMBER(D_MAX),D_MAX,D_MAX_AUTO)", "m",
              "D = D_max from the aperture (sheet 1), unless overridden", "0.000", name="D_PROP", bold=True)
    r_h = row("Shaft immersion below the waterline", "h", "=T_LOAD-(TIP_CLR+D_PROP/2)", "m",
              "h = T − (tip clearance + D/2)", "0.000", name="H_SHAFT")
    r_p0 = row("Absolute static pressure at the shaft", "p0", "=101325+RHO_W*G_*H_SHAFT", "Pa",
               "p0 = patm + ρ·g·h   with patm = 101 325 Pa", "#,##0", name="P0_")
    r_pv = row("Vapour pressure of sea water", "pv", "=0.61121*EXP(17.502*T_SW/(T_SW+240.97))*1000", "Pa",
               "pv = 0.61121·exp[17.502·t/(t + 240.97)] kPa  (Buck, t in °C)", "#,##0", name="PV_")
    r_T = row("Thrust required at service speed (sea margin included)", "T", "=THRUST_L", "N",
              "T = RT,service/(1 − t)   (sheet 3)", "#,##0", name="T_DESIGN")
    r_kel = row("Keller minimum blade-area ratio", "(AE/A0)min", "=(1.3+0.3*Z_BL)*T_DESIGN/((P0_-PV_)*D_PROP^2)", "–",
                "(AE/A0)min = (1.3 + 0.3Z)·T/[(p0 − pv)·D²]   (k = 0)", "0.0000", name="AE_KELLER")
    r_ae = row("Blade-area ratio adopted", "AE/A0", "=MIN(1.05,CEILING(MAX(AE_KELLER,AE_MIN),0.05))", "–",
               "Largest of Keller and the user minimum, rounded up to the nearest 0.05 of the series", "0.00",
               name="AE_PROP", bold=True, isres=True)
    r_imm = row("Immersion ratio", "h/D", "=H_SHAFT/D_PROP", "–", "Should be ≥ 1.0 for a fully submerged propeller", "0.000")
    r += 2

    # ---- sweep (positions fixed before writing)
    section(ws, r, "B.  THRUST IDENTITY FOR EVERY SHAFT SPEED  —  pitch ratio that produces the required thrust", ncols=14)
    r += 1
    hdr = r
    thead(ws, r, [(1, "Shaft speed [rpm]"), (2, "n [1/s]"), (3, "J = VA/(nD)"), (4, "KT required"),
                  (5, "P/D solution"), (6, "KT"), (7, "KQ"), (8, "ηO"), (9, "Q [N·m]"), (10, "PD [kW]"),
                  (11, "ηD = PE(1+SM)/PD"), (12, "Status"), (13, "PB [kW]"), (14, "PD if valid [kW]")], height=42)
    sf = hdr + 1
    sl = sf + N_RPM - 1
    ib = sl + 4          # first row of the bisection log (see section C)
    for i in range(N_RPM):
        r = sf + i
        calc(ws, r, 1, 150 + i * 75, fmt="0", bold=True)
        calc(ws, r, 2, f"=A{r}/60", fmt="0.0000")
        calc(ws, r, 3, f"=VA_L/(B{r}*D_PROP)", fmt="0.0000")
        calc(ws, r, 4, f"=T_DESIGN/(RHO_W*B{r}^2*D_PROP^4)", fmt="0.00000")
        last = ib + i * N_ITER + N_ITER - 1
        calc(ws, r, 5, f"=(B{last}+C{last})/2", fmt="0.0000", bold=True)
        calc(ws, r, 6, f"=SUMPRODUCT(KT_C,C{r}^KT_S,E{r}^KT_T,AE_PROP^KT_U,Z_BL^KT_V)", fmt="0.00000")
        calc(ws, r, 7, f"=SUMPRODUCT(KQ_C,C{r}^KQ_S,E{r}^KQ_T,AE_PROP^KQ_U,Z_BL^KQ_V)", fmt="0.00000")
        calc(ws, r, 8, f"=C{r}*F{r}/(2*PI()*G{r})", fmt="0.0000", bold=True)
        calc(ws, r, 9, f"=G{r}*RHO_W*B{r}^2*D_PROP^5", fmt="#,##0")
        calc(ws, r, 10, f"=2*PI()*B{r}*I{r}/ETA_R_L/1000", fmt="#,##0.0", bold=True)
        calc(ws, r, 11, f"=PE_L*(1+SM_/100)/J{r}", fmt="0.000")
        calc(ws, r, 12,
             f'=IF(D{r}>SUMPRODUCT(KT_C,C{r}^KT_S,1.4^KT_T,AE_PROP^KT_U,Z_BL^KT_V),"P/D would exceed 1.40",'
             f'IF(D{r}<SUMPRODUCT(KT_C,C{r}^KT_S,0.5^KT_T,AE_PROP^KT_U,Z_BL^KT_V),"P/D would fall below 0.50","OK"))',
             fmt="@")
        calc(ws, r, 13, f"=J{r}/ETA_S/ETA_G", fmt="#,##0.0")
        calc(ws, r, 14, f'=IF(L{r}="OK",J{r},1000000)', fmt="#,##0.0")
    nm.add("SW_N", f"'4 Propeller'!$A${sf}:$A${sl}")
    nm.add("SW_PD", f"'4 Propeller'!$J${sf}:$J${sl}")
    nm.add("SW_STATUS", f"'4 Propeller'!$L${sf}:$L${sl}")
    nm.add("SW_PB", f"'4 Propeller'!$M${sf}:$M${sl}")
    ws.conditional_formatting.add(f"L{sf}:L{sl}", CellIsRule(operator="equal", formula=['"OK"'],
                                  fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT)))

    # ---- bisection log
    ir0 = sl + 2
    section(ws, ir0, "C.  BISECTION LOG FOR SECTION B  —  every step of the pitch-ratio solution "
                     "(grouped rows: use the +/- control at the left margin to expand)", ncols=14)
    thead(ws, ir0 + 1, [(1, "RPM point"), (2, "P/D lower"), (3, "P/D upper"), (4, "P/D test"),
                        (5, "KT at P/D test"), (6, "KT required"), (7, "Bracket update")], height=30)
    for i in range(N_RPM):
        sp = sf + i
        for s in range(N_ITER):
            rr = ib + i * N_ITER + s
            ws.row_dimensions[rr].outlineLevel = 1
            ws.row_dimensions[rr].hidden = True
            value(ws, rr, 1, int(150 + i * 75), fmt="0", align="center", size=8)
            if s == 0:
                calc(ws, rr, 2, "=0.5", fmt="0.00000", size=8)
                calc(ws, rr, 3, "=1.4", fmt="0.00000", size=8)
            else:
                calc(ws, rr, 2, f"=IF(E{rr-1}>F{rr-1},B{rr-1},D{rr-1})", fmt="0.00000", size=8)
                calc(ws, rr, 3, f"=IF(E{rr-1}>F{rr-1},D{rr-1},C{rr-1})", fmt="0.00000", size=8)
            calc(ws, rr, 4, f"=(B{rr}+C{rr})/2", fmt="0.00000", size=8)
            calc(ws, rr, 5, f"=SUMPRODUCT(KT_C,$C${sp}^KT_S,D{rr}^KT_T,AE_PROP^KT_U,Z_BL^KT_V)", fmt="0.00000", size=8)
            calc(ws, rr, 6, f"=$D${sp}", fmt="0.00000", size=8)
            calc(ws, rr, 7, f'=IF(E{rr}>F{rr},"KT too high → P/D too large → new upper limit","KT too low → P/D too small → new lower limit")',
                 fmt="@", size=8)

    # ---- optimum
    r = ib + N_RPM * N_ITER + 1
    section(ws, r, "D.  OPTIMUM SHAFT SPEED OF THE SWEEP  (reference: the engine and gear decide the actual speed)", ncols=14)
    r += 1
    thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Unit"), (5, "Note")], height=20)
    r += 1
    r_nopt = row("Shaft speed giving the lowest delivered power", "n_opt",
                 f"=INDEX(A{sf}:A{sl},MATCH(MIN(N{sf}:N{sl}),N{sf}:N{sl},0))", "rpm",
                 "Highest overall efficiency achievable at this diameter", "0", name="N_OPT", bold=True)
    r_pdopt = row("Lowest delivered power of the sweep", "PD,min", f"=MIN(N{sf}:N{sl})", "kW",
                  "Locates the efficient rpm band for the gear-ratio choice", "#,##0.0", name="PD_OPT", bold=True)
    r += 2

    # ---- final design
    section(ws, r, "E.  FINAL PROPELLER  —  solved at the shaft speed of the selected engine (sheet 5)", ncols=14); r += 1
    thead(ws, r, [(1, "Quantity"), (2, "Symbol"), (3, "Value"), (4, "Unit"), (5, "Equation / note")], height=20)
    r += 1
    r_nf = row("Shaft speed of the selected engine / gear", "n", "=ENG_NSEL", "rpm",
               "n = engine rated speed / gear ratio   (sheet 5)", "#,##0", name="FIN_N", bold=True, isres=True)
    r_jf = row("Advance coefficient", "J", "=VA_L/(FIN_N/60*D_PROP)", "–", "J = VA/(n·D)", "0.0000", name="J_FIN")
    r_kt = row("Thrust coefficient required", "KT,req", "=T_DESIGN/(RHO_W*(FIN_N/60)^2*D_PROP^4)", "–",
               "KT,req = T/(ρ·n²·D⁴)", "0.00000")
    bt = r
    thead(ws, bt, [(1, "Step"), (2, "P/D lower"), (3, "P/D upper"), (4, "P/D test"), (5, "KT at P/D test"),
                   (6, "KT required")], height=28)
    r = bt + 1
    b0 = r
    for s in range(N_FIN):
        value(ws, r, 1, s + 1, fmt="0", align="center", size=9)
        if s == 0:
            calc(ws, r, 2, "=0.5", fmt="0.00000", size=9)
            calc(ws, r, 3, "=1.4", fmt="0.00000", size=9)
        else:
            calc(ws, r, 2, f"=IF(E{r-1}>F{r-1},B{r-1},D{r-1})", fmt="0.00000", size=9)
            calc(ws, r, 3, f"=IF(E{r-1}>F{r-1},D{r-1},C{r-1})", fmt="0.00000", size=9)
        calc(ws, r, 4, f"=(B{r}+C{r})/2", fmt="0.00000", size=9)
        calc(ws, r, 5, f"=SUMPRODUCT(KT_C,$C${r_jf}^KT_S,D{r}^KT_T,AE_PROP^KT_U,Z_BL^KT_V)", fmt="0.00000", size=9)
        calc(ws, r, 6, f"=$C${r_kt}", fmt="0.00000", size=9)
        r += 1
    blast = r - 1
    r += 1
    r_fpd = row("PITCH RATIO", "P/D", f"=(B{blast}+C{blast})/2", "–",
                "Converged by the bisection above (KT(J, P/D) = KT,req)", "0.00000", name="FIN_PD", bold=True, isres=True)
    r_fp = row("Pitch", "P", "=FIN_PD*D_PROP", "m", "P = (P/D)·D", "0.000", name="FIN_PITCH", bold=True)
    r_fkt = row("Thrust coefficient at the design point", "KT",
                "=SUMPRODUCT(KT_C,J_FIN^KT_S,FIN_PD^KT_T,AE_PROP^KT_U,Z_BL^KT_V)", "–",
                "B-series polynomial evaluated at the converged P/D", "0.00000", name="FIN_KT")
    r_fkq = row("Torque coefficient at the design point", "KQ",
                "=SUMPRODUCT(KQ_C,J_FIN^KQ_S,FIN_PD^KQ_T,AE_PROP^KQ_U,Z_BL^KQ_V)", "–",
                "B-series polynomial evaluated at the converged P/D", "0.00000", name="FIN_KQ")
    r_fq = row("Torque", "Q", "=FIN_KQ*RHO_W*(FIN_N/60)^2*D_PROP^5", "N·m", "Q = KQ·ρ·n²·D⁵", "#,##0",
               name="Q_FIN")
    r_feo = row("OPEN-WATER EFFICIENCY", "ηO", "=J_FIN*FIN_KT/(2*PI()*FIN_KQ)", "–", "ηO = J·KT/(2π·KQ)", "0.0000",
                name="FIN_ETAO", bold=True, isres=True)
    r_fpd = row("DELIVERED POWER", "PD", "=2*PI()*(FIN_N/60)*Q_FIN/ETA_R_L/1000", "kW", "PD = 2π·n·Q/ηR", "#,##0.0",
                name="FIN_PD_KW", bold=True, isres=True)
    r_fps = row("Shaft power", "PS", "=FIN_PD_KW/ETA_S", "kW", "PS = PD/ηS", "#,##0.0", name="FIN_PS")
    r_fpb = row("Brake power at service speed", "PB", "=FIN_PS/ETA_G", "kW", "PB = PS/ηG", "#,##0.0", name="FIN_PB")
    r_fmr = row("Required engine MCR", "PMCR", "=FIN_PB/(1-EM_/100)", "kW", "PMCR = PB/(1 − engine margin)", "#,##0.0",
                name="FIN_PMCR")
    kt_lo = "SUMPRODUCT(KT_C,J_FIN^KT_S,0.5^KT_T,AE_PROP^KT_U,Z_BL^KT_V)"
    kt_hi = "SUMPRODUCT(KT_C,J_FIN^KT_S,1.4^KT_T,AE_PROP^KT_U,Z_BL^KT_V)"
    eta_d = ('=IF(AND(%s<=T_DESIGN/(RHO_W*(FIN_N/60)^2*D_PROP^4),T_DESIGN/(RHO_W*(FIN_N/60)^2*D_PROP^4)<=%s),'
             'PE_L*(1+SM_/100)/FIN_PD_KW,"–")' % (kt_lo, kt_hi))
    r_fd = row("TOTAL PROPULSIVE EFFICIENCY", "ηD", eta_d, "–",
               "ηD = PE(1+SM)/PD = ηH·ηO·ηR   (blank when the thrust identity has no solution)", "0.0000",
               name="FIN_ETAD", bold=True, isres=True)
    r_ftip = row("Blade tip speed", "Vtip", "=PI()*(FIN_N/60)*D_PROP", "m/s",
                 "Keep below ≈45 m/s to limit erosion, noise and vibration", "0.00")
    r += 1

    # ---- checks
    section(ws, r, "F.  DESIGN CHECKS", ncols=14); r += 1
    thead(ws, r, [(1, "Check"), (2, "Limit"), (3, "Value"), (4, "Unit"), (5, "Verdict")], height=20)
    r += 1
    checks = [
        ("Pitch ratio inside the Wageningen B-series range", "0.50 – 1.40", "=FIN_PD", "–",
         '=IF(AND(FIN_PD>=0.5,FIN_PD<=1.4),"PASS","REVIEW")'),
        ("Blade-area ratio inside the series range", "0.30 – 1.05", "=AE_PROP", "–",
         '=IF(AND(AE_PROP>=0.3,AE_PROP<=1.05),"PASS","REVIEW")'),
        ("Blade area satisfies Keller (cavitation)", "≥ Keller", "=AE_PROP-AE_KELLER", "–",
         '=IF(AE_PROP>=AE_KELLER,"PASS","REVIEW")'),
        ("Propeller fully immersed (h/D)", "≥ 1.00", "=H_SHAFT/D_PROP", "–",
         '=IF(H_SHAFT/D_PROP>=1,"PASS","REVIEW")'),
        ("Blade tip speed", "≤ 45 m/s", "=PI()*(FIN_N/60)*D_PROP", "m/s",
         '=IF(PI()*(FIN_N/60)*D_PROP<=45,"PASS","REVIEW")'),
        ("Thrust loading τc = 8·KT/(π·J²)", "τc ≤ 0.28·σ", "=8*FIN_KT/(PI()*J_FIN^2)", "–",
         '=IF(8*FIN_KT/(PI()*J_FIN^2)<=0.28*(P0_-PV_)/(0.5*RHO_W*VA_L^2),"PASS","REVIEW")'),
        ("Cavitation number σ = (p0 − pv)/(½ρVA²)", "> 1.0", "=(P0_-PV_)/(0.5*RHO_W*VA_L^2)", "–",
         '=IF((P0_-PV_)/(0.5*RHO_W*VA_L^2)>1,"PASS","REVIEW")'),
        ("Advance coefficient J", "0.10 – 1.20", "=J_FIN", "–",
         '=IF(AND(J_FIN>=0.1,J_FIN<=1.2),"PASS","REVIEW")'),
        ("Keller check repeated in ballast (reduced immersion)", "≥ Keller",
         "=AE_PROP-(1.3+0.3*Z_BL)*THRUST_B/((101325+RHO_W*G_*(T_BAL-TIP_CLR-D_PROP/2)-PV_)*D_PROP^2)", "–",
         '=IF(AE_PROP>=(1.3+0.3*Z_BL)*THRUST_B/((101325+RHO_W*G_*(T_BAL-TIP_CLR-D_PROP/2)-PV_)*D_PROP^2),"PASS","REVIEW")'),
    ]
    for lab, lim, f, unit, verdict in checks:
        label(ws, r, 1, lab); value(ws, r, 2, lim, fmt="@", align="center", size=9)
        calc(ws, r, 3, f, fmt="0.000")
        value(ws, r, 4, unit, fmt="@", align="center")
        calc(ws, r, 5, verdict, fmt="@", bold=True)
        ws.cell(row=r, column=5).alignment = Alignment(horizontal="center")
        ws.conditional_formatting.add(f"E{r}", CellIsRule(operator="equal", formula=['"PASS"'],
                                      fill=fill(OK_FILL), font=Font(name=FONT, color=OK_FONT, bold=True)))
        ws.conditional_formatting.add(f"E{r}", CellIsRule(operator="equal", formula=['"REVIEW"'],
                                      fill=fill(WARN_FILL), font=Font(name=FONT, color=WARN_FONT, bold=True)))
        r += 1

    # ---- notes
    r += 2
    section(ws, r, "G.  NOTES ON THIS SHEET", ncols=14); r += 1
    for txt in [
        "Section B solves the thrust identity KT(J, P/D) = KT,req for every shaft speed on a 75 rev/min grid, by "
        "bisection between P/D = 0.50 and P/D = 1.40 (the validity limits of the Wageningen B-series). Section C shows "
        "every bisection step in full, so the solution can be audited by hand.",
        "A row whose status is not OK cannot develop the required thrust at that shaft speed: the pitch ratio would have "
        "to leave the 0.50–1.40 band. Those rows are extrapolations, their PD is printed for the shape of the curve only, "
        "and they are excluded from the optimum search (column N).",
        "The optimum of section D maximises overall efficiency at the fixed diameter. It is a reference point: the "
        "propeller that is actually built is the one of section E, solved at the shaft speed that the selected engine and "
        "gear ratio can deliver.",
        "Keller's criterion fixes the minimum blade area against cavitation, using the static pressure at the shaft "
        "depth and the vapour pressure of sea water at the site temperature. The blade area is never allowed below the "
        "value entered on sheet 1.",
        "The thrust-loading check uses the Burrill diagram: with τc = 8·KT/(π·J²) and σ = (p0 − pv)/(½·ρ·VA²), the "
        "5 % back-cavitation line is closely τc = 0.28·σ over the range that marine propellers occupy. A point below "
        "that line means the blade area of this design keeps back cavitation under about 5 % of the blade area.",
        "Wageningen B-series accuracy: about ±2 % on KT and KQ inside the validity box, against about ±5 % for the "
        "resistance itself. That, not the polynomial, is the accuracy limit of the whole calculation.",
    ]:
        note(ws, r, 1, "•  " + txt, size=9, span=14)
        ws.row_dimensions[r].height = 26
        r += 1

    # ---- charts
    ch = ScatterChart()
    ch.title = "Delivered power against shaft speed"
    ch.style = 2
    ch.x_axis.title = "Shaft speed  [rpm]"
    ch.y_axis.title = "PD  [kW]"
    ch.height = 8.5; ch.width = 13
    ch.x_axis.majorGridlines = None
    xref = Reference(ws, min_col=1, min_row=sf, max_row=sl)
    s1 = Series(Reference(ws, min_col=10, min_row=sf, max_row=sl), xref, title="PD [kW]")
    s1.marker = Marker(symbol="circle", size=5)
    ch.series.append(s1)
    ws.add_chart(ch, "A%d" % (r + 2))

    ch2 = ScatterChart()
    ch2.title = "Open-water efficiency against shaft speed"
    ch2.style = 2
    ch2.x_axis.title = "Shaft speed  [rpm]"
    ch2.y_axis.title = "ηO"
    ch2.height = 8.5; ch2.width = 13
    ch2.x_axis.majorGridlines = None
    s2 = Series(Reference(ws, min_col=8, min_row=sf, max_row=sl), xref, title="ηO")
    s2.marker = Marker(symbol="diamond", size=4)
    ch2.series.append(s2)
    ws.add_chart(ch2, "H%d" % (r + 2))

    ws.freeze_panes = "A4"
    return ws
