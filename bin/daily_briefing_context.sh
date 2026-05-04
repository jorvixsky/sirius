#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.npm-global/bin:$HOME/.npm-global/lib/node_modules/.bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

VAULT_PATH="/home/sirius/obsidian/vaults/main"
TODO_NOTE="$VAULT_PATH/Work/Global To-dos.md"
LOCATION="Granollers,Spain"

printf '=== Daily briefing context generated at %s ===\n\n' "$(date -Is)"

printf '=== Weather source: wttr.in (%s, metric) ===\n' "$LOCATION"
# Compact current conditions + 3-day JSON-derived daily summary.
if weather_json=$(curl -fsS --max-time 20 "https://wttr.in/${LOCATION}?format=j1&m" 2>/dev/null); then
  printf '%s\n' "$weather_json" | jq -r '
    .current_condition[0] as $c |
    "Current: \($c.weatherDesc[0].value), \($c.temp_C)°C (feels \($c.FeelsLikeC)°C), wind \($c.windspeedKmph) km/h, humidity \($c.humidity)%, precipitation \($c.precipMM) mm" ,
    "Forecast:",
    (.weather[0:3][] | "- \(.date): \(.hourly[4].weatherDesc[0].value // .hourly[0].weatherDesc[0].value), min \(.mintempC)°C / max \(.maxtempC)°C, rain chance \([.hourly[].chanceofrain | tonumber] | max)%")
  '
else
  echo 'Weather fetch failed.'
fi

printf '\n=== Obsidian sync status / best-effort refresh ===\n'
if pgrep -af "ob sync --path $VAULT_PATH --continuous" >/dev/null 2>&1; then
  echo 'Continuous Obsidian sync is running; using local synced vault copy.'
elif command -v ob >/dev/null 2>&1; then
  timeout 45s ob sync --path "$VAULT_PATH" 2>&1 || echo 'Best-effort one-shot sync failed or timed out; using local vault copy.'
else
  echo 'ob command not found; using local vault copy.'
fi

printf '\n=== Obsidian task note: %s ===\n' "$TODO_NOTE"
if [[ -f "$TODO_NOTE" ]]; then
  cat "$TODO_NOTE"
else
  echo 'Task note not found.'
fi
