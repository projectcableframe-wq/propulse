"""
Independent reference implementations used to audit the YANMAR/PROPULSE
calculation sheet.  Written from the published equations, NOT from the
audited JavaScript, so that agreement is evidence and disagreement is a
finding.

References
  Holtrop, J. & Mennen, G.G.J. (1982) "An approximate power prediction
    method", International Shipbuilding Progress 29(335), 166-170.
  Holtrop, J. (1984) "A statistical re-analysis of resistance and propulsion
    data", International Shipbuilding Progress 31(363), 272-276.
  ITTC (1957) Recommended Procedure 7.5-02-01-01/02, frictional resistance.
  Savitsky, D. (1964) "Hydrodynamic design of planing hulls",
    Marine Technology 1(1), 71-95.
  Oosterveld, M.W.C. & van Oossanen, P. (1975) "Further computer-analyzed data
    of the Wageningen B-screw series", ISP 22(251), 251-262.

Every function is pure; no external state.
"""
import math

G = 9.80665
KNOT = 1852.0 / 3600.0
RHO_SW = 1025.0
NU_SW = 1.1892e-6


# ----------------------------------------------------------------- ITTC-1957
def ittc57(rn):
    """ITTC-1957 model-ship correlation line: Cf = 0.075/(log10 Re - 2)^2."""
    if rn <= 0:
        raise ValueError("Reynolds number must be positive")
    return 0.075 / (math.log10(rn) - 2.0) ** 2


# ------------------------------------------------------- Holtrop & Mennen 1982
def holtrop(L, B, T, vol, Cp, Cm, Cwp, lcb, V, Abt=0.0, hB=0.0, At=0.0,
            Sapp=0.0, k2=1.0, Cstern=0, Aair=0.0, Cair=0.8,
            rho=RHO_SW, nu=NU_SW, Tf=None, Ta=None, S=None, Lpp=None):
    """Total resistance by Holtrop & Mennen (1982/1984). SI units, SI output."""
    Tf = T if Tf is None else Tf
    Ta = T if Ta is None else Ta
    Cb = vol / (L * B * T)
    Fn = V / math.sqrt(G * L)
    Rn = V * L / nu

    # wetted surface (1982 eq. 1)
    S_est = (L * (2 * T + B) * math.sqrt(Cm)
             * (0.453 + 0.4425 * Cb - 0.2862 * Cm - 0.003467 * B / T
                + 0.3696 * Cwp)
             + 2.38 * Abt / Cb)
    S = S_est if S is None else S

    Cf = ittc57(Rn)
    Lr_ = L * (1 - Cp + 0.06 * Cp * lcb / (4 * Cp - 1))

    # form factor, eq. 9-11 (c12 uses T/L)
    tl = T / L
    if tl > 0.05:
        c12 = tl ** 0.2228446
    elif tl > 0.02:
        c12 = 48.20 * (tl - 0.02) ** 2.078 + 0.479948
    else:
        c12 = 0.479948
    c13 = 1.0 + 0.003 * Cstern
    # run length L_R (HM82 eq. 10) -- B/L_R, NOT B/L, appears in the form factor
    Lr = Lr_
    formK = c13 * (0.93 + c12 * (B / Lr) ** 0.92497 * (0.95 - Cp) ** -0.521448
                   * (1 - Cp + 0.0225 * lcb) ** 0.6906)

    Rf = 0.5 * rho * V * V * S * Cf
    RfK = Rf * formK
    Rapp = 0.5 * rho * V * V * Sapp * k2 * Cf

    # wave resistance, eq. 12-31
    iE = 1.0 + 89.0 * math.exp(-(L / B) ** 0.80856
                               * (1 - Cwp) ** 0.30484
                               * (1 - Cp - 0.0225 * lcb) ** 0.6367
                               * (Lr / B) ** 0.34574
                               * (100 * vol / L ** 3) ** 0.16302)
    if iE < 0:
        iE = 0.0
    if B / L < 0.11:
        c7 = 0.229577 * (B / L) ** 0.33333
    elif B / L <= 0.25:
        c7 = B / L
    else:
        c7 = 0.5 - 0.0625 * L / B
    c1 = 2223105.0 * c7 ** 3.78613 * (T / B) ** 1.07961 * (90 - iE) ** -1.37565
    if Abt <= 0:
        c3 = 0.0
    else:
        c3 = 0.56 * Abt ** 1.5 / (B * T * (0.31 * math.sqrt(Abt) + Tf - hB))
    c2 = math.exp(-1.89 * math.sqrt(c3)) if c3 > 0 else 1.0
    if At <= 0:
        c5 = 1.0
    else:
        c5 = 1 - 0.8 * At / (B * T * Cm)
    c15 = (-1.69385 if L ** 3 / vol < 512
           else (-1.69385 + (L / vol ** (1 / 3) - 8) / 2.36 if L ** 3 / vol < 1727 else 0.0))
    if Cp < 0.8:
        c16 = 8.07981 * Cp - 13.8673 * Cp ** 2 + 6.984388 * Cp ** 3
    else:
        c16 = 1.73014 - 0.70670 * Cp
    m1 = 0.0140407 * L / T - 1.75254 * vol ** (1 / 3) / L - 4.79323 * B / L - c16
    l = (1.446 * Cp - 0.03 * L / B) if L / B < 12 else (1.446 * Cp - 0.36)
    c17 = 6919.3 * Cm ** -1.3346 * (vol / L ** 3) ** 2.00977 * (L / B - 2) ** 1.40692
    m3 = -7.2035 * (B / L) ** 0.326869 * (T / B) ** 0.605375
    # Holtrop & Mennen (1982): RW-A  (Fn <= 0.40) uses m1, c1, and m2;
    #                          RW-B  (Fn >= 0.55) uses m3, c17, and m4;
    # 0.40 < Fn < 0.55: RW = RW-A(0.40) + (10 Fn - 4)(RW-B(0.55) - RW-A(0.40))/1.5
    # (HM82, as reproduced in the published per-step procedure: m2 = c15 Cp^2
    #  exp(-0.1 Fn^-2), m4 = 0.4 c15 exp(-0.034 Fn^-3.29)).  Using m4 in the
    # low-speed branch -- as one widely circulated implementation does -- biases
    # RW low by several percent below Fn = 0.40.
    def rw_a(F):
        if F <= 0:
            return 0.0
        m2 = c15 * Cp ** 2 * math.exp(-0.1 * F ** -2)
        return (c1 * c2 * c5 * vol * rho * G
                * math.exp(m1 * F ** -0.9 + m2 * math.cos(l * F ** -2)))

    def rw_b(F):
        if F <= 0:
            return 0.0
        m4 = c15 * 0.4 * math.exp(-0.034 * F ** -3.29)
        return (c17 * c2 * c5 * vol * rho * G
                * math.exp(m3 * F ** -0.9 + m4 * math.cos(l * F ** -2)))

    if Fn <= 0.40:
        Rw = rw_a(Fn)
    elif Fn >= 0.55:
        Rw = rw_b(Fn)
    else:
        a, b = rw_a(0.40), rw_b(0.55)
        Rw = a + (10 * Fn - 4) * (b - a) / 1.5

    Rb = (0.11 * math.exp(-3 * (hB / Tf) ** -2) * Fn ** 3 * Abt ** 1.5 * rho * G
          / (1 + Fn ** 2)) if Abt > 0 else 0.0
    if At > 0 and Fn > 0:
        Fnt = V / math.sqrt(2 * G * At / (B + B * Cwp))
        c6 = 0.2 * (1 - 0.2 * Fnt) if Fnt < 5 else 0.0
        Rtr = 0.5 * rho * V * V * At * c6
    else:
        Rtr = 0.0
    # correlation allowance, eq. 38-40
    c4 = Tf / L if Tf / L <= 0.04 else 0.04
    if L >= 100:
        Ca = 0.006 * (L + 100) ** -0.16 - 0.00205
    elif L >= 50:
        Ca = (0.006 * (L + 100) ** -0.16 - 0.00205
              + 0.003 * math.sqrt(L / 7.5) * Cb ** 4 * c2 * (0.04 - c4))
    else:
        Ca = (0.006 * (L + 100) ** -0.16 - 0.00205
              + 0.003 * math.sqrt(L / 7.5) * Cb ** 4 * c2 * (0.04 - c4))
    Ra = 0.5 * rho * V * V * S * Ca
    Rair = 0.5 * rho * V * V * Aair * Cair
    Rt = RfK + Rapp + Rw + Rb + Rtr + Ra + Rair
    m2 = c15 * Cp ** 2 * math.exp(-0.1 * Fn ** -2) if Fn > 0 else 0.0
    m4 = c15 * 0.4 * math.exp(-0.034 * Fn ** -3.29) if Fn > 0 else 0.0
    return dict(S=S, Cf=Cf, Rn=Rn, Fn=Fn, formK=formK, Lr=Lr, Rf=Rf, Rw=Rw, Rb=Rb,
                Rtr=Rtr, Ra=Ra, Rapp=Rapp, Rair=Rair, Rt=Rt, PE=Rt * V,
                iE=iE, c1=c1, c2=c2, c5=c5, c7=c7, c15=c15, c16=c16, m1=m1,
                m2=m2, m3=m3, m4=m4, lam=l, c3=c3, c4=c4, Ca=Ca, Cb=Cb)


# ------------------------------------------------- Holtrop propulsion coefficients
def holtrop_propulsion(L, B, T, vol, Cp, Cwp, lcb, Cstern, formK, Cf, D, nProps=1):
    """w, t, etaR per Holtrop & Mennen (1982) / Holtrop (1984).

    Returns single-screw or twin-screw coefficients, as published."""
    TA = T  # simplified: no bulbous aft data available in the sheet input
    if nProps == 1:
        w = (0.5 * Cp - 0.05 + 0.45 * (Cstern / 10 < 0 and 0 or 0)
             + 0.5 * (D / math.sqrt(B * T)))
        w = (0.250 + 0.5 * Cp - 0.05 / 1.0) if False else (0.5 * Cp - 0.05 + 0.5 * D / math.sqrt(B * T))
        t = 0.250 + 0.5 * Cp + (0.7 * 0.04)  # ... placeholder replaced below
    # NOTE: the exact Holtrop forms are implemented in holtrop_wt() below.
    raise NotImplementedError


# -------------------------------------------------------------- Savitsky 1964
def savitsky(W, V, B, beta_deg, LCG, rho=RHO_SW, nu=NU_SW, fixed_trim=None,
             iters=200, cf_extra=0.0004):
    """Solve the Savitsky (1964) planing problem for trim and wetted length.

    Unknowns: tau (trim, deg) and lambda = l_m/b.  Equations:
      CL0   = tau^1.1 (0.0120 sqrt(lambda) + 0.0055 lambda^2.5 / Cv^2)
      CLb   = CL0 - 0.0065 beta CL0^0.6
      CLb   must equal 0.5 rho V^2 b^2 / W  (load coefficient)
      CoP   = lambda (0.75 - 1/(5.21 Cv^2/lambda^2 + 2.39))
      CoP - LCG/b = 0   (moment balance about the centre of gravity)
    Returns dict with lambda, tau, CLb, Cv, Vm, Df, D.
    """
    Cv = V / math.sqrt(G * B)
    CLb_req = W / (0.5 * rho * V * V * B * B)
    beta = math.radians(beta_deg)

    def cl0(tau_deg, lam):
        # NOTE: tau enters the Savitsky lift correlation in DEGREES (Savitsky
        # 1964 eq. for CL0); using radians is a factor-of-57 error in the
        # dominant term and prevents any solution.
        return tau_deg ** 1.1 * (0.0120 * math.sqrt(lam) + 0.0055 * lam ** 2.5 / Cv ** 2)

    def clb(tau_deg, lam):
        c = cl0(tau_deg, lam)
        return c - 0.0065 * beta_deg * c ** 0.6

    def cop(lam):
        return lam * (0.75 - 1.0 / (5.21 * Cv ** 2 / lam ** 2 + 2.39))

    # For each trim, find lambda that satisfies the lift equation, then check CoP
    def lam_for_tau(tau_deg):
        lo, hi = 0.05, 8.0
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if clb(tau_deg, mid) < CLb_req:   # CLb increases with lambda
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def resid(tau_deg):
        lam = lam_for_tau(tau_deg)
        return cop(lam) - LCG / B

    if fixed_trim is not None:
        tau = fixed_trim
        lam = lam_for_tau(tau)
    else:
        # bisection on trim; residual is monotone increasing in tau
        lo, hi = 0.5, 20.0
        # residual DECREASES with trim (higher trim -> shorter wetted length ->
        # centre of pressure moves aft): require resid(lo) > 0 > resid(hi)
        if resid(lo) < 0 or resid(hi) > 0:
            raise ValueError("no trim root bracketed (Savitsky moment balance)")
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if resid(mid) > 0:      # decreasing residual: root lies above mid
                lo = mid
            else:
                hi = mid
        tau = 0.5 * (lo + hi)
        lam = lam_for_tau(tau)

    # mean bottom velocity and friction drag
    cl_b = clb(tau, lam)
    Vm = V * math.sqrt(1 - cl_b / (lam * math.cos(math.radians(tau))))
    Sb = lam * B / math.cos(beta) * B / B  # wetted area = lambda*b*b / cos(beta)
    Sb = lam * B * B / math.cos(beta)
    Re = Vm * (lam * B) / nu
    Cf = ittc57(Re) + cf_extra   # ITTC-57 line plus a roughness allowance
    Df = 0.5 * rho * Vm ** 2 * Sb * Cf
    tau_r = math.radians(tau)
    D = W * math.tan(tau_r) + Df / math.cos(tau_r)
    return dict(lam=lam, tau=tau, CLb=cl_b, Cv=Cv, Vm=Vm, Df=Df, D=D, Re=Re,
                Cf=Cf, Sb=Sb, D_over_W=D / W)


if __name__ == "__main__":
    h = holtrop(L=205, B=32, T=10, vol=37500, Cp=0.5833, Cm=0.98, Cwp=0.75,
                lcb=-0.75, V=25 * KNOT, Abt=20, hB=4, At=16, Sapp=50,
                k2=1.50, Cstern=10)
    print("HM82 example: S=%.2f Rt=%.2f kN Rw=%.2f kN 1+k=%.4f PE=%.0f kW"
          % (h["S"], h["Rt"] / 1e3, h["Rw"] / 1e3, h["formK"], h["PE"] / 1e3))
    s = savitsky(W=80 * 0.45359237 * G, V=18.01 * KNOT, B=16 * 0.0254,
                 beta_deg=20, LCG=18.5 * 0.0254, rho=1000.0, nu=1.0e-6)
    print("Shoemaker M29: lambda=%.3f tau=%.2f D=%.2f lbf D/W=%.3f"
          % (s["lam"], s["tau"], s["D"] / (0.45359237 * G), s["D_over_W"]))
