# Glossary — Formal Verification Workshop

**Verification vs. validation.** Verification: "are we building the product
right?" (code meets spec). Validation: "are we building the right product?"
(spec meets need).

**Sound** (technique). Never misses a bug of the class it targets. If a
sound tool says "safe", it is safe (within the tool's assumptions).

**Complete** (technique). Never raises a false alarm. If a complete tool
reports a bug, it is a real bug.

*Every practical tool trades one for the other: testing is neither;
bounded model checking is complete, and sound only up to its bound.*

**SAT.** The Boolean satisfiability problem: given a propositional formula,
is there an assignment of true/false making it true? Solvers answer
**sat** (and give a *model* — a satisfying assignment) or **unsat**.

**SMT (Satisfiability Modulo Theories).** SAT extended with theories that
match programming languages: bit-vectors (machine integers, with overflow),
arrays, floating point, pointers. Z3, Bitwuzla, and CVC5 are SMT solvers.

**Model checking.** Exhaustively explore all states of a system to check a
property. For software: all values of all inputs, all interleavings of all
threads — up to a bound.

**Bounded model checking (BMC).** Unroll loops up to a bound *k*, convert
program + negated property into one SMT formula C ∧ ¬P, and ask the solver:
- **sat** → a real bug, with a *counterexample* (concrete inputs + trace);
- **unsat** → no bug exists *within the bound k*.

**Counterexample.** A concrete execution that violates the property: input
values, line-by-line trace, thread schedule. The tool's evidence — and your
debugging script.

**SSA (static single assignment).** Renaming so every variable is assigned
once (`x = x+1` becomes `x2 = x1 + 1`); turns a program into equations.

**Loop unwinding / `--unwind k`.** Replacing a loop by *k* copies of its
body. The *unwinding assertion* checks whether *k* was enough; if it fails,
the bound is too small — the verdict says nothing about longer runs.

**Nondeterministic value (`nondet_int()`).** "Any possible value" — models
untrusted input. One nondet input = all tests of that input at once.

**Assume (`__ESBMC_assume(cond)`).** Restricts the search to executions
where `cond` holds — preconditions, input ranges.

**Assert (`assert(cond)`).** The property to verify: must hold on *every*
execution the tool explores.

**k-induction.** A technique to lift bounded results to *unbounded* proofs:
prove the base case and that the property is inductive over k steps.

**Symbolic execution.** Run the program on symbolic inputs, collecting a
*path condition* per path; ask a solver which paths are feasible. (KLEE)

**Abstract interpretation.** Over-approximate all behaviours (e.g. track
intervals instead of values). Sound, fast — but incomplete: false alarms.
(Astrée)

**Fuzzing.** Throw mutated random inputs at a program and watch for
crashes. No proofs, embarrassingly effective. (AFL, OSS-Fuzz)
