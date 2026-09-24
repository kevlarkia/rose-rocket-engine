# Handoff: the supercute.fyi shelf

Audience: Grok, implementing in this repository.
Owner: Clinton.
Reader of the paper: Marko.
Host: supercute.fyi.

The front door is the shelf. supercute.fyi is where that shelf is presented. Ms. Rocket stands on the shelf. The tools on that same shelf are for Clinton. Build those tools. Do not build a separate command-line product and call it the door.

Do not send anything. Do not open SmartInmate. Do not draft a newspaper while building the shelf.

## What is already true

supercute.fyi is on Cloudflare. Mail points at Microsoft 365. As of this handoff there is no public website address record, and no supercute.fyi tool API in this repo. Do not invent a host API, a login, or a live page that is not here. Build the shelf tools in this repository so they can be placed on supercute.fyi when the site exists.

Ms. Rocket is the SmartInmate newspaper for Marko. She is not commercial trucking software. The object on the shelf that represents her is the sealed reader copy. The tools around her are operator tools. Marko does not see them.

## Read these first

- `rose_rocket_v2.5/rules/CURRENT_RULES.md` — standing rules. These win over the prompts when they disagree.
- `rose_rocket_v2.5/prompts/PROMPT_GENERATE_ISSUE.txt`
- `rose_rocket_v2.5/prompts/PROMPT_QA_CHECK.txt`
- `rose_rocket_v2.5/prompts/PROMPT_FEEDBACK_LOOP.txt`
- `rose_rocket_v2.5/prompts/PROMPT_RULE_UPDATE.txt`
- `rose_rocket_v2.5/archive/ISSUE_LEDGER.md`
- `rose_rocket_v2.5/archive/2026-09-23_176/` — sealed Issue 176. Fixture. Do not edit it.

Issue 176's two TXT paths are the same 21,208 ASCII bytes. SHA-256 is `220d19d57a2cc8a9dd13ac65d33f4c590702fb846d927b59a65dad2e3b27f269`. Re-hash both in tests. If either digest changes, the build has failed.

Do not put passwords, tokens, API keys, cookies, booking numbers, street addresses, or confirmation codes in any file you add.

## The shelf

One surface. Two kinds of things on it.

1. Ms. Rocket: the current sealed payload, its issue number, its date, and its delivery card. Read-only once sealed.
2. Clinton's tools, listed below. Each tool does one job. None of them send.

Put the tools in `rose_rocket_v2.5/shelf/`. Add `rose_rocket_v2.5/shelf/MANIFEST.md` with each tool's name, the one sentence Clinton would read, its inputs, and what it refuses to do. Implement them as plain Python functions a later supercute.fyi page can call. No network.

## Clinton's tools

### day_slate

Shows what today's paper owes, in America/Los_Angeles. This view is for Clinton. It must never be copied into a payload.

- Monday, Wednesday, Friday: full AI Deep Dive.
- Any other weekday: short AI desk.
- Monday: FROM ME is due only when Clinton has supplied the text. The tool does not write it.
- Thursday and Sunday: Birthdays are due only when a verified list is on file. Do not invent a birthday.
- Friday: Music is lyrics and themes only, and only when a verified source and an approved trigger-word list both exist.
- Research appears only when Clinton has filed research for that issue.

Fail closed on the unpinned rotations:

- Workout/Fitness is anchored Friday, September 25, 2026. The cycle length is still 17 or 18 days, not one number. Until Clinton sets `CYCLE_DAYS` in the rules, leave Workout off the paper, including on the anchor date.
- Candy Market's first day is not named. "The week after September 23, 2026" is not a date. Until Clinton sets `CANDY_ANCHOR`, leave Candy Market off the paper.
- There is no approved trigger-word list. Do not write one. Until Clinton adds `rose_rocket_v2.5/rules/SMARTINMATE_TRIGGER_WORDS.txt`, leave Friday music off the paper.

The slate may tell Clinton a section was left off. The payload may not contain `NOT DUE`, `SOURCE HOLD`, `NOT VERIFIED`, or `OMITTED`.

### from_me

Accepts text Clinton typed. Stores it for a Monday issue. Refuses to draft, polish from memory, or invent a personal section. If Monday arrives with no text, the paper omits FROM ME silently.

### source_drawer

Accepts a verified birthday list, a music note, or a research note that Clinton files. The paper may use only what is in the drawer. An empty drawer means that section is absent from the payload.

### check_copy

Runs exact-file QA on the payload bytes Clinton is holding. On failure, name the line and the rule. Do not seal.

Checks, in order:

1. Every byte is 7-bit ASCII (0-127).
2. No line begins with a space or a tab. A completely empty line is legal. Issue 176 uses empty lines and is already `VALIDATED_READY`. `PROMPT_QA_CHECK.txt` item 2 says every line must start with a visible character. That sentence is wrong for this paper. Follow the standing rule.
3. Byte length is strictly under 30,000.
4. The payload does not contain `NOT DUE`, `SOURCE HOLD`, `NOT VERIFIED`, or `OMITTED`.
5. On Friday, if music text is present and the trigger list exists, reject a listed trigger word. If the trigger list does not exist, reject a payload that contains a music section.
6. No credential material: no `API_KEY`, `PASSWORD`, `BEGIN PRIVATE`, `sk-`, or `token.json`.

### seal_copy

Runs `check_copy` on the same bytes. If it fails, write nothing. If it passes, SHA-256 those bytes and create `rose_rocket_v2.5/archive/YYYY-MM-DD_N/` with:

- `payload.txt` — the original bytes
- `sha256_seal.json`
- `qa_record.json`
- `delivery_state.json` with `current_state: VALIDATED_READY`, `staging_status: SMARTINMATE_REQUIRES_HUMAN`, `send_status: NOT_SENT`, recipient Marko

`--issue` is required. Do not invent the next number. If the archive directory already exists, stop. Do not overwrite Issue 176. Append one factual line to `ISSUE_LEDGER.md`. Then stop.

### delivery_card

Reads the delivery state and shows it to Clinton: validated, waiting on a human, or sent. Sending is not this tool. There is no button that transmits.

### marko_note

Stores feedback Clinton types in from Marko. Confirms what would change in later drafting. Does not generate an issue. Does not edit `CURRENT_RULES.md` by itself. A rule change is only a draft for Clinton to approve.

### rule_slip

Takes a rule Clinton wants added. Checks it against the 30,000-character cap, 7-bit ASCII, and flush-left. If it conflicts, say so and do not change the rules. If it does not conflict, write the proposed text beside the current rules and wait. Do not apply it. Do not generate an issue.

## Tests

Use `unittest`. No network.

- Both Issue 176 TXT paths still hash to `220d19d57a2cc8a9dd13ac65d33f4c590702fb846d927b59a65dad2e3b27f269`.
- `check_copy` rejects one leading space and does not leave a new archive directory.
- `check_copy` accepts `Hello.\n\nWorld.\n`.
- A 30,000-byte payload fails. 29,999 passes the length check.
- A non-ASCII byte fails.
- `day_slate` for Wednesday 2026-09-23 includes the full AI Deep Dive and does not include FROM ME.
- `day_slate` for Monday 2026-09-28 includes FROM ME and the full AI Deep Dive.
- `day_slate` for Thursday 2026-09-24 includes Birthdays.
- `day_slate` for Friday 2026-09-25 includes the full AI Deep Dive and leaves Music and Workout off the paper.
- `seal_copy` refuses to write `rose_rocket_v2.5/archive/2026-09-23_176/` again.
- `from_me` with an empty Monday stores nothing and does not invent a letter.
- `delivery_card` cannot move a state to `SENT_TO_MARKO`.

## Out of scope

- A supercute.fyi login, page design beyond the shelf, or any host API that is not in this repo.
- SmartInmate login, recipient selection, composer staging, credit use, or send.
- Choosing `CYCLE_DAYS` or the first Candy Market date.
- Inventing Marko's memories, playlists, birthdays, or FROM ME.
- Rewriting Issue 176.
