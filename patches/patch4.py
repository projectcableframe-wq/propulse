import io, sys
P='app/yanmar_engine_propeller_selector.html'
s=open(P,encoding='utf-8').read()
orig=s

def rep(old,new,n=1):
    global s
    c=s.count(old)
    assert c==n, (c,n,old[:90])
    s=s.replace(old,new)

# --- 1. Burrill: use the resolved C, not the raw argument -------------------
rep("""  const tauC  = burrillTauC(sigma, backCavPct);""",
    """  /* AUDIT v3 FIX (B-02): the limit must be evaluated with the RESOLVED
     permissible back cavitation C (default 5 % when none is entered), not with
     the raw argument. Passing null/undefined here produced NaN, which then fell
     through to the misleading message "Burrill limit non-positive
     (super-cavitating regime)" for an ordinary 5 % default. */
  const tauC  = burrillTauC(sigma, C);""")

# --- 2. bSeries: refuse evaluation outside the series envelope --------------
rep("""function bSeries(J, PD, EAR, Z, Rn){
  const c = bsCoeffs(J, EAR, Z, Rn);
  const KT = evalPD(c.kt, PD), KQ = evalPD(c.kq, PD);
  const eta = (KQ>1e-9 && J>0) ? (J*KT)/(2*Math.PI*KQ) : 0;
  return {KT:KT, KQ:KQ, eta:eta};
}""",
"""function bSeries(J, PD, EAR, Z, Rn){
  /* AUDIT v3 FIX (P-02): the polynomial is a curve fit, not a physical model.
     Outside the series envelope it returns negative thrust and torque at high J
     and a fictitious efficiency at high pitch, so an out-of-envelope call is
     REFUSED here rather than silently extrapolated. The design solver already
     restricts itself to these bounds internally; this guard protects the
     exported evaluator (charts, external tooling, tests).
       J 0-1.5, P/D 0.5-1.4, A_E/A_O 0.30-1.05, Z 2-7
     (Oosterveld & van Oossanen 1975 series definition; see BS_RANGE.) */
  const bad = [];
  if(!isNum(J) || J < 0 || J > 1.5) bad.push('J = '+J+' (valid 0-1.5)');
  if(!isNum(PD) || PD < BS_RANGE.PDmin || PD > BS_RANGE.PDmax)
    bad.push('P/D = '+PD+' (valid '+BS_RANGE.PDmin+'-'+BS_RANGE.PDmax+')');
  if(!isNum(EAR) || EAR < BS_RANGE.EARmin || EAR > BS_RANGE.EARmax)
    bad.push('A_E/A_O = '+EAR+' (valid '+BS_RANGE.EARmin+'-'+BS_RANGE.EARmax+')');
  if(!isNum(Z) || Z < BS_RANGE.Zmin || Z > BS_RANGE.Zmax || Z !== Math.round(Z))
    bad.push('Z = '+Z+' (valid integer '+BS_RANGE.Zmin+'-'+BS_RANGE.Zmax+')');
  if(!isNum(Rn) || Rn <= 0) bad.push('Rn = '+Rn+' (must be a positive Reynolds number)');
  if(bad.length) return {error:'Wageningen B-series: out of the series envelope — '+bad.join('; ')+
    '. The 39/47-term polynomials are a curve fit over that envelope and are not to be extrapolated.'};
  const c = bsCoeffs(J, EAR, Z, Rn);
  const KT = evalPD(c.kt, PD), KQ = evalPD(c.kq, PD);
  const eta = (KQ>1e-9 && J>0) ? (J*KT)/(2*Math.PI*KQ) : 0;
  return {KT:KT, KQ:KQ, eta:eta, inEnvelope:true};
}""")

# --- 3. Savitsky core: gate deadrise and record the trim band --------------
rep("""  const g=CONST.g, rho=p.rho, nu=p.nu, W=p.W, V=p.V, B=p.B, beta=p.beta;
  const out={steps:[]};""",
"""  const g=CONST.g, rho=p.rho, nu=p.nu, W=p.W, V=p.V, B=p.B, beta=p.beta;
  const out={steps:[]};
  /* AUDIT v3 FIX (S-03): validity gates are enforced in the primitive as well
     as in the UI, so any caller (including external tooling) cannot obtain a
     number that the deadrise correction was never fitted for. */
  if(!isNum(beta) || beta < 0 || beta > 30)
    return {error:'Savitsky deadrise beta = '+beta+' deg is outside the documented domain (0-30 deg). No resistance is reported.'};
  if(!isNum(W) || W <= 0) return {error:'Savitsky requires a positive displacement weight.'};
  if(!isNum(B) || B <= 0) return {error:'Savitsky requires a positive chine beam.'};
  if(!isNum(V) || V <= 0) return {error:'Savitsky requires a positive speed.'};
  if(!(p.LCG > 0)) return {error:'Savitsky requires the LCG forward of the transom (positive).'};""")

rep("""  out.trimResidual = cpResidual(tau);
  out.trimBracketed = !p.fixedTrim;""",
"""  out.trimResidual = cpResidual(tau);
  out.trimBracketed = !p.fixedTrim;
  /* The 2-15 deg band belongs to the regression (AUDIT v3 S-02). Recorded in
     the primitive so the caller cannot lose the information. */
  out.trimOutOfBand = !(tau >= 2 && tau <= 15);""")

open(P,'w',encoding='utf-8').write(s)
print("patched: +%d bytes" % (len(s)-len(orig)))
