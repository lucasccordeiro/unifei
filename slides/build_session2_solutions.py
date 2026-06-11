#!/usr/bin/env python3
"""Build ../instructor/session2-solutions.pptx — the instructor-only
solution-reveal deck for Session 2. One reveal block per lab, shown after
each lab closes. Lives under instructor/ (the do-not-distribute zone);
every verdict quoted here is verified in instructor/solutions/expected-verdicts.md.

Usage:  python3 -m venv venv && venv/bin/pip install python-pptx
        venv/bin/python build_session2_solutions.py
"""
from pptx_helpers import new_presentation, add_slide, add_body, add_table

prs = new_presentation()

s = add_slide(prs, "Session 2 — Solutions", lead=True)
add_body(s, ["Instructor deck — do not distribute before the session.",
             "All verdicts verified: ESBMC 8.3.0 / Z3 4.16.0 "
             "(solutions/expected-verdicts.md)."], top=3.9, size=24)

s = add_slide(prs, "Lab 1, Stage 1 — answers")
add_body(s, [
    "1c: NOT equivalent — counterexample [b = False].",
    ("With b false, a → (b → a) is true but b is false.", 1),
    "",
    "1d (the TODO): implication is NOT associative.",
    ("equivalent(Implies(Implies(a, b), c),", 1, True),
    ("           Implies(a, Implies(b, c)), \"1d\")", 1, True),
    ("Counterexample: a and c both false — lhs is false "
     "(T → F), rhs is true (F → anything).", 1),
])

s = add_slide(prs, "Lab 1, Stages 2–3 — answers")
add_body(s, [
    "Stage 2 — the missing constraint:",
    ("send  = 1000*S + 100*E + 10*N + D   (more, money alike)", 1, True),
    ("s.add(send + more == money)", 1, True),
    ("Unique model: 9567 + 1085 = 10652", 1),
    "",
    "Stage 3, Q3 — still sat even with x >= 0:",
    ("x = 0x7FFFFFFF wraps y to INT_MIN; 2 * INT_MIN wraps to 0 < 2.",
     1),
    ("Same bug class --overflow-check hunts in Lab 2.", 1),
])

s = add_slide(prs, "Lab 2 — overflow.c")
add_body(s, [
    "Verdict: FAILED — solver picks i = -1, x = -1; the write lands on "
    "a[0], a[1] stays garbage.",
    "",
    "Fix (overflow_fixed.c): repair the index AND the spec — keep x "
    "untrusted:",
    ("int a[2] = {0, 0};  int i = 0;  int x = nondet_int();", 1, True),
    ("assert(x == 0 ? *(p + i) == 0 : *(p + i + 1) == 1);", 1, True),
    ("esbmc overflow_fixed.c  =>  VERIFICATION SUCCESSFUL", 1, True),
    "",
    "Takeaway: fix the index and the assertion; the input stays nondet.",
])

s = add_slide(prs, "Lab 2 — leak.c")
add_body(s, [
    ("dereference failure: forgotten memory: dynamic_1_array", 0, True),
    ("CWE: CWE-401", 0, True),
    "",
    "p = q overwrote the only pointer to the first malloc(5) — those "
    "5 bytes can never be freed.",
    "",
    "Fix (leak_fixed.c): free(p) BEFORE aliasing it.",
    ("esbmc leak_fixed.c --memory-leak-check  =>  SUCCESSFUL", 1, True),
    "",
    "Takeaway: a leak is unreachable memory, not just un-freed memory.",
])

s = add_slide(prs, "Lab 2 — vla.c (two bugs)")
add_body(s, [
    "Bug 1: the loop runs to size + 1 — one write past a VLA of size n "
    "when size == n.",
    "Bug 2: the first call is foo(0, b, 0) — a zero-sized VLA is "
    "undefined behaviour before any access.",
    "",
    "Fix (vla_fixed.c): guard the sizes, loop strictly below size:",
    ("if (n <= 0 || size > n) return 0;", 1, True),
    ("for (i = 0; i < size; i++) a[i] = b[i];", 1, True),
    ("esbmc vla_fixed.c --unwind 6  =>  VERIFICATION SUCCESSFUL",
     1, True),
])

s = add_slide(prs, "Lab 2 — getpassword.c (stretch)")
add_body(s, [
    "Fix (getpassword_fixed.c): bounded read, strip the newline:",
    ("if (!fgets(buf, sizeof(buf), stdin)) return 1;", 1, True),
    ("buf[strcspn(buf, \"\\n\")] = '\\0';", 1, True),
    "",
    "Gotcha: the fixed file (char buf[8]) needs --unwind 10, not 8 — "
    "the fgets model iterates further.",
    ("A minimal fix keeping buf[4] verifies at --unwind 8.", 1),
    "",
    "Discussion bridge: why does the right bound depend on the code? "
    "→ Lab 3, Part 2.",
])

s = add_slide(prs, "Lab 3 — triangle.c")
add_body(s, [
    "Seeded bug: classify() forgot the third inequality b + c <= a.",
    "",
    "The two TODO properties (triangle_solution.c):",
    ("assert(!(a+b<=c || a+c<=b || b+c<=a) || r == 4);  /* P3 */",
     1, True),
    ("assert(classify(a, b, c) == classify(c, b, a));   /* P4 */",
     1, True),
    "",
    "Observed counterexamples — both correct outcomes of the same bug:",
    ("a=999, b=1, c=1 fires P3 directly;  a=512, b=256, c=768 fires P4.",
     1),
    "Fixed + specified: VERIFICATION SUCCESSFUL in ~0.5 s.",
])

s = add_slide(prs, "Lab 3 — unwind.c scoreboard")
add_table(s, [
    ["Run", "Verdict", "What it means"],
    ["--unwind 5", "FAILED (unwinding assertion)",
     "Bound truncated the loop — not a program bug"],
    ["--unwind 20", "FAILED (unwinding assertion)", "Same — still short"],
    ["--unwind 60", "SUCCESSFUL",
     "Complete proof: every n <= MAX=50 fully unwound"],
    ["--k-induction", "UNKNOWN",
     "Assertion not k-inductive without invariant sum == 2*i"],
], top=1.7, size=16, col_widths=[2.4, 3.9, 5.4])
add_body(s, ["The most important 5 minutes of the evening: SUCCESSFUL "
             "at 60 is a proof; FAILED at 5 says nothing about the "
             "program."], top=4.6, size=20)

s = add_slide(prs, "Lab 4, Track A — race.c")
add_body(s, [
    "The failing interleaving, straight from the trace:",
    ("State 71 ... function t1 thread 1      g = 1", 1, True),
    ("State 78 ... function t2 thread 2      g = 2", 1, True),
    ("State 87 ... function t1 thread 1", 1, True),
    ("Violated property: assertion t1   (g == 1)", 1, True),
    "",
    "Fix (race_fixed.c): one mutex makes write-then-check atomic — "
    "lock around g = 1; assert(g == 1); in t1 and around g = 2 in t2.",
    ("esbmc race_fixed.c --context-bound 2  =>  SUCCESSFUL", 1, True),
])

s = add_slide(prs, "Lab 4, Track B — float.c")
add_body(s, [
    "FAILED is the correct verdict — the program is genuinely wrong.",
    ("0.1, 0.2 and 0.3 have no exact binary64 representation — same "
     "reason 1/3 has none in decimal.", 1),
    ("0.1 + 0.2 rounds to the double nearest 0.30000000000000004, "
     "which is not the double nearest 0.3.", 1),
    "",
    "There is no float_fixed.c — by design. Discuss the remedies:",
    ("compare with an epsilon: fabs(w - z) < 1e-9", 1, True),
    ("use decimal / fixed-point where exactness matters (money!)", 1),
    ("or specify the property you actually mean.", 1),
])

s = add_slide(prs, "Master verdict table (fallback if live demos die)")
add_table(s, [
    ["File", "Command", "Buggy", "Fixed"],
    ["overflow.c", "esbmc overflow.c", "FAILED", "SUCCESSFUL"],
    ["leak.c", "esbmc leak.c --memory-leak-check", "FAILED",
     "SUCCESSFUL"],
    ["vla.c", "esbmc vla.c --unwind 6", "FAILED", "SUCCESSFUL"],
    ["getpassword.c", "esbmc getpassword.c --unwind 8", "FAILED",
     "SUCCESSFUL (--unwind 10)"],
    ["triangle.c", "esbmc triangle.c", "SUCCESSFUL (weak spec!)",
     "SUCCESSFUL (full spec)"],
    ["unwind.c", "--unwind 5 / 20 / 60 / --k-induction",
     "F / F / S / UNKNOWN", "—"],
    ["race.c", "esbmc race.c --context-bound 2", "FAILED", "SUCCESSFUL"],
    ["float.c", "esbmc float.c", "FAILED", "— (by design)"],
], top=1.6, size=13, col_widths=[1.9, 4.6, 2.9, 2.3])

prs.save("../instructor/session2-solutions.pptx")
print(f"saved ../instructor/session2-solutions.pptx with "
      f"{len(prs.slides)} slides")
