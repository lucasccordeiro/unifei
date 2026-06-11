/*
 * Lab 3, part 2 — the bounds discussion.
 *
 * The array size is not fixed: it is any value up to MAX.
 * Try increasing --unwind and watch what happens to the verdict and
 * the runtime:
 *
 *   esbmc unwind.c --unwind 5
 *   esbmc unwind.c --unwind 20
 *   esbmc unwind.c --unwind 60
 *
 * Question for the room: which of these runs PROVED something, and
 * what exactly did it prove? What would `--k-induction` buy us?
 */
#include <assert.h>

#define MAX 50

int nondet_int(void);
void __ESBMC_assume(_Bool);

int main(void)
{
  int n = nondet_int();
  __ESBMC_assume(n > 0 && n <= MAX);

  int sum = 0;
  for (int i = 0; i < n; i++)
    sum += 2;

  assert(sum == 2 * n);
  return 0;
}
