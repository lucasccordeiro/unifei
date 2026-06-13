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
*(yes, FAILED — your tool just found a real bug)*

---

# Tonight

| | | |
|---|---|---|
| 18:15 | **Lab 1** | Constraint solving with Z3 |
| 18:50 | **Lab 2** | Bug hunting with ESBMC |
| 19:30 | *Break* | |
| 19:40 | **Lab 3** | Writing your own specifications |
| 20:15 | **Lab 4** | Team challenge |
| 20:45 | | Debrief + where next |

Work in **pairs** · keep `labs/CHEATSHEET.md` open · **predict before you run**

---

# The one trick behind the whole evening

To prove a property **P**, ask the solver whether **¬P** is satisfiable.

- `unsat` ⇒ P always holds *(a proof)*
- a model ⇒ a concrete **counterexample** to P

Everything tonight — Z3 puzzles, ESBMC bug hunts, your own
specifications — is this one move in different costumes.

---

# Another route to a proof: abstract interpretation

Tonight's trick hunts a **counterexample**. Abstract interpretation proves
**P** the other way — **over-approximate every run at once** to a fixpoint
invariant: no bound, no search.

- You met the mechanism in **Session 1**: abstract domain, widening (∇),
  narrowing (Δ) — iterate to a **fixpoint**; if it implies P, P holds for
  **every** run.
- **Sound, not complete:** too coarse an over-approximation → a *false
  alarm*. (Astrée proved the A380 fly-by-wire this way.)
- ESBMC ships it too — `--interval-analysis` — feeding the invariant
  **k-induction** needs for `unwind.c` (Lab 3).

---

# Lab 1 — Constraint solving (35 min)

`labs/lab1/lab1.py` — three stages, instructions inside.

- **Stage 1 (guided):** are these formulas equivalent? Encode `lhs ≠ rhs`,
  ask the solver.
- **Stage 2:** `SEND + MORE = MONEY` — let Z3 search 10⁸ assignments.
- **Stage 3:** a 3-line C function as SSA equations — you are doing
  ESBMC's job by hand.

**Predict before every run:** write your guess as a comment first.
**Box B (optional):** re-run Stage 3 as Python ESBMC checks for you —
`stage3_esbmc.py`.

---

# Z3's Python API — the whole toolkit

```python
from z3 import Bools, Ints, BitVec, Solver, sat, unsat
a, b = Bools("a b")     # symbolic booleans, not values
x = BitVec("x", 32)     # a 32-bit machine integer

s = Solver()
s.add(formula)           # constrain
s.check()                # -> sat or unsat
s.model()                # the witness, when sat
```

Every stage of `lab1.py` is these five calls — nothing else.

---

# Walkthrough: `equivalent()` from lab1.py

```python
def equivalent(lhs, rhs, name):
    slv = Solver()
    slv.add(lhs != rhs)            # can they EVER differ?
    if slv.check() == unsat:       # never differ: a proof
        print(name, "EQUIVALENT")
    else:                          # a witness they differ
        print(name, slv.model())
```

- 1a De Morgan: EQUIVALENT · 1b distribution: EQUIVALENT
- 1c trick question: `NOT equivalent, counterexample: [b = False]`
- Read the model: with `b = False`, `a → (b → a)` is true but `b` is false.

---

# Walkthrough: Stage 3 is ESBMC by hand

```python
x, y, z = BitVec("x", 32), BitVec("y", 32), BitVec("z", 32)
s.add(y == x + 1)        # int y = x + 1;
s.add(z == y * 2)        # int z = y * 2;
s.add(Not(z >= 2))       # assert(z >= 2) — NEGATED
```

`sat` — counterexample e.g. `x = 1073741824` (= 2³⁰)

- `y * 2` overflows the 32-bit range: `z` comes out negative.

Would your test suite have tried 1073741824?

**ESBMC builds exactly this formula from your C — automatically. That's Lab 2.**

---

# Box B: hand that same Python to ESBMC

```python
def f(x: int) -> int:
    y = x + 1
    z = y * 2
    assert z >= 2        # ESBMC negates this for you
x: int = nondet_int()    # every int at once, like BitVec("x")
f(x)
```

`esbmc stage3_esbmc.py` → `VERIFICATION FAILED` (`x = 2⁶³ − 1`)

- You wrote the function; **ESBMC wrote AND solved** the formula.
- Z3 is the SMT engine; ESBMC is a model checker built **on** it — it
  calls Z3 underneath.
- Same overflow, wider word: `2³⁰` (your 32-bit `BitVec`) vs `2⁶³`
  (ESBMC's default 64-bit `int`). But should a Python `int` overflow at
  all? → next slide.

---

# Which integers? machine word vs math (`--ir`)

Both runs print `VERIFICATION FAILED` — but only one counterexample is real
in CPython:

```
esbmc stage3_esbmc.py        →  x = 2⁶³ − 1   default: int = 64-bit machine word
esbmc stage3_esbmc.py --ir   →  x = -1        --ir: unbounded integer/real
```

- **Default** blames `x = 2⁶³−1` — but Python ints are *unbounded*, so that
  overflow never happens (`z` stays huge, `z ≥ 2` holds). A **modelling
  artifact**.
- **`--ir`** blames `x = -1` → `z = 0 < 2` — **reproduces in CPython**:
  `python3 stage3_ir_reproduce.py` → `AssertionError`. Unbounded
  integer/real matches Python's bignums, and is often faster.
- **`--ir-ieee`** adds **IEEE-754** enclosure for *reals* — the honest
  model once floats appear (Lab 4, `float.c`).

Match the integer model to your program. *(Session 1: machine arithmetic ≠
mathematics.)*

---

# Checkpoint before Lab 2

## What does `unsat` mean in Stage 1?
## What does `unsat` mean in Stage 3?

Same verdict — two different questions answered. If you can articulate
the difference, you understand verification.

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

**Box B (optional):** `esbmc safe_div.py` — same loop, Python input.

---

# How to read a counterexample

Real output — `esbmc getpassword.c --unwind 8`:

```
State 1 file getpassword.c line 18 function getPassword thread 0
  buf = { 0, 0, 0, 0 }              ← the state so far
State 2 file ...library/io.c line 91 function gets thread 0
Violated property:
  dereference failure: array bounds violated   ← what broke
  CWE: CWE-121, CWE-125, CWE-129, ...           ← the vuln class
VERIFICATION FAILED
```

Read **bottom-up**: what was violated, then scroll up for which values
caused it.

---

# Deep dive: overflow.c — the trace

```
State 1 ...  a = { 0, -1 }   ← stack garbage in the array
State 2 ...  i = -1          ← the index the solver chose
State 3 ...  x = -1          ← the branch the solver chose
Violated property:
  file overflow.c line 24 ... assertion main
  !((_Bool)((signed long int)(!(p[1] == 1))))
```

- `x = -1` takes the *else* branch; `a[i + 1]` with `i = -1` writes `a[0]`.
- So `a[1]` keeps its garbage (`-1`) and `assert(*(p + 1) == 1)` dies.

`i = -1, x = -1` is a ready-made failing test case — keep it.

---

# Deep dive: what broke, and its CWE

Two shapes of violated property:

- **an assertion** — names *your* line:
  `overflow.c line 24 ... assertion main`
- **a built-in check** — names the bug kind plus its CWE classes:
  `dereference failure: array bounds violated`
  `CWE: CWE-121, CWE-125, CWE-129, CWE-131, CWE-193, CWE-787`
  *(stack overflow · OOB read · bad index · size miscalc · off-by-one · OOB write)*

The path may point inside ESBMC's model of the C library
(`io.c line 91` = the `gets` model).
**That names the API you misused — it is not a bug in ESBMC.**

---

<!-- _class: lead -->

# Break — back at 19:40

---

# Lab 3 — Specifications (35 min)

`triangle.c` verifies **SUCCESSFUL** as shipped.

## Does that mean it's correct?

Write the two TODO properties and find out.

*The tool checks what you specify — with a weak spec, green is cheap.*

---

# Your specification toolkit

```c
int nondet_int(void);              /* any possible int */
void __ESBMC_assume(_Bool);

int x = nondet_int();              /* every value at once */
__ESBMC_assume(x > 0 && x < 100);  /* now: every value in 1..99 */
assert(property(x));               /* must hold for ALL of them */
```

One nondet input = all tests of that input at once.

---

# Lab 3, Part 2 — what did we prove?

```
esbmc unwind.c --unwind 5     → ?
esbmc unwind.c --unwind 20    → ?
esbmc unwind.c --unwind 60    → ?
```

- What is the *unwinding assertion* telling you at 5 and 20?
- At 60 — what exactly is proven, and for which `n`?
- Stretch: `--k-induction` answers `VERIFICATION UNKNOWN`. Why is the
  unbounded question fundamentally harder?
  *(Background deck: `03-k-induction.pptx`)*

---

# Lab 4 — Team challenge (30 min)

Teams of 3–4. Points on the whiteboard:

- **1 pt** — verdict predicted correctly *in writing, before running*
- **2 pts** — file fixed and re-verified

**Track A:** `race.c` — write down the failing interleaving first,
then `esbmc race.c --context-bound 2`
**Track B:** `float.c` — primary-school arithmetic. Or is it?

---

# Why machines beat humans at Track A

- Sequentially, `race.c` is bulletproof — run it a million times, the
  bug may never show.
- Two threads of just 2 and 1 statements already have 3 interleavings;
  real code has billions.
- The model checker enumerates **every** interleaving up to the context
  bound — including the one that kills the assertion.
- The counterexample includes the **thread schedule**: read it as a
  story of who ran when.

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
