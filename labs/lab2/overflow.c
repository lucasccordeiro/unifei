/*
 * Lab 2, file 1 of 4 — buffer overflow.
 * Based on COMP63342 CW03 Q4(a).
 *
 * i and x are never initialised: the model checker treats them as
 * "any possible value" — exactly what an attacker controls.
 *
 * Run:    esbmc overflow.c
 * Tasks:  1. Read the counterexample. Which values did the solver pick
 *            for i and x to break the program?
 *         2. Fix the program (initialise/bound the index, repair the
 *            assertion) and re-run until VERIFICATION SUCCESSFUL.
 */
#include <assert.h>

int main(void)
{
  int a[2], i, x, *p;
  p = a;
  if (x == 0)
    a[i] = 0;
  else
    a[i + 1] = 1;
  assert(*(p + 1) == 1);
  return 0;
}
