#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


LINTER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ui_text_lint.py"
spec = importlib.util.spec_from_file_location("ui_text_lint", LINTER_PATH)
ui_text_lint = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(ui_text_lint)


def lint(text, component=None):
    return ui_text_lint.lint_item(ui_text_lint.items_from_text(text, component)[0], component)


class FinalPeriodTests(unittest.TestCase):
    def test_removes_period_from_one_sentence(self):
        issues = lint("Done.")
        self.assertEqual(issues[0]["suggestion"], "Done")

    def test_removes_only_final_period_from_two_sentences(self):
        issues = lint("Couldn't load. Try again.")
        self.assertEqual(issues[0]["suggestion"], "Couldn't load. Try again")

    def test_allows_final_period_from_three_sentences(self):
        self.assertEqual(lint("First. Second. Third."), [])

    def test_removes_period_before_closing_quote(self):
        issues = lint("“Done.”")
        self.assertEqual(issues[0]["suggestion"], "“Done”")

    def test_ignores_abbreviations(self):
        issues = lint("Use e.g. this. Try again.")
        self.assertEqual(issues[0]["suggestion"], "Use e.g. this. Try again")

    def test_keeps_ellipsis(self):
        issues = lint("Loading...")
        self.assertEqual(issues[0]["suggestion"], "Loading…")


class SecurityTests(unittest.TestCase):
    def test_long_number_does_not_crash(self):
        self.assertEqual(lint("9" * 5000), [])

    def test_display_text_strips_terminal_control_chars(self):
        cleaned = ui_text_lint.extract_ui_strings.display_text("\x1b[31mred\x1b[0m")
        self.assertNotIn("\x1b", cleaned)
        self.assertEqual(cleaned, "[31mred[0m")

    def test_formatted_output_has_no_terminal_control_chars(self):
        issues = lint("\x1b[31mOops! Something went wrong.\x1b[0m")
        output = ui_text_lint.format_text(issues)
        self.assertNotIn("\x1b", output)

    def test_extractor_markdown_has_no_terminal_control_chars(self):
        item = {
            "file": "x.tsx",
            "line": 1,
            "key": "k",
            "component_guess": "unknown_ui_string",
            "value": "\x1b[31mred\x1b[0m",
        }
        output = ui_text_lint.extract_ui_strings.format_md([item])
        self.assertNotIn("\x1b", output)

    def test_display_text_truncates_long_values(self):
        cleaned = ui_text_lint.extract_ui_strings.display_text("a" * 1000)
        self.assertEqual(len(cleaned), 500)
        self.assertTrue(cleaned.endswith("…"))


class TypographyTests(unittest.TestCase):
    def test_percent_without_space(self):
        issues = lint("50 %")
        self.assertEqual(issues[0]["suggestion"], "50%")

    def test_currency_symbol_before_number(self):
        issues = lint("$ 10")
        self.assertEqual(issues[0]["suggestion"], "$10")

    def test_sentence_case_for_button(self):
        issues = lint("Save Changes", "button")
        self.assertEqual(issues[0]["suggestion"], "Save changes")

    def test_thousands_separator(self):
        issues = lint("10000 items")
        self.assertEqual(issues[0]["suggestion"], "10,000 items")


if __name__ == "__main__":
    unittest.main()
