# Handoff: build the Rose Rocket v2.5 front door

Audience: Grok, implementing in this repository.
Owner: Clinton.
Reader: Marko.
Do not send anything. Do not open SmartInmate. Do not draft a newspaper while building the door.

## What the front door is

The front door is the local operator entry for one publication date in America/Los_Angeles. It decides which sections are due, accepts the exact payload bytes, runs QA on those bytes, and, only on a full pass, writes the archive and the SHA-256 seal.

It stops at `VALIDATED_READY` with `SMARTINMATE_REQUIRES_HUMAN` and `NOT_SENT`.

The front door is not the Smart Communications composer, not a Gmail draft, and not the older newsletter lane in `rose_rocket_engine.py`.

## Read these first

- `rose_rocket_v2.5/rules/CURRENT_RULES.md` — standing rules. These win over the prompts when they disagree.
- `rose_rocket_v2.5/prompts/PROMPT_GENERATE_ISSUE.txt` — how a later draft is written. The door does not call a model.
- `rose_rocket_v2.5/prompts/PROMPT_QA_CHECK.txt` — QA checklist. See the blank-line ruling below.
- `rose_rocket_v2.5/archive/ISSUE_LEDGER.md`
- `rose_rocket_v2.5/archive/2026-09-23_176/` — sealed Issue 176. Treat it as a fixture, not as a file to edit.

## Do not touch

- `rose_rocket_v2.5/archive/2026-09-23_176/payload.txt`
- `output/THE_ROSE_ROCKET__ISSUE-176__2026-09-23__Hump_Day_Dispatch.txt`

Both files are the same 21,208 ASCII bytes. SHA-256 is `220d19d57a2cc8a9dd13ac65d33f4c590702fb846d927b59a65dad2e3b27f269`. A post-seal edit is a failed release. Re-hash them in tests and fail the build if either digest changes.

Rose Rocket is the SmartInmate newspaper for Marko. Do not connect it to commercial trucking software. Do not put passwords, tokens, API keys, cookies, booking numbers, street addresses, or confirmation codes in any file you add.

## Blank-line ruling

`CURRENT_RULES.md` blocks a line that begins with a space or a tab. A completely empty line is legal. Issue 176 uses empty lines between sections and is already `VALIDATED_READY`.

`PROMPT_QA_CHECK.txt` item 2 says every line must start with a non-whitespace character. That wording would reject Issue 176. Implement the standing rule, not that stricter sentence. Do not rewrite the sealed payload to satisfy the prompt.

## What to build

Add a Python package the operator runs from the repo root:

```bash
python3 -m rose_rocket_v2.5.front_door slate --date YYYY-MM-DD
python3 -m rose_rocket_v2.5.front_door seal --date YYYY-MM-DD --issue N --payload PATH
```

`--date` is the publication date, interpreted as a calendar date in America/Los_Angeles. If `--date` is omitted, use today's date in that timezone. Do not use the machine timezone.

`--issue` is required for `seal`. Do not auto-assign the next issue number. Issue 176 already exists.

`--payload` is the exact file that would be pasted to Marko. QA and the hash run on those bytes, not on a rewritten copy.

### `slate`

Print an operator log to stdout. This log is not a reader copy. It may name sections that are due and sections that are skipped. It must never be written into `payload.txt`.

Due sections:

- Monday, Wednesday, Friday: full AI Deep Dive.
- Any other weekday: short AI desk.
- Monday: FROM ME, and only if Clinton supplies the text at draft time. The door does not write FROM ME.
- Thursday and Sunday: Birthdays, and only if a verified birthday list is supplied. Do not invent a birthday.
- Friday: Music, lyrics and themes only, and only when both a verified source and an approved trigger-word list exist. No audio.
- Research: include only when the caller passes research material. It floats. It is not on a fixed weekday.

Rotation, fail closed:

- Workout/Fitness anchor is Friday, September 25, 2026. The cycle length is not pinned. `CURRENT_RULES.md` says about 17 or 18 days. Do not choose 17 or 18. Until Clinton sets `CYCLE_DAYS` in the rules, omit Workout/Fitness, including on the anchor date.
- Candy Market's first date is not pinned. "The week after September 23, 2026" is not a single day. Until Clinton sets `CANDY_ANCHOR` in the rules, omit Candy Market.

There is no approved SmartInmate trigger-word list in the repo. Do not invent one. Until Clinton adds `rose_rocket_v2.5/rules/SMARTINMATE_TRIGGER_WORDS.txt`, omit Friday music.

Skipped sections are silent inside the payload. The slate may say they were skipped. The payload may not contain `NOT DUE`, `SOURCE HOLD`, `NOT VERIFIED`, or `OMITTED`.

### `seal`

1. Read the payload as bytes.
2. Run exact-file QA. On any failure, print the line number and the rule, write nothing under `archive/`, and exit non-zero.
3. On a full pass, SHA-256 the same bytes.
4. Create `rose_rocket_v2.5/archive/YYYY-MM-DD_N/` with:
   - `payload.txt` — the original bytes, unchanged
   - `sha256_seal.json` — hash, byte count, line count, issue, date, edition label, `archive_status: VALIDATED_READY`
   - `qa_record.json` — each check and its pass/fail, plus character count
   - `delivery_state.json` — `current_state: VALIDATED_READY`, `staging_status: SMARTINMATE_REQUIRES_HUMAN`, `send_status: NOT_SENT`, recipient Marko, and the same `actions_not_taken` list used for Issue 176
5. Append a short factual line to `rose_rocket_v2.5/archive/ISSUE_LEDGER.md`.
6. Stop. Print the archive path and the hash. Do not stage and do not send.

If that archive directory already exists, exit non-zero. Do not overwrite a sealed issue.

QA checks, in order:

1. Every byte is 7-bit ASCII (0-127).
2. No line begins with a space or a tab. Empty lines pass.
3. Byte length is strictly under 30,000.
4. The payload does not contain `NOT DUE`, `SOURCE HOLD`, `NOT VERIFIED`, or `OMITTED`.
5. On Friday, if music text is present and the trigger list exists, reject any listed trigger word. If the trigger list does not exist, reject a payload that contains a music section rather than guessing. On other weekdays this check passes.
6. The payload contains no credential material: no `API_KEY`, `PASSWORD`, `BEGIN PRIVATE`, `sk-`, or `token.json`.

A failure does not produce a seal "with a warning". No seal file means not ready.

## Acceptance tests

Use the standard library and `unittest`. No network.

- Issue 176's two TXT paths still hash to `220d19d57a2cc8a9dd13ac65d33f4c590702fb846d927b59a65dad2e3b27f269`.
- A payload with one leading space fails QA and leaves the archive directory absent.
- A payload that is only `Hello.\n\nWorld.\n` passes flush-left, seals, and records `NOT_SENT`.
- A 30,000-byte ASCII payload fails. 29,999 passes the length check.
- A non-ASCII byte fails.
- `slate --date 2026-09-23` (Wednesday) includes the full AI Deep Dive and does not include FROM ME.
- `slate --date 2026-09-28` (Monday) includes FROM ME and the full AI Deep Dive.
- `slate --date 2026-09-24` (Thursday) includes Birthdays.
- `slate --date 2026-09-25` (Friday) includes the full AI Deep Dive, names Music and Workout as skipped until their anchors exist, and does not print those skip reasons in a way that could be copied into a payload by the seal command.
- `seal` refuses to write `rose_rocket_v2.5/archive/2026-09-23_176/` again.

## Out of scope

- SmartInmate login, recipient selection, composer staging, credit use, or send.
- Rewriting `PROMPT_GENERATE_ISSUE.txt` into an API call.
- Changing Issue 176.
- Choosing `CYCLE_DAYS` or the first Candy Market date.
- Inventing Marko's memories, playlists, birthdays, or FROM ME.
