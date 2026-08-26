# Fugue Lab

A viewer for Bach fugues: one staff per voice, a piano roll drawn on the same horizontal axis as
the score, a map of the whole piece, and audio. Every statement of the subject is found by the
build, not typed in by hand.

**→ [Open the site](https://flyingworkshop.github.io/bach-fugue-lab/)**  ·  [jump straight into the lab](https://flyingworkshop.github.io/bach-fugue-lab/lab.html)

Fifty-eight fugues: all forty-eight of the Well-Tempered Clavier, and ten from *The Art of
Fugue*. Two to five voices, 27 to 239 bars.

| Collection | Fugues | Voices |
|---|---|---|
| Well-Tempered Clavier, Book I | 24 of 24 | 2–5 |
| Well-Tempered Clavier, Book II | 24 of 24 | 3–4 |
| *The Art of Fugue* | Contrapunctus I–V, VIII–XI, XIV | 3–4 |

One caveat on completeness. **BWV 865** (A minor, Book I No. 20) has its last eight bars — the
five-voice ending — commented out in the kern encoding, so the fugue would stop at bar 79,
mid-phrase. The build restores them, and that piece's own notes say so; the encoder's header records
that the voicing in the final measure is "somewhat arbitrary". No other file in the repertoire
contains commented-out music. The canons of *The Art of Fugue* are not fugues and are not here.

## What it shows

**Open score.** One staff per voice, so a fugal line never jumps between staves the way it does
in a two-stave keyboard reduction. Each voice keeps its colour in the notation, the roll and the
map.

**A shared x-axis.** The piano roll below the score is drawn at the exact horizontal positions of
the engraving, so a note in the roll sits under its own notehead. Two spacings:

* *Time-proportional* — horizontal distance is strictly proportional to duration; a half note is
  twice the width of a quarter.
* *Notation* — conventional engraver's spacing, which fits more bars on screen.

**Subject entries, found not typed.** The build slides the opening statement over every note of
every voice and compares in **diatonic space** — letter-name steps rather than semitones. So a
*tonal answer* (whose head is mutated) or a modally adjusted entry still matches, and gets labelled
`exact` / `tonal` / `adjusted` / `partial`. The countersubject goes through the same pass, and so
do inversion and augmentation where a piece uses them.

The one thing that is sometimes typed in is where the subject *ends*. The detector takes the
opening voice up to the answer's entry and shortens it until the later statements agree, which
works for 32 of the 58 and fails on the rest — usually by settling on a fragment of the head, which
then matches far too much. Those 26 spans are set by hand in `build/pieces.py`, and each piece's
notes panel says which kind it is. Every statement is still found by the matcher either way.

For five of them the accepted span is the subject's *head* rather than the whole subject, because
Bach re-values the tail on restatement and a full-length template then walks past entries that are
plainly there — in BWV 860 a four-bar template found 4 entries where the one-bar head finds 18. The
notes panel says when a bracket is head-only.

**A whole-piece map.** Every entry as a block on its voice's lane, episodes greyed, strettos
flagged, and the estimated key underneath.

**Per-voice audio.** Mute, solo and volume on each voice; *spotlight subject* raises whichever
voice is currently stating the theme and ducks the rest; loop any entry or episode; tempo control.
Synthesised in the browser with the Web Audio API — no samples, no network.

**No dynamics.** Bach wrote none, so there are none here; the Well-Tempered Clavier is harpsichord
and clavichord music. Playback is flat by default — every note the same weight. Two aids under
**Sound** will change that if you switch them on: a slight metrical accent, and a spotlight that
lifts whichever voice is stating the subject and ducks the rest. Both are for following the
counterpoint, not for performance. Low notes do get a little extra weight so the bass stays
audible; that is mixing, not interpretation, and it is always on.

**Subject lab.** Every statement drawn on top of a ghost of the original, optionally transposed to a
common pitch. The entries Bach bent are the interesting ones.

## Keys

`space` play/pause · `←`/`→` bar · `shift`+`←`/`→` previous/next entry · `1`…`5` solo a voice ·
`0` all voices · `L` loop the current section · `S` spotlight · `N` notes panel · `esc` close

## Building it yourself

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./build/fetch.sh          # downloads the kern encodings (not committed here)
.venv/bin/python build/make.py
python3 -m http.server 8777      # then open http://localhost:8777
```

The pipeline is:

| file | job |
|---|---|
| `build/kernparse.py` | exact Humdrum `**kern` reader — absolute pitch, onsets, ties, spine splits, editorial *ossia* branches |
| `build/analyze.py` | motif matching in diatonic space, with transposition/inversion/augmentation |
| `build/autosubject.py` | works out how long the subject is: what every expository entry has in common |
| `build/build.py` | Verovio engraving + geometry extraction (note positions, staff boxes, bar lines) |
| `build/kernprep.py` | normalises the two Humdrum constructs Verovio will not import (see below) |
| `build/pieces.py` | the repertoire and its editorial matter |
| `build/facts.py` | dumps what the analysis found per piece, so the prose can be checked against it |
| `build/look.py` | CLI: dump a voice as bar:beat, or test a candidate subject span |
| `build/make.py` | puts it together into `data/<id>.json`, `<id>.svg`, `<id>.p.svg` |
| `build/bundle.py` | packs the lab into one self-contained `dist/fugue-lab.html` |

The site itself is two pages: `index.html` is the front page (`home.css` / `home.js`) and
`lab.html` is the tool (`app.css` / `app.js`). The front page loads `data/hero.json` — every note of
one fugue, for the figure at the top — and `data/maps.json`, which holds each fugue's thumbnail as
one character per voice per instant. That keeps the front page under 90 kB for all 57; shipping the
full note list for every piece would have cost 1.3 MB.

Nothing is hand-transcribed. Onsets are cross-checked against Verovio's own timemap, and every
note id in the JSON is verified to exist in the engraved SVG, so the score, the roll and the audio
can never drift apart. The build also asserts that the number of bars matches the number of
engraved measures — an anacrusis carries no barline marker in kern and will otherwise put every
bar one measure out.

`build/audit-dom.js` can be pasted into the browser console on either page: it walks every fugue
and reports any text that was meant to be markup but rendered literally.

### Verovio 6.3 notes

Four quirks cost enough time to be worth writing down.

* `getMIDIValuesForElement` and MIDI export **ignore key signatures**, so pitches here come from the
  `**kern` tokens instead, which spell every accidental explicitly.
* A note carrying an explicit stem-direction marker (`/` or `\`) sometimes loses its `xml:id`, which
  breaks the join between kern data and engraved geometry. The markers are cosmetic, so when
  geometry comes back short the build re-renders without them and tries again.
* A **phantom empty column** in the spine header (wtc1f24 has one) shifts every field number by one.
* `*+`, which adds a spine mid-piece for a voice that enters late (wtc1f20 gains a fifth voice for
  its last bars), makes the Humdrum importer return an **empty score** with no error. `kernprep.py`
  declares the spine from the start instead and leaves it silent until it enters — padded with
  invisible bar rests, not null tokens, since kern time comes from durations and a spine of nulls
  never advances its own clock.

## Sources & credits

* **The music** is Bach's and long out of copyright. The edition underneath is the
  Bach-Gesellschaft Ausgabe (Breitkopf & Härtel, 1866, ed. Franz Kroll).
* **The encodings** are the Humdrum `**kern` digital editions:
  [humdrum-tools/bach-wtc-fugues](https://github.com/humdrum-tools/bach-wtc-fugues) (WTC, encoded by
  David Huron) and [craigsapp/art-of-the-fugue](https://github.com/craigsapp/art-of-the-fugue).
  Neither repository has a licence file, so this one does **not** redistribute them; `build/fetch.sh`
  pulls them from upstream at build time. The rendered SVG and analysis JSON in `data/` are derived
  from them. If either encoder would prefer that not be published, open an issue and it comes down.
* **The engraving** is by [Verovio](https://www.verovio.org/) (MIT), run at build time.
* To read the printed score alongside: [IMSLP](https://imslp.org/wiki/Das_wohltemperierte_Klavier_I,_BWV_846-869_(Bach,_Johann_Sebastian)).

## Licence

Code: MIT (see `LICENSE`). Score data: see above.
