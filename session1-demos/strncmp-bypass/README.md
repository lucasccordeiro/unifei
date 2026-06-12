# Session 1 demo — a logic-flaw access-control bypass

A sequel to [`../ctest-gen`](../ctest-gen). There, ESBMC extracted the
hard-coded password. Here the check is simply **wrong**, and ESBMC finds an
input that gets in *without* being the password — the empty string.

Docs: <https://esbmc.github.io/docs/c-cpp/ctest-gen/>

## The bug

```c
int access_granted(const char *buf)
{
  return strncmp(buf, "SMT", strlen(buf)) == 0;   /* compares only strlen(buf) chars */
}
```

Using `strlen(buf)` as the length means **any prefix of the password passes** —
`"S"`, `"SM"`, `"SMT"` … and the empty string, which is a prefix of everything.
For `buf = ""`, `strlen` is `0`, `strncmp` compares zero characters and returns
`0`, so whoever typed nothing is let in.

The harness only reaches the protected branch when the accepted input is *not*
the real password, so a counterexample is a genuine bypass:

```c
if (access_granted(buf) && strcmp(buf, "SMT") != 0)
  assert(0);   /* claim: unreachable — ESBMC breaks it */
```

## Step 1 — let ESBMC find the bypass and write the test

```bash
esbmc getpassword.c --unwind 8 --generate-ctest-testcase
```

ESBMC reports `VERIFICATION FAILED` with `buf = { 0, 0, 0 }` (the empty string)
and writes `test_case.c`:

```c
static const char v[] = { 0, 0, 0 };   /* buf[0] == '\0' → "" */
```

## Step 2 — build and run the generated test (no ESBMC needed)

```bash
mkdir build && cd build
cmake .. && cmake --build .
./test_case
```

Expected output:

```
Bypass! Access granted to non-password input ""
Assertion failed: (0), function main, file getpassword.c, line 50.
```

The program is granted access while typing **nothing**, then aborts on
`assert(0)`. Under `ctest --output-on-failure` the test reports as
**failed (subprocess aborted)** — the expected signal that the bypass is
reachable. A green run would mean the check could not be defeated.

## Talking point

The fix is to compare the *whole* password, not `strlen(buf)` characters:
`strcmp(buf, "SMT") == 0`. The lesson: an "obvious" one-character change to a
comparison opens the door to everyone — and a model checker finds it in
milliseconds, with the worst-case input (the empty string) as proof.
