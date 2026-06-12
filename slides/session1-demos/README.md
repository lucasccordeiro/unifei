# Session 1 demo — ESBMC test-case generation

Companion to the slide **"From counterexample to a runnable test."** It shows
ESBMC deriving the password that grants access and emitting it as a concrete,
runnable test — no one has to guess the right input.

Docs: <https://esbmc.github.io/docs/c-cpp/ctest-gen/>

## Files

| File | Origin | Purpose |
|------|--------|---------|
| `getpassword.c` | authored | the program under test + the security property |
| `test_case.c` | generated | concrete `__VERIFIER_nondet_char` returning `"SMT"` |
| `CMakeLists.txt` | generated | links the source with the test case under CTest |
| `esbmc_verifier.h` | generated | declarations force-included during the native build |

`test_case.c`, `CMakeLists.txt`, and `esbmc_verifier.h` are committed as a
reference, but they are **regenerated** by step 1 below.

## Step 1 — let ESBMC find the input and write the test

```bash
esbmc getpassword.c --unwind 8 --generate-ctest-testcase
```

ESBMC refutes the property `assert(!granted)`, reports `VERIFICATION FAILED`,
and writes `test_case.c` whose `__VERIFIER_nondet_char()` replays the witness:

```c
static const char v[] = { 83, 77, 84, 0 };   /* 'S','M','T','\0' */
```

## Step 2 — build and run the generated test (no ESBMC needed)

```bash
mkdir build && cd build
cmake .. && cmake --build .
./test_case
```

Expected output:

```
Access Granted
Assertion failed: (!granted), function main, file getpassword.c, line 40.
```

The program prints **Access Granted** because ESBMC handed it the exact
password, then aborts on the assertion. The abort is the point: the witness
*reproduces* the security-property violation. Running it under CTest

```bash
ctest --output-on-failure
```

therefore reports the test as **failed (subprocess aborted)** — the expected,
correct signal that the "never granted" property is reachable. A green run
would mean the bypass could not be reproduced.
