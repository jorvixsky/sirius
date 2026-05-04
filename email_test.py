#!/usr/bin/env python3
"""
Test email configuration for sirius@jordiplanas.cat
"""
import imaplib
import smtplib
import ssl
import socket
from email.message import EmailMessage

# Configuration
EMAIL = "sirius@jordiplanas.cat"
PASSWORD = "@0OmXOSLstaDFD17"

# Common IMAP/SMTP server patterns to test
IMAP_SERVERS = [
    "mail.jordiplanas.cat",
    "imap.jordiplanas.cat",
    "imap.cdmon.com",
    "mail.cdmon.com"
]

SMTP_SERVERS = [
    "mail.jordiplanas.cat",
    "smtp.jordiplanas.cat",
    "smtp.cdmon.com",
    "mail.cdmon.com"
]

IMAP_PORTS = [993, 143]
SMTP_PORTS = [587, 465, 25]

def test_imap_connection(server, port):
    """Test IMAP connection."""
    try:
        print(f"Testing IMAP {server}:{port}...")
        
        if port == 993:
            # SSL/TLS
            context = ssl.create_default_context()
            imap = imaplib.IMAP4_SSL(server, port, ssl_context=context)
        else:
            # StartTLS on port 143
            imap = imaplib.IMAP4(server, port)
            imap.starttls()
        
        # Try to login
        imap.login(EMAIL, PASSWORD)
        
        # List folders
        status, folders = imap.list()
        
        imap.logout()
        
        print(f"✓ IMAP {server}:{port} - Success!")
        print(f"  Folders found: {len(folders) if folders else 0}")
        return True
    except Exception as e:
        print(f"✗ IMAP {server}:{port} - Failed: {e}")
        return False

def test_smtp_connection(server, port):
    """Test SMTP connection."""
    try:
        print(f"Testing SMTP {server}:{port}...")
        
        if port == 465:
            # SSL/TLS
            context = ssl.create_default_context()
            smtp = smtplib.SMTP_SSL(server, port, context=context)
        else:
            # StartTLS on ports 587, 25
            smtp = smtplib.SMTP(server, port)
            if port in [587, 25]:
                smtp.starttls()
        
        # Try to login
        smtp.login(EMAIL, PASSWORD)
        
        # Create test message
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = "Test Email from Sirius AI"
        msg.set_content("This is a test email from your AI assistant.")
        
        # Try to send
        smtp.send_message(msg)
        
        smtp.quit()
        
        print(f"✓ SMTP {server}:{port} - Success!")
        return True
    except Exception as e:
        print(f"✗ SMTP {server}:{port} - Failed: {e}")
        return False

def main():
    print(f"Testing email configuration for {EMAIL}")
    print("=" * 60)
    
    # Test DNS resolution first
    print("\n1. DNS Resolution:")
    for server in set(IMAP_SERVERS + SMTP_SERVERS):
        try:
            ip = socket.gethostbyname(server)
            print(f"  {server} -> {ip}")
        except socket.gaierror as e:
            print(f"  {server} -> DNS resolution failed: {e}")
    
    # Test IMAP connections
    print("\n2. IMAP Connection Tests:")
    imap_success = False
    for server in IMAP_SERVERS:
        for port in IMAP_PORTS:
            if test_imap_connection(server, port):
                imap_success = True
                break
        if imap_success:
            break
    
    # Test SMTP connections
    print("\n3. SMTP Connection Tests:")
    smtp_success = False
    for server in SMTP_SERVERS:
        for port in SMTP_PORTS:
            if test_smtp_connection(server, port):
                smtp_success = True
                break
        if smtp_success:
            break
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  IMAP: {'✓ CONNECTED' if imap_success else '✗ FAILED'}")
    print(f"  SMTP: {'✓ CONNECTED' if smtp_success else '✗ FAILED'}")
    
    if imap_success and smtp_success:
        print("\n✅ Email configuration is working!")
    else:
        print("\n❌ Email configuration needs adjustment.")
        print("\nRecommended next steps:")
        print("1. Check CDMon control panel for exact server settings")
        print("2. Verify password is correct")
        print("3. Check if account is activated and not blocked")
        print("4. Contact CDMon support for exact IMAP/SMTP settings")

if __name__ == "__main__":
    main()