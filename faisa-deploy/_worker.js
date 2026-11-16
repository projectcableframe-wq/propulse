/* ============================================================================
   Faisaa sync server — Cloudflare Worker
   ----------------------------------------------------------------------------
   Serves the static app AND a tiny JSON API so every device (Windows laptop,
   iPhone, iPad) shares one ledger.

   Storage: one KV namespace bound as ASSETS_KV? No — bound as FAISAA_KV.
     key "ledger"   -> { accounts:[], txns:[], recurring:[], rates:[],
                         budgets:[], settings:{}, rev:int, updatedAt:iso }

   API
     GET  /api/state            -> { ok, rev, state }
     POST /api/ops  {ops:[...]} -> applies ops, returns { ok, rev } (+ any
                                   ops other devices pushed since `since`)
     GET  /api/ping             -> { ok, rev }   used for polling fallback

   Auth: optional shared PIN. If the `FAISAA_PIN` secret is set, every /api
   request must send `x-faisaa-pin: <pin>`. The app asks for the PIN once per
   device and stores it locally. Without a PIN the ledger is open to anyone
   who knows the URL, so setting one is strongly recommended.

   WebSockets are intentionally NOT used: Workers can't keep durable in-memory
   state across requests, so a socket would need Durable Objects. Instead the
   client polls /api/ping (cheap) and pulls on change — simpler, cheaper, and
   reliable on iOS where sockets die when the app backgrounds.
   ========================================================================== */

const LEDGER_KEY = 'ledger';
const MAX_OPS_PER_PUSH = 400;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // ---- API routes ----
    if (url.pathname.startsWith('/api/')) {
      return handleApi(request, env, url);
    }

    // ---- static assets ----
    if (env.ASSETS) {
      const res = await env.ASSETS.fetch(request);
      // Never let a stale HTML shell be reused after a deploy.
      if (res.headers.get('content-type')?.includes('text/html')) {
        const h = new Headers(res.headers);
        h.set('Cache-Control', 'no-cache, must-revalidate');
        return new Response(res.body, { status: res.status, headers: h });
      }
      return res;
    }
    return new Response('Not found', { status: 404 });
  }
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'content-type,x-faisaa-pin',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
  });
}

async function handleApi(request, env, url) {
  if (request.method === 'OPTIONS') return json({ ok: true });

  // ---- auth ----
  const pin = env.FAISAA_PIN;
  if (pin) {
    const given = request.headers.get('x-faisaa-pin') || url.searchParams.get('pin') || '';
    if (given !== pin) return json({ ok: false, error: 'pin_required' }, 401);
  }

  if (!env.FAISAA_KV) {
    return json({ ok: false, error: 'no_kv', message: 'Bind a KV namespace as FAISAA_KV' }, 500);
  }

  const path = url.pathname;

  try {
    if (path === '/api/state' && request.method === 'GET') {
      const ledger = await loadLedger(env);
      return json({ ok: true, rev: ledger.rev || 0, state: ledger });
    }

    if (path === '/api/ping') {
      const ledger = await loadLedger(env);
      return json({ ok: true, rev: ledger.rev || 0 });
    }

    if (path === '/api/ops' && request.method === 'POST') {
      const body = await request.json().catch(() => null);
      if (!body || !Array.isArray(body.ops)) return json({ ok: false, error: 'bad_body' }, 400);

      const ops = body.ops.slice(0, MAX_OPS_PER_PUSH);
      const since = Number(body.since) || 0;

      const ledger = await loadLedger(env);
      const before = ledger.rev || 0;

      // Collect what this device missed FIRST — before our own ops are logged,
      // otherwise a device would receive an echo of its own change.
      const missed = (ledger.log || []).filter(o => (o._rev || 0) > since && o.dev !== body.deviceId);

      for (const op of ops) applyOp(ledger, op, before + 1);

      ledger.rev = before + 1;
      ledger.updatedAt = new Date().toISOString();
      ledger.log = (ledger.log || []).slice(-300);
      await saveLedger(env, ledger);

      return json({ ok: true, rev: ledger.rev, missed, accepted: ops.length });
    }

    return json({ ok: false, error: 'not_found' }, 404);
  } catch (e) {
    return json({ ok: false, error: 'server_error', message: String(e && e.message || e) }, 500);
  }
}

async function loadLedger(env) {
  const raw = await env.FAISAA_KV.get(LEDGER_KEY);
  if (!raw) return emptyLedger();
  try {
    const l = JSON.parse(raw);
    const base = Object.assign(emptyLedger(), l);
    // _ts is used for last-write-wins; strip it from records we hand to the app
    (['accounts','txns','recurring','rates','budgets']).forEach(k=>{
      (base[k]||[]).forEach(r=>{ if(r && typeof r==='object') delete r._ts; });
    });
    return base;
  } catch {
    return emptyLedger();
  }
}
async function saveLedger(env, ledger) {
  await env.FAISAA_KV.put(LEDGER_KEY, JSON.stringify(ledger));
}
function emptyLedger() {
  return { accounts: [], txns: [], recurring: [], rates: [], budgets: [],
           settings: {}, rev: 0, updatedAt: null, log: [] };
}

/* Apply one op from the client. Ops are last-write-wins by timestamp, which is
   right for a single user moving between their own devices. */
function applyOp(ledger, op, rev) {
  if (!op || !op.entity) return;
  const ts = Number(op.ts) || Date.now();

  if (op.entity === 'settings') {
    ledger.settings = Object.assign({}, ledger.settings, op.data || {});
    return;
  }

  const COLL = { account: 'accounts', txn: 'txns', recurring: 'recurring',
                 rate: 'rates', budget: 'budgets' };
  const key = COLL[op.entity];
  if (!key) return;
  if (!Array.isArray(ledger[key])) ledger[key] = [];

  const list = ledger[key];
  const id = op.id || (op.data && (op.data.id || (op.data.base && op.data.quote ? op.data.base + op.data.quote : null)));
  if (!id) return;

  const i = list.findIndex(r => r.id === id || (r.base && r.quote && r.base + r.quote === id));

  if (op.op === 'delete') {
    if (i >= 0) list.splice(i, 1);
  } else {
    const rec = Object.assign({}, op.data, { id });
    if (i >= 0) {
      // Last-write-wins: ignore an older edit arriving late.
      const prevTs = Number(list[i]._ts) || 0;
      if (ts >= prevTs) list[i] = Object.assign(rec, { _ts: ts });
    } else {
      list.push(Object.assign(rec, { _ts: ts }));
    }
  }
  ledger.log = (ledger.log || []);
  ledger.log.push(Object.assign({}, op, { _rev: rev || (ledger.rev || 0) + 1 }));
}
