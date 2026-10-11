// Accompaniment algorithm A (port of accomp.py): returns {prog, acc:[{ch,pitch,start,end,vel}], fadeEnd, skips, shift}
const ACC = (() => {
const BPM = 92, TPB = 480, TEMPO = Math.round(60e6 / BPM);
const tick = s => Math.round(s * 1e6 * TPB / TEMPO), sec = t => t * TEMPO / 1e6 / TPB;
const CH0 = { Bbm: [10, [10, 1, 5]], Gb: [6, [6, 10, 1]], Cm7b5: [0, [0, 3, 6, 10]], F7: [5, [5, 9, 0, 3]], Ebm: [3, [3, 6, 10]], Db: [1, [1, 5, 8]], Ab: [8, [8, 0, 3]], F: [5, [5, 9, 0]] };
const PREF = { Bbm: .3, F7: .2, Gb: .15, Ebm: .1, Cm7b5: .05, Db: .05, Ab: 0, F: 0 };
const NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];
function arrange(notes, autoKey = true) {
  const mel = notes.map(n => [n.pitch, tick(n.start), tick(n.end)]).sort((a, b) => a[1] - b[1]);
  let shift = 0;
  if (autoKey) { const w = new Array(12).fill(0); for (const [p, s, e] of mel) w[p % 12] += e - s;
    const sc = [10, 0, 1, 3, 5, 6, 8]; let best = -1;
    for (let k = 0; k < 12; k++) { const v = sc.reduce((a, q) => a + w[(q + k) % 12], 0) + 0.5 * w[(10 + k) % 12] + 0.3 * w[(5 + k) % 12]; if (v > best) { best = v; shift = k; } } }
  const CH = {}; for (const c in CH0) CH[c] = [(CH0[c][0] + shift) % 12, CH0[c][1].map(q => (q + shift) % 12)];
  const keys = Object.keys(CH0);
  const T0 = mel[0][1], LAST = Math.max(...mel.map(n => n[2])), SEG = 2 * TPB, nseg = Math.floor((LAST - T0) / SEG) + 1;
  const prog = []; let prev = null;
  for (let k = 0; k < nseg; k++) { const s0 = T0 + k * SEG, b = s0 + SEG, w = {};
    for (const [p, s, e] of mel) { const d = Math.min(e, b) - Math.max(s, s0); if (d > 0) w[p % 12] = (w[p % 12] || 0) + d * (s <= s0 + Math.floor(TPB / 4) ? 1.5 : 1); }
    const tot = Object.values(w).reduce((a, x) => a + x, 0) || 1;
    let best = null, bv = -Infinity;
    for (const c of keys) { let inn = 0, out = 0; for (const q in w) { if (CH[c][1].includes(+q)) inn += w[q]; else out += w[q]; }
      const v = inn / tot - 0.6 * out / tot + PREF[c] + (c === prev ? 0.15 : 0); if (v > bv) { bv = v; best = c; } }
    if (k === 0 || k === nseg - 1) best = 'Bbm';
    if (k === nseg - 2 && best !== 'F7' && best !== 'F') best = 'F7';
    prog.push([s0, best]); prev = best; }
  const sounding = (p, s, e) => mel.some(([q, ms, me]) => q === p && s < me && e > ms);
  const below = s => { const c = mel.filter(([q, ms, me]) => ms <= s + TPB && me >= s).map(n => n[0]); return c.length ? Math.min(...c) : 60; };
  let acc = [], skips = 0;
  const add = (ch, p, s, e, v) => { if (s < T0) return; if (sounding(p, s, e)) { skips++; return; } acc.push([ch, p, s, e, v]); };
  const FADE_END = tick(sec(LAST) + 3.0);
  prog.forEach(([s0, c], i) => { const [root, pcs] = CH[c], last = i === prog.length - 1;
    add(1, 29 + (((root - 5) % 12) + 12) % 12, s0, last ? FADE_END : s0 + SEG - 10, 48);
    const tones = []; for (let p = 40; p < 56; p++) if (pcs.includes(p % 12)) tones.push(p);
    const pat = tones.length > 3 ? [0, 2, 1, 3, 2, 1] : [0, 2, 1, 2];
    if (last) { tones.slice(0, 4).forEach((p, j) => add(2, p, s0 + j * 40, FADE_END, 52 - 4 * j)); return; }
    for (let k = 0; k < 4; k++) { const s = s0 + k * TPB / 2, lim = below(s); let cand = tones.filter(p => p < lim); if (!cand.length) cand = tones.slice(0, 2);
      add(2, cand[pat[k % pat.length] % cand.length], s, s0 + SEG - 10, k === 0 ? 44 : 36); } });
  acc.sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2]);
  for (let i = 0; i + 1 < acc.length; i++) { const [c, p, s, e, v] = acc[i]; if (acc[i + 1][0] === c && acc[i + 1][1] === p && acc[i + 1][2] < e + 5) acc[i] = [c, p, s, acc[i + 1][2] - 5, v]; }
  const keyName = NAMES[(10 + shift) % 12] + 'm';
  return { shift, keyName, skips, fadeStart: sec(prog[prog.length - 1][0]), fadeEnd: sec(FADE_END), lastMel: sec(LAST),
    prog: prog.map(([s, c]) => ({ time: sec(s), name: c, root: NAMES[CH[c][0]] })),
    acc: acc.map(([ch, pitch, s, e, vel]) => ({ ch, pitch, start: sec(s), end: sec(e), vel })),
    mel: mel.map(([pitch, s, e]) => ({ pitch, start: sec(s), end: sec(e) })) };
}
return { arrange, BPM };
})();
if (typeof module !== 'undefined') module.exports = ACC;
