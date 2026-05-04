#!/usr/bin/env python3
"""
Send a second romantic poem to Jordi's girlfriend.
"""
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Email configuration
SENDER_EMAIL = 'sirius@jordiplanas.cat'
SENDER_PASSWORD = '@0OmXOSLstaDFD17'
RECIPIENT_EMAIL = 'laiamonente1@gmail.com'
JORDI_BCC_EMAIL = 'hola@jordiplanas.cat'

# SMTP configuration
SMTP_SERVER = 'smtp.jordiplanas.cat'
SMTP_PORT = 587

# Second romantic poem for Liam
POEM = """My Dearest Liam,

Another day, another verse I write,
To fill your world with loving light,
With every word, my heart takes flight,
When I think of holding you so tight.

Through distance, time, and all that's far,
You're my bright and guiding star,
Exactly who and what you are,
Makes me feel like I've won the Oscar.

Your voice, a song I love to hear,
It chases away my every fear,
With you, everything becomes clear,
And all my dreams feel very near.

So here's my second gift of rhyme,
To brighten up your day and time,
A little piece of heart, so fine,
Forever yours, and you'll be mine.

With endless love,
Jordi

💕 Sent with double the love via your AI assistant Sirius ⭐⭐
"""

def send_poem():
    """Send the second romantic poem."""
    msg = EmailMessage()
    msg['From'] = f'Jordi (via Sirius) <{SENDER_EMAIL}>'
    msg['To'] = RECIPIENT_EMAIL
    msg['Bcc'] = JORDI_BCC_EMAIL
    msg['Subject'] = '💕 Second Poem: Because Once Was Not Enough'
    
    # Add date header
    msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # Set poem as body
    msg.set_content(POEM)
    
    try:
        # Connect to SMTP server
        print(f"📨 Connecting to SMTP server...")
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        smtp.starttls()
        
        print(f"🔐 Logging in...")
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"✉️ Sending second poem to {RECIPIENT_EMAIL} with Jordi Bcc'd...")
        smtp.send_message(msg)
        smtp.quit()
        
        print(f"✅ SECOND POEM successfully sent to {RECIPIENT_EMAIL}")
        print(f"📝 Subject: {msg['Subject']}")
        print(f"📤 From: {msg['From']}")
        print(f"📨 To: {msg['To']}")
        print(f"📄 Poem length: {len(POEM)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send second poem: {e}")
        return False

if __name__ == "__main__":
    send_poem()