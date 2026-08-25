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
    "Book I of *Das wohltemperirte Clavier* came together in Köthen, and Bach dated the title "
    "page 1722. Twenty-four preludes and fugues, one in every major and minor key, written, in "
    "his words, “for the profit and use of musical youth desirous of learning, and especially "
    "for the pastime of those already skilled in this study.” Copies went round in manuscript "
    "for decades; the first printed editions appeared in 1801.")
WTC2_CONTEXT = (
    "Book II was put together in Leipzig around 1739–42, nearly twenty years after Book I, out "
    "of pieces Bach had been writing over a much longer span. The main source is the London "
    "autograph in the British Library, some of it in his hand, some in Anna Magdalena's.")
AOF_CONTEXT = (
    "Bach worked at *Die Kunst der Fuge* through his last decade; it was published in 1751, "
    "after he died. Every movement grows out of the same D minor subject, and the collection "
    "works in order through simple fugues, counter-fugues, double and triple fugues, canons and "
    "mirror fugues. Then it breaks off, unfinished, in the middle of a quadruple fugue.")


def perf(who, note, query):
    return {"who": who, "note": note, "q": query}


PIECES = [
 dict(
  id="bwv855", file="wtc1f10.krn", bpm=116,
  title="Fugue in E minor", bwv="BWV 855", book="WTC I, No. 10", collection="wtc1",
  blurb="The only two-voice fugue in either book. One line above and one below, so you hear "
        "every entry without trying. Start here.",
  history=[
    "Every other fugue in Book I has three, four or five voices. This one has two. That leaves "
    "Bach almost nothing to hide behind, which is exactly why students are often handed it "
    "first.",
    "Halfway through, the quavers start and never stop: the second half is a *perpetuum mobile* "
    "running under and over the subject. Hence the habit of calling it a two-part invention that "
    "grew up.",
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
  blurb="Three voices, a compact subject, a countersubject that returns nearly every time, and "
        "episodes spun from the subject's own tail. If you learn to hear one fugue, make it this one.",
  history=[
    "Two-bar subject, tonal answer, a countersubject that comes back intact with most entries, "
    "episodes built by sequencing fragments of the subject itself. Everything lines up, which is "
    "presumably why no fugue of Bach's has been analysed more often.",
    "The last entry arrives over a tonic pedal, and the piece ends in C major rather than C "
    "minor — a *tierce de Picardie*, the standard Baroque way of finishing a minor-key "
    "movement.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in C minor, BWV 847", "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C_minor,_BWV_847"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano, 1963", "Glenn Gould Bach Fugue C minor BWV 847"),
    perf("Edwin Fischer", "piano, 1933–36, the first complete recording", "Edwin Fischer Bach Well Tempered Clavier BWV 847"),
    perf("Wanda Landowska", "harpsichord", "Landowska Bach Well Tempered Clavier C minor fugue"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 847 fugue"),
  ]),

 dict(
  id="bwv851", file="wtc1f06.krn", bpm=126, forms=("P", "I"),
  title="Fugue in D minor", bwv="BWV 851", book="WTC I, No. 6", collection="wtc1",
  blurb="Short, fast, three voices, and halfway through Bach turns the subject upside down. "
        "Switch on the entry brackets and watch the shape flip.",
  history=[
    "The subject is barely two bars of running quavers, short enough that Bach can stack the "
    "entries close together and then invert the thing outright. Every rising step becomes a "
    "falling one.",
    "Inversion, stretto and a tonic pedal at the close, all inside forty-odd bars. He is showing "
    "off.",
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
  blurb="A 3/8 fugue that moves like a dance. The subject is long and nearly all stepwise, so "
        "each voice reads as a tune rather than a knot of figuration.",
  history=[
    "3/8, full of scale figures, closer to a gigue than to a study. The subject is long, so there "
    "are fewer entries than usual and the episodes between them stretch out to match.",
    "Teachers reach for it early in Book I because the three lines stay easy to tell apart by ear.",
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
  blurb="Cheerful, three voices, and a subject that leaps about for nearly four bars before it "
        "finishes. At that length there is room for only a handful of entries.",
  history=[
    "Because the subject runs close to four bars, the fugue holds far fewer statements than a "
    "piece its length normally would. Most of what you hear is episode.",
    "The prelude in front of it is the toccata-like one that opens with a big sweeping flourish. "
    "Recitalists love the pair.",
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
  blurb="Almost nothing but subject. Four voices, no regular countersubject, barely an episode "
        "anywhere; the entries pile up in stretto until there is no room left for anything else.",
  history=[
    "Statements of the subject overlap almost continuously, and the music never settles into the "
    "subject-then-episode alternation most fugues run on. It is the densest fugue in Book I, and "
    "Bach put it first.",
    "No countersubject comes back reliably, which is unusual for him and part of why the fugue "
    "sounds so single-minded. Every voice is doing the same thing, just at different times.",
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
  blurb="Four voices, a short subject with a very definite rhythm, and a countersubject that "
        "sticks to it. Play it after the two-voice E minor and you can hear what the extra lines do.",
  history=[
    "Four real voices moving at once, and the texture still never turns to mud. The subject is "
    "short and rhythmically sharp enough to stay audible under everything else.",
    "Three voices give you three pairs of intervals to keep under control at any moment; four "
    "voices give you six. This is the standard example of how Bach handles the extra line.",
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
  blurb="Bach writing in an idiom that was already old when he was born. Long white notes, alla "
        "breve, four voices moving like a Renaissance motet.",
  history=[
    "*Stile antico*, the archaic idiom of Palestrina and his successors, which Bach studied and "
    "revived. Alla breve notation, a subject that moves in semibreves and minims, and harmony "
    "that changes slowly enough for every suspension to land.",
    "The long note values mean you can take the intervals between the voices one at a time, by "
    "eye and by ear. If you want to watch counterpoint in slow motion, open this one.",
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
  blurb="One subject, four voices, no tricks. It opens The Art of Fugue as plainly as it can, and "
        "everything else in the cycle is a variation on it.",
  history=[
    "A *simple fugue* in the technical sense: one subject, treated straightforwardly. Bach puts it "
    "first so that the transformations to come have something to be measured against.",
    "The collection is written in open score, one staff per voice, with no instrument specified. "
    "That is the layout on this page too. Bach engraved it to be read as much as played, which is "
    "most of why the counterpoint stays legible.",
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
