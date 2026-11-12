# 🏁 MALABAR RUSH — Episode 1: Thamarassery Churam

**Created by Hadee Mohammed** · *One State. Fourteen Districts. Unlimited Speed.*

A 3D open-world arcade racing game — set on Kerala's legendary **Thamarassery Churam**
mountain pass — that runs in any browser with **zero installation and zero external files**.

## ▶ How to run

**Option 1 — just play it (offline, forever):**
Double-click **`index.html`**. That's it. Works with no internet (Three.js is bundled in `libs/`).

**Option 2 — serve it (recommended for best performance):**
```bash
cd malabar-rush
python3 -m http.server 8000
# open http://localhost:8000
```

Works in **Chrome, Edge, Firefox, Safari** — desktop and **iPhone/Android (touch controls)**.

## 🎮 Controls

| Key | Action | | Key | Action |
|---|---|---|---|---|
| W / ↑ | Accelerate | | Space | Handbrake (drift) |
| S / ↓ | Brake / Reverse | | Shift | Nitro boost |
| A D / ← → | Steer | | C | Change camera |
| Esc | Pause | | R | Reset car |

On mobile: on-screen GAS / BRAKE / steering / NITRO / HANDBRAKE buttons.

## 🚗 Features
- **3 modes:** Churam Circuit (3-lap race vs 3 AI) · Time Trial · Free Roam (living traffic)
- **3 vehicles** with full spec cards + Engine/Turbo/Tyre upgrades (₹ currency, saved progress)
- **Dynamic world:** hairpin bends, guardrails, signboards (EN + മലയാളം), village huts, palm valleys, tea gardens, misty mountains
- **Weather:** Clear / Mist / Rain · **Time:** Day / Sunset / Night (headlights)
- Procedural engine audio, nitro whoosh, collisions · mute button
- Speedometer + nitro bar + live minimap + race positions + best-lap saving
- Graphics quality: Low / Med / High (adaptive for weak GPUs)

## 🗺 Roadmap
Episodes 2–14 expand this same world into the complete connected Kerala map
(Munnar, Kochi, Kovalam, Alleppey, Athirappilly… all 14 districts, 15+ vehicles).
See `design-doc.md`.

## 📁 Files
```
malabar-rush/
├── index.html        ← open this to play
├── js/game.js        ← the full game engine
├── libs/three.min.js ← bundled 3D engine (offline)
├── design-doc.md     ← game design document
└── README.md
```

*Original UI, map and assets. Vehicle names are fictionalised (inspired-by),
performance figures are game-adjusted. Family-friendly, ages 10+.*
