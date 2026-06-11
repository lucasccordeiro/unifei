/*
 * Lab 3 — writing your own specifications.
 *
 * classify(a, b, c) is SUPPOSED to return:
 *   1 = equilateral, 2 = isosceles, 3 = scalene, 4 = not a valid triangle
 *
 * The implementation below contains a seeded bug. Your job is not to
 * stare at the code — it is to SPECIFY the intended behaviour and let
 * the model checker find the bug for you.
 *
 * Step 1: model arbitrary inputs with nondet_int() and bound them
 *         with __ESBMC_assume (already done below — read it).
 * Step 2: complete the assertions marked TODO.
 * Step 3: esbmc triangle.c
 *         Read the counterexample: which inputs expose the bug?
 * Step 4: fix classify() and re-run until VERIFICATION SUCCESSFUL.
 */
#include <assert.h>

int nondet_int(void);
void __ESBMC_assume(_Bool);

int classify(int a, int b, int c)
{
  /* triangle inequality: every side must be shorter than the sum of
     the other two */
  if (a + b <= c || a + c <= b)
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

  /* keep the search space small and overflow-free */
  __ESBMC_assume(a > 0 && a < 1000);
  __ESBMC_assume(b > 0 && b < 1000);
  __ESBMC_assume(c > 0 && c < 1000);

  int r = classify(a, b, c);

  /* Property 1: the result is always a legal code */
  assert(r >= 1 && r <= 4);

  /* Property 2: three equal sides are always equilateral */
  assert(!(a == b && b == c) || r == 1);

  /* Property 3 (TODO): if ANY triangle inequality is violated,
     the result must be 4. Write it. */

  /* Property 4 (TODO): the result must not depend on the order of
     the sides: classify(a,b,c) == classify(c,b,a). Write it. */

  return 0;
}
