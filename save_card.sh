#!/bin/bash
set -e

API_KEY="cck_live_386c2fa4ab908bbf35eb92a704badb8d112323a05a950091"
CARD_FILE="/home/sirius/.openclaw/workspace/.creditclaw/cards/Card-Sirius-Revolut-6568.md"

# Get messages
RESPONSE=$(curl -s -X GET https://creditclaw.com/api/v1/bot/messages \
  -H "Authorization: Bearer $API_KEY")

# Extract file content using jq
FILE_CONTENT=$(echo "$RESPONSE" | jq -r '.messages[0].payload.file_content')

# Save to file
echo "$FILE_CONTENT" > "$CARD_FILE"
echo "Card file saved to $CARD_FILE"

# Confirm delivery
curl -X POST https://creditclaw.com/api/v1/bot/rail5/confirm-delivery \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json"
echo -e "\nDelivery confirmed"