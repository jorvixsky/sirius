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

Weekend rule:

- On **Saturday or Sunday in Europe/Madrid**, do **not** include any Global To-dos in the briefing.
- On weekends, omit both task sections entirely: `Urgent / critical` and `Next 5 tasks — in progress`.
- Still send the briefing with weather and, if useful, a short weekend-friendly note. Do not mention hidden to-dos unless there is a genuine source/blocker problem.

Weekday task interpretation:

1. Read the `🔴 PENDING (HIGH PRIORITY - URGENT)` section.
2. In `Urgent / critical`, list **all unchecked top-level tasks** from that red urgent section. Do not filter them down. Do not include checked tasks. Include nested bullets under an urgent task only when they are part of that task and useful for context.
3. Read the `🟡 PENDING (IN PROGRESS)` section.
4. In `Next 5 tasks`, list the **first five unchecked top-level tasks from the yellow in-progress section only**. Do not pull tasks from the red urgent section into this list.
5. Preserve Jordi's original task language when helpful; add short context only if it clarifies priority.

## Output format

Use Telegram-friendly Markdown-style formatting. Keep it readable, not noisy.

Use this weekday structure:

```text
☀️ **Bon dia Jordi — briefing ràpid**

🌦️ **Weather — Granollers**
- _Ara:_ ...
- _Avui:_ ...
- _Nota:_ ...

🚨 **Urgent / critical**
- ...
- ...

📌 **Next 5 tasks — in progress**
1. ...
2. ...
3. ...
4. ...
5. ...
```

Use this weekend structure:

```text
☀️ **Bon dia Jordi — briefing ràpid**

🌦️ **Weather — Granollers**
- _Ara:_ ...
- _Avui:_ ...
- _Nota:_ ...

🌿 **Cap de setmana**
- ...
```

Formatting rules:
- Use **bold** for section headers and truly important labels.
- Use _italics_ for small labels like _Ara_, _Avui_, _Nota_ or short context.
- Use emojis only at section starts or for genuinely useful emphasis; avoid clutter.
- Keep task text mostly as Jordi wrote it.

On weekdays, if no urgent/critical task is found, say so plainly and still provide the next 5 tasks.
