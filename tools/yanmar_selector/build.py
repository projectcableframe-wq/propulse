"""Build the Propulse Yanmar propeller + engine selection workbook.

    python build.py [output.xlsx]

Every sheet is produced by its own module; this file only wires them together and
registers the workbook-wide defined names.
"""
import re
import sys
import datetime

from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName

import s_input
import s_res
import s_prop
import s_propeller
import s_engines
import s_summary
import s_dbyanmar
import s_dbb
import s_eq
import s_verify


class Namer:
    """Collects sheet-local references and turns them into workbook defined names."""

    def __init__(self, wb):
        self.wb = wb
        self.sheet = None
        self.log = []

    def add(self, name, ref):
        if "!" in ref:
            text = ref
        else:
            m = re.match(r"^\$?([A-Z]+)\$?(\d+)$", ref.replace("$", ""))
            if not m:
                raise ValueError("bad reference %r for name %s" % (ref, name))
            text = "'%s'!$%s$%s" % (self.sheet, m.group(1), m.group(2))
        if name in self.wb.defined_names:
            del self.wb.defined_names[name]
        self.wb.defined_names[name] = DefinedName(name, attr_text=text)
        self.log.append((name, text))
        return name


TAB_COLOURS = {
    "0 Summary": "0B2033",
    "1 Input": "C8A24A",
    "2 Resistance": "00787A",
    "3 Propulsion": "00787A",
    "4 Propeller": "00787A",
    "5 Engines": "00787A",
    "6 Yanmar data": "5B6B7B",
    "7 B-series": "5B6B7B",
    "8 Equations": "5B6B7B",
    "9 Verification": "1E6B33",
}


def autofit_rows(ws):
    """Give wrapped text the row height it needs (Excel does not do this on open)."""
    from openpyxl.utils import get_column_letter, range_boundaries

    def cw(col):
        dim = ws.column_dimensions.get(get_column_letter(col))
        return (dim.width if dim and dim.width else 8.43)

    spans = {}
    for rng in ws.merged_cells.ranges:
        c1, r1, c2, r2 = range_boundaries(str(rng))
        if r1 == r2:
            spans[(r1, c1)] = sum(cw(c) for c in range(c1, c2 + 1))

    for row in ws.iter_rows():
        need = 0.0
        for cell in row:
            if not isinstance(cell.value, str) or not cell.value:
                continue
            wrap = bool(cell.alignment and cell.alignment.wrap_text)
            if not wrap:
                continue
            width = spans.get((cell.row, cell.column), cw(cell.column))
            size = (cell.font.sz or 10) if cell.font else 10
            chars = max(4.0, width * (11.0 / float(size)))
            lines = -(-len(cell.value) // int(chars))
            need = max(need, lines * size * 1.32 + 3)
        if need:
            r = row[0].row
            cur = ws.row_dimensions[r].height or 0
            ws.row_dimensions[r].height = min(max(cur, need), 150)


def polish(wb):
    """Tab colours, print set-up and viewing defaults for every sheet."""
    for ws in wb.worksheets:
        autofit_rows(ws)
        ws.sheet_properties.tabColor = TAB_COLOURS.get(ws.title, "5B6B7B")
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_options.horizontalCentered = False
        ws.oddFooter.left.text = "Propulse - Yanmar engine and propeller selection"
        ws.oddFooter.left.size = 8
        ws.oddFooter.right.text = "&A   page &P of &N"
        ws.oddFooter.right.size = 8
        if ws.max_row > 40:
            ws.print_title_rows = "1:3"
        if ws.title not in ("0 Summary", "9 Verification"):
            ws.sheet_view.zoomScale = 90


def main(path):
    wb = Workbook()
    wb.remove(wb.active)
    wb.properties.title = "Propulse - Yanmar engine and propeller selection"
    wb.properties.subject = "Holtrop-Mennen 1982 resistance, Wageningen B-series propeller, ISO 3046-1 derated Yanmar engine"
    wb.properties.creator = "Propulse"
    wb.properties.description = ("Fully formula-driven design workbook. Resistance by Holtrop & Mennen (1982), "
                                 "propeller by the Wageningen B-series polynomials, engine selection on "
                                 "ISO 3046-1 site-corrected Yanmar ratings.")
    wb.properties.created = datetime.datetime(2026, 11, 10)

    nm = Namer(wb)
    builders = [
        ("0 Summary", s_summary),
        ("1 Input", s_input),
        ("2 Resistance", s_res),
        ("3 Propulsion", s_prop),
        ("4 Propeller", s_propeller),
        ("5 Engines", s_engines),
        ("6 Yanmar data", s_dbyanmar),
        ("7 B-series", s_dbb),
        ("8 Equations", s_eq),
        ("9 Verification", s_verify),
    ]
    for sheet_name, mod in builders:
        nm.sheet = sheet_name
        mod.build(wb, nm)
    s_eq.fill_names(wb)  # section B of sheet 8 lists the names of every sheet, so it runs last

    wb.calculation.fullCalcOnLoad = True
    polish(wb)
    wb.active = 0
    wb.save(path)
    print("wrote %s" % path)
    print("%d sheets, %d defined names" % (len(wb.sheetnames), len(nm.log)))
    for name, text in nm.log:
        print("   %-12s %s" % (name, text))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Propulse_Yanmar_propeller_design.xlsx")
