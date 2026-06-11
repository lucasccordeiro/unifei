/* Lab 2, file 2 — fix.
 * The bug: `p = q` overwrote the only pointer to p's first allocation,
 * so those 5 bytes could never be freed. Free p before aliasing it.
 *
 * esbmc leak_fixed.c --memory-leak-check  =>  VERIFICATION SUCCESSFUL
 */
#include <stdlib.h>

int main(void)
{
  char *p = malloc(5);
  char *q = malloc(5);
  free(p);
  p = q;
  free(p);
  p = malloc(5);
  free(p);
  return 0;
}
