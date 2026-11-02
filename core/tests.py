from django.test import SimpleTestCase

from core.translit import latin1995_to_2026, restore_english_2026


class RestoreEnglishTests(SimpleTestCase):
    def test_restores_english_words(self):
        cases = {
            "Sçool Tests": "School Tests",
            "Tests for sçool çildren": "Tests for school children",
            "ÇANGE THE ALPHABET": "CHANGE THE ALPHABET",
            "Bubble Şooter - online game": "Bubble Shooter - online game",
            "<b>Şe</b> is a teaçer": "<b>She</b> is a teacher",
            "Şe’s here, şouldn’t": "She’s here, shouldn’t",
            "T-şirt": "T-shirt",
        }
        for src, expected in cases.items():
            self.assertEqual(restore_english_2026(src), expected, src)

    def test_keeps_uzbek_words(self):
        for text in ("Çap va öngga.", "Toşkent çoy tiş", "nasriy şe’r", "şe&#39;rlar", "şop-şup", "işlaş", "birç᧐k"):
            self.assertEqual(restore_english_2026(text), text, text)

    def test_forward_conversion_skips_english(self):
        self.assertEqual(
            latin1995_to_2026("Bubble Shooter for school children, she shouldn't; Toshkent choy, she'r"),
            "Bubble Shooter for school children, she shouldn't; Toşkent çoy, şe'r",
        )
