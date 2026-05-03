# CreditClaw Encrypted Card — Sirius - Revolut (****6568)

Card ID: r5card_ab0ca58d1c986007

This file contains your encrypted card details for Rail 5 sub-agent checkout.
Do not edit or share this file. Place it in your bot's `.creditclaw/cards/` folder.

## Card Details

- **BIN:** 416598
- **Expiry:** 05/2031
- **Cardholder Name:** Jordi planas bielsa
- **Brand:** visa

## Billing Address

- **Street:** C/ Francesc Ribas 58 2o 4a
- **City:** Granollers
- **State:** BA
- **ZIP:** 08402
- **Country:** ES

## Quick Start

1. Save this file to `.creditclaw/cards/`
2. Your bot will receive the decryption key at checkout time via CreditClaw API
3. Use the decrypt script below to extract card details when needed

Full docs: https://creditclaw.com/SKILL.md#rail-5

## Encrypted Card Data

ENCRYPTED_CARD_START
cGU9OJ8OWh8nb3Iy40uBIujxj5MXyNcx7CvS/VkfJLDCW2kEm0EHpsf/eiY8GLCGG7FwZNlOgu5kdEhtnw+TKQrb9+SjuaMjD9iNMzZkkGSas8zeg2hXcFxXc67if1732CLLgI7Cn5SbwuIMdl1xeIrCbJW7qGTutJDJCjqyc/jF/i95cqmTzgt9uXWOlTKy49Xw87Lw+nm4KAx8wIJ07anuqRFy2AfJjAxszbRMdpPHPnYIuZIPpNikKiKe8YZdrheRbFZD+078NVlEBJu18tRPsOHITcDLGg==
ENCRYPTED_CARD_END

## Decrypt Script

DECRYPT_SCRIPT_START
const crypto = require("crypto");
const fs = require("fs");
const [,, keyHex, ivHex, tagHex, filePath] = process.argv;

const raw = fs.readFileSync(filePath, "utf8");
const match = raw.match(/ENCRYPTED_CARD_START\n([\s\S]+?)\nENCRYPTED_CARD_END/);
const b64 = match[1].trim();
const data = Buffer.from(b64, "base64");

const decipher = crypto.createDecipheriv(
  "aes-256-gcm",
  Buffer.from(keyHex, "hex"),
  Buffer.from(ivHex, "hex")
);
decipher.setAuthTag(Buffer.from(tagHex, "hex"));
const plain = decipher.update(data.slice(0, -16)) + decipher.final("utf8");
process.stdout.write(plain);
DECRYPT_SCRIPT_END

