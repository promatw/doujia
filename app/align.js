// 豆莢浪歌 alignment helpers: accompaniment ↔ melody offset, lyric line ↔ phrase mapping
const ALIGN = (() => {
const FPS = 100;
function onsetEnv(x, sr) { const h = Math.round(sr / FPS), n = Math.floor(x.length / h), e = new Float64Array(n), o = new Float64Array(n);
  for (let k = 0; k < n; k++) { let s = 0; for (let i = k * h; i < (k + 1) * h; i++) s += x[i] * x[i]; e[k] = 10 * Math.log10(s / h + 1e-10); }
  for (let k = 1; k < n; k++) o[k] = Math.max(0, e[k] - e[k - 1]); return o; }
function phrases(notes, gap = 0.45) { const P = []; notes.forEach((n, i) => { if (!i || n.start - notes[i - 1].end > gap) P.push({ start: n.start, end: n.end, first: i, last: i }); else { const p = P[P.length - 1]; p.end = n.end; p.last = i; } }); return P; }
// offset (s) = how far the vocal/melody must be delayed to sit on the accompaniment timeline
function estimateOffset(x, sr, notes, maxLag = 8) {
  const o = onsetEnv(x, sr), n = o.length, m = new Float64Array(n);
  const add = (t, w) => { const c = Math.round(t * FPS); for (let d = -3; d <= 3; d++) if (c + d >= 0 && c + d < n) m[c + d] += w * Math.exp(-d * d / 4); };
  for (const p of phrases(notes)) add(p.start, 3); for (const nt of notes) add(nt.start, 1);
  let best = 0, bv = -Infinity; const L = Math.round(maxLag * FPS);
  for (let lag = Math.round(-1 * FPS); lag <= L; lag++) { let s = 0; for (let i = 0; i < n; i++) { const j = i + lag; if (j >= 0 && j < n) s += m[i] * o[j]; } if (s > bv) { bv = s; best = lag; } }
  return best / FPS; }
// map typed lyric lines onto melody phrases (simple: merge/split phrases so counts match)
function alignLyrics(lines, notes) { let P = phrases(notes).map(p => ({ ...p }));
  if (!lines.length || !P.length) return [];
  while (P.length > lines.length) { let k = 0, g = Infinity; for (let i = 0; i + 1 < P.length; i++) { const d = P[i + 1].start - P[i].end + 0.3 * (P[i].end - P[i].start + P[i + 1].end - P[i + 1].start); if (d < g) { g = d; k = i; } }
    P.splice(k, 2, { start: P[k].start, end: P[k + 1].end, first: P[k].first, last: P[k + 1].last }); }
  while (P.length < lines.length) { let k = 0; for (let i = 1; i < P.length; i++) if (P[i].last - P[i].first > P[k].last - P[k].first) k = i;
    const p = P[k]; if (p.last === p.first) break; const mid = Math.floor((p.first + p.last + 1) / 2);
    P.splice(k, 1, { start: p.start, end: notes[mid - 1].end, first: p.first, last: mid - 1 }, { start: notes[mid].start, end: p.end, first: mid, last: p.last }); }
  return lines.map((text, i) => P[i] ? { text, start: P[i].start, end: P[i].end, notes: P[i].last - P[i].first + 1, chars: [...text.replace(/\s/g, '')].length } : { text, start: null, end: null, notes: 0, chars: text.length }); }
function toLRC(al, off = 0) { const f = t => { t += off; const m = Math.floor(t / 60), s = t - 60 * m; return `[${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}]`; };
  return al.filter(a => a.start != null).map(a => f(a.start) + a.text).join('\n') + '\n'; }
return { phrases, estimateOffset, alignLyrics, toLRC, onsetEnv };
})();
if (typeof module !== 'undefined') module.exports = ALIGN;
