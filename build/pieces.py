"""Repertoire: which fugues the site ships, plus the editorial matter shown
alongside them. Facts here are limited to things that are uncontroversial and
checkable from the linked sources; the bar counts, entry counts and structural
labels shown in the app are computed from the score itself, not typed in."""

WTC1_SCORE = ("Complete score (IMSLP)",
              "https://imslp.org/wiki/Das_wohltemperierte_Klavier_I,_BWV_846-869_(Bach,_Johann_Sebastian)")
WTC2_SCORE = ("Complete score (IMSLP)",
              "https://imslp.org/wiki/Das_wohltemperierte_Klavier_II,_BWV_870-893_(Bach,_Johann_Sebastian)")
AOF_SCORE  = ("Complete score (IMSLP)",
              "https://imslp.org/wiki/Die_Kunst_der_Fuge,_BWV_1080_(Bach,_Johann_Sebastian)")
WTC_WIKI   = ("The Well-Tempered Clavier", "https://en.wikipedia.org/wiki/The_Well-Tempered_Clavier")
AOF_WIKI   = ("The Art of Fugue", "https://en.wikipedia.org/wiki/The_Art_of_Fugue")
KERN_WTC   = ("Note data: bach-wtc-fugues (Humdrum **kern)",
              "https://github.com/humdrum-tools/bach-wtc-fugues")
KERN_AOF   = ("Note data: art-of-the-fugue (Humdrum **kern)",
              "https://github.com/craigsapp/art-of-the-fugue")

WTC1_CONTEXT = (
    "Book I of *Das wohltemperirte Clavier* was assembled in Köthen and dated 1722 on "
    "Bach's title page. Twenty-four preludes and fugues, one in every major and minor key, "
    "written — in Bach's own words — “for the profit and use of musical youth desirous "
    "of learning, and especially for the pastime of those already skilled in this study.” "
    "It circulated in manuscript copies for decades; the first printed editions appeared only "
    "in 1801.")
WTC2_CONTEXT = (
    "Book II was gathered in Leipzig around 1739–42, nearly twenty years after Book I, "
    "from pieces written across a long span. The main source is the so-called London autograph "
    "in the British Library, partly in Bach's hand and partly in Anna Magdalena's.")
AOF_CONTEXT = (
    "*Die Kunst der Fuge* occupied Bach in his last decade and was published posthumously in "
    "1751. Every movement grows from one D minor subject; the collection works systematically "
    "through simple fugues, counter-fugues, double and triple fugues, canons and mirror fugues, "
    "and breaks off unfinished in the middle of a quadruple fugue.")


def perf(who, note, query):
    return {"who": who, "note": note, "q": query}


PIECES = [
 dict(
  id="bwv855", file="wtc1f10.krn", bpm=116,
  title="Fugue in E minor", bwv="BWV 855", book="WTC I, No. 10", collection="wtc1",
  blurb="The only two-voice fugue in either book. With just one line above and one below, "
        "every entry, every episode and every crossing is unmistakable — the best place to start.",
  history=[
    "The E minor is the outlier of Book I: two voices where every other fugue has three, four "
    "or five. Bach gives himself almost no room to hide, and the piece is often the first fugue "
    "a student takes apart for exactly that reason.",
    "The second half turns into a *perpetuum mobile* — continuous running quavers under and over "
    "the subject — which is why it is sometimes described as a two-part invention that grew up.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in E minor, BWV 855", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_E_minor,_BWV_855"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano, 1965", "Glenn Gould Bach Fugue E minor BWV 855"),
    perf("Sviatoslav Richter", "piano, 1973", "Richter Bach Well Tempered Clavier BWV 855 fugue"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach WTC BWV 855"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 855 fugue"),
  ]),

 dict(
  id="bwv847", file="wtc1f02.krn", bpm=80,
  title="Fugue in C minor", bwv="BWV 847", book="WTC I, No. 2", collection="wtc1",
  blurb="The textbook fugue: three voices, a compact subject, one regular countersubject, and "
        "episodes spun from the subject's own tail. If you learn to hear one fugue, it is this one.",
  history=[
    "No fugue of Bach's has been analysed more often. Its proportions are unusually clean — a "
    "two-bar subject, a tonal answer, a countersubject that returns intact with most entries, "
    "and episodes built by sequencing fragments of the subject itself.",
    "The last entry arrives over a tonic pedal, and the piece closes in C major: a *tierce de "
    "Picardie*, the standard Baroque way of ending a minor-key movement.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in C minor, BWV 847", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C_minor,_BWV_847"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano, 1963", "Glenn Gould Bach Fugue C minor BWV 847"),
    perf("Edwin Fischer", "piano, 1933–36 — the first complete recording", "Edwin Fischer Bach Well Tempered Clavier BWV 847"),
    perf("Wanda Landowska", "harpsichord", "Landowska Bach Well Tempered Clavier C minor fugue"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 847 fugue"),
  ]),

 dict(
  id="bwv851", file="wtc1f06.krn", bpm=126, forms=("P", "I"),
  title="Fugue in D minor", bwv="BWV 851", book="WTC I, No. 6", collection="wtc1",
  blurb="A short, fast three-voice fugue whose subject Bach turns upside down halfway through. "
        "Switch on the entry brackets and watch the shape flip.",
  history=[
    "The subject is barely two bars of running quavers, which lets Bach stack entries closely and "
    "then invert the subject outright — every rising step becomes a falling one.",
    "Inversion, stretto and a tonic pedal at the close pack a remarkable amount of fugal "
    "technique into forty-odd bars.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in D minor, BWV 851", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_D_minor,_BWV_851"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 851 fugue D minor"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue D minor BWV 851"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier BWV 851"),
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 851"),
  ]),

 dict(
  id="bwv856", file="wtc1f11.krn", bpm=104,
  title="Fugue in F major", bwv="BWV 856", book="WTC I, No. 11", collection="wtc1",
  blurb="A dancing 3/8 fugue. The subject is long and almost entirely stepwise, so each voice "
        "reads as a clear melodic line rather than a knot of figuration.",
  history=[
    "In 3/8 and full of scale figures, this fugue behaves more like a gigue than a study. The "
    "long subject means fewer entries than usual, and correspondingly long episodes between them.",
    "It is one of the pieces that show up early in the Book I teaching sequence precisely because "
    "the three lines stay so easy to follow by ear.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 856 fugue F major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue F major BWV 856"),
    perf("Bob van Asperen", "harpsichord", "van Asperen Bach Well Tempered Clavier BWV 856"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 856 fugue"),
  ]),

 dict(
  id="bwv866", file="wtc1f21.krn", bpm=132,
  title="Fugue in B-flat major", bwv="BWV 866", book="WTC I, No. 21", collection="wtc1",
  blurb="A cheerful three-voice fugue on an unusually long, leaping subject — nearly four bars of "
        "it — which leaves room for only a handful of entries.",
  history=[
    "The subject runs on for close to four bars, so the whole fugue contains far fewer statements "
    "than a piece of its length usually would; most of the music is episode.",
    "The prelude that precedes it is the toccata-like one with the sweeping opening flourish, and "
    "the pair is a favourite of recitalists.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in B-flat major, BWV 866", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B-flat_major,_BWV_866"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue B flat major BWV 866"),
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 866 fugue"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier BWV 866"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 866"),
  ]),

 dict(
  id="bwv846", file="wtc1f01.krn", bpm=72,
  title="Fugue in C major", bwv="BWV 846", book="WTC I, No. 1", collection="wtc1",
  blurb="Almost nothing but subject. Four voices, no regular countersubject, barely an episode — "
        "entry piles on entry in stretto until the piece is saturated with its own theme.",
  history=[
    "The opening fugue of Book I is the densest in the collection: statements of the subject "
    "overlap almost continuously, and the music never settles into the subject/episode alternation "
    "that most fugues rely on.",
    "There is no countersubject that returns reliably, which is unusual for Bach and is one reason "
    "the piece sounds so single-minded. Every voice is doing the same thing, just at different times.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in C major, BWV 846", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C_major,_BWV_846"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano, 1962", "Glenn Gould Bach Fugue C major BWV 846"),
    perf("Sviatoslav Richter", "piano, Innsbruck 1973", "Richter Bach BWV 846 fugue"),
    perf("Wanda Landowska", "harpsichord", "Landowska Bach C major fugue Well Tempered Clavier"),
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 846 fugue"),
  ]),

 dict(
  id="bwv861", file="wtc1f16.krn", bpm=80,
  title="Fugue in G minor", bwv="BWV 861", book="WTC I, No. 16", collection="wtc1",
  blurb="Four voices, a short and sharply characterised subject, and a countersubject that sticks "
        "to it. A good demonstration of how much four-part texture changes the sound of a fugue.",
  history=[
    "The subject is compact and rhythmically distinctive, which lets Bach keep four real voices "
    "moving without the texture turning muddy.",
    "Adding a fourth voice roughly doubles the number of simultaneous intervals you have to control; "
    "this fugue is a standard example of how the extra line is handled.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in G minor, BWV 861", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_G_minor,_BWV_861"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue G minor BWV 861"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 861 fugue"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 861"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 861"),
  ]),

 dict(
  id="bwv878", file="wtc2f09.krn", bpm=104,
  title="Fugue in E major", bwv="BWV 878", book="WTC II, No. 9", collection="wtc2",
  blurb="Bach writing deliberately in the old style: long white notes, alla breve, four voices "
        "moving like a Renaissance motet. Counterpoint at its most transparent.",
  history=[
    "This is *stile antico* — the archaic idiom of Palestrina and his successors, which Bach "
    "studied and revived. The notation is alla breve, the subject moves in semibreves and minims, "
    "and the harmonic rhythm is slow enough that every suspension registers.",
    "Because the note values are long, the vertical intervals between the voices are unusually easy "
    "to see and hear; this is the fugue to open if you want to watch counterpoint in slow motion.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 878 fugue E major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 878 fugue"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 878"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 878"),
  ]),

 dict(
  id="bwv1080-1", file="artfugue-001.krn", bpm=76, modernClefs=True,
  title="Contrapunctus I", bwv="BWV 1080/1", book="The Art of Fugue", collection="aof",
  blurb="The plainest possible statement of the greatest fugal project ever undertaken: four "
        "voices, one subject, no tricks. Everything else in the cycle is a variation on this.",
  history=[
    "Contrapunctus I opens *The Art of Fugue* with a *simple fugue* — one subject, treated "
    "straightforwardly — so that the transformations to come have something to be measured against.",
    "The collection is written in open score, one staff per voice, with no instrument specified. "
    "That is exactly the layout used here, and it is why the counterpoint is so legible: Bach "
    "engraved it to be read, not just played.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Musica Antiqua Köln", "instrumental ensemble", "Musica Antiqua Koln Art of Fugue Contrapunctus 1"),
    perf("Glenn Gould", "organ, 1962", "Glenn Gould Art of Fugue Contrapunctus 1 organ"),
    perf("Pierre-Laurent Aimard", "piano, DG", "Aimard Art of Fugue Contrapunctus 1"),
    perf("Emerson String Quartet", "string quartet", "Emerson Quartet Art of Fugue Contrapunctus 1"),
  ]),
]

VOICE_NAMES = {
  2: ["Upper", "Lower"],
  3: ["Soprano", "Alto", "Bass"],
  4: ["Soprano", "Alto", "Tenor", "Bass"],
  5: ["Soprano", "Mezzo", "Alto", "Tenor", "Bass"],
}
