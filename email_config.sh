#!/bin/bash

# Install Himalaya locally in user directory
echo "Installing Himalaya..."
curl -L -o /tmp/himalaya.tar.gz https://github.com/soywod/himalaya/releases/latest/download/himalaya-linux-x86_64.tar.gz
mkdir -p ~/.local/bin
tar -xzf /tmp/himalaya.tar.gz -C ~/.local/bin himalaya
chmod +x ~/.local/bin/himalaya

# Add to PATH if not already
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create Himalaya config directory
mkdir -p ~/.config/himalaya

# Create config file for sirius@jordiplanas.cat
cat > ~/.config/himalaya/config.toml << 'EOF'
[accounts.sirius]
email = "sirius@jordiplanas.cat"
display-name = "Sirius AI Assistant"
default = true

# IMAP settings for CDMon
backend.type = "imap"
backend.host = "mail.jordiplanas.cat"  # Common pattern for custom domains
backend.port = 993
backend.encryption.type = "tls"
backend.login = "sirius@jordiplanas.cat"
backend.auth.type = "password"
backend.auth.raw = "@0OmXOSLstaDFD17"

# SMTP settings for CDMon
message.send.backend.type = "smtp"
message.send.backend.host = "mail.jordiplanas.cat"  # Same as IMAP usually
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "sirius@jordiplanas.cat"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "@0OmXOSLstaDFD17"

# Folder aliases
[accounts.sirius.folder.alias]
inbox = "INBOX"
sent = "Sent"
drafts = "Drafts"
trash = "Trash"
EOF

echo "Himalaya configuration created at ~/.config/himalaya/config.toml"
echo "Testing connection..."

# Test the installation
if command -v ~/.local/bin/himalaya &> /dev/null; then
    echo "Himalaya installed successfully"
    echo "Version: $(~/.local/bin/himalaya --version 2>/dev/null || echo "version check failed")"
else
    echo "Himalaya installation failed"
fi