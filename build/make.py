"""Full pipeline: Humdrum **kern  ->  engraved SVG (two spacings) + analysed JSON."""
import sys, os, json, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from kernparse import parse, merge_ties
from analyze import by_voice, make_template, find_statements, dedupe
from autosubject import find_subject
from build import extract as verovio_extract
from pieces import PIECES, VOICE_NAMES
from kernprep import normalise as normalise_kern

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA = os.path.join(PROJ, "data")
PRO  = {"spacingNonLinear": 1.0, "spacingLinear": 0.07}

KK_MAJ = [6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]
KK_MIN = [6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17]
PC_SHARP = ['C','C♯','D','D♯','E','F','F♯','G','G♯','A','A♯','B']
PC_FLAT  = ['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B']

def corr(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    num = sum((a-mx)*(b-my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a-mx)**2 for a in x)); dy = math.sqrt(sum((b-my)**2 for b in y))
    return num/(dx*dy) if dx and dy else 0.0

def best_key(hist):
    best = None
    for tonic in range(12):
        for mode, prof in (("major", KK_MAJ), ("minor", KK_MIN)):
            rot = [prof[(i - tonic) % 12] for i in range(12)]
            c = corr(hist, rot)
            if best is None or c > best[0]: best = (c, tonic, mode)
    return best

def key_name(tonic, mode, flats=True):
    return f"{(PC_FLAT if flats else PC_SHARP)[tonic]} {'maj' if mode=='major' else 'min'}"

# ------------------------------------------------------------------ kern head
def kern_header(path, modern_clefs=False):
    """Meter, key and (optionally) the editor's modern clef substitutes."""
    meter, keysig, keytok = None, None, None
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    for ln in lines:
        if ln.startswith('*M') and re.match(r'\*M\d+/\d+', ln.split('\t')[0]):
            meter = meter or ln.split('\t')[0][2:]
        if ln.startswith('*k['): keysig = keysig or ln.split('\t')[0][2:]
        m = re.match(r'\*([A-Ga-g][#-]?):', ln.split('\t')[0])
        if m and keytok is None: keytok = m.group(1)
    return meter or '4/4', keysig or '', keytok or 'C'

def key_label(keytok):
    letter = keytok[0]
    acc = {'#': '♯', '-': '♭', '': ''}[keytok[1:2] if len(keytok) > 1 else '']
    mode = 'minor' if letter.islower() else 'major'
    return f"{letter.upper()}{acc} {mode}", (mode == 'minor')

def modernise_clefs(src, dst):
    """The Art of Fugue kern carries original C clefs plus the editor's modern
    equivalents; swap them so the score reads on treble/bass staves."""
    lines = open(src, encoding='utf-8').read().split('\n')
    mclef = next(([t.replace('*mclef', '*clef') for t in ln.split('\t')]
                  for ln in lines if ln.startswith('*mclef')), None)
    out, done = [], False
    for ln in lines:
        if ln.startswith('*mclef'): continue
        if ln.startswith('*clef') and mclef and not done:
            out.append('\t'.join(mclef)); done = True; continue
        out.append(ln)
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    return dst

# ------------------------------------------------------------------ labelling
def strip_stems(src, dst):
    """Verovio 6.3 silently drops the xml:id of a handful of notes that carry an
    explicit stem-direction marker (/ or \\). The markers are cosmetic — verovio
    stems by itself — so when geometry comes back short we re-render without them."""
    out = []
    for ln in open(src, encoding='utf-8', errors='replace').read().split('\n'):
        if ln[:1] in ('!', '*', '='):
            out.append(ln)
        else:
            out.append('\t'.join(t.replace('/', '').replace('\\', '')
                                  for t in ln.split('\t')))
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    return dst

def label_for(st, flats):
    if st['form'] == 'I':   return "Inversion", (PC_FLAT if flats else PC_SHARP)[st['p0'] % 12]
    if st['form'] == 'Aug': return "Augmented", (PC_FLAT if flats else PC_SHARP)[st['p0'] % 12]
    deg = st['K'] % 7
    role = "Answer" if deg == 4 else "Subject"
    return role, (PC_FLAT if flats else PC_SHARP)[st['p0'] % 12]

def statement_dict(st, flats, motif):
    role, on = label_for(st, flats)
    return {'v': st['v'], 'q0': round(st['q'], 4), 'q1': round(st['endq'], 4),
            'role': role, 'on': on, 'kind': st['kind'], 'form': st['form'],
            'K': st['K'], 'C': st['C'], 'p0': st['p0'],
            'dhit': st['dhit'], 'N': st['N'], 'chit': st['chit'], 'motif': motif}

# ----------------------------------------------------------------------- main
def build(P):
    krn = os.path.join(HERE, "kern-open", P["file"])
    krn, fixed = normalise_kern(krn, os.path.join(HERE, "kern-open", "_n_" + P["file"]))
    if fixed: print(f"  {P['id']}: normalised kern ({fixed})")
    if P.get("modernClefs"):
        krn = modernise_clefs(krn, os.path.join(HERE, "kern-open", "_mc_" + P["file"]))

    ev, marks, total = parse(krn)
    notes = merge_ties(ev)
    nv = max(n['spine'] for n in notes) + 1
    for n in notes: n['v'] = nv - 1 - n['spine']

    meter, keysig, keytok = kern_header(krn)
    key_text, is_minor = key_label(keytok)
    flats = ('-' in keysig) or keysig == ''
    mnum, mden = (int(x) for x in meter.split('/'))
    beats, qpb = mnum, 4.0 / mden

    # ---- geometry from verovio, in two spacings
    for attempt in (0, 1):
        tk,  svg,  vnotes,  vmeasures,  viewBox,  staffboxes,  *_ = verovio_extract(krn)
        tk2, svgP, vnotesP, vmeasuresP, viewBoxP, _,            *_ = verovio_extract(krn, PRO)
        pos, posP = {n['id']: n for n in vnotes}, {n['id']: n for n in vnotesP}
        for n in notes:
            g = next((pos[i] for i in n['ids'] if i in pos), None)
            gp = next((posP[i] for i in n['ids'] if i in posP), None)
            n['x'], n['y'] = (g['x'], g['y']) if g else (None, None)
            n['xp'] = gp['x'] if gp else None
        missing = [n for n in notes if n['x'] is None or n['xp'] is None]
        if not missing or attempt: break
        # stripping the cosmetic stem markers gets the dropped ids back; line
        # numbers are untouched, so the kern-side note ids still line up
        print(f"  {P['id']}: {len(missing)} notes without geometry, re-rendering without stem markers")
        krn = strip_stems(krn, os.path.join(HERE, "kern-open", "_ns_" + P["file"]))
    assert not missing, f"{P['id']}: {len(missing)} notes without geometry, e.g. {missing[:2]}"

    # ---- bars.  An anacrusis has no "=" marker of its own, but Verovio still
    #      engraves it as a measure, so record it or every bar is one out.
    bars = []
    marked = [m for m in marks if m['n'] is not None]
    if marked and marked[0]['q'] > 1e-9:
        bars.append({'n': 0, 'q0': 0.0, 'q1': marked[0]['q']})
    for i, m in enumerate(marked):
        q1 = marked[i+1]['q'] if i+1 < len(marked) else total
        bars.append({'n': m['n'], 'q0': m['q'], 'q1': q1})
    full = [b for b in bars if b['n'] > 0]
    qbar = (full[0]['q1'] - full[0]['q0']) if full else 4.0
    assert len(bars) == len(vmeasures), \
        f"{P['id']}: {len(bars)} bars but {len(vmeasures)} engraved measures"

    for i, b in enumerate(bars):
        b['x0']  = round(vmeasures[i]['x0'], 2)  if i < len(vmeasures)  else None
        b['x1']  = round(vmeasures[i]['x1'], 2)  if i < len(vmeasures)  else None
        b['px0'] = round(vmeasuresP[i]['x0'], 2) if i < len(vmeasuresP) else None
        b['px1'] = round(vmeasuresP[i]['x1'], 2) if i < len(vmeasuresP) else None
    pickup = bars[0]['q0'] if bars else 0.0

    def anchors(xkey, bkey):
        a = {}
        for n in notes:
            q = round(n['q'], 6); a[q] = min(a.get(q, 1e9), n[xkey])
        for b in bars:
            if b[bkey] is not None:
                q = round(b['q0'], 6); a[q] = min(a.get(q, 1e9), b[bkey])
        return [[q, round(a[q], 2)] for q in sorted(a)]

    # ---- subject, answer, countersubject
    V = by_voice(notes)
    S = P.get("subject")
    subject_by_hand = bool(S)          # the detector got this one wrong; the span is set in pieces.py
    if not S: S = find_subject(notes)
    # Some subjects begin with the very notes every answer bends, so a template that
    # includes them matches nothing. `head` is where the subject really starts: match
    # on the span, then draw each bracket from the head so it still covers the theme.
    head_q0 = S.get('head', S['q0'])
    head_shift = round(S['q0'] - head_q0, 6)
    assert head_shift >= 0, f"{P['id']}: subject head must come before the matched span"
    tpl = make_template(V, S['v'], S['q0'], S['q1'])
    full_tpl = make_template(V, S['v'], head_q0, S['q1']) if head_shift else tpl
    forms = [('P', 1, 1.0)]
    for f in P.get("forms", ()):
        if f == 'I': forms.append(('I', -1, 1.0))
        if f == 'Aug': forms.append(('Aug', 1, 2.0))
    sts = dedupe(find_statements(V, tpl, forms=tuple(forms)))
    sts = [s for s in sts if s['form'] == 'P' or s['kind'] in ('exact', 'tonal', 'altered')]
    entries = [statement_dict(s, flats, 'subject') for s in sts]
    if head_shift:
        for e in entries: e['q0'] = round(e['q0'] - head_shift, 6)

    counters = []
    cs_span = P.get("counter")
    if cs_span is None:
        # what the first voice plays against the answer, if it comes back with later entries
        ansQ = min((e['q0'] for e in entries if e['v'] != S['v']), default=None)
        if ansQ is not None:
            cs_span = dict(v=S['v'], q0=ansQ, q1=ansQ + (S['q1'] - S['q0']))
    if cs_span:
        cseq = [n for n in V[cs_span['v']] if cs_span['q0'] <= n['q'] < cs_span['q1']]
        if len(cseq) >= 6:
            ctpl = make_template(V, cs_span['v'], cs_span['q0'], cs_span['q1'])
            cst = [s for s in dedupe(find_statements(V, ctpl))
                   if s['kind'] in ('exact', 'tonal', 'altered')]
            if len(cst) >= 3:
                counters = [statement_dict(s, flats, 'counter') for s in cst]
                for c in counters: c['role'] = 'Countersubject'

    for n in notes: n['e'] = -1; n['cs'] = -1
    for idx, e in enumerate(entries):
        for n in V[e['v']]:
            if e['q0'] - 1e-6 <= n['q'] < e['q1'] - 1e-6: n['e'] = idx
    for idx, e in enumerate(counters):
        for n in V[e['v']]:
            if e['q0'] - 1e-6 <= n['q'] < e['q1'] - 1e-6 and n['e'] < 0: n['cs'] = idx

    stretto = [[i, j] for i in range(len(entries)) for j in range(i+1, len(entries))
               if entries[j]['q0'] < entries[i]['q1'] - 1e-6 and entries[i]['q0'] < entries[j]['q1'] - 1e-6]

    merged = []
    for a, b in sorted((e['q0'], e['q1']) for e in entries):
        if merged and a <= merged[-1][1] + 1e-6: merged[-1][1] = max(merged[-1][1], b)
        else: merged.append([a, b])
    episodes, cur = [], 0.0
    for a, b in merged:
        if a - cur >= qbar * 0.75: episodes.append([round(cur, 4), round(a, 4)])
        cur = max(cur, b)
    if total - cur >= qbar * 0.75: episodes.append([round(cur, 4), round(total, 4)])

    seen, expo_end = set(), 0.0
    for e in entries:
        seen.add(e['v']); expo_end = e['q1']
        if len(seen) == nv: break

    # ---- key path: per-bar key-profile correlations, smoothed with Viterbi so
    #      the reading only changes key when the evidence is worth the switch
    win = max(qbar * 1.5, 5.0)
    frames = []
    for b in bars:
        a0, a1 = max(0.0, b['q0'] - qbar * 0.3), min(total, b['q0'] + win)
        hist = [0.0] * 12
        for n in notes:
            s, t = max(n['q'], a0), min(n['q'] + n['d'], a1)
            if t > s: hist[n['p'] % 12] += (t - s)
        if sum(hist) == 0: continue
        scores = []
        for tonic in range(12):
            for mode, prof in (("major", KK_MAJ), ("minor", KK_MIN)):
                rot = [prof[(i - tonic) % 12] for i in range(12)]
                scores.append(corr(hist, rot))
        frames.append({'b': b, 's': scores})
    fixed = []
    if frames:
        KEYS = [(t, m) for t in range(12) for m in ("major", "minor")]
        home_pc = ([0,2,4,5,7,9,11]['CDEFGAB'.index(keytok[0].upper())]
                   + (1 if '#' in keytok else -1 if '-' in keytok else 0)) % 12
        home_i = KEYS.index((home_pc, 'minor' if keytok[0].islower() else 'major'))
        fifths = lambda a, b: min((a - b) % 12, (b - a) % 12)
        n_k, n_f = len(KEYS), len(frames)
        EDGE, DIST = 0.30, 0.02

        def viterbi(switch):
            bonus = lambda f, k: (EDGE if (k == home_i and (f < 2 or f >= n_f - 2)) else 0.0)
            dp = [frames[0]['s'][k] + bonus(0, k) for k in range(n_k)]
            bp = [[0] * n_k for _ in range(n_f)]
            for f in range(1, n_f):
                nd = [0.0] * n_k
                for k in range(n_k):
                    best_j, best_v = 0, -1e9
                    for j in range(n_k):
                        v = dp[j] - (0.0 if j == k else switch + DIST * fifths(KEYS[j][0], KEYS[k][0]))
                        if v > best_v: best_v, best_j = v, j
                    nd[k] = best_v + frames[f]['s'][k] + bonus(f, k)
                    bp[f][k] = best_j
                dp = nd
            k = max(range(n_k), key=lambda i: dp[i])
            path = [k]
            for f in range(n_f - 1, 0, -1):
                k = bp[f][k]; path.append(k)
            return path[::-1]

        # as much detail as the piece can carry without the ribbon turning to confetti
        target = max(4, min(9, round(len(bars) / 5) + 1))
        path = None
        for switch in (0.06, 0.09, 0.12, 0.16, 0.20, 0.26, 0.33, 0.42, 0.55, 0.7, 0.9, 1.2):
            path = viterbi(switch)
            if sum(1 for a, b in zip(path, path[1:]) if a != b) + 1 <= target: break
        for f, ki in zip(frames, path):
            name = key_name(KEYS[ki][0], KEYS[ki][1], flats)
            if fixed and fixed[-1]['k'] == name: fixed[-1]['q1'] = f['b']['q1']
            else: fixed.append({'q0': f['b']['q0'], 'q1': f['b']['q1'], 'k': name})
        fixed[0]['q0'] = 0.0
        for a, b in zip(fixed, fixed[1:]): a['q1'] = b['q0']
        fixed[-1]['q1'] = total

    # ---- pedal points in the lowest voice
    pedals, low, i = [], V[nv-1], 0
    while i < len(low):
        j = i
        while j + 1 < len(low) and low[j+1]['p'] == low[i]['p']: j += 1
        span = low[j]['q'] + low[j]['d'] - low[i]['q']
        if span >= qbar * 1.8:
            if pedals and low[i]['q'] < pedals[-1]['q1'] - 1e-6:
                pedals[-1]['q1'] = max(pedals[-1]['q1'], low[j]['q'] + low[j]['d'])
            else:
                pedals.append({'q0': low[i]['q'], 'q1': low[j]['q'] + low[j]['d'], 'p': low[i]['p']})
        i = j + 1

    out_notes = [{'id': n['ids'][0], 'ids': n['ids'], 'v': n['v'], 'p': n['p'], 'n': n['n'],
                  'q': round(n['q'], 4), 'd': round(n['d'], 4),
                  'x': round(n['x'], 2), 'xp': round(n['xp'], 2), 'y': round(n['y'], 2),
                  'e': n['e'], 'cs': n['cs']}
                 for n in sorted(notes, key=lambda z: (z['q'], -z['p']))]

    doc = {
        'id': P['id'], 'title': P['title'], 'bwv': P['bwv'], 'book': P['book'],
        'key': key_text, 'meter': meter, 'bpm': P['bpm'], 'blurb': P['blurb'],
        'card': P.get('card') or P['blurb'],
        'subjectByHand': subject_by_hand,
        'subjectSkipsHead': bool(head_shift),
        'subjectHeadOnly': bool(P.get('headOnly')),
        'history': P['history'], 'links': [{'label': a, 'url': b} for a, b in P['links']],
        'performances': P['performances'],
        'qpb': qpb, 'beats': beats, 'qbar': qbar, 'pickup': pickup,
        'nv': nv, 'voiceNames': VOICE_NAMES[nv], 'total': total,
        'viewBox': viewBox, 'viewBoxP': viewBoxP,
        'staffBox': {str(k): v for k, v in staffboxes.items()},
        'bars': bars, 'anchors': anchors('x', 'x0'), 'anchorsP': anchors('xp', 'px0'),
        'notes': out_notes,
        'subject': {'v': S['v'], 'q0': head_q0, 'q1': S['q1'], 'len': len(full_tpl),
                    'tpl': [{'dq': t['dq'], 'p': t['p'], 'd': t['d']} for t in full_tpl]},
        'entries': entries, 'counters': counters, 'stretto': stretto,
        'episodes': episodes, 'expoEnd': round(expo_end, 4),
        'keys': fixed, 'pedals': pedals,
    }
    os.makedirs(DATA, exist_ok=True)
    def clean(x):
        x = re.sub(r'<style type="text/css">.*?</style>', '', x, flags=re.S)
        x = re.sub(r'<desc>.*?</desc>', '', x, flags=re.S)
        x = re.sub(r'>\s+<', '><', x)                    # verovio indents heavily
        x = re.sub(r'\s{2,}', ' ', x).strip()
        # Verovio stamps the root element and every glyph definition with a fresh
        # random nonce on each run, so an unchanged piece would still rewrite its
        # whole SVG on every build. Drop the root id and the nonce; the glyph ids
        # stay unique within the file, and identical across files, which is fine
        # because a given code point is the same glyph either way.
        x = re.sub(r'^(<svg\b[^>]*?) id="[^"]*"', r'\1', x)
        x = re.sub(r'(id="E[0-9A-F]{3})-[a-z0-9]+"', r'\1"', x)
        x = re.sub(r'(href="#E[0-9A-F]{3})-[a-z0-9]+"', r'\1"', x)
        x = re.sub(r'(class="pageMilestoneEnd) [a-z0-9]+"', r'\1"', x)
        # only note / staff / measure ids are addressed by the app; drop the rest
        head, sep, tail = x.partition('</defs>')
        tail = re.sub(r' id="(?!note-|staff-|measure-)[^"]*"', '', tail)
        return head + sep + tail
    json.dump(doc, open(f"{DATA}/{P['id']}.json", "w"), separators=(',', ':'), ensure_ascii=False)
    open(f"{DATA}/{P['id']}.svg", "w").write(clean(svg))
    open(f"{DATA}/{P['id']}.p.svg", "w").write(clean(svgP))
    kinds = Counter(e['kind'] for e in entries)
    print(f"{P['id']:10s} {key_text:12s} {meter:4s} {nv}v {len(bars):3d} bars  "
          f"subj {len(tpl):2d} notes  entries {len(entries):2d} {dict(kinds)}  "
          f"CS {len(counters)}  epi {len(episodes)}  stretto {len(stretto):2d}  "
          f"json {os.path.getsize(f'{DATA}/{P['id']}.json')//1024}kB")
    return doc

def teaser(d):
    """The whole piece note by note — only the front page's hero figure needs this."""
    return {
        'id': d['id'], 'nv': d['nv'], 'total': d['total'], 'qbar': d['qbar'],
        'notes': [[round(n['q'], 2), round(n['d'], 2), n['p'], n['v'], 1 if n['e'] >= 0 else 0]
                  for n in d['notes']],
        'entries': [[e['v'], round(e['q0'], 2), round(e['q1'], 2), e['role'], e['on']]
                    for e in d['entries']],
        'counters': [[c['v'], round(c['q0'], 2), round(c['q1'], 2)] for c in d['counters']],
        'episodes': d['episodes'],
    }

MAP_BUCKETS = 160

def mapdata(d, buckets=MAP_BUCKETS):
    """A thumbnail-sized shape of the piece: one character per voice per instant,
    '1' where that voice is sounding. The cards draw voices as lanes and ignore pitch,
    so this is all they need, and it is a fiftieth of the bytes — which matters because
    the front page loads every piece's map at once."""
    total = d['total'] or 1.0
    w = total / buckets
    lanes = [['0'] * buckets for _ in range(d['nv'])]
    byv = {}
    for n in d['notes']:
        byv.setdefault(n['v'], []).append(n)
    for v, seq in byv.items():
        seq.sort(key=lambda n: n['q'])
        i = 0
        for k in range(buckets):
            t = (k + 0.5) * w
            while i + 1 < len(seq) and seq[i + 1]['q'] <= t: i += 1
            n = seq[i]
            if n['q'] <= t < n['q'] + n['d'] + 1e-9: lanes[v][k] = '1'
    lanes = [''.join(L) for L in lanes]
    return {
        'nv': d['nv'], 'total': round(total, 2), 'qbar': d['qbar'], 'lanes': lanes,
        'entries': [[e['v'], round(e['q0'], 2), round(e['q1'], 2)] for e in d['entries']],
        'episodes': [[round(a, 2), round(b, 2)] for a, b in d['episodes']],
        'stretto': [[round(d['entries'][i]['q0'], 2), round(d['entries'][j]['q1'], 2)]
                    for i, j in d['stretto']],
    }

if __name__ == "__main__":
    only = set(sys.argv[1:])
    docs, failed = [], []
    for P in PIECES:
        if only and P['id'] not in only: continue
        try:
            docs.append(build(P))
        except Exception as e:
            failed.append((P['id'], f"{type(e).__name__}: {e}"))
            print(f"  !! {P['id']} FAILED: {type(e).__name__}: {str(e)[:120]}")
    if failed:
        print(f"\n{len(failed)} of {len(failed)+len(docs)} pieces failed to build:")
        for i, m in failed: print(f"  {i:12s} {m[:150]}")
        print("(they are left out of index.json rather than shipped broken)\n")
    HERO = "bwv847"
    for d in docs:
        if d['id'] == HERO:
            json.dump(teaser(d), open(f"{DATA}/hero.json", "w"),
                      separators=(',', ':'), ensure_ascii=False)
    mp = {}
    if only and os.path.exists(f"{DATA}/maps.json"):
        mp = json.load(open(f"{DATA}/maps.json", encoding="utf-8"))
    mp.update({d['id']: mapdata(d) for d in docs})
    json.dump(mp, open(f"{DATA}/maps.json", "w"), separators=(',', ':'), ensure_ascii=False)
    idx = [{k: d[k] for k in ('id', 'title', 'bwv', 'book', 'key', 'meter', 'nv', 'blurb', 'card', 'bpm')}
           for d in docs]
    for d, i in zip(docs, idx):
        i['bars'] = sum(1 for b in d['bars'] if b['n'] > 0); i['entries'] = len(d['entries'])
    if only and os.path.exists(f"{DATA}/index.json"):
        prev = {p['id']: p for p in json.load(open(f"{DATA}/index.json", encoding="utf-8"))}
        prev.update({p['id']: p for p in idx})
        order = [P['id'] for P in PIECES]
        idx = [prev[i] for i in order if i in prev]
    json.dump(idx, open(f"{DATA}/index.json", "w"), indent=1, ensure_ascii=False)
