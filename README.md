# Sirius – AI Assistant Configuration Backup

This repository contains the complete workspace and configuration backup for Sirius, an OpenClaw AI assistant.

## Repository Purpose

- **Daily automatic backups**: Configuration, memory files, and skills are backed up daily via cron
- **Disaster recovery**: Quickly restore your AI assistant after system failure
- **Version history**: Track changes to your assistant's personality, tools, and memory over time

## What's Included

- `AGENTS.md` – Workspace documentation and conventions
- `SOUL.md` – Personality and behavioral guidelines
- `USER.md` – Information about the human you're assisting
- `MEMORY.md` – Long-term curated memory (updated periodically)
- `TOOLS.md` – Local tool configurations and API keys (keep private!)
- `IDENTITY.md` – Assistant identity metadata
- `HEARTBEAT.md` – Periodic check configuration
- `memory/` – Daily session logs and memory files
- `skills/` – Installed skills and their configurations
- `avatars/` – Custom avatar images
- `.clawhub/` – Skill registry cache
- `.creditclaw/` – CreditClaw API configuration

## 📋 Recovery Guide: After a Catastrophic Loss

If your OpenClaw installation is lost or corrupted, follow these steps to restore your Sirius assistant:

### 1. Prerequisites

Ensure you have:
- A fresh Ubuntu/Linux installation (or any compatible system)
- Node.js 24+ installed
- Git installed
- OpenClaw installed globally (`npm install -g openclaw`)

### 2. Clone and Restore

```bash
# Clone this repository
git clone https://github.com/jorvixsky/sirius.git ~/.openclaw/workspace

# Navigate to the workspace
cd ~/.openclaw/workspace

# Verify the backup
ls -la
```

### 3. Configure OpenClaw

```bash
# Run OpenClaw configuration wizard
openclaw configure --mode local

# Follow the prompts to set up:
# - Model provider (OpenRouter)
# - Telegram bot token
# - Other channels as needed
```

### 4. Restore API Keys and Secrets

Some sensitive data may need manual restoration:

1. **CreditClaw API Key**: Add to `TOOLS.md` or set environment variable:
   ```bash
   export CREDITCLAW_API_KEY=cck_live_386c2fa4ab908bbf35eb92a704badb8d112323a05a950091
   ```

2. **OpenRouter API Key**: Configure via OpenClaw auth profiles

3. **Telegram Bot Token**: Set in OpenClaw config

### 5. Verify and Test

```bash
# Check OpenClaw status
openclaw status

# Start the gateway
openclaw gateway start

# Test with a message via Telegram
```

### 6. Restore Cron Jobs

The backup includes cron job definitions in `cron/jobs.json`. To restore scheduled tasks:

```bash
# Check existing cron jobs
openclaw cron list

# If jobs aren't auto-restored, recreate them:
# - Daily backup at 01:00 UTC
# - Daily auto-update at 04:00 Europe/Madrid
```

### 7. Update Skills

```bash
# Update all skills to latest versions
clawdhub update --all
```

## 🔄 Daily Backup Schedule

- **01:00 UTC**: Full workspace backup (this repository)
- **04:00 Europe/Madrin**: Auto-update routine (OpenClaw + skills)

Backups run automatically via OpenClaw cron jobs. The `daily-sirius-config-backup` job commits all changes and pushes to GitHub.

## ⚠️ Security Notes

- **Private data**: This repository contains API keys and configuration. Keep it private!
- **GitHub token**: Uses a fine-grained personal access token for push access
- **Sensitive files**: Review `.gitignore` to ensure no secrets are accidentally committed

## 🛠️ Manual Backup

To trigger a manual backup:

```bash
cd ~/.openclaw/workspace
git add -A
git commit -m "Manual backup"
git push
```

## 📈 Monitoring

- Check backup status via Telegram messages
- Review commit history on GitHub
- Monitor cron job failures in OpenClaw logs

## 🆘 Troubleshooting

### Backup Failing
- Check GitHub token validity
- Verify network connectivity
- Check disk space

### Restoration Issues
- Ensure file permissions are correct (`~/.openclaw/` should be owned by your user)
- Verify OpenClaw version compatibility
- Check model provider API keys

---

*Last updated: 2026-05-04 | Backup commit: 6e5e93d*