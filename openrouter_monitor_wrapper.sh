#!/bin/bash
# OpenRouter Monitor Wrapper
# Runs the Python monitor and handles alerts

LOG_FILE="/home/sirius/.openclaw/workspace/openrouter_monitor.log"
PYTHON_SCRIPT="/home/sirius/.openclaw/workspace/monitor_openrouter.py"

echo "========================================" >> "$LOG_FILE"
echo "$(date): Starting OpenRouter monitor" >> "$LOG_FILE"

# Run the Python monitor
cd /home/sirius/.openclaw/workspace
python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "$(date): Monitor finished with exit code $EXIT_CODE" >> "$LOG_FILE"

# If there was an error, send alert
if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: Monitor script failed" >> "$LOG_FILE"
    # Could send Telegram alert here
    # openclaw message send --channel telegram --to "647735879" "OpenRouter monitor failed!"
fi

echo "========================================" >> "$LOG_FILE"