#!/usr/bin/env python3
"""Build session2/01-session2-hands-on.pptx — the authored framing slides
for the hands-on evening. Shown between labs; the labs themselves run in
the terminal. Companion extracted decks: 02-memory-model.pptx (Lab 2
background) and 03-k-induction.pptx (Lab 3 stretch background).

Usage:  python3 -m venv venv && venv/bin/pip install python-pptx
        venv/bin/python build_session2.py
"""
from pptx_helpers import new_presentation, add_slide, add_body, add_table

prs = new_presentation()

s = add_slide(prs, "Formal Verification Workshop", lead=True)
add_body(s, ["Session 2 — Hands-On", "18:00 – 21:00",
             "Tonight you drive."], top=3.9, size=26)

s = add_slide(prs, "Recap quiz (while machines boot)")
add_body(s, [
    "1. To prove property P with a solver, you ask whether … is "
    "satisfiable?",
    "2. sat + a model in that setup means …?",
    "3. --unwind 5 reports a violated unwinding assertion. "
    "Is the program buggy?",
    "",
    "Smoke test, everyone:",
    ("esbmc lab4/float.c   →  VERIFICATION FAILED", 0, True),
    ("(yes, FAILED — your tool just found a real bug)", 1),
], size=24)

s = add_slide(prs, "Tonight")
add_table(s, [
    ["18:15", "Lab 1", "Constraint solving with Z3"],
    ["18:50", "Lab 2", "Bug hunting with ESBMC"],
    ["19:30", "Break", ""],
    ["19:40", "Lab 3", "Writing your own specifications"],
    ["20:15", "Lab 4", "Team challenge"],
    ["20:45", "", "Debrief + where next"],
], top=1.6, size=20, col_widths=[1.6, 1.8, 8.3])
add_body(s, ["Work in pairs · keep labs/CHEATSHEET.md open · "
             "predict before you run"], top=4.6, size=22)

s = add_slide(prs, "The one trick behind the whole evening")
add_body(s, [
    "To prove a property P, ask the solver whether ¬P is satisfiable.",
    ("unsat  ⇒  P always holds (a proof)", 1),
    ("a model  ⇒  a concrete counterexample to P", 1),
    "",
    "Everything tonight — Z3 puzzles, ESBMC bug hunts, your own "
    "specifications — is this one move in different costumes.",
], top=2.0, size=26)

s = add_slide(prs, "Another route to a proof: abstract interpretation")
add_body(s, [
    "Tonight's trick hunts a counterexample. Abstract interpretation "
    "proves P the other way — over-approximate every run at once to a "
    "fixpoint invariant: no bound, no search.",
    "",
    ("You met the mechanism in Session 1: abstract domain, widening (∇), "
     "narrowing (Δ) — iterate to a fixpoint; if it implies P, P holds for "
     "every run.", 1),
    ("Sound, not complete: too coarse an over-approximation → a false "
     "alarm. (Astrée proved the A380 fly-by-wire this way.)", 1),
    ("ESBMC ships it too — --interval-analysis — feeding the invariant "
     "k-induction needs for unwind.c (Lab 3).", 1),
], top=2.0, size=24)

s = add_slide(prs, "Lab 1 — Constraint solving (35 min)")
add_body(s, [
    "labs/lab1/lab1.py — three stages, instructions inside.",
    ("Stage 1 (guided): are these formulas equivalent? "
     "Encode lhs ≠ rhs, ask the solver.", 1),
    ("Stage 2: SEND + MORE = MONEY — let Z3 search 10⁸ assignments.", 1),
    ("Stage 3: a 3-line C function as SSA equations — you are doing "
     "ESBMC's job by hand.", 1),
    "",
    "Predict before every run: write your guess as a comment first.",
    ("Box B (optional): re-run Stage 3 as Python ESBMC checks for you — "
     "stage3_esbmc.py.", 1),
])

s = add_slide(prs, "Z3's Python API — the whole toolkit")
add_body(s, [
    ("from z3 import Bools, Ints, BitVec, Solver, sat, unsat", 0, True),
    ("a, b = Bools(\"a b\")     # symbolic booleans, not values", 0, True),
    ("x = BitVec(\"x\", 32)     # a 32-bit machine integer", 0, True),
    ("", 0, True),
    ("s = Solver()", 0, True),
    ("s.add(formula)           # constrain", 0, True),
    ("s.check()                # -> sat or unsat", 0, True),
    ("s.model()                # the witness, when sat", 0, True),
    "",
    "Every stage of lab1.py is these five calls — nothing else.",
])

s = add_slide(prs, "Walkthrough: equivalent() from lab1.py")
add_body(s, [
    ("def equivalent(lhs, rhs, name):", 0, True),
    ("    slv = Solver()", 0, True),
    ("    slv.add(lhs != rhs)            # can they EVER differ?", 0, True),
    ("    if slv.check() == unsat:       # never differ: a proof",
     0, True),
    ("        print(name, \"EQUIVALENT\")", 0, True),
    ("    else:                          # a witness they differ",
     0, True),
    ("        print(name, slv.model())", 0, True),
    "",
    ("1a De Morgan: EQUIVALENT   ·   1b distribution: EQUIVALENT", 1),
    ("1c trick question: NOT equivalent, counterexample: [b = False]",
     1, True),
    ("Read the model: with b = False, a → (b → a) is true but b is "
     "false.", 1),
])

s = add_slide(prs, "Walkthrough: Stage 3 is ESBMC by hand")
add_body(s, [
    ("x, y, z = BitVec(\"x\", 32), BitVec(\"y\", 32), BitVec(\"z\", 32)",
     0, True),
    ("s.add(y == x + 1)        # int y = x + 1;", 0, True),
    ("s.add(z == y * 2)        # int z = y * 2;", 0, True),
    ("s.add(Not(z >= 2))       # assert(z >= 2) — NEGATED", 0, True),
    "",
    ("sat — counterexample e.g. x = 1073741824 (= 2^30)", 0, True),
    ("y * 2 overflows the 32-bit range: z comes out negative.", 1),
    "Would your test suite have tried 1073741824?",
    "",
    "ESBMC builds exactly this formula from your C — automatically. "
    "That's Lab 2.",
])

s = add_slide(prs, "Box B: hand that same Python to ESBMC")
add_body(s, [
    ("def f(x: int) -> int:", 0, True),
    ("    y = x + 1", 0, True),
    ("    z = y * 2", 0, True),
    ("    assert z >= 2        # ESBMC negates this for you", 0, True),
    ("x: int = nondet_int()    # every int at once, like BitVec(\"x\")",
     0, True),
    ("f(x)", 0, True),
    "",
    ("esbmc stage3_esbmc.py  →  VERIFICATION FAILED   (x = 2^63 - 1)",
     0, True),
    ("You wrote the function; ESBMC wrote AND solved the formula.", 1),
    ("Z3 is the SMT engine; ESBMC is a model checker built ON it — it "
     "calls Z3 underneath.", 1),
    ("Same bug, different number: 2^30 (your 32-bit BitVec) vs 2^63 — "
     "ESBMC models a Python int as 64-bit.", 1),
], size=22)

s = add_slide(prs, "Checkpoint before Lab 2")
add_body(s, [
    "What does unsat mean in Stage 1?",
    "What does unsat mean in Stage 3?",
    "",
    "Same verdict — two different questions answered. If you can "
    "articulate the difference, you understand verification.",
], top=2.2, size=28)

s = add_slide(prs, "Lab 2 — Bug hunting (40 min)")
add_body(s, ["predict → verify → READ THE COUNTEREXAMPLE → "
             "fix → re-verify"], top=1.5, size=22)
add_table(s, [
    ["#", "File", "By"],
    ["1", "overflow.c", "—"],
    ["2", "leak.c", "19:05"],
    ["3", "vla.c  (two bugs!)", "19:20"],
    ["4", "getpassword.c", "stretch"],
], top=2.3, size=18, col_widths=[0.8, 5.2, 2.2])
add_body(s, ["Done = VERIFICATION SUCCESSFUL on your fixed file, same "
             "flags.",
             "Finished early? You are now a TA — help the pair next to "
             "you.",
             ("Box B (optional): esbmc safe_div.py — same loop, Python "
              "input.", 0, True)], top=5.0, size=20)

s = add_slide(prs, "How to read a counterexample")
add_body(s, [
    "Real output — esbmc getpassword.c --unwind 8:",
    ("State 1 file getpassword.c line 18 function getPassword thread 0",
     0, True),
    ("  buf = { 0, 0, 0, 0 }              ← the state so far", 0, True),
    ("State 2 file ...library/io.c line 91 function gets thread 0",
     0, True),
    ("Violated property:", 0, True),
    ("  dereference failure: array bounds violated   ← what broke",
     0, True),
    ("  CWE: CWE-121, CWE-125, CWE-129, ...           ← the vuln class",
     0, True),
    ("VERIFICATION FAILED", 0, True),
    "",
    "Read bottom-up: what was violated, then scroll up for which "
    "values caused it.",
])

s = add_slide(prs, "Deep dive: overflow.c — the trace")
add_body(s, [
    ("State 1 ...  a = { 0, -1 }   ← stack garbage in the array",
     0, True),
    ("State 2 ...  i = -1          ← the index the solver chose",
     0, True),
    ("State 3 ...  x = -1          ← the branch the solver chose",
     0, True),
    ("Violated property:", 0, True),
    ("  file overflow.c line 24 ... assertion main", 0, True),
    ("  !((_Bool)((signed long int)(!(p[1] == 1))))", 0, True),
    "",
    ("x = -1 takes the else branch; a[i + 1] with i = -1 writes a[0].",
     1),
    ("So a[1] keeps its garbage (-1) and assert(*(p + 1) == 1) dies.",
     1),
    "i = -1, x = -1 is a ready-made failing test case — keep it.",
])

s = add_slide(prs, "Deep dive: what broke, and its CWE")
add_body(s, [
    "Two shapes of violated property:",
    ("an assertion — names YOUR line:", 1),
    ("  overflow.c line 24 ... assertion main", 1, True),
    ("a built-in check — names the bug kind plus its CWE classes:", 1),
    ("  dereference failure: array bounds violated", 1, True),
    ("  CWE: CWE-121, CWE-125, CWE-129, CWE-131, CWE-193, CWE-787",
     1, True),
    ("  (stack overflow · OOB read · bad index · size miscalc · "
     "off-by-one · OOB write)", 2),
    "",
    "The path may point inside ESBMC's model of the C library "
    "(io.c line 91 = the gets model).",
    ("That names the API you misused — it is not a bug in ESBMC.", 1),
])

s = add_slide(prs, "Break — back at 19:40", lead=True)

s = add_slide(prs, "Lab 3 — Specifications (35 min)")
add_body(s, [
    "triangle.c verifies SUCCESSFUL as shipped.",
    "Does that mean it's correct?",
    "Write the two TODO properties and find out.",
    "",
    "The tool checks what you specify — with a weak spec, green is "
    "cheap.",
], top=2.0, size=28)

s = add_slide(prs, "Your specification toolkit")
add_body(s, [
    ("int nondet_int(void);              /* any possible int */", 0, True),
    ("void __ESBMC_assume(_Bool);", 0, True),
    ("", 0, True),
    ("int x = nondet_int();              /* every value at once */",
     0, True),
    ("__ESBMC_assume(x > 0 && x < 100);  /* now: every value in 1..99 */",
     0, True),
    ("assert(property(x));               /* must hold for ALL of them */",
     0, True),
    "",
    "One nondet input = all tests of that input at once.",
])

s = add_slide(prs, "Lab 3, Part 2 — what did we prove?")
add_body(s, [
    ("esbmc unwind.c --unwind 5      →  ?", 0, True),
    ("esbmc unwind.c --unwind 20     →  ?", 0, True),
    ("esbmc unwind.c --unwind 60     →  ?", 0, True),
    "",
    "What is the unwinding assertion telling you at 5 and 20?",
    "At 60 — what exactly is proven, and for which n?",
    "Stretch: --k-induction answers VERIFICATION UNKNOWN. Why is the "
    "unbounded question fundamentally harder? "
    "(Background deck: 03-k-induction.pptx)",
])

s = add_slide(prs, "Lab 4 — Team challenge (30 min)")
add_body(s, [
    "Teams of 3–4. Points on the whiteboard:",
    ("1 pt — verdict predicted correctly in writing, before running", 1),
    ("2 pts — file fixed and re-verified", 1),
    "",
    "Track A:  race.c — write down the failing interleaving first, then",
    ("esbmc race.c --context-bound 2", 0, True),
    "Track B:  float.c — primary-school arithmetic. Or is it?",
])

s = add_slide(prs, "Why machines beat humans at Track A")
add_body(s, [
    "Sequentially, race.c is bulletproof — run it a million times, "
    "the bug may never show.",
    "Two threads of just 2 and 1 statements already have 3 "
    "interleavings; real code has billions.",
    "The model checker enumerates every interleaving up to the "
    "context bound — including the one that kills the assertion.",
    "",
    "The counterexample you get includes the thread schedule: "
    "read it as a story of who ran when.",
])

s = add_slide(prs, "Debrief")
add_body(s, [
    "One thing the tool caught that YOU wouldn't have?",
    "The arc you just walked: intuition → concepts → tools "
    "→ application",
    "",
    "Where next:",
    ("SV-COMP benchmarks: sv-comp.sosy-lab.org", 1),
    ("Full course: COMP63342 Software Security (slides online)", 1),
    ("ESBMC: esbmc.org · Z3: github.com/Z3Prover/z3", 1),
    ("The complementary technique: fuzzing (AFL, OSS-Fuzz)", 1),
    "",
    "Feedback poll: pace / best lab / one improvement. Thank you!",
])

prs.save("session2/01-session2-hands-on.pptx")
print(f"saved session2/01-session2-hands-on.pptx with {len(prs.slides)} slides")
