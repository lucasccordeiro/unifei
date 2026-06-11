# Lab 2 — Bug Hunting with ESBMC (40 min)

Four C programs, strictly increasing difficulty. For each one:
**predict → verify → read the counterexample → fix → re-verify to green.**
A file is "done" when ESBMC prints `VERIFICATION SUCCESSFUL` on your fixed
version *with the same flags*.

| # | File | Command | You should be here by |
|---|---|---|---|
| 1 | `overflow.c` | `esbmc overflow.c` | — |
| 2 | `leak.c` | `esbmc leak.c --memory-leak-check` | 19:05 |
| 3 | `vla.c` | *you choose the flags* (hint: it has loops) | 19:20 |
| 4 | `getpassword.c` | `esbmc getpassword.c --unwind 8` | stretch |

## Per-file notes

**1. `overflow.c`** — `i` and `x` are never initialised, so the model
checker treats them as *any value* (exactly what an attacker controls).
Write down the values the solver picked before you fix anything.

**2. `leak.c`** — the leak is one aliasing assignment. Which `malloc` can
never be freed, and why?

**3. `vla.c`** — two distinct problems. One is a wrong loop bound; the
other is about the very first call from `main` (what size does the array
`a` have on that call?). Fix both; partial fixes still fail.

**4. `getpassword.c`** — Session 1's opening demo, now yours. Fix it
properly: `fgets(buf, sizeof(buf), stdin)`, and mind the trailing newline
(`strcspn`). Re-verify. If you also enlarged the buffer, raise `--unwind`
to match (a `char buf[8]` needs `--unwind 10`) — can you explain why the
bound depends on your fix? That question is the bridge to Lab 3.

## Checkpoint

For one of your fixed files, explain to your partner *what the tool now
guarantees* — and what it still doesn't (think: bounds, environment).
