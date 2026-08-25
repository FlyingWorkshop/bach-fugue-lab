/* Fugue Lab — score + piano roll + structural map, in sync, with audio. */
(() => {
'use strict';

const $ = s => document.querySelector(s);
const el = (t, a, ...kids) => {
  const n = document.createElement(t);
  for (const k in (a || {})) {
    if (k === 'class') n.className = a[k];
    else if (k === 'html') n.innerHTML = a[k];
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), a[k]);
    else n.setAttribute(k, a[k]);
  }
  for (const c of kids) {
    if (c == null) continue;
    if (typeof c === 'string' && /<\/?[a-z][a-z0-9]*\b[^>]*>/i.test(c))
      console.warn('Fugue Lab: markup passed as text — use { html: … }:', c.slice(0, 70));
    n.append(c);
  }
  return n;
};
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
/* *asterisks* mark italics in the editorial text; that is the whole of the markup */
const esc = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const md = t => esc(t).replace(/\*([^*]+)\*/g, '<em>$1</em>');
const PCS = ['C','C♯','D','E♭','E','F','F♯','G','A♭','A','B♭','B'];
const pname = p => PCS[((p % 12) + 12) % 12] + (Math.floor(p / 12) - 1);
const VCOL = {
  2: ['#5cc8ff', '#52d6a4'],
  3: ['#5cc8ff', '#ffc247', '#52d6a4'],
  4: ['#5cc8ff', '#ffc247', '#ff7eb6', '#52d6a4'],
  5: ['#5cc8ff', '#ffc247', '#ff7eb6', '#c58bff', '#52d6a4'],
};
const vcol = (nv, i) => (VCOL[nv] || VCOL[4])[i] || '#8e9aac';

/* ============================================================ data loading */
async function loadIndex() {
  if (window.__BUNDLE__) return window.__BUNDLE__.index;
  return (await fetch('data/index.json')).json();
}
async function loadPiece(id) {
  if (window.__BUNDLE__) {
    const b = window.__BUNDLE__.pieces[id];
    return { doc: typeof b.json === 'string' ? JSON.parse(b.json) : b.json, svg: b.svg, svgP: b.svgP };
  }
  const [doc, svg, svgP] = await Promise.all([
    fetch(`data/${id}.json`).then(r => r.json()),
    fetch(`data/${id}.svg`).then(r => r.text()),
    fetch(`data/${id}.p.svg`).then(r => r.text()),
  ]);
  return { doc, svg, svgP };
}

/* ================================================================== state */
const S = {
  doc: null, svg: null, svgP: null, id: null, spacing: 'p',
  q: 0, playing: false, bpm: 76, zoom: 1.1,
  follow: true, loopOn: false, loop: null, spotlight: false, accents: false,
  mute: [], solo: -1, master: 0.8, levels: [],
  show: { entries: true, cs: true, threads: true, dim: true, grid: true,
          diss: false, cross: false, score: true, keys: true },
  PXU: 1.45, scoreW: 0, scoreH: 0, rollH: 190,
};
const G = {};   // derived per-piece geometry / indexes

/* ================================================================== audio */
const A = {
  ctx: null, master: null, wet: null, voices: [], waves: [],
  t0: 0, q0: 0, nextIdx: 0, timer: null, live: [],
};

function harmonics(profile) {
  const n = 20, re = new Float32Array(n), im = new Float32Array(n);
  for (let k = 1; k < n; k++) im[k] = profile(k);
  return { re, im };
}
function makeIR(ctx, secs, decay) {
  const len = Math.floor(ctx.sampleRate * secs);
  const buf = ctx.createBuffer(2, len, ctx.sampleRate);
  for (let ch = 0; ch < 2; ch++) {
    const d = buf.getChannelData(ch);
    for (let i = 0; i < len; i++) {
      const t = i / len;
      d[i] = (Math.random() * 2 - 1) * Math.pow(1 - t, decay) * (i < 60 ? i / 60 : 1);
    }
  }
  return buf;
}
function initAudio() {
  if (A.ctx) return;
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  A.ctx = ctx;
  A.master = ctx.createGain(); A.master.gain.value = S.master;
  const comp = ctx.createDynamicsCompressor();
  comp.threshold.value = -14; comp.ratio.value = 3; comp.attack.value = 0.004; comp.release.value = 0.25;
  A.master.connect(comp); comp.connect(ctx.destination);
  const conv = ctx.createConvolver(); conv.buffer = makeIR(ctx, 1.9, 2.6);
  A.wet = ctx.createGain(); A.wet.gain.value = 0.20;
  A.master.connect(conv); conv.connect(A.wet); A.wet.connect(ctx.destination);
  // one timbre per voice: brighter on top, rounder at the bottom
  A.waves = [0, 1, 2, 3].map(i => {
    const bright = 1.55 - i * 0.16;
    const h = harmonics(k => Math.pow(k, -bright) * (k % 2 === 0 ? 0.72 : 1));
    return ctx.createPeriodicWave(h.re, h.im, { disableNormalization: false });
  });
}
function buildVoiceChain(nv) {
  if (!A.ctx) return;
  A.voices.forEach(v => { try { v.gain.disconnect(); } catch (e) {} });
  A.voices = [];
  for (let i = 0; i < nv; i++) {
    const g = A.ctx.createGain();
    g.gain.value = S.levels[i] == null ? 0.9 : S.levels[i];
    const p = A.ctx.createStereoPanner();
    p.pan.value = nv === 1 ? 0 : (-0.42 + (i / (nv - 1)) * 0.84) * 0.75;
    g.connect(p); p.connect(A.master);
    A.voices.push({ gain: g, pan: p });
  }
  applyVoiceGains();
}
/* One place decides how loud each voice is: the slider, and whether it is muted
   or soloed. Applied to the live gain node so it takes effect mid-note. */
function applyVoiceGains() {
  if (!A.ctx) return;
  A.voices.forEach((vo, i) => {
    const lvl = S.levels[i] == null ? 0.9 : S.levels[i];
    vo.gain.gain.setTargetAtTime(voiceAudible(i) ? lvl : 0, A.ctx.currentTime, 0.015);
  });
}
function voiceAudible(v) {
  if (S.solo >= 0) return S.solo === v;
  return !S.mute[v];
}
function playNote(v, midi, when, durSec, amp) {
  const ctx = A.ctx; if (!ctx) return;
  const f = 440 * Math.pow(2, (midi - 69) / 12);
  const osc = ctx.createOscillator();
  osc.setPeriodicWave(A.waves[Math.min(v, 3)]);
  osc.frequency.value = f;
  const lp = ctx.createBiquadFilter();
  lp.type = 'lowpass'; lp.Q.value = 0.4;
  lp.frequency.setValueAtTime(Math.min(11000, f * 9), when);
  lp.frequency.exponentialRampToValueAtTime(Math.max(500, f * 2.6), when + Math.min(0.7, durSec));
  const g = ctx.createGain();
  const peak = amp * clamp(1.25 - (midi - 48) / 130, 0.55, 1.15);
  const end = when + durSec;
  g.gain.setValueAtTime(0.0001, when);
  g.gain.exponentialRampToValueAtTime(peak, when + 0.007);
  g.gain.exponentialRampToValueAtTime(peak * 0.55, when + Math.min(0.16, durSec * 0.5));
  g.gain.setTargetAtTime(peak * 0.30, when + Math.min(0.16, durSec * 0.5), 0.9);
  g.gain.setTargetAtTime(0.0001, end, 0.035);
  osc.connect(lp); lp.connect(g); g.connect(A.voices[v].gain);
  osc.start(when); osc.stop(end + 0.28);
  A.live.push(osc);
  if (A.live.length > 220) A.live = A.live.slice(-160);
}

/* ============================================================== transport */
const qps = () => S.bpm / 60;
function currentQ() {
  if (!S.playing || !A.ctx) return S.q;
  return A.q0 + (A.ctx.currentTime - A.t0) * qps();
}
function firstIdxAtOrAfter(q) {
  const N = S.doc.notes; let lo = 0, hi = N.length;
  while (lo < hi) { const m = (lo + hi) >> 1; if (N[m].q < q - 1e-9) lo = m + 1; else hi = m; }
  return lo;
}
function play() {
  initAudio();
  if (A.ctx.state === 'suspended') A.ctx.resume();
  if (!A.voices.length) buildVoiceChain(S.doc.nv);
  if (S.q >= S.doc.total - 1e-6) S.q = 0;
  A.q0 = S.q; A.t0 = A.ctx.currentTime + 0.06;
  A.nextIdx = firstIdxAtOrAfter(S.q);
  S.playing = true;
  $('#playBtn').classList.add('playing');
  A.timer = setInterval(schedule, 25);
  schedule();
}
function pause() {
  if (!S.playing) return;
  S.q = clamp(currentQ(), 0, S.doc.total);
  S.playing = false;
  clearInterval(A.timer); A.timer = null;
  $('#playBtn').classList.remove('playing');
  A.live.forEach(o => { try { o.stop(); } catch (e) {} });
  A.live = [];
}
let lastSetScroll = -1;
function setScroll(sc, x) { sc.scrollLeft = x; lastSetScroll = sc.scrollLeft; }
function scrollToQ(q, always) {
  const sc = $('#scroller');
  if (!G.xu) return;
  const x = G.xu(q) * S.PXU;
  if (always || x < sc.scrollLeft + 40 || x > sc.scrollLeft + sc.clientWidth - 60)
    setScroll(sc, x - sc.clientWidth * 0.33);
}
function seek(q, keepPlaying, noScroll) {
  q = clamp(q, 0, S.doc.total);
  const was = S.playing;
  if (was) pause();
  S.q = q;
  if (was && keepPlaying !== false) play();
  if (!noScroll) scrollToQ(q, false);
  paint(true);
}
function schedule() {
  if (!S.playing) return;
  const doc = S.doc, N = doc.notes;
  const nowQ = currentQ();
  const endQ = (S.loopOn && S.loop) ? S.loop[1] : doc.total;
  const aheadQ = nowQ + 0.25 * qps() + 0.12 * qps();
  while (A.nextIdx < N.length) {
    const n = N[A.nextIdx];
    if (n.q >= endQ - 1e-9) break;
    if (n.q > aheadQ) break;
    if (voiceAudible(n.v)) {
      const when = A.t0 + (n.q - A.q0) / qps();
      const dur = Math.max(0.06, (n.d / qps()) * 0.96);
      let amp = 0.19;
      if (S.spotlight) amp *= (n.e >= 0 ? 1.45 : (n.cs >= 0 ? 1.0 : 0.52));
      if (S.accents) {
        const inBar = (((n.q - doc.pickup) % doc.qbar) + doc.qbar) % doc.qbar;
        if (inBar < 1e-6) amp *= 1.13;
        else if (Math.abs(inBar % doc.qpb) < 1e-6) amp *= 1.05;
      }
      if (when > A.ctx.currentTime - 0.02) playNote(n.v, n.p, Math.max(when, A.ctx.currentTime), dur, amp);
    }
    A.nextIdx++;
  }
  if (nowQ >= endQ - 1e-6) {
    if (S.loopOn && S.loop) {
      S.q = S.loop[0]; pause(); play();
    } else if (endQ >= doc.total - 1e-6) {
      pause(); S.q = doc.total; paint(true);
    }
  }
}

/* =============================================================== geometry */
function curSvg()     { return S.spacing === 'p' ? S.svgP : S.svg; }
function curViewBox() { return S.spacing === 'p' ? S.doc.viewBoxP : S.doc.viewBox; }
function noteX(n)     { return S.spacing === 'p' ? n.xp : n.x; }
function buildGeometry() {
  const doc = S.doc;
  const P = S.spacing === 'p';
  const anchors = (P ? doc.anchorsP : doc.anchors).slice();
  const lastBar = doc.bars[doc.bars.length - 1];
  const endX = (P ? lastBar.px1 : lastBar.x1) || curViewBox()[2];
  if (anchors[anchors.length - 1][0] < doc.total) anchors.push([doc.total, endX]);
  for (let i = 1; i < anchors.length; i++)          // never let x(q) run backwards
    if (anchors[i][1] < anchors[i - 1][1]) anchors[i][1] = anchors[i - 1][1];
  const AQ = anchors.map(a => a[0]), AX = anchors.map(a => a[1]);
  G.anchors = anchors; G.AQ = AQ; G.AX = AX;
  G.xu = q => {
    if (q <= AQ[0]) return AX[0];
    if (q >= AQ[AQ.length - 1]) return AX[AX.length - 1];
    let lo = 0, hi = AQ.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (AQ[m] <= q) lo = m; else hi = m; }
    const t = (q - AQ[lo]) / (AQ[hi] - AQ[lo] || 1);
    return AX[lo] + t * (AX[hi] - AX[lo]);
  };
  G.qOfXu = x => {
    if (x <= AX[0]) return AQ[0];
    if (x >= AX[AX.length - 1]) return AQ[AQ.length - 1];
    let lo = 0, hi = AX.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (AX[m] <= x) lo = m; else hi = m; }
    const t = (x - AX[lo]) / (AX[hi] - AX[lo] || 1);
    return AQ[lo] + t * (AQ[hi] - AQ[lo]);
  };
  G.lo = Math.min(...doc.notes.map(n => n.p)) - 2;
  G.hi = Math.max(...doc.notes.map(n => n.p)) + 2;
  G.byId = new Map(); doc.notes.forEach(n => n.ids.forEach(i => G.byId.set(i, n)));
  G.entryNotes = doc.entries.map(e =>
    doc.notes.filter(n => n.v === e.v && n.q >= e.q0 - 1e-6 && n.q < e.q1 - 1e-6));
  G.counterNotes = doc.counters.map(e =>
    doc.notes.filter(n => n.v === e.v && n.q >= e.q0 - 1e-6 && n.q < e.q1 - 1e-6));
  G.barOfQ = q => {
    const B = doc.bars;
    for (let i = B.length - 1; i >= 0; i--) if (q >= B[i].q0 - 1e-9) return B[i];
    return { n: 0, q0: 0, q1: B.length ? B[0].q0 : doc.qbar };
  };
  // dissonance + crossing analysis
  G.diss = analyseDissonance(doc);
  G.cross = analyseCrossings(doc);
}
function analyseDissonance(doc) {
  const onsets = [...new Set(doc.notes.map(n => n.q))].sort((a, b) => a - b);
  const out = [];
  let start = 0;
  for (const q of onsets) {
    while (start < doc.notes.length && doc.notes[start].q + doc.notes[start].d <= q + 1e-9) start++;
    const sounding = [];
    for (let i = start; i < doc.notes.length; i++) {
      const n = doc.notes[i];
      if (n.q > q + 1e-9) break;
      if (n.q <= q + 1e-9 && n.q + n.d > q + 1e-9) sounding.push(n);
    }
    if (sounding.length < 2) continue;
    const bass = Math.min(...sounding.map(n => n.p));
    for (const n of sounding) {
      if (n.q < q - 1e-9) continue;           // only flag at its own onset
      const iv = ((n.p - bass) % 12 + 12) % 12;
      if (n.p === bass) continue;
      if ([1, 2, 5, 6, 10, 11].includes(iv)) out.push({ i: doc.notes.indexOf(n), iv });
    }
  }
  return out;
}
function analyseCrossings(doc) {
  const onsets = [...new Set(doc.notes.map(n => n.q))].sort((a, b) => a - b);
  const spans = [];
  for (let k = 0; k < onsets.length; k++) {
    const q = onsets[k], q2 = onsets[k + 1] != null ? onsets[k + 1] : doc.total;
    const cur = new Map();
    for (const n of doc.notes) {
      if (n.q <= q + 1e-9 && n.q + n.d > q + 1e-9) {
        if (!cur.has(n.v) || n.p > cur.get(n.v)) cur.set(n.v, n.p);
      }
    }
    let bad = false;
    const vs = [...cur.keys()].sort((a, b) => a - b);
    for (let i = 0; i + 1 < vs.length; i++) if (cur.get(vs[i]) < cur.get(vs[i + 1])) bad = true;
    if (bad) {
      if (spans.length && Math.abs(spans[spans.length - 1][1] - q) < 1e-6) spans[spans.length - 1][1] = q2;
      else spans.push([q, q2]);
    }
  }
  return spans;
}

/* ================================================================== score */
function mountScore() {
  const host = $('#score');
  host.innerHTML = curSvg();
  const svg = host.querySelector('svg');
  svg.removeAttribute('height'); svg.removeAttribute('width');
  svg.style.width = S.scoreW + 'px';
  svg.style.height = S.scoreH + 'px';
  // tag each staff with its voice (document order inside a measure = top→bottom)
  host.querySelectorAll('g.measure').forEach(m => {
    let i = 0;
    for (const c of m.children) if (c.classList && c.classList.contains('staff')) c.dataset.v = i++;
  });
  const nv = S.doc.nv;
  let css = '';
  for (let v = 0; v < nv; v++) {
    css += `#score [data-v="${v}"]{--vc:${vcol(nv, v)};color:var(--vc)}\n`;
  }
  let st = host.querySelector('style#vcss');
  if (!st) { st = document.createElement('style'); st.id = 'vcss'; host.append(st); }
  st.textContent = css;
  G.scoreNotes = new Map();
  host.querySelectorAll('g.note').forEach(g => G.scoreNotes.set(g.id, g));
  tagControlElements(host, svg);
  buildScoreOverlay();
  applyScoreClasses();
}

/* Ties, slurs and ornaments are emitted at measure level, outside any staff, so
   they inherit no voice colour and would otherwise render bright white. Assign
   each to the nearest staff and note roughly where in the piece it sits, so it
   can be coloured and dimmed exactly like the notes it belongs to. */
const CTRL_SEL = 'g.tie,g.slur,g.phrase,g.mordent,g.trill,g.turn,g.fermata,' +
                 'g.dir,g.dynam,g.hairpin,g.arpeg,g.octave,g.ornam,g.breath';
function tagControlElements(host, svg) {
  const left = svg.getBoundingClientRect().left;
  G.ctrlEls = [];
  host.querySelectorAll('g.measure').forEach(m => {
    const staves = [...m.children].filter(c => c.classList && c.classList.contains('staff'));
    if (!staves.length) return;
    const mids = staves.map(st => { const r = st.getBoundingClientRect(); return r.top + r.height / 2; });
    m.querySelectorAll(CTRL_SEL).forEach(g => {
      if (g.closest('g.staff')) return;
      const r = g.getBoundingClientRect();
      if (!r.width && !r.height) return;
      const cy = r.top + r.height / 2;
      let bi = 0, bd = Infinity;
      mids.forEach((y, i) => { const d = Math.abs(cy - y); if (d < bd) { bd = d; bi = i; } });
      g.dataset.v = staves[bi].dataset.v;
      g.dataset.q = G.qOfXu((r.left + r.width / 2 - left) / S.PXU).toFixed(3);
      G.ctrlEls.push(g);
    });
  });
}

/* brackets drawn over the engraving showing where each statement runs */
function buildScoreOverlay() {
  const doc = S.doc, host = $('#score');
  host.querySelector('#scoreOverlay')?.remove();
  const W = S.scoreW, H = S.scoreH;
  const svgEl = host.querySelector('svg');
  const svgTop = svgEl ? svgEl.getBoundingClientRect().top : 0;
  const ov = sel('svg', { id: 'scoreOverlay', width: W, height: H, viewBox: `0 0 ${W} ${H}` });
  ov.style.cssText = `position:absolute;left:0;top:6px;width:${W}px;height:${H}px;pointer-events:none;overflow:visible`;
  const X = q => G.xu(q) * S.PXU;
  const staffTop = v => (doc.staffBox[v] ? doc.staffBox[v][0] : 0) * S.PXU;
  const staffBot = v => (doc.staffBox[v] ? doc.staffBox[v][1] : 0) * S.PXU;

  /* Put the bracket just clear of the tallest thing the statement actually
     draws — stems and beams included — instead of a fixed offset that would
     cut through high notes. */
  const spanTop = (v, notes) => {
    let top = Infinity;
    for (const n of notes) {
      const g = G.scoreNotes.get(n.ids[0]); if (!g) continue;
      let t = g.getBoundingClientRect().top;
      const b = g.parentElement;
      if (b && b.classList && b.classList.contains('beam')) t = Math.min(t, b.getBoundingClientRect().top);
      if (t < top) top = t;
    }
    if (top === Infinity) return staffTop(v) - 12;
    const y = top - svgTop - 8;
    const ceiling = v > 0 ? staffBot(v - 1) + 11 : 11;
    return Math.max(y, ceiling);
  };

  G.entryBrackets = []; G.entryLabels = [];
  const draw = (e, i, isCS, notes) => {
    if (!notes.length) return;
    const y = spanTop(e.v, notes) - (isCS ? -6 : 0);
    const x0 = X(e.q0) - 5, x1 = X(e.q1) - 2;
    const col = isCS ? '#98a3b3' : vcol(doc.nv, e.v);
    const g = sel('g', { class: isCS ? 'ovcs' : 'oventry', 'data-entry': i,
                         style: 'pointer-events:auto;cursor:pointer' });
    g.append(sel('path', {
      d: `M${x0} ${y + 5} L${x0} ${y} L${x1} ${y} L${x1} ${y + 5}`,
      fill: 'none', stroke: col, 'stroke-width': 1.2,
      'stroke-opacity': isCS ? .5 : .8, 'stroke-dasharray': isCS ? '3 3' : 'none',
    }));
    if (!isCS) {
      const t = sel('text', { class: 'ovlabel', x: x0 + 5, y: y - 3.5, fill: col,
                              'font-size': 10.5, 'font-weight': 600,
                              'font-family': 'ui-sans-serif,system-ui', style: 'paint-order:stroke',
                              stroke: '#0d1014', 'stroke-width': 3.5, 'stroke-linejoin': 'round' });
      t.textContent = `${e.role} · ${e.on}${e.kind === 'partial' ? ' (partial)' : ''}`;
      g.append(t);
      G.entryLabels.push({ el: t, x0: x0 + 5, x1, w: 0 });
    }
    ov.append(g);
    if (!isCS) G.entryBrackets[i] = g;
  };
  if (S.show.entries) doc.entries.forEach((e, i) => draw(e, i, false, G.entryNotes[i] || []));
  if (S.show.cs) doc.counters.forEach((e, i) => draw(e, i, true, G.counterNotes[i] || []));
  host.append(ov);
  G.entryLabels.forEach(L => { try { L.w = L.el.getComputedTextLength(); } catch (err) { L.w = 60; } });
  stickyLabels();
}

/* Keep a statement's label in view for as long as any part of that statement is:
   it slides along the bracket rather than scrolling off with it. */
function stickyLabels() {
  const sc = $('#scroller');
  if (!sc) return;
  const left = sc.scrollLeft + 10;
  for (const L of (G.entryLabels || [])) {
    const lo = L.x0, hi = Math.max(lo, L.x1 - L.w - 3);
    L.el.setAttribute('x', Math.min(Math.max(lo, left), hi));
  }
  for (const L of (G.rollLabels || [])) {
    const lo = L.x0, hi = Math.max(lo, L.x1 - L.w - 3);
    L.el.setAttribute('x', Math.min(Math.max(lo, left), hi));
  }
}

function applyScoreClasses() {
  const host = $('#score'), doc = S.doc;
  host.classList.toggle('dimmed', S.show.dim);
  host.style.display = S.show.score ? '' : 'none';
  const beams = new Set();
  G.scoreNotes.forEach((g, id) => {
    const n = G.byId.get(id);
    const on = !!n && (n.e >= 0 || (S.show.cs && n.cs >= 0));
    g.classList.toggle('inSubj', on);
    const b = g.parentElement;
    if (on && b && b.classList && b.classList.contains('beam')) beams.add(b);
  });
  host.querySelectorAll('g.beam').forEach(b => b.classList.toggle('inSubj', beams.has(b)));
  const inMotif = (v, q) =>
    doc.entries.some(e => e.v === v && q >= e.q0 - 1e-6 && q < e.q1) ||
    (S.show.cs && doc.counters.some(e => e.v === v && q >= e.q0 - 1e-6 && q < e.q1));
  (G.ctrlEls || []).forEach(g => {
    const v = +g.dataset.v;
    g.classList.toggle('inSubj', inMotif(v, +g.dataset.q));
    g.classList.toggle('muted', !voiceAudible(v));
  });
  host.querySelectorAll('g.staff').forEach(g => {
    g.classList.toggle('muted', !voiceAudible(+g.dataset.v));
  });
}

/* =================================================================== roll */
const SVGNS = 'http://www.w3.org/2000/svg';
function sel(t, a) { const n = document.createElementNS(SVGNS, t); for (const k in a) n.setAttribute(k, a[k]); return n; }

function buildRoll() {
  const doc = S.doc, W = S.scoreW, H = S.rollH, nv = doc.nv;
  const host = $('#rollHost'); host.innerHTML = '';
  const svg = sel('svg', { class: 'roll', width: W, height: H, viewBox: `0 0 ${W} ${H}` });
  svg.style.width = W + 'px'; svg.style.height = H + 'px';
  const X = q => G.xu(q) * S.PXU;
  const PAD = 8;
  const Y = p => PAD + (H - 2 * PAD) * (1 - (p - G.lo) / (G.hi - G.lo));
  const nh = Math.max(3.4, (H - 2 * PAD) / (G.hi - G.lo) * 0.94);
  G.X = X; G.Y = Y;

  const gGrid = sel('g', { class: 'g-grid' });
  const gBands = sel('g', {});
  const gThread = sel('g', { class: 'g-thread' });
  const gNotes = sel('g', { class: 'g-notes' });
  const gMarks = sel('g', { class: 'g-marks' });
  const gBox = sel('g', { class: 'g-box' });
  svg.append(gBands, gGrid, gThread, gNotes, gMarks, gBox);

  // octave guide lines
  for (let p = Math.ceil(G.lo / 12) * 12; p <= G.hi; p += 12) {
    gGrid.append(sel('line', { class: 'octline', x1: 0, x2: W, y1: Y(p), y2: Y(p) }));
    const ol = sel('text', { class: 'octlabel', x: 3, y: Y(p) - 2 });
    ol.textContent = pname(p); gGrid.append(ol);
  }
  // bar / beat grid
  for (const b of doc.bars) {
    if (S.show.grid) {
      gGrid.append(sel('line', { class: 'grid-bar', x1: X(b.q0), x2: X(b.q0), y1: 0, y2: H }));
      for (let k = 1; k < doc.beats; k++) {
        const q = b.q0 + k * doc.qpb;
        if (q >= b.q1) break;
        gGrid.append(sel('line', { class: 'grid-beat', x1: X(q), x2: X(q), y1: 0, y2: H }));
      }
    }
    const bn = sel('text', { class: 'barnum', x: X(b.q0) + 3, y: 10 });
    bn.textContent = b.n; gGrid.append(bn);
  }
  // episode + stretto + pedal bands
  for (const [a, b] of doc.episodes)
    gBands.append(sel('rect', { x: X(a), y: 0, width: Math.max(1, X(b) - X(a)), height: H, fill: 'rgba(255,255,255,.028)' }));
  for (const [i, j] of doc.stretto) {
    const a = Math.max(doc.entries[i].q0, doc.entries[j].q0), b = Math.min(doc.entries[i].q1, doc.entries[j].q1);
    gBands.append(sel('rect', { x: X(a), y: 0, width: Math.max(1, X(b) - X(a)), height: H, fill: 'rgba(255,107,107,.07)' }));
  }
  if (S.show.cross) for (const [a, b] of G.cross)
    gBands.append(sel('rect', { class: 'crossband', x: X(a), y: 0, width: Math.max(1, X(b) - X(a)), height: H }));

  // voice threads
  if (S.show.threads) {
    for (let v = 0; v < nv; v++) {
      const pts = doc.notes.filter(n => n.v === v).map(n => `${X(n.q)},${Y(n.p)} ${X(n.q + n.d)},${Y(n.p)}`).join(' ');
      gThread.append(sel('polyline', { class: 'thread', points: pts, stroke: vcol(nv, v), 'data-v': v }));
    }
  }
  // notes
  G.rollRects = [];
  doc.notes.forEach((n, i) => {
    const x = X(n.q), w = Math.max(2.2, X(n.q + n.d) - x - 0.8);
    const r = sel('rect', {
      class: 'nb' + (n.e >= 0 ? ' thematic' : '') + (n.cs >= 0 ? ' cs' : ''),
      x, y: Y(n.p) - nh / 2, width: w, height: nh,
      fill: vcol(nv, n.v), 'data-i': i, 'data-v': n.v, rx: 2.2,
    });
    gNotes.append(r); G.rollRects[i] = r;
  });
  // dissonance dots
  if (S.show.diss) for (const d of G.diss) {
    const n = doc.notes[d.i]; if (!n) continue;
    gMarks.append(sel('circle', { class: 'diss', cx: X(n.q) + 1.5, cy: Y(n.p) - nh / 2 - 2.6, r: 1.7 }));
  }
  // entry boxes
  G.entryBoxes = []; G.rollLabels = [];
  if (S.show.entries) doc.entries.forEach((e, i) => {
    const ns = doc.notes.filter(n => n.v === e.v && n.q >= e.q0 - 1e-6 && n.q < e.q1 - 1e-6);
    if (!ns.length) return;
    const lo = Math.min(...ns.map(n => n.p)), hi = Math.max(...ns.map(n => n.p));
    const x0 = X(e.q0) - 3, x1 = X(e.q1) + 1;
    const y0 = Y(hi) - nh / 2 - 7, y1 = Y(lo) + nh / 2 + 3;
    const box = sel('rect', {
      class: 'ebox', x: x0, y: y0, width: x1 - x0, height: y1 - y0,
      stroke: vcol(nv, e.v), 'stroke-opacity': .75, 'data-entry': i,
    });
    gBox.append(box); G.entryBoxes[i] = box;
    const t = sel('text', { class: 'elabel', x: x0 + 4, y: y0 - 2.5, fill: vcol(nv, e.v) });
    t.textContent = `${e.role === 'Answer' ? 'A' : 'S'}${e.on ? ' · ' + e.on : ''}${e.kind === 'partial' ? ' (part)' : ''}`;
    gBox.append(t);
    G.rollLabels.push({ el: t, x0: x0 + 4, x1, w: 0 });
  });
  if (S.show.cs) doc.counters.forEach((e, i) => {
    const ns = doc.notes.filter(n => n.v === e.v && n.q >= e.q0 - 1e-6 && n.q < e.q1 - 1e-6);
    if (!ns.length) return;
    const lo = Math.min(...ns.map(n => n.p)), hi = Math.max(...ns.map(n => n.p));
    gBox.append(sel('rect', {
      class: 'csbox', x: X(e.q0) - 2, y: Y(hi) - nh / 2 - 4,
      width: X(e.q1) - X(e.q0) + 3, height: Y(lo) - Y(hi) + nh + 8,
    }));
  });
  host.append(svg);
  G.rollLabels.forEach(L => { try { L.w = L.el.getComputedTextLength(); } catch (err) { L.w = 40; } });
  svg.classList.toggle('dim', S.show.dim);
  updateVoiceVisibility();
}
/* A keyboard down the left edge, sharing the roll's vertical axis exactly, so a
   lit key sits on the same row as the note that lit it. */
function buildKeyboard() {
  const host = $('#keys');
  host.innerHTML = '';
  host.hidden = !S.show.keys;
  if (!S.show.keys) return;
  const H = S.rollH, W = 56, PAD = 8;
  const span = (H - 2 * PAD) / Math.max(1, G.hi - G.lo);
  const Y = p => PAD + (H - 2 * PAD) * (1 - (p - G.lo) / (G.hi - G.lo));
  const svg = sel('svg', { class: 'kbd', width: W, height: H, viewBox: `0 0 ${W} ${H}` });
  svg.style.width = W + 'px'; svg.style.height = H + 'px';
  svg.style.marginTop = ((S.show.score ? S.scoreH + 6 : 0) + 1) + 'px';  // +1 for the scroller border
  const black = p => [1, 3, 6, 8, 10].includes(((p % 12) + 12) % 12);
  G.keyEls = {};
  for (let p = Math.ceil(G.lo); p <= Math.floor(G.hi); p++) {
    const h = Math.max(1.6, span - 0.7), y = Y(p) - h / 2;
    const isB = black(p);
    const r = sel('rect', {
      class: 'key ' + (isB ? 'blk' : 'wht'),
      x: isB ? 0 : 0, y, width: isB ? (W - 8) * 0.6 : W - 8, height: h, rx: 1.4,
      'data-p': p,
    });
    svg.append(r); G.keyEls[p] = r;
  }
  for (let p = Math.ceil(G.lo / 12) * 12; p <= G.hi; p += 12) {
    if (p < G.lo) continue;
    const t = sel('text', { class: 'klab', x: W - 9, y: Y(p) + 3, 'text-anchor': 'end' });
    t.textContent = 'C' + (Math.floor(p / 12) - 1);
    svg.append(t);
  }
  svg.append(sel('rect', { class: 'kframe', x: 0, y: PAD - span / 2, width: W - 8,
                           height: H - 2 * PAD + span, rx: 3 }));
  host.append(svg);
  G.keysLit = new Map();
}
function litKeys(map) {
  if (!G.keyEls) return;
  const prev = G.keysLit || new Map();
  prev.forEach((v, p) => {
    if (map.has(p)) return;
    const el = G.keyEls[p]; if (!el) return;
    el.style.fill = ''; el.style.color = ''; el.classList.remove('on');
  });
  map.forEach((v, p) => {
    if (prev.get(p) === v) return;
    const el = G.keyEls[p]; if (!el) return;
    const c = vcol(S.doc.nv, v);
    el.style.fill = c; el.style.color = c; el.classList.add('on');
  });
  G.keysLit = map;
}
function updateVoiceVisibility() {
  const svg = $('#rollHost svg'); if (!svg) return;
  svg.querySelectorAll('[data-v]').forEach(n => {
    n.classList.toggle('voicemuted', !voiceAudible(+n.dataset.v));
  });
  $('#score') && applyScoreClasses();
}

/* ==================================================================== map */
function buildMap() {
  const doc = S.doc, host = $('#map');
  const W = host.clientWidth || 900;
  const nv = doc.nv;
  const laneH = 15, top = 16, keyH = 17;
  const H = top + nv * laneH + 10 + keyH;
  host.innerHTML = '';
  const svg = sel('svg', { viewBox: `0 0 ${W} ${H}`, height: H, preserveAspectRatio: 'none' });
  svg.style.height = H + 'px';
  const X = q => 4 + (W - 8) * (q / doc.total);
  G.mapX = X; G.mapW = W;

  for (const [a, b] of doc.episodes)
    svg.append(sel('rect', { x: X(a), y: top - 4, width: Math.max(1, X(b) - X(a)), height: nv * laneH + 8, fill: 'rgba(255,255,255,.035)' }));
  for (const [i, j] of doc.stretto) {
    const a = Math.max(doc.entries[i].q0, doc.entries[j].q0), b = Math.min(doc.entries[i].q1, doc.entries[j].q1);
    svg.append(sel('rect', { x: X(a), y: top - 4, width: Math.max(1.5, X(b) - X(a)), height: nv * laneH + 8, fill: 'rgba(255,107,107,.14)' }));
  }
  // bar ticks
  const every = doc.bars.length > 60 ? 10 : 5;
  for (const b of doc.bars) {
    if (b.n % every) continue;
    svg.append(sel('line', { x1: X(b.q0), x2: X(b.q0), y1: 9, y2: H - keyH - 4, stroke: '#1e2530' }));
    const t = sel('text', { x: X(b.q0) + 2, y: 9, fill: '#4a5666', 'font-size': 8.5, 'font-family': 'ui-monospace,monospace' });
    t.textContent = b.n; svg.append(t);
  }
  // voice activity + entries
  for (let v = 0; v < nv; v++) {
    const y = top + v * laneH;
    svg.append(sel('line', { x1: X(0), x2: X(doc.total), y1: y + laneH / 2, y2: y + laneH / 2, stroke: '#1b222c' }));
    // thin activity strokes
    const gAct = sel('g', { 'data-v': v, opacity: .5 });
    for (const n of doc.notes) if (n.v === v)
      gAct.append(sel('rect', { x: X(n.q), y: y + laneH / 2 - 1, width: Math.max(0.6, X(n.q + n.d) - X(n.q)), height: 2, fill: vcol(nv, v) }));
    svg.append(gAct);
  }
  doc.counters.forEach(e => {
    const y = top + e.v * laneH;
    svg.append(sel('rect', {
      x: X(e.q0), y: y + 2, width: Math.max(2, X(e.q1) - X(e.q0)), height: laneH - 4,
      fill: 'none', stroke: '#7d8797', 'stroke-dasharray': '2 2', rx: 3, class: 'map-cs',
    }));
  });
  doc.entries.forEach((e, i) => {
    const y = top + e.v * laneH;
    const g = sel('g', { class: 'map-entry', 'data-entry': i, style: 'cursor:pointer' });
    g.append(sel('rect', {
      x: X(e.q0), y: y + 1, width: Math.max(3, X(e.q1) - X(e.q0)), height: laneH - 2,
      fill: vcol(nv, e.v), 'fill-opacity': e.kind === 'partial' ? .34 : .82, rx: 3,
      stroke: e.kind === 'partial' ? vcol(nv, e.v) : 'none', 'stroke-dasharray': '2 2',
    }));
    const w = X(e.q1) - X(e.q0);
    if (w > 22) {
      const t = sel('text', { x: X(e.q0) + 3.5, y: y + laneH - 4.5, fill: '#0d1014', 'font-size': 9, 'font-weight': 700 });
      t.textContent = (e.role === 'Answer' ? 'A' : 'S') + (e.on ? ' ' + e.on : '');
      g.append(t);
    }
    const ttl = sel('title'); ttl.textContent =
      `${e.role} in ${doc.voiceNames[e.v]} · bar ${G.barOfQ(e.q0).n} · on ${e.on} · ${e.kind}`;
    g.append(ttl);
    svg.append(g);
  });
  // key ribbon
  const ky = H - keyH;
  doc.keys.forEach((k, i) => {
    const w = X(k.q1) - X(k.q0);
    svg.append(sel('rect', { x: X(k.q0), y: ky, width: Math.max(1, w), height: keyH - 3, fill: i % 2 ? '#1a212b' : '#1f2733', rx: 2 }));
    if (w > 30) {
      const t = sel('text', { x: X(k.q0) + w / 2, y: ky + 11.5, fill: '#93a0b1', 'font-size': 9.5, 'text-anchor': 'middle' });
      t.textContent = k.k; svg.append(t);
    }
  });
  G.mapView = sel('rect', { x: 0, y: 5, width: 10, height: H - keyH - 8, fill: 'rgba(255,255,255,.055)', stroke: 'rgba(255,255,255,.22)', rx: 3, 'pointer-events': 'none' });
  G.mapHead = sel('line', { x1: 0, x2: 0, y1: 4, y2: H - 3, stroke: '#fff', 'stroke-width': 1.4, 'pointer-events': 'none' });
  svg.append(G.mapView, G.mapHead);
  host.append(svg);

  let dragging = false;
  const toQ = ev => {
    const r = host.getBoundingClientRect();
    return clamp(((ev.clientX - r.left - 4) / (r.width - 8)) * doc.total, 0, doc.total);
  };
  host.onpointerdown = ev => {
    const g = ev.target.closest('.map-entry');
    if (g) { const e = doc.entries[+g.dataset.entry]; setLoop([e.q0, e.q1], true); seek(e.q0); scrollToQ(e.q0, true); return; }
    dragging = true; host.setPointerCapture(ev.pointerId); seek(toQ(ev), true, true); scrollToQ(toQ(ev), true);
  };
  host.onpointermove = ev => { if (dragging) { seek(toQ(ev), true, true); scrollToQ(toQ(ev), true); } };
  host.onpointerup = ev => { dragging = false; try { host.releasePointerCapture(ev.pointerId); } catch (e) {} };
}

/* ==================================================================== lab */
function buildLab() {
  const doc = S.doc, host = $('#lab');
  host.innerHTML = '';
  $('#labCount').textContent = `— ${doc.entries.length} statements of the subject`;
  const align = $('#labAlign').checked;
  const tplLo = Math.min(...doc.subject.tpl.map(t => t.p)), tplHi = Math.max(...doc.subject.tpl.map(t => t.p));
  const span = doc.subject.q1 - doc.subject.q0;
  doc.entries.forEach((e, i) => {
    const ns = doc.notes.filter(n => n.v === e.v && n.q >= e.q0 - 1e-6 && n.q < e.q1 - 1e-6);
    if (!ns.length) return;
    const W = 210, H = 54, P = 5;
    const dur = Math.max(span, e.q1 - e.q0);
    const shift = align ? -e.C : 0;
    const lo = Math.min(tplLo, ...ns.map(n => n.p + shift)) - 1;
    const hi = Math.max(tplHi, ...ns.map(n => n.p + shift)) + 1;
    const X = q => P + (W - 2 * P) * ((q - e.q0) / dur);
    const Y = p => P + (H - 2 * P) * (1 - (p - lo) / (hi - lo));
    const svg = sel('svg', { viewBox: `0 0 ${W} ${H}` });
    // ghost of the original subject
    for (const t of doc.subject.tpl) {
      const x = X(e.q0 + t.dq), w = Math.max(2, (W - 2 * P) * (t.d / dur));
      svg.append(sel('rect', { x: x - 1, y: Y(t.p) - 4.6, width: w + 2, height: 9.2, fill: '#3d4756', rx: 2 }));
    }
    for (const n of ns) {
      const x = X(n.q), w = Math.max(2, X(n.q + n.d) - x - 0.5);
      svg.append(sel('rect', { x, y: Y(n.p + shift) - 2.4, width: w, height: 4.8, fill: vcol(doc.nv, e.v), rx: 1.6 }));
    }
    const bar = G.barOfQ(e.q0);
    const beat = ((e.q0 - bar.q0) / doc.qpb + 1);
    const card = el('div', { class: 'labcard', 'data-entry': i },
      el('div', { class: 'labhead' },
        el('span', { class: 'role', style: `color:${vcol(doc.nv, e.v)}` }, `${e.role} · ${doc.voiceNames[e.v]}`),
        el('span', { class: `labtag tag-${e.kind}` }, e.kind === 'exact' ? 'exact' : e.kind === 'tonal' ? 'tonal' : e.kind === 'altered' ? 'adjusted' : 'partial')),
      el('div', { class: 'labfoot' },
        el('span', {}, `bar ${bar.n}${beat > 1.001 ? ', beat ' + (Math.round(beat * 100) / 100) : ''}`),
        el('span', {}, `on ${e.on} · ${e.C >= 0 ? '+' : ''}${e.C} st`)));
    card.append(svg);
    card.append(el('div', { class: 'labfoot' },
      el('span', {}, `${e.dhit}/${e.N} notes in shape`),
      el('span', {}, e.chit === e.N ? 'exact transposition' : `${e.N - e.chit} note${e.N - e.chit === 1 ? '' : 's'} adjusted`)));
    card.onclick = () => {
      setLoop([e.q0, e.q1], true); seek(e.q0); scrollToQ(e.q0, true);
      document.querySelectorAll('.labcard').forEach(c => c.classList.toggle('cur', c === card));
      if (!S.playing) play();
    };
    host.append(card);
  });
}

/* ================================================================ painting */
let lastActive = new Set();
function paint(force) {
  const doc = S.doc; if (!doc) return;
  const q = clamp(currentQ(), 0, doc.total);
  const xpx = G.xu(q) * S.PXU;
  $('#playhead').style.transform = `translateX(${xpx}px)`;
  const bar = G.barOfQ(q);
  const beat = Math.floor((q - bar.q0) / doc.qpb) + 1;
  $('#posBar').textContent = bar.n;
  $('#posBeat').textContent = clamp(beat, 1, doc.beats);
  // map cursor + viewport
  if (G.mapHead) {
    const mx = G.mapX(q);
    G.mapHead.setAttribute('x1', mx); G.mapHead.setAttribute('x2', mx);
    const sc = $('#scroller');
    const q0 = G.qOfXu(sc.scrollLeft / S.PXU), q1 = G.qOfXu((sc.scrollLeft + sc.clientWidth) / S.PXU);
    G.mapView.setAttribute('x', G.mapX(q0));
    G.mapView.setAttribute('width', Math.max(4, G.mapX(q1) - G.mapX(q0)));
  }
  // active notes
  const act = new Set();
  let i = firstIdxAtOrAfter(q - 8);
  for (; i < doc.notes.length; i++) {
    const n = doc.notes[i];
    if (n.q > q + 1e-9) break;
    if (n.q + n.d > q + 1e-9) act.add(i);
  }
  if (force || act.size !== lastActive.size || [...act].some(x => !lastActive.has(x))) {
    lastActive.forEach(k => {
      if (act.has(k)) return;
      G.rollRects[k] && G.rollRects[k].classList.remove('playing');
      const n = doc.notes[k];
      n.ids.forEach(id => { const g = G.scoreNotes.get(id); g && g.classList.remove('playing'); });
    });
    act.forEach(k => {
      if (lastActive.has(k)) return;
      G.rollRects[k] && G.rollRects[k].classList.add('playing');
      const n = doc.notes[k];
      n.ids.forEach(id => { const g = G.scoreNotes.get(id); g && g.classList.add('playing'); });
    });
    lastActive = act;
    paintNow(q, act);
    const lit = new Map();
    act.forEach(k => { const n = doc.notes[k]; if (!lit.has(n.p) && voiceAudible(n.v)) lit.set(n.p, n.v); });
    litKeys(lit);
  }
  // spotlight whichever statements are sounding right now
  const liveSet = new Set();
  doc.entries.forEach((e, i) => { if (q >= e.q0 - 1e-6 && q < e.q1) liveSet.add(i); });
  if (force || !G.liveEntries || liveSet.size !== G.liveEntries.size ||
      [...liveSet].some(x => !G.liveEntries.has(x))) {
    doc.entries.forEach((e, i) => {
      const on = liveSet.has(i);
      G.entryBrackets && G.entryBrackets[i] && G.entryBrackets[i].classList.toggle('live', on);
      G.entryBoxes && G.entryBoxes[i] && G.entryBoxes[i].classList.toggle('live', on);
    });
    G.liveEntries = liveSet;
  }
  // follow
  if (S.follow && S.playing) {
    const sc = $('#scroller');
    const target = xpx - sc.clientWidth * 0.33;
    const cur = sc.scrollLeft;
    if (Math.abs(target - cur) > 1)
      setScroll(sc, cur + (target - cur) * (Math.abs(target - cur) > 400 ? 1 : 0.18));
    stickyLabels();
  }
}
function paintNow(q, act) {
  const doc = S.doc, host = $('#now');
  const ent = doc.entries.filter(e => q >= e.q0 - 1e-6 && q < e.q1);
  const cs = doc.counters.filter(e => q >= e.q0 - 1e-6 && q < e.q1);
  const epi = doc.episodes.find(([a, b]) => q >= a && q < b);
  const key = doc.keys.find(k => q >= k.q0 && q < k.q1);
  const inStretto = doc.stretto.some(([i, j]) => {
    const a = Math.max(doc.entries[i].q0, doc.entries[j].q0), b = Math.min(doc.entries[i].q1, doc.entries[j].q1);
    return q >= a && q < b;
  });
  const sounding = [...act].map(i => doc.notes[i]).sort((a, b) => b.p - a.p);
  let ivs = '';
  if (sounding.length > 1) {
    const parts = [];
    for (let i = 0; i + 1 < sounding.length; i++) {
      const d = sounding[i].p - sounding[i + 1].p;
      parts.push(intervalName(d));
    }
    ivs = parts.join(' / ');
  }
  const rows = [];
  const section = ent.length ? (inStretto ? 'Stretto' : (q < doc.expoEnd ? 'Exposition' : 'Subject entry'))
    : epi ? 'Episode' : 'Free counterpoint';
  const one = (txt, on) => el('div', { class: 'val one' + (on ? '' : ' muted') }, on ? txt : '—');
  rows.push(row('Section', one(section, true)));

  const lines = ent.slice(0, 2).map(e => `${e.role} · ${doc.voiceNames[e.v]} · ${e.on}`);
  if (ent.length > 2) lines[1] += `  +${ent.length - 2}`;
  const subj = el('div', { class: 'val stack2' + (lines.length ? '' : ' muted') });
  (lines.length ? lines : ['—']).forEach(t => subj.append(el('div', {}, t)));
  rows.push(row('Subject', subj));

  rows.push(row('Counter', one((cs.length && S.show.cs) ? cs.map(e => doc.voiceNames[e.v]).join(', ') : '', cs.length && S.show.cs)));
  rows.push(row('Key', one(key ? key.k.replace('maj', 'major').replace('min', 'minor') : '', !!key)));
  rows.push(row('Intervals', one(ivs, !!ivs)));

  const snd = el('div', { class: 'sounding', style: `height:${doc.nv * 17}px` });
  for (const n of sounding.slice(0, doc.nv)) snd.append(el('div', {},
    el('i', { style: `background:${vcol(doc.nv, n.v)}` }),
    el('span', { class: 'pn' }, pname(n.p)),
    el('span', { class: 'k' }, doc.voiceNames[n.v])));
  if (!sounding.length) snd.append(el('div', { class: 'muted' }, el('span', { class: 'pn' }, '—')));
  rows.push(row('Sounding', snd));
  host.replaceChildren(...rows);
}
function row(lbl, val) { return el('div', { class: 'row' }, el('span', { class: 'lbl' }, lbl), val); }
function intervalName(semi) {
  const qual = ['P', 'm', 'M', 'm', 'M', 'P', 'A', 'P', 'm', 'M', 'm', 'M'];
  const num  = [1, 2, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7];
  const oct = Math.floor(semi / 12), r = ((semi % 12) + 12) % 12;
  if (r === 6) return oct ? `TT+${oct}8ve` : 'tritone';
  return qual[r] + (num[r] + oct * 7);
}

/* ================================================================ controls */
function setLoop(range, on) {
  S.loop = range; S.loopOn = on !== undefined ? on : S.loopOn;
  $('#loopChk').checked = S.loopOn;
  const band = $('#loopBand');
  if (S.loop && S.loopOn) {
    band.style.display = 'block';
    band.style.left = (G.xu(S.loop[0]) * S.PXU) + 'px';
    band.style.width = ((G.xu(S.loop[1]) - G.xu(S.loop[0])) * S.PXU) + 'px';
    const b0 = G.barOfQ(S.loop[0]).n, b1 = G.barOfQ(S.loop[1] - 1e-6).n;
    $('#loopLabel').textContent = `bars ${b0}–${b1}`;
  } else { band.style.display = 'none'; $('#loopLabel').textContent = ''; }
}
function currentSection() {
  const doc = S.doc, q = currentQ();
  const e = doc.entries.find(e => q >= e.q0 && q < e.q1);
  if (e) return [e.q0, e.q1];
  const ep = doc.episodes.find(([a, b]) => q >= a && q < b);
  if (ep) return ep.slice();
  const b = G.barOfQ(q); return [b.q0, b.q1];
}
function relayout() {
  const vb = curViewBox();
  S.PXU = (S.spacing === 'p' ? 1.35 : 1.55) * S.zoom;
  const doc = S.doc;
  S.scoreW = vb[2] * S.PXU;
  S.scoreH = vb[3] * S.PXU;
  S.rollH = Math.round(clamp(160 + doc.nv * 26, 200, 300) * clamp(S.zoom, .85, 1.4));
  $('#canvasStack').style.width = S.scoreW + 'px';
  mountScore();
  buildRoll();
  buildKeyboard();
  setLoop(S.loop, S.loopOn);
  paint(true);
}

function buildVoicePanel() {
  const doc = S.doc, host = $('#voiceList');
  host.innerHTML = '';
  S.mute = new Array(doc.nv).fill(false); S.solo = -1;
  S.levels = new Array(doc.nv).fill(0.9);
  doc.voiceNames.forEach((nm, v) => {
    const wrap = el('div', { class: 'voice', 'data-v': v });
    const mBtn = el('button', {}, 'M'), sBtn = el('button', {}, 'S');
    mBtn.onclick = () => { S.mute[v] = !S.mute[v]; refreshVoices(); };
    sBtn.onclick = () => { S.solo = S.solo === v ? -1 : v; refreshVoices(); };
    if (S.levels[v] == null) S.levels[v] = 0.9;
    const vol = el('input', { type: 'range', min: 0, max: 1.4, step: 0.01, value: S.levels[v],
                              title: 'Volume of this voice' });
    vol.oninput = () => { S.levels[v] = +vol.value; applyVoiceGains(); };
    const nameEl = el('span', { class: 'nm' }, nm);
    nameEl.onclick = () => { S.solo = S.solo === v ? -1 : v; refreshVoices(); };
    wrap.append(el('span', { class: 'swatch', style: `background:${vcol(doc.nv, v)}` }), nameEl,
      el('span', { class: 'btns' }, mBtn, sBtn), vol);
    host.append(wrap);
  });
  refreshVoices();
}
function refreshVoices() {
  const doc = S.doc;
  document.querySelectorAll('#voiceList .voice').forEach(w => {
    const v = +w.dataset.v;
    w.classList.toggle('off', !voiceAudible(v));
    const [m, s] = w.querySelectorAll('.btns button');
    m.classList.toggle('on', S.mute[v]); s.classList.toggle('on', S.solo === v);
  });
  applyVoiceGains();
  updateVoiceVisibility();
}

function buildLegend() {
  const doc = S.doc, host = $('#mapLegend');
  const items = [];
  doc.voiceNames.forEach((nm, v) => items.push([vcol(doc.nv, v), nm]));
  items.push(['rgba(255,255,255,.10)', 'episode']);
  if (doc.stretto.length) items.push(['rgba(255,107,107,.35)', 'stretto']);
  if (doc.counters.length) items.push(['transparent', 'countersubject (dashed)']);
  host.replaceChildren(...items.map(([c, t]) =>
    el('span', {}, el('i', { style: `background:${c};${c === 'transparent' ? 'border:1px dashed #7d8797' : ''}` }), t)));
}

/* ================================================================ tooltips */
function wireTips() {
  const tip = $('#tip'), viewer = $('.viewer');
  const show = (ev, n) => {
    const doc = S.doc, bar = G.barOfQ(n.q);
    const beat = (n.q - bar.q0) / doc.qpb + 1;
    const e = n.e >= 0 ? doc.entries[n.e] : null;
    tip.innerHTML =
      `<b>${n.n.replace('b', '♭').replace('#', '♯')}</b> <span class="k">${doc.voiceNames[n.v]}</span><br>` +
      `<span class="k">bar ${bar.n}, beat ${Math.round(beat * 100) / 100} · ${durName(n.d, doc)}</span>` +
      (e ? `<br><b style="color:${vcol(doc.nv, n.v)}">${e.role} on ${e.on}</b> <span class="k">(${e.kind})</span>` : '') +
      (n.cs >= 0 ? `<br><span class="k">countersubject</span>` : '');
    const r = viewer.getBoundingClientRect();
    tip.style.left = clamp(ev.clientX - r.left + 12, 4, r.width - 190) + 'px';
    tip.style.top = (ev.clientY - r.top + 14) + 'px';
    tip.style.opacity = 1;
  };
  const hide = () => tip.style.opacity = 0;
  $('#rollHost').addEventListener('mousemove', ev => {
    const t = ev.target.closest('rect.nb');
    if (!t) return hide();
    show(ev, S.doc.notes[+t.dataset.i]);
  });
  $('#rollHost').addEventListener('mouseleave', hide);
  $('#score').addEventListener('mousemove', ev => {
    const g = ev.target.closest('g.note');
    if (!g) return hide();
    const n = G.byId.get(g.id); if (!n) return hide();
    show(ev, n);
  });
  $('#score').addEventListener('mouseleave', hide);
}
function durName(d, doc) {
  const names = { 4: 'whole', 3: 'dotted half', 2: 'half', 1.5: 'dotted quarter', 1: 'quarter',
    0.75: 'dotted 8th', 0.5: '8th', 0.375: 'dotted 16th', 0.25: '16th', 0.125: '32nd', 0.0625: '64th' };
  return names[d] || (d + '♩');
}

/* ============================================================ interactions */
function wireStage() {
  const stack = $('#canvasStack');
  let down = false;
  stack.addEventListener('pointerdown', ev => {
    if (ev.target.closest('.ebox') || ev.target.closest('.elabel')) {
      const g = ev.target.closest('[data-entry]');
      if (g) { const e = S.doc.entries[+g.dataset.entry]; setLoop([e.q0, e.q1], true); seek(e.q0); scrollToQ(e.q0, true); return; }
    }
    const r = stack.getBoundingClientRect();
    seek(G.qOfXu((ev.clientX - r.left) / S.PXU), true, true);
    down = true; stack.setPointerCapture(ev.pointerId);
  });
  stack.addEventListener('pointermove', ev => {
    if (!down) return;
    const r = stack.getBoundingClientRect();
    seek(G.qOfXu((ev.clientX - r.left) / S.PXU), true, true);
  });
  stack.addEventListener('pointerup', ev => { down = false; try { stack.releasePointerCapture(ev.pointerId); } catch (e) {} });
  $('#scroller').addEventListener('scroll', () => {
    const sc = $('#scroller');
    // a hand-scroll during playback releases the auto-follow rather than fighting it
    if (S.playing && S.follow && Math.abs(sc.scrollLeft - lastSetScroll) > 3) {
      S.follow = false; $('#follow').checked = false;
    }
    stickyLabels();
    if (!S.playing) paint(false);
  }, { passive: true });
  $('#scroller').addEventListener('wheel', ev => {
    if (Math.abs(ev.deltaX) < Math.abs(ev.deltaY) && !ev.shiftKey) {
      $('#scroller').scrollLeft += ev.deltaY; ev.preventDefault();
      lastSetScroll = -1;
    }
  }, { passive: false });
}
function wireControls() {
  $('#playBtn').onclick = () => S.playing ? pause() : play();
  $('#stopBtn').onclick = () => { seek(0, false); };
  $('#tempo').oninput = e => {
    const was = S.playing; if (was) pause();
    S.bpm = +e.target.value; $('#tempoOut').textContent = S.bpm;
    if (was) play();
  };
  $('#zoom').oninput = e => {
    const q = currentQ();
    S.zoom = +e.target.value; relayout();
    const sc = $('#scroller'); setScroll(sc, G.xu(q) * S.PXU - sc.clientWidth * 0.33);
  };
  $('#follow').onchange = e => {
    S.follow = e.target.checked;
    if (S.follow) scrollToQ(currentQ(), true);
  };
  $('#loopChk').onchange = e => {
    S.loopOn = e.target.checked;
    if (S.loopOn && !S.loop) S.loop = currentSection();
    setLoop(S.loop, S.loopOn);
  };
  $('#spotlight').onchange = e => S.spotlight = e.target.checked;
  $('#accents').onchange = e => S.accents = e.target.checked;
  $('#soundWhy').onclick = e => {
    e.preventDefault();
    $('#drawer').hidden = false;
    const t = $('#secSound');
    if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  $('#vol').oninput = e => { S.master = +e.target.value; if (A.master) A.master.gain.value = S.master; };
  const tg = { tEntries: 'entries', tCS: 'cs', tThreads: 'threads', tDim: 'dim',
               tGrid: 'grid', tDiss: 'diss', tCross: 'cross', tScore: 'score', tKeys: 'keys' };
  for (const id in tg) $('#' + id).onchange = e => {
    S.show[tg[id]] = e.target.checked;
    if (tg[id] === 'score') { applyScoreClasses(); buildKeyboard(); paint(true); return; }
    if (tg[id] === 'keys') { buildKeyboard(); paint(true); return; }
    if (tg[id] === 'dim') { $('#rollHost svg').classList.toggle('dim', S.show.dim); applyScoreClasses(); return; }
    buildRoll(); buildScoreOverlay(); applyScoreClasses(); paint(true);
  };
  document.querySelectorAll('#spacingSeg button').forEach(b => b.onclick = () => {
    if (S.spacing === b.dataset.sp) return;
    const q = currentQ();
    S.spacing = b.dataset.sp;
    document.querySelectorAll('#spacingSeg button').forEach(x => x.classList.toggle('on', x === b));
    buildGeometry(); relayout();
    const sc = $('#scroller'); setScroll(sc, G.xu(q) * S.PXU - sc.clientWidth * 0.33);
  });
  $('#labAlign').onchange = buildLab;
  $('#helpBtn').onclick = () => $('#help').hidden = false;
  $('#helpClose').onclick = () => $('#help').hidden = true;
  $('#help').onclick = e => { if (e.target.id === 'help') $('#help').hidden = true; };
  addEventListener('keydown', ev => {
    if (ev.target.matches('input,textarea')) return;
    const doc = S.doc; if (!doc) return;
    const K = ev.key;
    if (K === ' ') { ev.preventDefault(); S.playing ? pause() : play(); }
    else if (K === 'ArrowLeft' && ev.shiftKey) { prevEntry(-1); ev.preventDefault(); }
    else if (K === 'ArrowRight' && ev.shiftKey) { prevEntry(1); ev.preventDefault(); }
    else if (K === 'ArrowLeft') { seek(G.barOfQ(currentQ() - 1e-4).q0 - doc.qbar); ev.preventDefault(); }
    else if (K === 'ArrowRight') { seek(G.barOfQ(currentQ()).q1); ev.preventDefault(); }
    else if (K === 'Home') seek(0);
    else if (K === 'l' || K === 'L') { S.loop = currentSection(); setLoop(S.loop, !S.loopOn); }
    else if (K === 's' || K === 'S') { S.spotlight = !S.spotlight; $('#spotlight').checked = S.spotlight; }
    else if (K === '0') { S.solo = -1; S.mute.fill(false); refreshVoices(); }
    else if (/^[1-9]$/.test(K)) { const v = +K - 1; if (v < doc.nv) { S.solo = S.solo === v ? -1 : v; refreshVoices(); } }
    else if (K === 'Escape') { $('#drawer').hidden = true; $('#picker').hidden = true; $('#help').hidden = true; }
    else if (K === 'n' || K === 'N') $('#drawer').hidden = !$('#drawer').hidden;
  });
  addEventListener('resize', () => { buildMap(); paint(true); });
}
function prevEntry(dir) {
  const doc = S.doc, q = currentQ();
  const qs = doc.entries.map(e => e.q0).sort((a, b) => a - b);
  let t = null;
  if (dir > 0) t = qs.find(x => x > q + 1e-3);
  else { const c = qs.filter(x => x < q - 1e-3); t = c.length ? c[c.length - 1] : 0; }
  if (t != null) seek(t);
}

/* =================================================================== boot */
async function selectPiece(id) {
  pause();
  const { doc, svg, svgP } = await loadPiece(id);
  S.doc = doc; S.svg = svg; S.svgP = svgP; S.id = id; S.q = 0; S.loop = null; S.loopOn = false;
  S.bpm = doc.bpm; $('#tempo').value = doc.bpm; $('#tempoOut').textContent = doc.bpm;
  $('#pTitle').textContent = doc.title;
  $('#pBwv').textContent = doc.bwv;
  $('#pBook').textContent = doc.book;
  $('#pKey').textContent = doc.key;
  $('#pMeter').textContent = doc.meter;
  $('#pVoices').textContent = doc.nv + ' voices';
  $('#pBlurb').innerHTML = md(doc.blurb);
  $('#pieceBtnTitle').textContent = doc.title;
  $('#pieceBtnSub').textContent = `${doc.bwv} · ${doc.nv} voices`;
  document.querySelectorAll('#picker .pcard').forEach(b => b.classList.toggle('on', b.dataset.id === id));
  buildDrawer(doc);
  history.replaceState(null, '', location.pathname + '?piece=' + id);
  buildGeometry();
  buildVoicePanel();
  if (A.ctx) buildVoiceChain(doc.nv);
  relayout();
  buildMap();
  buildLegend();
  buildLab();
  setScroll($('#scroller'), 0);
  paint(true);
}
const GROUPS = [
  ['wtc1', 'The Well-Tempered Clavier, Book I (1722)'],
  ['wtc2', 'The Well-Tempered Clavier, Book II (c. 1740)'],
  ['aof',  'The Art of Fugue (c. 1745–50)'],
];
function groupOf(p) {
  if (p.book.startsWith('WTC I,')) return 'wtc1';
  if (p.book.startsWith('WTC II')) return 'wtc2';
  return 'aof';
}
function buildPicker(idx) {
  const host = $('#picker');
  host.innerHTML = '';
  // 58 fugues is too many to scan, so the list filters as you type
  const box = el('div', { class: 'pfilter' });
  const inp = el('input', { type: 'search', id: 'pfind', placeholder: 'Filter: key, BWV, book, voices\u2026',
                            autocomplete: 'off', spellcheck: 'false' });
  const count = el('span', { class: 'pcount' });
  box.append(inp, count);
  host.append(box);
  for (const [key, label] of GROUPS) {
    const rows = idx.filter(p => groupOf(p) === key);
    if (!rows.length) continue;
    host.append(el('div', { class: 'grp' }, label));
    for (const p of rows) {
      const b = el('button', { class: 'pcard', 'data-id': p.id },
        el('b', {}, p.title),
        el('span', { class: 'sub' }, `${p.bwv} · ${p.book}`),
        el('span', { class: 'tags' },
          el('span', { class: 'tag v' }, `${p.nv} voices`),
          el('span', { class: 'tag' }, p.meter),
          el('span', { class: 'tag' }, `${p.bars} bars`),
          el('span', { class: 'tag' }, `${p.entries} entries`)));
      b.onclick = () => { $('#picker').hidden = true; selectPiece(p.id); };
      b.dataset.find = [p.title, p.bwv, p.book, p.key, p.meter, `${p.nv} voices`].join(' ').toLowerCase();
      host.append(b);
    }
  }
  const apply = () => {
    const q = inp.value.trim().toLowerCase();
    let shown = 0;
    for (const b of host.querySelectorAll('.pcard')) {
      const hit = !q || q.split(/\s+/).every(t => b.dataset.find.includes(t));
      b.hidden = !hit; if (hit) shown++;
    }
    // hide a group heading whose whole group filtered away
    for (const g of host.querySelectorAll('.grp')) {
      let n = g.nextElementSibling, any = false;
      while (n && !n.classList.contains('grp')) { if (!n.hidden) { any = true; break; } n = n.nextElementSibling; }
      g.hidden = !any;
    }
    count.textContent = q ? `${shown} of ${idx.length}` : `${idx.length} fugues`;
  };
  inp.oninput = apply;
  inp.onkeydown = e => {
    if (e.key === 'Escape') { if (inp.value) { inp.value = ''; apply(); } else $('#picker').hidden = true; e.stopPropagation(); }
    if (e.key === 'Enter') { const f = host.querySelector('.pcard:not([hidden])'); if (f) f.click(); }
  };
  apply();
}
function buildDrawer(doc) {
  const body = $('#drawerBody');
  $('#drawerTitle').textContent = `${doc.title} · ${doc.bwv}`;
  const sec = (h, ...kids) => el('section', { class: 'dsec' }, el('h4', {}, h), ...kids);

  const kinds = {};
  doc.entries.forEach(e => kinds[e.kind] = (kinds[e.kind] || 0) + 1);
  const facts = el('div', { class: 'facts' });
  const fact = (k, v) => facts.append(el('div', {}, el('div', { class: 'k' }, k), el('div', { class: 'v' }, v)));
  fact('Voices', String(doc.nv));
  fact('Bars', String(doc.bars.length));
  fact('Metre', doc.meter);
  fact('Key', doc.key);
  fact('Subject', `${doc.subject.len} notes · ${(Math.round((doc.subject.q1 - doc.subject.q0) / doc.qbar * 100) / 100)} bars`);
  fact('Statements', String(doc.entries.length));
  fact('Strettos', String(doc.stretto.length));
  fact('Episodes', String(doc.episodes.length));

  const term = (t, d) => el('div', {}, el('b', {}, t), el('span', { html: d }));

  body.replaceChildren(
    sec('At a glance', facts),
    // the last paragraph is the shared note on the collection, identical across every
    // piece in it, so it reads as a footnote rather than as this fugue's history
    sec('About this fugue',
      ...doc.history.slice(0, -1).map(t => el('p', { html: md(t) })),
      el('p', { class: 'dnote', html: md(doc.history[doc.history.length - 1]) })),
    sec('Scores, sources & data', el('div', { class: 'dlinks' },
      ...doc.links.map(l => el('a', { href: l.url, target: '_blank', rel: 'noopener' },
        el('span', { class: 'who' }, l.label), el('span', { class: 'arr' }, '↗'))))),
    sec('Listen elsewhere', el('div', { class: 'dlinks' },
      ...doc.performances.map(p => el('a', {
        href: 'https://www.youtube.com/results?search_query=' + encodeURIComponent(p.q),
        target: '_blank', rel: 'noopener',
      }, el('span', {}, el('span', { class: 'who' }, p.who), el('br'), el('span', { class: 'note' }, p.note)),
         el('span', { class: 'arr' }, '↗')))),
      el('p', { class: 'dnote', style: 'margin-top:9px' },
        'These run a search rather than pointing at one video. Recordings get taken down; searches don\'t.')),
    (() => { const x = sec('About the sound',
      el('p', {}, 'Bach wrote no dynamics, so there are none here. A harpsichord answers the same ' +
        'way however hard you press, and The Art of Fugue does not even name an instrument.'),
      el('p', { html: 'Playback is flat by default. Two switches above change that: ' +
        '<b>metrical accents</b> leans slightly on downbeats, and <b>spotlight subject</b> lifts ' +
        'whichever voice is stating the theme and ducks the rest. Both are for following the ' +
        'counterpoint, not for playing it.' }),
      el('p', { class: 'dnote' }, 'Low notes get extra weight so the bass survives under three ' +
        'other voices; that is mixing, and it is always on. Ornaments are drawn but not played.'));
      x.id = 'secSound'; return x; })(),
    sec('What the labels mean', el('div', { class: 'dterms' },
      term('Subject', 'The theme, alone at the start.'),
      term('Answer', 'The same theme a fifth up, or a fourth down, bringing in the second voice. A <i>tonal</i> answer ' +
                     'bends a note or two of its head to stay in key; a <i>real</i> answer transposes exactly.'),
      term('Countersubject', 'What the first voice plays against the answer, if it comes back with later entries.'),
      term('Episode', 'The stretches between entries, usually spun from fragments of the subject.'),
      term('Stretto', 'Entries overlapping: the next voice starts before the last has finished.'),
      term('Inversion', 'The subject upside down, every rise a fall.'))),
    sec('How the analysis works', el('p', { class: 'dnote' },
      'Pitches come from a Humdrum **kern edition, which spells every accidental out, so they are ' +
      'the edition\'s and not a guess. Verovio engraves. Entries are found by sliding the opening ' +
      'statement over every voice and comparing letter-name steps rather than semitones, so a tonal ' +
      'answer still matches. ' +
      (doc.subjectHeadOnly
        ? 'One caveat here: the bracket marks the head of the subject, not the whole of it. Bach ' +
          're-values the tail when he brings the subject back, and a template that includes the ' +
          'tail finds far fewer of the entries that are plainly there.'
        : doc.subjectByHand
        ? 'Where the subject itself ends was set by hand for this one — the detector picked a ' +
          'fragment of the head, which then matched far too much.'
        : 'Where the subject ends was worked out by the build too.'))),
  );
}
async function boot() {
  const idx = await loadIndex();
  G.index = idx;
  buildPicker(idx);
  const pb = $('#pieceBtn'), pk = $('#picker');
  pb.onclick = e => {
    e.stopPropagation(); pk.hidden = !pk.hidden;
    if (!pk.hidden) { const f = $('#pfind'); if (f) { f.select(); f.focus(); } }
  };
  document.addEventListener('click', e => {
    if (!pk.hidden && !pk.contains(e.target) && e.target !== pb) pk.hidden = true;
  });
  $('#notesBtn').onclick = () => $('#drawer').hidden = !$('#drawer').hidden;
  $('#drawerClose').onclick = () => $('#drawer').hidden = true;
  wireControls(); wireStage(); wireTips();
  const want = new URLSearchParams(location.search).get('piece');
  await selectPiece(idx.some(p => p.id === want) ? want : idx[0].id);
  const frame = () => { if (S.playing) paint(false); requestAnimationFrame(frame); };
  requestAnimationFrame(frame);
}
window.__FL = { S, G, A, seek, play, pause, paint };
boot();
})();
