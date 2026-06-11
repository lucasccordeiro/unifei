#!/usr/bin/env bash
# Validates that every command printed in a student-facing file produces
# the verdict documented in instructor/solutions/expected-verdicts.md,
# and that the Python labs run and print their expected results.
#
# Usage:  ESBMC=/path/to/esbmc tests/run_checks.sh
#         (ESBMC defaults to `esbmc` on PATH)
set -u
cd "$(dirname "$0")/.." || exit 1

ESBMC="${ESBMC:-esbmc}"
pass=0
fail=0

# Stock macOS has no `timeout`; fall back to a perl shim.
if ! command -v timeout >/dev/null 2>&1; then
  timeout() { perl -e 'alarm shift; exec @ARGV' "$@"; }
fi

check() {
  local f="$1" expect="$2"; shift 2
  local v
  v=$(timeout 90 "$ESBMC" "$f" "$@" 2>&1 |
      grep -m1 -oE "VERIFICATION (SUCCESSFUL|FAILED|UNKNOWN)")
  if [ "$v" = "$expect" ]; then
    pass=$((pass + 1)); echo "PASS  $f $* ($v)"
  else
    fail=$((fail + 1)); echo "FAIL  $f $* expected=$expect got=${v:-none}"
  fi
}

check_py() {
  local f="$1" token="$2"
  if python3 "$f" 2>/dev/null | grep -q "$token"; then
    pass=$((pass + 1)); echo "PASS  $f (output contains '$token')"
  else
    fail=$((fail + 1)); echo "FAIL  $f (no '$token' in output)"
  fi
}

# Buggy files, as shipped — must FAIL (except the by-design greens)
check session1-demos/getpassword.c          "VERIFICATION FAILED"     --unwind 8
check session1-demos/offbyone.c             "VERIFICATION FAILED"     --unwind 7
check session1-demos/predict/predict1.c     "VERIFICATION FAILED"     --unwind 6
check session1-demos/predict/predict2.c     "VERIFICATION FAILED"     --unwind 4
check session1-demos/predict/predict3.c     "VERIFICATION SUCCESSFUL" --unwind 6
check labs/lab2/overflow.c                  "VERIFICATION FAILED"
check labs/lab2/leak.c                      "VERIFICATION FAILED"     --memory-leak-check
check labs/lab2/vla.c                       "VERIFICATION FAILED"     --unwind 6
check labs/lab2/getpassword.c               "VERIFICATION FAILED"     --unwind 8
check labs/lab3/triangle.c                  "VERIFICATION SUCCESSFUL"  # weak spec, by design
check labs/lab3/unwind.c                    "VERIFICATION FAILED"     --unwind 5
check labs/lab3/unwind.c                    "VERIFICATION FAILED"     --unwind 20
check labs/lab3/unwind.c                    "VERIFICATION SUCCESSFUL" --unwind 60
check labs/lab3/unwind.c                    "VERIFICATION UNKNOWN"    --k-induction  # stretch task, by design
check labs/lab4/race.c                      "VERIFICATION FAILED"     --context-bound 2
check labs/lab4/float.c                     "VERIFICATION FAILED"      # also the setup.md smoke test

# Fixed files — must all be SUCCESSFUL
check instructor/solutions/overflow_fixed.c     "VERIFICATION SUCCESSFUL"
check instructor/solutions/leak_fixed.c         "VERIFICATION SUCCESSFUL" --memory-leak-check
check instructor/solutions/vla_fixed.c          "VERIFICATION SUCCESSFUL" --unwind 6
check instructor/solutions/getpassword_fixed.c  "VERIFICATION SUCCESSFUL" --unwind 10
check instructor/solutions/triangle_solution.c  "VERIFICATION SUCCESSFUL"
check instructor/solutions/race_fixed.c         "VERIFICATION SUCCESSFUL" --context-bound 2

# Python labs — check the pedagogically load-bearing output, not just exit 0
check_py session1-demos/z3_demo.py              "unsat"
check_py labs/lab1/lab1.py                      "assertion can FAIL"
check_py instructor/solutions/lab1_solution.py  "9567 + 1085 = 10652"

echo "=== $pass passed, $fail failed ==="
exit "$((fail > 0))"
