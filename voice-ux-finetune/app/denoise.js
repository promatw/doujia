// 豆莢浪歌 denoise — JS port of v60/v2/denoise.py (see v60/v3/DENOISE_ALGORITHM.md)
// 80 Hz 4th-order Butterworth HP (zero-phase) -> stationary spectral gate (noisereduce, prop 0.5) -> downward expander (floor+8 dB, 1:4, range -35 dB, 5/80 ms)
const DENOISE = (() => {
function floorDb(x, sr) { const n = Math.floor(sr * 0.05), m = Math.floor(x.length / n), r = [];
  for (let k = 0; k < m; k++) { let s = 0; for (let i = k * n; i < (k + 1) * n; i++) s += x[i] * x[i]; r.push(20 * Math.log10(Math.sqrt(s / n) + 1e-10)); }
  if (!r.length) return -100; r.sort((a, b) => a - b); const p = 0.1 * (r.length - 1), lo = Math.floor(p); return r[lo] + (r[Math.min(lo + 1, r.length - 1)] - r[lo]) * (p - lo); }
function biquadHP(fc, sr, Q) { const w = 2 * Math.PI * fc / sr, al = Math.sin(w) / (2 * Q), c = Math.cos(w), a0 = 1 + al;
  return [(1 + c) / 2 / a0, -(1 + c) / a0, (1 + c) / 2 / a0, -2 * c / a0, (1 - al) / a0]; }
function runSos(x, sos) { for (const [b0, b1, b2, a1, a2] of sos) { let z1 = 0, z2 = 0;
  // steady-state init from first sample (like sosfilt_zi * x0): HP -> output 0 for DC
  for (let i = 0; i < x.length; i++) { const v = x[i], y = b0 * v + z1; z1 = b1 * v - a1 * y + z2; z2 = b2 * v - a2 * y; x[i] = y; } } }
function highpassFiltFilt(x, sr, fc) {
  const sos = [biquadHP(fc, sr, 0.5411961), biquadHP(fc, sr, 1.3065630)], pl = Math.min(15, x.length - 1), n = x.length;
  const e = new Float64Array(n + 2 * pl);
  for (let i = 0; i < pl; i++) { e[i] = 2 * x[0] - x[pl - i]; e[n + pl + i] = 2 * x[n - 1] - x[n - 2 - i]; }
  e.set(x, pl); runSos(e, sos); e.reverse(); runSos(e, sos); e.reverse(); return e.slice(pl, pl + n); }
function fft(re, im) { const n = re.length;
  for (let i = 1, j = 0; i < n; i++) { let b = n >> 1; for (; j & b; b >>= 1) j ^= b; j ^= b; if (i < j) { let t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; } }
  for (let len = 2; len <= n; len <<= 1) { const a = -2 * Math.PI / len, wr = Math.cos(a), wi = Math.sin(a);
    for (let i = 0; i < n; i += len) { let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) { const p = i + k, q = p + len / 2, xr = re[q] * cr - im[q] * ci, xi = re[q] * ci + im[q] * cr;
        re[q] = re[p] - xr; im[q] = im[p] - xi; re[p] += xr; im[p] += xi; const t = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = t; } } } }
function tri(n) { const a = []; for (let i = 0; i < n + 1; i++) a.push(i / (n + 1)); for (let i = 0; i < n + 2; i++) a.push(1 - i / (n + 1)); return a.slice(1, -1); }
function spectralGate(x, sr, prop) {
  const N = 1024, H = 256, B = N / 2 + 1, win = new Float64Array(N); for (let i = 0; i < N; i++) win[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / N);
  const pad = new Float64Array(x.length + N); pad.set(x, N / 2);
  const T = 1 + Math.floor((pad.length - N) / H), RE = new Float64Array(T * B), IM = new Float64Array(T * B), DB = new Float32Array(T * B);
  const re = new Float64Array(N), im = new Float64Array(N);
  for (let t = 0; t < T; t++) { for (let i = 0; i < N; i++) { re[i] = pad[t * H + i] * win[i]; im[i] = 0; } fft(re, im);
    for (let f = 0; f < B; f++) { RE[t * B + f] = re[f]; IM[t * B + f] = im[f]; DB[t * B + f] = 20 * Math.log10(Math.max(1e-12, Math.hypot(re[f], im[f]))); } }
  const Tn = Math.min(T, 1 + Math.floor((Math.min(pad.length, 600000 + N) - N) / H)), thr = new Float64Array(B);
  for (let f = 0; f < B; f++) { let mx = -1e9; for (let t = 0; t < Tn; t++) mx = Math.max(mx, DB[t * B + f]); const fl = mx - 80; let s = 0, s2 = 0;
    for (let t = 0; t < Tn; t++) { const v = Math.max(DB[t * B + f], fl); s += v; s2 += v * v; } const m = s / Tn; thr[f] = m + 1.5 * Math.sqrt(Math.max(0, s2 / Tn - m * m)); }
  const M = new Float32Array(T * B); for (let t = 0; t < T; t++) for (let f = 0; f < B; f++) M[t * B + f] = (DB[t * B + f] > thr[f] ? 1 : 0) * prop + (1 - prop);
  const kf = tri(5), kt = tri(8); let ks = 0; for (const a of kf) for (const b of kt) ks += a * b;
  const tmp = new Float32Array(T * B), SM = new Float32Array(T * B); // separable 2D convolution, zero padding ('same')
  for (let t = 0; t < T; t++) for (let f = 0; f < B; f++) { let s = 0; for (let k = 0; k < 11; k++) { const ff = f + k - 5; if (ff >= 0 && ff < B) s += kf[k] * M[t * B + ff]; } tmp[t * B + f] = s; }
  for (let t = 0; t < T; t++) for (let f = 0; f < B; f++) { let s = 0; for (let k = 0; k < 17; k++) { const tt = t + k - 8; if (tt >= 0 && tt < T) s += kt[k] * tmp[tt * B + f]; } SM[t * B + f] = s / ks; }
  const out = new Float64Array(pad.length), wsum = new Float64Array(pad.length);
  for (let t = 0; t < T; t++) { for (let f = 0; f < B; f++) { const g = SM[t * B + f]; re[f] = RE[t * B + f] * g; im[f] = IM[t * B + f] * g; if (f > 0 && f < N / 2) { re[N - f] = re[f]; im[N - f] = -im[f]; } }
    for (let i = 0; i < N; i++) im[i] = -im[i]; fft(re, im); // inverse via conj
    for (let i = 0; i < N; i++) { out[t * H + i] += re[i] / N * win[i]; wsum[t * H + i] += win[i] * win[i]; } }
  const y = new Float64Array(x.length); for (let i = 0; i < x.length; i++) { const w = wsum[i + N / 2]; y[i] = w > 1e-10 ? out[i + N / 2] / w : 0; } return y; }
function expander(x, sr, o) { const f1 = floorDb(x, sr), thrDb = f1 + o.offset, w = Math.floor(sr * 0.01), n = x.length, cs = new Float64Array(n + 1);
  for (let i = 0; i < n; i++) cs[i + 1] = cs[i] + x[i] * x[i];
  const aA = Math.exp(-1 / (sr * o.att / 1000)), aR = Math.exp(-1 / (sr * o.rel / 1000)), y = new Float64Array(n); let s = null;
  const h = Math.floor(w / 2);
  for (let i = 0; i < n; i++) { const a = Math.max(0, i - h), b = Math.min(n, i - h + w); const env = Math.sqrt(Math.max(0, cs[b] - cs[a]) / w) + 1e-10;
    const g = Math.max(o.range, Math.min(0, (20 * Math.log10(env) - thrDb) * (o.ratio - 1))); if (s === null) s = g; const c = g > s ? aA : aR; s = c * s + (1 - c) * g; y[i] = x[i] * Math.pow(10, s / 20); }
  return { y, f1, thr: thrDb }; }
function process(x, sr) { const f0 = floorDb(x, sr); let y = highpassFiltFilt(x, sr, 80); y = spectralGate(y, sr, 0.5);
  const r = expander(y, sr, { offset: 8, ratio: 4, range: -35, att: 5, rel: 80 }); y = r.y; let pk = 0; for (const v of y) pk = Math.max(pk, Math.abs(v));
  if (pk > 0.98) for (let i = 0; i < y.length; i++) y[i] *= 0.98 / pk; return { y, f0, f1: r.f1, thr: r.thr, f2: floorDb(y, sr) }; }
function encodeWav(x, sr) { const n = x.length, b = new ArrayBuffer(44 + 2 * n), v = new DataView(b), w = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, 'RIFF'); v.setUint32(4, 36 + 2 * n, true); w(8, 'WAVEfmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true); v.setUint32(24, sr, true); v.setUint32(28, sr * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, 2 * n, true);
  for (let i = 0; i < n; i++) v.setInt16(44 + 2 * i, Math.max(-32768, Math.min(32767, Math.round(x[i] * 32767))), true); return b; }
return { process, highpassFiltFilt, spectralGate, expander, floorDb, encodeWav };
})();
if (typeof module !== 'undefined') module.exports = DENOISE;
