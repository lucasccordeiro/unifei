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
