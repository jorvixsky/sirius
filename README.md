# Sirius – AI Assistant Configuration Backup

This repository contains the complete workspace and configuration backup for Sirius, an OpenClaw AI assistant.

It is intended to be a **private, drop-in recovery image**: if Sirius breaks or the host is lost, this repo should contain enough workspace state, cron wrappers, memory, skills, and local conventions to restore the assistant quickly.

## Repository Purpose

- **Daily automatic backups**: Configuration, memory files, and skills are backed up daily via cron
- **Disaster recovery**: Quickly restore your AI assistant after system failure
- **Drop-in replacement**: Preserve scripts, memory, cron helpers, logs/state, and skill files so a rebuilt Sirius behaves like the current one
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
- `cron_*.sh` – Cron wrapper scripts used by OpenClaw scheduled tasks
- `.env.example` – Environment variable template for secrets and service settings

## Important Current Behaviors

- **Quiet monitoring**: Cron jobs should not notify Jordi just because they ran. They only surface relevant events: new email, low OpenRouter credits, update/failure, or backup activity/errors.
- **Email Bcc rule**: Sirius should always Bcc Jordi at `hola@jordiplanas.cat` on emails it sends. This is documented in `USER.md`/`MEMORY.md` and represented by `SIRIUS_DEFAULT_BCC` in `.env.example`.
- **Secret handling**: Live secrets should be supplied via environment variables or `~/.openclaw/secrets/*` fallback files, not hardcoded in active scripts. Current cron wrappers support fallback files for the Sirius email password and OpenRouter management key.

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

Some sensitive data needs manual restoration. Start from the template:

```bash
cd ~/.openclaw/workspace
cp .env.example .env
$EDITOR .env
```

Then export these variables in your shell/service environment, or copy the values into the equivalent OpenClaw/systemd/cron environment.

Required or commonly used values:

1. **Email account**: `SIRIUS_EMAIL_PASSWORD`, plus SMTP/IMAP settings if they change. Fallback file supported by `cron_email_monitor.sh`:

   ```bash
   mkdir -p ~/.openclaw/secrets
   printf '%s\n' 'EMAIL-PASSWORD-REPLACE-ME' > ~/.openclaw/secrets/sirius_email_password
   chmod 600 ~/.openclaw/secrets/sirius_email_password
   ```

2. **Jordi Bcc**: `SIRIUS_DEFAULT_BCC=hola@jordiplanas.cat`

3. **OpenRouter management key**: `OPENROUTER_MANAGEMENT_KEY`, or this fallback file:

   ```bash
   mkdir -p ~/.openclaw/secrets
   printf '%s\n' 'OPENROUTER-MANAGEMENT-KEY-REPLACE-ME' > ~/.openclaw/secrets/openrouter_management_key
   chmod 600 ~/.openclaw/secrets/openrouter_management_key
   ```

4. **CreditClaw API Key**: Restore from secure storage or regenerate if needed

5. **OpenRouter chat/model API key**: Configure via OpenClaw auth profiles

6. **Telegram Bot Token**: Set in OpenClaw config

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
- **04:00 Europe/Madrid**: Auto-update routine (OpenClaw + skills)

Backups run automatically via OpenClaw cron jobs. The `daily-sirius-config-backup` job runs `cron_daily_backup.sh`, commits all workspace changes, and pushes to GitHub. Because this repo is private and meant for disaster recovery, it intentionally captures broad workspace state; however, provider push protection may still reject obvious secret literals, so active scripts prefer environment variables or `~/.openclaw/secrets/*` for live secrets.

## ⚠️ Security Notes

- **Private data**: This repository may contain sensitive configuration and operational history. Keep it private.
- **Secrets**: Prefer `.env`/service environment variables or `~/.openclaw/secrets/*`; `.env.example` is safe to commit and contains placeholders only.
- **GitHub token**: Uses a fine-grained personal access token for push access
- **Push protection**: GitHub may block commits containing recognized secret patterns. If that happens, remove the literal secret from the commit history before pushing.

## 🛠️ Manual Backup

To trigger a manual backup:

```bash
cd ~/.openclaw/workspace
./cron_daily_backup.sh
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

*Last updated: 2026-05-04 | Backup commit: 39782c5*
