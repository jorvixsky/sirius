#!/usr/bin/env python3
"""
Final email test to hola@jordiplanas.cat
"""
import smtplib
from email.message import EmailMessage
import datetime

def send_test_email():
    email = 'sirius@jordiplanas.cat'
    password = '@0OmXOSLstaDFD17'
    recipient = 'hola@jordiplanas.cat'
    
    msg = EmailMessage()
    msg['From'] = 'Sirius AI Assistant <sirius@jordiplanas.cat>'
    msg['To'] = recipient
    msg['Subject'] = f'✅ Email Test from Sirius - {datetime.datetime.now().strftime("%H:%M")}'
    
    body = f"""Hola Jordi,

This confirms that your AI assistant Sirius has full email capabilities.

✅ Configuration Complete:
• Email: sirius@jordiplanas.cat
• IMAP Server: mail.jordiplanas.cat:993
• SMTP Server: smtp.jordiplanas.cat:587
• Sent: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

✅ What I can now do:
1. Send emails on your behalf
2. Receive and process incoming emails
3. Set up email notifications
4. Manage email communications

This is perfect for:
• OpenRouter balance alerts
• System status reports
• Task completion notifications
• General internet presence

Best regards,
Sirius ⭐
Your AI Assistant
"""
    
    msg.set_content(body)
    
    try:
        print("Connecting to SMTP server...")
        smtp = smtplib.SMTP('smtp.jordiplanas.cat', 587, timeout=10)
        smtp.starttls()
        print("Logging in...")
        smtp.login(email, password)
        print("Sending email...")
        smtp.send_message(msg)
        smtp.quit()
        print(f"\n✅ SUCCESS: Email sent to {recipient}")
        print(f"   From: {email}")
        print(f"   Subject: {msg['Subject']}")
        print(f"   Server: smtp.jordiplanas.cat:587")
        return True
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Sirius AI Email Configuration")
    print("=" * 60)
    send_test_email()