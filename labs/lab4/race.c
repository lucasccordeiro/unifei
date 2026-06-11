/*
 * Lab 4, Track A — concurrency challenge.
 * Based on COMP63342 CW04 Q2 (multi-threaded C).
 *
 * BEFORE running anything, as a team, predict:
 *   - Can the assertion in t1 fail?
 *   - If yes, write down the interleaving (order of statements
 *     across threads) that breaks it.
 *
 * Then check your prediction:
 *   esbmc race.c --context-bound 2
 *
 * The counterexample now contains THREAD SCHEDULES — find the
 * context switch that breaks the assertion.
 *
 * Fix idea: protect g with a pthread_mutex_t, then re-verify.
 */
#include <pthread.h>
#include <assert.h>

int g;

void *t1(void *arg)
{
  g = 1;
  assert(g == 1);
  return 0;
}

void *t2(void *arg)
{
  g = 2;
  return 0;
}

int main(void)
{
  pthread_t id1, id2;
  pthread_create(&id1, 0, t1, 0);
  pthread_create(&id2, 0, t2, 0);
  pthread_join(id1, 0);
  pthread_join(id2, 0);
  return 0;
}
