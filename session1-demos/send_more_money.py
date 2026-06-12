"""
Session 1 live demo: SEND + MORE = MONEY as an SMT search.

The same engine that solves this puzzle finds your bugs: a counterexample
is just a satisfying assignment to a set of constraints.

Run: python3 send_more_money.py
"""
from z3 import Ints, Distinct, Or, Solver, sat

# One integer per letter — these are the unknowns the solver fills in.
S, E, N, D, M, O, R, Y = Ints("S E N D M O R Y")
letters = [S, E, N, D, M, O, R, Y]

# A word is its digits times their place value.
SEND = 1000 * S + 100 * E + 10 * N + D
MORE = 1000 * M + 100 * O + 10 * R + E
MONEY = 10000 * M + 1000 * O + 100 * N + 10 * E + Y

s = Solver()
s.add([0 <= x for x in letters])  # each letter is a digit 0..9
s.add([x <= 9 for x in letters])
s.add(Distinct(letters))          # all eight different
s.add(S != 0, M != 0)             # no number starts with 0
s.add(SEND + MORE == MONEY)       # the puzzle itself

print("Searching for an assignment...")
assert s.check() == sat
m = s.model()
sol = {x: int(str(m[x])) for x in letters}

print("  " + "  ".join(f"{x}={sol[x]}" for x in letters))
val = lambda *ds: int("".join(str(sol[d]) for d in ds))
print(f"  {val(S, E, N, D)} + {val(M, O, R, E)} = {val(M, O, N, E, Y)}")

# Is it the ONLY solution? Ask the solver for a *different* assignment.
# This is tonight's negation trick: rule out the model we just found,
# then re-check — unsat means the answer is unique.
s.add(Or([x != sol[x] for x in letters]))
print("\nAnother solution?", s.check(), "(unsat = the answer is unique)")
