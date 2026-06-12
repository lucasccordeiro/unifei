/*
 * Session 1 demo: let ESBMC FIND an input that bypasses the password
 * check, and emit it as a runnable CTest.
 *
 *   1. Search for a bypassing input and write the test:
 *        esbmc getpassword.c --unwind 8 --generate-ctest-testcase
 *      We claim the "access granted" branch is unreachable; ESBMC
 *      disproves it and writes test_case.c with the input that gets in
 *      (here buf = {83, 77, 84, 0} = "SMT").
 *
 *   2. Build and run that test natively (no ESBMC needed):
 *        mkdir build && cd build && cmake .. && cmake --build .
 *        ./test_case        # prints the bypassing input, then aborts
 *
 * The assert(0) marks the protected state as one we claim is
 * unreachable. It uses the standard <assert.h> macro so the generated
 * CTest compiles with plain cc.
 *
 * Docs: https://esbmc.github.io/docs/c-cpp/ctest-gen/
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>

char __VERIFIER_nondet_char(void);

/* The access control: returns 1 iff the supplied password is correct. */
int access_granted(const char *buf)
{
  return strcmp(buf, "SMT") == 0;
}

int main(void)
{
  /* An unknown input ESBMC gets to choose (NUL-terminated to stay in
   * bounds). Can any choice get past the check? */
  char buf[4];
  for (int i = 0; i < 3; i++)
    buf[i] = __VERIFIER_nondet_char();
  buf[3] = '\0';

  if (access_granted(buf))
  {
    printf("Access Granted with input \"%s\"\n", buf);
    assert(0); /* claim: unreachable. ESBMC finds the input that reaches it. */
  }

  printf("Access Denied\n");
  return 0;
}
