#!/usr/bin/env python3
"""Send email via himalaya with Jordi always Bcc'd.

Usage:
  send-email-himalaya-bcc.py --to a@example.com,b@example.com --subject "Subject" --body-file body.txt

This intentionally pipes a raw RFC822 message to `himalaya message send` over stdin.
Do not use direct SMTP helpers for user-requested email sends.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

DEFAULT_BCC = "hola@jordiplanas.cat"
FROM = "Sirius <sirius@jordiplanas.cat>"


def split_addresses(value: str) -> list[str]:
    return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True, help="Comma/semicolon-separated recipients")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", help="Plain text body")
    parser.add_argument("--body-file", help="Path to plain text body")
    parser.add_argument("--cc", default="")
    parser.add_argument("--bcc", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true", help="Print raw message instead of sending")
    args = parser.parse_args()

    if bool(args.body) == bool(args.body_file):
        parser.error("provide exactly one of --body or --body-file")

    body = args.body if args.body is not None else Path(args.body_file).read_text()

    to = split_addresses(args.to)
    cc = split_addresses(args.cc)
    extra_bcc = []
    for item in args.bcc:
        extra_bcc.extend(split_addresses(item))
    bcc = list(dict.fromkeys([*extra_bcc, DEFAULT_BCC]))

    if DEFAULT_BCC not in bcc:
        raise RuntimeError(f"mandatory Bcc missing: {DEFAULT_BCC}")

    msg = EmailMessage()
    msg["From"] = FROM
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = args.subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="jordiplanas.cat")
    msg.set_content(body)

    raw = msg.as_string()
    if args.dry_run:
        print(raw)
        return 0

    proc = subprocess.run(["himalaya", "--quiet", "message", "send"], input=raw, text=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
