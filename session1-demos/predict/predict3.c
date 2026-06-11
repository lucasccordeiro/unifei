/*
 * Exercise 2 (Predict the verdict) — snippet 3 of 3.
 *
 * Predict: does the model checker report a bug? At which line?
 *
 * Run:    esbmc predict3.c --unwind 6
 */
#include <assert.h>

int main(void)
{
  int a[5];
  int sum = 0;
  for (int i = 0; i < 5; i++)
    a[i] = 2 * i;
  for (int i = 0; i < 5; i++)
    sum += a[i];
  /* sum of 0,2,4,6,8 */
  assert(sum == 20);
  return 0;
}
