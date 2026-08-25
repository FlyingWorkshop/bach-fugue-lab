import sys, json; sys.path.insert(0,'build')
from kernparse import parse, merge_ties
from analyze import *
NAM=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
def pn(p): return f"{NAM[p%12]}{p//12-1}"
f, nv, sq0, sq1, sv = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
qpm = float(sys.argv[6]) if len(sys.argv)>6 else 4.0
q_of_m1 = float(sys.argv[7]) if len(sys.argv)>7 else 0.0
ev, ms, tot = parse(f); notes = merge_ties(ev)
for n in notes: n['v'] = nv - 1 - n['spine']
V = by_voice(notes)
tpl = make_template(V, sv, sq0, sq1)
print("template", len(tpl), "notes, span", sq1-sq0)
kept = dedupe(find_statements(V, tpl, forms=(('P',1,1.0),('I',-1,1.0),('Aug',1,2.0))))
for c in kept:
    b = (c['q']-q_of_m1)/qpm + 1
    print(f"  v{c['v']} m{int(b)}+{(b%1)*qpm:.2f}  q={c['q']:7.2f}  {c['kind']:8s} {c['form']:3s} "
          f"start={pn(c['p0'])} K={c['K']:+d}dia C={c['C']:+d}st  dhit={c['dhit']}/{c['N']} chit={c['chit']} miss={c['miss']}")
print("total statements", len(kept))
