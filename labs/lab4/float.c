/*
 * Lab 4, Track B — floating-point challenge.
 * Based on COMP63342 CW04 Q1 (floating-point arithmetic).
 *
 * BEFORE running anything, as a team, predict the verdict of each
 * assertion. They look obviously true — are they?
 *
 *   esbmc float.c
 *
 * Then explain WHY, in one sentence, to the instructor.
 * (Hint: 0.1 has no exact representation in binary, for the same
 *  reason 1/3 has none in decimal.)
 */
#include <assert.h>

int main(void)
{
  double x = 0.1;
  double y = 0.2;
  double w = 0.3;
  double z = x + y;
  assert(w == z);
  return 0;
}
