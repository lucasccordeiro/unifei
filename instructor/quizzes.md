# Polls, Quizzes, and Exercise Answers (instructor only)

## Session 1, 18:00 — Icebreaker

Open question: *"Name a software failure that made the news."*
Cluster live into **safety** (Therac-25, Ariane 5 flight 501, Toyota
unintended acceleration, Boeing 737 MAX/MCAS) and **security**
(Heartbleed, WannaCry/EternalBlue, log4shell, Equifax/Struts). Point out
how many were ordinary memory or logic errors in heavily tested code.

## Session 1, 18:35 — Spot the Bug: answers

Snippet from `handouts/spot-the-bug.md` (CW01 Q1):

1. `++zPtr;` — `zPtr` is **uninitialised**; arithmetic on an
   indeterminate pointer is undefined behaviour even without
   dereferencing.
2. `number = zPtr;` — assigns a **pointer to an int** without a cast;
   loses provenance, truncates on LP64.
3. `number = *zPtr[2];` — `zPtr[2]` is an `int`, so `*` dereferences an
   **int as a pointer** (type error); and it indexes off an uninitialised
   pointer anyway.
4. `number = *sPtr;` — dereference of a **`void *`**: illegal C, no
   object type to read.
5. `++z;` — an **array name is not a modifiable lvalue**; arrays are not
   pointers.
6. `aPtr` is initialised to NULL and never reassigned — any later
   dereference is a **NULL dereference**; also a dead variable.
7. (bonus) `number` and `i` are read nowhere / uninitialised pattern —
   invite discussion of what the compiler vs. a verifier flags.

Consequences to draw out: the compiler already refuses 3, 4, and 5
(constraint violations); the interesting ones are those it happily
accepts — silent corruption / arbitrary read (1), portability time-bombs
(2, often a mere warning), and a latent crash (6). Lesson: the compiler
catches type errors, not behaviour errors.

## Session 1, 20:15 — Predict the Verdict: answers

| File | Verdict | Why |
|---|---|---|
| `predict1.c` | FAILED | loop runs to `size+1` → writes one past the VLA when `size == n`; additionally the first call is `foo(0, …)` — a zero-sized VLA |
| `predict2.c` | FAILED | global `int *a` is NULL (never allocated); `foo` writes through it once `n = 2` |
| `predict3.c` | SUCCESSFUL | the assertion `sum == 20` holds; included so the tool is seen agreeing with correct code |

## Session 1, 20:50 — Closing quiz (with answers)

1. *A tool that never raises a false alarm is called…?*
   **Complete.** (Sound = never misses a real bug.)
2. *ESBMC returns UNSAT for C ∧ ¬P with `--unwind 10`. What do we know?*
   **No execution within 10 loop iterations violates P.** Nothing about
   iteration 11. (Sharp-student caveat: ESBMC's unwinding assertions are
   on by default, so an actual `VERIFICATION SUCCESSFUL` verdict at
   `--unwind 10` additionally certifies that 10 iterations covered every
   execution — that distinction is exactly Lab 3, Part 2.)
3. *What does a counterexample contain?*
   **Concrete input values and a step-by-step failing execution trace**
   (for concurrent programs: the thread schedule too).
4. *Which technique proved absence of runtime errors in Airbus A380
   flight-control code?* **Abstract interpretation (Astrée).**
5. *Why can't testing prove the `getPassword` program safe?*
   **The input space is unbounded/astronomical; testing samples it,
   verification covers it exhaustively (up to a bound).**

## Session 2, 18:00 — Recap quiz (with answers)

1. *To prove property P with a solver, you ask whether…?*
   **¬P is satisfiable; unsat ⇒ P holds.**
2. *sat + model in that setup means…?* **A counterexample to P.**
3. *`--unwind 5` reports a violated "unwinding assertion". Is the program
   buggy?* **Unknown — the bound was too small; raise it.**

## Session 2, 20:45 — Feedback poll

1. Pace: too slow / right / too fast?
2. Which lab taught you the most? (1 / 2 / 3 / 4)
3. One thing to change for the next cohort. (free text)
