"""
Lab 1 — Stage 3, Box B: hand the SAME problem to ESBMC.

In lab1.py Stage 3 you encoded this C function as SSA bit-vector equations
and negated its assertion BY HAND in Z3:

    int f(int x) {
        int y = x + 1;
        int z = y * 2;
        assert(z >= 2);
    }

Here you just write the function in Python and let ESBMC build that same
formula for you. Same trick (prove P by asking whether NOT P is SAT) — but
the tool does the encoding and the solving.

Run:    esbmc stage3_esbmc.py
Expect: VERIFICATION FAILED, with a counterexample value of x.
"""


def f(x: int) -> int:
    y = x + 1
    z = y * 2
    assert z >= 2          # ESBMC negates this for you and searches
    return z


x: int = nondet_int()      # "every int at once" — exactly like BitVec("x", ..)
f(x)


# Questions (answer in a comment before moving on):
#   Q1. Z3 Stage 3 reported x = 1073741824 (2^30). ESBMC reports
#       x = 9223372036854775807 (2^63 - 1). Same bug — why a different
#       number? (Hint: what width does ESBMC model a Python int as?)
#   Q2. Stretch: add  __ESBMC_assume(x >= 0)  just above the call to f().
#       In the 32-bit C world that does NOT rescue the assertion, and it
#       does not here either. Run it — at which x does y * 2 still overflow?
#   Q3. Z3 is the SMT engine; ESBMC is a bounded model checker built ON a
#       solver like Z3. In this file, who wrote the formula — you or the
#       tool? Who solved it? Compare with lab1.py Stage 3.
