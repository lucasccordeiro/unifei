/*
 * Lab 2, file 3 of 4 — variable-length array.
 * Based on COMP63342 CW02 Q1 (variable-length automatic arrays).
 *
 * No command given this time — pick your own checks and unwind bound
 * (hint: the outer loop runs 4 times; see CHEATSHEET.md).
 *
 * Tasks:  1. There are TWO distinct problems here. Find both.
 *            (One is a wrong loop bound; one is about the very first
 *             call from main.)
 *         2. Fix and re-run until VERIFICATION SUCCESSFUL.
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
