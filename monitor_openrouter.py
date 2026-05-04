#!/usr/bin/env python3
"""Quiet OpenRouter credit monitor.

Outputs only when something relevant happens:
- balance crosses below the configured threshold
- balance remains low and the reminder cooldown has elapsed
- API/configuration errors occur
Healthy unchanged checks print nothing.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

OPENROUTER_MANAGEMENT_KEY = os.environ.get("OPENROUTER_MANAGEMENT_KEY", "").strip()
OPENROUTER_CREDITS_API = "https://openrouter.ai/api/v1/credits"
MIN_BALANCE = float(os.environ.get("OPENROUTER_MIN_BALANCE", "5.0"))
ADD_AMOUNT = float(os.environ.get("OPENROUTER_SUGGESTED_ADD_AMOUNT", "20.0"))
LOW_REMINDER_HOURS = float(os.environ.get("OPENROUTER_LOW_REMINDER_HOURS", "24"))

BASE_DIR = Path("/home/sirius/.openclaw/workspace")
LOG_FILE = BASE_DIR / "openrouter_monitor_log.jsonl"
STATE_FILE = BASE_DIR / "openrouter_monitor_state.json"


def now() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now().isoformat()


def load_state() -> dict:
    default = {"was_below_threshold": False, "last_low_alert_at": None, "last_remaining": None, "total_checks": 0}
    try:
        if STATE_FILE.exists():
            default.update(json.loads(STATE_FILE.read_text()))
    except Exception:
        pass
    return default


def save_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(STATE_FILE)


def append_log(entry: dict) -> None:
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def get_openrouter_balance() -> dict:
    if not OPENROUTER_MANAGEMENT_KEY:
        return {"success": False, "error": "OPENROUTER_MANAGEMENT_KEY is not configured"}

    try:
        response = requests.get(
            OPENROUTER_CREDITS_API,
            headers={"Authorization": f"Bearer {OPENROUTER_MANAGEMENT_KEY}"},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()["data"]
        total = float(data["total_credits"])
        used = float(data["total_usage"])
        return {"success": True, "total": total, "used": used, "remaining": total - used}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def reminder_due(state: dict) -> bool:
    last = state.get("last_low_alert_at")
    if not last:
        return True
    try:
        then = datetime.fromisoformat(last)
        return (now() - then).total_seconds() >= LOW_REMINDER_HOURS * 3600
    except Exception:
        return True


def main() -> int:
    state = load_state()
    state["total_checks"] = int(state.get("total_checks") or 0) + 1

    balance = get_openrouter_balance()
    if not balance["success"]:
        append_log({"timestamp": now_iso(), "success": False, "error": balance["error"], "total_checks": state["total_checks"]})
        save_state(state)
        print(f"❌ OpenRouter credit monitor failed: {balance['error']}")
        return 1

    remaining = balance["remaining"]
    below = remaining < MIN_BALANCE
    append_log(
        {
            "timestamp": now_iso(),
            "success": True,
            "total_credits": balance["total"],
            "used_credits": balance["used"],
            "remaining_credits": remaining,
            "below_threshold": below,
            "total_checks": state["total_checks"],
        }
    )

    should_alert = below and (not state.get("was_below_threshold") or reminder_due(state))

    state.update(
        {
            "was_below_threshold": below,
            "last_remaining": remaining,
            "last_check_at": now_iso(),
        }
    )
    if should_alert:
        state["last_low_alert_at"] = now_iso()
    save_state(state)

    if should_alert:
        print(f"⚠️ OpenRouter credits are low: {remaining:.2f} remaining, below threshold {MIN_BALANCE:.2f}.")
        print(f"Add credits: https://openrouter.ai/credits")
        print(f"Suggested top-up: {ADD_AMOUNT:.2f} credits")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
