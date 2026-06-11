#!/usr/bin/env python3
"""Build workshop-extras.pptx — the authored Session 1 slides that
complement the three decks extracted from the COMP63342 lectures
(see slides/README.md). Session 2's authored slides live in
session2/01-session2-hands-on.pptx, built by build_session2.py.

The canonical content lives in workshop-extras.md; this script renders the
same content as a native, editable PowerPoint file.

Usage:  python3 -m venv venv && venv/bin/pip install python-pptx
        venv/bin/python build_extras.py
"""
from pptx_helpers import new_presentation, add_slide, add_body, add_table

prs = new_presentation()

s = add_slide(prs, "Formal Verification Workshop", lead=True)
add_body(s, ["Session 1 — Fundamentals and Real-World Applications",
             "18:00 – 21:00",
             "Built on the COMP63342 Software Security course "
             "(University of Manchester)"], top=3.9, size=26)

s = add_slide(prs, "Tonight")
add_table(s, [
    ["18:00", "Welcome + a question for you"],
    ["18:10", "Why software fails"],
    ["18:35", "Exercise 1: spot the bug"],
    ["18:50", "Testing vs. verification"],
    ["19:15", "Break"],
    ["19:25", "From programs to formulas: SAT, SMT"],
    ["19:50", "Bounded model checking"],
    ["20:15", "Exercise 2: predict the verdict"],
    ["20:30", "Who uses this in the real world?"],
    ["20:50", "Quiz + what to install for Session 2"],
], top=1.5, size=20, col_widths=[1.6, 10.1])

s = add_slide(prs, "Icebreaker")
add_body(s, ["Name a software failure that made the news.",
             "Any failure. Any decade. Shout it out / drop it in the poll."],
         top=2.6, size=30)

s = add_slide(prs, "Exercise 1 — Spot the Bug (15 min)")
add_body(s, [
    "In pairs, 7 minutes, on the handout:",
    ("int *zPtr;", 0, True),
    ("int *aPtr = NULL;", 0, True),
    ("void *sPtr = NULL;", 0, True),
    ("int number, i;", 0, True),
    ("int z[5] = {1, 2, 3, 4, 5};", 0, True),
    ("sPtr = z;   ++zPtr;   number = zPtr;", 0, True),
    ("number = *zPtr[2];   number = *sPtr;   ++z;", 0, True),
    "For each bug: WHAT is wrong, and what could happen at runtime?",
    "There are at least six. Debrief: one bug per pair.",
])

s = add_slide(prs, "Where does your technique sit?")
add_table(s, [
    ["", "Complete (no false alarms)", "Incomplete"],
    ["Sound (no missed bugs)", "the dream", "abstract interpretation"],
    ["Unsound", "bounded model checking*", "testing, code review"],
], top=1.7, size=20, col_widths=[3.4, 4.4, 3.9])
add_body(s, ["* sound up to its bound — tonight's central fine print",
             "Think–pair–share (5 min): place testing, code review, compiler "
             "warnings, and “prove it with maths” on this grid. "
             "Defend your placement."], top=4.1, size=22)

s = add_slide(prs, "Exercise 2 — Predict the Verdict (15 min)")
add_body(s, [
    "Groups of 3–4. Three short C programs on the handout "
    "(predict1.c, predict2.c, predict3.c).",
    "For each program, write down BEFORE we run anything:",
    ("Will the model checker say VERIFICATION FAILED or SUCCESSFUL?", 1),
    ("If FAILED — which line is the culprit?", 1),
    "Then we run ESBMC live and settle every bet.",
])

s = add_slide(prs, "Who uses this? — Model checking")
add_body(s, [
    "Amazon Web Services — CBMC proves memory safety of the TLS library "
    "s2n; bounded proofs run in CI on every commit",
    "ESBMC / CBMC — the tools from tonight's demos; compete yearly in "
    "SV-COMP on tens of thousands of benchmarks",
    "The counterexample you saw for getpassword.c is the same artefact "
    "AWS engineers read when a proof fails",
])

s = add_slide(prs, "Who uses this? — Symbolic execution & fuzzing")
add_body(s, [
    "KLEE found 56 bugs in GNU coreutils — code tested for 15 years",
    "Microsoft SAGE fuzzed Windows file parsers with symbolic execution; "
    "credited with finding 1/3 of all Win7 file-parsing bugs",
    "AFL / OSS-Fuzz — Google fuzzes ~1,000 open-source projects "
    "continuously; tens of thousands of bugs found",
    "The pragmatic cousin of verification: no proofs, ruthless "
    "effectiveness",
])

s = add_slide(prs, "Who uses this? — Proofs all the way up")
add_body(s, [
    "Astrée (abstract interpretation) proved absence of runtime errors "
    "in Airbus A380 fly-by-wire control code",
    "seL4 — an OS microkernel with a machine-checked proof of functional "
    "correctness",
    "CompCert — a C compiler with a proof that compilation preserves "
    "semantics; fuzzers find zero wrong-code bugs in it",
])

s = add_slide(prs, "Discussion")
add_body(s, [
    "If verification can prove the absence of bugs…",
    "why isn't all software verified?",
    "(Let's collect reasons — then I'll tell you which ones the industry "
    "actually cites.)",
], top=2.4, size=28)

s = add_slide(prs, "Closing quiz")
add_body(s, [
    "1. A tool that never raises a false alarm is called …?",
    "2. ESBMC returns UNSAT for C ∧ ¬P at --unwind 10. "
    "What do we know?",
    "3. What's inside a counterexample?",
    "4. Which technique proved the A380 flight-control code free of "
    "runtime errors?",
    "5. Why can't testing prove the getPassword program safe?",
], size=24)

s = add_slide(prs, "Before Session 2 — 10 minutes of homework")
add_body(s, [
    "Follow handouts/setup.md in the repo:",
    ("1.  pip install z3-solver", 0, True),
    ("2.  download ESBMC: github.com/esbmc/esbmc/releases", 0, True),
    ("3.  smoke test:  esbmc labs/lab4/float.c", 0, True),
    ("    → should print VERIFICATION FAILED "
     "(yes, failed — that's the point)", 0, True),
    "Can't make it work? Come at 17:45 — we'll fix it together.",
])

prs.save("workshop-extras.pptx")
print(f"saved workshop-extras.pptx with {len(prs.slides)} slides")
