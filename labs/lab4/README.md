# Lab 4 — Team Challenge (30 min, teams of 3–4)

Scoring (whiteboard): **1 point** per correctly predicted verdict
(written down *before* running), **2 points** per fixed-and-verified file.

## Track A — Concurrency: `race.c`

1. Read the program. **Before running anything**, write down as a team:
   can the `assert(g == 1)` in `t1` fail? If yes, write the exact
   interleaving (order of statements across threads) that breaks it.
2. Check yourselves: `esbmc race.c --context-bound 2`
3. The counterexample contains **thread schedules** — find the context
   switch that kills the assertion. Compare with your prediction.
4. (2 points) Fix it with a `pthread_mutex_t` so the write and the check
   are atomic; re-verify with the same command.

Sequentially this program is bulletproof — you could run it a million
times and never see the bug. The model checker tries *every interleaving*.

## Track B — Floating point: `float.c`

1. Read the assertion. It looks like primary-school arithmetic.
   **Predict the verdict as a team.**
2. `esbmc float.c`
3. (1 point) Explain *why* in one sentence to the instructor.
   Hint: 0.1 in binary is what 1/3 is in decimal.
4. (Stretch) Find the smallest change that makes it verifiable. Is using
   `==` on doubles ever a good idea? What do real codebases do instead?

## Done early?

- Swap tracks.
- Or: run `esbmc ../lab3/unwind.c --k-induction` (it answers
  `VERIFICATION UNKNOWN`) and explain to a TA (a) why the `--unwind 60`
  run was nevertheless a complete proof for that program, and (b) what a
  tool would need to know to prove the loop for *unbounded* `MAX`.
