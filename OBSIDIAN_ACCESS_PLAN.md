# Obsidian Access Plan for Sirius

Goal: give Sirius server-side access to Jordi's Obsidian vault using official Obsidian Sync Headless, so Sirius can read/search notes and optionally write structured notes back.

## Chosen approach: Option A — Obsidian Sync + official headless client

Why this option:
- Official Obsidian Sync support.
- Works on a server without GUI.
- Preserves Obsidian Sync encryption/version history/conflict handling.
- Vault remains plain Markdown locally, which is ideal for AI-assisted reading/searching/editing.
- Avoids fragile desktop/GUI workarounds.

## What Jordi needs to do

1. Purchase Obsidian Sync.
2. In Obsidian desktop/mobile, connect the target vault to Sync.
3. Decide which vault Sirius should access.
4. Decide whether Sirius should have:
   - read-only access initially, recommended; or
   - bidirectional read/write access after trust/testing.
5. Provide the following securely during setup:
   - Obsidian account email.
   - Obsidian account password, or be present for interactive login.
   - MFA code if enabled.
   - E2EE vault password if the Sync vault uses end-to-end encryption.
6. Tell Sirius the remote vault name exactly as shown in Obsidian Sync.

Important: do not paste passwords into persistent notes. Use interactive prompts where possible.

## What Sirius will do on the VPS

### 1. Confirm prerequisites

- Node.js >= 22 is required.
- Current server has Node v24, so this should be fine.

Command:

```bash
node --version
npm --version
```

### 2. Install official headless client

```bash
npm install -g obsidian-headless
```

Then confirm:

```bash
ob --help
```

### 3. Create a dedicated vault location

Recommended path:

```bash
mkdir -p /home/sirius/obsidian
mkdir -p /home/sirius/obsidian/vaults
```

Example vault path:

```bash
/home/sirius/obsidian/vaults/main
```

### 4. Login to Obsidian from the server

Preferred: interactive login so credentials are not written into shell history.

```bash
ob login
```

Jordi will provide email/password/MFA interactively when needed.

### 5. List remote vaults

```bash
ob sync-list-remote
```

We identify the target vault name or ID.

### 6. Set up local sync

```bash
cd /home/sirius/obsidian/vaults/main
ob sync-setup --vault "VAULT NAME" --device-name "sirius-vps"
```

If E2EE is enabled, the command will ask for the encryption password.

### 7. Start with safe sync mode

Initial recommended mode: pull-only.

```bash
ob sync-config --path /home/sirius/obsidian/vaults/main --mode pull-only --device-name "sirius-vps"
```

This lets Sirius read and index notes without accidentally changing Jordi's vault.

### 8. Perform first sync

```bash
ob sync --path /home/sirius/obsidian/vaults/main
```

Check status:

```bash
ob sync-status --path /home/sirius/obsidian/vaults/main
```

### 9. Optional continuous sync service

Once first sync works, create a systemd user/service or cron-managed process to keep the vault updated:

```bash
ob sync --path /home/sirius/obsidian/vaults/main --continuous
```

We should run this as a managed background service, not manually in a terminal forever.

### 10. Create Sirius operating rules for vault access

Recommended policy:

- Read freely when helping Jordi with tasks.
- Do not expose private notes to other chats or third parties.
- Do not edit notes unless Jordi explicitly asks, until write mode is enabled.
- Put Sirius-generated notes in a dedicated folder, e.g. `Sirius/`.
- For writes, prefer appending dated notes or creating new files over editing human-authored notes.

### 11. Optional: enable write access later

After testing read-only mode:

```bash
ob sync-config --path /home/sirius/obsidian/vaults/main --mode bidirectional
```

Recommended Sirius write folder:

```text
Sirius/
Sirius/Inbox/
Sirius/Summaries/
Sirius/Tasks/
```

## Security notes

- Obsidian Sync may be end-to-end encrypted remotely, but once synced, local Markdown files on the VPS are readable by processes/users with file access.
- The VPS should be treated as trusted infrastructure.
- Avoid syncing unnecessary sensitive folders if possible.
- Prefer pull-only first.
- Avoid storing plaintext credentials in files.
- Backups/versioning should be considered before bidirectional writes.

## First test after setup

Ask Sirius:

- "List the top-level folders in my Obsidian vault."
- "Find notes mentioning BSC."
- "Summarize my current active projects from Obsidian, but do not modify anything."

If results are good, then decide whether to allow write-back.
