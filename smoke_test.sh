#!/usr/bin/env bash
################################################################################
#: Title       : smoke_test
#: Date        : 2019-April-14
#: Author      : Anthony Tilelli
#: Version     : 0.1
#: Description : smoke tests for app_curses application (venv is assumed active)
#:             : Creates file ".smoke_test_results.txt" if smoke test passes
#: Usage       : Call "smoke_test.sh"
################################################################################

# strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# CONSTANTS
readonly WORKING_DIR="/tmp/smoke"
readonly FILE_RESULT="test/smoke_test_results.txt"

# FUNCTIONS
function fail() {
  # Outputs error-message and force-quits script

  local -r ERRORCODE="${1:-1}"
  local -r ERROR_MESSAGE="${2:-"fail called but \"ERROR_MESSAGE\" not set"}"
  printf "ERROR %d: %s\\n" "$ERRORCODE" "$ERROR_MESSAGE" >&2
  exit "$ERRORCODE"
}

function expected_fail() {
  # Tests expected Failure conditions
  set +e

  # TEST fail without arguments
  python app_curses.py > "$WORKING_DIR/output" 2> "$WORKING_DIR/error"

  if (( $? != 2 )); then
    fail 1 "app_curses.py did not fail as expected"
  fi

  if [[ -s "$WORKING_DIR/output" ]] ; then
    fail 1 "app_curses.py output to standard out instead of std error"
  fi

  if [[ ! -s "$WORKING_DIR/error" ]] ; then
    fail 1 "app_curses.py did not output to standard error"
  fi

  # TEST only -d fail without argument
  rm "$WORKING_DIR/error" "$WORKING_DIR/output"
  python app_curses.py -d > "$WORKING_DIR/output" 2> "$WORKING_DIR/error"

  if [[ $? != 2 ]]; then
    fail 1 "app_curses.py did not fail as expected"
  fi

  if [[ ! -s "$WORKING_DIR/error" ]] ; then
    fail 1 "app_curses.py did not output to standard error"
  fi

  if [[ -s "$WORKING_DIR/output" ]] ; then
    fail 1 "app_curses.py output to standard out instead of std error"
  fi

  set -e
  rm "$WORKING_DIR/error" "$WORKING_DIR/output"
  return 0
}

function main() {
  if ((BASH_VERSINFO[0] > 4)); then
    fail 1 "Bash-4.0+ is required to run this script"
  fi

  # Remove old smoke results file
  rm -f "$FILE_RESULT"

  mkdir -p $WORKING_DIR
  expected_fail

  # Smoke tests
  python app_curses.py -h > /dev/null # help
  echo -ne 'q' | python app_curses.py easy > /dev/null # Easy
  echo -ne 'q' | python app_curses.py advanced -s > /dev/null # Advanced (with extra difficulty)
  echo -ne 'q' | python app_curses.py expert -t 5 > /dev/null # Expert (Non-default tries)
  echo -ne 'q' | python app_curses.py master > /dev/null # Master

  # ALL tests passed
  printf "Smoke test passed, recording results at \'%s\'\\n" "$FILE_RESULT"
  printf "Smoke Test PASSED -> %s\\n" "$(date -u --iso-8601)" > "$FILE_RESULT"
}

main "$@"
exit 0
