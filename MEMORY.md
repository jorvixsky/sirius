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
- creditcard: [Unknown - needs investigation]

## Heartbeat Setup
- Created heartbeat-state.json for tracking periodic checks
- HEARTBEAT.md is empty (no scheduled tasks)

## Recent Work
- Fixed Telegram connectivity issues
- Analyzed model configuration problems
- Started investigating skill dependency issues

## Lessons Learned
- Always check session_status for current model configuration
- PATH issues can prevent CLI commands from working
- Memory files are essential for continuity between sessions