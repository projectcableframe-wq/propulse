"""Visual theme helpers for the workbook."""
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---- palette -------------------------------------------------------------
NAVY      = "0B2033"
NAVY_2    = "123A5A"
TEAL      = "00A6A6"
TEAL_DK   = "00787A"
TEAL_LT   = "E6F7F7"
GREY_HDR  = "E8EDF2"
GREY_LT   = "F4F7FA"
GREY_MID  = "C9D3DD"
WHITE     = "FFFFFF"
INPUT_FILL= "FFF6D9"
INPUT_BRD = "D9B44A"
OUT_FILL  = "E3F2FD"
OUT_BRD   = "4A90C2"
OK_FILL   = "D8F0DC"
OK_FONT   = "1E6B33"
WARN_FILL = "FDE2E2"
WARN_FONT = "9E1B1B"
NOTE_FONT = "5B6B7B"
GOLD      = "C8A24A"

FONT = "Calibri"
THIN = Side(style="thin", color=GREY_MID)
MED  = Side(style="medium", color=NAVY_2)


def fill(c):
    return PatternFill("solid", fgColor=c)


def title(ws, text, sub, ncols=12, height=30):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=text)
    c.font = Font(name=FONT, size=18, bold=True, color=WHITE)
    c.fill = fill(NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = height
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c2 = ws.cell(row=2, column=1, value=sub)
    c2.font = Font(name=FONT, size=10, italic=True, color=WHITE)
    c2.fill = fill(NAVY_2)
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 20
    for col in range(1, ncols + 1):
        ws.cell(row=1, column=col).fill = fill(NAVY)
        ws.cell(row=2, column=col).fill = fill(NAVY_2)


def section(ws, row, text, ncols=12, fillc=None):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name=FONT, size=11, bold=True, color=WHITE)
    c.fill = fill(fillc or TEAL_DK)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 22
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).fill = fill(fillc or TEAL_DK)


def thead(ws, row, cols, height=32, wrap=True):
    for i, (col, txt) in enumerate(cols):
        c = ws.cell(row=row, column=col, value=txt)
        c.font = Font(name=FONT, size=9, bold=True, color=WHITE)
        c.fill = fill(NAVY_2)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=wrap)
        c.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    ws.row_dimensions[row].height = height


def label(ws, row, col, text, bold=False, size=10, color=NAVY, indent=1):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(name=FONT, size=size, bold=bold, color=color)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=indent)
    return c


def value(ws, row, col, val, fmt="0.000", bold=False, size=10, align="right"):
    c = ws.cell(row=row, column=col, value=val)
    c.font = Font(name=FONT, size=size, bold=bold, color=NAVY)
    c.number_format = fmt
    c.alignment = Alignment(horizontal=align, vertical="center")
    return c


def inp(ws, row, col, val, fmt="0.000", name=None):
    c = ws.cell(row=row, column=col, value=val)
    c.font = Font(name=FONT, size=10, bold=False, color="1F2D3D")
    c.number_format = fmt
    c.fill = fill(INPUT_FILL)
    c.border = Border(left=Side(style="thin", color=INPUT_BRD),
                      right=Side(style="thin", color=INPUT_BRD),
                      top=Side(style="thin", color=INPUT_BRD),
                      bottom=Side(style="thin", color=INPUT_BRD))
    c.alignment = Alignment(horizontal="right", vertical="center")
    return c


def calc(ws, row, col, formula, fmt="0.000", bold=False, size=10, fillc=None):
    c = ws.cell(row=row, column=col, value=formula)
    c.font = Font(name=FONT, size=size, bold=bold, color=NAVY)
    c.number_format = fmt
    c.fill = fill(fillc or GREY_LT)
    c.alignment = Alignment(horizontal="right", vertical="center")
    c.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    return c


def result(ws, row, col, formula, fmt="0.000", bold=True, size=10):
    c = ws.cell(row=row, column=col, value=formula)
    c.font = Font(name=FONT, size=size, bold=bold, color=NAVY)
    c.number_format = fmt
    c.fill = fill(OUT_FILL)
    c.border = Border(left=Side(style="medium", color=OUT_BRD),
                      right=Side(style="medium", color=OUT_BRD),
                      top=Side(style="medium", color=OUT_BRD),
                      bottom=Side(style="medium", color=OUT_BRD))
    c.alignment = Alignment(horizontal="right", vertical="center")
    return c


def note(ws, row, col, text, size=9, italic=True, color=NOTE_FONT, span=1):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(name=FONT, size=size, italic=italic, color=color)
    c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    if span > 1:
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + span - 1)
    return c


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def band(ws, r1, r2, c1, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(row=r, column=c).fill = fill(color)
