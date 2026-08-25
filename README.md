# Fugue Lab

A viewer for Bach fugues: one staff per voice, a piano roll drawn on the same horizontal axis as
the score, a map of the whole piece, and audio. Every statement of the subject is found by the
build, not typed in by hand.

**→ [Open the site](https://flyingworkshop.github.io/bach-fugue-lab/)**  ·  [jump straight into the lab](https://flyingworkshop.github.io/bach-fugue-lab/lab.html)

Nine fugues: the Well-Tempered Clavier Books I and II, plus Contrapunctus I from *The Art of
Fugue*, ranging from two voices to four.

| | Fugue | Voices | Bars | Statements |
|---|---|---|---|---|
| BWV 855 | E minor, WTC I/10 | 2 | 42 | 8 |
| BWV 847 | C minor, WTC I/2 | 3 | 31 | 8 |
| BWV 851 | D minor, WTC I/6 | 3 | 44 | 14 (3 inverted) |
| BWV 856 | F major, WTC I/11 | 3 | 72 | 13 |
| BWV 866 | B♭ major, WTC I/21 | 3 | 48 | 8 |
| BWV 846 | C major, WTC I/1 | 4 | 27 | 22 |
| BWV 861 | G minor, WTC I/16 | 4 | 34 | 15 |
| BWV 878 | E major, WTC II/9 | 4 | 43 | 15 |
| BWV 1080/1 | Contrapunctus I | 4 | 78 | 9 |

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

**A whole-piece map.** Every entry as a block on its voice's lane, episodes greyed, strettos
flagged, and the estimated key underneath.

**Per-voice audio.** Mute, solo and volume on each voice; *spotlight subject* raises whichever
voice is currently stating the theme and ducks the rest; loop any entry or episode; tempo control.
Synthesised in the browser with the Web Audio API — no samples, no network.

**No dynamics.** Bach wrote none, so there are none here; the Well-Tempered Clavier is harpsichord
and clavichord music. The synthesiser does add loudness of its own: a slight metrical accent and
the subject spotlight, both under **Sound** and both switchable off for a flat, harpsichord-like
reading. Low notes also get a little extra weight so the bass stays audible; that is mixing, not
interpretation.

**Subject lab.** Every statement drawn on top of a ghost of the original, optionally transposed to a
common pitch. The entries Bach bent are the interesting ones.

## Keys

`space` play/pause · `←`/`→` bar · `shift`+`←`/`→` previous/next entry · `1`…`4` solo a voice ·
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
| `build/pieces.py` | the repertoire and its editorial matter |
| `build/make.py` | puts it together into `data/<id>.json`, `<id>.svg`, `<id>.p.svg` |
| `build/bundle.py` | packs the lab into one self-contained `dist/fugue-lab.html` |

The site itself is two pages: `index.html` is the front page (`home.css` / `home.js`, drawing its
figures from `data/teasers.json`), and `lab.html` is the tool (`app.css` / `app.js`).

Nothing is hand-transcribed. Onsets are cross-checked against Verovio's own timemap, and every
note id in the JSON is verified to exist in the engraved SVG, so the score, the roll and the audio
can never drift apart. The build also asserts that the number of bars matches the number of
engraved measures — an anacrusis carries no barline marker in kern and will otherwise put every
bar one measure out.

`build/audit-dom.js` can be pasted into the browser console on either page: it walks every fugue
and reports any text that was meant to be markup but rendered literally.

A note on pitch: Verovio 6.3's `getMIDIValuesForElement` and MIDI export ignore key signatures, so
pitches here come from the `**kern` tokens instead, which spell every accidental explicitly.

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
