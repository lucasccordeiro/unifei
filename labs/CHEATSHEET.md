# ESBMC Cheatsheet — Session 2

Run on a C file: `esbmc file.c [flags]`
Verdict is the last lines: `VERIFICATION SUCCESSFUL` or
`VERIFICATION FAILED` + a `[Counterexample]` trace.

## Flags you will need tonight

| Flag | Meaning |
|---|---|
| *(none)* | Bounds, pointer-safety, and division checks plus your `assert`s are already on by default |
| `--unwind N` | Unroll every loop N times. If you see a violated **unwinding assertion**, N was too small — raise it |
| `--memory-leak-check` | Also check that every allocation is eventually freed |
| `--overflow-check` | Also check signed integer overflow |
| `--context-bound N` | (Concurrency) allow up to N context switches between threads |
| `--k-induction` | Try to prove the property for ALL bounds, not just one — may answer `VERIFICATION UNKNOWN`: unbounded proofs are fundamentally harder (extension) |
| `--incremental-bmc` | Keep increasing the bound automatically until a bug or timeout |

## Reading a counterexample

```
State 3 file overflow.c line 21 ...
  i = 2 (00000000 ... 010)        <- the input values the solver chose
...
Violated property:
  file overflow.c line 21 ...
  dereference failure: array bounds violated   <- what went wrong
  CWE: CWE-121, CWE-125, ...                   <- the vulnerability class
```

Read it bottom-up: *what* was violated, then scroll up for *which values*
caused it. Those values are a ready-made failing test case.

## Specification intrinsics (Lab 3)

```c
int nondet_int(void);            /* "any possible int" — untrusted input */
void __ESBMC_assume(_Bool);      /* declare once, then: */

int x = nondet_int();            /* x is every value at once...        */
__ESBMC_assume(x > 0 && x < 100);/* ...now it is every value in 1..99  */
assert(property(x));             /* must hold for ALL remaining values */
```

## If you are stuck

1. Re-read the violated property line — it names the file, line, and kind.
2. `--unwind` too small? The output names the loop it gave up on.
3. Still stuck for >5 min: ask a TA or the pair next to you.
