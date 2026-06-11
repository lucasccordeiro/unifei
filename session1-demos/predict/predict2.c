/*
 * Exercise 2 (Predict the verdict) — snippet 2 of 3.
 * Based on COMP63342 CW02 Q1 (dynamic memory allocation).
 *
 * Predict: does the model checker report a bug? At which line?
 *
 * Run:    esbmc predict2.c --unwind 4
 */
#include <stdlib.h>

int *a;
int n;

void foo(void)
{
  int i;
  for (i = 0; i < n; i++)
    a[i] = -1;
}

int main(void)
{
  n = 2;
  foo();
  return 0;
}
