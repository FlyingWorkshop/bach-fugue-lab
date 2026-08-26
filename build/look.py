"""Inspect a kern fugue: dump a voice as bar:beat, or test a candidate subject span.

  python3 build/inspect.py voice  wtc1f05 0 --bars 1-6
  python3 build/inspect.py subject wtc1f05 --v 0 --from 1:1 --to 2:1
"""
import sys, os, re, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernparse import parse, merge_ties
from analyze import by_voice, make_template, find_statements, dedupe
from autosubject import find_subject
from kernprep import normalise

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    path = os.path.join(HERE, "kern-open", name if name.endswith(".krn") else name + ".krn")
    # the build normalises before parsing, so look at the same file it does
    path, _ = normalise(path, os.path.join(HERE, "kern-open", "_n_" + os.path.basename(path)))
    ev, marks, total = parse(path)
    notes = merge_ties(ev)
    nv = max(n['spine'] for n in notes) + 1
    for n in notes: n['v'] = nv - 1 - n['spine']
    marked = [m for m in marks if m['n'] is not None]
    bars = []
    if marked and marked[0]['q'] > 1e-9: bars.append({'n': 0, 'q0': 0.0, 'q1': marked[0]['q']})
    for i, m in enumerate(marked):
        bars.append({'n': m['n'], 'q0': m['q'], 'q1': marked[i+1]['q'] if i+1 < len(marked) else total})
    full = [b for b in bars if b['n'] > 0]
    qbar = (full[0]['q1'] - full[0]['q0']) if full else 4.0
    meter = '4/4'
    for ln in open(path, encoding='utf-8', errors='replace'):
        t = ln.split('\t')[0]
        if t.startswith('*M') and re.match(r'\*M\d+/\d+', t): meter = t[2:].strip(); break
    return notes, bars, total, qbar, nv, meter, path

def bb(q, bars, qbar, meter):
    """quarter position -> 'bar:beat' using the notated beat of the metre."""
    den = int(meter.split('/')[1]); qpb = 4.0 / den
    b = next((x for x in bars if x['q0'] - 1e-6 <= q < x['q1'] - 1e-6), bars[-1])
    return f"{b['n']}:{(q - b['q0'])/qpb + 1:g}"

def q_of(spec, bars, qbar, meter):
    """'bar:beat' -> quarter position."""
    if ':' not in spec: return float(spec)
    bn, beat = spec.split(':'); bn = int(bn); beat = float(beat)
    den = int(meter.split('/')[1]); qpb = 4.0 / den
    b = next((x for x in bars if x['n'] == bn), None)
    if b is None: raise SystemExit(f"no bar {bn}")
    return b['q0'] + (beat - 1) * qpb

NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def pn(p): return f"{NAMES[p%12]}{p//12-1}"

def cmd_voice(a):
    notes, bars, total, qbar, nv, meter, path = load(a.file)
    V = by_voice(notes)
    lo, hi = (a.bars.split('-') + [a.bars.split('-')[0]])[:2] if a.bars else (None, None)
    seq = sorted(V[a.v], key=lambda n: n['q'])
    print(f"# {os.path.basename(path)}  {nv} voices, meter {meter}, {len(bars)} bars, qbar={qbar}")
    print(f"# voice {a.v} (0 = top staff); {len(seq)} notes")
    for n in seq:
        b = next((x for x in bars if x['q0'] - 1e-6 <= n['q'] < x['q1'] - 1e-6), bars[-1])
        if lo and not (int(lo) <= b['n'] <= int(hi)): continue
        print(f"  q={n['q']:8.3f}  {bb(n['q'],bars,qbar,meter):>8s}  {pn(n['p']):>4s}  dur={n['d']:g}")

def cmd_subject(a):
    notes, bars, total, qbar, nv, meter, path = load(a.file)
    V = by_voice(notes)
    if a.auto:
        S = find_subject(notes)
        if not S: raise SystemExit("auto: no subject found")
        v, q0, q1 = S['v'], S['q0'], S['q1']
    else:
        v = a.v
        q0 = q_of(getattr(a, 'from'), bars, qbar, meter)
        q1 = q_of(a.to, bars, qbar, meter)
    if not [n for n in V.get(v, []) if q0 - 1e-6 <= n['q'] < q1 - 1e-6]:
        raise SystemExit(f"voice {v} has no notes in q {q0:g}..{q1:g}; "
                         f"voices sounding there: {sorted({n['v'] for n in notes if q0-1e-6 <= n['q'] < q1-1e-6})}")
    tpl = make_template(V, v, q0, q1)
    forms = [('P', 1, 1.0)]
    if a.inv: forms.append(('I', -1, 1.0))
    if a.aug: forms.append(('Aug', 1, 2.0))
    sts = dedupe(find_statements(V, tpl, forms=tuple(forms)))
    sts = [s for s in sts if s['form'] == 'P' or s['kind'] in ('exact','tonal','altered')]
    print(f"# {os.path.basename(path)}  {nv}v  meter {meter}  {len(bars)} bars  qbar={qbar}")
    print(f"# subject: voice {v}, q {q0:g}..{q1:g}  = bars {bb(q0,bars,qbar,meter)}..{bb(q1,bars,qbar,meter)}"
          f"  ({(q1-q0)/qbar:.2f} bars, {len(tpl)} notes)")
    print(f"# {len(sts)} statements, voices used: {sorted({s['v'] for s in sts})}, "
          f"kinds: {({k: sum(1 for s in sts if s['kind']==k) for k in ('exact','tonal','altered','partial')})}")
    for s in sts:
        print(f"  bar {bb(s['q'],bars,qbar,meter):>8s}  v{s['v']}  {s['form']}  {s['kind']:8s} "
              f"start {pn(s['p0'])}  miss={s['miss']} dhit={s['dhit']}/{s['N']}")

p = argparse.ArgumentParser()
sub = p.add_subparsers(dest='cmd', required=True)
pv = sub.add_parser('voice'); pv.add_argument('file'); pv.add_argument('v', type=int)
pv.add_argument('--bars'); pv.set_defaults(fn=cmd_voice)
ps = sub.add_parser('subject'); ps.add_argument('file'); ps.add_argument('--v', type=int, default=0)
ps.add_argument('--from', default='1:1'); ps.add_argument('--to', default='2:1')
ps.add_argument('--auto', action='store_true'); ps.add_argument('--inv', action='store_true')
ps.add_argument('--aug', action='store_true'); ps.set_defaults(fn=cmd_subject)
a = p.parse_args(); a.fn(a)
