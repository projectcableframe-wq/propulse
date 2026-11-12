# MALABAR RUSH — Game Design Document
**Episode 1: Thamarassery Churam**
Created by **Hadee Mohammed** · One State. Fourteen Districts. Unlimited Speed.

---

## 1. Vision
A next-generation 3D open-world arcade racing game set in Kerala — the complete
14-district map, connected highways, iconic vehicles, dynamic weather, and the
cinematic feel of Asphalt / Forza Horizon / NFS Heat, with its own original
identity, UI, map and assets (no copyrighted content reproduced).

## 2. Scope honesty (read this first)
The full vision (14 districts · 15+ vehicles · living traffic · full weather ·
career mode) is a **large studio-scale project** — the roadmap in §8 breaks it
into episodes. **This release = Episode 1 MVP**: one complete, polished,
bug-free playable slice — the legendary **Thamarassery Churam** mountain pass —
which proves every core system (driving, racing, garage, weather, day/night,
traffic, HUD, save) and becomes the foundation for all 14 districts.

## 3. Tech stack
- **Three.js r147 (UMD, vendored locally)** — runs offline, double-click `index.html`, no CDN
- WebGL 2 renderer · adaptive resolution · ACES tone mapping · fog
- Fully **procedural assets** (no external model/texture downloads → zero missing-file errors)
- Vanilla JS + HTML/CSS UI · WebAudio procedural sound · localStorage saves
- Platforms: **Chrome / Edge / Firefox / Safari (desktop + iPhone/Android touch)**

## 4. Episode 1 content
| System | MVP content |
|---|---|
| Map | **Thamarassery Churam circuit** — climbing hairpin pass, misty hills, palm valleys, tea-garden slopes, signboards (EN + മലയാളം), guardrails, checkpoints |
| Vehicles | 3 driveable (see §5), each with spec card + upgrades |
| Modes | **Churam Circuit** (3-lap race vs 3 AI), **Time Trial**, **Free Roam** (+ traffic) |
| Weather | Clear · Mist · Rain-lite (wet fog + rain particles) |
| Time | Day · Sunset · Night (headlight mood) |
| Audio | Procedural engine, tyre screech, nitro, collisions, UI · mute toggle |
| HUD | Speedometer, nitro bar, lap/checkpoint timer, race position, minimap |
| Controls | Keyboard (WASD/arrows, Space handbrake, Shift nitro, C camera, R reset, Esc pause) + full **touch controls** |
| Save | Money, owned cars, upgrades, best lap, settings (localStorage) |

## 5. Vehicles (Episode 1)
> Commercial names/likenesses are **not reproduced**. These are original,
> lightly-fictionalised vehicles *inspired by* the brief's favourites.
> All performance figures are **game-adjusted stats**.

| Vehicle | Inspired by | Category | Top speed | Accel | Handling | Price |
|---|---|---|---|---|---|---|
| **Malabar K10** | Maruti Suzuki Alto K10 | Kerala favourite | 145 km/h | ★★☆ | ★★★ | ₹0 (starter) |
| **Ghats Thar-X** | Mahindra Thar | SUV / off-road | 165 km/h | ★★★ | ★★☆ | ₹120,000 |
| **Rush GT-R** | Nissan GT-R | Premium hyper | 230 km/h | ★★★★★ | ★★★★ | ₹350,000 |

Upgrades (3 levels each): **Engine · Turbo · Tyres** — bought with race winnings.

## 6. Core loop
Select vehicle → Race / Free Roam → earn ₹ + reputation → upgrade & unlock cars →
beat best laps → become the Churam Champion → *(roadmap: next districts)*

## 7. Art & audio bible
- **Palette:** deep forest green · tropical emerald · ocean blue · sunset orange · asphalt black · metallic silver
- **Mood:** fast, adventurous, cinematic, premium, distinctly Kerala
- **UI identity:** dark premium chrome, gold-leaf accents, Kerala green
- **Audio:** engine-led, subtle ambience, Malayalam-infused signage culture

## 8. Roadmap — the complete Kerala
| Ep | District | Hero location | Status |
|---|---|---|---|
| **1** | **Kozhikode ↔ Wayanad** | **Thamarassery Churam** | ✅ **THIS BUILD** |
| 2 | Idukki | Munnar tea-garden hairpins | planned |
| 3 | Ernakulam | Kochi city street racing | planned |
| 4 | Thiruvananthapuram | Kovalam coastal run | planned |
| 5 | Alappuzha | Alleppey backwater bridges | planned |
| 6 | Thrissur | Athirappilly waterfall road | planned |
| 7–14 | Kollam, Pathanamthitta, Kottayam, Palakkad, Malappuram, Kannur, Kasaragod + connective open-world highways | 42 destinations, 15+ vehicles, boss races, career | planned |

Each new episode ships as an **expansion of the same world** — one continuous
connected Kerala map, exactly as the brief demands.

## 9. QA checklist (every build)
- [x] No console errors on load (all assets procedural/local)
- [x] Keyboard + touch controls both playable
- [x] Pause/resume, tab-switch auto-pause
- [x] Race/TimeTrial/FreeRoam all finishable
- [x] Save/load survives refresh
- [x] 60 FPS target on integrated GPUs (adaptive quality: Low/Med/High)
- [x] Works offline (double-click index.html)

## 10. Licensing note
Vehicle names are fictionalised; UI, map, signage and assets are original.
Real-world brand assets, logos and likenesses require licensing and are out of
scope. Specs shown are game-adjusted, not manufacturer data.
