"""Check the built data against things that ought to be true, and against the
specific claims the site's own prose makes. Run it after any rebuild:

    .venv/bin/python build/validate.py

Structural checks apply to every fugue. Claim checks exist because the editorial
text quotes numbers and superlatives: when an analysis changes, or a fugue is added,
a sentence somewhere else can quietly become false. That has happened three times."""
import json, os, sys, glob

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(PROJ, "data")

# Voices that genuinely do not sound until late, so the subject cannot have reached
# them during the exposition. Not detection failures — the music is like this.
LATE_VOICES = {
    "bwv865": "the soprano is silent until bar 80; the five-voice texture is only the ending",
    "bwv871": "the fourth voice does not sound until bar 19, and enters with the subject",
}

# Expositions the matcher cannot complete, with the reason. Recorded rather than
# waived silently: each is a real limit, and each was checked before being listed.
KNOWN_INCOMPLETE = {
    "bwv849": "the four-note soggetto is too short to match on safely; a span that reaches the "
              "middle voices also matches ordinary figuration, and it would put every bracket "
              "a bar after the entry it marks",
    "bwv864": "the alto answer is there at bar 2, but no span recovers it without turning half "
              "the statements into partial matches",
}

def load():
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "bwv*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        out[d["id"]] = d
    return out

def coll(d):
    b = d["book"]
    return "wtc1" if b.startswith("WTC I,") else "wtc2" if b.startswith("WTC II") else "aof"

def structural(D):
    fails = []
    for i, d in D.items():
        q = d["qbar"]; nv = d["nv"]
        ent = sorted(d["entries"], key=lambda e: e["q0"])
        if not ent:
            fails.append((i, "no entries at all")); continue
        if ent[0]["q0"] / q + 1 >= 2.0:
            fails.append((i, f"first entry is in bar {ent[0]['q0']/q+1:.2f}, not bar 1"))
        seen = []
        for e in ent:
            if e["v"] in seen: break
            seen.append(e["v"])
            if len(seen) == nv: break
        if len(seen) < nv and i not in LATE_VOICES and i not in KNOWN_INCOMPLETE:
            missing = [v for v in range(nv) if v not in seen]
            names = [d["voiceNames"][v] for v in missing]
            fails.append((i, f"exposition reaches {len(seen)} of {nv} voices; "
                             f"no entry in {', '.join(names)}"))
        for e in d["entries"]:
            if not (0 <= e["q0"] < e["q1"] <= d["total"] + 1e-6):
                fails.append((i, f"entry outside the piece: {e['q0']}..{e['q1']}"))
            if e["v"] >= nv:
                fails.append((i, f"entry on voice {e['v']} but the piece has {nv}"))
        if len(d["history"]) < 2: fails.append((i, "history has fewer than two paragraphs"))
        if len(d["performances"]) < 3: fails.append((i, "fewer than three recordings listed"))
        if len(d["card"]) > 155: fails.append((i, f"card is {len(d['card'])} characters"))
    return fails

def claims(D):
    """Each entry: the piece whose text makes the claim, a description, and a test."""
    V = list(D.values())
    b1 = [d for d in V if coll(d) == "wtc1"]
    b2 = [d for d in V if coll(d) == "wtc2"]
    wtc = b1 + b2
    aof = [d for d in V if coll(d) == "aof"]
    bars = lambda d: len([b for b in d["bars"] if b["n"] > 0])
    subj_bars = lambda d: (d["subject"]["q1"] - d["subject"]["q0"]) / d["qbar"]
    longest_ep = lambda d: max([(b - a) / d["qbar"] for a, b in d["episodes"]], default=0)
    forms = lambda d, f: sum(1 for e in d["entries"] if e["form"] == f)
    kinds = lambda d, k: sum(1 for e in d["entries"] if e["kind"] == k)
    cs = lambda d: len(d["counters"])
    def keys(d):                      # consecutive runs, which is what the ribbon draws
        out = []
        for k in d["keys"]:
            if not out or out[-1] != k["k"]: out.append(k["k"])
        return len(out)
    mn = lambda pool, key: min(pool, key=key)["id"]
    mx = lambda pool, key: max(pool, key=key)["id"]
    only = lambda pool, pred: sorted(d["id"] for d in pool if pred(d))

    return [
      ("bwv846", "shortest longest-episode of all",      mx is not None and mn(V, longest_ep) == "bwv846"),
      ("bwv850", "shortest subject in bars of all",      mn(V, subj_bars) == "bwv850"),
      ("bwv852", "most episodes per bar in Book I",      mx(b1, lambda d: len(d["episodes"]) / bars(d)) == "bwv852"),
      ("bwv854", "earliest exposition end of all",       mn(V, lambda d: d["expoEnd"] / d["qbar"]) == "bwv854"),
      ("bwv855", "only two-voice fugue in the WTC",      only(wtc, lambda d: d["nv"] == 2) == ["bwv855"]),
      ("bwv856", "fewest notes in Book I",               mn(b1, lambda d: len(d["notes"])) == "bwv856"),
      ("bwv859", "only fugue in 6/4",                    only(V, lambda d: d["meter"] == "6/4") == ["bwv859"]),
      ("bwv860", "most episodes in Book I",              mx(b1, lambda d: len(d["episodes"])) == "bwv860"),
      ("bwv864", "only fugue in 9/8 in the WTC",         only(wtc, lambda d: d["meter"] == "9/8") == ["bwv864"]),
      ("bwv865", "most notes in Book I",                 mx(b1, lambda d: len(d["notes"])) == "bwv865"),
      ("bwv865", "most inverted entries in Book I",      mx(b1, lambda d: forms(d, "I")) == "bwv865"),
      ("bwv867", "one of three five-voice WTC fugues",   only(wtc, lambda d: d["nv"] == 5) == ["bwv849", "bwv865", "bwv867"]),
      ("bwv871", "only Book II fugue with augmentation", only(b2, lambda d: forms(d, "Aug") > 0) == ["bwv871"]),
      ("bwv874", "most entries in Book II",              mx(b2, lambda d: len(d["entries"])) == "bwv874"),
      ("bwv875", "shortest fugue in Book II",            mn(b2, bars) == "bwv875"),
      ("bwv878", "fewest subject notes in Book II",      mn(b2, lambda d: d["subject"]["len"]) == "bwv878"),
      ("bwv879", "most subject notes in the WTC",        mx(wtc, lambda d: d["subject"]["len"]) == "bwv879"),
      ("bwv880", "only fugue in 6/16 in the WTC",        only(wtc, lambda d: d["meter"] == "6/16") == ["bwv880"]),
      ("bwv885", "only four-voice 3/4 fugue in the WTC", only(wtc, lambda d: d["meter"] == "3/4" and d["nv"] == 4) == ["bwv885"]),
      ("bwv887", "longest fugue in the WTC",             mx(wtc, bars) == "bwv887"),
      ("bwv888", "densest subject in Book II",           mx(b2, lambda d: d["subject"]["len"] / subj_bars(d)) == "bwv888"),
      ("bwv889", "four countersubjects, no stretto, 28 bars",
                                                        cs(D["bwv889"]) == 4 and not D["bwv889"]["stretto"] and bars(D["bwv889"]) == 28),
      ("bwv891", "most key regions in the WTC",          mx(wtc, keys) == "bwv891"),
      ("bwv892", "longest four-voice fugue in the WTC",  mx([d for d in wtc if d["nv"] == 4], bars) == "bwv892"),
      ("bwv1080-3", "more countersubject statements than the rest of the Art of Fugue combined",
                                                        cs(D["bwv1080-3"]) > sum(cs(d) for d in aof if d["id"] != "bwv1080-3")),
      ("bwv1080-4", "longest subject-free stretch of all", mx(V, longest_ep) == "bwv1080-4"),
      ("bwv1080-8", "most episodes of all",              mx(V, lambda d: len(d["episodes"])) == "bwv1080-8"),
      ("bwv1080-9", "most subject notes of all",         mx(V, lambda d: d["subject"]["len"]) == "bwv1080-9"),
    ]

def main():
    D = load()
    print(f"{len(D)} fugues\n")
    sf = structural(D)
    print("STRUCTURE")
    if sf:
        for i, m in sf: print(f"  FAIL  {i:11s} {m}")
    else:
        print("  every fugue opens with the subject in bar 1, reaches every voice that sounds")
        print("  in time to take it, and keeps its entries inside the piece")
    for i, why in LATE_VOICES.items():
        print(f"  note  {i:11s} exposition check waived: {why}")
    for i, why in KNOWN_INCOMPLETE.items():
        print(f"  known {i:11s} exposition incomplete: {why}")

    cf = [(i, d) for i, d, ok in ((i, d, ok) for i, d, ok in claims(D)) if not ok]
    print(f"\nCLAIMS THE PROSE MAKES ({len(claims(D))} checked)")
    if cf:
        for i, d in cf: print(f"  FAIL  {i:11s} {d}")
    else:
        print("  all still true")

    n = sum(len(d["entries"]) for d in D.values())
    ks = {k: sum(1 for d in D.values() for e in d["entries"] if e["kind"] == k)
          for k in ("exact", "tonal", "altered", "partial")}
    print(f"\nHOW THE {n} STATEMENTS CLASSIFY")
    for k, v in ks.items(): print(f"  {k:8s} {v:4d}  {v/n*100:4.1f}%")
    raise SystemExit(1 if (sf or cf) else 0)

main()
