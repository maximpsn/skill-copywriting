#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


LINTER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ui_text_lint.py"
spec = importlib.util.spec_from_file_location("ui_text_lint", LINTER_PATH)
ui_text_lint = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(ui_text_lint)


def lint(text: str):
    return ui_text_lint.lint_item(ui_text_lint.items_from_text(text, None)[0])


class FinalPeriodTests(unittest.TestCase):
    def test_removes_period_from_one_sentence(self):
        issues = lint("Готово.")
        self.assertEqual(issues[0]["suggestion"], "Готово")

    def test_removes_only_final_period_from_two_sentences(self):
        issues = lint("Не загрузилось. Попробуйте снова.")
        self.assertEqual(issues[0]["suggestion"], "Не загрузилось. Попробуйте снова")

    def test_allows_final_period_from_three_sentences(self):
        self.assertEqual(lint("Первое. Второе. Третье."), [])

    def test_removes_period_before_closing_quote(self):
        issues = lint("«Готово.»")
        self.assertEqual(issues[0]["suggestion"], "«Готово»")


class OneLetterPrepositionTests(unittest.TestCase):
    def test_replaces_spaces_after_all_one_letter_prepositions(self):
        issues = lint("Оплатите в приложении к сроку с карты у кассира о тарифе")
        self.assertEqual(
            issues[0]["suggestion"],
            "Оплатите в приложении к сроку с карты у кассира о тарифе",
        )

    def test_accepts_existing_nonbreaking_space(self):
        self.assertEqual(lint("Оплатите в приложении"), [])


class SecurityTests(unittest.TestCase):
    def test_display_text_strips_terminal_control_chars(self):
        cleaned = ui_text_lint.extract_ui_strings.display_text("\x1b[31mКрасный\x1b[0m")
        self.assertNotIn("\x1b", cleaned)
        self.assertEqual(cleaned, "[31mКрасный[0m")

    def test_formatted_output_has_no_terminal_control_chars(self):
        issues = [
            {
                "file": "x",
                "line": 1,
                "key": "k",
                "component": "any",
                "value": "\x1b[31mred\x1b[0m",
                "rule_id": "test",
                "severity": "warning",
                "message": "test",
            }
        ]
        self.assertNotIn("\x1b", ui_text_lint.format_text(issues))

    def test_strip_control_keeps_cyrillic(self):
        self.assertEqual(ui_text_lint.extract_ui_strings.strip_control("\x1bГотово\x1b"), "Готово")


if __name__ == "__main__":
    unittest.main()
