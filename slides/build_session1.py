#!/usr/bin/env python3
"""Build session1/01-session1-fundamentals.pptx — the single authored deck
for Session 1, in exact run order (no deck-switching during the evening).
Designed to lay every foundation Session 2's labs assume: the negation
trick, counterexample reading, --unwind verdict semantics, the
nondet/assume/assert toolkit, and the concurrency/floating-point hooks.

The same content lives in session1/01-session1-fundamentals.md (Marp).

Usage:  python3 -m venv venv && venv/bin/pip install python-pptx
        venv/bin/python build_session1.py
"""
from pptx_helpers import (new_presentation, add_slide, add_body, add_table,
                          add_chart, add_flow)

prs = new_presentation()

# ---------------------------------------------------------------- welcome
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

# ------------------------------------------------ why software fails 18:10
s = add_slide(prs, "When software fails: two classics")
add_body(s, [
    "Ariane 5, 1996 — a 64-bit float squeezed into a 16-bit integer. "
    "The conversion overflowed; the rocket self-destructed 40 seconds "
    "after lift-off.",
    ("The code was reused from Ariane 4, where that value "
     "“could never get that large”.", 1),
    "Therac-25, 1985–87 — a race condition between operator keystrokes "
    "and the radiation beam controller. Six massive overdoses, "
    "several fatal.",
    ("Sequential testing never showed it: the bug needed precise, "
     "fast operator timing.", 1),
    "",
    "An integer overflow and a race condition. Hold that thought — "
    "you will hunt both bug classes yourself in Session 2.",
])

s = add_slide(prs, "A password check in 11 lines of C")
add_body(s, [
    ("char *gets(char *s);  /* removed from C11 — unsafe by design */",
     0, True),
    ("", 0, True),
    ("int getPassword(void)", 0, True),
    ("{", 0, True),
    ("  char buf[4];", 0, True),
    ("  gets(buf);", 0, True),
    ("  return strcmp(buf, \"SMT\");", 0, True),
    ("}", 0, True),
    ("", 0, True),
    ("/* main: 0 from getPassword => \"Access Granted\" */", 0, True),
    "",
    "session1-demos/getpassword.c — what happens if you type more "
    "than three characters?",
], size=24)

s = add_slide(prs, "What gets() does to the stack")
add_table(s, [
    ["The stack frame", ""],
    ["return address", "where main continues after the call"],
    ["saved registers", "the caller's state"],
    ["buf[0] … buf[3]", "gets(buf) starts writing here…"],
], top=1.6, size=20, col_widths=[4.2, 7.5])
add_body(s, [
    "gets() never checks the size: byte 5, 6, 7… keep overwriting "
    "whatever lies above the buffer — up to the return address.",
    "An attacker chooses those bytes. That is not a crash; that is "
    "control of your program.",
    "Could a test suite find this? Only if someone thinks to type the "
    "right garbage.",
], top=3.6, size=22)

s = add_slide(prs, "Let's ask a tool instead of an attacker")
add_body(s, [
    ("$ esbmc getpassword.c --unwind 8", 0, True),
    ("", 0, True),
    ("[Counterexample]", 0, True),
    ("...", 0, True),
    ("Violated property:", 0, True),
    ("  dereference failure: array bounds violated", 0, True),
    ("  CWE: CWE-787 (out-of-bounds write)", 0, True),
    ("", 0, True),
    ("VERIFICATION FAILED", 0, True),
    "",
    "No input was typed. No exploit was written. The tool proved the "
    "overflow is reachable — and printed the input that triggers it.",
], size=22)

s = add_slide(prs, "Safety and security: two sides of one coin")
add_body(s, [
    "Safety — the system must not harm the world "
    "(Therac-25, Ariane 5).",
    "Security — the world must not harm the system "
    "(getPassword).",
    "Same root cause tonight: the program reaches a state it was "
    "never meant to reach.",
], top=1.5, size=24)
add_table(s, [
    ["Security goal", "Meaning", "getPassword breaks it?"],
    ["Confidentiality", "no unauthorised reading", "yes — secrets behind "
     "the check"],
    ["Integrity", "no unauthorised writing", "yes — the stack itself"],
    ["Availability", "service stays up", "crash = denial of service"],
], top=4.0, size=18, col_widths=[2.8, 4.2, 4.7])

s = add_slide(prs, "Memory safety: the bug class that won't die")
add_body(s, [
    "C trusts you completely: every array index, every pointer "
    "dereference, every free() is your problem.",
    "Get it wrong and the result is undefined behaviour — the program "
    "may crash, corrupt data, or look perfectly fine until it ships.",
    "“Looks fine in testing” is exactly what undefined behaviour does "
    "best.",
    "",
    "How big is the problem? Let's look at the data.",
], top=1.8, size=24)

s = add_slide(prs, "Vulnerabilities keep climbing")
add_chart(s, "line",
          ["2016", "2017", "2018", "2019", "2020",
           "2021", "2022", "2023", "2024", "2025"],
          "CVE records published",
          [6447, 14645, 16511, 17305, 18325,
           20153, 25084, 29066, 40009, 48185],
          top=1.5, height=4.9)
add_body(s, ["More than 48,000 new CVEs in 2025 — almost tripled since "
             "2020.   Sources: nvd.nist.gov · cve.org (2026)"],
         top=6.6, size=18)

# Official 2025 CWE Top 25 (cwe.mitre.org, Dec 2025): top 10 by score.
# Reversed for the bar chart, which plots the first category at the bottom.
CWE_TOP10 = [
    ("1. Cross-site Scripting (CWE-79)", 60.38),
    ("2. SQL Injection (CWE-89)", 28.72),
    ("3. Cross-Site Request Forgery (CWE-352)", 13.64),
    ("4. Missing Authorization (CWE-862)", 13.28),
    ("5. Out-of-bounds Write (CWE-787)", 12.68),
    ("6. Path Traversal (CWE-22)", 8.99),
    ("7. Use After Free (CWE-416)", 8.47),
    ("8. Out-of-bounds Read (CWE-125)", 7.88),
    ("9. OS Command Injection (CWE-78)", 7.85),
    ("10. Code Injection (CWE-94)", 7.57),
]

s = add_slide(prs, "And the same weaknesses top the chart")
add_chart(s, "bar",
          [name for name, _ in reversed(CWE_TOP10)],
          "2025 CWE Top 25 score",
          [v for _, v in reversed(CWE_TOP10)],
          left=2.0, top=1.4, width=10.6, height=5.0)
add_body(s, ["Memory safety still everywhere: out-of-bounds write #5, "
             "use-after-free #7, out-of-bounds read #8 — plus classic "
             "buffer overflow at #11.   Source: cwe.mitre.org/top25 "
             "(Dec 2025)"], top=6.5, size=16)

s = add_slide(prs, "Industry's conclusion")
add_body(s, [
    "~70% of the vulnerabilities Microsoft patches every year are "
    "memory-safety bugs (MSRC, 2019) — a figure that has barely moved "
    "in a decade.",
    "Every one of those products shipped with a serious test suite. "
    "Testing did not stop them.",
    "",
    "Two industry answers:",
    ("memory-safe languages for new code (Rust, …)", 1),
    ("proving the C/C++ we already run correct — formal verification. "
     "Tonight is about this one.", 1),
], top=1.8, size=24)

# ------------------------------------------------------- exercise 1 18:35
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

# ------------------------------------- testing vs. verification 18:50
s = add_slide(prs, "Verification vs. validation")
add_body(s, [
    "Validation — are we building the right thing? "
    "(ask the users)",
    "Verification — are we building the thing right? "
    "(ask the specification)",
    "",
    "Tonight is verification: given a program and a property, does "
    "every execution satisfy the property?",
], top=2.0, size=26)

s = add_slide(prs, "Why testing cannot prove absence")
add_body(s, [
    "One int input = 2³² cases. At a billion tests per second: "
    "about 4 seconds. Fine.",
    "Two int inputs = 2⁶⁴ cases. Same machine: about 585 years.",
    "getPassword's input isn't even bounded — there is no test suite "
    "to write.",
    "",
    "“Program testing can be used to show the presence of bugs, but "
    "never to show their absence.” — E. W. Dijkstra, 1970",
    "",
    "A green test suite means: no bug in the cases we tried.",
], top=1.7, size=24)

s = add_slide(prs, "The idea of verification")
add_body(s, [
    "Turn the program and the property into mathematics, and ask one "
    "question:",
    "",
    "Can the program reach a state where the property fails?",
    "",
    ("NO — for all inputs, all paths:  a proof.", 1),
    ("YES — and here is the exact input:  a counterexample.", 1),
    "",
    "Both answers are useful. The second one is a free bug report.",
], top=1.8, size=26)

s = add_slide(prs, "Soundness and completeness")
add_body(s, [
    "Sound — the tool never misses a bug.",
    ("If a sound tool says SAFE, it is safe.", 1),
    "Complete — the tool never raises a false alarm.",
    ("If a complete tool says BUG, it is a real bug.", 1),
    "",
    "Testing is complete but not sound (every failure is real; absence "
    "proves nothing).",
    "Most static analysers are sound but not complete (no missed bugs, "
    "but false alarms).",
], top=1.8, size=24)

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

s = add_slide(prs, "The technique landscape")
add_table(s, [
    ["Technique", "What you get", "What it costs"],
    ["Testing", "real failures, fast", "proves nothing about absence"],
    ["Static analysis / abstract interp.", "sound warnings, scales",
     "false alarms"],
    ["Symbolic execution", "real bugs + the triggering input",
     "path explosion"],
    ["Bounded model checking", "counterexample, or proof up to a bound",
     "the bound"],
    ["Interactive proof (Coq, Isabelle)", "full functional correctness",
     "person-years of effort"],
], top=1.6, size=18, col_widths=[3.8, 4.4, 3.5])
add_body(s, ["Tonight: bounded model checking. At 20:30 we tour who uses "
             "the rest."], top=5.4, size=20)

s = add_slide(prs, "The one trick to remember")
add_body(s, [
    "To prove a property P, ask whether ¬P is satisfiable.",
    ("unsat  ⇒  no way to violate P exists — a proof", 1),
    ("satisfiable, with a model  ⇒  a concrete counterexample to P", 1),
    "",
    "Every tool tonight, and every lab in Session 2, is this one move "
    "in different costumes.",
    "",
    "So we need an oracle for “is this formula satisfiable?” — "
    "it exists, it is free, and it is absurdly good. After the break.",
], top=1.9, size=26)

s = add_slide(prs, "Break — back at 19:25", lead=True)

# --------------------------------------------------- SAT and SMT 19:25
s = add_slide(prs, "SAT: the original hard problem")
add_body(s, [
    ("(a ∨ ¬b) ∧ (b ∨ c) ∧ (¬a ∨ ¬c)", 0, True),
    "",
    "Is there a true/false assignment that makes the whole formula "
    "true?",
    "",
    "The first problem ever proved NP-complete (Cook, 1971) — in "
    "theory, hopeless.",
    "In practice: modern solvers eat formulas with millions of clauses "
    "for breakfast. Industrial SAT solving is the closest thing CS has "
    "to a superpower.",
], top=1.7, size=24)

s = add_slide(prs, "The two answers a solver can give")
add_body(s, [
    "sat — and here is a model:",
    ("a = true, b = true, c = false   ← check it by hand, it works", 1),
    "unsat — no satisfying assignment exists, anywhere.",
    ("Not “I didn't find one”. A proof that none exists.", 1),
    "",
    "Now recall the trick: encode the bug as the formula.",
    ("sat + model  =  bug found, with the input that triggers it", 1),
    ("unsat  =  that bug is impossible", 1),
], top=1.8, size=24)

s = add_slide(prs, "SMT: SAT that speaks C")
add_table(s, [
    ["In your C program", "SMT theory"],
    ["int, unsigned, wrap-around", "bit-vectors — exact machine "
     "arithmetic"],
    ["arrays, indexing", "theory of arrays"],
    ["float, double", "IEEE-754 floating point"],
    ["pointers, malloc/free", "memory models built on the above"],
], top=1.7, size=20, col_widths=[5.2, 6.5])
add_body(s, ["SMT = SAT + theories. The solver reasons about what your "
             "machine actually does — wrap-around, rounding and all — "
             "not idealised mathematics."], top=4.8, size=22)

s = add_slide(prs, "Worked example: one array access")
add_body(s, [
    ("int a[5];          /* valid indices: 0 .. 4 */", 0, True),
    ("a[i] = 0;          /* is this safe? */", 0, True),
    "",
    "The property P:  0 ≤ i ∧ i < 5",
    "The question to the solver:  can the program reach this line "
    "with  ¬(0 ≤ i ∧ i < 5)?",
    ("sat  →  the model contains the bad i — your counterexample", 1),
    ("unsat  →  the access is safe on every path", 1),
], top=1.8, size=24)

s = add_slide(prs, "Live: a solver in two queries")
add_body(s, [
    ("$ python3 z3_demo.py", 0, True),
    ("", 0, True),
    ("Query 1: x + y == 42 and x > 100", 0, True),
    ("[y = -59, x = 101]            ← a model, in milliseconds", 0, True),
    ("", 0, True),
    ("Query 2: x*x == 2*y*y, x > 0, y > 0 (no overflow)", 0, True),
    ("unsat                          ← a proof", 0, True),
    "",
    "Query 2 just proved that √2 is irrational — 32-bit bit-vector "
    "edition. unsat is a theorem, not a shrug.",
], size=22)

s = add_slide(prs, "Machine arithmetic is not mathematics")
add_body(s, [
    ("INT_MAX     =  2147483647", 0, True),
    ("INT_MAX + 1 =  ?            /* C: undefined behaviour */", 0, True),
    ("                            /* bit-vectors: wraps negative */",
     0, True),
    "",
    ("int y = x + 1;", 0, True),
    ("int z = y * 2;", 0, True),
    ("assert(z >= 2);   /* surely true for x >= 0 … ? */", 0, True),
    "",
    "A solver finds the x that breaks this in milliseconds. In Lab 1 "
    "you will encode these three lines yourself and watch it happen.",
], size=22)

s = add_slide(prs, "Solvers as search engines: SEND + MORE = MONEY")
add_body(s, [
    ("  S E N D", 0, True),
    ("+ M O R E", 0, True),
    ("---------", 0, True),
    ("M O N E Y", 0, True),
    "",
    "Eight letters, all different digits, S ≠ 0, M ≠ 0 — about 10⁸ "
    "candidate assignments.",
    "Z3 finds the unique solution in well under a second.",
    "The same engine that solves puzzles finds your bugs: a "
    "counterexample is just a solution to “break my program”.",
    "Lab 1, Stage 2: you run this yourself.",
], size=22)

# --------------------------------------------- bounded model checking 19:50
s = add_slide(prs, "Bounded model checking: the pipeline")
add_flow(s, ["C program", "unwind loops", "single static\nassignment",
             "program ∧ ¬P", "SMT solver"], top=1.9, size=15)
add_body(s, [
    "sat  →  VERIFICATION FAILED + a counterexample trace",
    "unsat  →  no violation exists within the bound",
    "",
    "This is exactly what ESBMC did to getpassword.c before the break — "
    "now we open the box.",
], top=3.8, size=24)

s = add_slide(prs, "Step 1 — unwind the loops")
add_body(s, [
    ("for (int i = 0; i <= 5; i++)  a[i] = i;", 0, True),
    "",
    "--unwind k copies the loop body k times, each copy guarded by the "
    "loop condition.",
    "Then one extra check, the unwinding assertion:",
    ("“could the loop have run a (k+1)-th time?”", 1),
    "",
    "Bounded — but honest: the tool tells you when its bound was too "
    "small, instead of silently missing behaviour.",
], top=1.7, size=24)

s = add_slide(prs, "How to read an --unwind k verdict")
add_table(s, [
    ["The tool prints", "It means"],
    ["VERIFICATION FAILED + trace", "a real bug, reachable within k "
     "iterations"],
    ["VERIFICATION SUCCESSFUL", "a proof — k covers every possible run "
     "of the loop"],
    ["FAILED: unwinding assertion", "the bound was too small — NOT a "
     "program bug; raise k and re-run"],
], top=1.7, size=20, col_widths=[5.0, 6.7])
add_body(s, ["In Session 2 you will choose k yourself for a loop with at "
             "most 50 iterations — keep this table within reach.",
             "“Sound up to its bound”, now made precise."],
         top=4.4, size=22)

s = add_slide(prs, "Step 2 — every assignment gets a fresh name (SSA)")
add_body(s, [
    ("int y = x + 1;        →   y₁ = x₀ + 1", 0, True),
    ("int z = y * 2;        →   z₁ = y₁ · 2", 0, True),
    ("assert(z >= 2);       →   check:  ¬(z₁ ≥ 2)  satisfiable?",
     0, True),
    "",
    "Once every name is assigned exactly once, straight-line code IS a "
    "system of equations — no execution needed.",
    "Recognise the three lines? In Lab 1, Stage 3 you translate exactly "
    "this function by hand and hand it to Z3. You will be doing ESBMC's "
    "job yourself.",
], top=1.8, size=24)

s = add_slide(prs, "Putting it together")
add_body(s, [
    ("⟦program⟧  ∧  ¬P      →  SMT solver", 0, True),
    "",
    "sat — the model assigns every input and every choice: replayed in "
    "program order, that is the counterexample trace.",
    "unsat — no execution within the bound violates P.",
    "",
    "One formula, every path at once. That is why nobody has to "
    "enumerate 2⁶⁴ test cases.",
], top=1.9, size=26)

s = add_slide(prs, "Anatomy of a counterexample")
add_body(s, [
    ("State 3  file offbyone.c  line 15", 0, True),
    ("  i = 5 (00000000 ... 101)      ← the value the solver chose",
     0, True),
    ("...", 0, True),
    ("Violated property:", 0, True),
    ("  array bounds violated: a[i]   ← what broke", 0, True),
    ("  CWE: CWE-787                   ← the vulnerability class",
     0, True),
    "",
    "Read it bottom-up: first what was violated, then scroll up for the "
    "values that caused it.",
    "Those values are a ready-made failing test case — keep them.",
])

s = add_slide(prs, "Live: the whole pipeline on five lines")
add_body(s, [
    ("int main(void)", 0, True),
    ("{", 0, True),
    ("  int a[5];", 0, True),
    ("  for (int i = 0; i <= 5; i++)", 0, True),
    ("    a[i] = i;", 0, True),
    ("}", 0, True),
    ("", 0, True),
    ("$ esbmc offbyone.c --unwind 7", 0, True),
    "",
    "Predict first: FAILED or SUCCESSFUL? If FAILED — at which i?",
    "Then we read the trace together, bottom-up.",
], size=22)

s = add_slide(prs, "Modelling the environment: a preview")
add_body(s, [
    ("int x = nondet_int();              /* every value at once */",
     0, True),
    ("__ESBMC_assume(x > 0 && x < 100);  /* now: every value in 1..99 */",
     0, True),
    ("assert(property(x));               /* must hold for ALL of them */",
     0, True),
    "",
    "One nondeterministic input = all tests of that input at once.",
    "In Session 2 you will use these three lines to expose a bug in a "
    "program that verifies green as shipped — the tool only checks what "
    "you specify.",
], size=22)

s = add_slide(prs, "Beyond one thread")
add_body(s, [
    "Two threads of two and one statements already have three "
    "interleavings. Real code has billions.",
    "Run the program a million times and the bad interleaving may "
    "never show up — Therac-25's bug hid exactly this way.",
    "A model checker enumerates every interleaving up to a bound, "
    "including the one that kills your assertion.",
    "",
    "Session 2, Lab 4: you write down the killer interleaving before "
    "the tool finds it.",
], top=1.8, size=24)

s = add_slide(prs, "Homework for your intuition")
add_body(s, [
    ("double w = 0.1 + 0.2;", 0, True),
    ("assert(w == 0.3);", 0, True),
    "",
    "FAILED or SUCCESSFUL?",
    "",
    "Bring your answer to Session 2 — Lab 4 settles it with a solver "
    "that does exact IEEE-754 arithmetic.",
    ("Hint: 0.1 in binary is like 1/3 in decimal.", 1),
], top=2.0, size=26)

# ------------------------------------------------------- exercise 2 20:15
s = add_slide(prs, "Exercise 2 — Predict the Verdict (15 min)")
add_body(s, [
    "Groups of 3–4. Three short C programs on the handout "
    "(predict1.c, predict2.c, predict3.c).",
    "For each program, write down BEFORE we run anything:",
    ("Will the model checker say VERIFICATION FAILED or SUCCESSFUL?", 1),
    ("If FAILED — which line is the culprit?", 1),
    "Then we run ESBMC live and settle every bet.",
])

# ------------------------------------------------- industry tour 20:30
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
    "KLEE found 56 serious bugs in coreutils, busybox and Minix — "
    "including three in coreutils that had survived 15 years of testing",
    "Microsoft SAGE fuzzed Windows file parsers with symbolic execution; "
    "it found ~1/3 of all bugs caught by file fuzzing during Windows 7 "
    "development — running last, after every other tool",
    "AFL / OSS-Fuzz — Google fuzzes ~1,000 open-source projects "
    "continuously; tens of thousands of bugs found",
    "The pragmatic cousin of verification: no proofs, ruthless "
    "effectiveness",
])

s = add_slide(prs, "Who uses this? — Proofs all the way up")
add_body(s, [
    "Astrée (abstract interpretation) proved absence of runtime errors "
    "in the Airbus A340 fly-by-wire code — 132,000 lines of C — and was "
    "then applied to the A380",
    "seL4 — an OS microkernel with a machine-checked proof of functional "
    "correctness",
    "CompCert — a C compiler with a proof that compilation preserves "
    "semantics; six CPU-years of fuzzing found no wrong-code bugs in "
    "its verified core, while every other compiler tested failed",
])

s = add_slide(prs, "Discussion")
add_body(s, [
    "If verification can prove the absence of bugs…",
    "why isn't all software verified?",
    "(Let's collect reasons — then I'll tell you which ones the industry "
    "actually cites.)",
], top=2.4, size=28)

# ------------------------------------------------------------ close 20:50
s = add_slide(prs, "Closing quiz")
add_body(s, [
    "1. A tool that never raises a false alarm is called …?",
    "2. ESBMC returns UNSAT for C ∧ ¬P at --unwind 10. "
    "What do we know?",
    "3. What's inside a counterexample?",
    "4. Which technique proved the A340 flight-control code free of "
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

prs.save("session1/01-session1-fundamentals.pptx")
print(f"saved session1/01-session1-fundamentals.pptx "
      f"with {len(prs.slides)} slides")
