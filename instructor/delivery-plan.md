# Formal Verification Workshop — Instructor Delivery Plan

**Audience:** Mixed undergraduate/graduate, limited prior exposure to formal methods
**Format:** Two 3-hour evening sessions (18:00–21:00)
**Slides:** ready to present in [`../slides/`](../slides/) — three subsets
extracted from the COMP63342 lectures plus the authored workshop deck;
per-block run order in [`../slides/README.md`](../slides/README.md).
Originals on the
[course page](https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html)
**Code:** everything referenced below lives in this repository, and every
command has been executed and recorded in
[`solutions/expected-verdicts.md`](solutions/expected-verdicts.md).

## Material map

| Workshop element | Source |
|---|---|
| Motivating example (`getPassword`/`gets`), CIA triad, safety vs. security | lecture 1, slides ~35–54 |
| Memory safety, CERT C, "70% of Microsoft security bugs are memory safety" | lecture 2 |
| V&V, soundness/completeness, SMT theories | lecture 3 |
| BMC internals: SSA, unwinding, guarded assignments | lecture 4 |
| Coverage, fuzzing, symbolic execution (landscape block) | lecture 5 |
| DNN verification (extension) | AI-security guest lecture |
| Demo/lab programs | `session1-demos/`, `labs/` here |

---

# Session 1 — Fundamentals and Real-World Applications

## Learning objectives

Participants can: (1) explain why testing cannot establish absence of
bugs; (2) define soundness/completeness and compare techniques with them;
(3) sketch how program + property becomes a SAT/SMT formula; (4) name
real deployments of formal verification; (5) read a counterexample trace.

## Preparation

- **Instructor:** slides ready in `../slides/` (the ~40-slide subset of the
  map above, already extracted — see the run order in `../slides/README.md`);
  ESBMC + Z3 working on the
  presentation machine — dry-run `session1-demos/README.md` top to bottom;
  live-poll quiz loaded from [`quizzes.md`](quizzes.md); print
  [`../handouts/spot-the-bug.md`](../handouts/spot-the-bug.md) and
  [`../handouts/glossary.md`](../handouts/glossary.md).
- **Students:** none. They leave with
  [`../handouts/setup.md`](../handouts/setup.md).

## Schedule

| Time | Min | Block | Format |
|---|---|---|---|
| 18:00 | 10 | Welcome + icebreaker poll | Interactive poll |
| 18:10 | 25 | Why software fails: security as motivation | Lecture + **demo: getpassword.c** |
| 18:35 | 15 | Exercise 1: Spot the bug | Pairs + debrief |
| 18:50 | 25 | Testing vs. verification: soundness & completeness | Lecture + think-pair-share |
| 19:15 | 10 | **Break** | — |
| 19:25 | 25 | From programs to formulas: SAT, SMT, Z3 | Lecture + **demo: z3_demo.py** |
| 19:50 | 25 | Bounded model checking | Lecture + **demo: offbyone.c** |
| 20:15 | 15 | Exercise 2: Predict the verdict | Groups + live runs of `predict/` |
| 20:30 | 20 | Landscape + industry reality | Lecture + discussion |
| 20:50 | 10 | Closing quiz, recap, Session 2 setup | Quiz |

## Block notes

**18:00 Icebreaker.** Poll: *"Name a software failure that made the
news."* Cluster on screen (safety: Therac-25, Ariane 5, Toyota; security:
Heartbleed, WannaCry, log4shell). Message: ordinary programming errors,
extraordinary consequences, well-tested code.

**18:10 Why software fails** *(lecture 1)*. Show `getPassword` (slide
~35); ask the room for the bug *before* explaining. Buffer overflow →
password bypass. Zoom out: CIA triad, safety vs. security, the 70%
memory-safety figure (lecture 2). **Demo:**
`esbmc getpassword.c --unwind 8` — the tool finds the overflow and names
the CWE classes. "Both evenings explain how that command works."

**18:35 Exercise 1** — run per
[`../handouts/spot-the-bug.md`](../handouts/spot-the-bug.md); answers in
[`quizzes.md`](quizzes.md). Debrief punchline: *you found these by being
clever — would you, in 2 million lines?*

**18:50 Testing vs. verification** *(lecture 3)*. Dijkstra's maxim made
concrete: two 32-bit `int` arguments = 2⁶⁴ exhaustive tests. Verification vs.
validation, then the **sound × complete** grid. Think-pair-share (5 min):
place testing / code review / compiler warnings / "prove it" on the grid.
Honesty point: every practical tool gives something up — BMC gives up
unbounded soundness, abstract interpretation gives up completeness,
testing gives up both.

**19:25 Programs → formulas** *(lectures 3–4)*. SAT in one slide → SMT
theories (bit-vectors, arrays, floats). **Demo:** `python3 z3_demo.py` —
a model in milliseconds, then an `unsat` proof. Frame: *a search engine
for maths*; verification asks "is there an input that violates my
assertion?"

**19:50 BMC** *(lecture 4)*. Four slides: unwind loops → SSA → guarded
assignments → give C ∧ ¬P to the solver. SAT = bug + counterexample;
UNSAT = safe *up to the bound*. **Demo:**
`esbmc offbyone.c --unwind 7`; walk the trace to `i = 5`. If ahead of
schedule, show `--unwind 3` and the unwinding assertion.

**20:15 Exercise 2.** Hand groups the three `predict/` programs on paper.
Each group writes a verdict + line number per file. Show of hands per
file, then run live. `predict3.c` is correct by design — don't let "the
tool always complains" take root.

**20:30 Landscape.** One slide per technique with flagship deployment:
BMC/model checking (AWS s2n & kernel CI, ESBMC/CBMC, SV-COMP), symbolic
execution (KLEE/coreutils, Microsoft SAGE), abstract interpretation
(Astrée/A380), interactive proof (seL4, CompCert), fuzzing (AFL,
OSS-Fuzz; lecture 5). Discussion: *"why isn't all software verified?"* —
let the room produce cost/scalability/spec-effort; add legacy and culture.

**20:50 Close.** Quiz from [`quizzes.md`](quizzes.md); distribute
[`../handouts/setup.md`](../handouts/setup.md). Contract: *arrive with
tools installed, or come at 17:45.*

## Contingencies

Behind schedule → cut Exercise 2 (it is rehearsed by Lab 2 anyway).
Never cut the break. Demos die → screenshots of every expected output are
reconstructible from `solutions/expected-verdicts.md`; keep a copy open.

---

# Session 2 — Hands-On Verification

## Learning objectives

Participants can: (1) check satisfiability and prove small equivalences
with Z3's Python API; (2) run ESBMC to find overflows, leaks, and
assertion violations, and read the counterexample; (3) write specs with
`assert`/`nondet_int`/`__ESBMC_assume`; (4) choose and justify an unwind
bound; (5, stretch) expose a concurrency bug via interleaving search.

## Preparation

- **Instructor:** TAs briefed (1 per ~15 students); whiteboard scoreboard
  for Lab 4; `solutions/` folder open on your machine; venue dry-run of
  `labs/` top to bottom.
- **Students:** [`../handouts/setup.md`](../handouts/setup.md) completed.
  Doors open 17:45 for triage.

## Schedule

| Time | Min | Block | Material |
|---|---|---|---|
| 18:00 | 15 | Recap quiz + environment smoke test | `quizzes.md`; `esbmc lab4/float.c` |
| 18:15 | 35 | **Lab 1:** Constraint solving with Z3 | `labs/lab1/` |
| 18:50 | 40 | **Lab 2:** Bug hunting with ESBMC | `labs/lab2/` |
| 19:30 | 10 | **Break** | — |
| 19:40 | 35 | **Lab 3:** Writing specifications | `labs/lab3/` |
| 20:15 | 30 | **Lab 4:** Team challenge | `labs/lab4/` |
| 20:45 | 15 | Debrief, where next, feedback | — |

## Block notes

**18:00.** Recap poll while everyone runs the smoke tests. Broken machine
⇒ pair up; pairs are the unit all evening anyway.

**18:15 Lab 1.** Demo Stage 1a yourself, then circulate. Checkpoint
question on screen before Lab 2: *"what does unsat mean in Stage 1 vs.
Stage 3?"* Watch for: students treating `unsat` as failure (it is the
proof!).

**18:50 Lab 2.** Strict predict → verify → fix → re-verify loop; lab
sheet has per-file pacing checkpoints (19:05 / 19:20). Deputize fast
pairs as helpers, explicitly. Common stalls: forgetting `--unwind` on
`vla.c` (point at the cheatsheet), "fixing" `vla.c` only one of two ways
(the sheet warns).

**19:40 Lab 3.** The pivotal moment is step 1: the buggy program verifies
SUCCESSFUL because the shipped spec is weak. Make the room say out loud
what a green verdict actually means *before* they write properties 3–4.
End with the whole-room `unwind.c` discussion (5/20/60) — the most
important 5 minutes of the evening. Key subtlety: at `--unwind 60` the
unwinding assertion passes, so that run is a *complete* proof for this
program; the bound was big enough to cover every execution. The stretch
task has students discover that `--k-induction` answers
`VERIFICATION UNKNOWN` — use it to introduce loop invariants and why
unbounded proofs are fundamentally harder.

**20:15 Lab 4.** Teams pick Track A (concurrency) or B (floating point).
Run the scoreboard visibly. With 10 minutes left, walk one thread-schedule
counterexample on the projector regardless of team progress.

**20:45 Debrief.** Round-the-room: one thing the tool caught that you
wouldn't have. Recap the arc *intuition → concepts → tools → application*.
Where next: SV-COMP benchmarks, full COMP63342 materials, ESBMC/CBMC
docs, fuzzing (lecture 5) as the complementary technique. 3-question
feedback poll.

## Contingencies

Installs fail en masse → pair up (Plan A, not a fallback of shame); Z3
works in the browser playground. Behind schedule → Lab 4 becomes a
10-minute instructor demo of `race.c`; Labs 2 and 3 must survive intact.
Mixed pace → every lab has numbered files plus a stretch task.

---

# Optional extensions for advanced students

1. **DNN verification** *(AI-security guest deck)* — adversarial
   robustness as verification; MNIST '8'→'5'; VNN-COMP. 15-min teaser or
   take-home.
2. **k-induction and loop invariants** — run
   `esbmc labs/lab3/unwind.c --k-induction` and study why it answers
   `VERIFICATION UNKNOWN` (verified on ESBMC 8.3.0): the assertion is
   not k-inductive on its own, so the tool would need an auxiliary
   invariant (`sum == 2*i`). Have students state the invariant and
   discuss how deductive verifiers (Frama-C/ACSL, Dafny) consume it.
3. **Floating-point deep dive** — derive C ∧ ¬P by hand for `float.c`
   under the FP theory.
4. **LTL and mutual exclusion** *(CW01 Q3)* — safety/liveness for a
   mutex algorithm in temporal logic.
5. **Sequentialization** *(CW04 Q2)* — the Lal–Reps reduction behind
   concurrent BMC.
6. **SV-COMP safari** — run ESBMC on three benchmarks from
   sv-comp.sosy-lab.org; compare with published verdicts.

# Expected outcomes

After both sessions every participant has: solved constraints with Z3,
found and fixed at least two memory-safety bugs from counterexamples,
written nondet-based specifications and seen why weak specs verify
"successfully", justified an unwind bound, and watched a concurrency or
floating-point bug defeat intuition. They can explain sound vs. complete,
what `unsat` proves, and where these tools run in industry.
