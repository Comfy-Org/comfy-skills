---
description: Build a classified action-items to-do list from someone's recent Slack and Notion activity and append it to a Notion page
---

Generate an action-items to-do list from a person's recent Slack and Notion activity, then append it to a Notion page as dated checkbox blocks.

ARGUMENTS: $ARGUMENTS

Expected arguments (in any order; ask for any that are missing):

- **Person** — the email (or Slack handle) of the person whose activity to digest. Used to resolve their Slack user.
- **Notion page** — the URL or ID of the Notion page to append the to-do list to.
- **Lookback window** (optional) — e.g. `3h`, `6h`, `since 9am`, `today`. Defaults to the last ~3 hours (the gap since the previous run).

Do not hardcode any person or page. Read them from the arguments. If either the person or the target Notion page is missing, ask for it before doing anything else.

## Lookback window

Cover activity from the last ~3 hours by default (since the previous run). If a clear timestamp boundary is unavailable, default to the past 3 hours. Honor an explicit window passed in the arguments.

## Step 1: Gather Slack activity

Load the Slack MCP tools first (via ToolSearch with keyword `slack` if they are not already available).

1. Resolve the person's Slack user ID with `slack_search_users` (using the provided email or handle).
2. Find messages from the lookback window that are EITHER (a) written by the person, OR (b) messages where the person is @-mentioned or tagged. Use `slack_search_public_and_private` with queries like `from:@<handle>` and `to:@<handle>`.
3. Read the relevant threads with `slack_read_thread` for full context before deciding what is an action. A single message out of context often reads as a commitment when the thread shows it was already handled, or vice versa.

## Step 2: Gather Notion comments

Load the Notion MCP tools first (via ToolSearch with keyword `notion` if they are not already available).

Look for recent Notion comments involving the person within the lookback window: comments they wrote, or comments that mention them or ask them for something. Use `notion-search` and `notion-get-comments` as needed. Read enough surrounding context to tell a real ask from a passing mention.

## Step 3: Derive action items

From the gathered Slack messages and Notion comments, produce a list of action items. Classify each into exactly one of three buckets:

1. **Committed** — the person clearly committed to doing something ("I'll send that", "I'll review by EOD", "on it"). State the action and, if mentioned, the deadline and who is waiting on it.
2. **Needs clarification (ambiguous)** — it is unclear whether the person owns an action, or whether one exists at all. Note what should be clarified and with whom.
3. **Likely no action** — items that looked like they might be tasks but, on reading, require nothing from the person. Note briefly why, so they can confirm.

Be precise and link back to the source Slack message or Notion comment wherever possible. Do not invent commitments. Only include what the text actually supports. When in doubt between Committed and Needs clarification, choose Needs clarification.

## Step 4: Write to Notion

Append the to-do list to the Notion page given in the arguments.

1. Read the page first with `notion-fetch`.
2. Append a new dated section (a heading with the current date and time, computed via bash `date`) using `notion-update-page`. Do NOT overwrite prior runs. The page is a running log.
3. Group the items under the three buckets above (Committed / Needs clarification / Likely no action) as Notion to-do (checkbox) blocks.
4. Avoid duplicating items that already appear from a recent run. If an identical open item already exists on the page, skip re-adding it.
5. Append an attribution line to the new section identifying the agent (e.g. "Created by Claude Code").

## Output

After updating Notion, briefly summarize in chat what you added:

- Counts per bucket.
- Any high-priority committed items with their deadlines.
- A link to the Notion page.

If there was no relevant activity in the window, say so and do NOT add an empty section to the page.

## Hard rules

1. **No invented commitments.** Every Committed item must trace to a specific message or comment where the person said they would do it. Link the source.
2. **Read threads before classifying.** Out-of-context messages mislead. Open the thread.
3. **Append, never overwrite.** Add a dated section; leave prior sections intact.
4. **No duplicate open items.** If a recent run already logged an identical open item, skip it.
5. **Empty window means no section.** Do not write a heading with nothing under it.
6. **No hardcoded identities.** Person and target page always come from the arguments.
