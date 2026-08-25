"""Dump the computed facts for each built fugue: what the analysis actually found.
Anything written about a piece on the site should be checkable against this."""
import json, os, sys, glob

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(PROJ, "data")

def facts(d):
    qbar = d['qbar']
    bar = lambda q: round(q / qbar + 1, 2)
    ent = d['entries']
    keys = d.get('keys') or []
    kp, kspan = [], []
    for k in keys:
        name = k.get('k') if isinstance(k, dict) else k
        if not kp or kp[-1] != name:
            kp.append(name)
            if isinstance(k, dict): kspan.append([name, bar(k['q0']), bar(k['q1'])])
    return dict(
        id=d['id'], title=d['title'], bwv=d['bwv'], book=d['book'], key=d['key'],
        meter=d['meter'], bpm=d['bpm'], nv=d['nv'],
        bars=sum(1 for b in d['bars'] if b['n'] > 0),
        notes=len(d['notes']),
        subjectVoice=d['subject']['v'],
        subjectBars=round((d['subject']['q1'] - d['subject']['q0']) / qbar, 2),
        subjectNotes=d['subject']['len'],
        entries=len(ent),
        entryBars=[bar(e['q0']) for e in ent],
        entryKinds={k: sum(1 for e in ent if e['kind'] == k)
                    for k in ('exact', 'tonal', 'altered', 'partial')},
        entryForms={f: sum(1 for e in ent if e['form'] == f) for f in {e['form'] for e in ent}},
        entryKeys=[e['on'] for e in ent],
        roles={r: sum(1 for e in ent if e['role'] == r) for r in {e['role'] for e in ent}},
        expositionEndsBar=bar(d['expoEnd']),
        expositionOrder=[e['v'] for e in ent if e['q0'] < d['expoEnd']],
        countersubjects=len(d['counters']),
        strettoPairs=len(d['stretto']),
        strettoBars=[bar(ent[i]['q0']) for i, _ in d['stretto']][:12],
        episodes=len(d['episodes']),
        episodeBars=[[bar(a), bar(b)] for a, b in d['episodes']],
        longestEpisodeBars=round(max(((b - a) / qbar for a, b in d['episodes']), default=0), 2),
        pedals=[{'fromBar': bar(p['q0']), 'bars': round((p['q1'] - p['q0']) / qbar, 2)} for p in d['pedals']],
        keyPath=kp,
        keyRegions=kspan,
        lastBarKey=(kp[-1] if kp else None),
    )

if __name__ == "__main__":
    want = sys.argv[1:]
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        b = os.path.basename(p)
        if b in ("index.json", "teasers.json", "maps.json", "hero.json"): continue
        d = json.load(open(p, encoding="utf-8"))
        if want and d['id'] not in want: continue
        out[d['id']] = facts(d)
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
