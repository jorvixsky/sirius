#!/usr/bin/env bash
set -uo pipefail
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
cd /home/sirius/.openclaw/workspace || exit 1

OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"
CLAWHUB_BIN="${CLAWHUB_BIN:-$HOME/.local/bin/clawhub}"
STATE_FILE="/home/sirius/.openclaw/workspace/auto_update_state.json"

before_oc=$($OPENCLAW_BIN --version 2>/dev/null || echo "unknown")

npm_output=$(npm update -g openclaw@latest 2>&1)
npm_code=$?
after_oc=$($OPENCLAW_BIN --version 2>/dev/null || echo "unknown")

doctor_output=$($OPENCLAW_BIN doctor --yes 2>&1)
doctor_code=$?

skill_output=$($CLAWHUB_BIN update --all --no-input 2>&1)
skill_code=$?

messages=()
if [[ $npm_code -ne 0 ]]; then
  messages+=("❌ OpenClaw npm update failed:" "$(printf '%s' "$npm_output" | tail -n 20)")
# Success update messages are suppressed; only errors are reported.
# elif [[ "$before_oc" != "$after_oc" ]]; then
#   messages+=("📦 OpenClaw updated: $before_oc → $after_oc")
fi

if [[ $doctor_code -ne 0 ]]; then
  messages+=("❌ openclaw doctor reported a problem:" "$(printf '%s' "$doctor_output" | tail -n 30)")
fi

if [[ $skill_code -ne 0 ]]; then
  # Safety skips/local modifications are common and not actionable daily noise unless the text changed.
  hash=$(printf '%s' "$skill_output" | sha256sum | awk '{print $1}')
  last_hash=""
  [[ -f "$STATE_FILE" ]] && last_hash=$(python3 - <<'PY' "$STATE_FILE" 2>/dev/null || true
import json, sys
print(json.load(open(sys.argv[1])).get('last_skill_error_hash',''))
PY
)
  if [[ "$hash" != "$last_hash" ]]; then
    messages+=("⚠️ Skill update did not complete cleanly:" "$(printf '%s' "$skill_output" | tail -n 40)")
  fi
  python3 - <<'PY' "$STATE_FILE" "$hash" >/dev/null 2>&1 || true
import json, sys, pathlib, datetime
p=pathlib.Path(sys.argv[1])
data={}
if p.exists():
    try: data=json.loads(p.read_text())
    except Exception: data={}
data['last_skill_error_hash']=sys.argv[2]
data['last_check_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
PY
else
  # Success update messages are suppressed; only errors are reported.
  # if grep -Eiq '(^|[^a-z])(updated|installed|upgraded)([^a-z]|$)' <<<"$skill_output"; then
  #   messages+=("🔄 Skills updated:" "$(printf '%s' "$skill_output" | grep -Ei 'updated|installed|upgraded' | head -n 20)")
  # fi
  python3 - <<'PY' "$STATE_FILE" >/dev/null 2>&1 || true
import json, pathlib, datetime, sys
p=pathlib.Path(sys.argv[1])
data={}
if p.exists():
    try: data=json.loads(p.read_text())
    except Exception: data={}
data['last_skill_error_hash']=''
data['last_check_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
PY
fi

if ((${#messages[@]})); then
  printf '%s\n' "${messages[@]}"
fi

if [[ $npm_code -ne 0 || $doctor_code -ne 0 ]]; then
  exit 1
fi
# Do not fail the whole job for known skill safety/local-modification skips; they are surfaced once above.
exit 0
