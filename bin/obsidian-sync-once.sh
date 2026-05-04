#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.npm-global/bin:$HOME/.npm-global/lib/node_modules/.bin:/home/linuxbrew/.linuxbrew/bin:$PATH"
VAULT_PATH="/home/sirius/obsidian/vaults/main"
LOG_DIR="$HOME/.openclaw/workspace/logs"
LOCK_FILE="/tmp/sirius-obsidian-sync.lock"
mkdir -p "$LOG_DIR"

{
  echo "===== $(date -Is) obsidian sync start ====="
  flock -n 9 || { echo "Another sync is already running; skipping."; exit 0; }
  ob sync --path "$VAULT_PATH"
  echo "===== $(date -Is) obsidian sync complete ====="
} 9>"$LOCK_FILE" >> "$LOG_DIR/obsidian-sync.log" 2>&1
