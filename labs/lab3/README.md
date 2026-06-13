# Lab 3 — Writing Your Own Specifications (35 min)

Lab 2 found *crashes*. This lab verifies *intent* — and intent is something
**you** must write down. The tool only checks what you specify.

## Part 1: `triangle.c` (~25 min)

`classify(a,b,c)` should return 1 = equilateral, 2 = isosceles,
3 = scalene, 4 = invalid. The implementation has a **seeded bug**.

1. Run `esbmc triangle.c` as given. It says `VERIFICATION SUCCESSFUL`.
   **Discuss with your partner: does that mean the code is correct?**
2. Read the harness in `main()`: nondeterministic sides, bounded to
   1..999 with `__ESBMC_assume`. Two properties are already written.
3. Write the two TODO properties (3: violated triangle inequality ⇒
   result 4; 4: argument order must not matter).
4. Re-run. Read the counterexample: which triangle exposes the bug?
   Check it by hand — is it really misclassified?
5. Fix `classify()` and re-run to `VERIFICATION SUCCESSFUL`.

The lesson of step 1 is the most important one tonight: *a green verdict
means "no specified property can be violated" — with a weak spec, green is
cheap.*

## Part 2: `unwind.c` — what did we actually prove? (~10 min, whole room)

```bash
esbmc unwind.c --unwind 5
esbmc unwind.c --unwind 20
esbmc unwind.c --unwind 60
```

- At 5 and 20: the *unwinding assertion* fails. What is the tool telling
  you? (Not that the program is buggy!)
- At 60: `VERIFICATION SUCCESSFUL` — and because the unwinding assertion
  passed (60 > MAX = 50), this is a **complete proof** for this program.
- **Stretch:** now imagine `MAX` were 2³¹−1, so no feasible `--unwind`
  could ever cover the loop. Try `esbmc unwind.c --k-induction`: on
  ESBMC 8.3.0 it answers `VERIFICATION UNKNOWN` — it can neither prove
  nor refute. Why is the unbounded question fundamentally harder than
  the bounded one? (Keyword to take home: *loop invariant*.)

## Part 3 (optional): function contracts — `contract.c`

Specify the **function**, not every call site. A contract attaches the
spec to the function itself:

- `__ESBMC_requires(P)` — the precondition the caller must establish.
- `__ESBMC_ensures(Q)` — the postcondition the function promises
  (`__ESBMC_return_value` is the result).

`contract.c` defines `clamp(x, lo, hi)` with a contract and a **seeded
bug**. Two complementary checks:

```bash
esbmc contract.c --enforce-contract clamp          # does the body keep its promise?
esbmc contract.c --replace-call-with-contract clamp # verify callers from the contract alone
```

1. `--enforce-contract` → `VERIFICATION FAILED`, `contract ensures`. Read
   the counterexample, fix `clamp` (the `x > hi` branch), re-run to
   `SUCCESSFUL`.
2. `--replace-call-with-contract` replaces the call by *assume requires;
   havoc; assume ensures* — the body is **not** re-analysed. That is
   **modular** (assume-guarantee) verification: enforce a contract once,
   then every caller reasons against it. This is deductive verification's
   core idea (Session 1: Dafny, Frama-C/WP, SPARK).

**Gotcha:** a contract is only checked if the function is **reachable** —
`main()` must call it, or `--enforce-contract` has nothing to do and
reports `SUCCESSFUL` vacuously.
