/* Session 1 demo: ESBMC derives the password that grants access, and
 * emits it as a runnable CTest test case.
 *
 *   1. Generate the witness as a test case:
 *        esbmc getpassword.c --unwind 8 --generate-ctest-testcase
 *      ESBMC refutes the "never granted" claim and writes test_case.c
 *      with the concrete input  buf = {83, 77, 84, 0} = "SMT".
 *
 *   2. Build and run that test natively (no ESBMC needed):
 *        mkdir build && cd build && cmake .. && cmake --build .
 *        ctest -V        # the program prints "Access Granted"
 *
 * The assert() below is the security property ESBMC checks; it uses the
 * standard <assert.h> macro so the generated CTest compiles with plain cc.
 *
 * Docs: https://esbmc.github.io/docs/c-cpp/ctest-gen/
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>

char __VERIFIER_nondet_char(void);

int getPassword(void)
{
  char buf[4];
  for (int i = 0; i < 4; i++)
    buf[i] = __VERIFIER_nondet_char();
  buf[3] = '\0';                 /* a terminated 4-byte string */
  return strcmp(buf, "SMT");     /* 0 => "Access Granted" */
}

int main(void)
{
  int granted = (getPassword() == 0);
  printf("%s\n", granted ? "Access Granted" : "Access Denied");

  /* Security property: access must never be granted. ESBMC refutes it
   * and hands back the exact input that does — here, "SMT". */
  assert(!granted);
  return 0;
}
