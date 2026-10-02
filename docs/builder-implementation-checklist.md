## The Builder's Implementation Checklist

Status: implemented on the newsletter lane. Today's Issue is unchanged.

Target process: outbound newsletter prep. Hacker News signals go in. A person approves the draft before Gmail.

### Phase 1: Workflow Automation (The 60% Rule)

- [x] **Identify the target:** Outbound newsletter prep (fetch signals, draft the edition, hand it to a person).
- [x] **Draw the line:** Machine stages are fetch, classify, plan, execute, schema check, and the banned-word filter. Human stages are edit, rate, approve/send, and the Monday prompt review. `AUTOMATED_STAGES` is 60 percent of that list.
- [x] **Automate the first half:** `run_automated_pipeline()` in `builder_pipeline.py` stops when the packet is written. It does not send mail.
- [x] **Standardize the handoff:** `REVIEW_DASHBOARD=1` opens the local review desk. The operator edits the draft and uses Approve / Send.

### Phase 2: Feedback & Iteration Moats

- [x] **Install micro-feedback UI:** The review desk asks "Was this helpful?" with Yes and No on the newsletter draft.
- [x] **Capture the "Why":** No reveals an optional "What was missing?" field before the rating is saved.
- [x] **Centralize the logs:** Ratings append to `output/feedback/feedback.jsonl`. Set `SLACK_FEEDBACK_WEBHOOK` to also post each rating.
- [x] **Establish the ritual:** Monday 09:00 local, 30 minutes, in `fixtures/prompt_review_ritual.json`. `PROMPT_REVIEW=1` prints the agenda and the missing-notes.

### Phase 3: Cost & Latency Routing

- [x] **Audit current API calls:** `MODEL_AUDIT=1` prints the touchpoint list. The only model calls are classify, plan, and execute.
- [x] **Down-tier the basics:** Classification and outline planning use `gemini-1.5-flash`.
- [x] **Protect the premium tier:** `gemini-1.5-pro` runs only for final synthesis.

### Phase 4: Production Reliability

- [x] **Enforce structured outputs:** Planner and executor JSON is schema-checked before the markdown is rendered.
- [x] **Install the safety net:** The banned-word filter runs after generation and again when the desk saves or approves an edit.
- [x] **Define the fallback:** A timeout or invalid draft is replaced with the hardcoded held-for-review copy.
- [x] **Build the escalation path:** The same failure is written to `output/escalations/` and listed on the review desk.

### Phase 5: The "Brief, Then Build" Prompt Migration

- [x] **Identify the weakest output:** The old newsletter path asked one model call to invent the hook, the summaries, the feature section, and the takeaways together.
- [x] **Split the prompt:** Stage `plan_outline` writes the outline and success criteria on the fast tier. Stage `execute_draft` follows that outline on the premium tier. Story titles and URLs are copied from the outline, so the executor cannot swap in a new source.
