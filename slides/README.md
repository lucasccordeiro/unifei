# Slides

One authored deck per session, built with python-pptx from the scripts in
this directory, plus two decks extracted from the COMP63342 *Software
Security* lectures kept as optional background for Session 2's labs.

Each authored deck has a Marp-compatible Markdown twin with the same
content (`01-session1-fundamentals.md`, `01-session2-hands-on.md`) for
quick reading and diffing; the build scripts are the canonical source —
edit the script, regenerate the `.pptx`, and keep the Markdown in sync.

## Session 1 run order

A single deck in exact run order — no deck-switching during the evening:
`session1/01-session1-fundamentals.pptx` (49 slides).

| When (plan block) | Slides | Content |
|---|---|---|
| 18:00 welcome → icebreaker | 1–3 | title, agenda, icebreaker poll |
| 18:10 why software fails | 4–14 | Ariane 5/Therac-25/CrowdStrike, `getpassword.c` + stack smash, live ESBMC demo, **ESBMC test-case generation** (`--generate-ctest-testcase`, `session1-demos/ctest-gen/`), **logic-flaw bypass** (`strncmp-bypass/`, empty-string defeat), safety vs. security, memory safety, CVE growth and CWE Top 25 charts, industry's conclusion |
| 18:35 Exercise 1 | 15 | spot the bug |
| 18:50 testing vs. verification | 16–24 | V&V, why testing can't prove absence, soundness/completeness, **techniques as real tools** (Coverity/KLEE/Astrée/CBMC/Dafny by method), sound × complete grid (k-induction lifts BMC into the sound row), technique landscape, **LLMs as bug-finders** (Big Sleep, ESBMC-AI — LLM proposes, verifier disposes), **the negation trick** |
| 19:15 break | 25 | — |
| 19:25 SAT and SMT | 26–32 | SAT, sat/unsat as witness/proof, SMT theories for C, array-bounds worked example, live `z3_demo.py`, wrap-around, SEND+MORE=MONEY |
| 19:50 bounded model checking | 33–42 | pipeline, loop unwinding, **`--unwind k` verdict table**, SSA, **counterexample anatomy**, live `offbyone.c` demo, nondet/assume/assert preview, concurrency + floating-point hooks for Lab 4 |
| 20:15 Exercise 2 | 43 | predict the verdict |
| 20:30 industry landscape + discussion | 44–47 | AWS/SV-COMP, KLEE/SAGE/OSS-Fuzz, Astrée/seL4/CompCert, discussion |
| 20:50 quiz + setup homework | 48–49 | closing quiz, Session 2 setup |

The deck is designed to pre-teach everything Session 2's labs assume:
the negation trick (Lab 1), counterexample reading (Lab 2), the
specification toolkit and unwind-bound semantics (Lab 3), and the
concurrency/floating-point intuitions (Lab 4).

## Session 2 run order

Session 2 is hands-on; slides only frame the labs. The main deck is
`session2/01-session2-hands-on.pptx` (20 slides), shown as each lab
starts. Solutions are revealed from the instructor-only deck after each
lab closes.

| When (plan block) | Deck | Slides |
|---|---|---|
| 18:00 welcome, recap quiz, schedule, the one trick | `01-session2-hands-on` | 1–4 |
| 18:15 Lab 1 intro + Z3 API walkthrough | `01-session2-hands-on` | 5–8 |
| 18:50 checkpoint, Lab 2 intro, counterexample deep dive | `01-session2-hands-on` | 9–13 |
| Lab 2 background, on demand | `02-memory-model` (slides 5–9 are the authored appendix) | 1–9 |
| after each lab block: solution reveal | `../instructor/session2-solutions.pptx` (instructor only) | 1–12 |
| 19:30 break | `01-session2-hands-on` | 14 |
| 19:40 Lab 3 intro, spec toolkit, bounds discussion | `01-session2-hands-on` | 15–17 |
| Lab 3 stretch background | `03-k-induction` (slides 6–10 are the authored appendix) — slides 7 and 10 answer the Part 2 questions; show only **after** the whole-room discussion | 1–10 |
| 20:15 Lab 4 intro + Track A rationale | `01-session2-hands-on` | 18–19 |
| 20:45 debrief | `01-session2-hands-on` | 20 |

## Files

- `session1/01-session1-fundamentals.pptx` — the Session 1 deck
  (built by `build_session1.py`; Markdown twin alongside).
- `session2/01-session2-hands-on.pptx` — the Session 2 deck
  (built by `build_session2.py`; Markdown twin alongside).
- `../instructor/session2-solutions.pptx` — instructor-only solution
  reveals for Session 2 (built by `build_session2_solutions.py`;
  Markdown twin at `../instructor/session2-solutions.md`). Kept under
  `instructor/` so zipping `slides/` for students never leaks it.
- `session2/02-memory-model.pptx` (9 slides),
  `session2/03-k-induction.pptx` (10 slides) — extracted COMP63342
  background decks (converted to 16:9 by `widescreen.py`), each with an
  authored workshop appendix added by `extend_backup_decks.py`.
- `pptx_helpers.py` — shared slide/table/chart/flow-diagram helpers.

## Regenerating

```sh
python3 -m venv venv && venv/bin/pip install python-pptx
venv/bin/python build_session1.py             # session1/01-session1-fundamentals.pptx
venv/bin/python build_session2.py             # session2/01-session2-hands-on.pptx
venv/bin/python build_session2_solutions.py   # ../instructor/session2-solutions.pptx
```

The extracted background decks came from the original course files
(animation build-ups collapsed to their final state); to change the
subset, re-extract from the
[course page](https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html)
and convert with `widescreen.py`, then run `extend_backup_decks.py`
**once** to re-apply the authored appendices (it refuses to run on a
deck that is not at the pristine extracted slide count, so it cannot
double-append).
