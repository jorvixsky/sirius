#!/usr/bin/env python3
"""
Email utilities for Sirius AI Assistant.
Provides easy functions for sending emails from scripts.
"""
import smtplib
from email.message import EmailMessage
from typing import List, Optional

# Default configuration
DEFAULT_EMAIL = "sirius@jordiplanas.cat"
DEFAULT_PASSWORD = "@0OmXOSLstaDFD17"
DEFAULT_SMTP_SERVER = "smtp.jordiplanas.cat"
DEFAULT_SMTP_PORT = 587
DEFAULT_BCC_EMAIL = "hola@jordiplanas.cat"

def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: str = DEFAULT_EMAIL,
    from_name: str = "Sirius AI Assistant",
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    html_body: Optional[str] = None
) -> bool:
    """
    Send an email using Sirius email account.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text body
        from_email: Sender email (defaults to Sirius)
        from_name: Sender display name
        cc: List of CC recipients
        bcc: List of BCC recipients
        html_body: Optional HTML version of body
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    # Create message
    msg = EmailMessage()
    msg['From'] = f'{from_name} <{from_email}>'
    msg['To'] = to_email
    msg['Subject'] = subject
    
    if cc:
        msg['Cc'] = ', '.join(cc)

    # Jordi wants to be Bcc'd on every email Sirius sends.
    effective_bcc = list(dict.fromkeys([*(bcc or []), DEFAULT_BCC_EMAIL]))
    msg['Bcc'] = ', '.join(effective_bcc)
    
    # Set body
    if html_body:
        msg.set_content(body)
        msg.add_alternative(html_body, subtype='html')
    else:
        msg.set_content(body)
    
    # Prepare recipients
    all_recipients = [to_email]
    if cc:
        all_recipients.extend(cc)
    all_recipients.extend(effective_bcc)
    # BCC recipients are included in SMTP recipients; Python strips Bcc headers on send_message.
    
    try:
        # Connect and send
        smtp = smtplib.SMTP(DEFAULT_SMTP_SERVER, DEFAULT_SMTP_PORT, timeout=10)
        smtp.starttls()
        smtp.login(DEFAULT_EMAIL, DEFAULT_PASSWORD)
        
        # Send to all recipients (including BCC)
        smtp.send_message(msg, from_addr=from_email, to_addrs=all_recipients)
        smtp.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_alert_email(
    alert_type: str,
    message: str,
    severity: str = "info"
) -> bool:
    """
    Send a standardized alert email.
    
    Args:
        alert_type: Type of alert (e.g., "OpenRouter", "System", "Task")
        message: Alert message
        severity: "info", "warning", "critical"
    
    Returns:
        bool: Success status
    """
    severity_icons = {
        "info": "ℹ️",
        "warning": "⚠️",
        "critical": "🚨"
    }
    
    icon = severity_icons.get(severity, "ℹ️")
    
    subject = f"{icon} {alert_type} Alert: {message[:50]}..."
    
    body = f"""Sirius AI Assistant Alert

Type: {alert_type}
Severity: {severity.upper()}
Time: {__import__('datetime').datetime.now().isoformat()}

Message:
{message}

---
This alert was sent automatically by your AI assistant Sirius.
"""
    
    # Send to primary contact
    return send_email(
        to_email="hola@jordiplanas.cat",
        subject=subject,
        body=body
    )

def test_email_connection() -> bool:
    """Test SMTP connection and authentication."""
    try:
        smtp = smtplib.SMTP(DEFAULT_SMTP_SERVER, DEFAULT_SMTP_PORT, timeout=10)
        smtp.starttls()
        smtp.login(DEFAULT_EMAIL, DEFAULT_PASSWORD)
        smtp.quit()
        print("✅ SMTP connection successful")
        return True
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False

# Example usage
if __name__ == "__main__":
    print("Testing email utilities...")
    
    # Test connection
    if test_email_connection():
        # Send test email
        success = send_email(
            to_email="hola@jordiplanas.cat",
            subject="Email Utilities Test",
            body="This is a test of the email utilities module."
        )
        
        if success:
            print("✅ All tests passed!")
        else:
            print("❌ Failed to send test email")
    else:
        print("❌ Cannot proceed without SMTP connection")