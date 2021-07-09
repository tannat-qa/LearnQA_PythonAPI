import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

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

    # Ex13: User Agent
    user_agent_params = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mobile', 'No', 'Android'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1', 'Mobile', 'Chrome', 'iOS'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Googlebot', 'Unknown', 'Unknown'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', 'Web', 'Chrome', 'No'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', 'Mobile', 'No', 'iPhone')
    ]

    @pytest.mark.parametrize('useragent, platform, browser, device', user_agent_params)
    def test_user_agent(self, useragent, platform, browser, device):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",headers={"User-Agent":useragent})

        Assertions.assert_json_value_by_name(
            response,
            "platform",
            platform,
            "Parameter 'platform' in response doesn't equal expected value"
        )

        Assertions.assert_json_value_by_name(
            response,
            "browser",
            browser,
            "Parameter 'browser' in response doesn't equal expected value"
        )

        Assertions.assert_json_value_by_name(
            response,
            "device",
            device,
            "Parameter 'device' in response doesn't equal expected value"
        )