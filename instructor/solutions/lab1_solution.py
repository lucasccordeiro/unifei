"""Lab 1 — instructor solution. Run: python3 lab1_solution.py"""
from z3 import (
    Bools, BitVec, Ints, Solver, Distinct,
    And, Or, Not, Implies, sat, unsat,
)

# --- Stage 1 ---------------------------------------------------------------
print("=== Stage 1 ===")
a, b, c = Bools("a b c")


def equivalent(lhs, rhs, name):
    """Report whether two formulas are equivalent (lhs != rhs is unsat)."""
    slv = Solver()
    slv.add(lhs != rhs)
    if slv.check() == unsat:
        print(f"{name}: EQUIVALENT")
    else:
        print(f"{name}: NOT equivalent, counterexample: {slv.model()}")


equivalent(Not(And(a, b)), Or(Not(a), Not(b)), "1a De Morgan")
equivalent(And(a, Or(b, c)), Or(And(a, b), And(a, c)), "1b distribution")
equivalent(Implies(a, Implies(b, a)), b, "1c trick question")
# 1d: implication is NOT associative — expect a counterexample
#     (e.g. a=false, b=anything, c=false: lhs = c = false... read the model)
equivalent(Implies(Implies(a, b), c), Implies(a, Implies(b, c)),
           "1d implication associativity")

# --- Stage 2 ---------------------------------------------------------------
print("\n=== Stage 2 ===")
S, E, N, D, M, O, R, Y = Ints("S E N D M O R Y")
digits = [S, E, N, D, M, O, R, Y]

s = Solver()
s.add([And(0 <= d, d <= 9) for d in digits])
s.add(Distinct(digits))
s.add(S != 0, M != 0)
send = 1000 * S + 100 * E + 10 * N + D
more = 1000 * M + 100 * O + 10 * R + E
money = 10000 * M + 1000 * O + 100 * N + 10 * E + Y
s.add(send + more == money)

assert s.check() == sat
m = s.model()
print("model:", m)
print(f"check: {m.eval(send)} + {m.eval(more)} = {m.eval(money)}")
# unique solution: 9567 + 1085 = 10652

# --- Stage 3 ---------------------------------------------------------------
print("\n=== Stage 3 ===")
x, y, z = BitVec("x", 32), BitVec("y", 32), BitVec("z", 32)

s = Solver()
s.add(y == x + 1, z == y * 2, Not(z >= 2))
assert s.check() == sat
m = s.model()
print("assertion can FAIL, counterexample:", m)
print("check: x =", m[x], "-> z =", m.eval(z))

# Q1: Stage 1 unsat = "the formulas are equivalent";
#     Stage 3 unsat would be "no input violates the assertion" = program safe.
#     Same mechanics, different reading of the question we posed.
# Q2: Typically not — solvers jump straight to extreme/negative/overflow
#     values that hand-written tests rarely include.
# Q3: Even with x >= 0 the assertion STILL fails on bit-vectors:
#     e.g. x = 0x7FFFFFFF makes y wrap to INT_MIN and z = 2*INT_MIN wraps
#     to exactly 0, which is < 2 (Z3 may pick a different witness, e.g.
#     x = 2^30 giving a negative z). This is exactly the class of bug
#     --overflow-check finds in Lab 2.
s2 = Solver()
s2.add(y == x + 1, z == y * 2, Not(z >= 2), x >= 0)
print("Q3 with x >= 0:", s2.check())  # sat — overflow!
print("   model:", s2.model() if s2.check() == sat else "-")
