#!/usr/bin/env python3
"""
Reproduce ESBMC's --ir counterexample for stage3_esbmc.py in real CPython.

    esbmc stage3_esbmc.py        ->  FAILED, x = 9223372036854775807 (2^63-1)
    esbmc stage3_esbmc.py --ir   ->  FAILED, x = -1

This script runs the SAME function ESBMC checked, under plain CPython, on
BOTH witnesses — and shows only the --ir one is a real Python bug:

  * default witness x = 2^63-1 is a 64-bit-machine-word artifact: CPython
    ints are arbitrary-precision, so z stays huge and the assert HOLDS.
  * --ir witness x = -1 reproduces: y = 0, z = 0, and `assert z >= 2` FAILS.

Run (no ESBMC needed — this is ordinary Python):

    python3 stage3_ir_reproduce.py

Exit status is non-zero: it re-raises the AssertionError, reproducing the
counterexample end-to-end.
"""
import sys


def f(x: int) -> int:
    """The exact function from stage3_esbmc.py."""
    y = x + 1
    z = y * 2
    assert z >= 2          # the property ESBMC negated
    return z


def holds(x: int) -> bool:
    """True if f(x) returns normally, False if its assertion fails."""
    try:
        f(x)
        return True
    except AssertionError:
        return False


DEFAULT_WITNESS = 2**63 - 1      # esbmc stage3_esbmc.py
IR_WITNESS = -1                  # esbmc stage3_esbmc.py --ir

if __name__ == "__main__":
    # The default machine-word witness does NOT reproduce in CPython.
    assert holds(DEFAULT_WITNESS), "unexpected: default witness reproduced"
    print(f"x = 2^63-1: z = {f(DEFAULT_WITNESS)}, assert holds "
          f"-> machine-word artifact, not a real Python bug")

    # The --ir witness DOES reproduce.
    print(f"x = {IR_WITNESS}: reproducing the --ir counterexample ...",
          flush=True)
    f(IR_WITNESS)            # raises AssertionError: z = 0 < 2
    print("no error — counterexample did NOT reproduce", file=sys.stderr)
