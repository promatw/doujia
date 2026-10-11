// v60 core (algorithm A) — faithful JS port of librosa.pyin + v60 note rules
const V60 = (() => {
const SR = 22050, FL = 2048, HOP = 256;
const FMIN = 440 * Math.pow(2, (36 - 69) / 12), FMAX = 440 * Math.pow(2, (84 - 69) / 12); // C2, C6
function fft(re, im) { // in-place radix-2
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) { let b = n >> 1; for (; j & b; b >>= 1) j ^= b; j ^= b;
    if (i < j) { let t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; } }
  for (let len = 2; len <= n; len <<= 1) { const a = -2 * Math.PI / len, wr = Math.cos(a), wi = Math.sin(a);
    for (let i = 0; i < n; i += len) { let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) { const p = i + k, q = p + len / 2;
        const xr = re[q] * cr - im[q] * ci, xi = re[q] * ci + im[q] * cr;
        re[q] = re[p] - xr; im[q] = im[p] - xi; re[p] += xr; im[p] += xi;
        const t = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = t; } } }
}
function betaProbs(n) { // Beta(2,18) cdf diff on linspace(0,1,n+1)
  const cdf = x => { const m = 19; let s = 0; for (let j = 0; j < 2; j++) s += binom(m, j) * Math.pow(x, j) * Math.pow(1 - x, m - j); return 1 - s; };
  const out = []; for (let i = 0; i < n; i++) out.push(cdf((i + 1) / n) - cdf(i / n)); return out;
}
function binom(n, k) { let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }
function pyin(y, onProgress) {
  const minP = Math.floor(SR / FMAX), maxP = Math.min(Math.ceil(SR / FMIN), FL - 1);
  const pad = new Float64Array(y.length + FL); pad.set(y, FL / 2);
  const nF = 1 + Math.floor((pad.length - FL) / HOP);
  const NT = 100, BP = betaProbs(NT), thr = []; for (let i = 0; i <= NT; i++) thr.push(i / NT);
  const nbps = 10, NB = Math.floor(12 * nbps * Math.log2(FMAX / FMIN)) + 1, NS = 2 * NB;
  const lam = 2, bolt = (k, N) => (1 - Math.exp(-lam)) * Math.exp(-lam * k) / (1 - Math.exp(-lam * N));
  const obs = new Float64Array(nF * NS); // log later
  const NFFT = 4096, re = new Float64Array(NFFT), im = new Float64Array(NFFT);
  const nK = maxP - minP + 1, yin = new Float64Array(nK), shifts = new Float64Array(nK), probs = new Float64Array(nK);
  const dfun = new Float64Array(maxP + 1);
  for (let f = 0; f < nF; f++) {
    const o = f * HOP; re.fill(0); im.fill(0);
    for (let i = 0; i < FL; i++) re[i] = pad[o + i];
    // energy cumsum
    const cs = new Float64Array(maxP + 1); let acc = 0;
    for (let i = 0; i <= maxP; i++) { acc += pad[o + i] * pad[o + i]; cs[i] = acc; }
    fft(re, im); for (let i = 0; i < NFFT; i++) { re[i] = re[i] * re[i] + im[i] * im[i]; im[i] = 0; }
    fft(re, im); // real power spectrum symmetric -> forward fft == n * ifft
    const acf0 = re[0] / NFFT;
    let cm = 0; dfun[0] = 0;
    for (let k = 1; k <= maxP; k++) dfun[k] = 2 * (acf0 - re[k] / NFFT) - cs[k - 1];
    const cmean = new Float64Array(maxP + 1);
    for (let k = 1; k <= maxP; k++) { cm += dfun[k]; cmean[k] = cm / k; }
    for (let i = 0; i < nK; i++) { const k = minP + i; yin[i] = dfun[k] / (cmean[k] + 1e-300); }
    for (let i = 0; i < nK; i++) { shifts[i] = 0; if (i === 0 || i === nK - 1) continue;
      const a = yin[i + 1] + yin[i - 1] - 2 * yin[i], b = (yin[i + 1] - yin[i - 1]) / 2;
      shifts[i] = Math.abs(b) >= Math.abs(a) ? 0 : -b / a; }
    // troughs
    const tr = [];
    if (yin[0] < yin[1]) tr.push(0);
    for (let i = 1; i < nK - 1; i++) if (yin[i] < yin[i - 1] && yin[i] <= yin[i + 1]) tr.push(i);
    if (yin[nK - 1] < yin[nK - 2]) tr.push(nK - 1);
    if (!tr.length) { for (let s = NB; s < NS; s++) obs[f * NS + s] = 1 / NB; continue; }
    const pr = new Float64Array(tr.length);
    for (let t = 0; t < NT; t++) { const th = thr[t + 1]; let n = 0; for (const i of tr) if (yin[i] < th) n++;
      let pos = -1; for (let j = 0; j < tr.length; j++) if (yin[tr[j]] < th) { pos++; pr[j] += bolt(pos, n) * BP[t]; } }
    let gm = 0; for (let j = 1; j < tr.length; j++) if (yin[tr[j]] < yin[tr[gm]]) gm = j;
    let nb = 0; for (let t = 0; t < NT; t++) if (!(yin[tr[gm]] < thr[t + 1])) nb++;
    let sb = 0; for (let t = 0; t < nb; t++) sb += BP[t]; pr[gm] += 0.01 * sb;
    const row = f * NS;
    for (let j = 0; j < tr.length; j++) { if (pr[j] === 0) continue; const i = tr[j];
      const per = minP + i + shifts[i], f0 = SR / per;
      let bi = Math.round(12 * nbps * Math.log2(f0 / FMIN)); bi = Math.max(0, Math.min(NB, bi));
      obs[row + bi] = pr[j]; }
    let vp = 0; for (let s = 0; s < NB; s++) vp += obs[row + s]; vp = Math.min(1, Math.max(0, vp));
    for (let s = NB; s < NS; s++) obs[row + s] = (1 - vp) / NB;
    if (onProgress && f % 500 === 0) onProgress(f / nF * 0.6);
  }
  // transition: kron([[.99,.01],[.01,.99]], local triangle width 51), threshold 1e-4
  const W = 51, h = 25, win = []; for (let n = 0; n < W; n++) win.push(1 - Math.abs(n - h) / (h + 1));
  const loc = []; // loc[i] = {lo, vals} row-normalized
  for (let i = 0; i < NB; i++) { const lo = Math.max(0, i - h), hi = Math.min(NB - 1, i + h); const v = []; let s = 0;
    for (let j = lo; j <= hi; j++) { const w = win[j - i + h]; v.push(w); s += w; } loc.push({ lo, v: v.map(x => x / s) }); }
  const EPS = 2.2250738585072014e-308, LT = Math.log(1e-4 + EPS);
  // predecessors per target j: list of [k, logtrans]
  const preds = [];
  for (let j = 0; j < NS; j++) { const jb = j % NB, jv = j < NB; const P = [];
    for (let blk = 0; blk < 2; blk++) { const sw = (blk === 0) === jv ? 0.99 : 0.01;
      const kLo = Math.max(0, jb - h), kHi = Math.min(NB - 1, jb + h);
      for (let kb = kLo; kb <= kHi; kb++) { const L = loc[kb], idx = jb - L.lo; if (idx < 0 || idx >= L.v.length) continue;
        const lt = Math.log(sw * L.v[idx] + EPS); if (lt >= LT) P.push(blk * NB + kb, lt); } }
    preds.push(Float64Array.from(P)); }
  let prev = new Float64Array(NS), cur = new Float64Array(NS);
  const ptr = new Uint16Array(nF * NS), lpi = Math.log(1 / NS + EPS);
  for (let s = 0; s < NS; s++) prev[s] = Math.log(obs[s] + EPS) + lpi;
  for (let t = 1; t < nF; t++) {
    for (let j = 0; j < NS; j++) { const P = preds[j]; let best = -Infinity, bk = 0;
      for (let q = 0; q < P.length; q += 2) { const c = prev[P[q]] + P[q + 1]; if (c > best) { best = c; bk = P[q]; } }
      ptr[t * NS + j] = bk; cur[j] = Math.log(obs[t * NS + j] + EPS) + best; }
    const tmp = prev; prev = cur; cur = tmp;
    if (onProgress && t % 500 === 0) onProgress(0.6 + 0.4 * t / nF);
  }
  const st = new Int32Array(nF); let bs = 0; for (let s = 1; s < NS; s++) if (prev[s] > prev[bs]) bs = s; st[nF - 1] = bs;
  for (let t = nF - 2; t >= 0; t--) st[t] = ptr[(t + 1) * NS + st[t + 1]];
  const f0 = new Float64Array(nF), voiced = new Uint8Array(nF);
  for (let t = 0; t < nF; t++) { f0[t] = FMIN * Math.pow(2, (st[t] % NB) / (12 * nbps)); voiced[t] = st[t] < NB ? 1 : 0; }
  return { f0, voiced };
}
// pYIN bins are 0.1 semitone above C2. Ties (x.5) are resolved exactly as numpy/librosa does (float noise of hz_to_midi + round-half-even):
const TIE_UP = new Set([15,55,115,135,175,235,255,265,315,335,375,395,435,455]);
function binToMidi(b) { const lo = 36 + Math.floor(b / 10), r = b % 10; return r < 5 ? lo : r > 5 ? lo + 1 : lo + (TIE_UP.has(b) ? 1 : 0); }
function medfilt5(a) { const n = a.length, o = new Float64Array(n);
  for (let i = 0; i < n; i++) { const w = []; for (let k = -2; k <= 2; k++) w.push(i + k >= 0 && i + k < n ? a[i + k] : 0);
    w.sort((x, y) => x - y); o[i] = w[2]; } return o; }
function notesFromPitch(f0, voiced) {
  let idx = [], f = []; for (let i = 0; i < f0.length; i++) if (voiced[i]) { idx.push(i); f.push(f0[i]); }
  if (f.length) { const s = [...f].sort((a, b) => a - b), m = s.length;
    const med = m % 2 ? s[(m - 1) / 2] : (s[m / 2 - 1] + s[m / 2]) / 2;
    const ni = [], nf = []; for (let i = 0; i < f.length; i++) if (f[i] <= med * 1.9 && f[i] >= med / 1.9) { ni.push(idx[i]); nf.push(f[i]); }
    idx = ni; f = nf; }
  if (f.length >= 5) f = Array.from(medfilt5(f));
  const segs = [];
  for (let i = 0; i < f.length; i++) { const p = binToMidi(Math.round(120 * Math.log2(f[i] / FMIN))); const s = idx[i] * HOP / SR, e = s + HOP / SR;
    const L = segs[segs.length - 1]; if (L && L[0] === p && s - L[2] < 0.07) L[2] = e; else segs.push([p, s, e]); }
  const notes = segs.filter(n => n[2] - n[1] >= (n[0] < 50 ? 0.08 : 0.11));
  for (const n of notes) n[1] += n[0] < 50 ? 0.02 : 0.035;
  for (let i = 0; i + 1 < notes.length; i++) if (notes[i][2] > notes[i + 1][1] - 0.025) notes[i][2] = notes[i + 1][1] - 0.025;
  return notes.filter(n => n[2] > n[1]).map(([pitch, start, end]) => ({ pitch, start, end }));
}
function extract(y22050, onProgress) { const { f0, voiced } = pyin(y22050, onProgress); return notesFromPitch(f0, voiced); }
return { SR, extract, pyin, notesFromPitch };
})();
if (typeof module !== 'undefined') module.exports = V60;
