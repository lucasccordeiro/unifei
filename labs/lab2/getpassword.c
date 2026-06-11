/*
 * Lab 2, file 4 of 4 — full circle.
 * This is the very first program you saw in Session 1.
 *
 * Run:    esbmc getpassword.c --unwind 8
 * Tasks:  1. Find the overflow with the tool.
 *         2. Fix it properly (hint: fgets with sizeof) and re-run
 *            until VERIFICATION SUCCESSFUL.
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
