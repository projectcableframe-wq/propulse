# Faisaa — enable sync across your phone, iPad and laptop

Right now the app keeps its ledger in each browser's local storage, so every
device is separate. This folder adds a small server on Cloudflare that holds
one shared ledger, so a change on any device appears on the others within a
few seconds.

You need: a Cloudflare account (you have one), Node.js on your laptop, and
about 10 minutes.

---

## What is in this folder

| File | Role |
|---|---|
| `index.html` | the app |
| `_worker.js` | the sync server (`/api/state`, `/api/ping`, `/api/ops`) |
| `wrangler.toml` | deploy config — tells Cloudflare to run the script **and** serve the files |
| `manifest.webmanifest`, `sw.js`, `icon*.png`, `favicon-32.png` | app shell, Home Screen icons |

The dashboard's "upload static files" button **cannot** deploy this — that flow
only handles static assets. A script is required for the `/api` routes, so this
one goes up with Wrangler.

---

## Step 1 — Install Wrangler and log in

```bash
npm install -g wrangler
wrangler login
```

A browser opens; approve it.

## Step 2 — Create the storage

```bash
cd faisa-deploy
wrangler kv namespace create FAISAA_KV
```

It prints something like:

```
[[kv_namespaces]]
binding = "FAISAA_KV"
id = "a1b2c3d4e5f6..."
```

Copy that `id` into `wrangler.toml`, replacing
`PASTE_YOUR_KV_NAMESPACE_ID_HERE`.

## Step 3 — Set your PIN

```bash
wrangler secret put FAISAA_PIN
```

Type a PIN (4–6 digits is fine) and press Enter. **This is what protects your
finances** — without it, anyone who finds the URL can read the ledger. Wrangler
will not echo it back.

## Step 4 — Deploy

```bash
wrangler deploy
```

You should see the Worker and its assets upload, with a URL like
`https://faisa.projectcableframe.workers.dev`.

## Step 5 — Connect each device

1. Open the URL on your laptop. The header will show **PIN needed**.
2. Go to **Settings → Sync & devices → Connect this device** and enter your PIN.
3. The **first** device you connect uploads its existing ledger — that becomes
   the shared starting point.
4. On your iPhone and iPad: open the URL, **Connect this device**, same PIN.
   They download the shared ledger.

Check it works: add an expense on the phone, wait ~12 seconds (or switch apps
and come back), and it appears on the laptop.

---

## Important: your existing data

Whichever device you connect **first** uploads what it already has. If your
laptop is the one with the real ledger, connect the laptop first. If you connect
a nearly-empty device first, that empty state becomes the server's copy and the
other devices will adopt it.

If you get this wrong, fix it on the device that has the good data:

**Settings → Sync & devices → Upload this device's data**

That overwrites the server with the local ledger. Then hit
**Connect this device** on the others.

To be extra safe, connect the device holding your real data first and check the
totals match on the second device before entering anything new.

---

## Day to day

- **Offline is fine.** Changes queue locally and send when you reconnect.
- **Status pill** tells you the truth: `Synced` (server acknowledged),
  `Syncing N` (in flight), `PIN needed`, or `On this device` (local only).
- **Polling** is every 12 seconds, plus an immediate sync whenever the app comes
  back to the foreground. WebSockets are deliberately not used: Workers have no
  durable in-memory state, and iOS drops sockets when the app backgrounds.
- **Disconnect** a device from Settings without deleting its local data.

## Costs

This stays inside Cloudflare's free tier comfortably: KV reads and writes at
your volume are a few hundred per day, and the Worker free plan allows 100,000
requests/day.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `PIN needed` never clears | Wrong PIN — re-enter it. Stored in `faisaa.pin` locally. |
| `error: no_kv` | Step 2 skipped, or the `id` wasn't pasted into `wrangler.toml`. |
| Devices show different totals | One downloaded before the other uploaded. On the correct device: **Upload this device's data**, then reconnect the other. |
| Site 404s after deploying | `wrangler.toml` must have `directory = "."` and both `index.html` + `_worker.js` at the top level. |
| Old page after deploy | The Worker now sends `Cache-Control: no-cache` for HTML. Hard-refresh once (`Ctrl/Cmd+Shift+R`). |
| Want to wipe the server | `wrangler kv key delete ledger --binding=FAISAA_KV` |

## Security notes

- The PIN travels in a header over HTTPS; it is not stored in Cloudflare logs.
- All devices share one PIN — it identifies the household, not a person.
- Everything is in a single KV key. Fine for one user; if you ever want
  per-device auth or shared multi-user ledgers, that's a bigger design.
- Your PIN is stored in each browser's local storage. Clearing site data means
  re-entering it (the ledger on the server is untouched).
