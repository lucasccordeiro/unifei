/*
 * Session 1 BMC demo: a classic off-by-one.
 * The loop writes a[0] .. a[5], but the array only has indices 0 .. 4.
 *
 * Demo:   esbmc offbyone.c --unwind 7
 * Expect: VERIFICATION FAILED (array bounds violated at i == 5)
 *
 * Walk the counterexample trace with the audience: ESBMC shows the
 * value of i at the failing access.
 */
int main(void)
{
  int a[5];
  for (int i = 0; i <= 5; i++)
    a[i] = i;
  return 0;
}
