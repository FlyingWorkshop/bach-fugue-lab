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
  id="bwv846", file="wtc1f01.krn", bpm=72,
  title="Fugue in C major", bwv="BWV 846", book="WTC I, No. 1", collection="wtc1",
  card="Twenty-two entries in twenty-seven bars, piled into stretto. No regular countersubject, "
       "and barely an episode.",
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
  id="bwv847", file="wtc1f02.krn", bpm=80,
  title="Fugue in C minor", bwv="BWV 847", book="WTC I, No. 2", collection="wtc1",
  card="The textbook fugue. Compact subject, a countersubject that comes back with nearly every "
       "entry, episodes spun from the subject's tail.",
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
  id="bwv848", file="wtc1f03.krn", bpm=74,
  title="Fugue in C-sharp major", bwv="BWV 848", book="WTC I, No. 3", collection="wtc1",
  card="Seven sharps, twelve entries, and not one stretto, inversion or pedal point anywhere in "
       "it.",
  blurb="A countersubject that comes back with eight of the twelve entries, and a hole in the "
        "middle where the subject is out of all three voices for thirteen and a half bars. Turn "
        "the entry brackets on and watch bars 29 to 42 stay empty.",
  history=[
    "Twelve entries, three voices, and none of the tricks a fugue is supposed to show off with. "
    "The subject is under two bars of light quavers falling in broken sixths, and Bach's method "
    "throughout is to sequence it through neighbouring keys rather than stack it on itself. Turn "
    "on the map and it is entries, episodes and countersubject, nothing else. The longest of "
    "those episodes runs thirteen and a half bars, from bar 29 to bar 42, a quarter of the fugue "
    "with no subject in any voice.",
    "C-sharp major means seven sharps, and on a keyboard tuned the ordinary way in 1722 it was "
    "not a key anyone used. The collection exists to argue that it could be. Bach goes there "
    "exactly twice in the 48 — here, and again at No. 3 of Book II.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in C-sharp major, BWV 848",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C-sharp_major,_BWV_848"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue C sharp major BWV 848"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 848 fugue C sharp major"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier BWV 848"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 848 fugue C sharp major"),
  ]),

 dict(
  id="bwv849", file="wtc1f04.krn", bpm=88,
  title="Fugue in C-sharp minor", bwv="BWV 849", book="WTC I, No. 4", collection="wtc1",
  subject=dict(v=4, q0=0, q1=12),  # bars 1:1..4:1
  card="Five voices and 115 bars — the longest fugue in Book I, and one of only two in the book "
       "with five of them.",
  blurb="The biggest thing in Book I: five voices, 115 bars, and a subject so slow that all five "
        "have room to speak. The entry brackets follow the first subject only, which is why a "
        "forty-one-bar stretch early on looks empty. It isn't.",
  history=[
    "The subject is a cross motif in long notes — a falling semitone, a leap, a falling semitone "
    "— and its slowness is what makes five voices possible at all. The bass states it first and "
    "the others come in above, one at a time. Then Bach leaves it alone for a long while and "
    "brings it back harder: fourteen entries in all, four of them piled up between bars 94 and "
    "97, and from bar 105 the bass sits on a pedal almost to the last bar.",
    "It gets called a triple fugue, which is generous. Only the first subject receives a real "
    "exposition; the two later themes behave more like countersubjects that arrive late. The map "
    "on this page tracks the first subject and nothing else, so the forty-one-bar gap after bar 7 "
    "shows up as one enormous episode. That gap is not empty — it is where the second theme is "
    "introduced — and the tool cannot see it. Book II has no five-voice fugue at all.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in C-sharp minor, BWV 849",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C-sharp_minor,_BWV_849"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 849 fugue C sharp minor"),
    perf("Edwin Fischer", "piano, 1933–36, the first complete recording", "Edwin Fischer Bach Well Tempered Clavier BWV 849"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 849"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 849 fugue"),
  ]),

 dict(
  id="bwv850", file="wtc1f05.krn", bpm=62,
  title="Fugue in D major", bwv="BWV 850", book="WTC I, No. 5", collection="wtc1",
  subject=dict(v=3, q0=1, q1=4.75),  # bars 1:2..2:1.75
  card="Twenty-seven entries in twenty-seven bars, more than any other fugue in Book I, and "
       "thirteen overlapping pairs.",
  blurb="The subject is under a bar long and made of dotted figures, so entries can follow each "
        "other almost immediately. Bach takes the invitation: twenty-seven statements in "
        "twenty-seven bars, and no gap anywhere longer than two and a half bars.",
  history=[
    "Dotted rhythm, the idiom of a French overture — the music that played while somebody "
    "important walked into a room. Because the subject fits inside a single bar, the entries can "
    "come one on top of another, and they do: thirteen overlapping pairs. Four episodes, adding "
    "up to under six bars in total. Sixteen of the twenty-seven statements are partial rather "
    "than complete, which is what happens when you pack them this tightly: a head enters, the "
    "next voice arrives, and the tail never gets finished.",
    "Open this one next to the C-sharp major fugue two numbers earlier and the two structural "
    "maps barely look like the same kind of object. That one has a thirteen-bar hole in the "
    "middle with no subject in it. This one has no hole longer than two and a half bars. Only the "
    "C major fugue that opens the book spends less of its length in episode, and that one is here "
    "too.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue D major BWV 850"),
    perf("Wanda Landowska", "harpsichord", "Landowska Bach Well Tempered Clavier D major fugue"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 850 fugue"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier BWV 850"),
  ]),

 dict(
  id="bwv851", file="wtc1f06.krn", bpm=126, forms=("P", "I"),
  title="Fugue in D minor", bwv="BWV 851", book="WTC I, No. 6", collection="wtc1",
  card="Fast, and then halfway through Bach turns the subject upside down and carries on "
       "regardless.",
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
  id="bwv852", file="wtc1f07.krn", bpm=78,
  title="Fugue in E-flat major", bwv="BWV 852", book="WTC I, No. 7", collection="wtc1",
  subject=dict(v=0, q0=0, q1=8),  # bars 1:1..3:1
  card="Three statements of the subject in thirty-seven bars, the fewest of any fugue on this "
       "site.",
  blurb="The prelude in front of this fugue already contains a complete four-voice fugue of its "
        "own — the only one of the 48 that does. What follows is three voices, short and light: "
        "thirty-one of its thirty-seven bars are episode.",
  history=[
    "The tracker finds three statements of the subject and nothing after bar 22. Take that as "
    "much as a fact about the tracker as about the fugue: the matcher wants something close to a "
    "literal restatement, and it stops finding one. But the shape it reports is real enough. "
    "Thirty-one of thirty-seven bars fall inside an episode, a higher proportion than any other "
    "fugue in Book I, and the last episode alone runs fifteen and a half bars. The key path does "
    "the work the entries would normally do: E-flat, F minor, C minor, back to E-flat, out to C "
    "major and C minor, home.",
    "The prelude is the strange one of the pair. Seventy bars in three sections — a short "
    "toccata, then a chorale in four-part harmony, then a four-voice double fugue longer than the "
    "other two put together. No other prelude in either book has a finished fugue inside it. "
    "Which is presumably why what follows is three voices and unbothered: the contrapuntal "
    "argument had already been made.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in E-flat major, BWV 852",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_E-flat_major,_BWV_852"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 852 fugue E flat major"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 852 fugue"),
    perf("Pieter-Jan Belder", "harpsichord", "Pieter-Jan Belder Bach Well Tempered Clavier BWV 852"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue E flat major BWV 852"),
  ]),

 dict(
  id="bwv853", file="wtc1f08.krn", bpm=76,
  title="Fugue in D-sharp minor", bwv="BWV 853", book="WTC I, No. 8", collection="wtc1",
  subject=dict(v=1, q0=0, q1=10),  # bars 1:1..3:3
  forms=("I", "Aug"),
  card="Prelude in E-flat minor, fugue in D-sharp minor: same key, six flats swapped for six "
       "sharps.",
  blurb="The only fugue on this site with both augmentation and inversion in it, and the only one "
        "in Book I with augmentation at all. Switch the entry brackets on and watch three "
        "statements come back at double length.",
  history=[
    "Two and a half bars of slow steps around a rising fifth, and Bach then works the subject "
    "harder than anything else in Book I. Sixteen entries: twelve upright, three stretched into "
    "augmentation, one turned upside down. Five arrive in stretto. Thirteen of the sixteen are "
    "altered rather than literal, so the piece is bending the shape almost every time it returns "
    "rather than restating it. Across 87 bars there are nine episodes, the longest of them "
    "seventeen and a half — this is a fugue that takes its time between arguments.",
    "Six sharps or six flats: the same twelve keys under the hand, but only if the instrument is "
    "tuned so that they are. That is the claim the whole collection is making, and No. 8 makes it "
    "on a single opening — the prelude notated in E-flat minor, the fugue in D-sharp minor, and "
    "nothing changing except what the player reads. Some editions print the fugue both ways and "
    "let you pick.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in E-flat minor, BWV 853",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_E-flat_minor,_BWV_853"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 853 fugue D sharp minor"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 853 fugue"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 853"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 853 fugue E flat minor"),
  ]),

 dict(
  id="bwv854", file="wtc1f09.krn", bpm=84,
  title="Fugue in E major", bwv="BWV 854", book="WTC I, No. 9", collection="wtc1",
  card="A one-bar subject with a countersubject glued to it — six of the eleven entries carry "
       "both.",
  blurb="Small in every dimension: a subject one bar long, eleven entries, twenty-nine bars, "
        "exposition finished before bar five. Turn the entry brackets on and the subject drags "
        "its countersubject along with it, entry after entry.",
  history=[
    "A subject that fits inside one bar is about as short as Bach writes them, and it lets the "
    "next voice come in a bar later without waiting. Eleven entries, four of them in stretto, and "
    "six carrying the same countersubject each time. Then the surprise: seventeen of the "
    "twenty-nine bars have no subject in them anywhere. For a piece this compact, more than half "
    "of it is sequence.",
    "No inversion, no augmentation, no pedal point. The stretto is the only trick in it, and the "
    "piece is over before it could build to anything larger. What it has instead is a route: E "
    "major for two bars, B major, then bars 9 to 18 spent in C-sharp minor and G-sharp minor, and "
    "home. A third of a cheerful fugue is in the minor, and it does not sound like it.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 854 fugue E major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue E major BWV 854"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier BWV 854"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 854 fugue"),
  ]),

 dict(
  id="bwv855", file="wtc1f10.krn", bpm=116,
  title="Fugue in E minor", bwv="BWV 855", book="WTC I, No. 10", collection="wtc1",
  card="The only two-voice fugue in either book. One line above, one below, and nowhere to hide. "
       "Start here.",
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
  id="bwv856", file="wtc1f11.krn", bpm=104,
  title="Fugue in F major", bwv="BWV 856", book="WTC I, No. 11", collection="wtc1",
  card="A dancing 3/8, and a long subject that walks almost entirely by step, so each voice reads "
       "as a tune.",
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
  id="bwv857", file="wtc1f12.krn", bpm=66,
  title="Fugue in F minor", bwv="BWV 857", book="WTC I, No. 12", collection="wtc1",
  subject=dict(v=2, q0=1, q1=12.5),  # bars 1:2..4:1.5
  card="Four voices, a chromatic subject, and one note held for nine bars from bar 19 while "
       "everything moves over it.",
  blurb="A chromatic subject: eleven notes, most of them a semitone from the last, with two leaps "
        "in the middle so it never turns into a plain scale. Ten entries and eight episodes, and "
        "after the exposition the two simply alternate to the end.",
  history=[
    "Eleven notes over nearly three bars, most of them a semitone apart. The exposition closes in "
    "bar 16, and six more statements follow at bars 19, 27, 34, 40, 47 and 53, each with an "
    "episode in front of it. Eight episodes in all, none longer than five and a half bars, and "
    "the countersubject is marked three times.",
    "Watch bar 19. A pedal starts there and holds for nine bars while an entry, an episode and a "
    "change of key all happen above it; on the piano roll it is one long horizontal line with "
    "everything else moving around it. Then look at the last bar: F, A natural, C, F. The fugue "
    "ends on a major chord, a *tierce de Picardie*, even though the key strip above it still "
    "reads F minor.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in F minor, BWV 857",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_F_minor,_BWV_857"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Edwin Fischer", "piano", "Edwin Fischer Bach Well Tempered Clavier BWV 857 fugue"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 857 fugue F minor"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 857 fugue F minor"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 857"),
  ]),

 dict(
  id="bwv858", file="wtc1f13.krn", bpm=72,
  title="Fugue in F-sharp major", bwv="BWV 858", book="WTC I, No. 13", collection="wtc1",
  card="Seven entries in thirty-five bars, and after the exposition the subject disappears for "
       "eight of them.",
  blurb="Three voices, and no countersubject at all — nothing travels with the subject, so the "
        "other two lines are free every time it comes round.",
  history=[
    "Sixteen notes, not quite two bars. Seven statements across thirty-five bars with five "
    "episodes between them, and the longest of those runs from bar 7 to bar 15: the exposition "
    "ends and the subject is gone for close to a quarter of the piece.",
    "Six sharps. On a keyboard in the meantone tuning that was still common in Bach's day, "
    "F-sharp major sat somewhere between harsh and unplayable, which is the argument the whole "
    "collection is making. Having got there, the fugue then spends bars 3 to 18 in C-sharp major, "
    "which has seven.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 858 fugue F sharp major"),
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 858 fugue"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier BWV 858"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue F sharp major BWV 858"),
  ]),

 dict(
  id="bwv859", file="wtc1f14.krn", bpm=80,
  title="Fugue in F-sharp minor", bwv="BWV 859", book="WTC I, No. 14", collection="wtc1",
  forms=("I",),
  card="Six-four time, and four voices take eighteen of the forty bars just to finish entering.",
  blurb="Bach interrupts his own exposition twice with episodes, so the fourth voice does not "
        "enter until bar 15. Two of the nine statements arrive inverted, both of them after the "
        "exposition is finally over.",
  history=[
    "The subject walks: eighteen notes over nearly three bars of 6/4, which works out at about a "
    "note a beat. Two episodes cut into the exposition before the fourth voice has said anything, "
    "the longer one from bar 11 to bar 15, so four entries end up spread over eighteen of the "
    "forty bars. Nine statements in total, seven upright and two inverted, with the "
    "countersubject marked five times.",
    "The key map flickers here: nine regions in forty bars, including two short patches of "
    "F-sharp major inside a fugue that begins and ends minor. For the opposite case open the C "
    "major fugue, the one that starts Book I: twenty-two entries crammed into twenty-seven bars, "
    "overlapping from the first page.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 859 fugue F sharp minor"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 859"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier BWV 859"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 859 fugue F sharp minor"),
  ]),

 dict(
  id="bwv860", file="wtc1f15.krn", bpm=108,
  title="Fugue in G major", bwv="BWV 860", book="WTC I, No. 15", collection="wtc1",
  card="Eighty-six bars, four entries: three episodes account for sixty-nine of the bars.",
  blurb="The subject appears at bars 1, 5, 11 and 38, and the finder marks nothing after that. "
        "The last forty-five bars come out as one long episode.",
  history=[
    "Four bars and thirty-one notes of running quavers, long enough that Bach gets three voices "
    "in and then more or less stops. Three episodes account for sixty-nine of the eighty-six "
    "bars. From bar 42 to the end there is no statement marked at all, just sequences running "
    "through E minor, B minor, D major and A major before the music comes home, with a pedal "
    "under the last three bars.",
    "Turn the entry brackets on and the map goes blank after bar 42. Four entries in eighty-six "
    "bars is a strange count, and this is the page where the finder is least likely to be right: "
    "the labels are computed from the notes, and a late entry that has been altered is exactly "
    "the sort it misses. Check it against the score before taking the second half as "
    "subject-free.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue G major BWV 860"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 860 fugue G major"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier BWV 860"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 860 fugue"),
  ]),

 dict(
  id="bwv861", file="wtc1f16.krn", bpm=80,
  title="Fugue in G minor", bwv="BWV 861", book="WTC I, No. 16", collection="wtc1",
  card="Four voices, a short and sharply drawn subject, and a countersubject stuck to it. Hear "
       "how much thicker four parts sound than three.",
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
  id="bwv862", file="wtc1f17.krn", bpm=80,
  title="Fugue in A-flat major", bwv="BWV 862", book="WTC I, No. 17", collection="wtc1",
  subject=dict(v=2, q0=1, q1=5),  # bars 1:2..2:2
  card="A seven-note subject one bar long, stated thirteen times, four of them in four "
       "consecutive bars.",
  blurb="Seven notes and a single bar, so the subject can come round thirteen times in "
        "thirty-five bars without the texture ever thickening. Four voices, and nothing recurring "
        "against it anywhere.",
  history=[
    "The entries arrive in pairs a bar apart through the exposition — bars 1 and 2, then 5 and 6 "
    "— thin out across the middle for an eight-bar episode, then bunch again at bars 27, 28, 29 "
    "and 30. Thirteen statements in thirty-five bars, and because no countersubject comes back "
    "with them the texture never repeats itself.",
    "Each bracket carries two things: the role the finder gave the statement, and the note it "
    "starts on. Through the first ten bars those notes read A-flat, E-flat, A-flat, E-flat, "
    "A-flat. At bars 27 to 30 they read A-flat, G, E-flat, C: four bars, four different starting "
    "notes. It is the quickest way to see what those labels are for.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 862 fugue A flat major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue A flat major BWV 862"),
    perf("Christophe Rousset", "harpsichord", "Christophe Rousset Bach Well Tempered Clavier BWV 862"),
    perf("Edwin Fischer", "piano", "Edwin Fischer Bach Well Tempered Clavier BWV 862"),
  ]),

 dict(
  id="bwv863", file="wtc1f18.krn", bpm=76,
  title="Fugue in G-sharp minor", bwv="BWV 863", book="WTC I, No. 18", collection="wtc1",
  card="Eleven entries, a countersubject marked seven times, and two bars in G-sharp major — "
       "eight sharps, no signature.",
  blurb="Eleven entries in forty-one bars with the countersubject marked seven times, so for most "
        "of the piece two fixed lines travel together and the other voices fill in around them.",
  history=[
    "Only one of the eleven statements gets labelled an answer, even though five of them start on "
    "D-sharp. The labels on this page are computed from the notes rather than typed in, and this "
    "is a spot where the computation and a textbook would probably disagree, so take the roles as "
    "a first pass. The bar numbers and entry positions are exact.",
    "The harmony goes a long way out. Bars 20 to 22 come out as G-sharp major, which needs eight "
    "sharps and so has no signature at all; bars 22 to 26 come out as A-sharp minor, whose seven "
    "sharps are the ones Bach already used for the C-sharp major pair earlier in the book. He "
    "passes through both in a couple of bars each on the way to B major and back. Eight key "
    "regions in forty-one bars.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 863 fugue G sharp minor"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 863"),
    perf("Pieter-Jan Belder", "harpsichord", "Pieter-Jan Belder Bach Well Tempered Clavier BWV 863"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 863 fugue"),
  ]),

 dict(
  id="bwv864", file="wtc1f19.krn", bpm=112,
  title="Fugue in A major", bwv="BWV 864", book="WTC I, No. 19", collection="wtc1",
  subject=dict(v=0, q0=0, q1=9),  # bars 1:1..3:1
  card="The only 9/8 fugue in the forty-eight; seven entries in fifty-four bars, and the rest is "
       "episode.",
  blurb="Three voices, 9/8, and no other fugue in either book is in that metre. Seven entries in "
        "fifty-four bars, six episodes between them sequenced out of the subject's own rising "
        "fourths, and the episodes take up more of the piece than the entries do.",
  history=[
    "The subject opens with a single note, then a gap three quavers wide, then a chain of rising "
    "fourths, each one falling back before the next climbs higher. Fourteen notes, spanning a "
    "ninth. After that Bach more or less puts it away: six episodes between the seven entries, "
    "and the last of them runs nearly eleven bars.",
    "The analysis finds no countersubject and no stretto anywhere in the piece, and that is not "
    "the detector giving up — there is nothing there to find. What organises it instead is the "
    "key scheme: A, F-sharp minor, B minor, E, back to A for eleven bars, then out to B minor and "
    "F-sharp minor before the run home.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 864 fugue A major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue A major BWV 864"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 864"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 864 fugue"),
  ]),

 # BWV 865 (A minor, WTC I No. 20) is deliberately absent: in the kern encoding the
 # whole of its final bar is commented out ("the voicing in the final measure is
 # somewhat arbitrary"), so the fugue would end a bar early.


 dict(
  id="bwv866", file="wtc1f21.krn", bpm=132,
  title="Fugue in B-flat major", bwv="BWV 866", book="WTC I, No. 21", collection="wtc1",
  card="The subject leaps about for nearly four bars before it lets go. At that length there is "
       "no room for many entries, so most of what you hear is episode.",
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
  id="bwv867", file="wtc1f22.krn", bpm=72,
  title="Fugue in B-flat minor", bwv="BWV 867", book="WTC I, No. 22", collection="wtc1",
  subject=dict(v=0, q0=0, q1=10),  # bars 1:1..3:2
  card="Five voices, a seven-note subject with a minor ninth cut into it, and three entries a bar "
       "apart at the close.",
  blurb="Five voices, which happens twice in Book I. The subject is seven notes long with a "
        "silence and a minor-ninth leap cut into the middle, and at the close it comes back three "
        "times a bar apart: soprano, then alto, then bass.",
  history=[
    "Seven notes, spread over two and a half bars. The subject drops a fourth, stops dead for a "
    "crotchet, then leaps up a minor ninth and walks back down. That silence in the middle is the "
    "character of the whole piece, and with five voices running it means the texture is "
    "constantly thinning out and refilling. Eleven entries in seventy-five bars, six episodes, "
    "and the longest of those runs eighteen and a half bars with no subject in it at all.",
    "Book I has exactly two fugues in five voices: this one and the C-sharp minor at No. 4. Both "
    "are written alla breve, in the old church idiom — long note values, harmony moving at choir "
    "speed.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in B-flat minor, BWV 867",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B-flat_minor,_BWV_867"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 867 fugue B flat minor"),
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 867 fugue"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue B flat minor BWV 867"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier BWV 867"),
  ]),

 dict(
  id="bwv868", file="wtc1f23.krn", bpm=68,
  title="Fugue in B major", bwv="BWV 868", book="WTC I, No. 23", collection="wtc1",
  subject=dict(v=2, q0=0.5, q1=8),  # bars 1:1.5..3:1
  forms=("I",),
  card="Four voices in thirty-four bars, nine entries, and two of them turn the subject upside "
       "down.",
  blurb="Four voices inside thirty-four bars, so the episodes never run past four and a half. Two "
        "of the nine entries come in inverted; the subject is short enough and stepwise enough "
        "that you can hear the flip without looking.",
  history=[
    "Thirty-four bars is not much room for four voices, and none of it is spent idling: five "
    "episodes, the longest four and a half bars, with nine entries packed around them. The "
    "subject turns around B, drops a fifth, then walks a scale straight back up and over the top "
    "— thirteen notes, nearly all of them by step. The two inverted entries come one after the "
    "other, soprano then alto, and the alto one is still going when the bass brings the subject "
    "back up the right way.",
    "B major has five sharps, and in the meantone tunings common before Bach's day it was not a "
    "key anyone played in. Book I reaches it at No. 23, second from last. What comes out is "
    "short, bright and well travelled: G-sharp minor, F-sharp major and C-sharp minor all get "
    "visited inside those thirty-four bars.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 868 fugue"),
    perf("Edwin Fischer", "piano, 1933–36", "Edwin Fischer Bach Well Tempered Clavier BWV 868"),
    perf("Wanda Landowska", "harpsichord", "Landowska Bach Well Tempered Clavier B major fugue"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 868 fugue B major"),
  ]),

 dict(
  id="bwv869", file="wtc1f24.krn", bpm=56,
  title="Fugue in B minor", bwv="BWV 869", book="WTC I, No. 24", collection="wtc1",
  subject=dict(v=1, q0=0.5, q1=12),  # bars 1:1.5..4:1
  card="Last in Book I, marked Largo, with a twenty-note subject that uses all twelve chromatic "
       "pitches.",
  blurb="The last fugue in Book I, and the one Bach headed *Largo*. Its subject runs twenty notes "
        "and touches all twelve pitches of the chromatic scale before it finishes — you can watch "
        "it do that in the roll.",
  history=[
    "Twenty notes in the subject, and between them they cover all twelve pitches of the chromatic "
    "scale before it lands. Bach wrote *Largo* over the fugue. Twelve entries across seventy-six "
    "bars, three pedal points, and the last of those holds for nearly ten bars with everything "
    "else moving above it.",
    "It closes Book I. The twelve entries come in on six different notes — F-sharp, B, E, A, D "
    "and C-sharp — and the music gets as far out as D major and C-sharp minor before the last "
    "stretch home. Nine episodes, the longest of them just over nine bars, so the subject is "
    "never away for long.",
    WTC1_CONTEXT,
  ],
  links=[WTC1_SCORE, ("Prelude and Fugue in B minor, BWV 869",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B_minor,_BWV_869"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 869 fugue B minor"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach Fugue B minor BWV 869"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 869"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier B minor fugue BWV 869"),
  ]),

 dict(
  id="bwv870", file="wtc2f01.krn", bpm=84,
  title="Fugue in C major", bwv="BWV 870", book="WTC II, No. 1", collection="wtc2",
  subject=dict(v=1, q0=0.5, q1=8),  # bars 1:1.5..5:1
  card="Opens Book II with three countersubjects, and Gould's recording of it rode the Voyager "
       "Golden Record.",
  blurb="The piece that opens Book II: three voices in 2/4, with three countersubjects, so the "
        "subject keeps arriving with the same company. Eight entries across eighty-three bars.",
  history=[
    "Book II opens in 2/4, with the subject in the alto: two short gestures, then continuous "
    "semiquavers, twenty notes over not quite four bars. Three countersubjects come back with it, "
    "more regular company than most fugues here give their subject. Six of the eight entries sit "
    "on C or G; the other two go out to A and D in the middle of the piece.",
    "Glenn Gould's recording of this prelude and fugue was put on the Voyager Golden Record, so "
    "two copies of it are now past the edge of the heliosphere. An alternative version of the "
    "same pair is catalogued separately, as BWV 870a.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in C major, BWV 870",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C_major,_BWV_870"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano, the Voyager recording", "Glenn Gould Bach BWV 870 C major Well Tempered Clavier Book 2"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 870 fugue"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 870"),
    perf("Masaaki Suzuki", "harpsichord, BIS", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 870"),
  ]),

 dict(
  id="bwv871", file="wtc2f02.krn", bpm=60,
  title="Fugue in C minor", bwv="BWV 871", book="WTC II, No. 2", collection="wtc2",
  subject=dict(v=1, q0=0.5, q1=4.5),  # bars 1:1.5..2:1.5
  forms=("Aug",),
  card="A one-bar subject, eighteen entries in twenty-eight bars, and two of them stretched to "
       "double length.",
  blurb="Twenty-eight bars, and Bach gets eighteen entries into them — the subject is one bar "
        "long, which is what makes that possible. Two of the entries come in augmentation, at "
        "double the note values.",
  history=[
    "The subject is one bar long. Nine notes. Short enough that Bach can overlap entries more or "
    "less at will, and he does: eighteen entries in twenty-eight bars, with eight places where "
    "one entry starts before the last has finished, plus two stretched out to double the note "
    "values.",
    "It barely goes anywhere — C minor for eleven bars, one bar of A-flat, two of G minor, then C "
    "minor for the remaining fourteen. The interest is not in where the music travels but in how "
    "many ways the subject can be fitted against itself. Set it beside the C minor from Book I, "
    "No. 2, three voices with a tidy exposition and everything in its place: same key, opposite "
    "habits.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in C minor, BWV 871",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C_minor,_BWV_871"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 871 fugue C minor"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 871 fugue"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier Book 2 BWV 871"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 871"),
  ]),

 dict(
  id="bwv872", file="wtc2f03.krn", bpm=82,
  title="Fugue in C-sharp major", bwv="BWV 872", book="WTC II, No. 3", collection="wtc2",
  subject=dict(v=2, q0=0.5, q1=6),  # bars 1:1.5..2:3
  forms=("I",),
  card="Three voices and only four whole statements; the answer cuts in before the subject has "
       "finished.",
  blurb="Eleven notes off the C-sharp major triad, and the answer cuts in on top of it before it "
        "is over. Four whole statements in thirty-five bars, two of them upside down, then "
        "nineteen bars with no subject in them at all.",
  history=[
    "The subject is built out of the notes of the tonic triad and lasts under a bar and a half, "
    "which leaves room for the answer to enter on top of it — and it does, in bar two. After that "
    "Bach varies the thing so freely that only four statements come back whole: two upright, two "
    "inverted, and the last of the four does not arrive until bar 15. The remaining nineteen bars "
    "are episode, settling onto a pedal at bar 28 and another at bar 33.",
    "The prelude in front of it is worth staying for. It opens with the same kind of broken-chord "
    "writing as the C major prelude of Book I, then switches to 3/8 partway through and turns "
    "into a three-voice fugato. So BWV 872 is a prelude and fugue with a small fugue already "
    "sitting inside the prelude.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in C-sharp major, BWV 872",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C-sharp_major,_BWV_872"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 872 fugue C sharp major"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 872"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 872"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 872 fugue"),
  ]),

 dict(
  id="bwv873", file="wtc2f04.krn", bpm=92,
  title="Fugue in C-sharp minor", bwv="BWV 873", book="WTC II, No. 4", collection="wtc2",
  forms=("I",),
  card="The only fugue here in 12/16, and it drops the subject for twenty-nine bars in the "
       "middle.",
  blurb="Ten of the twelve entries land before bar 32, four of them two bars apart. Then the "
        "subject disappears for twenty-nine bars and comes back twice at the end.",
  history=[
    "Nineteen notes inside a bar and a half of 12/16, which is a dancing subject however you play "
    "it. Bach spends the first half of the piece stacking it up — entries at bars 24, 26, 28 and "
    "30, three of the twelve turned upside down — and then stops. From bar 32 to bar 61 there is "
    "no complete statement anywhere. The next longest gap in the piece is nine bars.",
    "The prelude is in 9/8 and covered in mordents and appoggiaturas; the fugue has almost none. "
    "Two pieces in compound time sitting next to each other, with all the decoration in one of "
    "them.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in C-sharp minor, BWV 873",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_C-sharp_minor,_BWV_873"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 873 fugue C sharp minor"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier BWV 873"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier Book 2 BWV 873"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 873 fugue"),
  ]),

 dict(
  id="bwv874", file="wtc2f05.krn", bpm=110,
  title="Fugue in D major", bwv="BWV 874", book="WTC II, No. 5", collection="wtc2",
  card="Fifteen stretto pairs, more than any fugue here, and four entries stacked inside a bar at "
       "the end.",
  blurb="Twenty-three statements in fifty bars and no countersubject at all — the entries are the "
        "material. Across bars 44 and 45 all four voices start the subject, each a crotchet "
        "behind the last.",
  history=[
    "Nine notes, a bar and a bit, and nothing that reliably comes back with it. What Bach has "
    "instead is overlap: the analysis counts fifteen stretto pairs here, more than in any other "
    "fugue on the site. The entries thicken as the piece goes on, and the last four begin a "
    "crotchet apart, one voice after another, across bars 44 and 45.",
    "It is written in cut time, which normally signals minims and crotchets moving broadly. This "
    "one moves in crotchets and quavers. Take the alla breve at face value and the entries a "
    "crotchet apart stop being separable by ear.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in D major, BWV 874",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_D_major,_BWV_874"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 874 fugue D major"),
    perf("Edwin Fischer", "piano, from the first complete recording of the 48", "Edwin Fischer Bach Well Tempered Clavier BWV 874"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 874"),
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 874 fugue"),
  ]),

 dict(
  id="bwv875", file="wtc2f06.krn", bpm=80,
  title="Fugue in D minor", bwv="BWV 875", book="WTC II, No. 6", collection="wtc2",
  subject=dict(v=1, q0=0, q1=7.5),  # bars 1:1..2:4.5
  card="More notes per bar than any other fugue here, and never two and a half bars go by without "
       "an entry.",
  blurb="Twenty-seven bars, twelve entries, three countersubjects and no room anywhere. Five of "
        "those entries are fragments: Bach starts the subject and then takes it somewhere else.",
  history=[
    "The subject opens in triplet semiquavers, turns chromatic in quavers, and is finished in not "
    "quite two bars — twenty-two notes, with three countersubjects that keep coming back "
    "alongside it. The entries crowd each other: at bar 14 the second voice comes in one crotchet "
    "behind the first, at bar 25 half a bar behind, and the longest episode in the whole piece is "
    "under two and a half bars. Bar for bar there are more notes here than in anything else on "
    "the site.",
    "The countersubjects run in plain semiquavers against those triplets, so the division of the "
    "beat keeps flipping between two and three. The entry count is soft as well: the five "
    "fragments are counted from the moment the subject starts, whether or not it finishes. Look "
    "at where the brackets fall on the map rather than trusting the total.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in D minor, BWV 875",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_D_minor,_BWV_875"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 875 fugue D minor"),
    perf("Sviatoslav Richter", "piano", "Richter Bach Well Tempered Clavier BWV 875"),
    perf("Bob van Asperen", "harpsichord", "van Asperen Bach Well Tempered Clavier BWV 875"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 875 fugue"),
  ]),

 dict(
  id="bwv876", file="wtc2f07.krn", bpm=104,
  title="Fugue in E-flat major", bwv="BWV 876", book="WTC II, No. 7", collection="wtc2",
  card="A six-bar subject, so the four voices need twenty-seven bars just to state it once each.",
  blurb="The subject runs six bars and the voices enter from the bass upwards, which puts the end "
        "of the exposition at bar 27 of 70. Later the entries come a bar apart, so two statements "
        "overlap for five bars.",
  history=[
    "The longest subject of any Book II fugue on the site: twenty notes stretched over six bars, "
    "mostly in long values. Bass first, then tenor, alto, soprano, climbing, and the exposition "
    "alone eats nearly two fifths of the piece. After that Bach stops repeating it exactly — five "
    "of the nine statements come back altered — and at bars 37 and 59 the next voice enters one "
    "bar behind the last, so a six-bar subject runs against itself for five of them.",
    "Two bars of the C minor fugue you can hold in your ear. Six you cannot; by the time the "
    "fourth bar of a statement arrives you have usually stopped hearing it as the subject. That "
    "is the case for the brackets.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 876 fugue E flat major"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 876"),
    perf("Pieter-Jan Belder", "harpsichord", "Pieter-Jan Belder Bach Well Tempered Clavier BWV 876"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 876 fugue"),
  ]),

 dict(
  id="bwv877", file="wtc2f08.krn", bpm=86,
  title="Fugue in D-sharp minor", bwv="BWV 877", book="WTC II, No. 8", collection="wtc2",
  subject=dict(v=1, q0=0.5, q1=8.5),  # bars 1:1.5..3:1.5
  forms=("I",),
  card="Six sharps, four voices, thirteen entries, and exactly one of them upside down.",
  blurb="A two-bar subject, an exposition that takes eleven bars, and then ten bars with no "
        "subject at all. At bar 43 two voices start it on the same beat, one on D-sharp and one "
        "on A-sharp.",
  history=[
    "The alto starts, the tenor answers, the bass follows and the soprano arrives last at bar "
    "nine, so the exposition runs to bar 11. Then nothing for ten bars, the longest episode in "
    "the piece. From bar 21 to bar 32 the entries come back every two or three bars, and the last "
    "of the three strettos puts two voices on the subject at the same instant in bar 43, a fifth "
    "apart. Only one of the thirteen statements is inverted.",
    "Book I spells its eighth pair two ways: the prelude in E-flat minor, the fugue in D-sharp "
    "minor, the same keys under the hands either way. Book II keeps sharps for both halves, which "
    "is why the page is full of double sharps — the leading note in D-sharp minor is C "
    "double-sharp, and it turns up constantly.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 877 fugue D sharp minor"),
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 877 fugue"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier Book 2 BWV 877"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 877"),
  ]),

 dict(
  id="bwv878", file="wtc2f09.krn", bpm=104,
  title="Fugue in E major", bwv="BWV 878", book="WTC II, No. 9", collection="wtc2",
  card="The long white notes and the alla breve are deliberate: this is Bach imitating a "
       "Renaissance motet.",
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
  id="bwv879", file="wtc2f10.krn", bpm=112,
  title="Fugue in E minor", bwv="BWV 879", book="WTC II, No. 10", collection="wtc2",
  subject=dict(v=0, q0=1, q1=24.3333),  # bars 1:1..6:2.66667
  card="Forty-three notes of subject before the second voice gets in, and the last nine bars have "
       "no subject at all.",
  blurb="The subject takes almost six bars and changes gear on the way: crotchets and semiquaver "
        "turns to begin with, a stream of triplets to finish. Nothing ever overlaps, so all nine "
        "statements are out in the open where you can hear them.",
  history=[
    "The answer cannot come in until bar 7, because the first voice is still busy. The exposition "
    "is not over until bar 19 — most of the length of the entire C major fugue that opens Book I "
    "— and this one only runs to 86 bars in total.",
    "After that Bach declines nearly every device that would tighten the piece up. No stretto, no "
    "countersubject that comes back, no pedal at the close, and the analysis marks six of the "
    "nine statements as altered rather than exact — he rewrites the subject more often than he "
    "repeats it. What he does instead is travel: nine key regions in 86 bars, out as far as D "
    "major. The last entry is finished by bar 78, and the remaining nine bars, the longest "
    "episode in the piece, carry on without it.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 879 fugue E minor Well Tempered Clavier"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 879 fugue"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier Book 2 BWV 879"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 879 fugue E minor"),
  ]),

 dict(
  id="bwv880", file="wtc2f11.krn", bpm=88,
  title="Fugue in F major", bwv="BWV 880", book="WTC II, No. 11", collection="wtc2",
  subject=dict(v=0, q0=0.75, q1=6.75),  # bars 1:4..5:4
  card="Six semiquavers to a bar, ninety-nine bars, seven entries — seven-tenths of it is "
       "episode.",
  blurb="Written in 6/16 — two light beats to a bar, three semiquavers each, so the bars go past "
        "very fast. The subject turns up seven times in ninety-nine bars; everything else is "
        "sequence, including one episode that runs for twenty-seven bars without it.",
  history=[
    "Twenty notes over four of those tiny bars, built round a three-note turn and a run back "
    "down. Bach then uses it sparingly: seven entries in the whole fugue, which leaves roughly "
    "seven bars in every ten to the episodes.",
    "The longest of those episodes goes on for twenty-seven bars, more than a quarter of the "
    "piece, spun out of the falling semiquaver groups that end the subject. The tune arrives, "
    "goes away for a very long time, comes back — closer to how a ritornello works than to the "
    "usual subject-and-episode alternation. Two pedal points late on, four bars from bar 61 and "
    "six from bar 76, are the only places the bass stops moving.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 880 fugue F major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 880 fugue F major"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 880"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 880"),
  ]),

 dict(
  id="bwv881", file="wtc2f12.krn", bpm=72,
  title="Fugue in F minor", bwv="BWV 881", book="WTC II, No. 12", collection="wtc2",
  subject=dict(v=0, q0=0, q1=7.25),  # bars 0:1..4:1.75
  card="One stretto, at bar 72 of 85. Everything before it keeps the three voices politely out of "
       "each other's way.",
  blurb="An upbeat, a drop of a fifth, that note repeated three times, and then the subject "
        "dissolves into semiquavers. The voices stay clear of each other until bar 72, where two "
        "entries finally overlap — thirteen bars from the end.",
  history=[
    "An upbeat quaver, a fifth down, the same note three times, and then most of two bars of "
    "unbroken semiquavers: twenty-three notes over three and a half bars, and the second half of "
    "the subject is the part that matters. Those semiquavers go on to carry the rest of the "
    "piece. Six episodes take up three bars in every five and they are all made of the same "
    "running figure.",
    "The voices avoid each other for seventy-one bars. Then at bar 72 two entries come three bars "
    "apart, and since the subject is three and a bit bars long they overlap by roughly a beat — a "
    "stretto by the letter rather than by the ear. Apart from a short pedal at bar 50, that is "
    "the whole of the drama.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 881 fugue F minor"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 881"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 881"),
    perf("Edwin Fischer", "piano, the first complete recording", "Edwin Fischer Bach Well Tempered Clavier BWV 881"),
  ]),

 dict(
  id="bwv882", file="wtc2f13.krn", bpm=116,
  title="Fugue in F-sharp major", bwv="BWV 882", book="WTC II, No. 13", collection="wtc2",
  subject=dict(v=1, q0=0, q1=15),  # bars 0:1..4:1.5
  card="The subject stops dead for a crotchet one bar in, and still comes back note-for-note "
       "exact nine times in eleven.",
  blurb="Dotted crotchet, two semiquavers, one crotchet, then silence — the subject stops before "
        "it has properly started, and the rest belongs to it. Eleven entries, nine of them exact, "
        "with three recurring countersubjects riding along.",
  history=[
    "The subject stops almost as soon as it starts: a dotted upbeat, two semiquavers, a crotchet "
    "on the downbeat, then a crotchet of rest. That rest sits inside the subject rather than "
    "between statements, and it is there every time it returns. Twenty notes across not quite "
    "four alla breve bars, so this is a slow-moving tune by the standards of Book II, and every "
    "note of it registers.",
    "It enters in the middle voice, then the top, then the bass, and after that Bach hardly "
    "touches it — nine of the eleven statements come back exact, just transposed, and three lines "
    "recur with them often enough for the analysis to count them as countersubjects. The dotted "
    "figure and the alla breve tread are the gestures of a French overture, and the fugue keeps "
    "that ceremonial walk going for all 84 bars.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 882 fugue F sharp major"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 882 fugue"),
    perf("Bob van Asperen", "harpsichord", "van Asperen Bach Well Tempered Clavier BWV 882"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 882 fugue F sharp major"),
  ]),

 dict(
  id="bwv883", file="wtc2f14.krn", bpm=72,
  title="Fugue in F-sharp minor", bwv="BWV 883", book="WTC II, No. 14", collection="wtc2",
  card="Bach adds a second and third subject later; the map tracks only the first, so its "
       "episodes are not empty.",
  blurb="A triple fugue. The first subject is short, and it keeps starting a dotted crotchet off "
        "the beat so that it hangs over the next one and never sits square with the bar. Two more "
        "subjects arrive later, and the closing stretch runs all three at once. The map on this "
        "page follows subject one only.",
  history=[
    "Fifteen notes over two and a half bars, and three times inside them the subject starts a "
    "dotted crotchet off the beat and lets it hang over the next one — twice across a barline. So "
    "it pulls against the metre from the first entry. Nine statements in all. Then a second "
    "subject arrives, then a third, and the last part of the fugue runs all three together.",
    "Which is a problem for the analysis here: the detector follows subject one and knows nothing "
    "about the other two. So the eight episodes it marks, including one of nearly fifteen bars "
    "from bar 37, are not gaps in the argument — they are where the other subjects get introduced "
    "and worked out. The numbers printed next to this fugue are accurate and describe about a "
    "third of it.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 883 fugue F sharp minor"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 883 fugue F sharp minor"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Bach Well Tempered Clavier Book 2 BWV 883"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 883 fugue"),
  ]),

 dict(
  id="bwv884", file="wtc2f15.krn", bpm=92,
  title="Fugue in G major", bwv="BWV 884", book="WTC II, No. 15", collection="wtc2",
  subject=dict(v=0, q0=0.25, q1=8.5),  # bars 1:1.5..6:3
  card="Thirty-three unbroken semiquavers, six entries in seventy-two bars, and a nineteen-bar "
       "gap before the last.",
  blurb="The subject is one unbroken run of thirty-three semiquavers — broken chords falling and "
        "climbing back, six notes to a 3/8 bar. Six statements, seventy-two bars, and between the "
        "fifth and the sixth it disappears for nineteen and a half of them.",
  history=[
    "No rests worth the name. The subject is a single line of broken chords running five and a "
    "half bars without stopping, and the piece never stops moving underneath it either. Six "
    "statements in seventy-two bars, with the exposition alone taking twenty of them.",
    "The interesting gap is at the end. After the fifth entry the subject disappears for a "
    "stretch almost as long as the entire exposition, and from bar 56 the bass parks on D for "
    "three and a half bars — the only point in the fugue where anything stands still. Then the "
    "last entry comes back, and the whole thing is over in about seventy seconds.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 884 fugue G major"),
    perf("Pieter-Jan Belder", "harpsichord", "Belder Bach Well Tempered Clavier BWV 884"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 884 fugue G major"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 884 fugue G major"),
  ]),

 dict(
  id="bwv885", file="wtc2f16.krn", bpm=104,
  title="Fugue in G minor", bwv="BWV 885", book="WTC II, No. 16", collection="wtc2",
  card="All four strettos held back until the second half, then twelve bars at the end with no "
       "subject at all.",
  blurb="Four voices in a quick 3/4, sixteen entries, and Bach saves every overlap for later: the "
        "first stretto does not arrive until bar 45. The last statement finishes around bar 73 "
        "and the fugue plays out its final twelve bars without the subject anywhere.",
  history=[
    "The subject runs three and a half bars, which is why the exposition needs seventeen. Through "
    "the first half the entries come one after another, cleanly separated; from bar 45 onwards "
    "Bach starts overlapping them, and all four stretto pairs fall in that second half. Three "
    "countersubjects keep coming back around them. The sixteen entries sit on seven pitch levels, "
    "but five of them start on D and three on G.",
    "The longest stay away from home is fifteen bars of C minor, bars 50 to 65, and two of the "
    "four strettos happen inside it. After that the music turns back to G minor and the last "
    "entry lands at bar 69. Then nothing: the longest episode in the piece is the one it finishes "
    "on.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 885 fugue G minor Well Tempered Clavier"),
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 885 fugue G minor"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 885"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 885 fugue"),
  ]),

 dict(
  id="bwv886", file="wtc2f17.krn", bpm=76,
  title="Fugue in A-flat major", bwv="BWV 886", book="WTC II, No. 17", collection="wtc2",
  card="Bach reshapes the subject nearly every time: eight of the fifteen entries come back "
       "altered.",
  blurb="Twenty notes of semiquavers in under two bars, four voices in by bar 10, and after that "
        "almost nothing is repeated literally. Watch the middle: from bar 26 the harmony walks "
        "down the flat side of the key and takes a while to find its way back.",
  history=[
    "No countersubject recurs, so what surrounds the subject is different every time — and so, "
    "mostly, is the subject. Of fifteen entries only two are exact transpositions; five take the "
    "ordinary tonal adjustment and eight come back altered. The two strettos, at bars 16 and 41, "
    "are the only places where entries overlap at all.",
    "From bar 26 the music goes flatwards in two-bar steps: C minor, F minor, B-flat minor, "
    "E-flat minor. The key tracker then labels bars 44 to 47 D-flat minor, which is not a key "
    "anyone writes in — it would take eight flats — so that label is the tool's best fit rather "
    "than Bach's notation. Take it as a measure of how far out the harmony has gone before it "
    "turns for home.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 886 fugue A flat major"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 886 fugue A flat"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 886"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 886 fugue"),
  ]),

 dict(
  id="bwv887", file="wtc2f18.krn", bpm=92,
  title="Fugue in G-sharp minor", bwv="BWV 887", book="WTC II, No. 18", collection="wtc2",
  card="A double fugue, and the opening subject vanishes for 38 bars in the middle while the "
       "second one takes over.",
  blurb="At 143 bars this is the longest fugue in either book, and the subject you hear at the "
        "start is only half the story. Between bars 59 and 97 it disappears completely; that "
        "stretch belongs to a second subject, which the entry finder here does not track.",
  history=[
    "Three voices, 6/8, a four-bar subject, and only twelve entries in 143 bars. The first "
    "subject gets its exposition and a run of statements up to bar 59 and then stops. A second "
    "subject arrives and works through an exposition of its own. A pedal point at bar 93 sets up "
    "the return, and when the first subject comes back at bar 97 it has the second one for "
    "company; the two run together to the end.",
    "The entry finder only knows the subject it locates in the opening bars, so it marks bars 59 "
    "to 97 as a single 38-bar episode. It is not an episode. That is the cost of doing this "
    "automatically, and it lands on the most interesting stretch of the piece, so watch the roll "
    "there rather than the brackets.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 887 fugue G sharp minor"),
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Well Tempered Clavier BWV 887"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 887"),
    perf("Rosalyn Tureck", "piano", "Rosalyn Tureck Bach BWV 887 fugue"),
  ]),

 dict(
  id="bwv888", file="wtc2f19.krn", bpm=80,
  title="Fugue in A major", bwv="BWV 888", book="WTC II, No. 19", collection="wtc2",
  card="Out of A major by bar 3 and not back until bar 25; the home key gets seven bars out of "
       "29.",
  blurb="Ten entries, no stretto, no inversion, no recurring countersubject — about as plainly as "
        "Bach ever set a fugue out. What moves instead is the key, and the tonic gets only the "
        "first two bars and the last five.",
  history=[
    "Nineteen notes in a bar and a third, near-continuous semiquavers, and he never bends the "
    "shape: four entries are exact, six take the standard tonal answer, none are altered. The "
    "episodes are short, the longest two and a half bars, so a statement turns up every few bars "
    "from the first to the last. Nothing overlaps at any point.",
    "The interest is in the middle. After the exposition the fugue spends seven bars in C-sharp "
    "minor and seven in B minor, and the entries follow it out there — F-sharp, C-sharp, D — "
    "before it comes back. For the opposite case, open the A minor fugue next door: BWV 889 "
    "registers no change of key at all.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano", "Andras Schiff Bach BWV 888 fugue A major"),
    perf("Edwin Fischer", "piano", "Edwin Fischer Bach Well Tempered Clavier BWV 888"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier Book 2 BWV 888"),
    perf("Angela Hewitt", "piano", "Angela Hewitt Bach BWV 888 fugue A major"),
  ]),

 dict(
  id="bwv889", file="wtc2f20.krn", bpm=74,
  title="Fugue in A minor", bwv="BWV 889", book="WTC II, No. 20", collection="wtc2",
  card="The only fugue here whose key never officially changes: 28 bars, all of them A minor.",
  blurb="Eight notes make the whole subject — wide leaps, chromatic, almost nothing joining them "
        "up — and the fugue around it has 733. Everything that moves is in the other voices.",
  history=[
    "The subject takes a bar and three quarters to say eight notes, which leaves the semiquavers "
    "to the lines underneath and above it. Four of those lines recur often enough to count as "
    "countersubjects, so the company the subject keeps is steadier than the subject itself: only "
    "four of the eight entries come back exact. The eight are spread evenly through the 28 bars, "
    "none of them overlapping, and no episode reaches three bars.",
    "The key analysis returns one region: A minor, bar 1 to bar 28. Nothing else on this site "
    "does that. Part of it is the tool being coarse — there are entries on G and on B, so the "
    "music is plainly going somewhere — but most of it is the piece. The chromaticism is local, "
    "the cadences keep landing back on A, and 28 bars is not long enough to properly leave.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 889 fugue A minor"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 889 fugue A minor"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 889"),
    perf("Evgeni Koroliov", "piano", "Koroliov Bach Well Tempered Clavier BWV 889 fugue"),
  ]),

 dict(
  id="bwv890", file="wtc2f21.krn", bpm=104,
  title="Fugue in B-flat major", bwv="BWV 890", book="WTC II, No. 21", collection="wtc2",
  card="Ten entries in 93 bars, and more than half of it is episode rather than subject.",
  blurb="A long, unhurried 3/4 built on a subject that takes nearly four bars to finish, so it "
        "can only be stated ten times in 93 bars. The gaps between statements add up to more of "
        "the piece than the statements do.",
  history=[
    "The length of the subject sets everything else: 24 notes over almost four bars, an "
    "exposition that runs to bar 17, and nine episodes that between them take about fifty of the "
    "93 bars. Two of those are long — ten and a half bars from bar 67, then almost twelve to "
    "close after the final entry. No countersubject recurs, so the episodes are not built out of "
    "a fixed companion line.",
    "For 41 bars the harmony sits still; everything up to bar 42 is B-flat major. Then it moves "
    "four times in twenty-six bars — G minor, E-flat, C minor — and is home again for the last "
    "quarter. That is a fugue you can lose your place in, which is a decent argument for leaving "
    "the entry brackets switched on.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, WTC_WIKI, KERN_WTC],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 890 fugue B flat major"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 890 fugue B flat"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 890"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 890 fugue B flat major"),
  ]),

 dict(
  id="bwv891", file="wtc2f22.krn", bpm=126,
  title="Fugue in B-flat minor", bwv="BWV 891", book="WTC II, No. 22", collection="wtc2",
  forms=("I",),
  card="The only fugue here in 3/2, and its twenty-one entries split almost evenly between "
       "upright and upside down.",
  blurb="Four voices in 3/2, and from bar 27 on Bach runs the subject against its own inversion. "
        "Eleven of the twenty-one entries stand upright and ten are turned over.",
  history=[
    "The exposition takes twenty-one bars, which is long, and after that the piece never really "
    "relaxes. Eleven entries keep the subject as it stands, ten invert it, and at eight points a "
    "statement begins before the one before it has finished. Thirteen episodes, none of them "
    "longer than six bars. There is very little here that is not the subject in one form or "
    "another.",
    "Three minims to a bar gives a four-bar subject enough room to overlap with itself without "
    "the texture clotting. The hard part for a listener is not the speed. It is recognising the "
    "inverted form as inverted while it goes past, and that is what the entry brackets are for.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in B-flat minor, BWV 891",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B-flat_minor,_BWV_891"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 891 fugue B flat minor"),
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 891 fugue"),
    perf("Kenneth Gilbert", "harpsichord", "Kenneth Gilbert Bach Well Tempered Clavier Book 2 BWV 891"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 891 fugue B flat minor"),
  ]),

 dict(
  id="bwv892", file="wtc2f23.krn", bpm=112,
  title="Fugue in B major", bwv="BWV 892", book="WTC II, No. 23", collection="wtc2",
  subject=dict(v=3, q0=0, q1=16),  # bars 1:1..5:1
  card="Bass first and building upward, on a subject of eleven notes in four bars — most entries "
       "never state all of it.",
  blurb="Bach starts at the bottom and stacks the voices upward. The subject is eleven notes "
        "spread over four bars, and after the exposition he stops stating it whole: ten of the "
        "fourteen entries are partial, the highest share of any fugue here.",
  history=[
    "Bass, tenor, alto, soprano. The exposition builds from the floor and takes eighteen bars to "
    "finish, with a pedal underneath the last of it held for five and a half bars. Three "
    "countersubjects come back through the piece. No stretto anywhere — instead of crowding the "
    "entries Bach separates them, and the episode starting at bar 64 runs eleven bars before the "
    "next one arrives.",
    "Ten of the fourteen entries are marked partial, which is the analyser admitting it only "
    "matched part of the subject. Take that as information rather than as an error. From bar 19 "
    "on, not one entry states all eleven notes, so the brackets get visibly shorter as the fugue "
    "goes on.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in B major, BWV 892",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B_major,_BWV_892"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 892 fugue B major"),
    perf("Masaaki Suzuki", "harpsichord", "Masaaki Suzuki Bach Well Tempered Clavier Book 2 BWV 892"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach BWV 892 fugue"),
    perf("Sviatoslav Richter", "piano", "Richter Bach BWV 892 fugue B major"),
  ]),

 dict(
  id="bwv893", file="wtc2f24.krn", bpm=104,
  title="Fugue in B minor", bwv="BWV 893", book="WTC II, No. 24", collection="wtc2",
  card="Last fugue in Book II, and it ends the collection in a hurry: three voices, 3/8, nine "
       "entries in a hundred bars.",
  blurb="The piece that closes Book II, and it closes it fast. Three voices in 3/8, only nine "
        "statements of the subject in a hundred bars, and the last thirteen have none at all.",
  history=[
    "The subject runs nearly six bars, which in 3/8 is not much clock time but is a lot of fugue: "
    "nine statements and eight episodes fill the whole hundred bars. Six of the nine are altered "
    "rather than transposed intact — Bach keeps bending intervals inside the subject to fit the "
    "harmony he happens to be in. The last entry starts at bar 82 and is finished by bar 88; the "
    "thirteen bars after it never touch the subject again.",
    "Book I finishes with a slow, chromatic, four-voice B minor fugue. Book II finishes with this "
    "one: quick, three voices, in dance metre. They make an odd pair of bookends, and whether the "
    "contrast was deliberate is not something the sources settle.",
    WTC2_CONTEXT,
  ],
  links=[WTC2_SCORE, ("Prelude and Fugue in B minor, BWV 893",
         "https://en.wikipedia.org/wiki/Prelude_and_Fugue_in_B_minor,_BWV_893"), WTC_WIKI, KERN_WTC],
  performances=[
    perf("András Schiff", "piano, ECM", "Andras Schiff Bach BWV 893 fugue B minor"),
    perf("Edwin Fischer", "piano", "Edwin Fischer Bach Well Tempered Clavier BWV 893"),
    perf("Richard Egarr", "harpsichord", "Richard Egarr Bach Well Tempered Clavier Book 2 BWV 893"),
    perf("Glenn Gould", "piano", "Glenn Gould Bach BWV 893 fugue B minor"),
  ]),

 dict(
  id="bwv1080-1", file="artfugue-001.krn", bpm=76, modernClefs=True,
  title="Contrapunctus I", bwv="BWV 1080/1", book="The Art of Fugue", collection="aof",
  card="One subject, four voices, no tricks. Everything else in the cycle is a variation on this "
       "one.",
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

 dict(
  id="bwv1080-2", file="artfugue-002.krn", bpm=96,
  title="Contrapunctus II", bwv="BWV 1080/2", book="The Art of Fugue", collection="aof", modernClefs=True,
  card="Contrapunctus I's subject again, this time in dotted rhythm, and the dotting spreads to "
       "every other voice.",
  blurb="The same D minor subject as Contrapunctus I, now with a dotted tail. The pitches are the "
        "ones you already know; what has changed is the rhythm, and it does not stay inside the "
        "subject for long.",
  history=[
    "Bass, tenor, alto, soprano, four bars apart each time, so the exposition is a staircase; the "
    "map finds four places where an entry begins fractionally before the previous one lets go, "
    "three of them inside that staircase. Ten entries in 84 bars, and the two long episodes, "
    "twelve bars from bar 19 and thirteen from bar 66, do most of the work between them. A pedal "
    "holds for three bars just before the final entry at bar 79.",
    "Contrapuncti I to IV are the four simple fugues, the plainest group in the collection: two "
    "on the subject upright, two on it inverted. This is the second of the upright pair. The "
    "dotted style is the one Bach used for French overtures, and that is how the movement is "
    "usually described — an ordinary fugue in fancy dress.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Evgeni Koroliov", "piano", "Koroliov Art of Fugue Contrapunctus 2"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Art of Fugue Contrapunctus 2 harpsichord"),
    perf("Glenn Gould", "organ", "Glenn Gould Art of Fugue Contrapunctus 2 organ"),
    perf("Phantasm", "viol consort", "Phantasm Bach Art of Fugue Contrapunctus 2"),
  ]),

 dict(
  id="bwv1080-3", file="artfugue-003.krn", bpm=84,
  title="Contrapunctus III", bwv="BWV 1080/3", book="The Art of Fugue", collection="aof", modernClefs=True,
  subject=dict(v=2, q0=0, q1=14.5),  # bars 1:1..4:2.25
  card="The subject upside down, chromatic lines around it, and five countersubjects that keep "
       "coming back.",
  blurb="The principal subject arrives upside down, and the lines around it are chromatic enough "
        "that the harmony keeps sliding out from under you. Five countersubjects come back "
        "through the piece.",
  history=[
    "Tenor first, then alto, soprano, bass. Eight entries in 72 bars, fewer than any of the other "
    "three simple fugues, and after the exposition the music runs from bar 19 to bar 43 — a third "
    "of its length — without a complete statement anywhere. It ends over a pedal held for the "
    "last three bars.",
    "The entry brackets label every statement here as prime, and that is the map being literal: "
    "it takes each movement's own opening as its reference shape, so it has no way of knowing "
    "that this shape is Contrapunctus I's subject turned over. Open the two side by side and "
    "compare the contours.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Davitt Moroney", "harpsichord", "Davitt Moroney Art of Fugue Contrapunctus 3"),
    perf("Pierre-Laurent Aimard", "piano, DG", "Aimard Art of Fugue Contrapunctus 3"),
    perf("Helmut Walcha", "organ", "Helmut Walcha Art of Fugue Contrapunctus 3 organ"),
    perf("Emerson String Quartet", "string quartet", "Emerson Quartet Art of Fugue Contrapunctus 3"),
  ]),

 dict(
  id="bwv1080-4", file="artfugue-004.krn", bpm=112,
  title="Contrapunctus IV", bwv="BWV 1080/4", book="The Art of Fugue", collection="aof", modernClefs=True,
  subject=dict(v=0, q0=0, q1=14.5),  # bars 1:1..4:2.25
  card="138 bars on the inverted subject, with a sixty-four-bar stretch in the middle and no "
       "complete entry in it.",
  blurb="The longest of the four simple fugues, and the one that spends least of its length on "
        "the subject. Between bar 43 and bar 107 the map finds no complete statement at all — "
        "sixty-four bars, the longest episode of any fugue here.",
  history=[
    "Soprano, alto, tenor, bass, straight down through the voices, with the exposition done by "
    "bar 19. Twelve entries in all across 138 bars, thinner on the ground than anything else in "
    "the first four contrapuncti. When the entries do come back they come close together: two of "
    "them start a crotchet apart at bar 107. There are pedal points from the middle of bar 35 and "
    "from bar 135, four bars each.",
    "Contrapunctus IV is absent from the Berlin autograph of the collection and appears only in "
    "the printed edition of 1751, so it is usually taken to be a later addition. The other three "
    "state and restate; this one spends most of its length on what can be built between the "
    "statements.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Tatiana Nikolayeva", "piano", "Nikolayeva Bach Art of Fugue Contrapunctus 4"),
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Bach Art of Fugue Contrapunctus 4"),
    perf("Glenn Gould", "organ", "Glenn Gould Art of Fugue Contrapunctus 4 organ"),
    perf("Akademie für Alte Musik Berlin", "instrumental ensemble", "Akademie fur Alte Musik Berlin Art of Fugue Contrapunctus 4"),
  ]),

 dict(
  id="bwv1080-5", file="artfugue-005.krn", bpm=108,
  title="Contrapunctus V", bwv="BWV 1080/5", book="The Art of Fugue", collection="aof", modernClefs=True,
  forms=("I",),
  card="Eleven statements the right way up, eleven upside down: Bach answers his own subject with "
       "its inversion.",
  blurb="A counter-fugue: the answer inverts the subject instead of copying it, and across 90 "
        "bars the two forms come out dead even at eleven each. Turn the entry brackets on from "
        "bar 33, where they start arriving in pairs.",
  history=[
    "The exposition drops an entry every three bars — 1, 4, 7, 10 — and the next four keep the "
    "same spacing, at 17, 20, 23 and 26. Of 22 statements, eleven run upright and eleven "
    "inverted, and the analysis finds 13 places where one begins before the last has finished. "
    "From bar 33 on they mostly come in couples a bar or half a bar apart: 33 and 33½, 41 and "
    "41½, 69 and 70, 77 and 78. The final two start on the same beat. It ends over a pedal, in D "
    "major.",
    "V, VI and VII are the counter-fugues of the set — VI does the same thing in French dotted "
    "rhythm, VII stacks the subject against itself at three speeds at once. This is the plain "
    "member of the three, which mostly means you can follow it. The *kern* edition the site reads "
    "files it under a different heading altogether, stretto fugue, and with 13 overlapping pairs "
    "in 90 bars that is fair enough.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Evgeni Koroliov", "piano, Tacet", "Koroliov Art of Fugue Contrapunctus 5"),
    perf("Glenn Gould", "organ, 1962", "Glenn Gould Art of Fugue Contrapunctus 5 organ"),
    perf("Davitt Moroney", "harpsichord", "Davitt Moroney Art of Fugue Contrapunctus 5"),
    perf("Phantasm", "viol consort", "Phantasm Bach Art of Fugue Contrapunctus 5"),
  ]),

 dict(
  id="bwv1080-8", file="artfugue-008.krn", bpm=120,
  title="Contrapunctus VIII", bwv="BWV 1080/8", book="The Art of Fugue", collection="aof", modernClefs=True,
  subject=dict(v=1, q0=2, q1=17),  # bars 1:2..5:1.5
  card="Three voices, three subjects, 188 bars, and one 43-bar stretch where the entry finder has "
       "nothing to draw.",
  blurb="A triple fugue, and the only movement from the collection on this site that is not in "
        "four voices. The site tracks its first subject, so the long empty runs in the map are "
        "where the other two are doing the work.",
  history=[
    "The first subject enters in the alto, then the bass, then the soprano, five bars apart, and "
    "the exposition is over by bar 15. Nineteen statements in all, never inverted, and exactly "
    "once does an entry overlap another. One stretto in 188 bars. Bach spends the rest of the "
    "piece on what three subjects do when you put them together.",
    "It is the longest fugue on this site that actually finishes, and it also shows up the limit "
    "of automatic entry-finding: between bar 71 and bar 114 the first subject is simply absent, "
    "so the map draws a single 43-bar episode across the middle of the piece. The analysis is not "
    "wrong; it is answering a question with one subject in it. Contrapunctus XI is this fugue "
    "again in four voices with the subjects upside down, and the two are worth opening side by "
    "side.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Angela Hewitt", "piano, Hyperion", "Angela Hewitt Art of Fugue Contrapunctus 8"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Art of Fugue Contrapunctus 8"),
    perf("Helmut Walcha", "organ", "Helmut Walcha Art of Fugue Contrapunctus 8 organ"),
    perf("Keller Quartett", "string quartet, ECM", "Keller Quartett Bach Art of Fugue Contrapunctus 8"),
  ]),

 dict(
  id="bwv1080-9", file="artfugue-009.krn", bpm=168,
  title="Contrapunctus IX", bwv="BWV 1080/9", book="The Art of Fugue", collection="aof", modernClefs=True,
  card="Eleven entries and not one overlaps another; the trick here is invertible counterpoint at "
       "the twelfth, not stretto.",
  blurb="*Alla Duodecima* — the two subjects are written so that either can be shifted a twelfth "
        "against the other and still work. The new one runs in quavers, the collection's D minor "
        "subject moves against it in long notes, and across 130 bars no entry ever overlaps "
        "another.",
  history=[
    "The subject here is new: nearly seven bars long, 46 notes, a couple of held ones and then a "
    "long stream of quavers. Entries arrive seven bars apart — alto, soprano, bass, tenor — so "
    "the exposition alone runs to bar 29. Eleven statements, none inverted, no strettos anywhere. "
    "You hear every one of them whole, which is not something the rest of the collection often "
    "lets you do.",
    "Invertible counterpoint at the twelfth is a harder constraint than it sounds. Invert two "
    "lines at the octave and a fifth turns into a fourth; invert them at the twelfth and a sixth "
    "turns into a seventh, so every sixth between the subjects has to be handled as a dissonance "
    "would be. Bach titled the movement after the constraint and then wrote the breeziest music "
    "in the whole book.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Glenn Gould", "organ, 1962", "Glenn Gould Art of Fugue Contrapunctus 9 organ"),
    perf("Pierre-Laurent Aimard", "piano, DG", "Aimard Art of Fugue Contrapunctus 9"),
    perf("Masaaki Suzuki", "harpsichord, BIS", "Masaaki Suzuki Art of Fugue Contrapunctus 9"),
    perf("Musica Antiqua Köln", "instrumental ensemble", "Musica Antiqua Koln Art of Fugue Contrapunctus 9"),
  ]),

 dict(
  id="bwv1080-10", file="artfugue-010.krn", bpm=132,
  title="Contrapunctus X", bwv="BWV 1080/10", book="The Art of Fugue", collection="aof", modernClefs=True,
  forms=("I",),
  card="The soprano waits 66 bars of 120 before it gets the subject; then, three times, two "
       "voices take it together.",
  blurb="*Alla Decima* — the subject is built to run against itself a tenth away, and the last "
        "third of the piece cashes that in: three times over, two voices start it on the same "
        "beat.",
  history=[
    "Alto, tenor and bass pass the subject round for more than half the piece before the soprano "
    "is allowed near it, at bar 66 of 120. That is why the map holds the exposition open until "
    "bar 69 — the analysis is waiting for the top voice, and Bach keeps it waiting. Thirteen "
    "statements, two of them inverted, and at bars 85, 103 and 115 they arrive two at a time.",
    "Counterpoint at the tenth costs something specific: invert two lines at the tenth and every "
    "third between them becomes an octave, so parallel thirds, the easiest sweetener in tonal "
    "music, are off the table for the whole movement. An earlier and shorter version of the fugue "
    "survives as well. It begins partway in, without the opening stretch of entries; that first "
    "section was added later.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Zhu Xiao-Mei", "piano", "Zhu Xiao-Mei Art of Fugue Contrapunctus 10"),
    perf("Lionel Rogg", "organ", "Lionel Rogg Art of Fugue Contrapunctus 10 organ"),
    perf("Ton Koopman and Tini Mathot", "two harpsichords", "Koopman Mathot Art of Fugue Contrapunctus 10"),
    perf("Fretwork", "viol consort", "Fretwork Bach Art of Fugue Contrapunctus 10"),
  ]),

 dict(
  id="bwv1080-11", file="artfugue-011.krn", bpm=116,
  title="Contrapunctus XI", bwv="BWV 1080/11", book="The Art of Fugue", collection="aof", modernClefs=True,
  forms=("I",),
  card="Contrapunctus VIII inverted and given a fourth voice: 3,034 notes, more than any other "
       "fugue on the site.",
  blurb="The three subjects of Contrapunctus VIII, turned upside down and rewritten for four "
        "voices. 184 bars and 3,034 notes, the most of anything on this site, with the exposition "
        "finished inside the first 17.",
  history=[
    "Alto, soprano, bass, tenor, an entry every four bars, and the subject has been through all "
    "four voices by bar 17. Then it vanishes for 44 bars while the second subject is set up, "
    "which is the longest gap in the piece and the most conspicuous thing on its map. Seventeen "
    "statements in all, five of them inverted; at bars 158 and 164 two voices start together, and "
    "two more entries follow before the end.",
    "Bach wrote VIII in three voices with the subjects the right way up, and this one in four "
    "with them inverted. Putting the two maps next to each other is as close as the collection "
    "comes to showing its working. It is still a hard listen the first time: 184 bars, a shade "
    "shorter than VIII and a good deal denser, with the subject you are following only one of the "
    "three at work.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Pierre-Laurent Aimard", "piano, DG", "Aimard Art of Fugue Contrapunctus 11"),
    perf("Gustav Leonhardt", "harpsichord", "Leonhardt Art of Fugue Contrapunctus 11"),
    perf("Helmut Walcha", "organ", "Helmut Walcha Art of Fugue Contrapunctus 11 organ"),
    perf("Emerson String Quartet", "string quartet", "Emerson Quartet Art of Fugue Contrapunctus 11"),
  ]),

 dict(
  id="bwv1080-14", file="artfugue-019.krn", bpm=96,
  title="Contrapunctus XIV", bwv="BWV 1080/14", book="The Art of Fugue", collection="aof", modernClefs=True,
  subject=dict(v=3, q0=2, q1=22),  # bars 1:3..6:3
  forms=("I",),
  card="Breaks off in bar 239, mid-phrase, and the D minor subject the whole collection is built "
       "on never turns up.",
  blurb="The unfinished one. 239 bars, the longest fugue on this site, and it stops dead. Three "
        "subjects get worked out, the third of them spelling B-A-C-H, and then the manuscript "
        "ends.",
  history=[
    "It builds from the bottom — bass, tenor, alto, soprano, five bars apart — and the exposition "
    "is done by bar 22. The first subject is heard 26 times in all, 22 upright and four inverted, "
    "with eight overlaps. The two long gaps, bars 111 to 148 and 189 to 234, are the second and "
    "third subjects taking their turns; the third of them spells B-A-C-H in German note names, "
    "which is B flat, A, C, B natural. Four bars after the last entry, it stops.",
    "C. P. E. Bach wrote on the manuscript that his father died while working on the fugue in "
    "which the name BACH appears. It is a good story and it is probably not true — the "
    "handwriting places the fragment earlier than the final illness. What is true is that nobody "
    "knows how it was meant to go. The collection's own D minor subject never appears in the 239 "
    "bars we have, but it fits against these three in invertible counterpoint, and completions "
    "have been built on that ever since.",
    AOF_CONTEXT,
  ],
  links=[AOF_SCORE, AOF_WIKI, KERN_AOF],
  performances=[
    perf("Evgeni Koroliov", "piano, Tacet", "Koroliov Art of Fugue Contrapunctus 14 unfinished fugue"),
    perf("Davitt Moroney", "harpsichord", "Davitt Moroney Art of Fugue unfinished fugue Contrapunctus 14"),
    perf("Helmut Walcha", "organ", "Helmut Walcha Art of Fugue final unfinished fugue organ"),
    perf("Keller Quartett", "string quartet, ECM", "Keller Quartett Bach Art of Fugue Contrapunctus 14"),
  ]),
]

VOICE_NAMES = {
  2: ["Upper", "Lower"],
  3: ["Soprano", "Alto", "Bass"],
  4: ["Soprano", "Alto", "Tenor", "Bass"],
  5: ["Soprano", "Mezzo", "Alto", "Tenor", "Bass"],
}
