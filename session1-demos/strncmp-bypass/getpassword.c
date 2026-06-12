/*
 * Session 1 demo: a LOGIC-FLAW access-control bypass.
 *
 * ESBMC finds an input that gets in WITHOUT being the password — no buffer
 * overflow, no guessing the secret. The check is just wrong.
 *
 * The bug: it compares only strlen(buf) characters
 *     strncmp(buf, "SMT", strlen(buf)) == 0
 * so any *prefix* of the password passes — and the empty string is a
 * prefix of everything. For buf = "", strlen is 0, strncmp compares zero
 * characters and returns 0, so whoever typed nothing is let in.
 *
 *   1. Search for a non-password input that gets in, and write the test:
 *        esbmc getpassword.c --unwind 8 --generate-ctest-testcase
 *      We claim "no wrong input is ever accepted"; ESBMC disproves it and
 *      writes test_case.c with the bypassing input it found.
 *
 *   2. Build and run that test natively (no ESBMC needed):
 *        mkdir build && cd build && cmake .. && cmake --build .
 *        ./test_case        # prints the bypass, then aborts on assert(0)
 *
 * Docs: https://esbmc.github.io/docs/c-cpp/ctest-gen/
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>

char __VERIFIER_nondet_char(void);

/* BUG: compares only strlen(buf) characters, so a prefix of the password
 * — including the empty string — is accepted as correct. */
int access_granted(const char *buf)
{
  return strncmp(buf, "SMT", strlen(buf)) == 0;
}

int main(void)
{
  /* An unknown input ESBMC gets to choose (NUL-terminated to stay in
   * bounds). */
  char buf[4];
  for (int i = 0; i < 3; i++)
    buf[i] = __VERIFIER_nondet_char();
  buf[3] = '\0';

  /* Reached only if a NON-password input is accepted — a true bypass. */
  if (access_granted(buf) && strcmp(buf, "SMT") != 0)
  {
    printf("Bypass! Access granted to non-password input \"%s\"\n", buf);
    assert(0); /* claim: unreachable. ESBMC finds the bypassing input. */
  }

  printf("Denied (or the one correct password)\n");
  return 0;
}
