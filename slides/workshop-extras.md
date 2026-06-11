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

---

<!-- _class: lead -->

# Formal Verification Workshop

## Session 2 — Hands-On

18:00 – 21:00

*Tonight you drive.*

---

# Recap quiz (while machines boot)

1. To prove property **P** with a solver, you ask whether … is satisfiable?
2. `sat` + a model in that setup means …?
3. `--unwind 5` reports a violated *unwinding assertion*.
   Is the program buggy?

**Smoke test, everyone:** `esbmc lab4/float.c` → `VERIFICATION FAILED`

---

# Tonight

| | | |
|---|---|---|
| 18:15 | **Lab 1** | Constraint solving with Z3 |
| 18:50 | **Lab 2** | Bug hunting with ESBMC |
| 19:30 | *Break* | |
| 19:40 | **Lab 3** | Writing your own specifications |
| 20:15 | **Lab 4** | Team challenge 🏆 |
| 20:45 | | Debrief + where next |

Work in **pairs** · keep `labs/CHEATSHEET.md` open · **predict before you run**

---

# Lab 1 — Constraint solving (35 min)

`labs/lab1/lab1.py` — three stages, instructions inside.

> **The one trick behind the whole evening:**
> to prove **P**, ask the solver if **¬P** is satisfiable.
> `unsat` ⇒ P holds. A model ⇒ a counterexample.

**Checkpoint before Lab 2:** what does `unsat` mean in Stage 1
vs. Stage 3?

---

# Lab 2 — Bug hunting (40 min)

predict → verify → **read the counterexample** → fix → re-verify

| # | File | By |
|---|---|---|
| 1 | `overflow.c` | — |
| 2 | `leak.c` | 19:05 |
| 3 | `vla.c` *(two bugs!)* | 19:20 |
| 4 | `getpassword.c` | stretch |

Done = `VERIFICATION SUCCESSFUL` on your fixed file, same flags.
Finished early? You are now a TA — help the pair next to you.

---

# Lab 3 — Specifications (35 min)

`triangle.c` verifies **SUCCESSFUL** as shipped.

## Does that mean it's correct?

Write the two TODO properties and find out.

*The tool checks what you specify — with a weak spec, green is cheap.*

---

# Lab 3, Part 2 — what did we prove?

```
esbmc unwind.c --unwind 5     → ?
esbmc unwind.c --unwind 20    → ?
esbmc unwind.c --unwind 60    → ?
```

- What is the *unwinding assertion* telling you at 5 and 20?
- At 60 — what exactly is proven, and for which `n`?
- Stretch: `--k-induction` answers `VERIFICATION UNKNOWN`. Why is
  the unbounded question fundamentally harder?

---

# Lab 4 — Team challenge (30 min) 🏆

Teams of 3–4. Points on the whiteboard:

- **1 pt** — verdict predicted correctly *in writing, before running*
- **2 pts** — file fixed and re-verified

**Track A:** `race.c` — write down the failing interleaving first,
then `esbmc race.c --context-bound 2`
**Track B:** `float.c` — primary-school arithmetic. Or is it?

---

# Debrief

- One thing the tool caught that **you** wouldn't have?
- The arc you just walked:
  **intuition → concepts → tools → application**

## Where next

- SV-COMP benchmarks: `sv-comp.sosy-lab.org`
- Full course: COMP63342 Software Security (slides online)
- ESBMC: `esbmc.org` — Z3: `github.com/Z3Prover/z3`
- The complementary technique: **fuzzing** (AFL, OSS-Fuzz)

**Feedback poll: pace / best lab / one improvement. Thank you!**
