import pytest
import requests
from lib.base_case import BaseCase

class TestExamples(BaseCase):

    # Ex10: Тест на короткую фразу
    def test_check_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, f"Phrase '{phrase}' is longer than 15 symbols"

    # Ex11: Тест запроса на метод cookie
    def test_get_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(dict(response.cookies))

        cookie_test = self.get_cookie(response, "HomeWork")
        assert cookie_test == "hw_value", f"The value of cookie with name 'HomeWork' doesn't equal 'hw_value'"

    # Ex12: Тест запроса на метод header
    def test_get_headers(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)

        header_value = self.get_header(response, "x-secret-homework-header")
        assert header_value == "Some secret value", "oops"
