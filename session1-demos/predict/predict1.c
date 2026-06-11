/*
 * Exercise 2 (Predict the verdict) — snippet 1 of 3.
 * Based on COMP63342 CW02 Q1 (variable-length automatic arrays).
 *
 * Predict: does the model checker report a bug? At which line?
 *
 * Run:    esbmc predict1.c --unwind 6
 */
int foo(int n, int b[], int size)
{
  int a[n], i;
  for (i = 0; i < size + 1; i++)
    a[i] = b[i];
  return i;
}

int main(void)
{
  int i, b[4];
  for (i = 0; i < 4; i++)
    b[i] = foo(i, b, i);
  return 0;
}
