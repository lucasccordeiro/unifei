# Expected Tool Verdicts (verified)

Every row below was executed with **ESBMC 8.3.0** (aarch64 macOS) and
**Z3 4.16.0** on 2026-06-11. If a venue machine disagrees, suspect the
ESBMC version first.

## Buggy files (as shipped to students)

| File | Command | Verdict | Violated property |
|---|---|---|---|
| `session1-demos/getpassword.c` | `esbmc getpassword.c --unwind 8` | FAILED | `dereference failure: array bounds violated` in `gets` model; CWE-121/125/129/131/193/787 |
| `session1-demos/offbyone.c` | `esbmc offbyone.c --unwind 7` | FAILED | array bounds violated at `i == 5` |
| `session1-demos/predict/predict1.c` | `esbmc predict1.c --unwind 6` | FAILED | VLA bounds violated |
| `session1-demos/predict/predict2.c` | `esbmc predict2.c --unwind 4` | FAILED | NULL-pointer write via global `a` |
| `session1-demos/predict/predict3.c` | `esbmc predict3.c --unwind 6` | **SUCCESSFUL** | (correct program, by design) |
| `labs/lab2/overflow.c` | `esbmc overflow.c` | FAILED | line-24 `assertion main` — solver picks `i = -1, x = -1`, so the write lands on `a[0]` and `a[1]` keeps its garbage |
| `labs/lab2/leak.c` | `esbmc leak.c --memory-leak-check` | FAILED | `forgotten memory` — first `malloc` orphaned by `p = q` |
| `labs/lab2/vla.c` | `esbmc vla.c --unwind 6` | FAILED | VLA bounds violated |
| `labs/lab2/getpassword.c` | `esbmc getpassword.c --unwind 8` | FAILED | as above |
| `labs/lab3/triangle.c` *(as shipped, TODOs empty)* | `esbmc triangle.c` | **SUCCESSFUL** | deliberate — weak spec, green verdict. The lab's punchline. |
| `labs/lab3/unwind.c` | `--unwind 5` / `--unwind 20` | FAILED | *unwinding assertion* (bound too small — not a program bug) |
| `labs/lab3/unwind.c` | `--unwind 60` | **SUCCESSFUL** | loop fully unwound (MAX=50 < 60) — a complete proof for this program |
| `labs/lab3/unwind.c` | `--k-induction` | **UNKNOWN** | "Unable to prove or falsify" — deliberate stretch-task outcome; the assertion is not k-inductive without the invariant `sum == 2*i` |
| `labs/lab4/race.c` | `esbmc race.c --context-bound 2` | FAILED | `assert(g == 1)` in t1 under interleaving t1:g=1 → t2:g=2 → t1:assert |
| `labs/lab4/float.c` | `esbmc float.c` | FAILED | `assert(w == z)` — 0.1+0.2 ≠ 0.3 in binary64 |

## Triangle, mid-lab state (buggy classify + completed properties)

`esbmc triangle.c` ⇒ **FAILED**. Observed counterexample:
`a = 512, b = 256, c = 768` — `classify(512,256,768)` correctly returns 4
(since 512+256 ≤ 768), but `classify(768,256,512)` misses the
`b + c <= a` case and returns 3; Property 4 (permutation invariance) is
violated. Other runs may surface Property 3 directly with inputs like
`a=999, b=1, c=1` — both are correct outcomes of the same seeded bug.

## Fixed files (this folder)

| File | Command | Verdict |
|---|---|---|
| `overflow_fixed.c` | `esbmc overflow_fixed.c` | SUCCESSFUL |
| `leak_fixed.c` | `esbmc leak_fixed.c --memory-leak-check` | SUCCESSFUL |
| `vla_fixed.c` | `esbmc vla_fixed.c --unwind 6` | SUCCESSFUL |
| `getpassword_fixed.c` | `esbmc getpassword_fixed.c --unwind 10` | SUCCESSFUL — note `--unwind 10`, not 8: this fix enlarges the buffer to `char buf[8]`, so the `fgets` model needs more iterations. A minimal fix that keeps `buf[4]` verifies at `--unwind 8`. The lab sheet flags this. |
| `triangle_solution.c` | `esbmc triangle_solution.c` | SUCCESSFUL (~0.5 s) |
| `race_fixed.c` | `esbmc race_fixed.c --context-bound 2` | SUCCESSFUL |

## Python

- `session1-demos/z3_demo.py` — Query 1 prints a model (e.g. `x = 101`),
  Query 2 prints `unsat`.
- `labs/lab1/lab1.py` *(as shipped)* — Stage 1: 1a/1b EQUIVALENT, 1c NOT
  equivalent with counterexample `[b = False]`; Stage 2 prints nothing
  until the TODO is done; Stage 3 finds the overflow counterexample
  `x = 1073741824 → z` negative/huge.
- `instructor/solutions/lab1_solution.py` — Stage 1 adds 1d NOT
  equivalent; Stage 2 prints the unique model `9567 + 1085 = 10652`;
  Stage 3 Q3 prints `sat` (overflow persists even with `x >= 0`).

## Box B — optional ESBMC-on-Python exercises (verified 2026-06-13, ESBMC 8.3.0)

These run under **`esbmc`**, not `python3` (`nondet_int` / `__ESBMC_assume`
are ESBMC intrinsics). Same evening trick, Python input.

| File | Command | Verdict | Notes |
|---|---|---|---|
| `labs/lab1/stage3_esbmc.py` | `esbmc stage3_esbmc.py` | FAILED | `assertion z >= 2`; counterexample `x = 9223372036854775807` (2⁶³−1). ESBMC's **default** models a Python `int` as a 64-bit machine word, so the witness is 2⁶³ (vs 2³⁰ in the 32-bit `BitVec` Z3 version). Q2 stretch (`__ESBMC_assume(x >= 0)`) still FAILS at the same value. **Caveat:** this 2⁶³ overflow does **not** reproduce in real CPython — Python ints are arbitrary-precision, so `z` stays huge and `z >= 2` holds. |
| `labs/lab1/stage3_esbmc.py` | `esbmc stage3_esbmc.py --ir` | FAILED | Same property, but `--ir` uses **unbounded** integer/real arithmetic (matches CPython's bignums; help: "overapproximating normal integers/reals while significantly boosting performance"). Witness becomes `x = -1` → `z = 0 < 2`, which **does** reproduce in real CPython. `--ir-ieee` (integers unbounded, reals pinned to IEEE-754) gives the same `x = -1` here since the example has no reals. |
| `labs/lab2/safe_div.py` | `esbmc safe_div.py` | FAILED | `division by zero`, CWE-369; solver picks `b = 0`. Fix = add `__ESBMC_assume(b != 0)` ⇒ **SUCCESSFUL**. |
