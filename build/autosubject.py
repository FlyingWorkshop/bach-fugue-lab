"""Find the fugue subject automatically: it starts with the first voice to sing
and is as long as it can be while still accounting for (nearly) every entry."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernparse import parse, merge_ties
from analyze import by_voice, make_template, find_statements, dedupe

def load(path, nv=None):
    ev, marks, total = parse(path)
    notes = merge_ties(ev)
    if nv is None: nv = max(n['spine'] for n in notes) + 1
    for n in notes: n['v'] = nv - 1 - n['spine']
    bars = [m for m in marks if m['n'] is not None]
    qbar = (bars[1]['q'] - bars[0]['q']) if len(bars) > 1 else 4.0
    return notes, bars, total, qbar, nv

def prefix_len(ix, cq, tpl, sign=1):
    """Longest leading run of the template that this entry point reproduces,
    tolerating up to two mutated notes (a tonal answer changes its head)."""
    from collections import Counter
    best = 0
    for L in range(len(tpl), 4, -1):
        offs, miss = [], 0
        for t in tpl[:L]:
            n = ix.get(round(cq + t['dq'], 6))
            if n is None: miss += 1; break
            offs.append(n['dia'] - sign * t['dia'])
        if miss or not offs: continue
        K = Counter(offs).most_common(1)[0][0]
        hits = sum(1 for o in offs if o == K)
        if hits >= L - 2:
            best = L; break
    return best

def find_subject(notes, verbose=False):
    V = by_voice(notes)
    firsts = sorted(((min(n['q'] for n in seq), v) for v, seq in V.items() if seq))
    q0, sv = firsts[0]
    ans = firsts[1][0] if len(firsts) > 1 else q0 + 8
    # provisional template: everything the first voice sings before the answer starts
    prov = make_template(V, sv, q0, ans + 1e-9)
    # each other voice states the subject once in the exposition: the subject is
    # what those statements still have in common with the first one.
    prefs = []
    for q_in, v in firsts[1:]:
        ix = {}
        for n in V[v]: ix.setdefault(round(n['q'], 6), n)
        L = prefix_len(ix, round(q_in, 6), prov)
        if L: prefs.append(L)
        if verbose: print(f"   voice {v} enters q={q_in} -> shares {L}/{len(prov)} notes")
    if not prefs: return None
    prefs.sort()
    L = prefs[0] if prefs[0] >= 0.6 * prefs[-1] else prefs[len(prefs) // 2]
    # shorten while the later entries do not state the whole thing
    while L > 8:
        q1 = q0 + prov[L - 1]['dq'] + 1e-6
        tpl = make_template(V, sv, q0, q1)
        sts = dedupe(find_statements(V, tpl))
        if not sts: L -= 1; continue
        part = sum(1 for s in sts if s['kind'] == 'partial') / len(sts)
        acc = sum(s['dhit'] / s['N'] for s in sts) / len(sts)
        if verbose: print(f"   L={L:3d} statements={len(sts):3d} partial={part:.2f} acc={acc:.3f}")
        if part > 0.20 or acc < 0.955: L -= 1
        else: break
    q1 = q0 + prov[L - 1]['dq'] + 1e-6
    tpl = make_template(V, sv, q0, q1)
    sts = dedupe(find_statements(V, tpl))
    good = [s for s in sts if s['kind'] in ('exact', 'tonal')]
    return dict(v=sv, q0=q0, q1=q1, n=len(tpl), full=len(good), all=len(sts),
                answerAt=ans, prefs=prefs, provN=len(prov))

if __name__ == '__main__':
    path = sys.argv[1]
    notes, bars, total, qbar, nv = load(path)
    r = find_subject(notes, verbose='-v' in sys.argv)
    V = by_voice(notes)
    tpl = make_template(V, r['v'], r['q0'], r['q1'])
    sts = dedupe(find_statements(V, tpl, forms=(('P',1,1.0),('I',-1,1.0),('Aug',1,2.0))))
    print(f"{os.path.basename(path)}: voices={nv} bars={len(bars)} qbar={qbar} total={total}")
    print(f"  subject voice {r['v']} q {r['q0']}..{round(r['q1'],3)} ({r['n']} notes, "
          f"{round((r['q1']-r['q0'])/qbar,2)} bars); answer enters {r['answerAt']}")
    from collections import Counter
    print("  kinds:", Counter(s['kind'] for s in sts), "forms:", Counter(s['form'] for s in sts))
    for s in sts:
        b = next((bb['n'] for bb in reversed(bars) if s['q'] >= bb['q'] - 1e-9), 0)
        print(f"    v{s['v']} bar{b:3d} q={s['q']:7.2f} {s['kind']:8s} {s['form']:3s} K={s['K']:+3d} C={s['C']:+4d} dhit={s['dhit']}/{s['N']}")
