/*
 * Lab 2, file 2 of 4 — memory leak.
 * Based on COMP63342 CW03 Q4(b).
 *
 * Run:    esbmc leak.c --memory-leak-check
 * Tasks:  1. Which allocation is never freed? Why?
 *         2. Fix the program and re-run until VERIFICATION SUCCESSFUL.
 */
#include <stdlib.h>

int main(void)
{
  char *p = malloc(5);
  char *q = malloc(5);
  p = q;
  free(p);
  p = malloc(5);
  free(p);
  return 0;
}
