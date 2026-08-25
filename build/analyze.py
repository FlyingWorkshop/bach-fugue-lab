"""Fugue analysis. Motif matching in DIATONIC space (letter-name steps) so that
real answers, tonal answers and diatonic sequences are all recognised, with
chromatic deviation reported separately."""
from collections import Counter

def by_voice(notes):
    d = {}
    for n in notes: d.setdefault(n['v'], []).append(n)
    for v in d: d[v].sort(key=lambda n: (n['q'], -n['p']))
    return d

def make_template(voices, v, q0, q1):
    seq = [n for n in voices[v] if q0 <= n['q'] < q1]
    t0 = seq[0]['q']
    return [{'dq': round(n['q'] - t0, 6), 'dia': n['dia'], 'p': n['p'], 'd': n['d']} for n in seq]

def _index(seq):
    ix = {}
    for n in seq: ix.setdefault(round(n['q'], 6), n)
    return ix

def score_at(ix, cq, tpl, sign=1, scale=1.0):
    pairs, miss = [], 0
    endq = cq
    for t in tpl:
        tq = round(cq + t['dq'] * scale, 6)
        n = ix.get(tq)
        if n is None:
            miss += 1; pairs.append(None); continue
        pairs.append((t, n))
        endq = max(endq, tq + n['d'])
    got = [pr for pr in pairs if pr]
    if not got: return None
    dofs = [pr[1]['dia'] - sign * pr[0]['dia'] for pr in got]
    cofs = [pr[1]['p']   - sign * pr[0]['p']   for pr in got]
    K = Counter(dofs).most_common(1)[0][0]
    C = Counter(cofs).most_common(1)[0][0]
    dhit = sum(1 for o in dofs if o == K)
    chit = sum(1 for o in cofs if o == C)
    N = len(tpl)
    devs = []
    for pr in pairs:
        devs.append(None if pr is None else (pr[1]['dia'] - sign * pr[0]['dia'] - K))
    # leading run of diatonically-correct notes
    prefix = 0
    for d in devs:
        if d == 0: prefix += 1
        else: break
    return {'q': cq, 'endq': endq, 'miss': miss, 'dhit': dhit, 'chit': chit,
            'N': N, 'K': K, 'C': C, 'devs': devs, 'prefix': prefix,
            'dscore': dhit / N, 'cscore': chit / N}

def classify(r):
    N = r['N']
    if r['miss'] == 0 and r['dhit'] == N:
        return 'exact' if r['chit'] == N else 'tonal'
    if r['miss'] <= max(1, N * 0.12) and r['dhit'] >= N * 0.85:
        return 'altered'
    if r['prefix'] >= max(5, N * 0.5) and r['dhit'] >= N * 0.55:
        return 'partial'
    return None

def find_statements(voices, tpl, forms=(('P', 1, 1.0),)):
    out = []
    for v, seq in voices.items():
        ix = _index(seq)
        for n in seq:
            for label, sign, scale in forms:
                r = score_at(ix, round(n['q'], 6), tpl, sign, scale)
                if not r: continue
                k = classify(r)
                if k:
                    out.append({**r, 'v': v, 'form': label, 'scale': scale, 'kind': k,
                                'p0': n['p'], 'dia0': n['dia']})
    return out

RANK = {'exact': 0, 'tonal': 1, 'altered': 2, 'partial': 3}

def dedupe(cands):
    cands = sorted(cands, key=lambda c: (RANK[c['kind']], -c['dscore'], -c['prefix'], c['q']))
    kept = []
    for c in cands:
        if any(k['v'] == c['v'] and c['q'] < k['endq'] and k['q'] < c['endq'] for k in kept):
            continue
        kept.append(c)
    kept.sort(key=lambda c: (c['q'], c['v']))
    return kept
