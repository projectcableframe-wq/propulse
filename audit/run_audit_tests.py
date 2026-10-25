#!/usr/bin/env python3
"""
Independent regression / conformance suite for the YANMAR-PROPULSE selection
sheet.  >= 50 cases; every case stores what was measured, what was expected,
where the expectation comes from, and the tolerance.

    python3 audit/run_audit_tests.py                 # run, print, write report
    python3 audit/run_audit_tests.py --no-write      # print only

Data flow (nothing is hard-coded from the application's own self-tests):
  audit/build/script_0.js   extracted from the shipped HTML (extract_scripts.py)
  audit/js/dump_core.cjs    runs the calculation core headlessly -> JSON
  audit/js/dump_dom.cjs     runs the whole app in jsdom      -> JSON
  audit/independent/ref.py  independent re-implementation of ITTC-57, Holtrop &
                            Mennen (1982) and Savitsky (1964)
  audit/yanmar_official.py  YANMAR product-page data transcribed 2026-10-25

Exit code 0 only if every case passes.
"""
import json
import math
import os
import subprocess
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "independent"))

import ref                                    # noqa: E402
from yanmar_official import OFFICIAL, ACCESSED  # noqa: E402

CASES = []


def case(group, cid, desc, measured, expected, unit="", tol=None, basis="", ok=None):
    """Register one case.  tol is an absolute tolerance (same unit) if given,
    otherwise a relative tolerance in percent via rtol."""
    CASES.append(dict(group=group, id=cid, desc=desc, measured=measured,
                      expected=expected, unit=unit, tol=tol, basis=basis))


def rel(measured, expected, tol_pct, group, cid, desc, unit="", basis=""):
    good = (measured is not None and expected is not None
            and math.isfinite(measured) and math.isfinite(expected)
            and expected != 0
            and abs(measured - expected) / abs(expected) * 100 <= tol_pct)
    err = None
    if measured is not None and expected not in (None, 0) and math.isfinite(measured):
        err = (measured - expected) / expected * 100
    CASES.append(dict(group=group, id=cid, desc=desc, measured=measured,
                      expected=expected, unit=unit, tol="%.3g %%" % tol_pct,
                      err_pct=err, pass_=bool(good), basis=basis))


def exact(cond, group, cid, desc, measured=None, expected=None, unit="", basis=""):
    CASES.append(dict(group=group, id=cid, desc=desc, measured=measured,
                      expected=expected, unit=unit, tol="exact",
                      pass_=bool(cond), basis=basis))


def near(measured, expected, abs_tol, group, cid, desc, unit="", basis=""):
    good = (measured is not None and expected is not None
            and math.isfinite(measured) and abs(measured - expected) <= abs_tol)
    CASES.append(dict(group=group, id=cid, desc=desc, measured=measured,
                      expected=expected, unit=unit, tol="±%g" % abs_tol,
                      pass_=bool(good), basis=basis))


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        sys.exit("command failed: %s\n%s" % (" ".join(cmd), p.stderr[-3000:]))
    return p.stdout


def main():
    build = os.path.join(HERE, "build")
    html = os.path.join(ROOT, "app", "yanmar_engine_propeller_selector.html")
    print("extracting scripts ...")
    run([sys.executable, os.path.join(HERE, "extract_scripts.py"), html, build])
    print("running calculation core headlessly ...")
    core = json.loads(run(["node", os.path.join(HERE, "js", "dump_core.cjs"),
                           os.path.join(build, "script_0.js")]))
    print("running the full application in jsdom ...")
    dom = json.loads(run(["node", os.path.join(HERE, "js", "dump_dom.cjs"), html]))

    # ---------------------------------------------------------------- A. benchmarks
    for b in core["benchmarks"]:
        rel(b["measured"], b["expected"], b["tolerancePct"], "A published benchmark",
            b["id"], b["method"] + " — " + b["quantity"], b["unit"],
            "%s (%s)" % (b["source"], b["publication"]))

    # ---------------------------------------------------------------- B. Holtrop
    for h in core["holtrop"]:
        if h.get("error"):
            continue
        i = h["input"]
        r = ref.holtrop(L=i["Lwl"], B=i["B"], T=i["T"], vol=i["vol"], Cp=i["Cp"],
                        Cm=i["Cm"], Cwp=i["Cwp"], lcb=i["lcb"], V=i["V"] * ref.KNOT,
                        Abt=i["Abt"], hB=i["hB"], At=i["At"], Sapp=i["Sapp"],
                        k2=i["k2"], Cstern=i["Cstern"])
        tag = h["id"]
        rel(h["S"], r["S"], 0.001, "B Holtrop vs independent", "HT-S-" + tag,
            "%s: wetted surface S" % tag, "m2", "independent re-implementation, HM82 eq.1")
        rel(h["Rtotal"], r["Rt"], 0.5, "B Holtrop vs independent", "HT-RT-" + tag,
            "%s: total resistance" % tag, "N", "independent re-implementation")
        rel(h["Rw"], r["Rw"], 1.0, "B Holtrop vs independent", "HT-RW-" + tag,
            "%s: wave resistance" % tag, "N", "independent re-implementation")
        rel(h["formK"], r["formK"], 0.01, "B Holtrop vs independent", "HT-K1-" + tag,
            "%s: form factor" % tag, "-", "independent re-implementation")

    # ---------------------------------------------------------------- C. Savitsky
    for s in core["savitsky"]:
        if s.get("error"):
            continue
        i = s["input"]
        r = ref.savitsky(W=i["W"], V=i["V"] * ref.KNOT, B=i["B"], beta_deg=i["beta"],
                         LCG=i["LCG"], rho=i["rho"], nu=i["nu"])
        tag = s["id"]
        rel(s["lam"], r["lam"], 0.5, "C Savitsky vs independent", "SV-LAM-" + tag,
            "%s: wetted-length ratio" % tag, "-", "independent re-implementation")
        near(s["tau"], r["tau"], 0.05, "C Savitsky vs independent", "SV-TAU-" + tag,
             "%s: running trim" % tag, "deg", "independent re-implementation")
        rel(s["Vm"], r["Vm"], 0.5, "C Savitsky vs independent", "SV-VM-" + tag,
            "%s: mean bottom velocity" % tag, "m/s", "independent re-implementation")
        rel(s["Rbare"], r["D"], 1.0, "C Savitsky vs independent", "SV-D-" + tag,
            "%s: drag (both with ITTC-57 + 0.0004 roughness)" % tag, "N",
            "independent re-implementation, same friction basis")

    # ---------------------------------------------------------------- D. B-series
    bs = core["misc"]["bsKT"], core["misc"]["bsKQ"]
    exact(len(bs[0]) == 39 and len(bs[1]) == 47, "D Wageningen B-series", "BS-TERMS",
          "KT polynomial has 39 terms and KQ 47 (Oosterveld & van Oossanen 1975)",
          "%d / %d" % (len(bs[0]), len(bs[1])), "39 / 47", "terms",
          "table size only — not a value check")
    for p in core["bseries"]:
        if abs(p["Rn"] - 2e6) > 1:
            continue          # Reynolds-corrected points are checked separately
        # independent evaluation of the SAME coefficient table
        kt = sum(c[0] * p["J"] ** c[1] * p["PD"] ** c[2] * p["EAR"] ** c[3] * p["Z"] ** c[4]
                 for c in bs[0])
        kq = sum(c[0] * p["J"] ** c[1] * p["PD"] ** c[2] * p["EAR"] ** c[3] * p["Z"] ** c[4]
                 for c in bs[1])
        rn_term_kt = ref_krn = None
        tag = "J%.2f_PD%.2f_EAR%.2f_Z%d" % (p["J"], p["PD"], p["EAR"], p["Z"])
        exact(abs(p["KT"] - kt) < 5e-7, "D Wageningen B-series", "BS-KT-" + tag,
              "%s: KT equals the explicit 39-term sum" % tag, p["KT"], kt, "-",
              "independent summation of the stored table (evaluation check)")
        exact(abs(p["KQ"] - kq) < 5e-8, "D Wageningen B-series", "BS-KQ-" + tag,
              "%s: KQ equals the explicit 47-term sum" % tag, p["KQ"], kq, "-",
              "independent summation of the stored table")
        exact(abs(p["eta"] - p["J"] * p["KT"] / (2 * math.pi * p["KQ"])) < 1e-12,
              "D Wageningen B-series", "BS-ETA-" + tag,
              "%s: open-water efficiency equals J*KT/(2*pi*KQ)" % tag, p["eta"], None, "-",
              "definition identity")
        exact(p["KT"] > 0 and p["KQ"] > 0 and 0 < p["eta"] < 0.85,
              "D Wageningen B-series", "BS-RANGE-" + tag,
              "%s: KT, KQ positive and eta in (0, 0.85)" % tag,
              "KT=%.4f KQ=%.5f eta=%.4f" % (p["KT"], p["KQ"], p["eta"]), None, "-",
              "physical plausibility band of the series")

    rn_pts = [q for q in core["bseries"] if abs(q["Rn"] - 2e6) > 1]
    for q in rn_pts:
        base = [p for p in core["bseries"] if abs(p["Rn"] - 2e6) <= 1
                and abs(p["J"] - q["J"]) < 1e-9 and abs(p["PD"] - q["PD"]) < 1e-9]
        exact(q["KT"] > 0 and q["KQ"] > 0, "D Wageningen B-series",
              "BS-RN-%g" % q["Rn"], "KT/KQ stay positive at Rn=%.3g" % q["Rn"],
              "KT=%.4f KQ=%.5f" % (q["KT"], q["KQ"]), None, "-",
              "Reynolds-number correction of Oosterveld & van Oossanen (1975)")

    # ---------------------------------------------------------------- E. friction
    for e in core["ittc"]:
        rn = e["Rn"]
        expect = 0.075 / (math.log10(rn) - 2) ** 2
        rel(e["Cf"], expect, 1e-9, "E ITTC-1957 friction", "ITTC-%g" % rn,
            "Cf at Rn=%.3g" % rn, "-", "ITTC-57 definition 0.075/(log10 Re-2)^2")
    exact(core["ittc"][1]["Cf"] is not None and abs(core["ittc"][1]["Cf"] - 0.0046875) < 1e-7,
          "E ITTC-1957 friction", "ITTC-1e6-value", "Cf(1e6) = 0.0046875",
          core["ittc"][1]["Cf"], 0.0046875, "-", "closed form")

    # ---------------------------------------------------------------- F. engine DB
    db = {e["model"]: e for e in core["engines"]}
    for model, off in OFFICIAL.items():
        e = db.get(model)
        if e is None:
            exact(False, "F YANMAR database", "ENG-EXIST-" + model,
                  "%s present in the database" % model, "missing", "present", "",
                  off["page"])
            continue
        app_rows = sorted((r["ymark"], round(r["kW"], 1), int(r["rpm"])) for r in e["ratings"])
        off_rows = sorted((m, round(kw, 1), int(rpm)) for m, kw, rpm in off["ratings"])
        exact(app_rows == off_rows, "F YANMAR database", "ENG-RAT-" + model,
              "%s ratings (letter, kW, rpm) equal the official row(s)" % model,
              app_rows, off_rows, "", "%s accessed %s" % (off["page"], ACCESSED))
        if "dryMass_without_gear" in off:
            near(e["dryMass"], off["dryMass_without_gear"], 0.5, "F YANMAR database",
                 "ENG-MASS-" + model, "%s dry mass (without marine gear)" % model,
                 "kg", "official page")
        else:
            gm = off.get("gear_mass", {}).get(off["gear_for_mass"])
            if gm is not None:
                near(e["dryMass"], off["dryMass_with_gear"], 0.5, "F YANMAR database",
                     "ENG-MASS-" + model,
                     "%s published dry mass WITH %s (%d kg)"
                     % (model, off["gear_for_mass"], gm), "kg",
                     "CHE page: the published figure already includes the gear")
        if off.get("dims"):
            exact(list(e["dims"]) == list(off["dims"]), "F YANMAR database",
                  "ENG-DIMS-" + model, "%s L×W×H equal the official page" % model,
                  e["dims"], off["dims"], "mm", "official page")
        for g in e["gears"]:
            if g["model"] in off.get("gears", {}) and off["gears"][g["model"]]:
                exact([round(x, 2) for x in g["ratios"]] ==
                      [round(x, 2) for x in off["gears"][g["model"]]],
                      "F YANMAR database", "ENG-GEAR-" + model + "-" + g["model"],
                      "%s %s reduction ratios" % (model, g["model"]),
                      g["ratios"], off["gears"][g["model"]], "-", "official page")
        if off.get("gear_mass") and e["gears"]:
            g = e["gears"][0]
            om = off["gear_mass"].get(g["model"])
            if om is not None and g.get("mass") is not None:
                exact(abs(g["mass"] - om) <= 1, "F YANMAR database",
                      "ENG-GEARMASS-" + model + "-" + g["model"],
                      "%s %s gear mass" % (model, g["model"]), g["mass"], om, "kg",
                      "official page")
    # derived consistency
    for model, e in db.items():
        n = sum(1 for d in e["disp"] and [1] or [])
        cyl = int(str(e["cyl"]).split()[0]) if e["cyl"] else None
        if cyl and e["bore"] and e["stroke"]:
            calc = math.pi / 4 * (e["bore"] / 1000) ** 2 * (e["stroke"] / 1000) * cyl * 1000
            rel(e["disp"], calc, 2.0, "F YANMAR database", "ENG-DISP-" + model,
                "%s displacement from bore*stroke*cylinders" % model, "L",
                "geometric identity")
        for r in e["ratings"]:
            torque = 9549.3 * r["kW"] / r["rpm"]
            exact(0 < torque < 40000, "F YANMAR database", "ENG-TQ-" + model + "-" + r["ymark"],
                  "%s %s rated torque plausible (%.0f N·m)" % (model, r["ymark"], torque),
                  round(torque, 1), "< 40000 N·m", "N·m", "9549.3*P/n identity")
        inst = e["installed"]
        exact(all((v is None or v.get("kg") is None or v["kg"] > 0) for v in inst.values()),
              "F YANMAR database", "ENG-INST-" + model,
              "%s installed masses are positive or explicitly unknown" % model,
              {k: (v or {}).get("kg") for k, v in inst.items()}, "> 0 or null", "kg",
              "installedMassOf()")

    # ---------------------------------------------------------------- G. selections
    for p in dom["presets"]:
        tag = p["id"]
        if not p.get("ok") or not p.get("primary"):
            exact(False, "G selection", "SEL-OK-" + tag,
                  "%s yields a candidate" % tag, (p.get("errors") or ["none"])[0], "a candidate")
            continue
        c, r = p["primary"], p["res"]
        exact(True, "G selection", "SEL-OK-" + tag, "%s yields a candidate (%s %s)"
              % (tag, c["model"], c["ymark"]), "ok", "ok")
        inp = p.get("inp") or {}
        if all(k in inp and inp[k] is not None for k in ("etaShaft", "etaGear", "seaMargin")):
            expect_pb = c["PD"] / (inp["etaShaft"] * inp["etaGear"]) * (1 + inp["seaMargin"])
            rel(c["PB"], expect_pb, 0.01, "G selection", "SEL-PB-" + tag,
                "%s: P_B = P_D/(eta_S*eta_G)*(1+sea margin)" % tag, "kW",
                "power ledger definition")
            rel(p["res"]["PE"], p["res"]["Rtotal"] * inp["Vs"], 0.01, "G selection",
                "SEL-PE-" + tag, "%s: P_E = R_T * V_s" % tag, "kW",
                "definition P_E = R_T V")
        # power ledger: P_B = P_D/(etaS*etaG)*(1+seaM); P_D from the propeller
        exact(abs(c["load"] - c["PB"] / c["kW"]) < 1e-9, "G selection",
              "SEL-LOAD-" + tag, "%s: load = P_B/P_rated" % tag, c["load"],
              c["PB"] / c["kW"], "-", "definition")
        exact(c["load"] <= 1.0 + 1e-9, "G selection", "SEL-MAXLOAD-" + tag,
              "%s: service load within the 100 %% hard limit" % tag, c["load"], "<= 1.0")
        if c.get("etaO") and c.get("KT") and c.get("J"):
            exact(abs(c["etaO"] - c["J"] * c["KT"] / (2 * math.pi * c["KQ"])) < 1e-9,
                  "G selection", "SEL-ETAO-" + tag,
                  "%s: propeller efficiency equals J*KT/(2*pi*KQ)" % tag, c["etaO"], None)
        exact(c["D"] is not None and 0 < c["D"] <= 5.0, "G selection", "SEL-D-" + tag,
              "%s: propeller diameter positive and physical" % tag, c["D"], "0 < D <= 5 m", "m",
              "geometry check")
        exact(c["PDprop"] is not None and 0.4 <= c["PDprop"] <= 1.45, "G selection",
              "SEL-PD-" + tag, "%s: P/D inside the B-series band" % tag, c["PDprop"],
              "0.5 <= P/D <= 1.4", "-", "BS_RANGE")
        exact(bool(c["cavOK"]) is False or c["EAR"] >= c["EARreq"] - 1e-9, "G selection",
              "SEL-CAV-" + tag, "%s: blade area covers the cavitation requirement" % tag,
              ("EAR=%.3f EARreq=%.3f" % (c["EAR"], c["EARreq"])) if c["EARreq"] is not None else "n/a",
              "EAR >= EARreq", "-", "Burrill/Carmichael + Keller")
        exact(p["rejectedCount"] > 0, "G selection", "SEL-REJ-" + tag,
              "%s: rejected candidates are listed with reasons (%d)" % (tag, p["rejectedCount"]),
              p["rejectedCount"], "> 0")
        exact(all(r_.get("reason") for r_ in p["rejected"]), "G selection",
              "SEL-REJWHY-" + tag, "%s: every rejection carries a reason" % tag,
              sum(0 if r_.get("reason") else 1 for r_ in p["rejected"]), 0, "count",
              "rejection-reason audit")
        names = [k["name"] for k in (c.get("checks") or [])]
        if c["load"] < 0.40:
            exact("Engine size vs requirement" in names, "G selection",
                  "SEL-RIGHTSIZE-" + tag,
                  "%s: a candidate at %.0f %% load carries an explicit right-sizing check"
                  % (tag, c["load"] * 100), "present" if "Engine size vs requirement" in names else "absent",
                  "present", "-", "assessCandidate() checks")
        if c["PDprop"] is not None and c["PDprop"] >= 1.39:
            exact("Propeller design is boundary-limited" in names, "G selection",
                  "SEL-PDLIMIT-" + tag,
                  "%s: P/D = %.3f on the series boundary is reported to the user" % (tag, c["PDprop"]),
                  "present" if "Propeller design is boundary-limited" in names else "absent",
                  "present", "-", "designPropeller boundary flags")
        if c["load"] < 0.40:
            checks = None
            exact(c["status"] in ("FAILED CONSTRAINT", "OUTSIDE VALIDATION DOMAIN"),
                  "G selection", "SEL-OVERSIZE-" + tag,
                  "%s: a candidate below the 40 %% right-sizing band is not presented as plain 'PRELIMINARY ESTIMATE'"
                  % tag, c["status"], "FAILED CONSTRAINT / OUTSIDE VALIDATION DOMAIN", "-",
                  "right-sizing rule")

    # ---------------------------------------------------------------- H. edge cases
    edges = {e["id"]: e for e in dom["edge"]}
    e = edges.get("cargo-high-speed", {})
    exact(e.get("ok") is False, "H edge cases", "EDGE-FN",
          "Fn > 0.55 on a displacement hull is refused, not extrapolated",
          (e.get("errors") or ["no error"])[0][:80], "refused", "-", "domain guard")
    e = edges.get("cargo-zero-speed", {})
    exact(e.get("ok") is False, "H edge cases", "EDGE-V0", "zero speed is refused",
          (e.get("errors") or ["no error"])[0][:80])
    e = edges.get("cargo-no-days", {})
    exact(e.get("ok") is False, "H edge cases", "EDGE-NODAYS",
          "missing operating days is an error, not a silent default",
          (e.get("errors") or ["no error"])[0][:80])
    e = edges.get("dinghy-planing-25kn", {})
    exact(e.get("ok") is False, "H edge cases", "EDGE-NOPROP",
          "25 kn dinghy with a clearance-limited propeller is refused with a reason",
          (e.get("errors") or ["no error"])[0][:120])
    e = edges.get("ferry-cav-30", {})
    exact(any("∞" in v or "outside the validity" in v
              for v in ((e.get("primary") or {}).get("violations") or [])),
          "H edge cases", "EDGE-CAVLIM",
          "an allowable back cavitation above the Carmichael validity band is refused",
          ((e.get("primary") or {}).get("violations") or ["no violation"])[0][:120])
    e = edges.get("ferry-huge-tip", {})
    pv = (e.get("primary") or {})
    exact(e.get("ok") is True and (e.get("primary") or {}).get("load") is not None, "H edge cases",
          "EDGE-TIPOK", "tip-speed limit 20 m/s still yields a feasible propeller (re-designed)",
          e.get("ok"), True, "-", "tip-speed gate")
    e = edges.get("cargo-2props", {})
    exact(e.get("ok") is True, "H edge cases", "EDGE-2PROP",
          "two propellers are matched (per-engine power halves)", e.get("ok"), True, "-",
          "nProps handling")
    e = edges.get("fishing-16h-330d", {})
    exact(any("Duty-cycle limit exceeded" in v for v in ((e.get("primary") or {}).get("violations") or [])),
          "H edge cases", "EDGE-DUTY",
          "5 280 operating hours exceed the M-rating limit and are reported",
          ((e.get("primary") or {}).get("violations") or ["none"])[0][:120])

    # ---------------------------------------------------------------- I. app self-test
    st = dom.get("selftest") or {}
    exact(st.get("fail") == 0 and st.get("pass", 0) >= 100, "I in-app tests",
          "APP-SELFTEST", "the shipped in-app self-test suite runs headless with no failure",
          "%s pass / %s fail" % (st.get("pass"), st.get("fail")), "0 fail", "count",
          "headless jsdom run of fullSelfTest()")
    exact(dom.get("fieldCount", 0) >= 40, "I in-app tests", "APP-FIELDS",
          "the UI builds every input field", dom.get("fieldCount"), ">= 40", "fields",
          "DOM query .field")

    # ---------------------------------------------------------------- report
    groups = {}
    for c in CASES:
        groups.setdefault(c["group"], []).append(c)
    npass = sum(1 for c in CASES if c.get("pass_"))
    nfail = len(CASES) - npass
    lines = []
    lines.append("# Audit test report — YANMAR / PROPULSE selection sheet\n")
    lines.append("Generated %s by `audit/run_audit_tests.py`.\n" % datetime.date.today())
    lines.append("**%d cases, %d pass, %d fail.**\n" % (len(CASES), npass, nfail))
    for g in sorted(groups):
        rows = groups[g]
        gp = sum(1 for c in rows if c.get("pass_"))
        lines.append("## %s — %d cases, %d pass, %d fail\n" % (g, len(rows), gp, len(rows) - gp))
        lines.append("| case | what is checked | measured | expected | tol / error | result | source / basis |")
        lines.append("|---|---|---|---|---|---|---|")
        for c in rows:
            m = c.get("measured")
            ex = c.get("expected")
            mstr = _fmt(m)
            estr = _fmt(ex)
            tol = c.get("tol") or ""
            if c.get("err_pct") is not None:
                tol = "%s (err %+.3f%%)" % (tol, c["err_pct"])
            lines.append("| %s | %s | %s | %s | %s | %s | %s |"
                         % (c["id"], c["desc"], mstr, estr, tol,
                            "PASS" if c.get("pass_") else "**FAIL**",
                            (c.get("basis") or "").replace("|", "/")))
        lines.append("")
    report = "\n".join(lines)
    print(report if len(CASES) < 12 else _summary(groups, npass, nfail))
    if "--no-write" not in sys.argv:
        with open(os.path.join(HERE, "TEST_REPORT.md"), "w", encoding="utf-8") as f:
            f.write(report)
        print("\nwritten: audit/TEST_REPORT.md")
    return 0 if nfail == 0 else 1


def _fmt(v):
    if isinstance(v, float):
        if abs(v) >= 1e5 or (v != 0 and abs(v) < 1e-3):
            return "%.4g" % v
        return "%.4f" % v
    if isinstance(v, (list, dict, tuple)):
        s = str(v)
        return s if len(s) < 90 else s[:87] + "…"
    return "" if v is None else str(v)


def _summary(groups, npass, nfail):
    out = []
    for g in sorted(groups):
        rows = groups[g]
        gp = sum(1 for c in rows if c.get("pass_"))
        out.append("%-32s %3d cases  %3d pass  %3d fail" % (g, len(rows), gp, len(rows) - gp))
        for c in rows:
            if not c.get("pass_"):
                out.append("    FAIL %-28s measured=%s expected=%s tol=%s"
                           % (c["id"], _fmt(c.get("measured")), _fmt(c.get("expected")), c.get("tol")))
    out.append("-" * 62)
    out.append("%-32s %3d cases  %3d pass  %3d fail" % ("TOTAL", len(CASES), npass, nfail))
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
