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
    for i in range(xi, p + 1):
        ln = out[i]
        if ln.startswith('!!'): continue
        f = _fields(ln)
        if i == xi:               fill = '**kern'
        elif ln.startswith('!'):  fill = '!'
        elif ln.startswith('*'):  fill = '*'
        elif ln.startswith('='):  fill = f[0]     # same barline token as its neighbours
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


def normalise(src, dst):
    """Returns dst if anything changed, else src."""
    lines = open(src, encoding='utf-8', errors='replace').read().split('\n')
    lines, n1 = drop_empty_fields(lines)
    lines, n2 = expand_spine_add(lines)
    if not (n1 or n2): return src, ''
    open(dst, 'w', encoding='utf-8').write('\n'.join(lines))
    what = ', '.join(x for x in (f"{n1} lines with empty fields" if n1 else '',
                                 "expanded a *+ spine addition" if n2 else '') if x)
    return dst, what
