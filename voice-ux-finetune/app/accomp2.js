// 豆莢浪歌 accompaniment v2 (Bob): rule-based, melody-aware. Tempo/beat grid from note onsets, key detection,
// per-bar / half-bar chords, three distinct piano styles, optional drums. No AI, no synthesized strings, never touches the melody.
const ACC2 = (() => {
const MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88], MIN = [6.33, 2.68, 3.52, 5.38, 2.6, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17];
const NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];
const corr = (a, b) => { const ma = a.reduce((x, y) => x + y) / 12, mb = b.reduce((x, y) => x + y) / 12; let n = 0, da = 0, db = 0; for (let i = 0; i < 12; i++) { n += (a[i] - ma) * (b[i] - mb); da += (a[i] - ma) ** 2; db += (b[i] - mb) ** 2; } return n / Math.sqrt(da * db + 1e-9); };
function detectKey(notes) { const h = new Array(12).fill(0); for (const n of notes) h[n.pitch % 12] += Math.min(1.5, n.end - n.start) + .1;
  let best = { tonic: 0, minor: false, r: -2 }; for (let k = 0; k < 12; k++) for (const [minor, P] of [[false, MAJ], [true, MIN]]) { const r = corr(h, P.map((_, i) => P[(i - k + 12) % 12])); if (r > best.r) best = { tonic: k, minor, r }; }
  best.name = NAMES[best.tonic] + (best.minor ? 'm' : ''); return best; }
// onsets weighted by duration (longer = more likely on a beat)
function onsets(notes) { return notes.map(n => ({ t: n.start, w: .5 + Math.min(1, n.end - n.start) })); }
function tempo(notes) { const O = onsets(notes); let best = { bpm: 90, phase: 0, s: -1 };
  for (let bpm = 60; bpm <= 160; bpm += 1) { const T = 60 / bpm, sg = .09 * T, prior = Math.exp(-.5 * (Math.log2(bpm / 92) / .45) ** 2);
    for (let ph = 0; ph < 24; ph++) { const p = ph / 24 * T; let s = 0, W = 0;
      for (const o of O) { const x = ((o.t - p) / T % 1 + 1) % 1, d = Math.min(x, 1 - x) * T, dh = Math.abs(x - .5) * T; s += o.w * Math.max(Math.exp(-d * d / (2 * sg * sg)), .45 * Math.exp(-dh * dh / (2 * sg * sg))); W += o.w; }
      s = s / W * prior; if (s > best.s) best = { bpm, phase: p, s }; } }
  return best; }
// beat tracking: start from the fitted grid, let each beat drift gently toward nearby onsets (humming is not a metronome)
function beatGrid(notes) { const tp = tempo(notes), O = onsets(notes), first = notes[0].start, last = Math.max(...notes.map(n => n.end));
  let T = 60 / tp.bpm, b = tp.phase + Math.floor((first - tp.phase) / T) * T; if (first - b > .5 * T) b += T; // beat nearest/before the first onset
  const beats = [b]; while (beats[beats.length - 1] < last + T) { const pred = beats[beats.length - 1] + T; let best = null, bw = 0;
    for (const o of O) { const d = o.t - pred; if (Math.abs(d) < .18 * T && o.w > bw) { bw = o.w; best = d; } }
    const nb = pred + (best == null ? 0 : .35 * best); T = Math.min(60 / 58, Math.max(60 / 165, .9 * T + .1 * (nb - beats[beats.length - 1]))); beats.push(nb); }
  // downbeat: which beat mod 4 collects the strongest onsets (long notes, phrase starts after a gap)
  const strength = new Array(4).fill(0); notes.forEach((n, i) => { const gap = i ? n.start - notes[i - 1].end : 1; const w = Math.min(1, n.end - n.start) + (gap > .35 ? 1.2 : 0);
    let k = 0, bd = 1e9; beats.forEach((t, j) => { const d = Math.abs(t - n.start); if (d < bd) { bd = d; k = j; } }); if (bd < .2 * (60 / tp.bpm)) strength[k % 4] += w; });
  const db = strength.indexOf(Math.max(...strength));
  return { bpm: tp.bpm, beats, down: db }; }
function chordsFor(key) { const t = key.tonic, M = key.minor;
  const deg = M ? [[0, 'm', .12], [5, 'm', .08], [7, '', .1], [8, '', .08], [3, '', .06], [10, '', .06]] : [[0, '', .12], [5, '', .1], [7, '', .1], [9, 'm', .08], [2, 'm', .04], [4, 'm', .02]];
  return deg.map(([d, q, pr]) => { const r = (t + d) % 12; return { root: r, q, pcs: [r, (r + (q === 'm' ? 3 : 4)) % 12, (r + 7) % 12], prior: pr, name: NAMES[r] + q }; }); }
function pickChord(C, notes, s, e, prev) { const w = new Array(12).fill(0); let tot = 0;
  for (const n of notes) { const d = Math.min(n.end, e) - Math.max(n.start, s); if (d > 0) { const v = d * (Math.abs(n.start - s) < .12 ? 1.6 : 1); w[n.pitch % 12] += v; tot += v; } }
  if (!tot) return { c: prev || C[0], v: 0 }; let best = null, bv = -1e9;
  for (const c of C) { let inn = 0; c.pcs.forEach(p => inn += w[p]); const v = inn / tot - .5 * (tot - inn) / tot + c.prior + (c === prev ? .08 : 0); if (v > bv) { bv = v; best = c; } } return { c: best, v: bv }; }
// style: '抒情' | '溫暖' | '簡約鋼琴'; drums: 0..3
function arrange(notes, style = '抒情', drums = 0) { notes = [...notes].sort((a, b) => a.start - b.start);
  const key = detectKey(notes), C = chordsFor(key), G = beatGrid(notes); let beats = G.beats;
  // bars start at the first downbeat at/after the first note's beat; one intro bar before it
  let d0 = G.down; while (d0 - 4 >= 0) d0 -= 4; const T0 = beats[1] - beats[0];
  const pre = []; for (let k = 1; k <= 4 + d0; k++) pre.unshift(beats[0] - k * T0); beats = pre.concat(beats); // pad so beat 0 is the intro downbeat
  const bars = []; for (let i = 0; i + 4 <= beats.length; i += 4) bars.push({ s: beats[i], b: beats.slice(i, i + 4), e: beats[i + 4] ?? beats[i + 3] + T0 });
  const lastMel = Math.max(...notes.map(n => n.end)); while (bars.length > 2 && bars[bars.length - 1].s > lastMel + .2) bars.pop();
  const tonic = C[0]; let prev = tonic;
  bars.forEach((B, i) => { if (i === 0) { B.ch = [tonic]; return; }
    const full = pickChord(C, notes, B.s, B.e, prev).c, h1 = pickChord(C, notes, B.s, B.b[2], prev), h2 = pickChord(C, notes, B.b[2], B.e, h1.c);
    B.ch = (h1.c !== h2.c && h2.v - pickChord(C, notes, B.b[2], B.e, h1.c).v > .25) ? [h1.c, h2.c] : [full]; prev = B.ch[B.ch.length - 1]; });
  if (bars.length > 2) { const L = bars[bars.length - 1]; L.ch = [tonic]; const P = bars[bars.length - 2]; if (P.ch.length === 1 && P.ch[0] !== C[2]) P.ch = [P.ch[0], C[2]]; }
  // keep accompaniment under the melody where it is sounding
  const melLow = (s, e) => { const c = notes.filter(n => n.start < e && n.end > s).map(n => n.pitch); return c.length ? Math.min(...c) : 72; };
  const ev = [], add = (p, s, d, v) => { if (p > 20 && p < 109) ev.push({ p, s, d: Math.max(.05, d), v }); };
  const voicing = (c, lo, hi, s, e) => { const top = Math.min(hi, melLow(s, e) - 2), out = []; for (let p = lo; p <= top; p++) if (c.pcs.includes(p % 12)) out.push(p); return out.length >= 3 ? out.slice(-4) : c.pcs.map(pc => lo + ((pc - lo) % 12 + 12) % 12).sort((a, b) => a - b); };
  const bass = c => 36 + ((c.root - 0) % 12 + 12) % 12 - (c.root > 7 ? 12 : 0);
  bars.forEach((B, i) => { const last = i === bars.length - 1, segs = B.ch.length === 2 ? [[B.s, B.b[2], B.ch[0], [0, 1]], [B.b[2], B.e, B.ch[1], [2, 3]]] : [[B.s, B.e, B.ch[0], [0, 1, 2, 3]]];
    const bt = k => k < 4 ? B.b[k] : B.e, intro = i === 0;
    for (const [s, e, c, ks] of segs) { const L = e - s, V = voicing(c, 48, 67, s, e), bp = bass(c);
      if (last) { add(bp, s, 4, .45); V.forEach((p, j) => add(p, s + j * .06, 4, .32)); continue; }
      if (style === '抒情') { add(bp, s, L * .98, .5); V.forEach((p, j) => add(p, s + j * .045, L * .97, .32)); // sustained, gently rolled
        const arp = voicing(c, 55, 74, s, e); ks.slice(1).forEach((k, j) => { if (arp.length) add(arp[(j + 1) % arp.length], bt(k) + (bt(k + 1) - bt(k)) * .5, (bt(k + 1) - bt(k)) * 1.2, .22); }); }
      else if (style === '溫暖') { const A = voicing(c, 50, 69, s, e); const pat = A.length >= 3 ? [0, A.length - 1, 1, A.length - 1] : [0, 1, 0, 1];
        ks.forEach((k, j) => { add(k % 2 === 0 ? bp : bp + 7 > 52 ? bp - 5 : bp + 7, bt(k), (bt(k + 1) - bt(k)) * .9, .4);
          for (let h = 0; h < 2; h++) { const t = bt(k) + h * (bt(k + 1) - bt(k)) / 2, q = pat[(j * 2 + h) % 4]; add(A[q % A.length], t, (bt(k + 1) - bt(k)) * .55, h ? .2 : .26); } }); }
      else { add(bp - 12 >= 28 ? bp - 12 : bp, s, L * .9, .42); if (ks.length > 2) add(bp, bt(ks[2]), (e - bt(ks[2])) * .9, .3);
        ks.forEach(k => V.forEach(p => add(p, bt(k), (bt(k + 1) - bt(k)) * .45, k % 2 ? .2 : .27))); } }
    if (intro && style !== '抒情') { /* intro bar already played above with the tonic */ } });
  const hits = []; if (drums) { const g = [0, .35, .6, .9][drums];
    bars.forEach((B, i) => { const last = i === bars.length - 1, bt = k => k < 4 ? B.b[k] : B.e;
      if (last) { hits.push({ k: 'kick', s: B.s, v: g }); return; }
      for (let k = 0; k < 4; k++) { const t = bt(k), half = (bt(k + 1) - t) / 2;
        if (k === 0 || (k === 2 && drums >= 2)) hits.push({ k: 'kick', s: t, v: g * (k ? .8 : 1) });
        if (drums >= 2 && (k === 1 || k === 3)) hits.push({ k: 'snare', s: t, v: g * .75 });
        if (drums === 1 && k === 2) hits.push({ k: 'snare', s: t, v: g * .5 });
        hits.push({ k: 'hihat', s: t, v: g * .45 }); if (drums >= 2) hits.push({ k: 'hihat', s: t + half, v: g * .28 });
        if (drums === 3 && k === 2) hits.push({ k: 'kick', s: t + half, v: g * .6 }); } }); }
  const shift = Math.max(0, -bars[0].s); // seconds the vocal must be delayed so the intro bar fits
  return { key: key.name, bpm: G.bpm, style, shift, introStart: bars[0].s, bars: bars.map(B => ({ t: B.s, ch: B.ch.map(c => c.name) })), ev, hits, end: Math.max(lastMel, ...ev.map(x => x.s + x.d)) + 2.5 };
}
return { arrange, detectKey, tempo, beatGrid };
})();
if (typeof module !== 'undefined') module.exports = ACC2;
