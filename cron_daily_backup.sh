#!/usr/bin/env bash
set -uo pipefail
cd /home/sirius/.openclaw/workspace || exit 1

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ Sirius backup failed: workspace is not a git repository."
  exit 1
fi

changes_before=$(git status --porcelain=v1)
if [[ -z "$changes_before" ]]; then
  exit 0
fi

if ! git add -A; then
  echo "❌ Sirius backup failed: git add failed."
  exit 1
fi

changed_count=$(printf '%s\n' "$changes_before" | sed '/^$/d' | wc -l | tr -d ' ')
commit_msg="Daily backup of Sirius workspace ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
commit_output=$(git commit -m "$commit_msg" 2>&1)
commit_code=$?
if [[ $commit_code -ne 0 ]]; then
  # Nothing to commit can happen if hooks/normalization consumed changes; don't alert for that.
  if grep -qi "nothing to commit" <<<"$commit_output"; then
    exit 0
  fi
  echo "❌ Sirius backup failed during commit:"
  echo "$commit_output" | tail -n 20
  exit $commit_code
fi

push_output=$(git push 2>&1)
push_code=$?
if [[ $push_code -ne 0 ]]; then
  echo "❌ Sirius backup committed locally but push failed:"
  echo "$push_output" | tail -n 20
  exit $push_code
fi

# Success: output nothing. Only errors produce output.
# No success message, as per Jordi's request to notify only on errors.
