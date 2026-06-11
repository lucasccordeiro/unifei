# Slides

The presentation material for both sessions: three decks carved out of the
COMP63342 *Software Security* lectures (animation build-up slides collapsed
to their final state), plus one authored deck with the workshop-specific
slides (agenda, exercises, industry landscape, quizzes, lab intros).

## Session 1 run order

| When (plan block) | Deck | Slides | Source |
|---|---|---|---|
| 18:00 welcome → icebreaker | `workshop-extras.pptx` 1–3 | 3 | authored |
| 18:10 why software fails | `session1/01-why-software-fails.pptx` | 16 | COMP63342 lecture 1 (short), slides 1, 19–21, 25–27, 29–31, 35, 38–39, 51, 53, 59 |
| 18:35 Exercise 1 | `workshop-extras.pptx` 4 | 1 | authored |
| 18:50 testing vs. verification + SAT/SMT (19:25) | `session1/02-testing-vs-verification-sat-smt.pptx` | 19 | COMP63342 lecture 3 (short), slides 1, 9, 18, 21, 30, 32, 34, 36–37, 39, 49, 66, 82–83, 87, 93, 96, 101, 105 |
| 18:50 sound × complete grid | `workshop-extras.pptx` 5 | 1 | authored |
| 19:50 BMC internals | `session1/03-bmc-internals.pptx` | 16 | COMP63342 lecture 4 (expanded), slides 1, 10, 14–16, 21, 28–29, 31, 33, 35, 50, 53–54, 61, 77 |
| 20:15 Exercise 2 | `workshop-extras.pptx` 6 | 1 | authored |
| 20:30 industry landscape + discussion | `workshop-extras.pptx` 7–10 | 4 | authored |
| 20:50 quiz + setup homework | `workshop-extras.pptx` 11–12 | 2 | authored |

## Session 2 run order

Session 2 is hands-on; slides only frame the labs.

| When | Deck | Slides |
|---|---|---|
| 18:00 welcome, recap quiz, schedule | `workshop-extras.pptx` 13–15 | 3 |
| Lab intros 1–4 + bounds discussion (shown as each lab starts) | `workshop-extras.pptx` 16–20 | 5 |
| 20:45 debrief + where next | `workshop-extras.pptx` 21 | 1 |

## Files

- `session1/01-why-software-fails.pptx` — motivating `getPassword` example,
  safety vs. security, CIA, vulnerability classes, CVE growth, "industry
  needs formal verification", BMC applied to security.
- `session1/02-testing-vs-verification-sat-smt.pptx` — V&V, soundness and
  completeness, static analysis vs. testing, BMC vs. symbolic execution,
  SAT, SMT theories with the array/bit-vector worked example.
- `session1/03-bmc-internals.pptx` — CBMC/ESBMC/LLBMC architecture, control-flow
  simplification, loop unwinding, safety conditions as assertions, SSA,
  guarded assignments, SAT vs. SMT, modelling with nondeterminism
  (bridges to Lab 3), concurrency teaser (bridges to Lab 4).
- `workshop-extras.pptx` — the authored workshop slides for both sessions.
- `workshop-extras.md` — canonical source of the authored deck
  (Marp-compatible Markdown; edit here first).
- `build_extras.py` — regenerates `workshop-extras.pptx` from the same
  content (`python3 -m venv venv && venv/bin/pip install python-pptx &&
  venv/bin/python build_extras.py`).

## Regenerating the extracted decks

The three `session1/` decks were extracted from the original course files
with PowerPoint automation, keeping the slide numbers listed above (build-up
sequences collapsed to their last, complete slide). To change a subset,
re-run the extraction against the originals from the
[course page](https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html)
and update the slide lists in this README.
