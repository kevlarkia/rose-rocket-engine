# Rose Rocket 2.5 — current rules

Rose Rocket is the digital newspaper Clinton writes for Marko and sends through SmartInmate (Smart Communications). It is not commercial trucking software. That mix-up is a source-discipline failure.

The paper must read like a newspaper. It must not read like a production log.

## Format

- 7-bit ASCII only. No emoji, smart quotes, or other Unicode.
- Flush left. No line may begin with a space or a tab. One leading-whitespace line blocks release.
- 30,000 characters is the hard ceiling, including spaces.
- QA runs on the exact TXT file that would be delivered.
- Seal that file with SHA-256. Any edit after the seal starts QA over.

## Truth

- Facts are computed for that day in America/Los_Angeles. Do not carry a stale status forward.
- Do not invent memories, feelings, relationship facts, plans, or Marko's preferences.
- Omission is better than fabrication.
- Silent omission: if a section is missing or not due, leave it out. Do not print production chatter such as NOT DUE or SOURCE HOLD.
- At most one exception report per issue, at the end, and only when something materially expected was left out.
- Do not let an internal evidence label sound stronger than it is. SOURCE_REPORTED is not INDEPENDENTLY_REVIEWED.
- No passwords, cookies, or secrets in artifacts.
- No booking numbers, street addresses, or confirmation codes.

## Sections

- AI Deep Dive: full column on Monday, Wednesday, and Friday. A short AI desk may run on other days.
- FROM ME: Monday only. Clinton writes it. The model may lightly polish. It may not ghostwrite.
- Music: Friday only, from a verified Marko playlist, song, or artist.
- Candy Market: monthly. The anchor day is not set. Do not force it.
- Birthdays: weekly. The weekday is not set.
- Workout / fitness: weekly. The weekday is not set.
- Research: floats, and continues when it is useful.

## Delivery

Archive the validated TXT, the QA record, the SHA-256 seal, and the delivery state before any send.

- `VALIDATED_READY`: QA passed, sealed, not staged.
- `STAGED_FOR_DELIVERY`: loaded into the SmartInmate UI, not sent.
- `SENT_TO_MARKO`: only with evidence that the message was transmitted.

Staging may be prepared. Sending is Clinton's. Never send automatically. If authentication, layout, recipient, or hash fails, stop.

`SMARTINMATE_REQUIRES_HUMAN` means the send gate is still closed.

## Not canonical

The Builder's Implementation Checklist is an idea on file. It is not part of these rules.
