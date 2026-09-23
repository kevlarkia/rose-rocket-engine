# Chat extraction — September 23, 2026

Recovered project record. This file does not replace a sealed issue.
Where it disagrees with `archive/2026-09-23_176/payload.txt`, the payload wins.
See `archive/ISSUE_LEDGER.md`.

## 1. Executive Reconstruction

Rose Rocket is a digital newspaper for one incarcerated reader, sent on a monitored platform. Delivery depends on flush-left 7-bit ASCII, the character ceiling, and a SHA-256 seal of the exact file. Recent rules cut production chatter so the paper reads as a newspaper.

## 2. Project Identity

- Project name: Rose Rocket, version 2.5
- Alternate names: none
- Purpose: news, research, music, and personal messages
- Intended reader: Marko
- Creator and operator: Clinton
- Distribution: SmartInmate (Smart Communications)
- Tone: reader-first, one editorial identity no matter which model drafted it
- FROM ME is Clinton's. The model does not ghostwrite it.
- Constraints: 7-bit ASCII, 30,000-character ceiling, cryptographic seal, pre-flight QA

## 3. Historical Timeline

- Before 2.5, the paper explained missing sections inside the reader copy.
- Version 2.5 separates QA, the seal, and delivery states.
- Clinton added silent omission: the system may know what is missing, and it does not tell Marko again and again.
- A September 23 chat drafted a Wednesday AI deep dive about GPT-6 Astra, Stripe/OpenRouter, an MIT AI drone, AlphaGenome, and Z.ai GLM-5.3-Flash. That draft is not the sealed Issue 176 in this repository.
- Clinton rejected a mix-up with commercial trucking software that uses the same name. Source discipline: this Rose Rocket is the Marko newspaper only.

## 4. Issue Ledger

The extraction that produced this note could not see an issue number for September 23. This repository can. Issue 176 is sealed. Headline: THE ROUTER IS PART OF THE MODEL. Status: VALIDATED_READY, not sent.

## 5. Editorial Section Inventory

- AI Deep Dive: active. Full column Monday, Wednesday, Friday. Shorter AI desk on other days.
- FROM ME: active. Monday only. Clinton writes it.
- Music: active. Friday only. Verified Marko playlist, song, or artist.
- Candy Market: active monthly. Anchor day unset. Do not force it.
- Birthdays: active weekly. Weekday unset.
- Workout / fitness: active weekly. Weekday unset.
- Research: active. Floats, and continues when useful.

## 6. Current Standing Rules

See `CURRENT_RULES.md`.

## 7. Retired and Superseded Rules

The reader copy used to explain what was missing. Silent omission replaces that. Clinton added it so Marko does not have to read the production system.

## 8. Production Workflow

1. Gather sources that are accurate for that America/Los_Angeles day, and build the sections that weekday calls for.
2. Run QA on the exact final TXT.
3. SHA-256 that file. Any later edit returns to step 2.
4. Archive the TXT, QA record, seal, and delivery state.
5. Staging into Smart Communications may be prepared.
6. Clinton sends. Never send automatically. Fail closed on MFA, CAPTCHA, a hash mismatch, or a recipient mismatch.

## 9. Rose Rocket 2.5 Architecture

Built so the SmartInmate reader does not break the layout.

- VALIDATED_READY: QA passed, sealed, not staged
- STAGED_FOR_DELIVERY: loaded into the UI, not sent
- SENT_TO_MARKO: only with evidence of transmission

Fail closed. Do not improvise past an auth failure, a layout change, or the wrong recipient.

## 10. Prompt Library

Name: ROSE ROCKET — COMPLETE CHAT INFORMATION EXTRACTION
Purpose: recover rules and state. Do not generate a newspaper.
Version: current
Inputs: full chat history
Output: the 20 sections listed in `tools/extraction_prompt.txt`

## 11. Archive and file system

Each issue keeps a validated TXT, a QA record, a SHA-256 seal, and a delivery state. Archive before any send attempt.

## 12. Design and format

7-bit ASCII. Flush left. No decoration that would break the SmartInmate reader.

## 13. Content sources

News and tech for the AI deep dive must be fresh for America/Los_Angeles. Clinton supplies FROM ME. Music comes from Marko's documented preferences or a verified playlist.

## 14. Marko request register

The music feature has to reflect Marko's real preferences.

## 15. Clinton decision register

- Silent omission
- Human send gate. Clinton alone authorizes transmission.
- Source discipline. Trucking software is out of scope.

## 16. Ideas not yet adopted

The Builder's Implementation Checklist (the 60 percent rule, routing, schema checks) was discussed. It is not part of the canonical rules. Schema checks and fail-closed behavior already fit version 2.5.

## 17. Contradictions and conflicts

- Version A, rejected: Rose Rocket is commercial transportation software.
- Version B, in force: Rose Rocket is the SmartInmate newspaper.
- Version B wins.

A second conflict: one chat described an unnumbered September 23 draft about GPT-6 Astra and related items. The sealed Issue 176 is a different paper. The seal wins.

## 18. Open questions

- Most historical issue numbers and dates are not in this repository.
- Candy Market has no permanent anchor day.
- Birthdays and Workout have no permanent weekday.
- The library path used for Issue 176 was `/Rose Rocket 2.5/Validated/2026/09/`. The in-repo tree is `rose_rocket_v2.5/archive/YYYY-MM-DD_Issue/`.

## 19. Current canonical state

Rose Rocket 2.5 is Clinton's newspaper for Marko on SmartInmate. QA and a SHA-256 seal of the exact file come before Clinton sends. The reader copy is flush-left 7-bit ASCII within 30,000 characters. Facts match America/Los_Angeles for that day. Missing sections stay out of the paper.

Issue 176 is VALIDATED_READY and NOT_SENT.

## 20. Recommended master file tree

```
rose_rocket_v2.5/
├── rules/
│   ├── CURRENT_RULES.md
│   └── CHAT_EXTRACTION_2026-09-23.md
├── archive/
│   ├── ISSUE_LEDGER.md
│   └── 2026-09-23_176/
│       ├── payload.txt
│       ├── seal.json
│       ├── qa_record.json
│       └── delivery_state.json
└── tools/
    └── extraction_prompt.txt
```
