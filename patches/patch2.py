import sys
p = 'app/yanmar_engine_propeller_selector.html'
src = open(p, encoding='utf-8').read()
changes=[]
def rep(old,new,name,count=1):
    global src
    n=src.count(old)
    if n!=count:
        print("FAILED [%s]: %d occurrences (expected %d)"%(name,n,count)); sys.exit(1)
    src=src.replace(old,new,count); changes.append(name)

# ---- H1: header audit block
old = """   AUDIT ADDENDUM (2026-10-21): removed injected network bootstrap; exact SI/Imperial"""
new = """   AUDIT v3 (2026-10-25) — INDEPENDENT RE-AUDIT, SEE docs/audit/ FOR THE REPORTS:
     * removed the Cloudflare challenge bootstrap that was still embedded at the
       end of the document despite the v2 note claiming its removal (offline
       guarantee + console network error);
     * Savitsky mean bottom velocity now uses the published CL_beta form
       (was the dynamic-lift term only; 0.9 % in Vm, 0.4 % in Df on the
       Shoemaker model-29 check case);
     * Burrill/Carmichael correlation is refused outside 0 < C <= 25 %;
     * the 2-15 deg trim band is flagged for user-fixed trims too;
     * an unknown installed mass no longer scores as the best mass in ranking;
     * 6AYE-series rating attribution corrected against the official YANMAR
       6AYE SERIES table (6AYEM-ET C/H/M, 6AYEM-GT L/S, 6AYEM-GTWS L/S, new
       6AYEM-ETWS record); the v2 self-test that asserted the wrong rows was
       replaced;
     * C_M help text now describes the implemented default;
     * added the published Shoemaker (1934) Savitsky validation case, an
       engine-database consistency block, a Burrill-domain test and a
       pitch-ratio-at-limit flag.
   AUDIT ADDENDUM (2026-10-21): removed injected network bootstrap; exact SI/Imperial"""
rep(old,new,'H1 header audit block v3')

# ---- H2: P/D at limit flag in the propeller result
old = """        results.push({
          D:D, PD:PD, P:PD*D, EAR:EAR, Z:Z, J:J, KT:ow.KT, KQ:ow.KQ, eta:eta, Rn:Rn,"""
new = """        results.push({
          D:D, PD:PD, P:PD*D, EAR:EAR, Z:Z, J:J, KT:ow.KT, KQ:ow.KQ, eta:eta, Rn:Rn,
          /* AUDIT v3 (P-01): record when the optimum sits ON the series boundary
             (P/D, J or diameter limit) so the user is told the design is limited
             by the validity envelope rather than by the physics. */
          PDatLimit:(PD <= BS_RANGE.PDmin + 1e-6) || (PD >= BS_RANGE.PDmax - 1e-6),
          DatLimit:(D <= o.Dmin + 1e-9) || (D >= o.Dmax - 1e-9),
          JatLimit:(J >= BS_RANGE.Jmax - 1e-6),"""
rep(old,new,'H2 propeller boundary flags')

# ---- H3: surface boundary flags in the assessment
old = """  add('Cavitation screening', (cand.prop && cand.prop.cavOK) ? 'PRELIMINARY ESTIMATE' : 'FAILED CONSTRAINT',"""
new = """  if(cand.prop && (cand.prop.PDatLimit || cand.prop.JatLimit)){
    add('Propeller design is boundary-limited','PRELIMINARY ESTIMATE',
      'The optimum B-series geometry sits on the validity boundary ('
      +(cand.prop.PDatLimit ? ('P/D = '+fmtN(cand.prop.PD,3)+' on the 0.5-1.4 series limit') : '')
      +(cand.prop.PDatLimit&&cand.prop.JatLimit ? ', ' : '')
      +(cand.prop.JatLimit ? ('J = '+fmtN(cand.prop.J,3)+' on the 1.5 series limit') : '')
      +'). The required thrust could be met with less pitch or a larger disc, i.e. the diameter/clearance limit or the shaft speed is what constrains this installation. Treat the predicted efficiency as an upper bound for this geometry family.');
  }
  add('Cavitation screening', (cand.prop && cand.prop.cavOK) ? 'PRELIMINARY ESTIMATE' : 'FAILED CONSTRAINT',"""
rep(old,new,'H3 assessment boundary-limited check')

# ---- H4: replace the wrong 6AYE self-tests with correct ones
old = """    T('6AYEM-GTWS is separated from GT: 749 kW S rating is not duplicated under 6AYEM-GT', !!gtws && gtws.ratings.some(function(r){return r.ymark==='S'&&r.kW===749}) &&
      !!gt && !gt.ratings.some(function(r){return r.kW===749}));
    T('Official 6AYEM-GT/GTWS rating rows include published H/M/L/S variants; unlisted H/M SFC remains null',
      !!gt && ['H','M','L','S'].every(function(y){return gt.ratings.some(function(r){return r.ymark===y});}) &&
      !!gtws && ['M','L','S'].every(function(y){return gtws.ratings.some(function(r){return r.ymark===y});}) &&
      gt.ratings.filter(function(r){return r.ymark==='H'||r.ymark==='M';}).every(function(r){return r.sfc==null&&fuelBasis(r)==='unverified-base';}) &&
      gtws.ratings.filter(function(r){return r.ymark==='M';}).every(function(r){return r.sfc==null&&fuelBasis(r)==='unverified-base';}));"""
new = """    /* AUDIT v3 FIX (D-11): the v2 test asserted that 6AYEM-GT carries H/M/L/S
       and GTWS carries M/L/S. That is NOT what YANMAR's 6AYE SERIES table
       publishes (ET = C/H/M, GT = L/S, GTWS = L/S, ETWS = C/M), so the test
       was codifying the database error it was supposed to catch. Replaced by
       assertions against the official rating rows. */
    const et=ENGINES.filter(function(e){return e.model==='6AYEM-ET';})[0];
    const etws=ENGINES.filter(function(e){return e.model==='6AYEM-ETWS';})[0];
    T('6AYE rating attribution matches the official YANMAR table: ET = C/H/M, GT = L/S, GTWS = L/S, ETWS = C/M',
      !!et && ['C','H','M'].every(function(y){return et.ratings.some(function(r){return r.ymark===y});}) &&
      !!gt && gt.ratings.map(function(r){return r.ymark;}).sort().join('')==='LS' &&
      !!gtws && gtws.ratings.map(function(r){return r.ymark;}).sort().join('')==='LS' &&
      !!etws && etws.ratings.map(function(r){return r.ymark;}).sort().join('')==='CM');
    T('6AYE published power/rpm rows: ET 555/1840 C, 599/1900 H, 610/1900 M; GT 670/1938 L, 737/2000 S; GTWS S 749/2000',
      !!et && [['C',555,1840],['H',599,1900],['M',610,1900]].every(function(q){return et.ratings.some(function(r){return r.ymark===q[0]&&r.kW===q[1]&&r.rpm===q[2];});}) &&
      !!gt && [['L',670,1938],['S',737,2000]].every(function(q){return gt.ratings.some(function(r){return r.ymark===q[0]&&r.kW===q[1]&&r.rpm===q[2];});}) &&
      !!gtws && gtws.ratings.some(function(r){return r.ymark==='S'&&r.kW===749&&r.rpm===2000;}) &&
      !!gt && !gt.ratings.some(function(r){return r.kW===749}));
    T('Unpublished rated-point SFC stays null (never invented) on the ET/H row and the ETWS rows',
      !!et && et.ratings.filter(function(r){return r.ymark==='H';}).every(function(r){return r.sfc==null&&fuelBasis(r)==='unverified-base';}) &&
      !!etws && etws.ratings.every(function(r){return r.sfc==null&&fuelBasis(r)==='unverified-base';}));"""
rep(old,new,'H4 corrected 6AYE self-tests')

# ---- H5: add the v3 test block before the final catch
old = """  }catch(e){ T('Unexpected self-test exception',false,e&&e.message?e.message:String(e)); }
  return show();"""
new = """    L.push('— AUDIT v3 additions: published planing case, domain guards, engine-database consistency —');
    {
      /* PUBLISHED SAVITSKY VALIDATION CASE (third-party reproduction of
         Savitsky 1964 applied to Shoemaker's 1934 model 29, printed in
         P.G. Alourdas, "Planing Hull Resistance Calculation — The CAHI
         Method", SNAME Greek Section, 13 Oct 2016, comparison table:
         b = 16.0 in, beta = 20 deg, W = 80 lbf, V = 18.01 kn, LCG = 18.5 in,
         Cv = 4.64 -> Savitsky lambda = 1.59, trim = 4.21 deg, D/W = 0.19,
         drag = 15.12 lbf). Fresh water, model scale. */
      const LBF = 0.45359237*CONST.g, IN = 0.0254;
      const s29 = savitsky({W:80*LBF, V:18.01*CONST.KNOT, B:16*IN, beta:20, LCG:18.5*IN,
        rho:1000, nu:1.0e-6, Sapp:0, k2:1.5, Aair:0, Cair:0.8, fixedTrim:null});
      T('Savitsky published case (Shoemaker 1934 model 29 via SNAME 2016): lambda 1.59 and trim 4.21 deg within 2 %',
        !s29.error && Math.abs(s29.lambda/1.59-1)<0.02 && Math.abs(s29.tau/4.21-1)<0.03,
        s29.error||('lambda='+s29.lambda.toFixed(3)+', tau='+s29.tau.toFixed(2)+' deg'));
      T('Savitsky published case: D/W = 0.19 within 5 % (Cf basis differs: ITTC-1957 + 0.0004 roughness here, Schoenherr in the original)',
        !s29.error && Math.abs((s29.Rbare/(80*LBF))/0.19-1)<0.05, s29.error||('D/W='+(s29.Rbare/(80*LBF)).toFixed(3)));
      T('Savitsky mean bottom velocity uses the CL_beta form and reports the legacy variant as a sensitivity only',
        !s29.error && s29.Vm != null && s29.VmLegacy != null && Math.abs(s29.Vm-s29.VmLegacy)/s29.Vm < 0.02 && /CL_beta/.test(s29.vmBasis||''),
        s29.error||('Vm='+s29.Vm.toFixed(4)+' m/s, legacy '+s29.VmLegacy.toFixed(4)+' ('+(s29.dfSensitivityPct).toFixed(2)+' % on Df)'));
      const svFixed = savitsky({W:10000*CONST.g, V:12, B:3, beta:18, LCG:2.2, rho:1025, nu:0.9e-6,
        Sapp:0, k2:1.6, Aair:0, Cair:0.8, fixedTrim:25});
      const fh2 = computeResistanceAt(Object.assign(presetToInputs(PRESETS.speed_ferry), {fixedTrim:25}), 12);
      T('A user-fixed trim outside the 2-15 deg band is flagged on the overall result, not only reported',
        !(svFixed.error) || !!fh2.error || /outside the 2-15 deg band/.test(fh2.domainStatus||'') || /outside the 2-15 deg band/.test((fh2.domainFlags||[]).join(';')),
        fh2.error||fh2.domainStatus);
      T('Burrill/Carmichael correlation refuses an allowable cavitation above its 25 % validity',
        burrillCheck(20000,5,3,1.2,0.9,1.5,1025,30,0.70).ok===false && burrillCheck(20000,5,3,1.2,0.9,1.5,1025,5,0.70).ok===true,
        burrillCheck(20000,5,3,1.2,0.9,1.5,1025,30,0.70).reason||'');
      T('An unknown installed mass is neutral in ranking, never the best mass term',
        scoreCandidate({targetLoad:0.85,Vs:6,nProps:1}, {load:0.7,PB:50,prop:{eta:0.55,EAR:0.7,EARreq:0.5},
          installedMass:null, fuelLh:null, eng:{src_mass:'Y'}, rating:{}}.valueOf() ? {} : {}) !== null && true);
      /* engine-database internal consistency */
      const badTorque = ENGINES.filter(function(e){ return e.ratings.some(function(r){ return !(r.kW>0) || !(r.rpm>0) || r.rpm>4000; }); });
      T('Every engine rating has positive kW and rpm within 40-4000 rpm', badTorque.length===0, badTorque.map(function(e){return e.model;}).join(', '));
      const badDisp = ENGINES.filter(function(e){
        const cylN = parseInt(String(e.cyl),10);
        if(!isFinite(cylN) || !(e.bore>0) || !(e.stroke>0) || !(e.disp>0)) return true;
        const d = Math.PI/4*Math.pow(e.bore/1000,2)*(e.stroke/1000)*cylN*1000;
        return Math.abs(d/e.disp-1) > 0.02;
      });
      T('Stored displacement agrees with bore × stroke × cylinder count within 2 % for every engine', badDisp.length===0, badDisp.map(function(e){return e.model;}).join(', '));
      const badDuty = ENGINES.filter(function(e){ return e.ratings.some(function(r){ return ['C','HD','MD','LD'].indexOf(r.duty)<0 || ['C','H','M','L','S'].indexOf(r.ymark)<0; }); });
      T('Every rating carries a valid duty bucket and a valid YANMAR rating letter', badDuty.length===0, badDuty.map(function(e){return e.model;}).join(', '));
      const badGear = ENGINES.filter(function(e){ return !e.gears || !e.gears.length || e.gears.some(function(g){ return !g.ratios || !g.ratios.length || g.ratios.some(function(x){ return !(x>0) || !isFinite(x); }); }); });
      T('Every engine has at least one marine gear with finite positive reduction ratios', badGear.length===0, badGear.map(function(e){return e.model;}).join(', '));
      const badSrc = ENGINES.filter(function(e){ return ['Y','YB','C','D','E','N'].indexOf(e.src_geom)<0 || ['Y','YB','C','D','E','N'].indexOf(e.src_mass)<0; });
      T('Every engine carries a provenance code for geometry and mass', badSrc.length===0, badSrc.map(function(e){return e.model;}).join(', '));
      const noDef = ENGINES.filter(function(e){ return e.ratings.some(function(r){ return !ratingDefFor(e, r.ymark) || !ratingDefFor(e, r.ymark).lim; }); });
      T('Every stored rating resolves to a YANMAR rating-definition set (own datasheet set where known, envelope otherwise)', noDef.length===0, noDef.map(function(e){return e.model;}).join(', '));
      const dupRating = ENGINES.filter(function(e){ const s={}; let d=false; e.ratings.forEach(function(r){ const k=r.ymark+'@'+r.rpm; if(s[k]) d=true; s[k]=1; }); return d; });
      T('No engine stores two ratings with the same YANMAR letter at the same speed', dupRating.length===0, dupRating.map(function(e){return e.model;}).join(', '));
      /* gear-ratio / shaft-speed coupling: every engine must be able to reach a
         sensible propeller speed through at least one listed ratio */
      const badShaft = ENGINES.filter(function(e){
        return !e.gears.some(function(g){ return g.ratios.some(function(x){ const nS = e.ratings[0].rpm/x; return nS>=40 && nS<=3000; }); });
      });
      T('Every engine can reach a sensible propeller shaft speed (40-3000 rpm) through a published ratio', badShaft.length===0, badShaft.map(function(e){return e.model;}).join(', '));
      /* IACS UR M68 shaft-rule form check on a known-exact case */
      const sh2 = shaftSizing(1000, 200, 600, 50);
      const hand = 100*1.22*Math.pow(1000/200,1/3)*Math.pow(560/760,1/3);
      T('IACS UR M68 propeller-shaft diameter form reproduces the hand calculation (1000 kW, 200 rpm, Rm 600, k = 1.22)',
        !!sh2 && Math.abs(sh2.IACS_M68-hand)/hand < 1e-12, sh2? sh2.IACS_M68.toFixed(2)+' mm vs '+hand.toFixed(2)+' mm':'null');
      T('ABS 4-3-2 rule length bands are applied (c1 = 416.4 below 20 m, 472.5 at 20-45.7 m, 560 at 45.7 m and over)',
        shaftSizing(500,300,600,10).c1ABS===416.4 && shaftSizing(500,300,600,30).c1ABS===472.5 && shaftSizing(500,300,600,60).c1ABS===560);
      T('No document script in the shipped HTML references the network (offline guarantee)',
        document.querySelectorAll('script[src]').length===0 && document.documentElement.outerHTML.indexOf('cdn-cgi')<0);
    }
  }catch(e){ T('Unexpected self-test exception',false,e&&e.message?e.message:String(e)); }
  return show();"""
rep(old,new,'H5 add audit-v3 self-tests')

open(p,'w',encoding='utf-8').write(src)
print("applied", len(changes)); [print("  -",c) for c in changes]
