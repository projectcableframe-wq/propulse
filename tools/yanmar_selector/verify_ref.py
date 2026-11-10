"""Independent Python re-implementation of the *exact* workbook chain.

The workbook (sheets 1-4) is derived from these formulas. This script re-computes
the same two reference vessels in double precision and writes refdata.py, which the
workbook's Verification sheet uses as an independent check of the Excel formulas.

Every definition here mirrors the sheet layout:
  sheet 2  resistance  (Holtrop-Mennen 1982)
  sheet 3  wake / thrust deduction / relative rotative efficiency
  sheet 4  Wageningen B-series propeller, bisection on P/D with the same bounds
"""
import math

RHO = 1025.0
NU = 1.139e-6
G = 9.81

KT_COEF = [
    (0.008804960, 0, 0, 0, 0), (0.014404300, 0, 0, 0, 1), (-0.000606848, 0, 0, 0, 2), (-0.012589400, 0, 0, 1, 1),
    (0.000690904, 0, 0, 1, 2), (-0.050721400, 0, 0, 2, 0), (0.166351000, 0, 1, 0, 0), (0.014348100, 0, 1, 0, 1),
    (0.158114000, 0, 2, 0, 0), (0.415437000, 0, 2, 1, 0), (-0.004107980, 0, 2, 2, 1), (-0.133698000, 0, 3, 0, 0),
    (-0.008417280, 0, 3, 0, 1), (-0.031779100, 0, 3, 1, 1), (0.004217490, 0, 3, 1, 2), (-0.001465640, 0, 3, 2, 2),
    (0.006384070, 0, 6, 0, 0),
    (-0.204554000, 1, 0, 0, 0), (-0.004981900, 1, 0, 0, 2), (0.010968900, 1, 0, 1, 1), (0.018604000, 1, 0, 2, 1),
    (0.060682600, 1, 1, 0, 1), (-0.481497000, 1, 1, 1, 0), (-0.001636520, 1, 2, 0, 2), (0.016842400, 1, 3, 0, 1),
    (-0.000328787, 1, 6, 0, 2), (0.010465000, 1, 6, 2, 0),
    (-0.053005400, 2, 0, 0, 1), (0.002598300, 2, 0, 0, 2), (-0.147581000, 2, 0, 1, 0), (0.085455900, 2, 0, 2, 0),
    (-0.001327180, 2, 6, 0, 0), (0.000116502, 2, 6, 0, 2), (-0.006482720, 2, 6, 2, 0),
    (-0.000560528, 3, 0, 0, 2), (0.168496000, 3, 0, 1, 0), (-0.050447500, 3, 0, 2, 0), (-0.001022960, 3, 3, 0, 1),
    (0.0000565229, 3, 6, 1, 2),
]
KQ_COEF = [
    (0.0037936800, 0, 0, 0, 0), (0.0158960000, 0, 0, 2, 0), (-0.0001843000, 0, 0, 2, 2), (0.0051369600, 0, 1, 0, 1),
    (-0.0408811000, 0, 1, 1, 0), (-0.0502782000, 0, 1, 2, 0), (0.0034477800, 0, 2, 0, 0), (0.1885610000, 0, 2, 1, 0),
    (-0.0269403000, 0, 2, 1, 1), (0.0015533400, 0, 2, 1, 2), (0.0126803000, 0, 2, 2, 1), (0.0161886000, 0, 3, 1, 0),
    (-0.0397722000, 0, 3, 2, 0), (-0.0004253990, 0, 3, 2, 2), (-0.0003139120, 0, 6, 0, 1), (-0.0014212100, 0, 6, 1, 1),
    (0.0003026830, 0, 6, 1, 2), (-0.0035002400, 0, 6, 2, 0), (0.0033426800, 0, 6, 2, 1), (-0.0004659000, 0, 6, 2, 2),
    (-0.0037087100, 1, 0, 0, 1), (0.0002695510, 1, 0, 1, 2), (0.0471729000, 1, 0, 2, 0), (-0.0038363700, 1, 0, 2, 1),
    (-0.0322410000, 1, 1, 0, 0), (0.0209449000, 1, 1, 0, 1), (-0.0018349100, 1, 1, 0, 2), (-0.1080090000, 1, 1, 1, 0),
    (0.0043838800, 1, 1, 1, 1), (0.0031809860, 1, 3, 1, 0), (0.0000554194, 1, 6, 2, 2),
    (0.0088652300, 2, 0, 0, 0), (-0.0072340800, 2, 0, 1, 1), (0.0008326500, 2, 0, 1, 2), (0.0047431900, 2, 1, 0, 1),
    (-0.0885381000, 2, 1, 1, 0), (0.0417122000, 2, 2, 2, 0), (-0.0031827800, 2, 3, 2, 1),
    (-0.0106854000, 3, 0, 0, 1), (0.0558082000, 3, 0, 1, 0), (0.0035985000, 3, 0, 1, 1), (0.0196283000, 3, 0, 2, 0),
    (-0.0300550000, 3, 1, 2, 0), (0.0001124510, 3, 2, 0, 2), (0.0011090300, 3, 3, 0, 1), (0.0000869243, 3, 3, 2, 2),
    (-0.0000297228, 3, 6, 0, 2),
]


def KT(J, pd, ae, z):
    return sum(C * J ** s * pd ** t * ae ** u * z ** v for C, s, t, u, v in KT_COEF)


def KQ(J, pd, ae, z):
    return sum(C * J ** s * pd ** t * ae ** u * z ** v for C, s, t, u, v in KQ_COEF)


def resistance(L, B, T, TF, vol, Cb, Cp, Cm, Cwp, lcb, ABT, hB, AT, Cstern, Sapp, k2, Vs, rho=RHO, nu=NU, g=G):
    d = {}
    Fn = Vs / math.sqrt(g * L)
    S = L * (2 * T + B) * math.sqrt(Cm) * (0.453 + 0.4425 * Cb - 0.2862 * Cm - 0.003467 * B / T + 0.3696 * Cwp) \
        + 2.38 * ABT / Cb
    Re = Vs * L / nu
    Cf = 0.075 / (math.log10(Re) - 2) ** 2
    LR = L * (1 - Cp + 0.06 * Cp * lcb / (4 * Cp - 1))
    c12 = (T / L) ** 0.2228446 if T / L >= 0.05 else 48.20 * (T / L - 0.02) ** 2.078 + 0.479948
    c13 = 1 + 0.003 * Cstern
    k1 = c13 * (0.93 + c12 * (B / LR) ** 0.92497 * (0.95 - Cp) ** -0.521448
                * (1 - Cp + 0.0225 * lcb) ** 0.6906)
    if B / L < 0.11:
        c7 = 0.229577 * (B / L) ** 0.33333333
    elif B / L < 0.25:
        c7 = B / L
    else:
        c7 = 0.5 - 0.0625 * L / B
    iE = 1 + 89 * math.exp(-(L / B) ** 0.80856 * (1 - Cwp) ** 0.30484 * (1 - Cp - 0.0225 * lcb) ** 0.6367
                           * (LR / B) ** 0.34574 * (100 * vol / L ** 3) ** 0.16302)
    c1 = 2223105 * c7 ** 3.78613 * (T / B) ** 1.07961 * (90 - iE) ** -1.37565
    c3 = 0.56 * ABT ** 1.5 / (B * T * (0.31 * math.sqrt(ABT) + TF - hB)) if ABT > 0 else 0.0
    c2 = math.exp(-1.89 * math.sqrt(c3)) if ABT > 0 else 1.0
    c5 = 1 - 0.8 * AT / (B * T * Cm)
    lam = 1.446 * Cp - 0.03 * L / B if L / B < 12 else 1.446 * Cp - 0.36
    c16 = 8.07981 * Cp - 13.8673 * Cp ** 2 + 6.984388 * Cp ** 3 if Cp < 0.8 else 1.73014 - 0.7067 * Cp
    m1 = 0.0140407 * L / T - 1.75254 * vol ** (1 / 3) / L - 4.79323 * B / L - c16
    if L ** 3 / vol < 512:
        c15 = -1.69385
    elif L ** 3 / vol <= 1727:
        c15 = -1.69385 + (L / vol ** (1 / 3) - 8.0) / 2.36
    else:
        c15 = 0.0
    m2 = c15 * Cp ** 2 * math.exp(-0.1 * Fn ** -2)
    Rw = c1 * c2 * c5 * vol * rho * g * math.exp(m1 * Fn ** -0.9 + m2 * math.cos(lam / Fn ** 2))
    Rf = 0.5 * rho * Vs * Vs * S * Cf
    Rv = k1 * Rf
    if ABT > 0:
        PB = 0.56 * math.sqrt(ABT) / (TF - 1.5 * hB)
        Fni = Vs / math.sqrt(g * (TF - hB - 0.25 * math.sqrt(ABT))) + 0.15 * Vs * Vs
        RB = 0.11 * math.exp(-3 * PB ** -2) * Fni ** 3 * ABT ** 1.5 * rho * g / (1 + Fni ** 2)
    else:
        RB = 0.0
    if AT > 0:
        FnT = Vs / math.sqrt(2 * g * AT / (B + B * Cwp))
        c6 = 0.2 * (1 - 0.2 * FnT) if FnT < 5 else 0.0
        RTR = 0.5 * rho * Vs * Vs * AT * c6
    else:
        RTR = 0.0
    c4 = min(TF / L, 0.04)
    CA = 0.006 * (L + 100) ** -0.16 - 0.00205 + 0.003 * math.sqrt(L / 7.5) * Cb ** 4 * c2 * (0.04 - c4)
    RA = 0.5 * rho * Vs * Vs * S * CA
    Rapp = 0.5 * rho * Vs * Vs * Sapp * k2 * Cf
    Rt = Rv + Rapp + Rw + RB + RTR + RA
    d.update(S=S, Re=Re, Cf=Cf, LR=LR, c12=c12, c13=c13, k1=k1, c7=c7, iE=iE, c1=c1, c2=c2, c3=c3, c5=c5,
             lam=lam, c16=c16, m1=m1, m2=m2, c15=c15, Rw=Rw, Rf=Rf, Rv=Rv, RB=RB, RTR=RTR, CA=CA, c4=c4, RA=RA,
             Rapp=Rapp, Rt=Rt, Fn=Fn, PE=Rt * Vs)
    return d


def prop_factors(L, B, T, Cb, Cp, lcb, S, Cf, CA, k1, D, Ae, Cstern=0.0):
    cv = k1 * Cf + CA
    c8 = B * S / (L * D * T) if B / T > 5 else S * (7 * B / T - 25) / (L * D * (B / T - 3))
    c9 = c8 if c8 < 28 else 32 - 16 / (c8 - 24)
    c11 = T / D if T / D < 2 else 0.0833333 * (T / D) ** 3 + 1.33333
    Cp1 = 1.45 * Cp - 0.315 - 0.0225 * lcb
    w = (c9 * cv * (L / T) ** 0.6459 * (0.0661875 + 1.21756 * c11 * cv / (1 - Cp1))
         + 0.24558 * math.sqrt(B / (L * (1 - Cp1)))
         - 0.09726 / (0.95 - Cp) + 0.11434 / (0.95 - Cb) + 0.75 * Cstern * Cp + 0.002 * Cstern)
    c10 = B / L if L / B >= 5.2 else 0.25 - 0.003328402 / (B / L - 0.134615385)
    t = (0.001979 * L / (B - B * Cp1) + 1.0585 * c10 - 0.00524 - 0.1418 * D * D / (B * T) + 0.0015 * Cstern)
    etaR = 0.9922 - 0.05908 * Ae + 0.07424 * (Cp - 0.0225 * lcb)
    return dict(cv=cv, c8=c8, c9=c9, c11=c11, Cp1=Cp1, w=w, c10=c10, t=t, etaR=etaR, etaH=(1 - t) / (1 - w))


def bisect(kt_req, J, ae, Z, iters=10):
    lo, hi = 0.5, 1.4
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if KT(J, mid, ae, Z) > kt_req:
            hi = mid          # KT too high -> P/D too large -> drop the upper bound
        else:
            lo = mid
    return 0.5 * (lo + hi)


def keller(T, D, h, Z, rho=RHO, p_atm=101325.0, pv=1705.0, g=G):
    p0 = p_atm + rho * g * h
    return (1.3 + 0.3 * Z) * T / ((p0 - pv) * D * D)


def std_ae(x, step=0.05, lo=0.30, hi=1.05):
    return max(lo, min(hi, round(math.ceil(x / step) * step, 2)))


def run_case(c):
    """Replicates sheets 1-4 exactly, including the rpm sweep grid."""
    d = resistance(L=c["L"], B=c["B"], T=c["T"], TF=c["TF"], vol=c["vol"], Cb=c["Cb"], Cp=c["Cp"],
                   Cm=c["Cm"], Cwp=c["Cwp"], lcb=c["lcb"], ABT=c["ABT"], hB=c["hB"], AT=c["AT"],
                   Cstern=c["Cstern"], Sapp=c["Sapp"], k2=c["k2"], Vs=c["Vs"])
    D = c["D"]
    h = c["T"] - (c["tip"] + D / 2)
    pv = 0.61121 * math.exp(17.502 * c["t_sw"] / (c["t_sw"] + 240.97)) * 1000.0
    Rt_s = d["Rt"] * (1 + c["SM"])
    # t does not depend on the blade area, so solve it first, then Keller with the real thrust
    t = prop_factors(c["L"], c["B"], c["T"], c["Cb"], c["Cp"], c["lcb"], d["S"], d["Cf"], d["CA"],
                     d["k1"], D, 0.55, c["Cstern"])["t"]
    T = Rt_s / (1 - t)
    kell = keller(T, D, h, c["Z"], pv=pv)
    ae = max(std_ae(kell), std_ae(c["Ae_min"]))
    pf = prop_factors(c["L"], c["B"], c["T"], c["Cb"], c["Cp"], c["lcb"], d["S"], d["Cf"], d["CA"],
                      d["k1"], D, ae, c["Cstern"])
    Va = c["Vs"] * (1 - pf["w"])
    sweep = []
    for i in range(31):
        n = 150 + 75 * i
        ns = n / 60.0
        J = Va / (ns * D)
        kt_req = T / (RHO * ns * ns * D ** 4)
        pd = bisect(kt_req, J, ae, c["Z"])
        kt = KT(J, pd, ae, c["Z"])
        kq = KQ(J, pd, ae, c["Z"])
        eta = J * kt / (2 * math.pi * kq) if kq > 0 else 0
        Q = kq * RHO * ns * ns * D ** 5
        PD = 2 * math.pi * ns * Q / pf["etaR"]
        ok = (KT(J, 0.5, ae, c['Z']) <= kt_req <= KT(J, 1.4, ae, c['Z'])) and kq > 0 and eta > 0
        sweep.append(dict(n=n, J=J, kt_req=kt_req, pd=pd, kt=kt, kq=kq, eta=eta, Q=Q, PD=PD, ok=ok))
    best = min([s for s in sweep if s["ok"]], key=lambda s: s["PD"])
    out = dict(d)
    out.update(pf)
    out['pv'] = pv
    out.update(J_opt=best["J"], kt_opt=best["kt"], kq_opt=best["kq"], Q_opt=best["Q"], kt_req_opt=best["kt_req"], pd_lim_opt=best["pd"])
    out.update(D=D, h=h, keller=kell, ae=ae, Rt_s=Rt_s, thrust=T, Va=Va, n_opt=float(best["n"]),
               pd_opt=best["pd"], eta_opt=best["eta"], PD_opt=best["PD"] / 1000.0,
               PE_kn=c["Vs"] * d["Rt"] / 1000.0)
    return out


DHONI = dict(name="30 m passenger dhoni", L=30.0, B=7.0, T=1.6, TF=1.6, vol=184.8, Cb=0.55, Cp=0.60,
             Cm=0.9167, Cwp=0.78, lcb=-1.0, ABT=0.0, hB=0.0, AT=0.0, Cstern=0.0, Sapp=6.0, k2=1.40,
             Vs=9.0 * 0.514444, SM=0.15, t_sw=32.0, D=0.90, tip=0.15, Z=4, Ae_min=0.55)
FERRY = dict(name="48 m passenger ferry", L=48.0, B=10.5, T=2.6, TF=2.6, vol=0.62 * 48 * 10.5 * 2.6,
             Cb=0.62, Cp=0.66, Cm=0.94, Cwp=0.80, lcb=-0.5, ABT=0.0, hB=0.0, AT=0.0, Cstern=0.0,
             Sapp=14.0, k2=1.45, Vs=11.0 * 0.514444, SM=0.15, t_sw=32.0, D=1.70, tip=0.15, Z=4, Ae_min=0.55)

if __name__ == "__main__":
    out = {}
    for key, case in (("DHONI", DHONI), ("FERRY", FERRY)):
        res = run_case(case)
        out[key] = dict(inputs=case, results={k: v for k, v in res.items() if isinstance(v, float)})
        print("=" * 70)
        print(case["name"])
        for k in ("S", "Cf", "k1", "c7", "iE", "c1", "Rw", "Rf", "Rv", "RA", "Rapp", "Rt", "PE_kn", "w", "t",
                  "etaR", "etaH", "keller", "ae", "thrust", "n_opt", "pd_opt", "eta_opt", "PD_opt"):
            print(f"  {k:9s} {res[k]:16.6f}")
    with open("refdata.py", "w") as f:
        f.write('"""Generated by verify_ref.py - independent reference values for the workbook."""\n')
        f.write("REF = %r\n" % (out,))
    print("\nwrote refdata.py")
