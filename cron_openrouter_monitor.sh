#!/usr/bin/env bash
set -uo pipefail
cd /home/sirius/.openclaw/workspace || exit 1
if [[ -z "${OPENROUTER_MANAGEMENT_KEY:-}" && -r /home/sirius/.openclaw/secrets/openrouter_management_key ]]; then
  export OPENROUTER_MANAGEMENT_KEY="$(tr -d '\r\n' < /home/sirius/.openclaw/secrets/openrouter_management_key)"
fi
output=$(python3 monitor_openrouter.py 2>&1)
code=$?
if [[ $code -ne 0 ]]; then
  printf '%s\n' "$output"
  exit $code
fi
if [[ -n "${output//[[:space:]]/}" ]]; then
  printf '%s\n' "$output"
fi
