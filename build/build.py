"""Build pipeline: kern -> engraved SVG + note/geometry/analysis JSON."""
import verovio, json, re, os, sys, math
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.dirname(ROOT), "data")

OPTS = {
    "breaks": "none", "adjustPageHeight": True, "adjustPageWidth": True,
    "scale": 40,
    "pageMarginLeft": 20, "pageMarginRight": 20,
    "pageMarginTop": 20, "pageMarginBottom": 20,
    "footer": "none", "header": "none",
    "svgViewBox": True, "svgHtml5": False, "svgRemoveXlink": True,
    "spacingLinear": 0.32, "spacingNonLinear": 0.58,
    "spacingStaff": 2, "systemDivider": "none",
    "lyricSize": 4.5,
}

# ---------------------------------------------------------------- svg parsing
def parse_geometry(svg):
    root = ET.fromstring(svg)
    outer = [float(v) for v in root.get("viewBox").split()]
    inner_el = None
    for ch in root:
        if ch.get("class") == "definition-scale":
            inner_el = ch; break
    inner = [float(v) for v in inner_el.get("viewBox").split()]
    k = outer[2] / inner[2]                      # inner units -> outer units
    pm = inner_el.find(f"{NS}g")
    tx, ty = 0.0, 0.0
    for ch in inner_el:
        if ch.get("class") == "page-margin":
            m = re.search(r"translate\(([-\d.]+),\s*([-\d.]+)\)", ch.get("transform") or "")
            if m: tx, ty = float(m.group(1)), float(m.group(2))
            pm = ch
            break
    def X(x): return (x + tx) * k
    def Y(y): return (y + ty) * k

    notes, measures, staff_boxes = {}, [], {}
    # measure -> ordered staff elements (top to bottom == voice order)
    voice_of_staffid = {}
    for mel in pm.iter():
        if mel.get("class") != "measure": continue
        mid = mel.get("id")
        staff_els = [c for c in mel if c.get("class") == "staff"]
        for vi, sel in enumerate(staff_els):
            voice_of_staffid[sel.get("id")] = vi
            ys = []
            for p in sel.findall(f"{NS}path"):
                mm = re.match(r"M([-\d.]+)\s+([-\d.]+)", p.get("d") or "")
                if mm: ys.append(float(mm.group(2)))
            if ys:
                staff_boxes.setdefault(vi, (Y(min(ys)), Y(max(ys))))
        xs = []
        for p in mel.iter(f"{NS}path"):
            mm = re.match(r"M([-\d.]+)", p.get("d") or "")
            if mm: xs.append(float(mm.group(1)))
        for u in mel.iter(f"{NS}use"):
            mm = re.search(r"translate\(([-\d.]+)", u.get("transform") or "")
            if mm: xs.append(float(mm.group(1)))
        measures.append({"id": mid, "x0": X(min(xs)) if xs else 0, "x1": X(max(xs)) if xs else 0})
        # notes inside, with voice from enclosing staff
        for sel in staff_els:
            vi = voice_of_staffid[sel.get("id")]
            for nel in sel.iter():
                if nel.get("class") != "note" or not nel.get("id"): continue
                u = nel.find(f".//{NS}use")
                if u is None: continue
                mm = re.search(r"translate\(([-\d.]+),\s*([-\d.]+)\)", u.get("transform") or "")
                if not mm: continue
                notes[nel.get("id")] = {"x": X(float(mm.group(1))), "y": Y(float(mm.group(2))), "v": vi}
            for rel in sel.iter():
                pass
    return outer, notes, measures, staff_boxes, k

# ---------------------------------------------------------------- kern header
def kern_meta(path):
    meta = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.startswith("!!!"): 
            if line.startswith("*") or line.startswith("="): continue
            continue
        m = re.match(r"!!!([A-Za-z@]+):\s*(.*)", line.strip())
        if m: meta.setdefault(m.group(1), m.group(2))
    return meta

# ---------------------------------------------------------------- extraction
def extract(krn, extra=None):
    tk = verovio.toolkit()
    o = dict(OPTS)
    if extra: o.update(extra)
    tk.setOptions(o)
    assert tk.loadFile(krn), krn
    svg = tk.renderToSVG(1)
    tmap = tk.renderToTimemap({"includeRests": True})
    outer, npos, measures, staff_boxes, k = parse_geometry(svg)

    onq, offq = {}, {}
    for ev in tmap:
        q = ev["qstamp"]
        for i in ev.get("on", []):  onq[i] = q
        for i in ev.get("off", []): offq[i] = q

    notes = []
    for nid, g in npos.items():
        mv = tk.getMIDIValuesForElement(nid)
        if not mv or "pitch" not in mv: continue
        q0 = onq.get(nid)
        tied_from = q0 is None
        if tied_from:
            continue                       # tie continuation: no separate attack
        q1 = offq.get(nid, q0 + 1)
        notes.append({"id": nid, "v": g["v"], "x": round(g["x"], 2), "y": round(g["y"], 2),
                      "p": mv["pitch"], "q": round(q0, 6), "d": round(q1 - q0, 6)})
    notes.sort(key=lambda n: (n["q"], -n["p"]))

    # tie continuations -> map to primary so highlighting covers them
    ties = {}
    for nid, g in npos.items():
        if nid not in onq:
            ties[nid] = g["v"]
    return tk, svg, notes, measures, outer, staff_boxes, ties, tmap

if __name__ == "__main__":
    krn = sys.argv[1]
    tk, svg, notes, measures, outer, sb, ties, tmap = extract(krn)
    print("notes", len(notes), "ties", len(ties), "measures", len(measures))
    print("viewBox", outer, "staffboxes", sb)
    print(json.dumps(notes[:6], indent=0))
    print(json.dumps(measures[:4], indent=0))
    print(kern_meta(krn))
