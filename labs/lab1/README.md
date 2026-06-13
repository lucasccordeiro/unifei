# Lab 1 — Constraint Solving with Z3 (35 min)

**File:** [`lab1.py`](lab1.py) — open it; the instructions are inside.
**Run:** `python3 lab1.py` after every change.

The one idea behind the entire evening:

> To **prove** a property P, ask the solver whether **¬P** is satisfiable.
> `unsat` ⇒ P always holds. A model ⇒ a concrete counterexample to P.

## Stages

1. **Equivalence checking (guided, ~10 min).** We do 1a together. You do
   1b–1d. For 1c and 1d, *predict the verdict before running*.
2. **SEND + MORE = MONEY (~10 min).** Complete the arithmetic constraint.
   You are asking the solver to search ~10⁸ assignments; time it.
3. **A C program as a formula (~10 min).** The file encodes a 3-line C
   function as SSA equations and negates its assertion. Run it, then
   answer Q1–Q3 in a comment. You have just done, by hand, what ESBMC
   automates in Lab 2.

## Box B (optional) — hand Stage 3 to ESBMC

ESBMC verifies **Python**, not just C. [`stage3_esbmc.py`](stage3_esbmc.py)
is the *same* function as Stage 3, written in Python — but you no longer
encode SSA equations by hand. You write the function; ESBMC builds the
formula and solves it (with Z3/Bitwuzla underneath).

```
esbmc stage3_esbmc.py        # -> VERIFICATION FAILED
```

- Run it under **`esbmc`**, not `python3` — `nondet_int()` is an ESBMC
  intrinsic, not a CPython function.
- Same bug, **different number**: Z3 Stage 3 reported `x = 2³⁰` (you chose
  a 32-bit `BitVec`); ESBMC reports `x = 2⁶³ − 1`, because it models a
  Python `int` as **64-bit**. Same overflow, different width.
- This is the literal version of "doing ESBMC's job by hand": compare who
  writes the formula and who solves it in each file.

## Checkpoint (before Lab 2)

Be able to answer out loud: *what does `unsat` mean in Stage 1, and what
does it mean in Stage 3?* Same verdict — two different readings. If you
can articulate the difference, you understand verification.

**Stretch:** Stage 3, Q3 — add `s.add(x >= 0)` and explain the result.
(Hint: 32-bit arithmetic wraps. This exact bug class reappears in Lab 2.)
