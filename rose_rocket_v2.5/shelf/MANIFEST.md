# Shelf tools

Ms. Rocket is the sealed paper. These tools are Clinton's. None of them send.

## day_slate

Clinton reads what one America/Los_Angeles date owes.
Inputs: publication date, optional drawer, optional FROM ME text.
Refuses to write a reader copy, invent a birthday, choose the workout cycle length, name the first Candy Market day, or write a trigger-word list.

## from_me

Clinton files the Monday letter in his own words.
Inputs: the text he typed, a Monday date, a store directory.
Refuses to draft, polish from memory, or invent a personal section. An empty Monday stores nothing.

## source_drawer

Clinton files a verified birthday list, music note, or research note.
Inputs: kind, text, store directory.
Refuses any other kind. An empty filing stores nothing.

## check_copy

Clinton checks the exact payload bytes.
Inputs: payload bytes, optional publication date, optional rules directory.
Refuses to seal. Names the line and the rule on failure. An empty line is legal. A line that begins with a space or a tab is not.

## seal_copy

Clinton seals a payload that already passed.
Inputs: payload bytes, publication date, issue number, archive root, ledger path.
Refuses a missing issue number, a failed check, and any archive directory that already exists, including Issue 176.

## delivery_card

Clinton reads validated, waiting on a human, or sent.
Inputs: an archive directory.
Refuses every request to change the state, including a move to sent.

## marko_note

Clinton stores what Marko said.
Inputs: the feedback text, a store directory.
Refuses to generate an issue or edit the standing rules.

## rule_slip

Clinton proposes a rule and waits.
Inputs: the proposed text, the rules file, a proposals directory.
Refuses a proposal that breaks the character cap, 7-bit ASCII, or flush-left. A clean proposal is written beside the rules and is not applied.
