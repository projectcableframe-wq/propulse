import re, sys, io
p = 'app/yanmar_engine_propeller_selector.html'
src = open(p, encoding='utf-8').read()
orig = src
changes = []

def rep(old, new, name, count=1):
    global src
    n = src.count(old)
    if n != count:
        print("FAILED [%s]: found %d occurrences (expected %d)" % (name, n, count))
        sys.exit(1)
    src = src.replace(old, new, count)
    changes.append(name)

# ---------------------------------------------------------------- E1 Cloudflare
m = re.search(r'-->[ \t]*<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>[ \t]*</body>', src, re.S)
assert m, "cloudflare script not found"
src = src[:m.start()] + '-->\n</body>' + src[m.end():]
changes.append('E1 remove injected Cloudflare bootstrap script')

# ---------------------------------------------------------------- E2 Savitsky Vm
old = """  const liftTerm = 0.0120*Math.sqrt(lam)*Math.pow(tau,1.1);
  const vmArg = 1 - (liftTerm - 0.0065*beta*Math.pow(liftTerm,0.60))/(lam*Math.cos(tauRad));
  /* FINAL-AUDIT FIX (FA-02): the original floored vmArg at 0.05, silently
     inventing a mean bottom velocity when the Savitsky velocity ratio is
     imaginary (lift term exceeds lambda*cos(tau)). That is outside the
     method's solution space: reject, do not floor. */"""
new = """  const liftTerm = 0.0120*Math.sqrt(lam)*Math.pow(tau,1.1);
  /* AUDIT v3 FIX (S-01) — MEAN BOTTOM VELOCITY.
     Savitsky (1964) defines the mean bottom velocity from the DEADRISE-
     CORRECTED LIFT COEFFICIENT:
        Vm/V = sqrt( 1 - CLbeta / (lambda cos tau) ),
        CLbeta = CL0 - 0.0065 beta CL0^0.6   (= the hull load coefficient CLb
                 that savitskyLiftCL0() solved for, by construction).
     The previous build used the dynamic-lift term only (0.0120 sqrt(lambda)
     tau^1.1) with the deadrise deduction applied to that term, i.e. it
     dropped the hydrostatic term 0.0055 lambda^2.5 / Cv^2. On the published
     Shoemaker (1934) model-29 check case the two forms differ by 0.9 % in Vm
     (0.4 % in frictional drag), so the correction is small but it makes the
     implementation match the published equation. The old form is still
     evaluated and reported as a sensitivity, not used. */
  const vmArgPublished = 1 - CLb/(lam*Math.cos(tauRad));
  const vmArgLegacy    = 1 - (liftTerm - 0.0065*beta*Math.pow(liftTerm,0.60))/(lam*Math.cos(tauRad));
  const vmArg = vmArgPublished;
  /* FINAL-AUDIT FIX (FA-02): never floor vmArg — an imaginary velocity ratio
     is outside the method's solution space. */"""
rep(old, new, 'E2 Savitsky Vm -> published CLbeta form')

old = """  const Vm = V*Math.sqrt(vmArg);
  out.Vm = Vm;"""
new = """  const Vm = V*Math.sqrt(vmArg);
  out.Vm = Vm;
  out.VmLegacy = (vmArgLegacy > 0) ? V*Math.sqrt(vmArgLegacy) : null;
  out.vmBasis = 'Vm/V = sqrt(1 - CL_beta/(lambda cos tau)), CL_beta = CL0 - 0.0065 beta CL0^0.6 (Savitsky 1964)';
  out.dfSensitivityPct = (out.VmLegacy != null && Vm > 0) ? (Math.pow(out.VmLegacy/Vm,2) - 1)*100 : null;"""
rep(old, new, 'E2b report Vm basis + legacy sensitivity')

# ---------------------------------------------------------------- E2c Df uses published basis note
old = """  out.DfBasis = 'Df at mean bottom velocity Vm (Savitsky 1964); V-basis variant reported for sensitivity only';"""
new = """  out.DfBasis = 'Df at mean bottom velocity Vm (Savitsky 1964, CL_beta form); V-basis variant reported for sensitivity only';"""
rep(old, new, 'E2c Df basis label')

# ---------------------------------------------------------------- E3 Burrill domain
old = """function burrillCheck(T, Va, n, D, PD, h, rho, backCavPct, EAR){
  const VR2 = Va*Va + Math.pow(0.7*Math.PI*n*D,2);"""
new = """function burrillCheck(T, Va, n, D, PD, h, rho, backCavPct, EAR){
  /* AUDIT v3 FIX (B-01): the Carmichael correlation of Burrill's chart is
     quoted by its own source (MIT OCW 2.611 cavitation notes) as valid for
     "C <= 25 (%) or so". Outside that band the correlation is an
     extrapolation and returns a non-physical limit (it goes negative for
     supercavitating propellers). Refuse instead of extrapolating. */
  const C = (backCavPct==null) ? 5 : backCavPct;
  if(!isFinite(C) || !(C > 0) || C > 25)
    return {ok:false, sigma:null, tauC:null, EARreq:Infinity,
      reason:'Allowable back cavitation '+(backCavPct==null?'(none)':backCavPct+' %')+
        ' is outside the validity of the Carmichael correlation of the Burrill chart (0 < C <= 25 %). Enter a value of 25 % or less.'};
  const VR2 = Va*Va + Math.pow(0.7*Math.PI*n*D,2);"""
rep(old, new, 'E3 Burrill/Carmichael C<=25% domain guard')

# ---------------------------------------------------------------- E4 Savitsky trim domain for fixed trim
old = """    if(!inp.fixedTrim && (r.tau<2 || r.tau>15)) flags.push('equilibrium trim '+(Math.round(r.tau*100)/100)+' deg outside 2-15 deg');"""
new = """    /* AUDIT v3 FIX (S-02): the 2-15 deg trim band belongs to the Savitsky
       regressions themselves, not to the way the trim was obtained. A
       USER-FIXED trim outside that band is equally outside the method's
       validation, so it is flagged too (it is additionally not an
       equilibrium solution). */
    if(r.tau<2 || r.tau>15) flags.push('running trim '+(Math.round(r.tau*100)/100)+' deg outside the 2-15 deg band of the Savitsky regressions'+
      (inp.fixedTrim ? ' (USER-FIXED trim: not an equilibrium solution either)' : ''));"""
rep(old, new, 'E4 Savitsky trim band also applies to user-fixed trim')

# ---------------------------------------------------------------- E5 scoreCandidate null mass
old = """  const wt = c.installedMass*inp.nProps;
  const wtS = (c.eng.src_mass==='Y' || c.eng.src_mass==='YB') ? 1/(1+wt/6000) : 0.5;"""
new = """  /* AUDIT v3 FIX (R-01): installed mass can legitimately be NULL when the gear
     mass is not in the database. The previous expression multiplied null by
     nProps (-> 0) and then scored 1/(1+0) = 1.0, i.e. the HIGHEST possible
     mass score for an engine whose installed mass is unknown. An unknown
     value must be neutral, never best. */
  const massKnown = (c.installedMass != null && isFinite(c.installedMass) && c.installedMass > 0);
  const wt = massKnown ? c.installedMass*inp.nProps : null;
  const wtS = (massKnown && (c.eng.src_mass==='Y' || c.eng.src_mass==='YB')) ? 1/(1+wt/6000) : 0.5;"""
rep(old, new, 'E5 null installed mass must not score best')

# ---------------------------------------------------------------- E6 Cm help text
old = """  defField({id:'Cm', label:'Midship coefficient C<sub>M</sub>', kind:'plain', unit:null, req:false,
    min:0.55, max:0.999, help:'Blank ⇒ estimated from hull type and C<sub>B</sub> (0.93 + 0.07·C<sub>B</sub> for full commercial forms, 0.90 + 0.08·C<sub>B</sub> for finer forms, 0.70 + 0.11·C<sub>B</sub> for slender hulls), flagged as estimated."""
new = """  defField({id:'Cm', label:'Midship coefficient C<sub>M</sub>', kind:'plain', unit:null, req:false,
    min:0.55, max:0.999, help:'Blank ⇒ estimated by CONTINUOUS piecewise-linear interpolation of the published per-type C<sub>M</sub> table at the computed C<sub>B</sub> (anchors C<sub>B</sub>/C<sub>M</sub> = 0.30/0.68 slender, 0.45/0.80 frigate, 0.60/0.945 cargo-container, 0.82/0.988 tanker-bulk; clamped to 0.55-0.995), flagged as estimated. AUDIT v3: this help text previously quoted three linear regressions that the code does NOT use."""
rep(old, new, 'E6 Cm help text now matches the implemented default')

# ---------------------------------------------------------------- E7a engine DB 6AYEM-ET
old = """    ratings:[
      {duty:'C',  ymark:'C', kW:555, rpm:1840, src:'Y', sfc:201, src_sfc:'Y'},   // PHASE-2 FIX (L-4): Yanmar 6AYEM product information C 201 g/kWh (+5 %, without gear)
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:204, src_sfc:'Y'},   // PHASE-2 FIX (L-4): M 204 g/kWh (+5 %, without gear)
      {duty:'LD', ymark:'L', kW:670, rpm:1938, src:'Y', sfc:203, src_sfc:'E'}
    ]"""
new = """    /* AUDIT v3 FIX (D-11): rating attribution corrected against the official
       YANMAR 6AYE SERIES table (yanmar.com, accessed 2026-10-25):
         6AYEM-ST / C 485(659)/1900
         6AYEM-ET / C 555(755)/1840, / H 599(814)/1900, / M 610(829)/1900
         6AYEM-GT / L 670(911)/1938, / S 737(1002)/2000
       The previous record gave 6AYEM-ET an L rating (that is the GT/L row),
       gave 6AYEM-GT an H and an M rating (both are ET rows), and omitted the
       ET/H rating altogether — so an H-duty vessel could be offered a
       GT/H configuration YANMAR does not publish. */
    ratings:[
      {duty:'C',  ymark:'C', kW:555, rpm:1840, src:'Y', sfc:201, src_sfc:'Y'},   // Yanmar 6AYEM product information: C 201 g/kWh (+5 %, without gear) — NOT re-verified in the v3 audit
      {duty:'HD', ymark:'H', kW:599, rpm:1900, src:'Y', sfc:null, src_sfc:'N'}, // 6AYE SERIES table: 6AYEM-ET / H 599(814)/1900; no rated-point SFC published for this row
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:204, src_sfc:'Y'}    // Yanmar 6AYEM product information: M 204 g/kWh (+5 %) — NOT re-verified in the v3 audit
    ]"""
rep(old, new, 'E7a 6AYEM-ET ratings corrected (C/H/M; L removed)')

# ---------------------------------------------------------------- E7b 6AYEM-GT
old = """    ratings:[
      {duty:'HD', ymark:'H', kW:599, rpm:1900, src:'Y', sfc:null, src_sfc:'N'},
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:null, src_sfc:'N'},
      {duty:'LD', ymark:'L', kW:670, rpm:1938, src:'Y', sfc:203, src_sfc:'E'},
      {duty:'LD', ymark:'S', kW:737, rpm:2000, src:'Y', sfc:207, src_sfc:'E'}
    ]"""
new = """    /* AUDIT v3 FIX (D-11): 6AYEM-GT is published by YANMAR only as an L and an
       S rating (6AYE SERIES table). The H and M rows that were stored here
       belong to 6AYEM-ET and have been moved there. */
    ratings:[
      {duty:'LD', ymark:'L', kW:670, rpm:1938, src:'Y', sfc:203, src_sfc:'E'},
      {duty:'LD', ymark:'S', kW:737, rpm:2000, src:'Y', sfc:207, src_sfc:'E'}
    ]"""
rep(old, new, 'E7b 6AYEM-GT restricted to published L/S ratings')

# ---------------------------------------------------------------- E7c 6AYEM-GTWS
old = """    ratings:[
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:null, src_sfc:'N'},
      {duty:'LD', ymark:'L', kW:670, rpm:1938, src:'Y', sfc:203, src_sfc:'E'},
      {duty:'LD', ymark:'S', kW:749, rpm:2000, src:'Y', sfc:207, src_sfc:'E'}
    ]
  },"""
new = """    /* AUDIT v3 FIX (D-11): 6AYEM-GTWS is published as L 670/1938 and
       S 749/2000 only. The M 610/1900 row belongs to 6AYEM-ETWS, which is now
       its own record. */
    ratings:[
      {duty:'LD', ymark:'L', kW:670, rpm:1938, src:'Y', sfc:203, src_sfc:'E'},
      {duty:'LD', ymark:'S', kW:749, rpm:2000, src:'Y', sfc:207, src_sfc:'E'}
    ]
  },
  {
    model:'6AYEM-ETWS', series:'6AYE', codeVerified:true,
    codeNote:'Emissions variant of 6AYEM-ET (IMO Tier III / EPA Tier IV). YANMAR 6AYE SERIES table lists C 555(755)/1840 and M 610(829)/1900. Confirm the build and the regional certificate with your Yanmar dealer.',
    cyl:'6 in-line', bore:155, stroke:180, disp:20.379, src_geom:'Y',
    aspiration:'Turbocharger + intercooler (common rail)', cooling:'Heat exchanger',
    emissions:'6AYEM-ETWS: IMO Tier III / EPA Tier IV (series table); confirm certificate', src_em:'Y',
    dryMass:2418, src_mass:'Y', dims:[2000,1305,1431], src_dims:'Y',
    gears:[{model:'YXH-240-7', ratios:[1.95,2.27,2.56,3.03,3.48], mass:632}], src_gear:'Y',
    apps:'Emissions-compliant commercial propulsion (Tier III / EPA Tier IV variant of the ET)',
    ratings:[
      {duty:'C',  ymark:'C', kW:555, rpm:1840, src:'Y', sfc:null, src_sfc:'N'},
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:null, src_sfc:'N'}
    ]
  },"""
rep(old, new, 'E7c 6AYEM-GTWS restricted; 6AYEM-ETWS record added')

# ---------------------------------------------------------------- E7d rating defs
old = """  '6AYEM-GTWS':{set:'YM-2016',    dn:200, note:'GTWS S rating listed by Yanmar; YM-2016 S limits used as conservative same-series screening pending the GTWS-specific rating sheet.'},"""
new = """  '6AYEM-GTWS':{set:'YM-2016',    dn:200, note:'GTWS S rating listed by Yanmar; YM-2016 S limits used as conservative same-series screening pending the GTWS-specific rating sheet.'},
  '6AYEM-ETWS':{set:'YM-2016',    dn:200, note:'Emissions variant of 6AYEM-ET; 2016 products guide limits applied as same-series screening pending the ETWS-specific rating sheet.'},"""
rep(old, new, 'E7d rating-definition mapping for 6AYEM-ETWS')

old = """  '6AYEM-GTWS':{dryWithoutGear:2365, withGear:null},"""
new = """  '6AYEM-GTWS':{dryWithoutGear:2365, withGear:null},
  '6AYEM-ETWS':{dryWithoutGear:2418, withGear:null},"""
rep(old, new, 'E7e mass table entry for 6AYEM-ETWS')

open(p,'w',encoding='utf-8').write(src)
print("applied:", len(changes))
for c in changes: print("  -", c)
print("size change:", len(src)-len(orig))
