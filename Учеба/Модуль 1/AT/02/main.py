def count_vowels(s: str) -> int:
    latin_vowels = "aeiouAEIOU"
    russian_vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    all_vowels = latin_vowels + russian_vowels
    return sum(1 for char in s if char in all_vowels)

import unittest

class TestCountVowels(unittest.TestCase):

    def test_only_latin_vowels(self):
        self.assertEqual(count_vowels("aeiouAEIOU"), 10)

    def test_only_russian_vowels(self):
        self.assertEqual(count_vowels("аеёиоуыэюяАЕЁИОУЫЭЮЯ"), 20)

    def test_mixed_latin_and_russian(self):
        self.assertEqual(count_vowels("Привет, Hello, друзья!"), 7)

    def test_no_vowels(self):
        self.assertEqual(count_vowels("bcdfghjklmnпрцчшщ"), 0)

    def test_empty_string(self):
        self.assertEqual(count_vowels(""), 0)

    def test_symbols_and_digits(self):
        self.assertEqual(count_vowels("123!@#$%^&*()"), 0)

    def test_alternating_case(self):
        self.assertEqual(count_vowels("AеIуOя"), 5)

    def test_with_whitespaces(self):
        self.assertEqual(count_vowels("     а о у     "), 3)

    def test_long_repetitive_string(self):
        long_string = "аоиеёэяуы"*1000 + "bcdfg"*1000
        self.assertEqual(count_vowels(long_string), 1000 * 10)

    def test_with_emojis_and_unicode(self):
        self.assertEqual(count_vowels("😊😂😍 оа 😃😜") , 2)

    def test_vowels_with_accents(self):
        self.assertEqual(count_vowels("áéíóú ÁÉÍÓÚ"), 0)  # не входят в список гласных

    def test_mixed_case_and_punctuation(self):
        self.assertEqual(count_vowels("ПрИвЕт!! How's it going?"), 7)

if __name__ == "__main__":
    unittest.main()
