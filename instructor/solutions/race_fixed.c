/* Lab 4, Track A — fix.
 * The failing interleaving: t1 runs g = 1, then a context switch lets
 * t2 run g = 2, then t1 resumes and asserts g == 1. A mutex makes the
 * write-then-check atomic.
 *
 * esbmc race_fixed.c --context-bound 2  =>  VERIFICATION SUCCESSFUL
 */
#include <pthread.h>
#include <assert.h>

int g;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

void *t1(void *arg)
{
  pthread_mutex_lock(&m);
  g = 1;
  assert(g == 1);
  pthread_mutex_unlock(&m);
  return 0;
}

void *t2(void *arg)
{
  pthread_mutex_lock(&m);
  g = 2;
  pthread_mutex_unlock(&m);
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
