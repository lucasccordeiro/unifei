/* Lab 3 — completed specification AND fixed implementation.
 *
 * The seeded bug: classify() checked only two of the three triangle
 * inequalities (it forgot b + c <= a). The model checker exposes it
 * with inputs like a=999, b=1, c=1, which the buggy version calls
 * "isosceles" instead of "invalid". Both TODO properties catch it:
 * Property 3 directly, Property 4 because classify(1,1,999) != classify(999,1,1).
 *
 * esbmc triangle_solution.c  =>  VERIFICATION SUCCESSFUL
 */
#include <assert.h>

int nondet_int(void);
void __ESBMC_assume(_Bool);

int classify(int a, int b, int c)
{
  if (a + b <= c || a + c <= b || b + c <= a) /* FIX: third inequality */
    return 4;
  if (a == b && b == c)
    return 1;
  if (a == b || b == c || a == c)
    return 2;
  return 3;
}

int main(void)
{
  int a = nondet_int();
  int b = nondet_int();
  int c = nondet_int();

  __ESBMC_assume(a > 0 && a < 1000);
  __ESBMC_assume(b > 0 && b < 1000);
  __ESBMC_assume(c > 0 && c < 1000);

  int r = classify(a, b, c);

  /* Property 1: the result is always a legal code */
  assert(r >= 1 && r <= 4);

  /* Property 2: three equal sides are always equilateral */
  assert(!(a == b && b == c) || r == 1);

  /* Property 3: any violated triangle inequality means "invalid" */
  assert(!(a + b <= c || a + c <= b || b + c <= a) || r == 4);

  /* Property 4: order of sides must not matter */
  assert(classify(a, b, c) == classify(c, b, a));

  return 0;
}
