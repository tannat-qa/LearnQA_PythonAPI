import pytest

class TestExamples:

    # Ex10: Тест на короткую фразу
    def test_check_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, f"Phrase '{phrase}' is longer than 15 symbols"
