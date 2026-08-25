"""Pack the site into one self-contained HTML file (and a body-only variant)."""
import os, re, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DIST = os.path.join(PROJ, "dist")

def read(p): return open(os.path.join(PROJ, p), encoding="utf-8").read()

def assemble(only=None):
    html = read("lab.html")
    css  = read("app.css")
    js   = read("app.js")

    idx = json.load(open(os.path.join(PROJ, "data", "index.json"), encoding="utf-8"))
    if only:
        idx = [p for p in idx if p["id"] in only]
        missing = only - {p["id"] for p in idx}
        if missing: raise SystemExit(f"no such piece: {', '.join(sorted(missing))}")
    blobs = ['<script type="application/json" id="bx-index">%s</script>'
             % json.dumps(idx, ensure_ascii=False)]
    for p in idx:
        i = p["id"]
        blobs.append('<script type="application/json" id="bx-%s">%s</script>'
                     % (i, read(f"data/{i}.json")))
        blobs.append('<script type="text/x-svg" id="bs-%s">%s</script>' % (i, read(f"data/{i}.svg")))
        blobs.append('<script type="text/x-svg" id="bp-%s">%s</script>' % (i, read(f"data/{i}.p.svg")))
    loader = """<script>
window.__BUNDLE__ = {
  index: JSON.parse(document.getElementById('bx-index').textContent),
  pieces: new Proxy({}, { get: (_, id) => ({
    json:  document.getElementById('bx-' + id).textContent,
    svg:   document.getElementById('bs-' + id).textContent,
    svgP:  document.getElementById('bp-' + id).textContent,
  })}),
};
</script>"""
    for tag in re.findall(r'</?script[^>]*>', "".join(blobs)):
        pass
    body = html
    # lambda replacements: the payload is code, not a substitution template, so a
    # backslash escape in it (\u2026) must not be read as a group reference
    body = re.sub(r'<link rel="stylesheet" href="app\.css[^"]*">',
                  lambda m: '<style>\n%s\n</style>' % css, body)
    payload = "\n".join(blobs) + "\n" + loader + "\n<script>\n" + js + "\n</script>"
    body = re.sub(r'<script src="app\.js[^"]*"></script>', lambda m: payload, body)
    return body

def lint():
    """Cheap guard against markdown leaking into the HTML as literal text."""
    bad = []
    for f in ("index.html", "lab.html"):
        for i, line in enumerate(read(f).split("\n"), 1):
            if "`" in line: bad.append(f"{f}:{i}: stray backtick — {line.strip()[:70]}")
    if bad:
        print("LINT:"); [print("  " + b) for b in bad]
        raise SystemExit(1)

def main():
    lint()
    os.makedirs(DIST, exist_ok=True)
    only = set(sys.argv[1:]) or None
    if not only:
        print("packing all 57 fugues — the result is around 70 MB.\n"
              "Pass ids for a smaller one, e.g. build/bundle.py bwv846 bwv847 bwv855")
    full = assemble(only)
    open(os.path.join(DIST, "fugue-lab.html"), "w", encoding="utf-8").write(full)

    # body-only variant: no doctype/html/head/body wrapper (the Artifact host adds one)
    inner = full
    inner = re.sub(r'^.*?<title>', '<title>', inner, flags=re.S)
    inner = inner.replace('</head>', '').replace('<body>', '')
    inner = re.sub(r'</body>\s*</html>\s*$', '', inner)
    open(os.path.join(DIST, "artifact.html"), "w", encoding="utf-8").write(inner)
    for f in ("fugue-lab.html", "artifact.html"):
        print(f, os.path.getsize(os.path.join(DIST, f)) // 1024, "kB")

main()
