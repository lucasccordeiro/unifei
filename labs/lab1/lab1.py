"""
Lab 1 — Constraint solving with Z3 (35 min, in pairs)

Install check:  python3 -c "import z3; print(z3.get_version_string())"
Run:            python3 lab1.py

Three stages. Finish one before starting the next.
The core trick of the whole evening:
    to PROVE a property P, ask the solver whether NOT P is satisfiable.
    unsat  =>  P holds. A model  =>  a counterexample to P.
"""
from z3 import (
    Bools, BitVec, Ints, Solver, Distinct,
    And, Or, Not, Implies, sat, unsat,
)

# ---------------------------------------------------------------------------
# Stage 1 (guided, ~10 min) — are these two formulas equivalent?
#
# Two formulas are equivalent iff (lhs != rhs) is UNSAT.
# ---------------------------------------------------------------------------
print("=== Stage 1: propositional equivalences ===")

a, b, c = Bools("a b c")


def equivalent(lhs, rhs, name):
    """Report whether two formulas are equivalent (lhs != rhs is unsat)."""
    slv = Solver()
    slv.add(lhs != rhs)
    if slv.check() == unsat:
        print(f"{name}: EQUIVALENT (lhs != rhs is unsat)")
    else:
        print(f"{name}: NOT equivalent, counterexample: {slv.model()}")


# 1a. De Morgan: not(a and b)  vs  (not a) or (not b)
equivalent(Not(And(a, b)), Or(Not(a), Not(b)), "1a De Morgan")

# 1b. Distribution: a and (b or c)  vs  (a and b) or (a and c)
equivalent(And(a, Or(b, c)), Or(And(a, b), And(a, c)), "1b distribution")

# 1c. A plausible-looking FALSE equivalence — read the counterexample!
#     a implies (b implies a)   vs   b
equivalent(Implies(a, Implies(b, a)), b, "1c trick question")

# TODO 1d: check whether  (a -> b) -> c   is equivalent to   a -> (b -> c).
#          Predict first, then encode it.


# ---------------------------------------------------------------------------
# Stage 2 (~10 min) — SEND + MORE = MONEY
#
# Each letter is a distinct digit 0..9; S and M are not 0.
# Let the solver search ~10^8 assignments for you.
# ---------------------------------------------------------------------------
print("\n=== Stage 2: SEND + MORE = MONEY ===")

S, E, N, D, M, O, R, Y = Ints("S E N D M O R Y")
digits = [S, E, N, D, M, O, R, Y]

s = Solver()
s.add([And(0 <= d, d <= 9) for d in digits])
s.add(Distinct(digits))
s.add(S != 0, M != 0)

# TODO: add the arithmetic constraint
#   SEND + MORE == MONEY, where SEND = 1000*S + 100*E + 10*N + D, etc.
# Then: if s.check() == sat: print(s.model())


# ---------------------------------------------------------------------------
# Stage 3 (~10 min) — verify a tiny C function BY HAND
#
# You are now doing manually what ESBMC automates in Lab 2.
#
#   int f(int x) {
#     int y = x + 1;
#     int z = y * 2;
#     assert(z >= 2);
#   }
#
# Translate to SSA equations over 32-bit bit-vectors, then ask:
# is there an x where all equations hold AND the assertion FAILS?
# ---------------------------------------------------------------------------
print("\n=== Stage 3: a C program as a formula ===")

x = BitVec("x", 32)
y = BitVec("y", 32)
z = BitVec("z", 32)

s = Solver()
s.add(y == x + 1)        # y = x + 1
s.add(z == y * 2)        # z = y * 2
s.add(Not(z >= 2))       # the assertion, NEGATED

if s.check() == sat:
    m = s.model()
    print("assertion can FAIL, counterexample:", m)
    print("check: x =", m[x], "-> z =", m.eval(z))
else:
    print("assertion always holds (unsat)")

# Questions (answer in a comment before moving on):
#   Q1. What does UNSAT mean here, vs. what it meant in Stage 1?
#   Q2. The solver found a counterexample. Is it one a normal test
#       suite would have tried?
#   Q3 (stretch). Add the precondition x >= 0 with s.add(x >= 0).
#       Does the assertion hold now? Why is that subtle on bit-vectors?
