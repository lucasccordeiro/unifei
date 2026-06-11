# Formal Verification Workshop (UNIFEI)

Two 3-hour evening workshops (6–9 PM) introducing formal verification to a
mixed undergraduate/graduate audience with little or no prior exposure to
formal methods.

- **Session 1 — Fundamentals and real-world applications:** why testing is
  not enough, SAT/SMT, bounded model checking, industry deployments.
- **Session 2 — Hands-on:** constraint solving with Z3, bug hunting and
  specification writing with ESBMC, a concurrency/floating-point challenge.

Based on the *Software Security* course materials (COMP63342, University of
Manchester): <https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html>

## Repository layout

| Path | Audience | Contents |
|---|---|---|
| `instructor/delivery-plan.md` | instructor | Minute-by-minute plan for both sessions |
| `instructor/quizzes.md` | instructor | Icebreaker, quizzes, exercise debriefs — with answers |
| `instructor/solutions/` | instructor | Fixed programs, completed lab scripts, expected tool verdicts |
| `handouts/setup.md` | students | Tool installation (send out after Session 1) |
| `handouts/glossary.md` | students | One-page glossary handout |
| `handouts/spot-the-bug.md` | students | Session 1, Exercise 1 |
| `session1-demos/` | instructor | Live-demo programs for Session 1, with exact commands |
| `labs/` | students | Session 2 starter pack (labs 1–4 + cheatsheet) |

## Quick start

**Students:** read [`handouts/setup.md`](handouts/setup.md), install Z3 and
ESBMC, run the two smoke tests. Done.

**Instructor:** read [`instructor/delivery-plan.md`](instructor/delivery-plan.md).
Every demo and lab command in this repository has been executed against
**ESBMC 8.3.0** and **Z3 4.16.0**; the expected outputs are recorded in
[`instructor/solutions/expected-verdicts.md`](instructor/solutions/expected-verdicts.md).

> Students: the `instructor/solutions/` folder is exactly what it says.
> You will learn far more by reading counterexample traces than by reading
> solutions — the tool gives you the answer anyway, with evidence.

## Slides

The lecture slides referenced in the delivery plan are available on the
[course page](https://ssvlab.github.io/lucasccordeiro/courses/2022/01/software-security/index.html)
(lectures 1–5). The plan tells you which slide ranges to extract for the
~40-slide Session 1 subset.
