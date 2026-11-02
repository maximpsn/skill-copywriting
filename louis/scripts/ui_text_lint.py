#!/usr/bin/env python3
"""Heuristic UX writing lint for English interface microcopy."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACT_PATH = SCRIPT_DIR / "extract_ui_strings.py"
spec = importlib.util.spec_from_file_location("extract_ui_strings", EXTRACT_PATH)
extract_ui_strings = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(extract_ui_strings)

Issue = Dict[str, Any]

ABBREVIATIONS = {
    "e.g.",
    "i.e.",
    "etc.",
    "vs.",
    "mr.",
    "ms.",
    "mrs.",
    "dr.",
    "st.",
    "inc.",
    "ltd.",
    "jr.",
    "sr.",
    "approx.",
    "no.",
    "fig.",
    "u.s.",
    "u.k.",
    "a.m.",
    "p.m.",
}

SMALL_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "but",
    "by",
    "for",
    "from",
    "in",
    "into",
    "nor",
    "of",
    "on",
    "onto",
    "or",
    "over",
    "per",
    "the",
    "to",
    "up",
    "via",
    "vs",
    "with",
    "without",
    "yet",
}


def issue(item: Dict[str, Any], rule_id: str, severity: str, message: str, suggestion: Optional[str] = None) -> Issue:
    result: Issue = {
        "file": item.get("file", "<text>"),
        "line": item.get("line", 1),
        "key": item.get("key", ""),
        "component": item.get("component_guess", "unknown_ui_string"),
        "value": item["value"],
        "rule_id": rule_id,
        "severity": severity,
        "message": message,
    }
    if suggestion:
        result["suggestion"] = suggestion
    return result


def strip_final_period(text: str) -> str:
    return re.sub(r"\.(?=([”’\"')\]]*)$)", "", text.strip())


def sentence_count(text: str) -> int:
    """Estimate sentence count without treating abbreviation periods as boundaries."""
    stripped = text.strip()
    if not stripped:
        return 0
    parts = re.split(r'(?<=[.!?…])["\'”’)\]]*\s+', stripped)
    count = 1
    for part in parts[:-1]:
        tokens = part.strip().split()
        last = tokens[-1].lower() if tokens else ""
        if last in ABBREVIATIONS:
            continue
        count += 1
    return count


def to_sentence_case(text: str) -> str:
    words = text.split()
    result: List[str] = []
    for index, word in enumerate(words):
        match = re.search(r"[A-Za-z][A-Za-z'’-]*", word)
        if index == 0 or not match:
            result.append(word)
            continue
        core = match.group(0)
        if core.isupper() or any(character.isupper() for character in core[1:]):
            result.append(word)
            continue
        start, end = match.span()
        result.append(word[:start] + core[0].lower() + core[1:] + word[end:])
    return " ".join(result)


def looks_title_case(text: str) -> bool:
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", text)
    if len(words) < 2:
        return False
    candidates = [word for word in words if not word.isupper()]
    content = [word for word in candidates if word.lower() not in SMALL_WORDS]
    if len(content) < 2:
        return False
    capitalized = [word for word in content if word[0].isupper()]
    return len(capitalized) >= max(2, round(len(content) * 0.75))


def normalize_button(text: str) -> Optional[str]:
    stripped = strip_final_period(text)
    replacements = {
        "I want to delete": "Delete",
        "I want to save": "Save",
        "Saving": "Save",
        "Deleting": "Delete",
        "Sending": "Send",
        "Loading": "Load",
        "I understand": "Got it",
        "OK": "Got it",
        "Ok": "Got it",
    }
    return replacements.get(stripped)


def lint_item(item: Dict[str, Any], forced_component: Optional[str] = None) -> List[Issue]:
    value = item["value"].strip()
    lower = value.lower()
    component = forced_component or item.get("component_guess", "unknown_ui_string")
    scoped = {**item, "component_guess": component}
    issues: List[Issue] = []

    if re.search(r"\b(oops|sorry|unfortunately|apolog(?:y|ies|ize))\b", lower):
        issues.append(
            issue(
                scoped,
                "ui.tone.no_apologies",
                "warning",
                "Ordinary UI errors read better without an apology or an emotional opener.",
            )
        )

    if re.search(r"\b(awesome|amazing|great news|congrats|congratulations|yay|woohoo)\b", lower):
        issues.append(issue(scoped, "ui.tone.no_hype", "suggestion", "Check whether the tone is too emotional for product UI."))

    if re.search(r"\b(something went wrong|an error occurred|error occurred)\b", lower):
        issues.append(
            issue(
                scoped,
                "ui.error.generic",
                "warning",
                "A generic error should say what failed and what the user can do.",
            )
        )

    if "!" in value:
        issues.append(issue(scoped, "ui.typography.no_exclamation", "suggestion", "An exclamation mark is rarely needed in ordinary UI."))

    button_suggestion = normalize_button(value)
    if component == "button":
        if re.match(r"^(i want to|i'd like to|i would like to|let me)\b", lower):
            issues.append(issue(scoped, "ui.button.no_i_want", "warning", "A button should usually be the user's direct action.", button_suggestion))
        if lower.rstrip(".") in {"saving", "deleting", "sending", "loading", "submitting", "processing"}:
            issues.append(
                issue(scoped, "ui.button.no_system_present_tense", "warning", "Do not use the system's present tense in a button.", button_suggestion)
            )
        if lower.rstrip(".") in {"ok", "okay"}:
            issues.append(issue(scoped, "ui.button.no_ok", "suggestion", "\"Got it\" or a specific action is usually clearer.", button_suggestion))
        if len(value) > 32:
            issues.append(issue(scoped, "ui.button.too_long", "suggestion", "Check the button length for narrow screens."))

    if component in {"label", "placeholder", "unknown_ui_string"}:
        match = re.match(r"^(enter|type|write|start typing)\s+(.+)$", value, re.IGNORECASE)
        if match:
            suggestion = match.group(2).strip()
            suggestion = suggestion[0].upper() + suggestion[1:] if suggestion else None
            issues.append(
                issue(scoped, "ui.form.no_enter_type", "warning", "A label or placeholder usually names the data.", suggestion)
            )

    if component in {"link", "unknown_ui_string"} and re.search(r"\b(click here|read more|learn more|this link)\b", lower):
        issues.append(issue(scoped, "ui.link.meaningful_text", "warning", "A link should name the destination or the action."))

    if re.search(r"\b(need to|needs to|must|should|have to|has to|required to)\b", lower):
        issues.append(issue(scoped, "ui.language.modal_verbs", "suggestion", "Check whether the modal verb is needed or a direct action is better."))

    if re.search(r"\bplease\b", lower):
        issues.append(issue(scoped, "ui.language.please", "suggestion", "Use \"please\" sparingly; an action is often clearer."))

    if re.search(r"\d+\s+%", value):
        issues.append(
            issue(scoped, "ui.typography.percent_no_space", "warning", "Do not put a space before the percent sign.", re.sub(r"(\d+)\s+%", r"\1%", value))
        )

    currency_suggestion = value
    currency_changed = False
    if re.search(r"\$\s+\d", currency_suggestion):
        currency_suggestion = re.sub(r"\$\s+(\d)", r"$\1", currency_suggestion)
        currency_changed = True
    if re.search(r"(\d[\d,]*)\s*\$", currency_suggestion):
        currency_suggestion = re.sub(r"(\d[\d,]*)\s*\$", r"$\1", currency_suggestion)
        currency_changed = True
    if currency_changed:
        issues.append(
            issue(
                scoped,
                "ui.typography.currency_symbol_before",
                "warning",
                "Put the currency symbol before the number, with no space.",
                currency_suggestion,
            )
        )

    if not re.search(r"[+#vV]\s*\d", value) and re.search(r"\b\d{4,}\b", value):
        def add_commas(match: re.Match[str]) -> str:
            number = match.group(0)
            if len(number) > 18:
                return number
            if len(number) == 4 and 1900 <= int(number) <= 2099:
                return number
            return f"{int(number):,}"

        thousands_suggestion = re.sub(r"\b\d{4,}\b", add_commas, value)
        if thousands_suggestion != value:
            issues.append(
                issue(
                    scoped,
                    "ui.typography.thousands_separator",
                    "suggestion",
                    "Separate thousands with commas in English UI numbers.",
                    thousands_suggestion,
                )
            )

    trimmed = value.rstrip("»”’\"')] ")
    if trimmed.endswith(".") and not trimmed.endswith("...") and sentence_count(value) <= 2:
        issues.append(
            issue(
                scoped,
                "text.typography.no_final_period_in_one_or_two_sentences",
                "warning",
                "Do not put a final period on one- or two-sentence text.",
                strip_final_period(value),
            )
        )

    if component in {"heading", "button", "label", "link", "unknown_ui_string"} and sentence_count(value) == 1 and looks_title_case(value):
        issues.append(
            issue(
                scoped,
                "ui.typography.sentence_case",
                "suggestion",
                "Use sentence case for headings, buttons, and labels.",
                to_sentence_case(value),
            )
        )

    if "..." in value:
        issues.append(
            issue(scoped, "ui.typography.ellipsis_character", "suggestion", "Use a single ellipsis character, not three periods.", value.replace("...", "…"))
        )

    if "  " in value:
        issues.append(
            issue(scoped, "ui.typography.double_space", "suggestion", "Use one space between words and after punctuation.", re.sub(r" {2,}", " ", value))
        )

    if re.search(r"\s+[,.;:!?]", value):
        issues.append(
            issue(
                scoped,
                "ui.typography.space_before_punctuation",
                "suggestion",
                "Do not put a space before punctuation.",
                re.sub(r"\s+([,.;:!?])", r"\1", value),
            )
        )

    if re.search(r"\band/or\b", lower):
        issues.append(
            issue(
                scoped,
                "ui.language.and_or",
                "suggestion",
                "Avoid \"and/or\"; write \"or\" and rephrase if needed.",
                re.sub(r"\band/or\b", "or", value, flags=re.IGNORECASE),
            )
        )

    if re.search(r"\b(utilize|utilise|leverage)\b", lower):
        issues.append(issue(scoped, "ui.language.plain_words", "suggestion", "Use a plainer word, usually \"use\"."))

    if re.search(r"\bin order to\b", lower):
        issues.append(
            issue(
                scoped,
                "ui.language.in_order_to",
                "suggestion",
                "Replace \"in order to\" with \"to\".",
                re.sub(r"\bin order to\b", "to", value, flags=re.IGNORECASE),
            )
        )

    if re.search(r"https?://\S+", value):
        issues.append(issue(scoped, "ui.link.raw_url", "warning", "A raw URL in UI is usually better as meaningful link text."))

    if re.search(r'"[^"\n]{2,}"', value):
        issues.append(
            issue(
                scoped,
                "ui.typography.curly_quotes",
                "suggestion",
                "Use curly quotes in UI text.",
                re.sub(r'"([^"\n]{2,})"', r"“\1”", value),
            )
        )

    if component == "heading" and len(value) > 70:
        issues.append(issue(scoped, "ui.heading.too_long", "suggestion", "Check whether the heading is too long for UI."))

    return issues


def items_from_text(text: str, component: Optional[str]) -> List[Dict[str, Any]]:
    return [
        {
            "file": "<text>",
            "line": 1,
            "key": "input",
            "value": text,
            "component_guess": component or "unknown_ui_string",
            "source_type": "text",
        }
    ]


def collect_items(paths: Iterable[Path]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for file_path in extract_ui_strings.iter_files(paths, include=None):
        items.extend(extract_ui_strings.extract_file(file_path))
    return items


def format_text(issues: List[Issue]) -> str:
    lines: List[str] = []
    for item in issues:
        location = f"{item['file']}:{item['line']} {item['key']}".strip()
        lines.append(f"{extract_ui_strings.display_text(location)} [{item['severity']}] {item['rule_id']}")
        lines.append(f'"{extract_ui_strings.display_text(item["value"])}"')
        if "suggestion" in item:
            lines.append(f'→ suggested: "{extract_ui_strings.display_text(item["suggestion"])}"')
        lines.append(f"Reason: {item['message']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--text", help="Lint a single string instead of files")
    parser.add_argument("--component", help="Force component type, for example button/error/label")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    if args.text is not None:
        items = items_from_text(args.text, args.component)
    elif args.paths:
        items = collect_items(args.paths)
    else:
        parser.error("Provide paths or --text")

    issues: List[Issue] = []
    for item in items:
        if args.component and item.get("component_guess") not in {args.component, "unknown_ui_string"}:
            continue
        issues.extend(lint_item(item, args.component))

    if args.format == "json":
        print(json.dumps(issues, ensure_ascii=True, indent=2))
    else:
        output = format_text(issues)
        if output:
            print(output)
    return 1 if any(item["severity"] in {"error", "warning"} for item in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
