/* Front page: everything drawn here comes from the same analysed data the lab uses. */
(async () => {
'use strict';

const $ = s => document.querySelector(s);
const NS = 'http://www.w3.org/2000/svg';
const sel = (t, a) => { const n = document.createElementNS(NS, t); for (const k in a) n.setAttribute(k, a[k]); return n; };
const VCOL = {
  2: ['#5cc8ff', '#52d6a4'],
  3: ['#5cc8ff', '#ffc247', '#52d6a4'],
  4: ['#5cc8ff', '#ffc247', '#ff7eb6', '#52d6a4'],
};
const vcol = (nv, i) => (VCOL[nv] || VCOL[4])[i] || '#8e9aac';

/* ------------------------------------------------------------- mini rolls */
function rollSvg(t, opts) {
  const { W, H, q0 = 0, q1 = t.total, pad = 6, boxes = false, labels = false,
          grid = false, nh = null, dim = 0.3 } = opts;
  const notes = t.notes.filter(n => n[0] + n[1] > q0 && n[0] < q1);
  if (!notes.length) return sel('svg', {});
  const lo = Math.min(...notes.map(n => n[2])) - 1.5;
  const hi = Math.max(...notes.map(n => n[2])) + 1.5;
  const X = q => ((q - q0) / (q1 - q0)) * W;
  const top = labels ? 16 : pad;
  const Y = p => top + (H - top - pad) * (1 - (p - lo) / (hi - lo));
  const h = nh || Math.max(2, (H - top - pad) / (hi - lo) * 0.95);
  const svg = sel('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H,
                           preserveAspectRatio: 'none' });
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

  if (grid) for (let q = Math.ceil(q0 / t.qbar) * t.qbar; q < q1; q += t.qbar)
    svg.append(sel('line', { x1: X(q), x2: X(q), y1: 0, y2: H, stroke: '#1e2530', 'stroke-width': 1 }));
  for (const [a, b] of (t.episodes || []))
    if (b > q0 && a < q1)
      svg.append(sel('rect', { x: X(Math.max(a, q0)), y: 0, width: Math.max(1, X(Math.min(b, q1)) - X(Math.max(a, q0))),
                               height: H, fill: 'rgba(255,255,255,.03)' }));
  // voice threads
  for (let v = 0; v < t.nv; v++) {
    const pts = notes.filter(n => n[3] === v)
      .map(n => `${X(n[0])},${Y(n[2])} ${X(n[0] + n[1])},${Y(n[2])}`).join(' ');
    if (pts) svg.append(sel('polyline', { points: pts, fill: 'none', stroke: vcol(t.nv, v),
                                          'stroke-width': 1, opacity: .35 }));
  }
  for (const n of notes) {
    const x = X(n[0]), w = Math.max(1.4, X(n[0] + n[1]) - x - 0.5);
    svg.append(sel('rect', { x, y: Y(n[2]) - h / 2, width: w, height: h, rx: Math.min(2, h / 2),
                             fill: vcol(t.nv, n[3]), opacity: n[4] ? 1 : dim }));
  }
  if (boxes) for (const [v, a, b, role, on] of t.entries) {
    if (b <= q0 || a >= q1) continue;
    const ns = notes.filter(n => n[3] === v && n[0] >= a - 1e-6 && n[0] < b - 1e-6);
    if (!ns.length) continue;
    const plo = Math.min(...ns.map(n => n[2])), phi = Math.max(...ns.map(n => n[2]));
    const x0 = X(a) - 3, x1 = X(Math.min(b, q1)) + 1;
    const y0 = Y(phi) - h / 2 - 6, y1 = Y(plo) + h / 2 + 3;
    svg.append(sel('rect', { x: x0, y: y0, width: x1 - x0, height: y1 - y0, rx: 4,
                             fill: 'none', stroke: vcol(t.nv, v), 'stroke-opacity': .8, 'stroke-width': 1.1 }));
    if (labels) {
      const tx = sel('text', { x: x0 + 4, y: y0 - 3, fill: vcol(t.nv, v),
                               'font-size': 9.5, 'font-weight': 650,
                               'font-family': 'ui-sans-serif,system-ui' });
      tx.textContent = `${role} · ${on}`;
      svg.append(tx);
    }
  }
  if (boxes) for (const [v, a, b] of (t.counters || [])) {
    if (b <= q0 || a >= q1) continue;
    const ns = notes.filter(n => n[3] === v && n[0] >= a - 1e-6 && n[0] < b - 1e-6);
    if (!ns.length) continue;
    const plo = Math.min(...ns.map(n => n[2])), phi = Math.max(...ns.map(n => n[2]));
    svg.append(sel('rect', { x: X(a) - 2, y: Y(phi) - h / 2 - 4, rx: 4,
                             width: X(Math.min(b, q1)) - X(a) + 3, height: Y(plo) - Y(phi) + h + 8,
                             fill: 'none', stroke: '#98a3b3', 'stroke-width': 1,
                             'stroke-dasharray': '3 3', 'stroke-opacity': .7 }));
  }
  return svg;
}

/* A tiny structural map: what shape does this fugue have from a distance? */
function mapSvg(t, { W, H }) {
  const lane = H / t.nv, X = q => (q / t.total) * W;
  const svg = sel('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H,
                           preserveAspectRatio: 'none' });
  for (const [a, b] of (t.episodes || []))
    svg.append(sel('rect', { x: X(a), y: 0, width: Math.max(1, X(b) - X(a)), height: H,
                             fill: 'rgba(255,255,255,.035)' }));
  // strettos: where two entries overlap
  for (let i = 0; i < t.entries.length; i++)
    for (let j = i + 1; j < t.entries.length; j++) {
      const a = t.entries[i], b = t.entries[j];
      const s0 = Math.max(a[1], b[1]), s1 = Math.min(a[2], b[2]);
      if (s1 > s0) svg.append(sel('rect', { x: X(s0), y: 0, width: Math.max(1, X(s1) - X(s0)),
                                            height: H, fill: 'rgba(255,107,107,.14)' }));
    }
  for (let v = 0; v < t.nv; v++) {
    const y = v * lane + lane / 2;
    svg.append(sel('line', { x1: 0, x2: W, y1: y, y2: y, stroke: '#1e2530', 'stroke-width': 1 }));
    const g = sel('g', { opacity: .45 });
    for (const n of t.notes) if (n[3] === v)
      g.append(sel('rect', { x: X(n[0]), y: y - 0.9, width: Math.max(0.5, X(n[0] + n[1]) - X(n[0])),
                             height: 1.8, fill: vcol(t.nv, v) }));
    svg.append(g);
  }
  for (const [v, a, b] of t.entries)
    svg.append(sel('rect', { x: X(a), y: v * lane + 1.5, width: Math.max(2, X(b) - X(a)),
                             height: lane - 3, rx: 2, fill: vcol(t.nv, v), 'fill-opacity': .85 }));
  return svg;
}

/* --------------------------------------------------------- feature icons */
function icons() {
  const mk = (id, draw) => {
    const svg = sel('svg', { viewBox: '0 0 200 58' });
    draw(svg); $(id).replaceChildren(svg);
  };
  const C = ['#5cc8ff', '#ffc247', '#52d6a4'];
  mk('#fi1', s => {
    for (let k = 0; k < 3; k++) {
      const y = 9 + k * 18;
      for (let l = 0; l < 5; l++)
        s.append(sel('line', { x1: 12, x2: 188, y1: y + l * 2.6, y2: y + l * 2.6, stroke: '#2b3542', 'stroke-width': .8 }));
      for (let n = 0; n < 5; n++)
        s.append(sel('ellipse', { cx: 34 + n * 32 + k * 7, cy: y + 2 + (n % 3) * 2.6, rx: 3.4, ry: 2.5, fill: C[k] }));
    }
  });
  mk('#fi2', s => {
    for (let l = 0; l < 5; l++)
      s.append(sel('line', { x1: 12, x2: 188, y1: 8 + l * 2.6, y2: 8 + l * 2.6, stroke: '#2b3542', 'stroke-width': .8 }));
    const xs = [30, 62, 94, 126, 158];
    xs.forEach((x, i) => {
      s.append(sel('ellipse', { cx: x, cy: 11 + (i % 3) * 2.6, rx: 3.4, ry: 2.5, fill: '#5cc8ff' }));
      s.append(sel('line', { x1: x, x2: x, y1: 16, y2: 34, stroke: '#3d4a5c', 'stroke-width': .8, 'stroke-dasharray': '2 2' }));
      s.append(sel('rect', { x: x - 12, y: 36 + (i % 3) * 5, width: 24, height: 5, rx: 2.5, fill: '#5cc8ff' }));
    });
  });
  mk('#fi3', s => {
    const shape = [0, 3, 1, 5, 2];
    [[16, 6, C[0]], [70, 20, C[1]], [124, 12, C[2]]].forEach(([x0, y0, col]) => {
      shape.forEach((d, i) => s.append(sel('rect', { x: x0 + i * 11, y: y0 + d * 4, width: 9, height: 4.5, rx: 2, fill: col })));
      s.append(sel('path', { d: `M${x0 - 3} ${y0 - 5} L${x0 - 3} ${y0 - 9} L${x0 + 57} ${y0 - 9} L${x0 + 57} ${y0 - 5}`,
                             fill: 'none', stroke: col, 'stroke-width': 1.1, 'stroke-opacity': .8 }));
    });
  });
  mk('#fi4', s => {
    [[0, 1], [1, .22], [2, .22]].forEach(([k, op]) => {
      const y = 12 + k * 15;
      for (let i = 0; i < 8; i++)
        s.append(sel('rect', { x: 14 + i * 22, y: y + (i % 3) * 3, width: 17, height: 5, rx: 2.5,
                               fill: C[k], opacity: op }));
    });
  });
}

/* -------------------------------------------------------------------- go */
const GROUPS = [
  ['WTC I,',  'The Well-Tempered Clavier, Book I (1722)'],
  ['WTC II,', 'The Well-Tempered Clavier, Book II (c. 1740)'],
  ['The Art',  'The Art of Fugue (c. 1745–50)'],
];
const NOTE = {
  bwv855: 'The only two-voice fugue in either book — one line above, one below, nothing to hide behind.',
  bwv847: 'The textbook fugue: a compact subject, one regular countersubject, cleanly separated episodes.',
  bwv851: 'Fast, tight, and halfway through Bach turns the subject upside down.',
  bwv856: 'A dancing 3/8 fugue on a long, almost entirely stepwise subject.',
  bwv866: 'A cheerful subject nearly four bars long, which leaves room for only a handful of entries.',
  bwv846: 'Almost nothing but subject: entry piles on entry in stretto for twenty-seven bars.',
  bwv861: 'Four voices and a sharply characterised subject that keeps its countersubject close.',
  bwv878: 'Bach writing deliberately in the old style: long white notes, counterpoint in slow motion.',
  'bwv1080-1': 'The plain opening statement of the greatest fugal project ever undertaken.',
};

const [index, teasers] = await Promise.all([
  fetch('data/index.json').then(r => r.json()),
  fetch('data/teasers.json').then(r => r.json()),
]);

icons();

// hero: the exposition of the C minor fugue
const t847 = teasers.bwv847;
$('#teaser').replaceChildren(rollSvg(t847, { W: 620, H: 250, q0: 0, q1: 29,
  boxes: true, labels: true, grid: true, nh: 4.6, dim: .26, pad: 14 }));

// the nine fugues
const grid = $('#pieceGrid');
for (const [key, label] of GROUPS) {
  const rows = index.filter(p => p.book.startsWith(key));
  if (!rows.length) continue;
  grid.insertAdjacentHTML('beforeend', `<div class="pgrp">${label}</div>`);
  for (const p of rows) {
    const a = document.createElement('a');
    a.className = 'pc';
    a.href = `lab.html?piece=${p.id}`;
    a.innerHTML =
      `<div class="ph"><b>${p.title}</b><span class="bwv">${p.bwv}</span></div>` +
      `<div class="sub">${p.book} · ${p.key} · ${p.meter}</div>` +
      `<div class="note">${NOTE[p.id] || ''}</div>` +
      `<div class="tags"><span class="tag v">${p.nv} voices</span>` +
      `<span class="tag">${p.bars} bars</span><span class="tag">${p.entries} entries</span></div>`;
    const mini = document.createElement('div');
    mini.className = 'mini';
    mini.append(mapSvg(teasers[p.id], { W: 250, H: 34 }));
    a.append(mini);
    grid.append(a);
  }
}
})();
