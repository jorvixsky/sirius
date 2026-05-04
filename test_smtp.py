#!/usr/bin/env python3
import smtplib
import ssl
import socket

email = "sirius@jordiplanas.cat"
password = "@0OmXOSLstaDFD17"
recipient = "hola@jordiplanas.cat"

servers = [
    ("mail.jordiplanas.cat", 587),  # StartTLS
    ("mail.jordiplanas.cat", 465),  # SSL
    ("smtp.jordiplanas.cat", 587),
    ("smtp.jordiplanas.cat", 465),
    ("smtp.cdmon.com", 587),
    ("smtp.cdmon.com", 465),
    ("mail.cdmon.com", 587),
    ("mail.cdmon.com", 465),
]

for server, port in servers:
    print(f"\nTrying {server}:{port}...")
    try:
        if port == 465:
            # SSL
            context = ssl.create_default_context()
            smtp = smtplib.SMTP_SSL(server, port, context=context, timeout=10)
        else:
            # StartTLS
            smtp = smtplib.SMTP(server, port, timeout=10)
            if port == 587:
                smtp.starttls()
        
        print(f"  Connected, trying login...")
        smtp.login(email, password)
        print(f"  ✓ Login successful!")
        
        # Test send
        msg = f"""From: {email}
To: {recipient}
Subject: SMTP Test {server}:{port}

Testing SMTP connection from {server}:{port}
"""
        smtp.sendmail(email, recipient, msg)
        print(f"  ✓ Send test successful!")
        
        smtp.quit()
        print(f"  ✅ {server}:{port} WORKS!")
        break
    except socket.timeout:
        print(f"  ✗ Timeout connecting")
    except ConnectionRefusedError:
        print(f"  ✗ Connection refused")
    except socket.gaierror as e:
        print(f"  ✗ DNS error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")
else:
    print("\n❌ No SMTP server worked")