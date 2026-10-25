/* Headless dump of the calculation core for the independent audit suite.
 * Loads audit/build/script_0.js in a vm context (no DOM required: the core
 * script is pure JavaScript) and prints a JSON document of every quantity the
 * Python reference needs.  Usage: node audit/js/dump_core.js <script_0.js>
 */
const fs = require('fs');
const vm = require('vm');
const path = process.argv[2];
const src = fs.readFileSync(path, 'utf8');
const ctx = {console, Math, JSON, isFinite, isNaN, Number, Array, Object, String,
             RangeError, Error, parseFloat, parseInt, Infinity, NaN};
vm.createContext(ctx);
const WANT = ['CONST','UNITS','ENGINES','ENGINE_MASS_DATA','RATING_DEFS','BS_KT','BS_KQ',
  'BS_RANGE','bsCoeffs','bSeries','evalPD','dKT_Rn','dKQ_Rn','propRn','burrillTauC',
  'burrillCheck','kellerEAR','ittc57','holtrop','holtropPropulsion','oortmerssen',
  'savitsky','designPropeller','shaftSizing','computeResistanceAt','solveCandidate',
  'runSelection','assessCandidate','dutyProfile','dutyCycleCheck','ratingDefFor',
  'installedMassOf','SFC_LOAD_CURVE','sfcAtLoad','SRC_INFO','pchip','defaultCm',
  'runBenchmarks','MIN_SENSIBLE_LOAD','SIZING_MIN_LOAD','PRESETS','powerOnlySuggestion'];
const tail = '\n;globalThis.__api={' + WANT.join(',') + '};';
vm.runInContext(src + tail, ctx);
const api = ctx.__api;
const G = 9.80665, KNOT = 1852/3600;

const out = {benchmarks: api.runBenchmarks(), engines: [], holtrop: [], savitsky: [],
             bseries: [], ittc: [], burrill: [], keller: [], shaft: [], misc: {}};

/* --- engine database ------------------------------------------------------ */
api.ENGINES.forEach(function(e){
  const rec = {model:e.model, series:e.series, cyl:e.cyl, bore:e.bore, stroke:e.stroke,
    disp:e.disp, dryMass:e.dryMass, src_mass:e.src_mass, src_geom:e.src_geom,
    src_gear:e.src_gear, dims:e.dims, codeVerified:e.codeVerified,
    gears:e.gears.map(function(g){ return {model:g.model, ratios:g.ratios, mass:(g.mass==null?null:g.mass)}; }),
    ratings:e.ratings.map(function(r){ return {ymark:r.ymark, duty:r.duty, kW:r.kW, rpm:r.rpm,
      sfc:r.sfc, src:r.src, src_sfc:r.src_sfc}; })};
  rec.installed = {};
  e.gears.forEach(function(g){
    let m=null; try{ m = api.installedMassOf(e, g.model); }catch(err){ m={error:String(err)}; }
    rec.installed[g.model]=m;
  });
  out.engines.push(rec);
});

/* --- Holtrop cases -------------------------------------------------------- */
const hulls = [
  {id:'HM82-PAPER', Lwl:205,B:32,T:10,vol:37500,Cp:0.5833,Cm:0.98,Cwp:0.75,lcb:-0.75,Abt:20,hB:4,At:16,Sapp:50,k2:1.50,Cstern:10,V:25},
  {id:'cargo_dhoni', Lwl:24,B:6.2,T:1.6,vol:212,Cp:0.62,Cm:0.96,Cwp:0.80,lcb:-1.2,Abt:0,hB:0,At:1.6,Sapp:3,k2:1.6,Cstern:0,V:9},
  {id:'ferry',       Lwl:28,B:7.2,T:1.75,vol:315,Cp:0.64,Cm:0.97,Cwp:0.82,lcb:-1.4,Abt:0,hB:0,At:2.0,Sapp:4,k2:1.6,Cstern:0,V:10},
  {id:'tanker-like', Lwl:180,B:30,T:10.5,vol:46000,Cp:0.81,Cm:0.98,Cwp:0.86,lcb:-1.5,Abt:25,hB:4,At:0,Sapp:40,k2:1.4,Cstern:0,V:14},
  {id:'container',   Lwl:150,B:23,T:8.5,vol:17000,Cp:0.65,Cm:0.97,Cwp:0.79,lcb:-1.0,Abt:10,hB:3,At:8,Sapp:25,k2:1.35,Cstern:0,V:16},
  {id:'tug',         Lwl:30,B:10,T:4.0,vol:1000,Cp:0.60,Cm:0.90,Cwp:0.78,lcb:-1.0,Abt:0,hB:0,At:0,Sapp:8,k2:1.5,Cstern:0,V:6},
  {id:'slender',     Lwl:60,B:8,T:2.5,vol:900,Cp:0.62,Cm:0.92,Cwp:0.76,lcb:-1.0,Abt:0,hB:0,At:3,Sapp:10,k2:1.5,Cstern:0,V:8},
  {id:'lowFn',       Lwl:100,B:16,T:5,vol:6000,Cp:0.70,Cm:0.95,Cwp:0.80,lcb:-1.0,Abt:0,hB:0,At:0,Sapp:20,k2:1.5,Cstern:0,V:3.5},
  {id:'highFn',      Lwl:40,B:9,T:2.2,vol:650,Cp:0.60,Cm:0.90,Cwp:0.75,lcb:-1.0,Abt:0,hB:0,At:4,Sapp:8,k2:1.5,Cstern:0,V:9.5},
  {id:'fullCb',      Lwl:120,B:20,T:7,vol:15000,Cp:0.83,Cm:0.99,Cwp:0.88,lcb:-1.5,Abt:0,hB:0,At:0,Sapp:20,k2:1.5,Cstern:0,V:11}
];
hulls.forEach(function(h){
  const V = h.V*KNOT;
  const r = api.holtrop({Lwl:h.Lwl,B:h.B,T:h.T,Tf:h.T,Ta:h.T,vol:h.vol,Cp:h.Cp,Cm:h.Cm,Cwp:h.Cwp,
    lcb:h.lcb,Abt:h.Abt,hB:h.hB,At:h.At,S:null,Sapp:h.Sapp,k2:h.k2,Cstern:h.Cstern,Aair:0,Cair:0.8,
    rho:1025,nu:1.188e-6,V:V});
  out.holtrop.push({id:h.id, input:h, error:(r.error||null),
    S:r.S,Cf:r.Cf,Rn:r.Rn,Fn:r.Fn,formK:r.formK,Rf:r.Rf,RfForm:r.RfForm,Rapp:r.Rapp,Rw:r.Rw,
    Rb:r.Rb,Rtr:r.Rtr,Ra:r.Ra,Ca:r.Ca,Rtotal:r.Rtotal,PE:r.PE});
});

/* --- Savitsky cases ------------------------------------------------------- */
const planing = [
  {id:'shoemaker-18.01kn', W:80*0.45359237*G, V:18.01, B:16*0.0254, beta:20, LCG:18.5*0.0254, rho:1000, nu:1.0e-6},
  {id:'shoemaker-20.92kn', W:80*0.45359237*G, V:20.92, B:16*0.0254, beta:20, LCG:18.5*0.0254, rho:1000, nu:1.0e-6},
  {id:'speed_ferry', W:9000*G, V:28*KNOT, B:3.2, beta:18, LCG:4.4, rho:1025, nu:1.19e-6},
  {id:'transfer',    W:12000*G, V:25*KNOT, B:3.0, beta:16, LCG:4.6, rho:1025, nu:1.19e-6},
  {id:'dinghy',      W:1200*G, V:22*KNOT, B:1.6, beta:14, LCG:1.9, rho:1025, nu:1.19e-6},
  {id:'deep-v',      W:6000*G, V:30*KNOT, B:2.6, beta:24, LCG:3.3, rho:1025, nu:1.19e-6}
];
planing.forEach(function(p){
  const r = api.savitsky({W:p.W,V:p.V*KNOT,B:p.B,beta:p.beta,LCG:p.LCG,rho:p.rho,nu:p.nu,
    Sapp:0,k2:1.5,Aair:0,Cair:0.8,fixedTrim:null});
  out.savitsky.push({id:p.id, input:p, error:(r.error||null), lam:r.lambda, tau:r.tau,
    CLb:r.CLb, Cv:r.Cv, Vm:r.Vm, Df:r.Df, Rbare:r.Rbare, Rtotal:r.Rtotal, Cf:r.Cf,
    Sb:r.Sb, rnFloored:r.rnFloored});
});

/* --- B-series evaluation -------------------------------------------------- */
const pts = [[0.5,1.0,0.70,4,2e6],[0.6,0.9,0.55,4,2e6],[0.3,1.2,0.85,5,2e6],
             [0.8,1.0,0.70,4,2e6],[0.2,0.6,0.50,3,2e6],[1.0,1.4,1.05,5,2e6],
             [0.7,0.8,0.65,6,2e6],[0.45,1.1,0.75,7,2e7]];
pts.forEach(function(q){
  const r = api.bSeries(q[0],q[1],q[2],q[3],q[4]);
  out.bseries.push({J:q[0],PD:q[1],EAR:q[2],Z:q[3],Rn:q[4],KT:r.KT,KQ:r.KQ,eta:r.eta});
});
out.misc.bsKT = api.BS_KT; out.misc.bsKQ = api.BS_KQ; out.misc.bsRange = api.BS_RANGE;

/* --- friction line, cavitation, shaft ------------------------------------ */
[1e5,1e6,1e7,1e8,1e9,2.2193e9].forEach(function(rn){
  let v=null; try{ v=api.ittc57(rn); }catch(e){ v=null; }
  out.ittc.push({Rn:rn,Cf:v});
});
[[20000,5,3,1.2,0.9,1.5,1025,5,0.70],[400000,4,5,0.45,0.70,1.0,1025,5,0.70],
 [80000,6,3,1.0,1.1,2.0,1025,5,0.55],[150000,4,4,0.8,0.8,1.2,1025,2.5,0.65]
].forEach(function(c){
  out.burrill.push({T:c[0],Va:c[1],n:c[2],D:c[3],PD:c[4],h:c[5],rho:c[6],C:c[7],EAR:c[8],
    r:api.burrillCheck(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8]),
    keller:api.kellerEAR(c[0],c[5],c[3],c[2],c[6],1)});
});
[[1000,200,600,50],[500,300,600,10],[2500,180,700,30],[200,900,400,8]].forEach(function(s){
  out.shaft.push({P:s[0],n:s[1],Rm:s[2],L:s[3],r:api.shaftSizing(s[0],s[1],s[2],s[3])});
});

/* --- designPropeller on fixed targets (deterministic) -------------------- */
out.design = [];
[[40000,4,5,3.5,0.9,1.2],[120000,5,3,4.0,1.1,1.1],[8000,6,4,2.5,0.7,1.0]].forEach(function(d){
  const r = api.designPropeller({T:d[0],Va:d[1],n:d[2],Dmin:0.3*0+ (d[3]*0.2),Dmax:d[3],Zlist:[3,4,5],
    EARlist:[0.50,0.70],rho:1025,nu:1.19e-6,h:d[4],nProps:1,backCavPct:5,tipMax:80});
  out.design.push({args:d, ok:!!r.ok, best:(r.best||null), error:r.error||null});
});
process.stdout.write(JSON.stringify(out));
