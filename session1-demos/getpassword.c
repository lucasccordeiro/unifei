/*
 * Session 1 motivating example (COMP63342, lecture 1).
 * A 4-byte buffer read with gets() lets an attacker smash the stack
 * and bypass the password check.
 *
 * Demo:   esbmc getpassword.c --unwind 8
 * Expect: VERIFICATION FAILED (buffer overflow in gets)
 * Note:   the unwind bound caps the unbounded input loop inside the
 *         gets() model — a first taste of "bounded" model checking.
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *gets(char *s); /* removed from C11 precisely because it is unsafe */

int getPassword(void)
{
  char buf[4];
  gets(buf);
  return strcmp(buf, "SMT");
}

int main(void)
{
  int x = getPassword();
  if (x) {
    printf("Access Denied\n");
    exit(0);
  }
  printf("Access Granted\n");
  return 0;
}
