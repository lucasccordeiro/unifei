# Session 1 — Live Demo Run Sheet (instructor)

All commands tested with ESBMC 8.3.0 / Z3 4.16.0. Dry-run on the venue
machine before 18:00. Expected outputs: see
[`../instructor/solutions/expected-verdicts.md`](../instructor/solutions/expected-verdicts.md).

| When | File | Command | Money shot |
|---|---|---|---|
| 18:10 block (end) | `getpassword.c` | `esbmc getpassword.c --unwind 8` | `dereference failure: array bounds violated` *inside gets* + CWE-787 tag — the tool just found the password bypass on its own |
| 18:10 block (slide "runnable test") | `ctest-gen/getpassword.c` | `esbmc getpassword.c --unwind 8 --generate-ctest-testcase`, then `cmake`-build | generates `test_case.c` replaying `"SMT"`; the built binary prints `Access Granted` — the bypass as a runnable test (see `ctest-gen/README.md`) |
| 18:10 block (bonus: logic flaw) | `strncmp-bypass/getpassword.c` | `esbmc getpassword.c --unwind 8 --generate-ctest-testcase`, then `cmake`-build | `strncmp(buf,"SMT",strlen(buf))` accepts any prefix; ESBMC finds `buf=""` (empty string) — a *non-password* bypass. Built binary prints `Bypass! … input ""` (see `strncmp-bypass/README.md`) |
| 19:25 block | `z3_demo.py` | `python3 z3_demo.py` | Query 1: a model in milliseconds. Query 2: `unsat` — a proof, not an opinion |
| 19:25 block (slide "let the solver search") | `send_more_money.py` | `python3 send_more_money.py` | Z3 returns `9567 + 1085 = 10652`; the negation-trick re-check is `unsat` — the answer is unique. The same engine that solves the puzzle finds bugs |
| 19:50 block (end) | `offbyone.c` | `esbmc offbyone.c --unwind 7` | Counterexample trace shows `i = 5` at the failing write — walk it line by line |
| 20:15 exercise | `predict/predict1.c` | `esbmc predict1.c --unwind 6` | FAILED — VLA overflow (two causes: `size+1` bound and the `n=0` first call) |
| 20:15 exercise | `predict/predict2.c` | `esbmc predict2.c --unwind 4` | FAILED — write through the NULL global pointer `a` |
| 20:15 exercise | `predict/predict3.c` | `esbmc predict3.c --unwind 6` | SUCCESSFUL — include one correct program so "the tool always complains" doesn't take root |

Talking points per demo:

- **getpassword:** before running, ask the room for the bug. After
  running, point at the CWE numbers — this maps to the vulnerability
  classes from the security lectures. Then: "everything tonight and next
  week explains how this command works." Note what ESBMC does here: it
  finds the **overflow** (CWE-787), not a magic password. The `strcmp`
  check is sound — only `"SMT"` passes (provable); the only non-`"SMT"`
  way in is to smash the stack, which ESBMC reports as a bug rather than
  synthesising the exploit. For a non-password input that *logically*
  gets in, that's the `strncmp-bypass` demo.
- **ctest-gen:** the sequel to getpassword — ask the tool the *opposite*
  question ("can anyone get in?") and it emits the password as a runnable
  CTest. The assertion abort under `ctest` is the violation reproducing,
  not a tooling error.
- **strncmp-bypass:** the punchline — here the *check itself* is wrong
  (`strncmp(buf,"SMT",strlen(buf))` accepts any prefix). ESBMC finds the
  empty string: access granted to someone who typed nothing. No overflow,
  no guessed secret — just a one-character bug, found in milliseconds.
- **z3_demo:** frame as *search engine for maths*. Query 2 is a proof of
  impossibility — no test suite can ever give you that.
- **offbyone:** this is the BMC pipeline made visible: the `--unwind 7`
  flag is the "bounded" in bounded model checking. Show what happens with
  `--unwind 3` if time allows (unwinding assertion ends the discussion of
  "did we look far enough?").
- **predict:** collect group predictions on a show of hands per file
  BEFORE each run. Misconceptions surfaced here are cheap; in Lab 2 next
  session they cost lab time.
