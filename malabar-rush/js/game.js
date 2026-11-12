/* ============================================================
   MALABAR RUSH — Episode 1: Thamarassery Churam  (v1.1 — Stage 1 Fixes & Visual Upgrade)
   Created by Hadee Mohammed
   Procedural 3D arcade racing (Three.js r147 UMD) — zero external assets.
   v1.1: steering fix, collision overhaul, premium vehicle/environment
         graphics, PMREM environment reflections, Kerala authenticity.
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

/* Merge multiple transformed primitive geometries into one (no BufferGeometryUtils needed) */
function mergeGeoms(list) {
  let vCount = 0, iCount = 0;
  list.forEach(({ geo }) => {
    vCount += geo.attributes.position.count;
    iCount += geo.index ? geo.index.count : geo.attributes.position.count;
  });
  const pos = new Float32Array(vCount * 3), nor = new Float32Array(vCount * 3), uv = new Float32Array(vCount * 2);
  const idx = new Uint32Array(iCount);
  let vOff = 0, iOff = 0;
  list.forEach(({ geo, matrix }) => {
    const g = geo.clone();
    if (matrix) g.applyMatrix4(matrix);
    if (!g.attributes.normal) g.computeVertexNormals();
    if (!g.index) {
      const n = g.attributes.position.count;
      const a = new Uint32Array(n);
      for (let i = 0; i < n; i++) a[i] = i;
      g.setIndex(new THREE.BufferAttribute(a, 1));
    }
    pos.set(g.attributes.position.array, vOff * 3);
    nor.set(g.attributes.normal.array, vOff * 3);
    if (g.attributes.uv) uv.set(g.attributes.uv.array, vOff * 2);
    const gi = g.index.array;
    for (let i = 0; i < gi.length; i++) idx[iOff + i] = gi[i] + vOff;
    vOff += g.attributes.position.count;
    iOff += gi.length;
  });
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  out.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  out.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  out.setIndex(new THREE.BufferAttribute(idx, 1));
  return out;
}
function mat4(rx, ry, rz, tx, ty, tz, sx, sy, sz) {
  return new THREE.Matrix4().compose(
    new THREE.Vector3(tx, ty, tz),
    new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz)),
    new THREE.Vector3(sx || 1, sy || 1, sz || 1)
  );
}

/* ---------------- 2. Save system ---------------- */
const SAVE_KEY = 'malabarRushSave_v1';
const DEFAULT_SAVE = {
  money: 0, owned: ['k10'], selected: 'k10', bestLap: 0,
  upgrades: {},
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

/* ---------------- 4. Audio (procedural) ---------------- */
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
      this.engineOsc = this.ctx.createOscillator(); this.engineOsc.type = 'sawtooth';
      this.engineOsc2 = this.ctx.createOscillator(); this.engineOsc2.type = 'square';
      const lp = this.ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 720;
      this.engineGain = this.ctx.createGain(); this.engineGain.gain.value = 0;
      this.engineOsc.connect(lp); this.engineOsc2.connect(lp);
      lp.connect(this.engineGain); this.engineGain.connect(this.master);
      this.engineOsc.frequency.value = 55; this.engineOsc2.frequency.value = 27;
      this.engineOsc.start(); this.engineOsc2.start();
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

/* ---------------- 6. Renderer / scene / lights ---------------- */
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
sun.shadow.bias = -0.0006;
sun.shadow.normalBias = 0.025;
scene.add(sun); scene.add(sun.target);

/* Sky dome */
const skyGeo = new THREE.SphereGeometry(3600, 24, 14);
const skyColors = new Float32Array(skyGeo.attributes.position.count * 3);
skyGeo.setAttribute('color', new THREE.BufferAttribute(skyColors, 3));
const skyMesh = new THREE.Mesh(skyGeo, new THREE.MeshBasicMaterial({
  vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false
}));
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

/* Sun disc + halo */
const sunDisc = new THREE.Mesh(new THREE.SphereGeometry(75, 18, 18),
  new THREE.MeshBasicMaterial({ color: 0xffe9b0, fog: false }));
const sunHalo = new THREE.Mesh(new THREE.SphereGeometry(190, 18, 18),
  new THREE.MeshBasicMaterial({ color: 0xffd98c, fog: false, transparent: true, opacity: 0.22, depthWrite: false }));
scene.add(sunDisc, sunHalo);

/* PMREM environment reflections (premium PBR look) */
let envRT = null;
function buildEnvironmentMap(skyTopHex, skyHorHex, groundHex) {
  const faces = [];
  for (let f = 0; f < 6; f++) {
    const cv = document.createElement('canvas');
    cv.width = 64; cv.height = 64;
    const c2 = cv.getContext('2d');
    if (f === 2) { // +Y top: sky
      c2.fillStyle = '#' + new THREE.Color(skyTopHex).getHexString(); c2.fillRect(0, 0, 64, 64);
    } else if (f === 3) { // -Y bottom: ground
      c2.fillStyle = '#' + new THREE.Color(groundHex).getHexString(); c2.fillRect(0, 0, 64, 64);
    } else { // sides: horizon gradient
      const g = c2.createLinearGradient(0, 0, 0, 64);
      g.addColorStop(0, '#' + new THREE.Color(skyTopHex).getHexString());
      g.addColorStop(0.55, '#' + new THREE.Color(skyHorHex).getHexString());
      g.addColorStop(1, '#' + new THREE.Color(groundHex).getHexString());
      c2.fillStyle = g; c2.fillRect(0, 0, 64, 64);
    }
    faces.push(cv);
  }
  const cubeTex = new THREE.CubeTexture(faces);
  cubeTex.needsUpdate = true;
  try {
    const pmrem = new THREE.PMREMGenerator(renderer);
    const rt = pmrem.fromCubemap(cubeTex);
    if (envRT) envRT.dispose();
    envRT = rt;
    scene.environment = rt.texture;
    pmrem.dispose();
  } catch (e) {}
  cubeTex.dispose();
}

const fogColor = new THREE.Color(0xcfe3f2);
scene.fog = new THREE.Fog(fogColor.getHex(), 80, 1400);

const PRESETS = {
  DAY:    { skyTop: 0x2f6fd0, skyHor: 0xbfe3ff, sunCol: 0xfff2dd, sunInt: 1.25, hemiInt: 0.72, fog: 0xcfe3f2, fogFar: 1500, exposure: 1.08, sunPos: [220, 420, 160] },
  SUNSET: { skyTop: 0x27346e, skyHor: 0xff9d5c, sunCol: 0xff8c42, sunInt: 1.18, hemiInt: 0.5,  fog: 0xe8a878, fogFar: 1350, exposure: 1.02, sunPos: [420, 130, 240] },
  NIGHT:  { skyTop: 0x050a1e, skyHor: 0x16234d, sunCol: 0x4a5f9e, sunInt: 0.4,  hemiInt: 0.22, fog: 0x0e1830, fogFar: 1050, exposure: 0.92, sunPos: [-260, 380, -180] }
};
const WEATHER = {
  CLEAR: { fogMul: 1,   dark: 1,   rain: false },
  MIST:  { fogMul: 3.1, dark: 0.88, rain: false },
  RAIN:  { fogMul: 2.1, dark: 0.78, rain: true  }
};
let headlightGroup = null;   // night cones on player
const headSpots = [];        // night spotlights on player

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
  // sun disc placement
  sunDisc.position.set(p.sunPos[0], p.sunPos[1], p.sunPos[2]);
  sunHalo.position.copy(sunDisc.position);
  sunDisc.visible = save.settings.time !== 'NIGHT';
  sunHalo.visible = sunDisc.visible;
  // environment reflections
  buildEnvironmentMap(p.skyTop, p.skyHor, save.settings.time === 'NIGHT' ? 0x101820 : 0x2d4a2e);
  // wet-road response
  if (roadMesh && roadMesh.material) {
    const wet = save.settings.weather === 'RAIN';
    roadMesh.material.roughness = wet ? 0.22 : 0.68;
    roadMesh.material.metalness = wet ? 0.42 : 0.08;
    roadMesh.material.color.setHex(wet ? 0x22262c : 0x2b2f36);
    roadMesh.material.needsUpdate = true;
  }
  // headlights
  const night = save.settings.time === 'NIGHT';
  if (headlightGroup) headlightGroup.visible = night;
  headSpots.forEach(s => { s.visible = night; });
  // sign glow at night
  glowSigns.forEach(m => { m.material.color.setHex(night ? 0xffe9b0 : 0xffffff); });
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
const samples = [];
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

/* Flatten terrain near road */
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
    if (dist < 46) h = lerp(bestY - 0.12, h, smoothstep(dist / 46));
    posAttr.setY(i, h);
  }
  terrainGeo.computeVertexNormals();
}
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
const terrainMesh = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.95, metalness: 0
}));
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);

/* Asphalt canvas texture */
function asphaltTexture() {
  const cv = document.createElement('canvas');
  cv.width = 256; cv.height = 256;
  const c2 = cv.getContext('2d');
  c2.fillStyle = '#2e3238'; c2.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 2600; i++) {
    const g = 32 + Math.random() * 34;
    c2.fillStyle = 'rgba(' + g + ',' + (g + 2) + ',' + (g + 6) + ',' + (0.16 + Math.random() * 0.22) + ')';
    c2.fillRect(Math.random() * 256, Math.random() * 256, 1 + Math.random() * 3, 1 + Math.random() * 3);
  }
  for (let i = 0; i < 26; i++) {
    c2.strokeStyle = 'rgba(18,20,24,0.14)';
    c2.lineWidth = 1 + Math.random() * 2;
    c2.beginPath();
    c2.moveTo(Math.random() * 256, 0); c2.lineTo(Math.random() * 256, 256);
    c2.stroke();
  }
  const tex = new THREE.CanvasTexture(cv);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.encoding = THREE.sRGBEncoding;
  tex.anisotropy = 8;
  return tex;
}

/* Road ribbon builder (with UVs) */
function buildRibbon(width, yOff, colorHex, dashGap, withUV) {
  const verts = [], idxs = [], cols = [], uvs = [];
  const c = new THREE.Color(colorHex);
  for (let i = 0; i <= N_SAMPLES; i++) {
    const s = samples[i % N_SAMPLES];
    const L = s.pos.clone().addScaledVector(s.side, -width);
    const R = s.pos.clone().addScaledVector(s.side, width);
    L.y += yOff; R.y += yOff;
    verts.push(L.x, L.y, L.z, R.x, R.y, R.z);
    cols.push(c.r, c.g, c.b, c.r, c.g, c.b);
    uvs.push(0, i / 8, 1, i / 8);
    if (i > 0) {
      const a = (i - 1) * 2, b = a + 1, cc = i * 2, d = cc + 1;
      const skip = dashGap && (i % dashGap) >= dashGap * 0.55;
      if (!skip) idxs.push(a, b, cc, b, d, cc);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  g.setIndex(idxs);
  return g;
}
const roadMesh = new THREE.Mesh(buildRibbon(6.2, 0.06, 0x2b2f36, 0, true), new THREE.MeshStandardMaterial({
  map: asphaltTexture(), vertexColors: true, roughness: 0.68, metalness: 0.08
}));
roadMesh.receiveShadow = true;
scene.add(roadMesh);
scene.add(new THREE.Mesh(buildRibbon(0.16, 0.11, 0xf2ecd8, 14), new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6 })));

/* edge lines */
{
  const mkEdge = (offset, colorHex) => {
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
  scene.add(mkEdge(5.4, 0xe6e6e6), mkEdge(-5.4, 0xe6e6e6));
}

/* Rumble strips (red/white) on sharp bends */
{
  const verts = [], idxs = [], cols = [];
  const red = new THREE.Color(0xb8402f), white = new THREE.Color(0xe8e4da);
  for (const sgn of [1, -1]) {
    for (let i = 0; i < N_SAMPLES; i++) {
      const s = samples[i];
      if (s.curv < 0.012) continue;
      const c = (Math.floor(i / 5) % 2) ? red : white;
      const base = verts.length / 3;
      const L = s.pos.clone().addScaledVector(s.side, sgn * 6.25);
      const R = s.pos.clone().addScaledVector(s.side, sgn * 7.1);
      L.y += 0.12; R.y += 0.12;
      verts.push(L.x, L.y, L.z, R.x, R.y, R.z);
      cols.push(c.r, c.g, c.b, c.r, c.g, c.b);
      if (base > 0 && samples[i - 1] && samples[i - 1].curv >= 0.012) {
        idxs.push(base - 2, base - 1, base, base - 1, base + 1, base);
      }
    }
  }
  if (verts.length) {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    g.setIndex(idxs);
    scene.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.65, side: THREE.DoubleSide })));
  }
}

/* Guardrails + posts + reflectors */
{
  const postGeo = new THREE.BoxGeometry(0.22, 1.1, 0.22);
  const postMat = new THREE.MeshStandardMaterial({ color: 0x9aa2ab, metalness: 0.55, roughness: 0.42 });
  const nPosts = Math.floor(N_SAMPLES / 10) * 2;
  const posts = new THREE.InstancedMesh(postGeo, postMat, nPosts);
  const refGeo = new THREE.BoxGeometry(0.16, 0.16, 0.06);
  const refMat = new THREE.MeshStandardMaterial({
    color: 0xffe9b0, emissive: 0xcf9b30, emissiveIntensity: 0.55, roughness: 0.35
  });
  const refs = new THREE.InstancedMesh(refGeo, refMat, nPosts);
  const m4 = new THREE.Matrix4();
  let k = 0;
  for (let i = 0; i < N_SAMPLES; i += 10) {
    for (const sgn of [1, -1]) {
      const s = samples[i];
      const p = s.pos.clone().addScaledVector(s.side, sgn * 6.85);
      m4.makeTranslation(p.x, p.y + 0.62, p.z);
      posts.setMatrixAt(k, m4);
      m4.makeTranslation(p.x, p.y + 1.02, p.z);
      refs.setMatrixAt(k, m4);
      k++;
    }
  }
  posts.instanceMatrix.needsUpdate = true;
  refs.instanceMatrix.needsUpdate = true;
  scene.add(posts, refs);
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
  scene.add(new THREE.Mesh(rg, new THREE.MeshStandardMaterial({
    vertexColors: true, metalness: 0.65, roughness: 0.35, side: THREE.DoubleSide
  })));
}

/* Bridges (2 spans over valleys) */
const BRIDGE_ZONES = [[205, 255], [555, 605]];
{
  const deckMat = new THREE.MeshStandardMaterial({ color: 0x6d7278, roughness: 0.85, metalness: 0.05 });
  const pilMat = new THREE.MeshStandardMaterial({ color: 0x8a8f94, roughness: 0.9 });
  BRIDGE_ZONES.forEach(([a, b]) => {
    for (let i = a; i < b; i += 2) {
      const s = samples[i], s2 = samples[Math.min(i + 2, b)];
      const mid = s.pos.clone().add(s2.pos).multiplyScalar(0.5);
      const ang = Math.atan2(s.tan.x, s.tan.z);
      const deck = new THREE.Mesh(new THREE.BoxGeometry(16.4, 0.7, segLen * 2.3), deckMat);
      deck.position.set(mid.x, mid.y - 0.42, mid.z);
      deck.rotation.y = ang;
      deck.receiveShadow = true;
      scene.add(deck);
    }
    for (let i = a; i < b; i += 16) {
      const s = samples[i];
      for (const sgn of [1, -1]) {
        const p = s.pos.clone().addScaledVector(s.side, sgn * 5.2);
        const h = p.y - terrainH(p.x, p.z) + 0.4;
        if (h > 1.2) {
          const pil = new THREE.Mesh(new THREE.BoxGeometry(1.5, h, 1.5), pilMat);
          pil.position.set(p.x, p.y - 0.7 - h / 2, p.z);
          scene.add(pil);
        }
      }
    }
  });
}

/* Checkpoint gates + start arch */
const GATES = [0, 140, 280, 420, 560, 700];
function buildGate(idx, big) {
  const s = samples[idx];
  const group = new THREE.Group();
  const pillarMat = new THREE.MeshStandardMaterial({ color: 0x22282e, metalness: 0.45, roughness: 0.42 });
  const bannerMat = new THREE.MeshStandardMaterial({
    color: big ? 0xe8b64c : 0x178a5c,
    emissive: big ? 0x6b4e12 : 0x0c3c26, emissiveIntensity: 0.7,
    metalness: 0.35, roughness: 0.35
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
}
GATES.forEach((g, i) => buildGate(g, g === 0));

/* Signboards (EN + Malayalam) */
const glowSigns = [];
function makeSign(text1, text2) {
  const cv = document.createElement('canvas');
  cv.width = 512; cv.height = 256;
  const c2 = cv.getContext('2d');
  c2.fillStyle = '#0e5c3f'; c2.fillRect(0, 0, 512, 256);
  c2.strokeStyle = '#e8b64c'; c2.lineWidth = 10; c2.strokeRect(10, 10, 492, 236);
  c2.fillStyle = '#f5e9c8'; c2.textAlign = 'center';
  c2.font = 'bold 52px Arial'; c2.fillText(text1, 256, 108);
  c2.font = '42px Arial'; c2.fillText(text2, 256, 180);
  const tex = new THREE.CanvasTexture(cv);
  tex.encoding = THREE.sRGBEncoding;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(9, 4.5),
    new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide }));
  glowSigns.push(mesh);
  return mesh;
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
    new THREE.MeshStandardMaterial({ color: 0x6b7076, metalness: 0.4, roughness: 0.5 }));
  post.position.set(p.x, p.y + 1.7, p.z);
  scene.add(post);
});

/* ---------------- 9. Vegetation & environment ---------------- */
function scatterTrees() {
  const qual = save.settings.quality;
  const nTree = qual === 'LOW' ? 220 : qual === 'MED' ? 480 : 820;
  const nPalm = qual === 'LOW' ? 90 : qual === 'MED' ? 190 : 320;

  // merged tree canopy (3 blobs) + straight trunk
  const canopyGeo = mergeGeoms([
    { geo: new THREE.IcosahedronGeometry(2.5, 1) },
    { geo: new THREE.IcosahedronGeometry(1.9, 1), matrix: mat4(0, 0, 0, 1.7, -0.7, 0.6) },
    { geo: new THREE.IcosahedronGeometry(1.7, 1), matrix: mat4(0, 0, 0, -1.5, -0.5, -0.8) }
  ]);
  const trunkGeo = new THREE.CylinderGeometry(0.22, 0.36, 4.6, 7);

  // merged palm: curved trunk + frond crown + coconuts
  const palmTrunkGeo = mergeGeoms([
    { geo: new THREE.CylinderGeometry(0.2, 0.3, 3.4, 7), matrix: mat4(0.06, 0, 0.04, 0, 1.7, 0) },
    { geo: new THREE.CylinderGeometry(0.16, 0.22, 3.2, 7), matrix: mat4(0.12, 0, 0.08, 0.55, 4.8, 0.3) }
  ]);
  const frondParts = [];
  for (let f = 0; f < 8; f++) {
    const ang = (f / 8) * Math.PI * 2;
    frondParts.push({
      geo: new THREE.ConeGeometry(0.75, 4.4, 5),
      matrix: mat4(1.15, ang, 0, Math.sin(ang) * 1.6, 6.8, Math.cos(ang) * 1.6, 1, 0.32, 1)
    });
  }
  for (let c = 0; c < 3; c++) {
    frondParts.push({
      geo: new THREE.SphereGeometry(0.3, 6, 6),
      matrix: mat4(0, 0, 0, Math.sin(c * 2.1) * 0.5, 6.15, Math.cos(c * 2.1) * 0.5)
    });
  }
  const palmTopGeo = mergeGeoms(frondParts);

  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x6b4f2f, roughness: 0.92 });
  const canopyMat = new THREE.MeshStandardMaterial({ color: 0x2c7a3e, roughness: 0.82, flatShading: true });
  const palmMat = new THREE.MeshStandardMaterial({ color: 0x2f8f47, roughness: 0.8, flatShading: true });

  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, nTree);
  const canopies = new THREE.InstancedMesh(canopyGeo, canopyMat, nTree);
  const pTrunks = new THREE.InstancedMesh(palmTrunkGeo, trunkMat, nPalm);
  const pTops = new THREE.InstancedMesh(palmTopGeo, palmMat, nPalm);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3();
  let ti = 0, pi = 0, guard = 0;
  while ((ti < nTree || pi < nPalm) && guard++ < 24000) {
    const x = (Math.random() * 2 - 1) * 820, z = (Math.random() * 2 - 1) * 820;
    if (nearestRoad(x, z).dist < 17) continue;
    const y = terrainH(x, z);
    const isPalm = pi < nPalm && y < 18;
    q.setFromEuler(new THREE.Euler(0, Math.random() * Math.PI * 2, 0));
    if (isPalm) {
      const s = 0.8 + Math.random() * 0.55;
      v.set(x, y, z); sc.set(s, s, s);
      m4.compose(v, q, sc); pTrunks.setMatrixAt(pi, m4);
      m4.compose(v, q, sc); pTops.setMatrixAt(pi, m4);
      pi++;
    } else if (ti < nTree) {
      const s = 0.75 + Math.random() * 0.85;
      v.set(x, y + 2.3 * s, z); sc.set(s, s, s);
      m4.compose(v, q, sc); trunks.setMatrixAt(ti, m4);
      v.set(x, y + 5.4 * s, z); sc.set(s * 1.15, s * 0.95, s * 1.15);
      m4.compose(v, q, sc); canopies.setMatrixAt(ti, m4);
      ti++;
    }
  }
  [trunks, canopies, pTrunks, pTops].forEach(m => {
    m.instanceMatrix.needsUpdate = true;
    if (save.settings.quality === 'HIGH') m.castShadow = true;
    scene.add(m);
  });

  // tea-bush rows on upper slopes (Munnar-style plantations)
  const nBush = qual === 'LOW' ? 200 : qual === 'MED' ? 420 : 700;
  const bushGeo = new THREE.SphereGeometry(0.95, 6, 5);
  const bushMat = new THREE.MeshStandardMaterial({ color: 0x4c9a4f, roughness: 0.9, flatShading: true });
  const bushes = new THREE.InstancedMesh(bushGeo, bushMat, nBush);
  let bi = 0; guard = 0;
  while (bi < nBush && guard++ < 12000) {
    const row = Math.floor(bi / 40);
    const x = (Math.random() * 2 - 1) * 620 + Math.sin(row * 1.7) * 220;
    const z = (Math.random() * 2 - 1) * 620 + Math.cos(row * 1.1) * 220;
    const y = terrainH(x, z);
    if (y < 14 || nearestRoad(x, z).dist < 22) continue;
    const s = 0.7 + Math.random() * 0.6;
    v.set(x, y + 0.35 * s, z); sc.set(s * 1.35, s * 0.62, s * 1.35);
    q.setFromEuler(new THREE.Euler(0, Math.random() * 3, 0));
    m4.compose(v, q, sc);
    bushes.setMatrixAt(bi++, m4);
  }
  bushes.instanceMatrix.needsUpdate = true;
  scene.add(bushes);

  // rocks near bends
  const rockGeo = new THREE.DodecahedronGeometry(0.9, 0);
  const rockMat = new THREE.MeshStandardMaterial({ color: 0x7d8288, roughness: 0.95, flatShading: true });
  const rocks = new THREE.InstancedMesh(rockGeo, rockMat, 120);
  let ri = 0; guard = 0;
  while (ri < 120 && guard++ < 4000) {
    const i = Math.floor(Math.random() * N_SAMPLES);
    const s = samples[i];
    if (s.curv < 0.008) continue;
    const sgn = Math.random() > 0.5 ? 1 : -1;
    const p = s.pos.clone().addScaledVector(s.side, sgn * (9 + Math.random() * 7));
    const y = terrainH(p.x, p.z);
    const sc2 = 0.5 + Math.random() * 1.4;
    v.set(p.x, y + sc2 * 0.3, p.z); sc.set(sc2, sc2 * 0.8, sc2);
    q.setFromEuler(new THREE.Euler(Math.random(), Math.random() * 3, Math.random() * 0.4));
    m4.compose(v, q, sc);
    rocks.setMatrixAt(ri++, m4);
  }
  rocks.instanceMatrix.needsUpdate = true;
  scene.add(rocks);
}
scatterTrees();

/* Kerala village houses + temple + church + shops */
function buildKeralaHouse(scale) {
  const g = new THREE.Group();
  const wallColors = [0xf2ead8, 0xe8dcc0, 0xf5f0e2, 0xded2b8];
  const walls = new THREE.Mesh(new THREE.BoxGeometry(6.2, 3.1, 4.6),
    new THREE.MeshStandardMaterial({ color: wallColors[Math.floor(Math.random() * 4)], roughness: 0.88 }));
  walls.position.y = 1.55;
  walls.castShadow = true;
  g.add(walls);
  // steep tiled roof
  const roof = new THREE.Mesh(new THREE.ConeGeometry(5.1, 2.6, 4),
    new THREE.MeshStandardMaterial({ color: [0x9c3b26, 0x8a4a2e, 0x7c3524][Math.floor(Math.random() * 3)], roughness: 0.82 }));
  roof.position.y = 4.35;
  roof.rotation.y = Math.PI / 4;
  roof.castShadow = true;
  g.add(roof);
  // verandah + pillars
  const ver = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.22, 1.5),
    new THREE.MeshStandardMaterial({ color: 0xcfc4a8, roughness: 0.85 }));
  ver.position.set(0, 0.12, 3.05);
  g.add(ver);
  for (const px of [-2.6, 2.6]) {
    const pil = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 2.7, 6),
      new THREE.MeshStandardMaterial({ color: 0xf0e8d2, roughness: 0.8 }));
    pil.position.set(px, 1.35, 3.55);
    g.add(pil);
  }
  // windows + door
  const winMat = new THREE.MeshStandardMaterial({ color: 0x2c3438, roughness: 0.3, metalness: 0.4 });
  for (const px of [-1.9, 1.9]) {
    const win = new THREE.Mesh(new THREE.BoxGeometry(1.05, 1.15, 0.08), winMat);
    win.position.set(px, 1.85, 2.33);
    g.add(win);
  }
  const door = new THREE.Mesh(new THREE.BoxGeometry(1.15, 2.1, 0.1),
    new THREE.MeshStandardMaterial({ color: 0x5c3a1e, roughness: 0.8 }));
  door.position.set(0, 1.05, 2.33);
  g.add(door);
  g.scale.setScalar(scale || 1);
  return g;
}
function buildTemple() {
  const g = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(7, 4, 7),
    new THREE.MeshStandardMaterial({ color: 0xc96f2e, roughness: 0.8 }));
  base.position.y = 2; base.castShadow = true;
  g.add(base);
  for (let t = 0; t < 3; t++) {
    const tier = new THREE.Mesh(new THREE.ConeGeometry(5 - t * 1.35, 2.2, 4),
      new THREE.MeshStandardMaterial({ color: t === 2 ? 0xd9a441 : 0xb15c28, roughness: 0.75, metalness: t === 2 ? 0.5 : 0.1 }));
    tier.position.y = 5.1 + t * 1.75;
    tier.rotation.y = Math.PI / 4;
    tier.castShadow = true;
    g.add(tier);
  }
  return g;
}
function buildChurch() {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(5.4, 5.2, 8.2),
    new THREE.MeshStandardMaterial({ color: 0xf2efe6, roughness: 0.85 }));
  body.position.y = 2.6; body.castShadow = true;
  g.add(body);
  const tower = new THREE.Mesh(new THREE.BoxGeometry(2.4, 8.4, 2.4),
    new THREE.MeshStandardMaterial({ color: 0xeae4d4, roughness: 0.85 }));
  tower.position.set(0, 4.2, 5.1); tower.castShadow = true;
  g.add(tower);
  const spire = new THREE.Mesh(new THREE.ConeGeometry(1.85, 3.2, 4),
    new THREE.MeshStandardMaterial({ color: 0x8c4a2e, roughness: 0.8 }));
  spire.position.set(0, 10, 5.1); spire.rotation.y = Math.PI / 4;
  g.add(spire);
  const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.18, 1.5, 0.18),
    new THREE.MeshStandardMaterial({ color: 0xd9a441, metalness: 0.6, roughness: 0.35 }));
  crossV.position.set(0, 12.2, 5.1);
  const crossH = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.18, 0.18), crossV.material);
  crossH.position.set(0, 12.45, 5.1);
  g.add(crossV, crossH);
  return g;
}
function buildShop() {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(7.2, 3, 4),
    new THREE.MeshStandardMaterial({ color: [0xe7d9b8, 0xd8c9a6, 0xcfe0d4][Math.floor(Math.random() * 3)], roughness: 0.85 }));
  body.position.y = 1.5; body.castShadow = true;
  g.add(body);
  const awning = new THREE.Mesh(new THREE.BoxGeometry(7.6, 0.16, 1.9),
    new THREE.MeshStandardMaterial({ color: [0x2f7d42, 0xb8402f, 0x2a5f9e][Math.floor(Math.random() * 3)], roughness: 0.7 }));
  awning.position.set(0, 2.65, 2.85);
  awning.rotation.x = 0.16;
  g.add(awning);
  const sign = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.85, 0.12),
    new THREE.MeshStandardMaterial({
      color: [0xe8b64c, 0x178a5c, 0xb8402f][Math.floor(Math.random() * 3)],
      emissive: 0x221800, emissiveIntensity: 0.4
    }));
  sign.position.set(0, 3.35, 2.1);
  g.add(sign);
  return g;
}
{
  for (let i = 0; i < 22; i++) {
    const idx = Math.floor(Math.random() * N_SAMPLES);
    const s = samples[idx];
    const sgn = Math.random() > 0.5 ? 1 : -1;
    const p = s.pos.clone().addScaledVector(s.side, sgn * (15 + Math.random() * 14));
    const y = terrainH(p.x, p.z);
    const r = Math.random();
    let b;
    if (r < 0.62) b = buildKeralaHouse(0.85 + Math.random() * 0.5);
    else if (r < 0.76) b = buildShop();
    else if (r < 0.89) b = buildTemple();
    else b = buildChurch();
    b.position.set(p.x, y, p.z);
    b.rotation.y = Math.atan2(s.tan.x, s.tan.z) + (Math.random() > 0.5 ? 1 : -1) * (Math.PI / 2) + (Math.random() - 0.5) * 0.5;
    scene.add(b);
  }
}

/* Distant mountains — layered ridgelines with aerial perspective */
[[1350, 0x2c5447, 300], [1750, 0x3a6157, 260], [2150, 0x4a7168, 220]].forEach(([dist, col, hBase], layer) => {
  for (let i = 0; i < 12; i++) {
    const ang = (i / 12) * Math.PI * 2 + layer * 0.26 + Math.random() * 0.3;
    const h = hBase + Math.random() * 200;
    const m = new THREE.Mesh(new THREE.ConeGeometry(300 + Math.random() * 230, h, 10),
      new THREE.MeshStandardMaterial({ color: col, roughness: 1, flatShading: true }));
    m.position.set(Math.sin(ang) * (dist + Math.random() * 220), h / 2 - 70, Math.cos(ang) * (dist + Math.random() * 220));
    scene.add(m);
  }
});

/* Drifting clouds */
const cloudMeshes = [];
{
  const puff = mergeGeoms([
    { geo: new THREE.SphereGeometry(16, 10, 8) },
    { geo: new THREE.SphereGeometry(12, 10, 8), matrix: mat4(0, 0, 0, 17, -3, 4) },
    { geo: new THREE.SphereGeometry(11, 10, 8), matrix: mat4(0, 0, 0, -15, -2, -6) },
    { geo: new THREE.SphereGeometry(9, 10, 8), matrix: mat4(0, 0, 0, 5, 5, -12) }
  ]);
  const cloudMat = new THREE.MeshStandardMaterial({
    color: 0xffffff, roughness: 1, transparent: true, opacity: 0.88,
    emissive: 0x8899aa, emissiveIntensity: 0.22, depthWrite: false
  });
  for (let i = 0; i < 14; i++) {
    const c = new THREE.Mesh(puff, cloudMat);
    c.position.set((Math.random() * 2 - 1) * 1900, 180 + Math.random() * 160, (Math.random() * 2 - 1) * 1900);
    c.scale.setScalar(1.2 + Math.random() * 1.8);
    scene.add(c);
    cloudMeshes.push(c);
  }
}

/* ---------------- 10. Vehicles ---------------- */
const VEHICLES = [
  {
    id: 'k10', name: 'Malabar K10', insp: 'inspired by Maruti Suzuki Alto K10', cat: 'Kerala Favourite',
    color: 0xd23a2f, accent: 0x8f1f18, topKmh: 145, accel: 8.6, grip: 1.0, price: 0, kind: 'hatch',
    specs: { Engine: '1.0 L 3-cyl', Power: '68 HP', Torque: '89 Nm', '0\u2013100': '13.9 s', Transmission: '5 MT', Drivetrain: 'FWD', Weight: '730 kg', Fuel: 'Petrol' }
  },
  {
    id: 'tharx', name: 'Ghats Thar-X', insp: 'inspired by Mahindra Thar', cat: 'SUV / Off-road',
    color: 0x3d5232, accent: 0x222e1c, topKmh: 165, accel: 9.8, grip: 0.92, price: 120000, kind: 'suv',
    specs: { Engine: '2.2 L turbo diesel', Power: '130 HP', Torque: '300 Nm', '0\u2013100': '10.2 s', Transmission: '6 MT', Drivetrain: '4x4', Weight: '1,750 kg', Fuel: 'Diesel' }
  },
  {
    id: 'gtr', name: 'Rush GT-R', insp: 'inspired by Nissan GT-R', cat: 'Premium Hyper',
    color: 0x9aa7b4, accent: 0x2c3a4a, topKmh: 230, accel: 14.2, grip: 1.14, price: 350000, kind: 'sport',
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

/* Detailed procedural vehicle — front faces local +Z */
function buildCar(colorHex, kind, detail) {
  const hi = detail !== 'low';
  const g = new THREE.Group();
  const paint = new THREE.MeshPhysicalMaterial({
    color: colorHex, metalness: 0.72, roughness: 0.3,
    clearcoat: 1, clearcoatRoughness: 0.08
  });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x16181b, metalness: 0.4, roughness: 0.55 });
  const glassMat = new THREE.MeshPhysicalMaterial({
    color: 0x18242e, metalness: 0.1, roughness: 0.06,
    clearcoat: 1, clearcoatRoughness: 0.03, transparent: true, opacity: 0.86
  });
  const chromeMat = new THREE.MeshStandardMaterial({ color: 0xd8dde2, metalness: 1, roughness: 0.16 });
  const tireMat = new THREE.MeshStandardMaterial({ color: 0x121417, roughness: 0.94 });
  const rimMat = new THREE.MeshStandardMaterial({ color: 0xb9c0c8, metalness: 1, roughness: 0.28 });
  const headMat = new THREE.MeshStandardMaterial({
    color: 0xfff8e0, emissive: 0xffedb0, emissiveIntensity: 0.95, roughness: 0.2
  });
  const tailMat = new THREE.MeshStandardMaterial({
    color: 0xff2a1e, emissive: 0xd41b0f, emissiveIntensity: 0.85, roughness: 0.25
  });

  let dims;
  if (kind === 'bus') dims = { len: 8.6, wid: 2.5, bodyH: 1.55, cabH: 1.25, wr: 0.52 };
  else if (kind === 'auto') dims = { len: 2.7, wid: 1.55, bodyH: 0.95, cabH: 0.85, wr: 0.3 };
  else if (kind === 'bike') dims = { len: 2.15, wid: 0.72, bodyH: 0.55, cabH: 0.5, wr: 0.32 };
  else if (kind === 'suv') dims = { len: 4.55, wid: 2.05, bodyH: 0.95, cabH: 0.85, wr: 0.44 };
  else if (kind === 'sport') dims = { len: 4.5, wid: 2.0, bodyH: 0.62, cabH: 0.52, wr: 0.38 };
  else dims = { len: 3.85, wid: 1.85, bodyH: 0.68, cabH: 0.58, wr: 0.35 };

  const wheels = [];
  const addWheel = (x, z, r, front) => {
    const pivot = new THREE.Group();
    pivot.position.set(x, r, z);
    const tire = new THREE.Mesh(new THREE.CylinderGeometry(r, r, r * 0.68, hi ? 18 : 10), tireMat);
    tire.rotation.z = Math.PI / 2;
    tire.castShadow = true;
    pivot.add(tire);
    if (hi) {
      const rim = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.62, r * 0.62, r * 0.7, 12), rimMat);
      rim.rotation.z = Math.PI / 2;
      pivot.add(rim);
      for (let sp = 0; sp < 5; sp++) {
        const spoke = new THREE.Mesh(new THREE.BoxGeometry(r * 0.7, r * 0.16, r * 0.1), rimMat);
        spoke.position.x = x > 0 ? r * 0.36 : -r * 0.36;
        spoke.rotation.x = (sp / 5) * Math.PI * 2;
        spoke.rotation.y = Math.PI / 2;
        spoke.rotation.z = Math.PI / 2;
        pivot.add(spoke);
      }
    }
    g.add(pivot);
    wheels.push({ pivot, mesh: tire, front });
  };

  if (kind === 'bike') {
    // motorcycle: slim body, inline wheels, rider silhouette
    addWheel(0, dims.len * 0.38, dims.wr, true);
    addWheel(0, -dims.len * 0.36, dims.wr * 1.08, false);
    const tank = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.34, 1.05), paint);
    tank.position.set(0, 0.82, 0.12);
    tank.castShadow = true;
    g.add(tank);
    const seat = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.18, 0.95), darkMat);
    seat.position.set(0, 0.92, -0.62);
    g.add(seat);
    const fork = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.85, 0.12), chromeMat);
    fork.position.set(0, 0.75, dims.len * 0.3);
    fork.rotation.x = -0.5;
    g.add(fork);
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.08, 0.08), chromeMat);
    bar.position.set(0, 1.18, dims.len * 0.24);
    g.add(bar);
    const riderTorso = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.62, 0.38), darkMat);
    riderTorso.position.set(0, 1.36, -0.18);
    riderTorso.rotation.x = 0.32;
    riderTorso.castShadow = true;
    const riderHead = new THREE.Mesh(new THREE.SphereGeometry(0.21, 10, 10),
      new THREE.MeshStandardMaterial({ color: 0x22262c, metalness: 0.5, roughness: 0.3 }));
    riderHead.position.set(0, 1.82, 0.02);
    g.add(riderTorso, riderHead);
    const hl = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), headMat);
    hl.position.set(0, 0.95, dims.len * 0.42);
    const tl = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.1, 0.06), tailMat);
    tl.position.set(0, 0.95, -dims.len * 0.46);
    g.add(hl, tl);
    return { group: g, wheels, dims, radius: 1.25, kind };
  }

  /* --- car-like bodies: extruded side profile + detail parts --- */
  const L = dims.len, W = dims.wid, BH = dims.bodyH, CH = dims.cabH;
  const isSport = kind === 'sport', isSUV = kind === 'suv', isBus = kind === 'bus', isAuto = kind === 'auto';

  // side profile (x = along length, y = height) — front at +Z after rotation
  const prof = new THREE.Shape();
  const nose = L / 2, tail = -L / 2;
  const hoodY = BH + 0.52, roofY = BH + 0.52 + CH;
  if (isBus) {
    prof.moveTo(tail, 0.28);
    prof.lineTo(tail, roofY);
    prof.lineTo(nose * 0.94, roofY);
    prof.lineTo(nose, roofY - 0.45);
    prof.lineTo(nose, 0.28);
  } else {
    prof.moveTo(tail, 0.28);
    prof.lineTo(tail, hoodY - (isSport ? 0.12 : 0.3));
    prof.lineTo(tail + L * 0.16, roofY - (isSport ? 0.2 : 0.04));
    prof.lineTo(tail + L * 0.46, roofY);
    prof.lineTo(nose - L * (isSport ? 0.3 : 0.36), roofY - 0.04);
    prof.lineTo(nose - L * 0.1, hoodY - (isSport ? 0.22 : 0.08));
    prof.lineTo(nose, hoodY - (isSport ? 0.4 : 0.26));
    prof.lineTo(nose, 0.28);
  }
  prof.closePath();
  const bodyGeo = new THREE.ExtrudeGeometry(prof, {
    depth: W * 0.82, bevelEnabled: true, bevelThickness: 0.09, bevelSize: 0.1, bevelSegments: 2, steps: 1
  });
  // extrude runs +Z depth; rotate so profile length lies along Z and width along X
  const bodyMesh = new THREE.Mesh(bodyGeo, paint);
  bodyMesh.rotation.y = Math.PI / 2;
  bodyMesh.position.set(-W * 0.41, 0, 0);
  bodyMesh.castShadow = true;
  bodyMesh.receiveShadow = true;
  g.add(bodyMesh);

  // glasshouse (cabin) — slightly narrower, dark glass
  if (!isAuto) {
    const glassProf = new THREE.Shape();
    const gx0 = tail + L * 0.14, gx1 = nose - L * 0.3;
    glassProf.moveTo(gx0 + L * 0.05, roofY - 0.3);
    glassProf.lineTo(gx0 + L * 0.14, roofY + 0.12);
    glassProf.lineTo(gx1 - L * 0.08, roofY + 0.12);
    glassProf.lineTo(gx1, roofY - 0.3);
    glassProf.closePath();
    const glassGeo = new THREE.ExtrudeGeometry(glassProf, {
      depth: W * 0.72, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 1, steps: 1
    });
    const glass = new THREE.Mesh(glassGeo, glassMat);
    glass.rotation.y = Math.PI / 2;
    glass.position.set(-W * 0.36, 0, 0);
    g.add(glass);
    // window chrome trim
    if (hi) {
      const trim = new THREE.Mesh(new THREE.BoxGeometry(W * 0.78, 0.06, L * 0.42), chromeMat);
      trim.position.set(0, roofY - 0.26, -L * 0.02);
      g.add(trim);
    }
  }

  // grille + front bumper (front = +Z)
  const grille = new THREE.Mesh(new THREE.BoxGeometry(W * 0.66, BH * 0.5, 0.16), darkMat);
  grille.position.set(0, 0.55 + BH * 0.25, nose + 0.02);
  g.add(grille);
  const frontBumper = new THREE.Mesh(new THREE.BoxGeometry(W * 0.96, BH * 0.36, 0.34),
    isSport ? paint : darkMat);
  frontBumper.position.set(0, 0.42, nose - 0.02);
  frontBumper.castShadow = true;
  g.add(frontBumper);
  const rearBumper = new THREE.Mesh(new THREE.BoxGeometry(W * 0.96, BH * 0.36, 0.32),
    isSport ? paint : darkMat);
  rearBumper.position.set(0, 0.42, tail + 0.02);
  g.add(rearBumper);

  // headlights / taillights
  for (const sgn of [1, -1]) {
    const hl = new THREE.Mesh(new THREE.BoxGeometry(W * 0.26, 0.17, 0.12), headMat);
    hl.position.set(sgn * W * 0.3, 0.55 + BH * 0.42, nose + 0.05);
    const tl = new THREE.Mesh(new THREE.BoxGeometry(W * 0.3, 0.16, 0.1), tailMat);
    tl.position.set(sgn * W * 0.28, 0.6 + BH * 0.5, tail - 0.04);
    g.add(hl, tl);
  }
  if (isSport) {
    // light-bar strip across the tail
    const bar = new THREE.Mesh(new THREE.BoxGeometry(W * 0.8, 0.08, 0.08), tailMat);
    bar.position.set(0, 0.72, tail - 0.05);
    g.add(bar);
  }

  // mirrors
  if (hi && !isAuto) {
    for (const sgn of [1, -1]) {
      const arm = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.06, 0.06), darkMat);
      arm.position.set(sgn * (W * 0.52), hoodY + 0.12, L * 0.14);
      const cap = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.16, 0.24), paint);
      cap.position.set(sgn * (W * 0.62), hoodY + 0.14, L * 0.14);
      g.add(arm, cap);
    }
  }

  // exhausts
  if (hi && !isBus && !isAuto) {
    for (const sgn of (isSport ? [1, -1] : [1])) {
      const ex = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.3, 8), chromeMat);
      ex.rotation.x = Math.PI / 2;
      ex.position.set(sgn * W * 0.3, 0.38, tail - 0.16);
      g.add(ex);
    }
  }

  // roof rails (SUV) / stripe (bus)
  if (isSUV) {
    for (const sgn of [1, -1]) {
      const rail = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, L * 0.42), darkMat);
      rail.position.set(sgn * W * 0.32, roofY + 0.2, -L * 0.03);
      g.add(rail);
    }
  }
  if (isBus) {
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(W * 0.87, 0.3, L * 0.96),
      new THREE.MeshStandardMaterial({ color: 0xf2ead8, roughness: 0.6 }));
    stripe.position.set(0, 0.52 + BH * 0.62, 0);
    g.add(stripe);
    const band = new THREE.Mesh(new THREE.BoxGeometry(W * 0.87, 0.16, L * 0.96),
      new THREE.MeshStandardMaterial({ color: 0x2a5f9e, roughness: 0.6 }));
    band.position.set(0, 0.5 + BH * 0.26, 0);
    g.add(band);
    for (let w = -2; w <= 2; w++) {
      for (const sgn of [1, -1]) {
        const win = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.75, 1.15), glassMat);
        win.position.set(sgn * (W * 0.44), 0.62 + BH * 0.66, w * 1.55);
        g.add(win);
      }
    }
  }
  if (isAuto) {
    const canopy = new THREE.Mesh(new THREE.BoxGeometry(W * 0.92, 0.08, L * 0.62),
      new THREE.MeshStandardMaterial({ color: 0x2c2c2c, roughness: 0.85 }));
    canopy.position.set(0, 0.95 + BH * 0.55, -L * 0.08);
    g.add(canopy);
    const hood = new THREE.Mesh(new THREE.BoxGeometry(W * 0.8, 0.5, L * 0.3), paint);
    hood.position.set(0, 0.62, L * 0.3);
    g.add(hood);
  }

  // underbody + wheel arches
  const under = new THREE.Mesh(new THREE.BoxGeometry(W * 0.86, 0.16, L * 0.88), darkMat);
  under.position.set(0, 0.3, 0);
  g.add(under);

  // wheels
  const wr = dims.wr;
  const wz = isBus ? L * 0.33 : L * 0.31;
  const wx = W * 0.48;
  addWheel(-wx, wz, wr, true);
  addWheel(wx, wz, wr, true);
  addWheel(-wx, -wz, wr, false);
  addWheel(wx, -wz, wr, false);

  const radius = Math.max(L, W) * 0.46;
  return { group: g, wheels, dims, radius, kind };
}

/* Player */
const playerDef = () => VEHICLES.find(v => v.id === save.selected) || VEHICLES[0];
let playerCar = buildCar(playerDef().color, playerDef().kind, 'high');
scene.add(playerCar.group);
const player = {
  heading: 0, speed: 0, slide: 0, nitro: 100, lap: 0, idx: 0, prevIdx: 0,
  lapStart: 0, bestLap: 0, raceTime: 0, finished: false, bodyRoll: 0, bodyPitch: 0
};
function respawnPlayer() {
  const s = samples[2];
  playerCar.group.position.set(s.pos.x, s.pos.y + 0.05, s.pos.z);
  player.heading = Math.atan2(s.tan.x, s.tan.z);
  player.speed = 0; player.slide = 0;
  player.idx = 2; player.prevIdx = 2; player.lap = 0;
  player.raceTime = 0; player.lapStart = 0; player.finished = false;
}
respawnPlayer();

/* Night headlights: glow cones + spotlights */
function attachHeadlights() {
  headlightGroup = new THREE.Group();
  const coneMat = new THREE.MeshBasicMaterial({
    color: 0xfff2b8, transparent: true, opacity: 0.13, depthWrite: false
  });
  for (const sgn of [1, -1]) {
    const cone = new THREE.Mesh(new THREE.ConeGeometry(1.5, 12, 12, 1, true), coneMat);
    cone.rotation.x = -Math.PI / 2;
    cone.position.set(sgn * 0.72, 0.72, 6.2);
    headlightGroup.add(cone);
    const spot = new THREE.SpotLight(0xfff0c2, 1.1, 60, 0.5, 0.55, 1.2);
    spot.position.set(sgn * 0.72, 0.78, playerCar.dims.len / 2);
    spot.target.position.set(sgn * 0.72, 0.3, playerCar.dims.len / 2 + 26);
    playerCar.group.add(spot, spot.target);
    headSpots.push(spot);
  }
  headlightGroup.visible = false;
  playerCar.group.add(headlightGroup);
}
attachHeadlights();

/* Nitro flames */
const nitroFlames = [];
{
  const flameMat = new THREE.MeshBasicMaterial({
    color: 0x66d4ff, transparent: true, opacity: 0.85, depthWrite: false
  });
  for (const sgn of [1, -1]) {
    const flame = new THREE.Mesh(new THREE.ConeGeometry(0.14, 1.1, 8), flameMat);
    flame.rotation.x = Math.PI / 2;
    flame.position.set(sgn * 0.34, 0.42, -playerCar.dims.len / 2 - 0.5);
    flame.visible = false;
    playerCar.group.add(flame);
    nitroFlames.push(flame);
  }
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
    const car = buildCar(d.color, i === 2 ? 'sport' : 'hatch', save.settings.quality === 'LOW' ? 'low' : 'high');
    scene.add(car.group);
    aiCars.push({
      car, def: d, s: -6 - i * 7, lap: 0, speed: 0,
      lane: (i % 2 === 0 ? 1 : -1) * 2.2, finished: false, _cool: -9
    });
  });
}
buildAI();

/* Traffic: Kerala buses, autos, cars, bikes — LEFT-hand traffic (passing on left) */
const traffic = [];
function buildTraffic() {
  traffic.forEach(t => scene.remove(t.car.group));
  traffic.length = 0;
  const kinds = ['car', 'auto', 'bus', 'bike', 'car', 'auto', 'bus', 'bike', 'car', 'car'];
  const cols = [0xc9b08c, 0xf2c230, 0x2f7d42, 0x22262c, 0x8899aa, 0xf2c230, 0xe0772c, 0x335577, 0xd23a2f, 0x6b7076];
  for (let i = 0; i < 10; i++) {
    const car = buildCar(cols[i], kinds[i], 'low');
    scene.add(car.group);
    traffic.push({
      car, kind: kinds[i], s: Math.floor((i / 10) * N_SAMPLES),
      speed: kinds[i] === 'bus' ? 13 : kinds[i] === 'auto' ? 11 : kinds[i] === 'bike' ? 19 : 17 + Math.random() * 4,
      lane: (i % 2 === 0 ? 1 : -1) * 2.4, _cool: -9
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
let state = 'MENU';
let gameMode = 'RACE';
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

/* ---------------- 12. Collision system (v1.1 — no sticking) ---------------- */
const _colN = new THREE.Vector3();
function resolveCollision(playerPos, otherGroup, otherRadius, otherObj, isAI, dt) {
  const dx = playerPos.x - otherGroup.position.x;
  const dz = playerPos.z - otherGroup.position.z;
  const rr = playerCar.radius + otherRadius;
  const d2 = dx * dx + dz * dz;
  if (d2 >= rr * rr) return false;
  const d = Math.sqrt(d2) || 0.001;
  // normal from other -> player
  _colN.set(dx / d, 0, dz / d);
  const overlap = rr - d;
  // 1) full positional separation: player pushed out completely, other nudged back
  playerPos.addScaledVector(_colN, overlap * 1.02);
  otherGroup.position.addScaledVector(_colN, -overlap * 0.35);
  // 2) velocity response: remove approach speed, gentle bounce (never zeroes motion)
  const vx = Math.sin(player.heading) * player.speed;
  const vz = Math.cos(player.heading) * player.speed;
  const approach = vx * _colN.x + vz * _colN.z; // negative = closing in
  if (approach < 0) {
    player.speed += -approach * 0.85;            // cancel most of the approach component
    player.speed = Math.max(player.speed, -6);   // never lock: reversing always possible
    if (isAI && otherObj) otherObj.speed = Math.max(6, otherObj.speed - (-approach) * 0.22);
    // slight deflection: angle the car away from the obstacle (slide, not trap)
    player.slide += (Math.sin(player.heading) * _colN.z - Math.cos(player.heading) * _colN.x > 0 ? 1 : -1) * 0.12;
  }
  // 3) sound with cooldown
  const now = player.raceTime;
  if (!otherObj || now - (otherObj._cool || -9) > 0.7) {
    AudioSys.thump();
    if (otherObj) otherObj._cool = now;
  }
  return true;
}

/* ---------------- 13. Physics & race logic ---------------- */
const tmpV = new THREE.Vector3();
const tmpV2 = new THREE.Vector3();
function updateGame(dt) {
  const v = playerDef();
  const st = statOf(v);
  const frozen = state === 'COUNT';

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

  /* --- driving inputs --- */
  const throttle = frozen ? 0 : (input.up ? 1 : 0);
  const brake = frozen ? 0 : (input.down ? 1 : 0);
  const nitroActive = !frozen && input.nitro && player.nitro > 1 && player.speed > 5;
  const boost = nitroActive ? 1.32 : 1;

  /* acceleration with power curve; braking; reverse */
  const powerCurve = 1 - Math.pow(clamp(Math.abs(player.speed) / (st.top * 1.02), 0, 1), 2) * 0.42;
  player.speed += (throttle * st.accel * boost * powerCurve
    - brake * (player.speed > 0.5 ? 16 : 6)
    - player.speed * 0.05
    - player.speed * Math.abs(player.speed) * 0.00042) * dt;
  if (brake && player.speed < 0.6 && !throttle) player.speed = Math.max(player.speed - 7 * dt, -8);
  if (!throttle && !brake && Math.abs(player.speed) > 0) {
    player.speed -= Math.sign(player.speed) * Math.min(Math.abs(player.speed), 2.4 * dt);
  }
  const maxSpeed = nitroActive ? st.top * 1.15 : st.top;
  player.speed = clamp(player.speed, -8, maxSpeed);

  /* nitro */
  if (nitroActive) {
    player.nitro = Math.max(0, player.nitro - 26 * dt);
    if (!player._whooshed) { AudioSys.whoosh(); player._whooshed = true; }
    nitroFlames.forEach((f, i) => {
      f.visible = true;
      const flick = 0.85 + Math.sin(player.raceTime * 34 + i * 2.2) * 0.35;
      f.scale.set(flick, flick * (1.1 + player.speed * 0.012), flick);
    });
  } else {
    player.nitro = Math.min(100, player.nitro + 5.5 * dt);
    player._whooshed = false;
    nitroFlames.forEach(f => { f.visible = false; });
  }

  /* steering — A = LEFT, D = RIGHT (screen-relative, v1.1 fix) */
  const steer = frozen ? 0 : ((input.left ? -1 : 0) + (input.right ? 1 : 0));
  const absSp = Math.abs(player.speed);
  const speedFactor = 0.34 + 0.66 * clamp(absSp / 16, 0, 1);
  const highSpeedDamp = 1 / (1 + absSp * 0.011);
  const steerRate = 1.62 * speedFactor * highSpeedDamp * st.grip * (input.hand ? 1.55 : 1);
  player.heading -= steer * steerRate * dt * Math.sign(player.speed || 1);
  const targetSlide = input.hand && absSp > 8 ? steer * 0.8 : 0;
  player.slide = lerp(player.slide, targetSlide, dt * (input.hand ? 2.2 : 3.4));

  /* movement with substeps (prevents tunneling through vehicles at speed) */
  const moveDir = player.heading + player.slide;
  const stepDist = player.speed * dt;
  const nSteps = clamp(Math.ceil(Math.abs(stepDist) / 1.6), 1, 4);
  const sdt = dt / nSteps;
  const px = playerCar.group.position;
  for (let s = 0; s < nSteps; s++) {
    px.x += Math.sin(moveDir) * player.speed * sdt;
    px.z += Math.cos(moveDir) * player.speed * sdt;
    /* vehicle collisions inside substep: AI + traffic */
    for (let i = 0; i < aiCars.length; i++) {
      resolveCollision(px, aiCars[i].car.group, aiCars[i].car.radius, aiCars[i], true, sdt);
    }
    for (let i = 0; i < traffic.length; i++) {
      resolveCollision(px, traffic[i].car.group, traffic[i].car.radius, traffic[i], false, sdt);
    }
  }

  /* road follow & off-road */
  const r = nearestRoad(px.x, px.z);
  let targetY = r.pos.y + 0.02;
  if (r.dist > 30) targetY = terrainH(px.x, px.z) + 0.02;
  px.y = lerp(px.y, targetY, clamp(dt * 7, 0, 1));
  if (r.dist > 8.2 && !frozen) player.speed *= (1 - 0.85 * dt);

  /* orientation + suspension-style body lean */
  playerCar.group.rotation.y = player.heading;
  const rollTarget = -steer * speedFactor * 0.05 - player.slide * 0.12;
  const pitchTarget = clamp((-throttle * 0.02 + brake * 0.026) * clamp(absSp / 12, 0, 1), -0.035, 0.035);
  player.bodyRoll = lerp(player.bodyRoll, rollTarget, dt * 5.5);
  player.bodyPitch = lerp(player.bodyPitch, pitchTarget, dt * 4.5);
  playerCar.group.rotation.z = player.bodyRoll;
  playerCar.group.rotation.x = player.bodyPitch;

  /* wheels: spin + steering pivots */
  const spin = player.speed / (playerCar.dims.wr || 0.38) * dt;
  playerCar.wheels.forEach(w => {
    w.mesh.rotation.x += spin;
    if (w.front) w.pivot.rotation.y = -steer * 0.42 * speedFactor;
  });

  /* progress & laps */
  player.prevIdx = player.idx;
  player.idx = r.idx;
  if (player.prevIdx > N_SAMPLES - 80 && player.idx < 80 && player.speed > 2) {
    player.lap++;
    const lapTime = player.raceTime - player.lapStart;
    player.lapStart = player.raceTime;
    if (lapTime > 2) {
      if (player.bestLap === 0 || lapTime < player.bestLap) {
        player.bestLap = lapTime;
        showMsg('BEST LAP ' + fmtTime(lapTime), 2);
      }
      AudioSys.blip(990, 0.14); setTimeout(() => AudioSys.blip(1318, 0.2), 150);
    }
    if (gameMode !== 'FREE' && player.lap >= (gameMode === 'TIME' ? 1 : 3)) {
      player.finished = true;
      finishRace();
      return;
    }
    showMsg('LAP ' + (player.lap + 1) + (gameMode === 'TIME' ? '' : ' / 3'), 1.6);
  }
  if (!frozen && state !== 'RESULTS') player.raceTime += dt;

  /* AI */
  aiCars.forEach((a) => {
    if (a.finished) return;
    const i0 = ((Math.floor(a.s) % N_SAMPLES) + N_SAMPLES) % N_SAMPLES;
    const curv = samples[i0].curv;
    let target = a.def.skill * (1 - clamp(curv * 26, 0, 0.52));
    const playerProg = player.lap * N_SAMPLES + player.idx;
    const aiProg = a.lap * N_SAMPLES + (a.s % N_SAMPLES);
    if (aiProg < playerProg - 120) target *= 1.06;
    if (aiProg > playerProg + 160) target *= 0.94;
    a.speed = lerp(a.speed, target, dt * 1.1);
    a.s += (a.speed * dt) / segLen;
    if (a.s >= N_SAMPLES) { a.s -= N_SAMPLES; a.lap++; }
    placeOnRoad(a.car, a.s, a.lane, 0.02);
    const spinAI = a.speed / (a.car.dims.wr || 0.38) * dt;
    a.car.wheels.forEach(w => { w.mesh.rotation.x += spinAI; });
  });

  /* traffic */
  traffic.forEach(t => {
    t.s += (t.speed * dt) / segLen;
    if (t.s >= N_SAMPLES) t.s -= N_SAMPLES;
    placeOnRoad(t.car, t.s, t.lane, 0.02);
    const spinT = t.speed / (t.car.dims.wr || 0.38) * dt;
    t.car.wheels.forEach(w => { w.mesh.rotation.x += spinT; });
  });

  /* sun follows player for tight shadows */
  sun.position.set(px.x + 70, px.y + 130, px.z + 45);
  sun.target.position.copy(px);
  sun.target.updateMatrixWorld();

  AudioSys.engine(absSp, throttle, nitroActive);
}

/* ---------------- 14. Camera ---------------- */
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
  let desired = tmpV2;
  if (camMode === 0) desired.set(p.x - fwd.x * 9.5, p.y + 3.6 + speedK * 0.8, p.z - fwd.z * 9.5);
  else if (camMode === 1) desired.set(p.x + fwd.x * 0.4, p.y + 1.55, p.z + fwd.z * 0.4);
  else if (camMode === 2) desired.set(p.x + fwd.x * 0.1, p.y + 1.22, p.z + fwd.z * 0.1);
  else desired.set(p.x - fwd.x * 15, p.y + 7.5, p.z - fwd.z * 15);
  const k = 1 - Math.exp(-dt * (camMode >= 1 && camMode <= 2 ? 14 : 5.5));
  camera.position.lerp(desired, k);
  const lookTarget = tmpV.clone().set(p.x + fwd.x * 14, p.y + 1.6, p.z + fwd.z * 14);
  camLook.lerp(lookTarget, 1 - Math.exp(-dt * 8));
  camera.lookAt(camLook);
  /* cinematic drift roll */
  camera.rotateZ(clamp(player.slide * 0.05, -0.05, 0.05));
  const targetFov = 64 + (input.nitro && player.nitro > 1 ? 12 * speedK + 6 : 0) + speedK * 5;
  camera.fov = lerp(camera.fov, targetFov, dt * 3.2);
  camera.updateProjectionMatrix();
  if (save.settings.weather === 'RAIN' && Math.abs(player.speed) > 20) {
    camera.position.x += (Math.random() - 0.5) * 0.04;
    camera.position.y += (Math.random() - 0.5) * 0.04;
  }
}

/* ---------------- 15. Rain ---------------- */
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

/* clouds drift */
function updateClouds(dt) {
  cloudMeshes.forEach((c, i) => {
    c.position.x += dt * (1.6 + (i % 3) * 0.7);
    if (c.position.x > 2100) c.position.x = -2100;
  });
}

/* ---------------- 16. HUD & minimap ---------------- */
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

/* ---------------- 17. Garage UI ---------------- */
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
  headSpots.length = 0;
  nitroFlames.length = 0;
  const v = playerDef();
  playerCar = buildCar(v.color, v.kind, 'high');
  scene.add(playerCar.group);
  attachHeadlights();
  const flameMat = new THREE.MeshBasicMaterial({ color: 0x66d4ff, transparent: true, opacity: 0.85, depthWrite: false });
  for (const sgn of [1, -1]) {
    const flame = new THREE.Mesh(new THREE.ConeGeometry(0.14, 1.1, 8), flameMat);
    flame.rotation.x = Math.PI / 2;
    flame.position.set(sgn * 0.34, 0.42, -playerCar.dims.len / 2 - 0.5);
    flame.visible = false;
    playerCar.group.add(flame);
    nitroFlames.push(flame);
  }
  applyEnvironment();
  respawnPlayer();
}

/* ---------------- 18. UI wiring ---------------- */
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
seg('seg-quality', 'quality');
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
    persist(); applyLang(); rebuildPlayerCar();
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

/* ---------------- 19. Quality ---------------- */
function applyQuality() {
  const q = save.settings.quality;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, q === 'LOW' ? 1 : q === 'MED' ? 1.5 : 1.75));
  renderer.shadowMap.enabled = q !== 'LOW';
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  sun.castShadow = q !== 'LOW';
  if (q === 'HIGH') sun.shadow.mapSize.set(3072, 3072);
}

/* ---------------- 20. Main loop ---------------- */
const clock = new THREE.Clock();
function loop() {
  requestAnimationFrame(loop);
  const dt = Math.min(clock.getDelta(), 0.05);
  if (state === 'RACE' || state === 'FREEROAM' || state === 'COUNT') {
    updateGame(dt);
    updateRain(dt);
    updateClouds(dt);
    updateHUD();
    if (state === 'PAUSED') AudioSys.silence();
  } else {
    if (playerCar.wheels) playerCar.wheels.forEach(w => { w.mesh.rotation.x += dt * 0.6; });
    if (AudioSys.ctx) AudioSys.silence();
    updateRain(dt);
    updateClouds(dt);
  }
  updateCamera(dt);
  renderer.render(scene, camera);
}

/* ---------------- 21. Boot ---------------- */
applyQuality();
applyEnvironment();
applyLang();
showScreen('screen-menu');
hudVisible(false);
document.getElementById('btn-mute').textContent = AudioSys.muted ? '\uD83D\uDD07' : '\uD83D\uDD0A';
loop();
