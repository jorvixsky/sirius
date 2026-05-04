#!/bin/bash
# Email monitoring script
# Checks for new emails and sends Telegram alerts

EMAIL_LOG="/home/sirius/.openclaw/workspace/email_monitor.log"
TELEGRAM_USER="647735879"

# Get email count using Himalaya
EMAIL_COUNT=$(himalaya envelope list --folder INBOX --output json 2>/dev/null | jq length 2>/dev/null || echo "0")

echo "$(date): Found $EMAIL_COUNT emails" >> "$EMAIL_LOG"

# If new emails detected (you'd need to track previous count)
# Could send Telegram alert here
# openclaw message send --channel telegram --to "$TELEGRAM_USER" "New emails: $EMAIL_COUNT"
