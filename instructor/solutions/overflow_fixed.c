/* Lab 2, file 1 — one possible fix.
 * The input x stays untrusted (nondet) — what we fixed is the INDEX,
 * which is now a constant inside the array, and the assertion, which now
 * states what each branch actually establishes. Both branches remain
 * reachable.
 *
 * esbmc overflow_fixed.c   =>  VERIFICATION SUCCESSFUL
 */
#include <assert.h>

int nondet_int(void);

int main(void)
{
  int a[2] = {0, 0};
  int i = 0;
  int x = nondet_int();
  int *p = a;
  if (x == 0)
    a[i] = 0;
  else
    a[i + 1] = 1;
  assert(x == 0 ? *(p + i) == 0 : *(p + i + 1) == 1);
  return 0;
}
