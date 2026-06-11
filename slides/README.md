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
`session1/01-session1-fundamentals.pptx` (45 slides).

| When (plan block) | Slides | Content |
|---|---|---|
| 18:00 welcome → icebreaker | 1–3 | title, agenda, icebreaker poll |
| 18:10 why software fails | 4–12 | Ariane 5/Therac-25, `getpassword.c` + stack smash, live ESBMC demo, safety vs. security, memory safety, CVE growth and CWE Top 25 charts, industry's conclusion |
| 18:35 Exercise 1 | 13 | spot the bug |
| 18:50 testing vs. verification | 14–20 | V&V, why testing can't prove absence, soundness/completeness, sound × complete grid, technique landscape, **the negation trick** |
| 19:15 break | 21 | — |
| 19:25 SAT and SMT | 22–28 | SAT, sat/unsat as witness/proof, SMT theories for C, array-bounds worked example, live `z3_demo.py`, wrap-around, SEND+MORE=MONEY |
| 19:50 bounded model checking | 29–38 | pipeline, loop unwinding, **`--unwind k` verdict table**, SSA, **counterexample anatomy**, live `offbyone.c` demo, nondet/assume/assert preview, concurrency + floating-point hooks for Lab 4 |
| 20:15 Exercise 2 | 39 | predict the verdict |
| 20:30 industry landscape + discussion | 40–43 | AWS/SV-COMP, KLEE/SAGE/OSS-Fuzz, Astrée/seL4/CompCert, discussion |
| 20:50 quiz + setup homework | 44–45 | closing quiz, Session 2 setup |

The deck is designed to pre-teach everything Session 2's labs assume:
the negation trick (Lab 1), counterexample reading (Lab 2), the
specification toolkit and unwind-bound semantics (Lab 3), and the
concurrency/floating-point intuitions (Lab 4).

## Session 2 run order

Session 2 is hands-on; slides only frame the labs.
`session2/01-session2-hands-on.pptx`, shown as each lab starts. Companion background decks (extracted from COMP63342 lectures,
optional): `02-memory-model.pptx` for Lab 2, `03-k-induction.pptx` for
the Lab 3 stretch question.

## Files

- `session1/01-session1-fundamentals.pptx` — the Session 1 deck
  (built by `build_session1.py`; Markdown twin alongside).
- `session2/01-session2-hands-on.pptx` — the Session 2 deck
  (built by `build_session2.py`; Markdown twin alongside).
- `session2/02-memory-model.pptx`, `session2/03-k-induction.pptx` —
  extracted COMP63342 background decks (converted to 16:9 by
  `widescreen.py`).
- `pptx_helpers.py` — shared slide/table/chart/flow-diagram helpers.

## Regenerating

```sh
python3 -m venv venv && venv/bin/pip install python-pptx
venv/bin/python build_session1.py   # session1/01-session1-fundamentals.pptx
venv/bin/python build_session2.py   # session2/01-session2-hands-on.pptx
```

The extracted background decks came from the original course files
(animation build-ups collapsed to their final state); to change the
subset, re-extract from the
[course page](https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html)
and convert with `widescreen.py`.
