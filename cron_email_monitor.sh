#!/usr/bin/env bash
set -uo pipefail
cd /home/sirius/.openclaw/workspace || exit 1
output=$(python3 email_monitor.py 2>&1)
code=$?
if [[ $code -ne 0 ]]; then
  printf '%s\n' "$output"
  exit $code
fi
if [[ -n "${output//[[:space:]]/}" ]]; then
  printf '%s\n' "$output"
fi
