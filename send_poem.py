#!/usr/bin/env python3
"""
Send a romantic poem to Jordi's girlfriend.
"""
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

# Email configuration
SENDER_EMAIL = os.environ.get('SIRIUS_EMAIL', 'sirius@jordiplanas.cat')
SENDER_PASSWORD = os.environ.get('SIRIUS_EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = 'laiamonente1@gmail.com'
JORDI_BCC_EMAIL = os.environ.get('SIRIUS_DEFAULT_BCC', 'hola@jordiplanas.cat')

# SMTP configuration
SMTP_SERVER = os.environ.get('SIRIUS_SMTP_SERVER', 'smtp.jordiplanas.cat')
SMTP_PORT = int(os.environ.get('SIRIUS_SMTP_PORT', '587'))

# Romantic poem for Liam - Second poem
POEM = """My Dearest Liam,

Across the pixels and through the air,
I send this message with loving care,
Though we're apart, you're always there,
In every thought, beyond compare.

Your laughter echoes in my mind,
A melody of the sweetest kind,
In your presence, peace I find,
A love that leaves all fear behind.

From morning coffee to evening wine,
Every moment feels divine,
Because I know that you are mine,
And in your love, I'll always shine.

So here's another verse, my dear,
To make your day bright and clear,
To whisper gently in your ear,
"I love you more with every year."

Forever yours,
Jordi

💖 Sent with infinite love via your AI assistant Sirius ⭐
"""

def send_poem():
    """Send the romantic poem."""
    msg = EmailMessage()
    msg['From'] = f'Jordi via Sirius <{SENDER_EMAIL}>'
    msg['To'] = RECIPIENT_EMAIL
    msg['Bcc'] = JORDI_BCC_EMAIL
    msg['Subject'] = '💖 Another Poem, Just Because'
    
    # Add date header
    msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # Set poem as body
    msg.set_content(POEM)
    
    try:
        # Connect to SMTP server
        print(f"Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}...")
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        smtp.starttls()
        
        print(f"Logging in as {SENDER_EMAIL}...")
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"Sending poem to {RECIPIENT_EMAIL} with Jordi Bcc'd...")
        smtp.send_message(msg)
        smtp.quit()
        
        print(f"✅ Poem successfully sent to {RECIPIENT_EMAIL}")
        print(f"Subject: 💌 A Poem Just For You")
        print(f"From: Jordi via Sirius <{SENDER_EMAIL}>")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send poem: {e}")
        return False

if __name__ == "__main__":
    send_poem()
