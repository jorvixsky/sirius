# MEMORY.md - Long-Term Memory

This is your curated long-term memory. Update it with significant events, lessons learned, preferences, and important context.

## Current Configuration Status
- **Date**: 2026-05-03 (initial setup)
- **Model**: openrouter/deepseek/deepseek-v3.2 ✓
- **Timezone**: Europe/Madrid (UTC+1/UTC+2)
- **Location**: Barcelona, Spain
- **Human**: Jordi Planas (Barcelona Supercomputing Center + software company)

## Issues Identified
1. **Model Configuration Issues**: Some sessions may be defaulting to incorrect models instead of deepseek-v3.2
2. **Missing Dependencies**: Some skills (like image processing) may have missing npm packages (e.g., sharp)
3. **PATH Configuration**: OpenClaw CLI not in PATH (located at ~/.npm-global/bin/openclaw)
4. **Memory System**: MEMORY.md didn't exist - now created

## Skills Installed
- auto-updater: Daily updates for Clawdbot and skills
- skill-vetter: Security-first skill vetting
- creditclaw-creditcard: Online shopping with payment methods
- himalaya-skill: Email CLI capabilities for IMAP/SMTP

## Heartbeat Setup
- Created heartbeat-state.json for tracking periodic checks
- HEARTBEAT.md is empty (no scheduled tasks)

## Recent Work
- Fixed Telegram connectivity issues
- Analyzed model configuration problems
- Started investigating skill dependency issues
- Created automated daily backup system with recovery guide
- Updated Node.js to version 24
- Configured email inbox monitoring every 15 minutes via cron job
- Optimized email monitor to notify only on new emails or errors (silent success)
- Set up complete email system with himalaya skill for sirius@jordiplanas.cat
- Implemented OpenRouter credit monitoring with email alerts
- Created multiple cron jobs for automated monitoring:
  - **Email Monitor**: Checks Sirius inbox every 15 minutes (silent on success, alerts on new emails/errors)
  - **OpenRouter Monitor**: Checks credit balance every 6 hours (silent on success, alerts when low)
  - **Daily Backup**: Daily git backup at 01:00 UTC (silent unless errors)
  - **Auto-Update**: Daily updates at 04:00 Madrid time (silent unless errors)
- All jobs configured with failure alerts (notify on Telegram when errors occur)
- **Silenced notifications**: Updated backup and auto-update scripts to output only errors (no success messages) per Jordi's request
- **Email Monitor**: Successfully checking Sirius inbox every 30 minutes - 14 checks completed, 1 test email present, no new emails detected

## Lessons Learned
- Always check session_status for current model configuration
- PATH issues can prevent CLI commands from working
- Memory files are essential for continuity between sessions
- Jordi wants to be Bcc'd at `hola@jordiplanas.cat` on all emails Sirius sends; treat this as mandatory and verify before sending.
- Jordi explicitly prefers that Sirius always use `himalaya` for sending email, not direct SMTP helper scripts. Prefer `/home/sirius/.openclaw/workspace/bin/send-email-himalaya-bcc.py` because it inserts the mandatory Bcc and pipes the message through `himalaya message send`.