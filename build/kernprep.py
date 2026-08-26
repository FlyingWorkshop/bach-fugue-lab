"""Normalise a few odd Humdrum constructs that Verovio 6.3 will not import.

Both transformations preserve line numbers, so the note ids (note-L{line}F{field})
that join kern data to engraved geometry stay consistent as long as the parser and
the engraver are both given the normalised file."""
import re


def _fields(ln):
    return ln.split('\t')


def drop_empty_fields(lines):
    """A Humdrum field is never the empty string; wtc1f24 carries a phantom column
    that is empty until a spine split fills it, which offsets every field number."""
    out, hit = [], 0
    for ln in lines:
        if ln.startswith('!!') or '\t' not in ln:
            out.append(ln); continue
        f = _fields(ln)
        if '' in f:
            hit += 1
            f = [x for x in f if x != '']
        out.append('\t'.join(f))
    return out, hit


def bar_rest(quarters):
    """A kern duration token covering one whole bar, as an invisible rest.
    A spine padded with null tokens never advances its own clock — kern time comes
    from durations — so a spine declared early has to be filled with real rests."""
    for recip in (0, 1, 2, 4, 8, 16, 32):
        base = 8.0 if recip == 0 else 4.0 / recip
        for dots in (0, 1, 2):
            if abs(base * (2 - 0.5 ** dots) - quarters) < 1e-9:
                return f"{recip}{'.' * dots}ryy"          # yy = invisible
    raise ValueError(f'no single kern duration covers a {quarters}-quarter bar')


def _bar_quarters(lines):
    for ln in lines:
        t = ln.split('\t')[0]
        m = re.match(r'\*M(\d+)/(\d+)$', t)
        if m: return int(m.group(1)) * 4.0 / int(m.group(2))
    return 4.0


def expand_spine_add(lines):
    """`*+` adds a spine mid-piece (wtc1f20 gains a fifth voice for the last eight
    bars). Verovio imports such a file as an empty score, so declare the spine from
    the start instead and leave it silent until it enters."""
    p = fi = None
    for i, ln in enumerate(lines):
        if ln.startswith('!!') or '\t' not in ln: continue
        f = _fields(ln)
        if '*+' in f:
            p, fi = i, f.index('*+'); break
    if p is None: return lines, 0
    xi = next(i for i, ln in enumerate(lines) if ln.startswith('**'))
    at = fi + 1                                   # the new spine sits after spine fi
    # if it is added after the last spine it can simply be appended, which keeps any
    # temporary *^ split earlier in the file at its own field numbers
    append = fi == len(_fields(lines[p])) - 1
    out = list(lines)
    rest = bar_rest(_bar_quarters(lines))
    owed = False                      # this bar still needs its rest written
    for i in range(xi, p + 1):
        ln = out[i]
        if ln.startswith('!!'): continue
        f = _fields(ln)
        if i == xi:               fill = '**kern'
        elif ln.startswith('!'):  fill = '!'
        elif ln.startswith('*'):  fill = '*'
        elif ln.startswith('='):  fill = f[0]; owed = True   # same barline token as its neighbours
        elif owed:                fill = rest; owed = False
        else:                     fill = '.'
        f.insert(len(f) if append else min(at, len(f)), fill)
        out[i] = '\t'.join(f)
    f = _fields(out[p]); f[fi] = '*'; out[p] = '\t'.join(f)
    # the spine declared its own **kern on the next line; it is already declared now
    for i in range(p + 1, min(p + 4, len(out))):
        f = _fields(out[i])
        if f and f[-1].startswith('**') and append:
            f[-1] = '*'; out[i] = '\t'.join(f); break
        if len(f) > at and f[at].startswith('**'):
            f[at] = '*'; out[i] = '\t'.join(f); break
    return out, 1


DATA_TOKEN = re.compile(r'^(=|\.|\d|\[|[a-gA-Gr])')


def restore_commented_music(lines):
    """wtc1f20 (BWV 865) ends with eight bars in five voices, and the encoder left the
    whole passage commented out. The file's headers say the texture goes to five voices
    in the final eight measures, and that the voicing in the *final measure* is
    "somewhat arbitrary". Without the passage the fugue stops at bar 79, mid-phrase, so
    the music is restored and the piece's own notes say so. Only local comments (!!)
    that parse as kern data are touched; reference records (!!!) and prose are left
    alone, and no other file in the repertoire contains commented-out music."""
    out, n = [], 0
    for ln in lines:
        if ln.startswith('!!') and not ln.startswith('!!!'):
            body = ln[2:]
            if '\t' in body and DATA_TOKEN.match(body.split('\t')[0]):
                out.append(body); n += 1; continue
        out.append(ln)
    return out, n


def normalise(src, dst):
    """Returns dst if anything changed, else src."""
    lines = open(src, encoding='utf-8', errors='replace').read().split('\n')
    lines, n0 = restore_commented_music(lines)
    lines, n1 = drop_empty_fields(lines)
    lines, n2 = expand_spine_add(lines)
    if not (n0 or n1 or n2): return src, ''
    open(dst, 'w', encoding='utf-8').write('\n'.join(lines))
    what = ', '.join(x for x in (f"restored {n0} commented-out lines of music" if n0 else '',
                                 f"{n1} lines with empty fields" if n1 else '',
                                 "expanded a *+ spine addition" if n2 else '') if x)
    return dst, what
