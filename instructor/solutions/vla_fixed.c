/* Lab 2, file 3 — fix.
 * Problem 1: the loop ran to size+1, writing one element past a VLA of
 *            size n when size == n.
 * Problem 2: the first call from main is foo(0, b, 0): a VLA of size 0
 *            is undefined behaviour in C, and even one write overflows.
 * Fix: loop strictly below size, never create a zero-sized VLA.
 *
 * esbmc vla_fixed.c --unwind 6  =>  VERIFICATION SUCCESSFUL
 */
int foo(int n, int b[], int size)
{
  if (n <= 0 || size > n)
    return 0;
  int a[n], i;
  for (i = 0; i < size; i++)
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
