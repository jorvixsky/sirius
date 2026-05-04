#!/usr/bin/env bash
set -uo pipefail
cd /home/sirius/.openclaw/workspace || exit 1
if [[ -z "${SIRIUS_EMAIL_PASSWORD:-}" && -r /home/sirius/.openclaw/secrets/sirius_email_password ]]; then
  export SIRIUS_EMAIL_PASSWORD="$(tr -d '\r\n' < /home/sirius/.openclaw/secrets/sirius_email_password)"
fi
output=$(python3 email_monitor.py 2>&1)
code=$?
if [[ $code -ne 0 ]]; then
  printf '%s\n' "$output"
  exit $code
fi
if [[ -n "${output//[[:space:]]/}" ]]; then
  printf '%s\n' "$output"
fi
