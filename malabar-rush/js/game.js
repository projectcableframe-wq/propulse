/* ============================================================
   MALABAR RUSH — Episode 1: Thamarassery Churam
   Created by Hadee Mohammed
   A procedural 3D arcade racing game (Three.js r147 UMD).
   All assets procedural — zero external files, zero missing-asset errors.
   ============================================================ */
'use strict';

/* ---------------- 1. Utilities ---------------- */
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const smoothstep = (t) => { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };
function fmtTime(t) {
  if (!t || t <= 0) return '--:--.--';
  const m = Math.floor(t / 60), s = Math.floor(t % 60), c = Math.floor((t * 100) % 100);
  return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s + '.' + (c < 10 ? '0' : '') + c;
}
function fmtMoney(n) { return '\u20B9' + Math.round(n).toLocaleString('en-IN'); }

/* ---------------- 2. Save system ---------------- */
const SAVE_KEY = 'malabarRushSave_v1';
const DEFAULT_SAVE = {
  money: 0, owned: ['k10'], selected: 'k10', bestLap: 0,
  upgrades: {}, // {carId: {engine:1, turbo:0, tyres:2}}
  settings: { quality: 'MED', weather: 'CLEAR', time: 'SUNSET', sound: 'ON', lang: 'EN' }
};
let save = loadSave();
function loadSave() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return JSON.parse(JSON.stringify(DEFAULT_SAVE));
    const data = JSON.parse(raw);
    return Object.assign(JSON.parse(JSON.stringify(DEFAULT_SAVE)), data);
  } catch (e) { return JSON.parse(JSON.stringify(DEFAULT_SAVE)); }
}
function persist() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(save)); } catch (e) {} }

/* ---------------- 3. i18n ---------------- */
const I18N = {
  EN: {},
  ML: {
    tagline: 'ഒരു സംസ്ഥാനം. പതിനാല് ജില്ലകള്‍. പരിധിയില്ലാ വേഗം.',
    credit: 'എപ്പിസോഡ് 1 · താമരശ്ശേരി ചുരം · സൃഷ്ടാവ്: ഹദീ മുഹമ്മദ്',
    startRace: '🏁 റേസ് തുടങ്ങുക — ചുരം സര്‍ക്യൂട്ട്',
    timeTrial: '⏱ ടൈം ട്രയല്‍',
    freeRoam: '🌴 ഫ്രീ റോം — കറങ്ങാം',
    garage: '🔧 ഗ്യാരേജ്',
    settings: '⚙ ക്രമീകരണങ്ങള്‍',
    about: 'ℹ കുറിപ്പുകളും റോഡ്‌മാപ്പും',
    back: '← മടക്കം',
    paused: '⏸ താല്‍ക്കാലിക വിരാമം',
    resume: '▶ തുടരുക',
    restart: '↺ വീണ്ടും തുടങ്ങുക',
    mainMenu: '🏠 മെയിന്‍ മെനു',
    garageNote: 'പ്രചോദനം ഉള്‍ക്കൊണ്ട വാഹനങ്ങള്‍ — യഥാര്‍ത്ഥ ഡിസൈനുകള്‍. കണക്കുകള്‍ ഗെയിം-അഡ്ജസ്റ്റഡ് ആണ്.',
    quality: 'ഗ്രാഫിക്സ് നിലവാരം',
    weather: 'കാലാവസ്ഥ',
    timeOfDay: 'ദിവസത്തിന്റെ സമയം',
    sound: 'ശബ്ദം',
    language: 'ഭാഷ',
    controlsNote: 'കണ്ട്രോളുകള്‍: WASD / ആരോ കീകള്‍ · Space ഹാന്‍ഡ്‌ബ്രേക്ക് · Shift നൈട്രോ · C ക്യാമറ · R റീസെറ്റ് · Esc പോസ്',
    resetSave: 'സേവ് റീസെറ്റ്',
    position: 'സ്ഥാനം',
    bestLap: 'മികച്ച ലാപ്പ്',
    totalTime: 'ആകെ സമയം',
    prize: 'സമ്മാനം',
    raceAgain: '🏁 വീണ്ടും റേസ്'
  }
};
function applyLang() {
  const dict = I18N[save.settings.lang] || {};
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (!el.dataset.enText) el.dataset.enText = el.textContent;
    el.textContent = (save.settings.lang === 'EN') ? el.dataset.enText : (dict[key] || el.dataset.enText);
  });
}

/* ---------------- 4. Audio (all procedural) ---------------- */
const AudioSys = {
  ctx: null, master: null, engineOsc: null, engineOsc2: null, engineGain: null,
  windGain: null, noiseBuf: null, muted: save.settings.sound === 'OFF',
  init() {
    if (this.ctx) return;
    try {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      this.ctx = new AC();
      this.master = this.ctx.createGain();
      this.master.gain.value = this.muted ? 0 : 0.55;
      this.master.connect(this.ctx.destination);
      // engine
      this.engineOsc = this.ctx.createOscillator(); this.engineOsc.type = 'sawtooth';
      this.engineOsc2 = this.ctx.createOscillator(); this.engineOsc2.type = 'square';
      const lp = this.ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 720;
      this.engineGain = this.ctx.createGain(); this.engineGain.gain.value = 0;
      this.engineOsc.connect(lp); this.engineOsc2.connect(lp);
      lp.connect(this.engineGain); this.engineGain.connect(this.master);
      this.engineOsc.frequency.value = 55; this.engineOsc2.frequency.value = 27;
      this.engineOsc.start(); this.engineOsc2.start();
      // wind noise
      const nb = this.ctx.createBuffer(1, this.ctx.sampleRate * 2, this.ctx.sampleRate);
      const d = nb.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      this.noiseBuf = nb;
      const wind = this.ctx.createBufferSource(); wind.buffer = nb; wind.loop = true;
      const wf = this.ctx.createBiquadFilter(); wf.type = 'bandpass'; wf.frequency.value = 480;
      this.windGain = this.ctx.createGain(); this.windGain.gain.value = 0;
      wind.connect(wf); wf.connect(this.windGain); this.windGain.connect(this.master);
      wind.start();
    } catch (e) {}
  },
  resume() { this.init(); if (this.ctx && this.ctx.state === 'suspended') { try { this.ctx.resume(); } catch (e) {} } },
  setMuted(m) {
    this.muted = m;
    if (this.master) this.master.gain.value = m ? 0 : 0.55;
  },
  engine(speed, throttle, nitro) {
    if (!this.ctx || this.muted) return;
    const f = 46 + speed * 2.3 + throttle * 14 + (nitro ? 24 : 0);
    this.engineOsc.frequency.value = f;
    this.engineOsc2.frequency.value = f * 0.5;
    this.engineGain.gain.value = 0.055 + throttle * 0.05 + speed * 0.0006;
    this.windGain.gain.value = clamp(speed / 900, 0, 0.09);
  },
  silence() {
    if (!this.ctx) return;
    this.engineGain.gain.value = 0; this.windGain.gain.value = 0;
  },
  blip(freq, dur, type, vol) {
    if (!this.ctx || this.muted) return;
    try {
      const o = this.ctx.createOscillator(), g = this.ctx.createGain();
      o.type = type || 'sine'; o.frequency.value = freq || 660;
      g.gain.value = vol || 0.16; g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + (dur || 0.18));
      o.connect(g); g.connect(this.master); o.start(); o.stop(this.ctx.currentTime + (dur || 0.18) + 0.02);
    } catch (e) {}
  },
  thump() {
    if (!this.ctx || this.muted) return;
    try {
      const s = this.ctx.createBufferSource(); s.buffer = this.noiseBuf;
      const f = this.ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 320;
      const g = this.ctx.createGain(); g.gain.value = 0.4;
      g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.22);
      s.connect(f); f.connect(g); g.connect(this.master); s.start(); s.stop(this.ctx.currentTime + 0.24);
    } catch (e) {}
  },
  whoosh() {
    if (!this.ctx || this.muted) return;
    try {
      const s = this.ctx.createBufferSource(); s.buffer = this.noiseBuf;
      const f = this.ctx.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 1200;
      f.frequency.exponentialRampToValueAtTime(260, this.ctx.currentTime + 0.5);
      const g = this.ctx.createGain(); g.gain.value = 0.3;
      g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.55);
      s.connect(f); f.connect(g); g.connect(this.master); s.start(); s.stop(this.ctx.currentTime + 0.6);
    } catch (e) {}
  }
};

/* ---------------- 5. Input ---------------- */
const input = { up: false, down: false, left: false, right: false, hand: false, nitro: false };
const KEYMAP = {
  ArrowUp: 'up', KeyW: 'up', ArrowDown: 'down', KeyS: 'down',
  ArrowLeft: 'left', KeyA: 'left', ArrowRight: 'right', KeyD: 'right',
  Space: 'hand', ShiftLeft: 'nitro', ShiftRight: 'nitro'
};
document.addEventListener('keydown', e => {
  if (KEYMAP[e.code]) { input[KEYMAP[e.code]] = true; e.preventDefault(); }
  if (e.code === 'KeyC') cycleCamera();
  if (e.code === 'KeyR') resetCar();
  if (e.code === 'Escape') togglePause();
});
document.addEventListener('keyup', e => {
  if (KEYMAP[e.code]) { input[KEYMAP[e.code]] = false; e.preventDefault(); }
});
function bindTouch(id, key) {
  const el = document.getElementById(id);
  if (!el) return;
  const on = e => { e.preventDefault(); input[key] = true; AudioSys.resume(); };
  const off = e => { e.preventDefault(); input[key] = false; };
  el.addEventListener('touchstart', on, { passive: false });
  el.addEventListener('touchend', off, { passive: false });
  el.addEventListener('touchcancel', off, { passive: false });
  el.addEventListener('mousedown', on);
  el.addEventListener('mouseup', off);
  el.addEventListener('mouseleave', off);
}
['t-left:left', 't-right:right', 't-gas:up', 't-brake:down', 't-nitro:nitro', 't-hand:hand']
  .forEach(pair => { const p = pair.split(':'); bindTouch(p[0], p[1]); });

/* ---------------- 6. Scene / renderer / sky / lights ---------------- */
const canvas = document.getElementById('game-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(66, window.innerWidth / window.innerHeight, 0.3, 6000);
camera.position.set(0, 10, -20);

const hemi = new THREE.HemisphereLight(0xbfe3ff, 0x2d4a2e, 0.65);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff2dd, 1.15);
sun.position.set(60, 120, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 10; sun.shadow.camera.far = 500;
sun.shadow.camera.left = -110; sun.shadow.camera.right = 110;
sun.shadow.camera.top = 110; sun.shadow.camera.bottom = -110;
scene.add(sun); scene.add(sun.target);

/* Sky dome (vertex-colored gradient) */
const skyGeo = new THREE.SphereGeometry(3600, 24, 14);
const skyColors = new Float32Array(skyGeo.attributes.position.count * 3);
skyGeo.setAttribute('color', new THREE.BufferAttribute(skyColors, 3));
const skyMat = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false });
const skyMesh = new THREE.Mesh(skyGeo, skyMat);
scene.add(skyMesh);

function paintSky(topHex, horizonHex) {
  const top = new THREE.Color(topHex), hor = new THREE.Color(horizonHex), tmp = new THREE.Color();
  const pos = skyGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const t = smoothstep((pos.getY(i) / 3600) * 1.35);
    tmp.copy(hor).lerp(top, t);
    skyColors[i * 3] = tmp.r; skyColors[i * 3 + 1] = tmp.g; skyColors[i * 3 + 2] = tmp.b;
  }
  skyGeo.attributes.color.needsUpdate = true;
}

const fogColor = new THREE.Color(0xcfe3f2);
scene.fog = new THREE.Fog(fogColor.getHex(), 80, 1400);

/* Time-of-day + weather presets */
const PRESETS = {
  DAY:    { skyTop: 0x2f6fd0, skyHor: 0xbfe3ff, sunCol: 0xfff2dd, sunInt: 1.25, hemiInt: 0.72, fog: 0xcfe3f2, fogFar: 1500, exposure: 1.08 },
  SUNSET: { skyTop: 0x27346e, skyHor: 0xff9d5c, sunCol: 0xff8c42, sunInt: 1.18, hemiInt: 0.5,  fog: 0xe8a878, fogFar: 1350, exposure: 1.02 },
  NIGHT:  { skyTop: 0x050a1e, skyHor: 0x16234d, sunCol: 0x4a5f9e, sunInt: 0.4,  hemiInt: 0.22, fog: 0x0e1830, fogFar: 1050, exposure: 0.92 }
};
const WEATHER = {
  CLEAR: { fogMul: 1,    dark: 1,    rain: false },
  MIST:  { fogMul: 3.1,  dark: 0.88, rain: false },
  RAIN:  { fogMul: 2.1,  dark: 0.78, rain: true  }
};

function applyEnvironment() {
  const p = PRESETS[save.settings.time] || PRESETS.SUNSET;
  const w = WEATHER[save.settings.weather] || WEATHER.CLEAR;
  paintSky(p.skyTop, p.skyHor);
  sun.color.setHex(p.sunCol); sun.intensity = p.sunInt * w.dark;
  hemi.intensity = p.hemiInt * w.dark;
  fogColor.setHex(p.fog);
  scene.fog.color.copy(fogColor);
  scene.fog.far = p.fogFar / w.fogMul;
  scene.fog.near = 40;
  renderer.toneMappingExposure = p.exposure * (0.92 + 0.08 * w.dark);
  rainPoints.visible = !!w.rain;
  if (headlightGroup) headlightGroup.visible = (save.settings.time === 'NIGHT');
}

/* ---------------- 7. Terrain ---------------- */
function terrainH(x, z) {
  return 26 * Math.sin(x * 0.0036) * Math.cos(z * 0.0041)
       + 13 * Math.sin(x * 0.0098 + 1.4) * Math.sin(z * 0.0087 + 0.6)
       + 6  * Math.sin(x * 0.021 + 2.1) * Math.cos(z * 0.019)
       + 3  * Math.sin(x * 0.043) * Math.sin(z * 0.039);
}
const TERRAIN_SIZE = 1900, TERRAIN_SEG = 118;
const terrainGeo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, TERRAIN_SEG, TERRAIN_SEG);
terrainGeo.rotateX(-Math.PI / 2);

/* ---------------- 8. Road (Thamarassery Churam circuit) ---------------- */
const ROAD_PTS = [
  [0, 0, 0], [130, 6, -50], [235, 20, -135], [272, 34, -248], [188, 47, -312],
  [58, 55, -338], [-86, 57, -312], [-206, 49, -244], [-268, 36, -138], [-232, 25, -18],
  [-306, 16, 88], [-262, 8, 192], [-132, 4, 238], [16, 3, 226], [132, 2, 158], [168, 1, 58]
];
const roadCurve = new THREE.CatmullRomCurve3(
  ROAD_PTS.map(p => new THREE.Vector3(p[0], p[1], p[2])), true, 'catmullrom', 0.5
);
const N_SAMPLES = 800;
const samples = [];       // {pos, tan, side, curv}
const curveLen = roadCurve.getLength();
const segLen = curveLen / N_SAMPLES;
{
  for (let i = 0; i < N_SAMPLES; i++) {
    const u = i / N_SAMPLES;
    const pos = roadCurve.getPointAt(u);
    const tan = roadCurve.getTangentAt(u).normalize();
    const side = new THREE.Vector3().crossVectors(tan, new THREE.Vector3(0, 1, 0)).normalize();
    samples.push({ pos, tan, side, curv: 0 });
  }
  for (let i = 0; i < N_SAMPLES; i++) {
    const a = samples[(i - 1 + N_SAMPLES) % N_SAMPLES].tan, b = samples[(i + 1) % N_SAMPLES].tan;
    samples[i].curv = a.angleTo(b);
  }
}

function nearestRoad(x, z) {
  let best = 0, bestD = Infinity;
  for (let i = 0; i < N_SAMPLES; i++) {
    const dx = samples[i].pos.x - x, dz = samples[i].pos.z - z;
    const d = dx * dx + dz * dz;
    if (d < bestD) { bestD = d; best = i; }
  }
  return { idx: best, dist: Math.sqrt(bestD), pos: samples[best].pos, side: samples[best].side, tan: samples[best].tan };
}

/* Flatten terrain near the road (load-time, once) */
{
  const posAttr = terrainGeo.attributes.position;
  for (let i = 0; i < posAttr.count; i++) {
    const x = posAttr.getX(i), z = posAttr.getZ(i);
    let h = terrainH(x, z), bestD = Infinity, bestY = h;
    for (let s = 0; s < N_SAMPLES; s += 4) {
      const dx = samples[s].pos.x - x, dz = samples[s].pos.z - z;
      const d = dx * dx + dz * dz;
      if (d < bestD) { bestD = d; bestY = samples[s].pos.y; }
    }
    const dist = Math.sqrt(bestD);
    if (dist < 46) {
      const t = smoothstep(dist / 46);
      h = lerp(bestY - 0.12, h, t);
    }
    posAttr.setY(i, h);
  }
  terrainGeo.computeVertexNormals();
}
/* Terrain vertex colors: greens by height */
{
  const posAttr = terrainGeo.attributes.position;
  const colors = new Float32Array(posAttr.count * 3);
  const cLow = new THREE.Color(0x2e7d4f), cMid = new THREE.Color(0x1e5c38), cHigh = new THREE.Color(0x8fbf7a), tmp = new THREE.Color();
  for (let i = 0; i < posAttr.count; i++) {
    const h = posAttr.getY(i);
    if (h < 12) tmp.copy(cLow).lerp(cMid, smoothstep(h / 12));
    else tmp.copy(cMid).lerp(cHigh, smoothstep((h - 12) / 45));
    colors[i * 3] = tmp.r; colors[i * 3 + 1] = tmp.g; colors[i * 3 + 2] = tmp.b;
  }
  terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
}
const terrainMesh = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, metalness: 0 }));
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);

/* Road ribbon */
function buildRibbon(width, yOff, colorHex, dashGap) {
  const verts = [], idxs = [], cols = [];
  const c = new THREE.Color(colorHex);
  const n = N_SAMPLES;
  for (let i = 0; i <= n; i++) {
    const s = samples[i % n];
    const L = s.pos.clone().addScaledVector(s.side, -width);
    const R = s.pos.clone().addScaledVector(s.side, width);
    L.y += yOff; R.y += yOff;
    verts.push(L.x, L.y, L.z, R.x, R.y, R.z);
    for (let k = 0; k < 2; k++) cols.push(c.r, c.g, c.b);
    if (dashGap && (i % dashGap) < dashGap * 0.55) {
      // handled below via index skip
    }
    if (i > 0) {
      const a = (i - 1) * 2, b = a + 1, cc = i * 2, d = cc + 1;
      const skip = dashGap && (i % dashGap) >= dashGap * 0.55;
      if (!skip) idxs.push(a, b, cc, b, d, cc);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  g.setIndex(idxs);
  return new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.82, metalness: 0.06, side: THREE.DoubleSide }));
}
const roadMesh = buildRibbon(6.2, 0.06, 0x2b2f36, 0);
roadMesh.receiveShadow = true;
scene.add(roadMesh);
const lineCenter = buildRibbon(0.16, 0.11, 0xe8e2c8, 14);
const lineL = buildRibbon(0.14, 0.1, 0xd8d8d8, 0);
lineL.position.addScaledVector(new THREE.Vector3(1, 0, 0), 0); // keep
scene.add(lineCenter);
/* edge lines as thin offset ribbons built manually */
function buildEdgeLines() {
  const mk = (offset, colorHex) => {
    const verts = [], idxs = [], cols = [], c = new THREE.Color(colorHex);
    for (let i = 0; i <= N_SAMPLES; i++) {
      const s = samples[i % N_SAMPLES];
      const L = s.pos.clone().addScaledVector(s.side, offset - 0.12);
      const R = s.pos.clone().addScaledVector(s.side, offset + 0.12);
      L.y += 0.1; R.y += 0.1;
      verts.push(L.x, L.y, L.z, R.x, R.y, R.z);
      cols.push(c.r, c.g, c.b, c.r, c.g, c.b);
      if (i > 0) { const a = (i - 1) * 2, b = a + 1, cc = i * 2, d = cc + 1; idxs.push(a, b, cc, b, d, cc); }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    g.setIndex(idxs);
    return new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.7 }));
  };
  scene.add(mk(5.4, 0xe6e6e6), mk(-5.4, 0xe6e6e6));
}
buildEdgeLines();
scene.add(lineL === null ? lineCenter : lineCenter); // center already added

/* Guardrail posts + rails */
{
  const postGeo = new THREE.BoxGeometry(0.22, 1.1, 0.22);
  const postMat = new THREE.MeshStandardMaterial({ color: 0x9aa2ab, metalness: 0.5, roughness: 0.5 });
  const count = Math.floor(N_SAMPLES / 10) * 2;
  const posts = new THREE.InstancedMesh(postGeo, postMat, count);
  const m4 = new THREE.Matrix4();
  let k = 0;
  for (let i = 0; i < N_SAMPLES; i += 10) {
    for (const sgn of [1, -1]) {
      const s = samples[i];
      const p = s.pos.clone().addScaledVector(s.side, sgn * 6.85);
      m4.makeTranslation(p.x, p.y + 0.62, p.z);
      posts.setMatrixAt(k++, m4);
    }
  }
  posts.instanceMatrix.needsUpdate = true;
  scene.add(posts);
  // rails
  const railVerts = [], railIdxs = [], railCols = [], rc = new THREE.Color(0xb7bec7);
  for (const sgn of [1, -1]) {
    const base = railVerts.length / 3;
    for (let i = 0; i <= N_SAMPLES; i += 2) {
      const s = samples[i % N_SAMPLES];
      const p = s.pos.clone().addScaledVector(s.side, sgn * 6.85);
      railVerts.push(p.x, p.y + 1.15, p.z, p.x, p.y + 0.72, p.z);
      railCols.push(rc.r, rc.g, rc.b, rc.r, rc.g, rc.b);
      if (i > 0) {
        const a = base + (i - 2) * 2, b = a + 1, cc = base + i * 2, d = cc + 1;
        railIdxs.push(a, b, cc, b, d, cc);
      }
    }
  }
  const rg = new THREE.BufferGeometry();
  rg.setAttribute('position', new THREE.Float32BufferAttribute(railVerts, 3));
  rg.setAttribute('color', new THREE.Float32BufferAttribute(railCols, 3));
  rg.setIndex(railIdxs);
  scene.add(new THREE.Mesh(rg, new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 0.6, roughness: 0.4, side: THREE.DoubleSide })));
}

/* Checkpoint gates + start arch */
const GATES = [0, 140, 280, 420, 560, 700];
const gateMeshes = [];
function buildGate(idx, label, big) {
  const s = samples[idx];
  const group = new THREE.Group();
  const pillarMat = new THREE.MeshStandardMaterial({ color: 0x22282e, metalness: 0.4, roughness: 0.5 });
  const bannerMat = new THREE.MeshStandardMaterial({
    color: big ? 0xe8b64c : 0x178a5c, emissive: big ? 0x6b4e12 : 0x0c3c26,
    emissiveIntensity: 0.7, metalness: 0.3, roughness: 0.4
  });
  const h = big ? 8.2 : 6.6;
  for (const sgn of [1, -1]) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(0.7, h, 0.7), pillarMat);
    const w = s.pos.clone().addScaledVector(s.side, sgn * 7);
    p.position.set(w.x, w.y + h / 2, w.z);
    p.castShadow = true;
    group.add(p);
  }
  const banner = new THREE.Mesh(new THREE.BoxGeometry(14.6, 1.5, 0.45), bannerMat);
  banner.position.set(s.pos.x, s.pos.y + h - 0.7, s.pos.z);
  banner.rotation.y = Math.atan2(s.tan.x, s.tan.z) + Math.PI / 2;
  group.add(banner);
  scene.add(group);
  gateMeshes.push({ idx, group, banner });
}
GATES.forEach((g, i) => buildGate(g, 'CP' + i, g === 0));

/* Signboards with canvas texture (EN + Malayalam) */
function makeSign(text1, text2) {
  const cv = document.createElement('canvas');
  cv.width = 512; cv.height = 256;
  const ctx = cv.getContext('2d');
  ctx.fillStyle = '#0e5c3f'; ctx.fillRect(0, 0, 512, 256);
  ctx.strokeStyle = '#e8b64c'; ctx.lineWidth = 10; ctx.strokeRect(10, 10, 492, 236);
  ctx.fillStyle = '#f5e9c8'; ctx.textAlign = 'center';
  ctx.font = 'bold 52px Arial'; ctx.fillText(text1, 256, 108);
  ctx.font = '42px Arial'; ctx.fillText(text2, 256, 180);
  const tex = new THREE.CanvasTexture(cv);
  tex.encoding = THREE.sRGBEncoding;
  return new THREE.Mesh(new THREE.PlaneGeometry(9, 4.5),
    new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide }));
}
[[52, 'THAMARASSERY CHURAM', '\u0D24\u0D3E\u0D2E\u0D30\u0D36\u0D4D\u0D36\u0D47\u0D30\u0D3F \u0D1A\u0D41\u0D30\u0D02', 1],
 [252, 'HAIRPIN BENDS AHEAD', '\u0D24\u0D3F\u0D30\u0D36\u0D4D\u0D36\u0D41\u0D15\u0D33\u0D4D\u200D \u0D36\u0D4D\u0D30\u0D26\u0D4D\u0D27', -1],
 [448, 'WAYANAD \u2192 36 KM', '\u0D35\u0D2F\u0D28\u0D3E\u0D21\u0D4D \u2192 36 \u0D15\u0D3F\u0D2E\u0D3F', 1],
 [640, 'KOZHIKODE \u2192 18 KM', '\u0D15\u0D4B\u0D34\u0D3F\u0D15\u0D4D\u0D15\u0D4B\u0D21\u0D4D \u2192 18 \u0D15\u0D3F\u0D2E\u0D3F', -1]
].forEach(([idx, t1, t2, sgn]) => {
  const s = samples[idx];
  const sign = makeSign(t1, t2);
  const p = s.pos.clone().addScaledVector(s.side, sgn * 11.5);
  sign.position.set(p.x, p.y + 3.4, p.z);
  sign.rotation.y = Math.atan2(s.tan.x, s.tan.z) + Math.PI;
  scene.add(sign);
  const post = new THREE.Mesh(new THREE.BoxGeometry(0.3, 3.4, 0.3),
    new THREE.MeshStandardMaterial({ color: 0x6b7076 }));
  post.position.set(p.x, p.y + 1.7, p.z);
  scene.add(post);
});

/* ---------------- 9. Vegetation, huts, mountains ---------------- */
function scatterTrees() {
  const qual = save.settings.quality;
  const nTree = qual === 'LOW' ? 220 : qual === 'MED' ? 480 : 820;
  const nPalm = qual === 'LOW' ? 90 : qual === 'MED' ? 180 : 300;
  const trunkGeo = new THREE.CylinderGeometry(0.22, 0.34, 4.4, 6);
  const canopyGeo = new THREE.IcosahedronGeometry(2.6, 0);
  const palmTrunkGeo = new THREE.CylinderGeometry(0.18, 0.3, 6.2, 6);
  const palmTopGeo = new THREE.ConeGeometry(2.9, 1.7, 7);
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x5d4327, roughness: 0.9 });
  const canopyMat = new THREE.MeshStandardMaterial({ color: 0x1f6b3a, roughness: 0.85, flatShading: true });
  const palmMat = new THREE.MeshStandardMaterial({ color: 0x2f7d42, roughness: 0.85, flatShading: true });
  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, nTree);
  const canopies = new THREE.InstancedMesh(canopyGeo, canopyMat, nTree);
  const pTrunks = new THREE.InstancedMesh(palmTrunkGeo, trunkMat, nPalm);
  const pTops = new THREE.InstancedMesh(palmTopGeo, palmMat, nPalm);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3();
  let ti = 0, pi = 0, guard = 0;
  while ((ti < nTree || pi < nPalm) && guard++ < 20000) {
    const x = (Math.random() * 2 - 1) * 820, z = (Math.random() * 2 - 1) * 820;
    const r = nearestRoad(x, z);
    if (r.dist < 17) continue;
    const y = terrainH(x, z);
    const isPalm = pi < nPalm && y < 16;
    const rot = Math.random() * Math.PI * 2;
    q.setFromEuler(new THREE.Euler(0, rot, 0));
    if (isPalm) {
      const s = 0.8 + Math.random() * 0.55;
      v.set(x, y + 3.1 * s, z); sc.set(s, s, s);
      m4.compose(v, q, sc); pTrunks.setMatrixAt(pi, m4);
      v.set(x, y + 6.3 * s, z); sc.set(s * 1.15, s, s * 1.15);
      m4.compose(v, q, sc); pTops.setMatrixAt(pi, m4);
      pi++;
    } else if (ti < nTree) {
      const s = 0.75 + Math.random() * 0.85;
      v.set(x, y + 2.2 * s, z); sc.set(s, s, s);
      m4.compose(v, q, sc); trunks.setMatrixAt(ti, m4);
      v.set(x, y + 5.3 * s, z); sc.set(s * 1.25, s * 0.9, s * 1.25);
      m4.compose(v, q, sc); canopies.setMatrixAt(ti, m4);
      ti++;
    }
  }
  [trunks, canopies, pTrunks, pTops].forEach(m => {
    m.instanceMatrix.needsUpdate = true;
    if (save.settings.quality === 'HIGH') m.castShadow = true;
    scene.add(m);
  });
}
scatterTrees();

/* Tea-garden patches on slopes */
for (let i = 0; i < 16; i++) {
  const x = (Math.random() * 2 - 1) * 700, z = (Math.random() * 2 - 1) * 700;
  if (nearestRoad(x, z).dist < 30) continue;
  const y = terrainH(x, z);
  const patch = new THREE.Mesh(new THREE.SphereGeometry(18 + Math.random() * 16, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2.6),
    new THREE.MeshStandardMaterial({ color: 0x3f8f4c, roughness: 0.95, flatShading: true }));
  patch.position.set(x, y - 3, z);
  patch.scale.y = 0.28;
  scene.add(patch);
}

/* Village huts */
for (let i = 0; i < 18; i++) {
  const idx = Math.floor(Math.random() * N_SAMPLES);
  const s = samples[idx];
  const sgn = Math.random() > 0.5 ? 1 : -1;
  const p = s.pos.clone().addScaledVector(s.side, sgn * (14 + Math.random() * 12));
  const y = terrainH(p.x, p.z);
  const hut = new THREE.Group();
  const walls = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.6, 3.6),
    new THREE.MeshStandardMaterial({ color: [0xd9c4a3, 0xc9b08c, 0xe3d2b0][i % 3], roughness: 0.9 }));
  walls.position.y = 1.3;
  const roof = new THREE.Mesh(new THREE.ConeGeometry(3.6, 1.8, 4),
    new THREE.MeshStandardMaterial({ color: 0x8c3b2a, roughness: 0.85 }));
  roof.position.y = 3.4; roof.rotation.y = Math.PI / 4;
  walls.castShadow = true;
  hut.add(walls, roof);
  hut.position.set(p.x, y, p.z);
  hut.rotation.y = Math.random() * Math.PI * 2;
  scene.add(hut);
}

/* Distant mountains */
for (let i = 0; i < 14; i++) {
  const ang = (i / 14) * Math.PI * 2 + Math.random() * 0.35;
  const dist = 1450 + Math.random() * 550;
  const h = 240 + Math.random() * 260;
  const m = new THREE.Mesh(new THREE.ConeGeometry(320 + Math.random() * 220, h, 9),
    new THREE.MeshStandardMaterial({ color: 0x2c5447, roughness: 1, flatShading: true }));
  m.position.set(Math.sin(ang) * dist, h / 2 - 60, Math.cos(ang) * dist);
  scene.add(m);
}

/* ---------------- 10. Vehicles ---------------- */
const VEHICLES = [
  {
    id: 'k10', name: 'Malabar K10', insp: 'inspired by Maruti Suzuki Alto K10', cat: 'Kerala Favourite',
    color: 0xd23a2f, topKmh: 145, accel: 8.6, grip: 1.0, price: 0,
    specs: { Engine: '1.0 L 3-cyl', Power: '68 HP', Torque: '89 Nm', '0\u2013100': '13.9 s', Transmission: '5 MT', Drivetrain: 'FWD', Weight: '730 kg', Fuel: 'Petrol' }
  },
  {
    id: 'tharx', name: 'Ghats Thar-X', insp: 'inspired by Mahindra Thar', cat: 'SUV / Off-road',
    color: 0x3d5232, topKmh: 165, accel: 9.8, grip: 0.92, price: 120000,
    specs: { Engine: '2.2 L turbo diesel', Power: '130 HP', Torque: '300 Nm', '0\u2013100': '10.2 s', Transmission: '6 MT', Drivetrain: '4x4', Weight: '1,750 kg', Fuel: 'Diesel' }
  },
  {
    id: 'gtr', name: 'Rush GT-R', insp: 'inspired by Nissan GT-R', cat: 'Premium Hyper',
    color: 0x9aa7b4, topKmh: 230, accel: 14.2, grip: 1.14, price: 350000,
    specs: { Engine: '3.8 L twin-turbo V6', Power: '565 HP', Torque: '633 Nm', '0\u2013100': '3.2 s', Transmission: '6 DCT', Drivetrain: 'AWD', Weight: '1,740 kg', Fuel: 'Petrol' }
  }
];
function getUpg(carId, cat) { return (save.upgrades[carId] && save.upgrades[carId][cat]) || 0; }
function upgCost(level) { return [25000, 45000, 80000][level] || 0; }
function statOf(v) {
  const eng = getUpg(v.id, 'engine'), tur = getUpg(v.id, 'turbo'), tyr = getUpg(v.id, 'tyres');
  return {
    top: (v.topKmh * (1 + 0.04 * eng)) / 3.6,
    accel: v.accel * (1 + 0.08 * tur),
    grip: v.grip * (1 + 0.06 * tyr)
  };
}

function buildCar(colorHex, kind) {
  const g = new THREE.Group();
  const bodyMat = new THREE.MeshStandardMaterial({ color: colorHex, metalness: 0.55, roughness: 0.35 });
  const glassMat = new THREE.MeshStandardMaterial({ color: 0x101820, metalness: 0.85, roughness: 0.18 });
  const tireMat = new THREE.MeshStandardMaterial({ color: 0x16181b, roughness: 0.92 });
  let len = 4.1, wid = 1.95, bodyH = 0.72, cabH = 0.62;
  if (kind === 'bus') { len = 8.2; wid = 2.4; bodyH = 1.5; cabH = 1.2; }
  if (kind === 'auto') { len = 2.6; wid = 1.5; bodyH = 0.85; cabH = 0.8; }
  const body = new THREE.Mesh(new THREE.BoxGeometry(wid, bodyH, len), bodyMat);
  body.position.y = 0.62 + bodyH / 2 - 0.35;
  body.castShadow = true;
  g.add(body);
  const cab = new THREE.Mesh(new THREE.BoxGeometry(wid * 0.82, cabH, len * 0.48), glassMat);
  cab.position.set(0, body.position.y + bodyH / 2 + cabH / 2 - 0.06, kind === 'auto' ? 0.1 : -len * 0.06);
  cab.castShadow = true;
  g.add(cab);
  const wheels = [];
  const wr = kind === 'bus' ? 0.52 : 0.38;
  const wheelGeo = new THREE.CylinderGeometry(wr, wr, 0.3, 14);
  const wp = [
    [-wid / 2, -len * 0.32], [wid / 2, -len * 0.32],
    [-wid / 2, len * 0.32], [wid / 2, len * 0.32]
  ];
  wp.forEach((p, i) => {
    const w = new THREE.Mesh(wheelGeo, tireMat);
    w.rotation.z = Math.PI / 2;
    w.position.set(p[0], wr, p[1]);
    w.castShadow = true;
    g.add(w);
    wheels.push({ mesh: w, front: i < 2 });
  });
  // lights
  const headMat = new THREE.MeshBasicMaterial({ color: 0xfff6cc });
  const tailMat = new THREE.MeshBasicMaterial({ color: 0xff3b2f });
  for (const sgn of [1, -1]) {
    const hl = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.16, 0.08), headMat);
    hl.position.set(sgn * wid * 0.32, 0.72, -len / 2 - 0.02);
    const tl = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.16, 0.08), tailMat);
    tl.position.set(sgn * wid * 0.32, 0.78, len / 2 + 0.02);
    g.add(hl, tl);
  }
  return { group: g, wheels, dims: { len, wid } };
}

/* Player */
const playerDef = () => VEHICLES.find(v => v.id === save.selected) || VEHICLES[0];
let playerCar = buildCar(playerDef().color, 'car');
scene.add(playerCar.group);
const player = {
  heading: 0, speed: 0, slide: 0, nitro: 100, lap: 0, idx: 0, prevIdx: 0,
  progress: 0, lapStart: 0, bestLap: 0, raceTime: 0, finished: false, cp: 1
};
function respawnPlayer() {
  const s = samples[2];
  playerCar.group.position.set(s.pos.x, s.pos.y + 0.05, s.pos.z);
  player.heading = Math.atan2(s.tan.x, s.tan.z);
  player.speed = 0; player.slide = 0;
  player.idx = 2; player.prevIdx = 2; player.lap = 0; player.cp = 1;
  player.raceTime = 0; player.lapStart = 0; player.finished = false;
}
respawnPlayer();

/* Headlight cones for night */
const headlightGroup = new THREE.Group();
{
  const coneMat = new THREE.MeshBasicMaterial({ color: 0xfff2b8, transparent: true, opacity: 0.14, depthWrite: false });
  for (const sgn of [1, -1]) {
    const cone = new THREE.Mesh(new THREE.ConeGeometry(1.6, 11, 12, 1, true), coneMat);
    cone.rotation.x = -Math.PI / 2;
    cone.position.set(sgn * 0.75, 0.75, -6);
    headlightGroup.add(cone);
  }
  playerCar.group.add(headlightGroup);
}

/* AI racers */
const AI_DEFS = [
  { name: 'Ravi', color: 0x2f6fd0, skill: 31.5 },
  { name: 'Asha', color: 0xe8b64c, skill: 33.2 },
  { name: 'Vikram', color: 0x7a3fbf, skill: 34.6 }
];
const aiCars = [];
function buildAI() {
  aiCars.forEach(a => scene.remove(a.car.group));
  aiCars.length = 0;
  AI_DEFS.forEach((d, i) => {
    const car = buildCar(d.color, 'car');
    scene.add(car.group);
    aiCars.push({
      car, def: d, s: -6 - i * 7, lap: 0, speed: 0, lane: (i % 2 === 0 ? 1 : -1) * 2.2, finished: false, finishTime: 0
    });
  });
}
buildAI();

/* Traffic (free-roam) */
const traffic = [];
function buildTraffic() {
  traffic.forEach(t => scene.remove(t.car.group));
  traffic.length = 0;
  const kinds = ['car', 'auto', 'bus', 'car', 'car', 'auto', 'car', 'bus'];
  const cols = [0xc9b08c, 0xf2c230, 0x2f7d42, 0x8899aa, 0xd23a2f, 0xf2c230, 0x335577, 0xe0772c];
  for (let i = 0; i < 8; i++) {
    const car = buildCar(cols[i], kinds[i]);
    scene.add(car.group);
    traffic.push({
      car, kind: kinds[i], s: Math.floor((i / 8) * N_SAMPLES),
      speed: kinds[i] === 'bus' ? 13 : kinds[i] === 'auto' ? 11 : 17 + Math.random() * 4,
      lane: (i % 2 === 0 ? 1 : -1) * 2.4
    });
  }
}
buildTraffic();

function placeOnRoad(obj, sFloat, lane, lift) {
  const n = N_SAMPLES;
  const i0 = ((Math.floor(sFloat) % n) + n) % n;
  const i1 = (i0 + 1) % n;
  const t = sFloat - Math.floor(sFloat);
  const pos = samples[i0].pos.clone().lerp(samples[i1].pos, t);
  const side = samples[i0].side.clone().lerp(samples[i1].side, t).normalize();
  pos.addScaledVector(side, lane);
  obj.group.position.set(pos.x, pos.y + (lift || 0.02), pos.z);
  const tan = samples[i0].tan.clone().lerp(samples[i1].tan, t);
  obj.group.rotation.y = Math.atan2(tan.x, tan.z);
  return { pos, tan };
}

/* ---------------- 11. Game state ---------------- */
let state = 'MENU'; // MENU, GARAGE, SETTINGS, ABOUT, COUNT, RACE, FREEROAM, PAUSED, RESULTS
let gameMode = 'RACE'; // RACE, TIME, FREE
let countdown = 0;
let camMode = 0;
const CAM_NAMES = ['CHASE', 'HOOD', 'COCKPIT', 'FAR CHASE'];
let msgTimer = 0;

function showScreen(id) {
  ['screen-menu', 'screen-garage', 'screen-settings', 'screen-about', 'screen-pause', 'screen-results']
    .forEach(s => document.getElementById(s).classList.add('hidden'));
  if (id) document.getElementById(id).classList.remove('hidden');
}
function hudVisible(v) {
  document.getElementById('hud').classList.toggle('hidden', !v);
  document.getElementById('touch').classList.toggle('hidden', !v);
  document.getElementById('btn-mute').classList.toggle('hidden', !v);
}
function showMsg(text, dur) {
  const el = document.getElementById('hud-msg');
  el.textContent = text;
  el.style.opacity = 1;
  msgTimer = dur || 2;
}

function startGame(mode) {
  AudioSys.resume();
  gameMode = mode;
  respawnPlayer();
  buildAI();
  buildTraffic();
  player.bestLap = 0;
  if (mode === 'FREE') {
    state = 'FREEROAM';
    showScreen(null);
    showMsg(save.settings.lang === 'ML' ? '\u0D2B\u0D4D\u0D30\u0D40 \u0D31\u0D4B\u0D02' : 'FREE ROAM', 2.2);
  } else {
    state = 'COUNT';
    countdown = 3.99;
    showScreen(null);
  }
  hudVisible(true);
}

function finishRace() {
  state = 'RESULTS';
  const positions = racePositions();
  const pos = positions.indexOf('YOU') + 1;
  const prizeMap = [50000, 30000, 18000, 10000];
  let prize = gameMode === 'TIME' ? 20000 : (prizeMap[pos - 1] || 8000);
  if (player.bestLap > 0 && (save.bestLap === 0 || player.bestLap < save.bestLap)) {
    save.bestLap = player.bestLap;
    prize += 15000;
    showMsg('NEW BEST LAP!', 3);
  }
  save.money += prize;
  persist();
  document.getElementById('result-title').textContent =
    gameMode === 'TIME' ? '\u23F1 TIME TRIAL COMPLETE' : '\uD83C\uDFC1 RACE COMPLETE';
  document.getElementById('result-pos').textContent =
    gameMode === 'TIME' ? '\u2014' : (pos === 1 ? '1st \uD83E\uDD47' : pos === 2 ? '2nd' : pos === 3 ? '3rd' : pos + 'th');
  document.getElementById('result-lap').textContent = fmtTime(player.bestLap);
  document.getElementById('result-time').textContent = fmtTime(player.raceTime);
  document.getElementById('result-money').textContent = fmtMoney(prize);
  showScreen('screen-results');
  hudVisible(false);
  AudioSys.silence();
  AudioSys.blip(880, 0.15); setTimeout(() => AudioSys.blip(1174, 0.22), 160);
}

function racePositions() {
  const list = [{ id: 'YOU', prog: player.lap + player.idx / N_SAMPLES }];
  aiCars.forEach((a, i) => list.push({ id: 'AI' + i, prog: a.lap + (a.s % N_SAMPLES) / N_SAMPLES }));
  list.sort((x, y) => y.prog - x.prog);
  return list.map(l => l.id);
}

function togglePause() {
  if (state === 'RACE' || state === 'FREEROAM' || state === 'COUNT') {
    state = 'PAUSED';
    showScreen('screen-pause');
    AudioSys.silence();
  } else if (state === 'PAUSED') {
    state = gameMode === 'FREE' ? 'FREEROAM' : (countdown > 0 ? 'COUNT' : 'RACE');
    showScreen(null);
    AudioSys.resume();
  }
}
function toMenu() {
  state = 'MENU';
  showScreen('screen-menu');
  hudVisible(false);
  AudioSys.silence();
}
function resetCar() {
  const r = nearestRoad(playerCar.group.position.x, playerCar.group.position.z);
  const s = samples[r.idx];
  playerCar.group.position.set(s.pos.x, s.pos.y + 0.05, s.pos.z);
  player.heading = Math.atan2(s.tan.x, s.tan.z);
  player.speed = 0; player.slide = 0;
}
function cycleCamera() {
  camMode = (camMode + 1) % 4;
  if (state === 'RACE' || state === 'FREEROAM') showMsg(CAM_NAMES[camMode], 1.1);
}

/* ---------------- 12. Physics & race logic ---------------- */
const tmpV = new THREE.Vector3();
function updateGame(dt) {
  const v = playerDef();
  const st = statOf(v);
  const frozen = state === 'COUNT';

  /* countdown */
  if (state === 'COUNT') {
    countdown -= dt;
    const n = Math.ceil(countdown);
    if (countdown > 0.25) {
      showMsg(n >= 1 ? String(n) : 'GO!', 0.9);
      if (Math.abs(countdown - Math.round(countdown)) < dt) AudioSys.blip(n >= 1 ? 440 : 880, 0.12);
    } else {
      state = 'RACE';
      showMsg('GO!', 1);
      AudioSys.blip(880, 0.25);
    }
  }

  /* player physics */
  const throttle = frozen ? 0 : (input.up ? 1 : 0);
  const brake = frozen ? 0 : (input.down ? 1 : 0);
  const nitroActive = !frozen && input.nitro && player.nitro > 1 && player.speed > 5;
  const boost = nitroActive ? 1.32 : 1;

  player.speed += (throttle * st.accel * boost - brake * 15 - player.speed * 0.055
    - player.speed * Math.abs(player.speed) * 0.00048) * dt;
  if (brake && player.speed < 0.6 && !throttle) player.speed = Math.max(player.speed - 7 * dt, -8);
  if (!throttle && !brake && player.speed > 0) player.speed = Math.max(0, player.speed - 2.2 * dt);
  const maxSpeed = nitroActive ? st.top * 1.15 : st.top;
  player.speed = clamp(player.speed, -8, maxSpeed);

  if (nitroActive) {
    player.nitro = Math.max(0, player.nitro - 26 * dt);
    if (!player._whooshed) { AudioSys.whoosh(); player._whooshed = true; }
  } else {
    player.nitro = Math.min(100, player.nitro + 5.5 * dt);
    player._whooshed = false;
  }

  const steer = frozen ? 0 : ((input.left ? -1 : 0) + (input.right ? 1 : 0));
  const speedFactor = 0.32 + 0.68 * clamp(Math.abs(player.speed) / 16, 0, 1);
  player.heading += steer * 1.55 * speedFactor * dt * (input.hand ? 1.65 : 1) * st.grip * Math.sign(player.speed || 1);
  const targetSlide = input.hand && Math.abs(player.speed) > 8 ? steer * 0.85 : 0;
  player.slide = lerp(player.slide, targetSlide, dt * 2.4);

  const moveDir = player.heading + player.slide;
  const px = playerCar.group.position, speedMs = player.speed;
  px.x += Math.sin(moveDir) * speedMs * dt;
  px.z += Math.cos(moveDir) * speedMs * dt;

  /* road follow & off-road */
  const r = nearestRoad(px.x, px.z);
  let targetY = r.pos.y + 0.02;
  if (r.dist > 30) targetY = terrainH(px.x, px.z) + 0.02;
  px.y = lerp(px.y, targetY, clamp(dt * 7, 0, 1));
  const offroad = r.dist > 8.2;
  if (offroad && !frozen) {
    player.speed *= (1 - 0.85 * dt);
  }
  playerCar.group.rotation.y = player.heading;
  playerCar.group.rotation.z = lerp(playerCar.group.rotation.z, -steer * speedFactor * 0.045 - player.slide * 0.1, dt * 6);

  /* wheels */
  const spin = speedMs / 0.38 * dt;
  playerCar.wheels.forEach(w => {
    w.mesh.rotation.x += spin;
    if (w.front) w.mesh.rotation.y = steer * 0.42;
  });

  /* progress & laps */
  player.prevIdx = player.idx;
  player.idx = r.idx;
  if (player.prevIdx > N_SAMPLES - 80 && player.idx < 80 && player.speed > 2) {
    player.lap++;
    const lapTime = player.raceTime - player.lapStart;
    player.lapStart = player.raceTime;
    if (lapTime > 2) {
      if (player.bestLap === 0 || lapTime < player.bestLap) { player.bestLap = lapTime; showMsg('BEST LAP ' + fmtTime(lapTime), 2); }
      AudioSys.blip(990, 0.14); setTimeout(() => AudioSys.blip(1318, 0.2), 150);
    }
    if (gameMode !== 'FREE' && player.lap >= (gameMode === 'TIME' ? 1 : 3)) {
      player.finished = true;
      finishRace();
      return;
    }
    if (gameMode === 'TIME') showMsg('LAP ' + (player.lap + 1), 1.4);
    else showMsg('LAP ' + (player.lap + 1) + ' / 3', 1.6);
  }
  if (!frozen && state !== 'RESULTS') player.raceTime += dt;

  /* AI */
  aiCars.forEach((a, i) => {
    if (a.finished) return;
    const curv = samples[((Math.floor(a.s) % N_SAMPLES) + N_SAMPLES) % N_SAMPLES].curv;
    let target = a.def.skill * (1 - clamp(curv * 26, 0, 0.52));
    // rubber band: if behind player, slightly faster
    const playerProg = player.lap * N_SAMPLES + player.idx;
    const aiProg = a.lap * N_SAMPLES + (a.s % N_SAMPLES);
    if (aiProg < playerProg - 120) target *= 1.06;
    if (aiProg > playerProg + 160) target *= 0.94;
    a.speed = lerp(a.speed, target, dt * 1.1);
    a.s += (a.speed * dt) / segLen;
    if (a.s >= N_SAMPLES) { a.s -= N_SAMPLES; a.lap++; }
    const info = placeOnRoad(a.car, a.s, a.lane, 0.02);
    a.car.wheels.forEach(w => { w.mesh.rotation.x += a.speed / 0.38 * dt; });
    /* collision with player */
    tmpV.copy(a.car.group.position).sub(playerCar.group.position);
    const d = tmpV.length();
    if (d < 3.1 && !frozen) {
      tmpV.normalize();
      playerCar.group.position.addScaledVector(tmpV, (3.1 - d) * 0.6);
      player.speed *= 0.965;
      a.speed *= 0.97;
      if (!a._cool || player.raceTime - a._cool > 0.8) { AudioSys.thump(); a._cool = player.raceTime; }
    }
  });

  /* traffic (free roam & always visual) */
  traffic.forEach(t => {
    t.s += (t.speed * dt) / segLen;
    if (t.s >= N_SAMPLES) t.s -= N_SAMPLES;
    placeOnRoad(t.car, t.s, t.lane, 0.02);
    t.car.wheels.forEach(w => { w.mesh.rotation.x += t.speed / 0.38 * dt; });
    tmpV.copy(t.car.group.position).sub(playerCar.group.position);
    const d = tmpV.length();
    if (d < 3.4 && !frozen) {
      tmpV.normalize();
      playerCar.group.position.addScaledVector(tmpV, (3.4 - d) * 0.7);
      player.speed *= 0.94;
      if (!t._cool || player.raceTime - t._cool > 0.8) { AudioSys.thump(); t._cool = player.raceTime; }
    }
  });

  /* sun follows player for tight shadows */
  sun.position.set(px.x + 70, px.y + 130, px.z + 45);
  sun.target.position.copy(px);
  sun.target.updateMatrixWorld();

  /* audio */
  AudioSys.engine(Math.abs(player.speed), throttle, nitroActive);
}

/* ---------------- 13. Camera ---------------- */
const camLook = new THREE.Vector3(0, 1, 0);
function updateCamera(dt) {
  const p = playerCar.group.position;
  const fwd = tmpV.set(Math.sin(player.heading), 0, Math.cos(player.heading));
  if (state === 'MENU' || state === 'GARAGE' || state === 'SETTINGS' || state === 'ABOUT') {
    const ang = performance.now() * 0.00012;
    camera.position.set(p.x + Math.sin(ang) * 17, p.y + 7, p.z + Math.cos(ang) * 17);
    camera.lookAt(p.x, p.y + 1.2, p.z);
    camera.fov = lerp(camera.fov, 58, dt * 3); camera.updateProjectionMatrix();
    return;
  }
  const speedK = clamp(Math.abs(player.speed) / 60, 0, 1);
  let desired = tmpV.clone();
  if (camMode === 0) desired.set(p.x - fwd.x * 9.5, p.y + 3.6 + speedK * 0.8, p.z - fwd.z * 9.5);
  else if (camMode === 1) desired.set(p.x + fwd.x * 0.4, p.y + 1.55, p.z + fwd.z * 0.4);
  else if (camMode === 2) desired.set(p.x + fwd.x * 0.1, p.y + 1.22, p.z + fwd.z * 0.1);
  else desired.set(p.x - fwd.x * 15, p.y + 7.5, p.z - fwd.z * 15);
  const k = 1 - Math.exp(-dt * (camMode >= 1 && camMode <= 2 ? 14 : 5.5));
  camera.position.lerp(desired, k);
  const lookTarget = tmpV.clone().set(p.x + fwd.x * 14, p.y + 1.6, p.z + fwd.z * 14);
  camLook.lerp(lookTarget, 1 - Math.exp(-dt * 8));
  camera.lookAt(camLook);
  const targetFov = 64 + (input.nitro && player.nitro > 1 ? 12 * speedK + 6 : 0) + speedK * 5;
  camera.fov = lerp(camera.fov, targetFov, dt * 3.2);
  camera.updateProjectionMatrix();
  if (save.settings.weather === 'RAIN' && Math.abs(player.speed) > 20) {
    camera.position.x += (Math.random() - 0.5) * 0.04;
    camera.position.y += (Math.random() - 0.5) * 0.04;
  }
}

/* ---------------- 14. Rain particles ---------------- */
const rainGeo = new THREE.BufferGeometry();
{
  const n = 900, arr = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    arr[i * 3] = (Math.random() - 0.5) * 70;
    arr[i * 3 + 1] = Math.random() * 34;
    arr[i * 3 + 2] = (Math.random() - 0.5) * 70;
  }
  rainGeo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
}
const rainPoints = new THREE.Points(rainGeo, new THREE.PointsMaterial({
  color: 0x9fc3e8, size: 0.19, transparent: true, opacity: 0.55, depthWrite: false
}));
rainPoints.visible = false;
scene.add(rainPoints);
function updateRain(dt) {
  if (!rainPoints.visible) return;
  rainPoints.position.set(camera.position.x, camera.position.y - 8, camera.position.z);
  const arr = rainGeo.attributes.position.array;
  for (let i = 1; i < arr.length; i += 3) {
    arr[i] -= 42 * dt;
    if (arr[i] < -12) arr[i] = 26;
  }
  rainGeo.attributes.position.needsUpdate = true;
}

/* ---------------- 15. HUD & minimap ---------------- */
const speedEl = document.getElementById('speed-val');
const nitroEl = document.getElementById('nitro-fill');
const posEl = document.getElementById('race-pos');
const lapEl = document.getElementById('race-lap');
const timeEl = document.getElementById('race-time');
const bestEl = document.getElementById('race-best');
const mm = document.getElementById('minimap');
const mmCtx = mm.getContext('2d');
let mmPath = null, mmBounds = null;
function computeMinimap() {
  let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
  samples.forEach(s => {
    minX = Math.min(minX, s.pos.x); maxX = Math.max(maxX, s.pos.x);
    minZ = Math.min(minZ, s.pos.z); maxZ = Math.max(maxZ, s.pos.z);
  });
  mmBounds = { minX, maxX, minZ, maxZ };
  const pad = 30, W = 320, H = 320;
  const sc = Math.min((W - pad * 2) / (maxX - minX), (H - pad * 2) / (maxZ - minZ));
  mmPath = samples.map(s => ({
    x: (s.pos.x - (minX + maxX) / 2) * sc + W / 2,
    y: (s.pos.z - (minZ + maxZ) / 2) * sc + H / 2
  }));
  mmPath._sc = sc;
}
computeMinimap();
function drawMinimap() {
  const W = 320, H = 320;
  mmCtx.clearRect(0, 0, W, H);
  mmCtx.fillStyle = 'rgba(12,20,16,0.85)';
  mmCtx.fillRect(0, 0, W, H);
  if (!mmPath) return;
  mmCtx.strokeStyle = '#c8d4c4'; mmCtx.lineWidth = 7; mmCtx.lineJoin = 'round';
  mmCtx.beginPath();
  mmPath.forEach((p, i) => { if (i === 0) mmCtx.moveTo(p.x, p.y); else mmCtx.lineTo(p.x, p.y); });
  mmCtx.closePath(); mmCtx.stroke();
  mmCtx.strokeStyle = '#3a463c'; mmCtx.lineWidth = 3;
  mmCtx.stroke();
  const sc = mmPath._sc;
  const dot = (x, z, color, r) => {
    let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
    if (!mmBounds) return;
    const cx = (x - (mmBounds.minX + mmBounds.maxX) / 2) * sc + W / 2;
    const cy = (z - (mmBounds.minZ + mmBounds.maxZ) / 2) * sc + H / 2;
    mmCtx.fillStyle = color;
    mmCtx.beginPath(); mmCtx.arc(cx, cy, r, 0, Math.PI * 2); mmCtx.fill();
  };
  aiCars.forEach(a => dot(a.car.group.position.x, a.car.group.position.z, '#f2c230', 6));
  if (gameMode === 'FREE') traffic.forEach(t => dot(t.car.group.position.x, t.car.group.position.z, '#7fa8d4', 4));
  const p = playerCar.group.position;
  mmCtx.save();
  const cx = (p.x - (mmBounds.minX + mmBounds.maxX) / 2) * sc + W / 2;
  const cy = (p.z - (mmBounds.minZ + mmBounds.maxZ) / 2) * sc + H / 2;
  mmCtx.translate(cx, cy);
  mmCtx.rotate(-player.heading + Math.PI);
  mmCtx.fillStyle = '#ff4b3e';
  mmCtx.beginPath(); mmCtx.moveTo(0, -11); mmCtx.lineTo(8, 9); mmCtx.lineTo(-8, 9); mmCtx.closePath(); mmCtx.fill();
  mmCtx.restore();
}
function updateHUD() {
  if (state !== 'RACE' && state !== 'FREEROAM' && state !== 'COUNT') return;
  speedEl.textContent = String(Math.round(Math.abs(player.speed) * 3.6));
  nitroEl.style.width = player.nitro + '%';
  if (gameMode === 'FREE') {
    posEl.textContent = 'FREE ROAM';
    lapEl.textContent = save.settings.lang === 'ML' ? '\u0D15\u0D31\u0D19\u0D4D\u0D19\u0D41\u0D02 \u0D2A\u0D30\u0D4D\u0D2F\u0D2F\u0D3F\u0D15\u0D4D\u0D15\u0D41\u0D02' : 'EXPLORE KERALA';
    timeEl.textContent = fmtTime(player.raceTime);
  } else {
    const positions = racePositions();
    posEl.textContent = 'P' + (positions.indexOf('YOU') + 1) + ' / 4';
    lapEl.textContent = gameMode === 'TIME' ? 'TIME TRIAL \u00B7 LAP ' + (player.lap + 1) : 'LAP ' + Math.min(player.lap + 1, 3) + ' / 3';
    timeEl.textContent = fmtTime(player.raceTime);
    bestEl.textContent = 'BEST ' + fmtTime(player.bestLap || save.bestLap);
  }
  if (msgTimer > 0) {
    msgTimer -= 1 / 60;
    if (msgTimer <= 0) document.getElementById('hud-msg').style.opacity = 0;
  }
  drawMinimap();
}

/* ---------------- 16. Garage UI ---------------- */
function renderGarage() {
  document.getElementById('money-val').textContent = fmtMoney(save.money);
  document.getElementById('bestlap-val').textContent = fmtTime(save.bestLap);
  const list = document.getElementById('car-list');
  list.innerHTML = '';
  VEHICLES.forEach(v => {
    const owned = save.owned.includes(v.id);
    const sel = save.selected === v.id;
    const st = statOf(v);
    const card = document.createElement('div');
    card.className = 'card' + (sel ? ' sel' : '');
    const upg = save.upgrades[v.id] || {};
    card.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
        <div>
          <b style="font-size:17px;color:var(--gold)">${v.name}</b>
          <div class="note" style="margin:2px 0">${v.cat} · ${v.insp}</div>
          <span class="tag">Top ${(st.top * 3.6).toFixed(0)} km/h</span>
          <span class="tag">Accel ${'\u2605'.repeat(Math.round(v.accel / 3.2))}</span>
          <span class="tag">Grip ${'\u2605'.repeat(Math.round(v.grip * 3))}</span>
        </div>
        <div style="text-align:right">
          ${owned
            ? (sel ? '<span class="tag em">\u2714 SELECTED</span>'
                   : `<button class="btn small primary" data-select="${v.id}">SELECT</button>`)
            : `<button class="btn small" data-buy="${v.id}" ${save.money < v.price ? 'disabled style="opacity:.45"' : ''}>BUY ${fmtMoney(v.price)}</button>`}
        </div>
      </div>
      <table class="spec">${Object.entries(v.specs).map(([k2, val]) => `<tr><td>${k2}</td><td>${val}</td></tr>`).join('')}
        <tr><td>Performance</td><td class="em">game-adjusted stats</td></tr></table>
      ${owned ? `<div class="row" style="margin-top:8px">
        ${['engine', 'turbo', 'tyres'].map(cat => {
          const lvl = upg[cat] || 0;
          const cost = upgCost(lvl);
          return `<button class="btn small" data-upg="${v.id}:${cat}" ${lvl >= 3 || save.money < cost ? 'disabled style="opacity:.45"' : ''}>
            ${cat.toUpperCase()} ${'\u2B50'.repeat(lvl)}${lvl >= 3 ? ' MAX' : ' \u00B7 ' + fmtMoney(cost)}</button>`;
        }).join('')}
      </div>` : ''}
    `;
    list.appendChild(card);
  });
  list.querySelectorAll('[data-select]').forEach(b => b.addEventListener('click', () => {
    save.selected = b.dataset.select; persist(); rebuildPlayerCar(); renderGarage(); AudioSys.blip(660, 0.1);
  }));
  list.querySelectorAll('[data-buy]').forEach(b => b.addEventListener('click', () => {
    const v = VEHICLES.find(x => x.id === b.dataset.buy);
    if (!v || save.money < v.price) return;
    save.money -= v.price;
    save.owned.push(v.id);
    save.selected = v.id;
    persist(); rebuildPlayerCar(); renderGarage();
    AudioSys.blip(880, 0.12); setTimeout(() => AudioSys.blip(1174, 0.18), 130);
  }));
  list.querySelectorAll('[data-upg]').forEach(b => b.addEventListener('click', () => {
    const [carId, cat] = b.dataset.upg.split(':');
    const lvl = getUpg(carId, cat);
    const cost = upgCost(lvl);
    if (lvl >= 3 || save.money < cost) return;
    save.money -= cost;
    if (!save.upgrades[carId]) save.upgrades[carId] = {};
    save.upgrades[carId][cat] = lvl + 1;
    persist(); renderGarage();
    AudioSys.blip(740, 0.1);
  }));
}
function rebuildPlayerCar() {
  scene.remove(playerCar.group);
  const v = playerDef();
  playerCar = buildCar(v.color, 'car');
  playerCar.group.add(headlightGroup);
  scene.add(playerCar.group);
  respawnPlayer();
}

/* ---------------- 17. UI wiring ---------------- */
function seg(id, key, after) {
  const el = document.getElementById(id);
  if (!el) return;
  const refresh = () => el.querySelectorAll('button').forEach(b =>
    b.classList.toggle('on', b.dataset.v === save.settings[key]));
  el.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
    save.settings[key] = b.dataset.v;
    persist(); refresh();
    if (after) after(b.dataset.v);
    AudioSys.blip(600, 0.08);
  }));
  refresh();
}
seg('seg-quality', 'quality', () => { /* trees rebuild needs reload; apply shadows live */ });
seg('seg-weather', 'weather', applyEnvironment);
seg('seg-time', 'time', applyEnvironment);
seg('seg-sound', 'sound', v => { AudioSys.setMuted(v === 'OFF'); AudioSys.resume(); });
seg('seg-lang', 'lang', applyLang);

document.getElementById('btn-race').addEventListener('click', () => startGame('RACE'));
document.getElementById('btn-time').addEventListener('click', () => startGame('TIME'));
document.getElementById('btn-free').addEventListener('click', () => startGame('FREE'));
document.getElementById('btn-garage').addEventListener('click', () => { renderGarage(); state = 'GARAGE'; showScreen('screen-garage'); });
document.getElementById('btn-settings').addEventListener('click', () => { state = 'SETTINGS'; showScreen('screen-settings'); });
document.getElementById('btn-about').addEventListener('click', () => { state = 'ABOUT'; showScreen('screen-about'); });
document.getElementById('btn-garage-back').addEventListener('click', toMenu);
document.getElementById('btn-settings-back').addEventListener('click', toMenu);
document.getElementById('btn-about-back').addEventListener('click', toMenu);
document.getElementById('btn-resume').addEventListener('click', togglePause);
document.getElementById('btn-restart').addEventListener('click', () => startGame(gameMode));
document.getElementById('btn-quit').addEventListener('click', toMenu);
document.getElementById('btn-race-again').addEventListener('click', () => startGame(gameMode));
document.getElementById('btn-results-menu').addEventListener('click', toMenu);
document.getElementById('btn-reset-save').addEventListener('click', () => {
  if (confirm('Reset all progress?')) {
    save = JSON.parse(JSON.stringify(DEFAULT_SAVE));
    persist(); applyLang(); applyEnvironment(); rebuildPlayerCar();
    alert('Save reset.');
  }
});
document.getElementById('btn-mute').addEventListener('click', () => {
  AudioSys.resume();
  const m = !AudioSys.muted;
  AudioSys.setMuted(m);
  save.settings.sound = m ? 'OFF' : 'ON';
  persist();
  document.getElementById('btn-mute').textContent = m ? '\uD83D\uDD07' : '\uD83D\uDD0A';
});

/* auto-pause when tab hidden */
document.addEventListener('visibilitychange', () => {
  if (document.hidden && (state === 'RACE' || state === 'FREEROAM' || state === 'COUNT')) togglePause();
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('touchmove', e => { if (e.target.closest && e.target.closest('#touch')) e.preventDefault(); }, { passive: false });

/* ---------------- 18. Quality application ---------------- */
function applyQuality() {
  const q = save.settings.quality;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, q === 'LOW' ? 1 : q === 'MED' ? 1.5 : 1.75));
  renderer.shadowMap.enabled = q !== 'LOW';
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  terrainMesh.receiveShadow = true;
  sun.castShadow = q !== 'LOW';
}

/* ---------------- 19. Main loop ---------------- */
const clock = new THREE.Clock();
function loop() {
  requestAnimationFrame(loop);
  const dt = Math.min(clock.getDelta(), 0.05);
  if (state === 'RACE' || state === 'FREEROAM' || state === 'COUNT') {
    updateGame(dt);
    updateRain(dt);
    updateHUD();
    if (state === 'PAUSED') AudioSys.silence();
  } else {
    if (playerCar.wheels) playerCar.wheels.forEach(w => { w.mesh.rotation.x += dt * 0.6; });
    if (AudioSys.ctx) AudioSys.silence();
    updateRain(dt);
  }
  updateCamera(dt);
  renderer.render(scene, camera);
}

/* ---------------- 20. Boot ---------------- */
applyQuality();
applyEnvironment();
applyLang();
showScreen('screen-menu');
hudVisible(false);
document.getElementById('btn-mute').textContent = AudioSys.muted ? '\uD83D\uDD07' : '\uD83D\uDD0A';
loop();
