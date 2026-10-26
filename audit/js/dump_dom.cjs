/* Headless (jsdom) dump of the *whole application* for the audit suite:
 * loads the shipped HTML, runs the presets and the edge-case selections
 * through the real UI entry points (applyPreset / gather / runSelection) and
 * prints JSON.  Usage:
 *   node audit/js/dump_dom.cjs app/yanmar_engine_propeller_selector.html
 * Requires the jsdom package (npm install in audit/js).
 */
const fs = require('fs');
const path = require('path');

function findJsdom() {
  const cands = [path.join(__dirname, 'node_modules', 'jsdom'),
                 path.join(__dirname, '..', '..', 'tests', 'node_modules', 'jsdom'),
                 path.join(__dirname, '..', '..', '..', 'audit_work', 'node_modules', 'jsdom'),
                 '/home/user/audit_work/node_modules/jsdom'];
  for (const c of cands) { if (fs.existsSync(c)) return require(c); }
  throw new Error('jsdom not installed: run `npm install` in audit/js');
}
const { JSDOM } = findJsdom();

const htmlPath = process.argv[2];
let html = fs.readFileSync(htmlPath, 'utf8');
/* Defensive: strip any injected network bootstrap (v2 shipped one). */
html = html.replace(/<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument[\s\S]*?<\/script>/, '');

const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/' });
const w = dom.window;
w.Element.prototype.scrollIntoView = function () {};

function runPreset(key) {
  w.applyPreset(key);
  const g = w.gather();
  if (g.errors) return { id: key, gatherErrors: g.errors };
  const o = w.runSelection(g.inp);
  const rec = { id: key, ok: !!o.ok, closest: !!o.closest,
                inp: { Vs: g.inp.Vs, etaShaft: g.inp.etaShaft, etaGear: g.inp.etaGear,
                       seaMargin: g.inp.seaMargin, nProps: g.inp.nProps,
                       maxLoadHard: g.inp.maxLoadHard, hull: g.inp.hull,
                       DmaxUse: g.inp.DmaxUse, Dmin: g.inp.Dmin },
                errors: (o.errors || []).map(String) };
  if (o.res) {
    rec.res = { method: o.res.method, Rtotal: o.res.Rtotal, PE: o.res.PE,
                domainStatus: o.res.domainStatus, governing: o.res.governing,
                voRatio: o.res.voRatio, S: o.res.S, Fn: o.res.Fn, Rn: o.res.Rn,
                formK: o.res.formK };
  }
  if (o.primary) {
    const c = o.primary;
    rec.primary = { model: c.eng.model, ymark: c.rating.ymark, kW: c.rating.kW,
      rpm: c.rating.rpm, duty: c.rating.duty, gear: c.gearModel, ratio: c.gear,
      nShaft: c.nShaft, load: c.load, PB: c.PB, PD: c.PD, nEng: c.nEng, PE: (rec.res ? rec.res.PE : null),
      w: c.w, t: c.t, etaR: c.etaR, etaS: c.etaS, etaG: c.etaG, etaD: c.etaD,
      etaO: (c.prop ? c.prop.eta : null), D: (c.prop ? c.prop.D : null),
      PDprop: (c.prop ? c.prop.PD : null), J: (c.prop ? c.prop.J : null),
      EAR: (c.prop ? c.prop.EAR : null), EARreq: (c.prop ? c.prop.EARreq : null),
      Z: (c.prop ? c.prop.Z : null), KT: (c.prop ? c.prop.KT : null),
      KQ: (c.prop ? c.prop.KQ : null), tauC: (c.prop ? c.prop.tauC : null),
      tauAct: (c.prop ? c.prop.tauAct : null), cavOK: (c.prop ? c.prop.cavOK : null),
      tipOK: (c.prop ? c.prop.tipOK : null), Vtip: (c.prop ? c.prop.Vtip : null),
      PDatLimit: (c.prop ? !!c.prop.PDatLimit : null),
      status: c.status, installedMass: c.installedMass,
      checks: (c.checks || []).map(function (k) { return { name: k.name, status: k.status }; }),
      installedBasis: (c.massInfo ? c.massInfo.basis : null),
      underLoaded: !!c.underLoaded, violations: (c.violations || []).map(function (v) { return v.text; }),
      engineLoadWithinHardLimit: c.load <= g.inp.maxLoadHard };
  }
  rec.rejectedCount = (o.rejected || []).length;
  rec.rejected = (o.rejected || []).slice(0, 40).map(function (r) {
    return { model: r.model, ymark: r.ymark, kW: r.kW, reason: r.reason, dutyFail: !!r.dutyFail };
  });
  rec.alternates = (o.alternates || []).map(function (c) { return c.eng.model + ' ' + c.rating.ymark; });
  return rec;
}

setTimeout(main, 600);

function main(){
const presets = ['fishing_dhoni','bokkura','cargo_dhoni','ferry','speed_ferry','transfer','safari','dinghy','custom'];
const out = { presets: [], edge: [], selftest: null, fieldCount: 0 };

try {
  w.fullSelfTest();
  const lines = w.document.querySelector('#stOut').textContent.split('\n');
  const nPass = lines.filter(function (l) { return l.indexOf('PASS') === 0; }).length;
  const nFail = lines.filter(function (l) { return l.indexOf('FAIL') === 0; }).length;
  out.selftest = { total: nPass + nFail, pass: nPass, fail: nFail,
                   fails: lines.filter(function (l) { return l.indexOf('FAIL') === 0; }) };
} catch (e) { out.selftest = { error: String(e) }; }
out.fieldCount = w.document.querySelectorAll('.field').length;

presets.forEach(function (k) { try { out.presets.push(runPreset(k)); } catch (e) { out.presets.push({ id: k, threw: String(e) }); } });

/* edge cases built from presets by overrides on the gathered input */
function edge(id, preset, patch, checkFn) {
  try {
    w.applyPreset(preset);
    const g = w.gather();
    if (g.errors) { out.edge.push({ id: id, gatherErrors: g.errors }); return; }
    const inp = Object.assign({}, g.inp, patch);
    const o = w.runSelection(inp);
    out.edge.push({ id: id, ok: !!o.ok, closest: !!o.closest,
      errors: (o.errors || []).map(String),
      primary: o.primary ? { model: o.primary.eng.model, ymark: o.primary.rating.ymark,
        load: o.primary.load, status: o.primary.status,
        violations: (o.primary.violations || []).map(function (v) { return v.text; }) } : null,
      rejected: (o.rejected || []).length });
  } catch (e) { out.edge.push({ id: id, threw: String(e) }); }
}
edge('cargo-high-speed', 'cargo_dhoni', { Vs: 25 * 1852 / 3600 }, null);
edge('cargo-zero-speed', 'cargo_dhoni', { Vs: 0 }, null);
edge('cargo-no-days', 'cargo_dhoni', { daysYear: undefined }, null);
edge('dinghy-planing-25kn', 'dinghy', { Vs: 25 * 1852 / 3600 }, null);
edge('fishing-16h-330d', 'fishing_dhoni', { hoursDay: 16, daysYear: 330, tripNm: 60, pctCruise: 70 }, null);
edge('ferry-huge-tip', 'ferry', { tipMax: 20 }, null);
edge('ferry-cav-30', 'ferry', { backCavPct: 30 }, null);
edge('cargo-2props', 'cargo_dhoni', { props: 2 }, null);

process.stdout.write(JSON.stringify(out));
}
