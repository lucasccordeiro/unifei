"""
Session 1 live demo: an SMT solver is a search engine for maths.

Run: python3 z3_demo.py
"""
from z3 import BitVecs, BVMulNoOverflow, Solver, solve

x, y = BitVecs("x y", 32)

# Query 1: find me numbers satisfying these constraints (a model, in ms).
print("Query 1: x + y == 42 and x > 100")
solve(x + y == 42, x > 100)

# Query 2: prove none exist.
# x*x == 2*y*y with x, y > 0 would make sqrt(2) = x/y rational.
# Over mathematical integers this is UNSAT; over 32-bit bit-vectors the
# solver reasons about wrap-around too — exactly machine arithmetic.
print("\nQuery 2: x*x == 2*y*y, x > 0, y > 0 (no overflow allowed)")
s = Solver()
s.add(x * x == 2 * y * y, x > 0, y > 0)
s.add(BVMulNoOverflow(x, x, signed=True))
s.add(BVMulNoOverflow(y, y, signed=True))
s.add(BVMulNoOverflow(2 * y, y, signed=True))
print(s.check())  # unsat: sqrt(2) is irrational, bit-vector edition
