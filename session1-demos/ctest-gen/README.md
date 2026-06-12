# Session 1 demo — ESBMC test-case generation

Companion to the slide **"From counterexample to a runnable test."** It shows
ESBMC *finding* an input that bypasses the password check and emitting it as a
concrete, runnable test — no one has to guess the right input.

Docs: <https://esbmc.github.io/docs/c-cpp/ctest-gen/>

## Files

| File | Origin | Purpose |
|------|--------|---------|
| `getpassword.c` | authored | the access check + the "no bypass" claim ESBMC tries to break |
| `test_case.c` | generated | concrete `__VERIFIER_nondet_char` replaying the bypassing input |
| `CMakeLists.txt` | generated | links the source with the test case under CTest |
| `esbmc_verifier.h` | generated | declarations force-included during the native build |

`test_case.c`, `CMakeLists.txt`, and `esbmc_verifier.h` are committed as a
reference, but they are **regenerated** by step 1 below.

## Step 1 — let ESBMC find a bypassing input and write the test

```bash
esbmc getpassword.c --unwind 8 --generate-ctest-testcase
```

`getpassword.c` claims the *access-granted* branch is unreachable (`assert(0)`
inside it). ESBMC disproves that claim, reports `VERIFICATION FAILED`, and
writes `test_case.c` whose `__VERIFIER_nondet_char()` replays the input that
gets in:

```c
static const char v[] = { 83, 77, 84 };   /* 'S','M','T' → "SMT" */
```

## Step 2 — build and run the generated test (no ESBMC needed)

```bash
mkdir build && cd build
cmake .. && cmake --build .
./test_case
```

Expected output:

```
Access Granted with input "SMT"
Assertion failed: (0), function main, file getpassword.c, line 45.
```

The program reaches the protected branch — it prints the bypassing input ESBMC
found, then aborts on `assert(0)`. The abort is the point: the witness
*reproduces* the access-control bypass. Running it under CTest

```bash
ctest --output-on-failure
```

therefore reports the test as **failed (subprocess aborted)** — the expected,
correct signal that the bypass is reachable. A green run would mean no input
could get past the check.
