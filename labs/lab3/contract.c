/*
 * Lab 3 — function contracts: specify the function, not the call site.
 *
 * Instead of sprinkling assert()s around every call, attach a CONTRACT to
 * the function itself:
 *   __ESBMC_requires(P)  -- the precondition the caller must establish
 *   __ESBMC_ensures(Q)   -- the postcondition the function promises
 *                           (use __ESBMC_return_value for the result)
 *
 * Two complementary checks:
 *
 *   esbmc contract.c --enforce-contract clamp
 *       Does the BODY keep its promise? Parameters are nondet, constrained
 *       by requires; ESBMC asserts ensures on every path through clamp.
 *
 *   esbmc contract.c --replace-call-with-contract clamp
 *       Verify CALLERS against the contract ALONE: each call is replaced by
 *       "assume requires; havoc the result; assume ensures". The body is not
 *       re-analysed — this is modular (assume-guarantee) verification.
 *
 * clamp() has a seeded bug. Find it with --enforce-contract, fix it, and
 * re-verify to VERIFICATION SUCCESSFUL.
 *
 * GOTCHA: a contract is only checked if the function is REACHABLE. main()
 * calls clamp() below; with no call site there is nothing to enforce and
 * ESBMC trivially reports SUCCESSFUL.
 */
#include <assert.h>

int nondet_int(void);
void __ESBMC_assume(_Bool);

int clamp(int x, int lo, int hi)
{
  __ESBMC_requires(lo <= hi);                  /* precondition */
  __ESBMC_ensures(__ESBMC_return_value >= lo); /* postconditions: lo <= r <= hi */
  __ESBMC_ensures(__ESBMC_return_value <= hi);

  if (x < lo) return lo;
  if (x > hi) return x;     /* BUG: should return hi */
  return x;
}

int main(void)
{
  int x = nondet_int(), lo = nondet_int(), hi = nondet_int();
  __ESBMC_assume(lo <= hi);          /* establish clamp's precondition */

  int r = clamp(x, lo, hi);
  assert(r >= lo && r <= hi);        /* exactly what the contract guarantees */
  return 0;
}
