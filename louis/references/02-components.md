# Components

## Headings

A heading orients the user on a screen or in a state.

Rules:

- short noun phrase, statement, or useful question;
- sentence case;
- no period at the end of a short heading;
- no decorative excitement;
- no generic "Important", "Information", "Note" without specifics;
- the heading and subheading must not repeat the same idea.

Bad: "Important".

Better: "Missing details".

## Buttons

A button is the user's line. It answers "What do I do?" and sets an expectation for what happens after the click.

Good buttons:

- "Save";
- "Delete";
- "Try again";
- "Translate";
- "Continue";
- "Got it".

Avoid:

- "I want to delete";
- "Saving";
- "I understand";
- "OK" when a specific verb is clearer;
- a long explanation inside a button.

For dangerous actions, be explicit: "Delete", "Yes, delete", "Delete project?".

For a pause or a refusal, use "Cancel", "Not now", "Later", "Back" as the context fits.

Do not use "Yes" and "No" in dialogs when verbs can name the action.

Keep buttons to 1-3 words when possible.

## Links

A link must say where the user will go or what it will open.

Bad:

- "here";
- "this link";
- "click here";
- "read more here".

Better:

- "See pricing details";
- "Open terms";
- "How it works";
- "Message us".

Keep links short: 2-6 words.

## Labels and placeholders

A label names the data. A placeholder prevents a mistake or shows an example.

Rules:

- a label is usually a noun: "Phone number", "Comment", "Date of birth";
- do not start labels with "Enter", "Type", "Write", "Start typing";
- do not repeat the label in the placeholder;
- do not hide required information only in a placeholder;
- if a field is optional, say "optional" or "if any".

Examples:

- "Middle name (optional)";
- "Documents (optional)";
- "Comment";
- "Phone number".

## Toggles

Toggle text must read equally well in the on and off states.

Rules:

- do not use negatives;
- do not write "Enable…";
- do not make the wording depend on the switch position;
- name the setting or the thing that gets turned on.

Bad:

- "Don't send notifications";
- "Enable auto-pay".

Better:

- "Notifications";
- "Auto-pay".

## Tooltips and hints

Tooltips and hints are read less often than the main text. Do not hide required or critical information there.

Use them only for extra explanation:

- what a term means;
- why a value is calculated this way;
- where the data comes from;
- what happens in a rare case.

If the user cannot finish the flow without the hint, the information belongs on the screen.

## Alerts

An alert is for important information: confirm an action, warn about a consequence, or report an error.

Structure:

- title: what happened or what to confirm;
- description: what it means;
- action: the specific next step.

For a critical action:

- title: "Delete project?";
- description: the consequence;
- primary button: "Delete";
- secondary button: "Cancel".

Alert buttons must differ in meaning.

## Legal text in UI

Change this text carefully. It must keep its meaning.

Base structure:

- "By clicking “Pay”, you agree to the terms."

If there are several agreements, be specific:

- "By clicking “Pay”, you agree to the data transfer terms."

If an edit may change the meaning, mark it as `needs legal review`.

## Empty states

An empty state explains why there is no content and what the user can do next.

Pattern:

- what is empty;
- why, if that is useful;
- how to create, connect, retry, or wait.

Avoid jokes, blaming the user, and empty optimism without an action.

## Loading

Loading text reduces uncertainty while the user waits.

Rules:

- describe the operation only if it matters;
- give a time estimate only when it is reliable;
- do not write a long message that flashes for a fraction of a second;
- for an action under a second, show no text.

## Code entry screen

Rules:

- say where the code was sent;
- do not reveal unnecessary security details;
- show resend as a separate control;
- if resend is not available immediately, show the wait time.
