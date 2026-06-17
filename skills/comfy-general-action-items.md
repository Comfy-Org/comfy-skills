Build a classified action-items to-do list from someone's recent Slack and Notion activity and append it to a Notion page: $ARGUMENTS

Give it a person (email or Slack handle) and a target Notion page, and it looks back over the last ~3 hours of Slack and Notion, finds anything that involves that person (messages they wrote or were tagged in, comments that ask them for something), and turns it into a to-do list.

Each item is classified into one of three buckets:

- **Committed** — they clearly said they'd do it. Includes the deadline and who's waiting, when stated.
- **Needs clarification** — unclear whether they own an action; notes what to clarify and with whom.
- **Likely no action** — looked like a task but needs nothing from them; notes why.

The list is appended to the given Notion page as checkbox blocks under a new dated heading, so prior runs stay intact as a history. Borderline items are filed under Needs clarification, never invented as commitments. If there's no relevant activity in the window, nothing is written.

Arguments: a person (email or Slack handle), a Notion page (URL or ID), and an optional lookback window (e.g. `6h`, `since 9am`). Needs the Slack and Notion MCP tools connected.
