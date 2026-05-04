#!/usr/bin/env python3
"""Quiet email monitor for Sirius.

Outputs only when something relevant happens:
- new email(s) since the last seen IMAP UID
- an execution/configuration error
Successful unchanged checks print nothing.
"""
from __future__ import annotations

import email
import imaplib
import json
import os
import ssl
from datetime import datetime, timezone
from email.header import decode_header, make_header
from pathlib import Path

EMAIL = os.environ.get("SIRIUS_EMAIL", "sirius@jordiplanas.cat")
PASSWORD = os.environ.get("SIRIUS_EMAIL_PASSWORD", "").strip()
IMAP_SERVER = os.environ.get("SIRIUS_IMAP_SERVER", "mail.jordiplanas.cat")
IMAP_PORT = int(os.environ.get("SIRIUS_IMAP_PORT", "993"))

BASE_DIR = Path("/home/sirius/.openclaw/workspace")
STATE_FILE = BASE_DIR / "email_monitor_state.json"
LOG_FILE = BASE_DIR / "email_monitor.log"
MAX_ALERT_ITEMS = int(os.environ.get("SIRIUS_EMAIL_MAX_ALERT_ITEMS", "5"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state() -> dict:
    default = {
        "last_check": None,
        "last_email_count": 0,
        "last_email_id": None,
        "last_seen_uid": 0,
        "total_checks": 0,
    }
    try:
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text())
            default.update(data)
    except Exception:
        # If state is corrupted, continue but do not crash the monitor.
        pass
    return default


def save_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(STATE_FILE)


def append_log(entry: dict) -> None:
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def decoded_header(value: str | None) -> str:
    if not value:
        return "(none)"
    try:
        return str(make_header(decode_header(value))).strip() or "(none)"
    except Exception:
        return value.strip() or "(none)"


def fetch_header(imap: imaplib.IMAP4_SSL, uid: bytes) -> dict:
    status, msg_data = imap.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if status != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
        return {"uid": uid.decode(errors="ignore"), "from": "Unknown", "subject": "Unknown", "date": "Unknown"}
    msg = email.message_from_bytes(msg_data[0][1])
    return {
        "uid": uid.decode(errors="ignore"),
        "from": decoded_header(msg.get("From")),
        "subject": decoded_header(msg.get("Subject")),
        "date": decoded_header(msg.get("Date")),
    }


def check_emails() -> dict:
    state = load_state()
    state["total_checks"] = int(state.get("total_checks") or 0) + 1

    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context, timeout=20) as imap:
            imap.login(EMAIL, PASSWORD)
            imap.select("INBOX")

            status, data = imap.uid("search", None, "ALL")
            if status != "OK":
                raise RuntimeError(f"IMAP UID search failed: {status}")

            uids = data[0].split() if data and data[0] else []
            current_count = len(uids)
            newest_uid = max((int(u) for u in uids), default=0)
            last_seen_uid = int(state.get("last_seen_uid") or state.get("last_email_id") or 0)

            # First run/bootstrap: preserve the current high-water mark without alerting.
            if last_seen_uid <= 0:
                new_uids: list[bytes] = []
            else:
                new_uids = [u for u in uids if int(u) > last_seen_uid]

            details = [fetch_header(imap, uid) for uid in new_uids[-MAX_ALERT_ITEMS:]]

        state.update(
            {
                "last_check": now_iso(),
                "last_email_count": current_count,
                "last_email_id": str(newest_uid) if newest_uid else None,
                "last_seen_uid": max(last_seen_uid, newest_uid),
            }
        )
        save_state(state)

        append_log(
            {
                "timestamp": now_iso(),
                "email_count": current_count,
                "new_emails": len(new_uids),
                "newest_uid": newest_uid,
                "total_checks": state["total_checks"],
                "success": True,
            }
        )

        return {"success": True, "email_count": current_count, "new_emails": len(new_uids), "details": details}

    except Exception as exc:
        state["last_check"] = now_iso()
        save_state(state)
        append_log({"timestamp": now_iso(), "error": str(exc), "success": False, "total_checks": state["total_checks"]})
        return {"success": False, "error": str(exc)}


def main() -> int:
    result = check_emails()
    if not result["success"]:
        print(f"❌ Sirius email monitor failed: {result['error']}")
        return 1

    new_count = result["new_emails"]
    if new_count:
        print(f"📧 Sirius inbox: {new_count} new email{'s' if new_count != 1 else ''} detected.")
        for item in result["details"]:
            print(f"• From: {item['from']}")
            print(f"  Subject: {item['subject']}")
        if new_count > len(result["details"]):
            print(f"…plus {new_count - len(result['details'])} more.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
