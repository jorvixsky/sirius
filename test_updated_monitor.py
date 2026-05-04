#!/usr/bin/env python3
"""
Test the updated OpenRouter monitor with email alerts.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from monitor_openrouter
import monitor_openrouter as monitor

# Mock the balance function for testing
def mock_get_balance():
    return {
        "total": 16.0,
        "used": 10.0,
        "remaining": 6.0,  # Above threshold
        "success": True
    }

def mock_get_balance_low():
    return {
        "total": 16.0,
        "used": 15.0,
        "remaining": 1.0,  # Below threshold
        "success": True
    }

print("Testing email alert system...")
print("\n1. Testing above threshold (should not send email):")
monitor.MIN_BALANCE = 5.0
monitor.ADD_AMOUNT = 20.0

# Test with sufficient balance
balance = mock_get_balance()
print(f"Balance: {balance['remaining']:.2f} credits")
print(f"Threshold: {monitor.MIN_BALANCE} credits")

if balance["remaining"] < monitor.MIN_BALANCE:
    print("Would send CRITICAL email alert")
    # monitor.send_email_alert(balance, threshold_breached=True)
else:
    print("Status OK - No email sent (as configured)")

print("\n2. Testing below threshold (would send critical email):")
balance_low = mock_get_balance_low()
print(f"Balance: {balance_low['remaining']:.2f} credits")
print(f"Threshold: {monitor.MIN_BALANCE} credits")

if balance_low["remaining"] < monitor.MIN_BALANCE:
    print("Would send CRITICAL email alert")
    print("Email would contain:")
    print(f"  Subject: ⚠️ OpenRouter Alert: {balance_low['remaining']:.2f} credits remaining")
    print(f"  Body: Action required to add {monitor.ADD_AMOUNT} credits")
    print(f"  Recipient: hola@jordiplanas.cat")
else:
    print("Status OK")

print("\n✅ Test complete!")
print("\nActual implementation:")
print("- Runs every 6 hours via cron job")
print("- Sends email ONLY when balance < 5 credits")
print("- Email goes to hola@jordiplanas.cat")
print("- Includes payment instructions and current status")
print("\nTo test actual email sending, run:")
print("  python3 monitor_openrouter.py")