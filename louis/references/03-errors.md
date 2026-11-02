# Errors

An error must help the user understand what happened and what to do next.

A good error answers three questions:

1. What happened.
2. How to fix it.
3. What happens next, if that is known.

Do not overload the error with technical causes the user cannot influence.

## Tone

Avoid:

- "Oops";
- "Sorry";
- "Unfortunately";
- "Something went wrong" without a concrete action;
- jokes.

Better:

- "Couldn't load. Try again";
- "No access";
- "No internet connection";
- "Page not found";
- "Temporarily unavailable. Try again later".

## Access error

Use when the user lacks permission or the object is unavailable.

Pattern:

- title: "No access";
- description: why, at the user's level;
- action: request access, switch account, or go back, if such a path exists.

## Load error

Use when part of the screen or the whole screen failed to load.

Pattern:

- title: "Couldn't load";
- action: "Try again";
- description only if the scale matters: "Couldn't load this month's transactions".

## Connection error

Use only when there is reason to think the problem is the internet connection.

Pattern:

- title: "No internet connection";
- action: "Check connection" or "Try again";
- do not blame the network when the cause is unknown.

## Temporary unavailability

Use when the problem is not on the user's side.

Pattern:

- title: "Temporarily unavailable";
- description: what exactly is unavailable and when to retry, if known;
- an alternative path only if it actually works.

## Generic error

Use when the cause is unknown or the action failed.

Pattern:

- title: "Couldn't complete that";
- description: what the user can do — retry, go back, or refresh the screen.

## Inline error

Use next to a field or a specific action.

Say exactly what to fix:

- "Enter 6 digits";
- "Date can't be in the past";
- "Fill in this field".

Do not write:

- "Invalid value";
- "Form error".

## 404 error

Pattern:

- title: "Page not found";
- description: "The link may be out of date, or the address may have a typo";
- action: "Go home" or "Go back".
