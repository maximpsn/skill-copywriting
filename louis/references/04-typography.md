# English typography

Use these rules for any English UI text. Pick one spelling variant (en-US or en-GB) per product and do not mix them.

## Capitalization

- Use sentence case for headings, buttons, labels, menu items, tabs, chips, table headers, and empty states.
- Capitalize the first word and proper nouns only.
- Do not capitalize every word. Title Case reads like a marketing banner and slows scanning.
- Do not use ALL CAPS for emphasis. It reads as shouting.
- Keep product and brand names in their official form: iPhone, GitHub, macOS.
- After a colon, lowercase the next word unless a full sentence follows.

## Periods

- One sentence: no final period.
- Two sentences: keep the period between them, drop the period at the end of the second: `Couldn't load your data. Try again`.
- Three or more sentences: a final period is allowed.
- Do not put a period after short headings, buttons, menu items, tabs, chips, labels, or short list items, regardless of length.
- Keep question marks, ellipses, and other meaningful punctuation.

## Dashes and hyphens

- Use an em dash (—) with a space on each side for a break in thought. A colon or a new sentence is often better.
- Use an en dash (–) for ranges, with no spaces: `25–27 September`, `9:30–10:15 am`, `pages 12–18`.
- Use a hyphen (-) for compound words: `sign-in`, `read-only`, `two-factor`.
- Never use a hyphen as a dash, and never put spaces around a hyphen.

## Other punctuation

- Use one space after a period or comma, never two.
- Do not put a space before `, . ; : ! ?`.
- Use the serial comma in lists of three or more: `name, email, and phone`.
- Use curly quotes: `“…”` and `‘…’`. Do not quote product names.
- Use a single ellipsis character `…`, not three periods.
- Do not use exclamation marks in ordinary UI.
- Use a colon to introduce a list, not a dash.
- Avoid `&` in running text; write `and`.
- Avoid `and/or`; write `or` and rephrase if the meaning needs it.
- Avoid `etc.`; finish the list or say "and more".
- Avoid `i.e.` and `e.g.` in UI; write "that is" and "for example".
- Avoid parentheses in UI when the phrase can be rewritten more simply.

## Numbers

- Spell out a number at the start of a sentence, or rewrite the sentence.
- Use digits for other numbers: `2 days`, `15%`, `3 items`.
- Thousands: comma, no space: `1,000`, `15,000`, `1,000,000`.
- Decimals: period: `10.25`, `10.10`.
- Ranges: en dash, no spaces: `10–20`, `15–20%`.
- Percent sign: no space: `50%`.
- Units: a space between the number and the unit: `5 GB`, `10 kg`, `3 min`. No space for `%` and `°`.
- Negative numbers: minus sign `−` (U+2212), no space: `−39,021`.
- Do not write cents in whole amounts: `$10`. If cents exist, use two digits: `$10.25`, `$10.10`.
- Ordinals: `1st`, `2nd`, `3rd`, `4th`.
- For a total count of items, use "X more": `5 more items`.
- Write a number as a word when the distinction matters: `one purchase` vs `your first purchase`.

## Currency

- Put the currency symbol before the number, with no space: `$1,000`, `€1,000`, `£1,000`.
- Use a currency code after the number, with a space, only when the symbol would be ambiguous: `1,000 USD`.
- Do not mix symbols and codes in the same view.
- Follow the project's locale for symbol choice, but keep one format per product.

## Dates and time

- Neutral UI default: `14 December 2023`.
- en-US: `December 14, 2023`. en-GB: `14 December 2023`.
- Never use an ambiguous all-numeric date in prose: `12/04/2023`.
- In inputs and masks, use the project's format and label it.
- Time: `9:30 am`, `9:30 pm`. Range: `9:30–10:15 am`.
- Durations: `2 min`, `1 hr 30 min`, `3 days`.
- Relative time is fine when it is accurate: `2 minutes ago`, `in 3 days`.
- Use `by` for a deadline, not `until`, when the action must happen before a point in time: `Pay by 12 April`.
- Add `inclusive` only when it matters.

## Words and terms

- Use plain words: `use`, not `utilize`; `help`, not `facilitate`; `before`, not `prior to`; `to`, not `in order to`.
- `log in` is the verb; `login` is the noun. `Sign in`, `Sign up`, `Sign out` are also fine if used consistently.
- `email`, not `e-mail`; `online`, not `on-line`; `website`, not `web site`.
- `OK` only if the product already uses it. Prefer a specific verb.
- No periods in abbreviations: `US`, `UK`, `API`, `PDF`.
- Lowercase `am` and `pm`, with no space before them.
- Do not use a slash to combine words: `and/or`, `he/she`.
- Do not use `&` for `and` in prose.

## Lists and links

- Use a numbered list when sequence matters. Use bullets otherwise.
- Start each item with a capital letter.
- Do not put punctuation at the end of short items. Use periods if the items are full sentences.
- Keep list items parallel in grammar and meaning.
- Link text must name the destination or the action, in 2-6 words.
- Do not use `click here`, `here`, `read more`, or `learn more` alone as link text.
- Do not put a period after a link.
- Include the preposition in the link if it belongs to the clickable phrase.

## What not to fix automatically

Do not change without context:

- legal text;
- markdown links and HTML fragments;
- ICU plural/select strings;
- code, IDs, URLs, filenames, environment variables, and placeholders;
- product names and user-generated values;
- capitalization inside code or brand names.
