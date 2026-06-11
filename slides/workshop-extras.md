---
marp: true
theme: default
paginate: true
style: |
  section { font-size: 26px; }
  h1 { color: #5a0a7a; }
  table { font-size: 22px; }
  code { font-size: 22px; }
---

<!-- _class: lead -->

# Formal Verification Workshop

## Session 1 — Fundamentals and Real-World Applications

18:00 – 21:00

*Built on the COMP63342 Software Security course (University of Manchester)*

---

# Tonight

| | |
|---|---|
| 18:00 | Welcome + a question for you |
| 18:10 | Why software fails |
| 18:35 | **Exercise 1:** spot the bug |
| 18:50 | Testing vs. verification |
| 19:15 | *Break* |
| 19:25 | From programs to formulas: SAT, SMT |
| 19:50 | Bounded model checking |
| 20:15 | **Exercise 2:** predict the verdict |
| 20:30 | Who uses this in the real world? |
| 20:50 | Quiz + what to install for Session 2 |

---

# Icebreaker

## Name a software failure that made the news.

Any failure. Any decade. Shout it out / drop it in the poll.

---

# Exercise 1 — Spot the Bug (15 min)

In **pairs**, 7 minutes, on the handout:

```c
int *zPtr;
int *aPtr = NULL;
void *sPtr = NULL;
int number, i;
int z[5] = {1, 2, 3, 4, 5};
sPtr = z;
++zPtr;
number = zPtr;
number = *zPtr[2];
number = *sPtr;
++z;
```

For each bug: **what** is wrong, and **what could happen at runtime**?
There are at least **six**. Debrief: one bug per pair.

---

# Where does your technique sit?

|  | **Complete** (no false alarms) | Incomplete |
|---|---|---|
| **Sound** (no missed bugs) | the dream | abstract interpretation |
| Unsound | bounded model checking* | testing, code review |

\* *sound up to its bound — tonight's central fine print*

**Think–pair–share (5 min):** place *testing*, *code review*, *compiler
warnings*, and *"prove it with maths"* on this grid. Defend your placement.

---

# Exercise 2 — Predict the Verdict (15 min)

Groups of 3–4. Three short C programs on the handout
(`predict1.c`, `predict2.c`, `predict3.c`).

For each program, write down **before we run anything**:

1. Will the model checker say `VERIFICATION FAILED` or `SUCCESSFUL`?
2. If FAILED — **which line** is the culprit?

Then we run ESBMC live and settle every bet.

---

# Who uses this? — Model checking

- **Amazon Web Services** — CBMC proves memory safety of the TLS
  library **s2n**; bounded proofs run in CI on every commit
- **ESBMC / CBMC** — the tools from tonight's demos; compete yearly
  in **SV-COMP** on tens of thousands of benchmarks
- The counterexample you saw for `getpassword.c` is the same artefact
  AWS engineers read when a proof fails

---

# Who uses this? — Symbolic execution & fuzzing

- **KLEE** found 56 bugs in GNU coreutils — code tested for 15 years
- **Microsoft SAGE** fuzzed Windows file parsers with symbolic
  execution; credited with finding ⅓ of all Win7 file-parsing bugs
- **AFL / OSS-Fuzz** — Google fuzzes ~1,000 open-source projects
  continuously; tens of thousands of bugs found
- Pragmatic cousin of verification: no proofs, ruthless effectiveness

---

# Who uses this? — Proofs all the way up

- **Astrée** (abstract interpretation) proved absence of runtime
  errors in **Airbus A380** fly-by-wire control code
- **seL4** — an OS microkernel with a machine-checked proof of
  functional correctness
- **CompCert** — a C compiler with a proof that compilation
  preserves semantics; fuzzers find **zero** wrong-code bugs in it

---

# Discussion

## If verification can prove the absence of bugs… why isn't all software verified?

*(Let's collect reasons — then I'll tell you which ones the industry actually cites.)*

---

# Closing quiz

1. A tool that never raises a *false alarm* is called …?
2. ESBMC returns UNSAT for **C ∧ ¬P** at `--unwind 10`. What do we know?
3. What's inside a counterexample?
4. Which technique proved the A380 flight-control code free of runtime errors?
5. Why can't testing prove the `getPassword` program safe?

---

# Before Session 2 — 10 minutes of homework

Follow **`handouts/setup.md`** in the repo:

1. `pip install z3-solver`
2. Download ESBMC from <https://github.com/esbmc/esbmc/releases>
3. Smoke test: `esbmc labs/lab4/float.c` → should print
   `VERIFICATION FAILED` *(yes, failed — that's the point)*

**Can't make it work? Come at 17:45 — we'll fix it together.**

<!-- Session 2's authored slides live in session2/01-session2-hands-on.pptx (source: session2/01-session2-hands-on.md, built by build_session2.py). -->
