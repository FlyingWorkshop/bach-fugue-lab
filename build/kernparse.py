"""Minimal but exact **kern parser: absolute pitch, onsets in quarter notes, ties.
Emits records keyed by the verovio element id  note-L{line}F{field}[...]"""
import re

STEP = {'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}

def kern_pitch(tok):
    m = re.search(r'([a-gA-G]+)', tok)
    if not m: return None
    ltr = m.group(1)
    ch = ltr[0]
    n = len(ltr)
    if ch.islower():
        midi = 60 + STEP[ch] + 12 * (n - 1)
    else:
        midi = 48 + STEP[ch.lower()] - 12 * (n - 1)
    midi += tok.count('#') - tok.count('-')
    return midi

def kern_spell(tok):
    m = re.search(r'([a-gA-G]+)', tok)
    if not m: return None
    ltr = m.group(1); ch = ltr[0]; n = len(ltr)
    octv = (4 + (n - 1)) if ch.islower() else (3 - (n - 1))
    alter = tok.count('#') - tok.count('-')
    acc = ('#' * alter) if alter > 0 else ('b' * -alter)
    dia = octv * 7 + 'CDEFGAB'.index(ch.upper())
    return ch.upper() + acc + str(octv), dia

def kern_dur(tok):
    m = re.match(r'(\d+)(\.*)', tok.lstrip('[]_ '))
    m = re.search(r'(\d+)(\.*)', tok)
    if not m: return None
    r = int(m.group(1)); dots = len(m.group(2))
    q = 8.0 if r == 0 else 4.0 / r
    return q * (2 - 0.5 ** dots)

def parse(path):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    spines = []        # list of dicts: {origin: int, q: float}
    events = []        # note/rest records
    measures = []      # (line_no, qstamp)
    exclusive_done = False
    open_ties = {}     # (spine idx) -> event record
    for ln, raw in enumerate(lines, start=1):
        if not raw.strip() or raw.startswith('!'):
            continue
        fields = raw.split('\t')
        if raw.startswith('**'):
            spines = [{'origin': i, 'q': 0.0, 'skip': False} for i, f in enumerate(fields)]
            continue
        if raw.startswith('*'):
            # interpretation line: handle splits/merges
            new = []
            i = 0
            for f_i, f in enumerate(fields):
                if f_i >= len(spines):
                    break
            out = []
            si = 0
            f_i = 0
            while f_i < len(fields):
                f = fields[f_i]
                if si >= len(spines):
                    break
                if f == '*S/ossia':
                    spines[si]['skip'] = True; out.append(dict(spines[si])); si += 1
                elif f == '*S/sic':
                    spines[si]['skip'] = False; out.append(dict(spines[si])); si += 1
                elif f == '*Xstrophe':
                    spines[si]['skip'] = False; out.append(dict(spines[si])); si += 1
                elif f == '*^':
                    out.append(dict(spines[si])); out.append(dict(spines[si])); si += 1
                elif f == '*v':
                    # consume consecutive *v
                    j = f_i
                    merged = dict(spines[si])
                    while j < len(fields) and fields[j] == '*v':
                        merged['q'] = max(merged['q'], spines[si]['q']); si += 1; j += 1
                    out.append(merged)
                    f_i = j - 1
                elif f == '*-':
                    si += 1
                else:
                    out.append(dict(spines[si])); si += 1
                f_i += 1
            spines = out
            continue
        if fields[0].startswith('='):
            qs = [s['q'] for s in spines]
            mnum = re.match(r'=+(\d+)', fields[0])
            measures.append({'line': ln, 'q': max(qs) if qs else 0,
                             'n': int(mnum.group(1)) if mnum else None})
            continue
        # data line
        for f_i, tok in enumerate(fields):
            if f_i >= len(spines): break
            sp = spines[f_i]
            if tok == '.' or tok == '' or sp.get('skip'):
                continue
            subtoks = tok.split(' ')
            dur = kern_dur(subtoks[0])
            if dur is None:
                continue
            grace = 'q' in subtoks[0] or 'Q' in subtoks[0]
            for k, st in enumerate(subtoks):
                eid = f'note-L{ln}F{f_i+1}'
                if len(subtoks) > 1:
                    eid = f'note-L{ln}F{f_i+1}S{k+1}'
                if 'r' in st and not re.search(r'[a-gA-G]', st):
                    events.append({'id': f'rest-L{ln}F{f_i+1}', 'kind': 'rest',
                                   'q': sp['q'], 'd': dur, 'spine': sp['origin'], 'line': ln})
                    continue
                p = kern_pitch(st)
                if p is None: continue
                rec = {'id': eid, 'kind': 'note', 'q': sp['q'], 'd': 0.0 if grace else dur,
                       'p': p, 'n': kern_spell(st)[0], 'dia': kern_spell(st)[1], 'spine': sp['origin'], 'line': ln,
                       'tie_start': '[' in st, 'tie_mid': '_' in st, 'tie_end': ']' in st,
                       'trill': ('t' in st.replace('tie','')) or ('T' in st),
                       'fermata': ';' in st}
                events.append(rec)
            if not grace:
                sp['q'] += dur
    total = max([s['q'] for s in spines] + [m['q'] for m in measures] + [0])
    return events, measures, total

def merge_ties(events):
    """Fold tied groups into single sounding notes; keep member ids."""
    out = []
    pending = {}   # (spine,pitch) -> record
    for e in sorted([e for e in events if e['kind'] == 'note'], key=lambda x: (x['q'], x['spine'])):
        key = (e['spine'], e['p'])
        if e['tie_mid'] or e['tie_end']:
            if key in pending:
                r = pending[key]
                r['d'] = e['q'] + e['d'] - r['q']
                r['ids'].append(e['id'])
                if e['tie_end']:
                    del pending[key]
                continue
        r = dict(e); r['ids'] = [e['id']]
        out.append(r)
        if e['tie_start']:
            pending[key] = r
    return out
