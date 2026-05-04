# Daily Briefing

Editable implementation notes for Sirius' daily 07:00 briefing to Jordi.

## Schedule

- Run every day at **07:00 Europe/Madrid**.
- Deliver to Jordi on Telegram.
- Keep it concise and useful; no need for long explanations.

## Sources

### Weather

- Location: **Granollers, Catalonia, Spain**.
- Units: international/metric standard:
  - temperature in °C
  - wind in km/h
  - precipitation in mm / % chance when available
- Use `wttr.in` or another reliable weather source.
- Include today's outlook and anything Jordi should know before leaving home: rain, unusual temperature, strong wind.

### Obsidian tasks

- Vault path: `/home/sirius/obsidian/vaults/main`
- Main task note: `Work/Global To-dos.md`
- Before reading, make a best-effort sync if safe. Continuous sync should already be running, so do not block the briefing if a one-shot sync fails.

Task interpretation for this first iteration:

1. Read the `🔴 PENDING (HIGH PRIORITY - URGENT)` section.
2. List anything that looks critical or urgent, especially:
   - explicit deadlines
   - overdue dates
   - words like urgent/critical/blocker/today/tomorrow
   - high-priority items with concrete deliverables
3. Then list the **next top 5 tasks** across pending sections.
4. Preserve Jordi's original task language when helpful; add short context only if it clarifies priority.

## Output format

Use this structure:

```text
Bon dia Jordi — briefing ràpid:

Weather — Granollers
- ...

Urgent / critical
- ...

Next 5 tasks
1. ...
2. ...
3. ...
4. ...
5. ...
```

If no urgent/critical task is found, say so plainly and still provide the next 5 tasks.
