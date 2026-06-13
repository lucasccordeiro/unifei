"""
Lab 2 — Box B (bonus): ESBMC checks Python, too.

Same tool, same evening trick — only the input language changed. This
"safe" wrapper guards against a non-positive total but forgot the OTHER
way an integer division can crash.

Run:    esbmc safe_div.py
Expect: VERIFICATION FAILED — division by zero (CWE-369).
        Read the counterexample: which value of b did the solver pick?
Fix:    add the missing precondition on b, re-run, get
        VERIFICATION SUCCESSFUL with the same command.
"""


def safe_div(a: int, b: int) -> int:
    return a // b          # a built-in check fires here — you never asserted it


a: int = nondet_int()
b: int = nondet_int()
__ESBMC_assume(a > 0)      # guards a ... but says nothing about b
safe_div(a, b)
