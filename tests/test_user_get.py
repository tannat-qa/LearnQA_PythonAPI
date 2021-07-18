from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Get user information test cases")
class TestUserGet(BaseCase):
    @allure.description("This test trying to get user data without authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Positive test")
    def test_get_user_details_not_auth(self):

        with allure.step("Retrieving user information with ID = 2 without authorization"):
            response = MyRequests.get("/user/2")

        with allure.step("Checking for the presence of the username attribute in the request response and the absence of email, firstName, lastName attributes"):
            Assertions.assert_json_has_key(response, "username")
            Assertions.assert_json_has_not_key(response, "email")
            Assertions.assert_json_has_not_key(response, "firstName")
            Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test trying to get user data with auth by same user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Positive test")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step(f"User authorization with email = {data['email']}"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Obtaining user authorization data"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        expected_fields = ['username', 'email', 'firstName', 'lastName']

        with allure.step(f"Verifying that attributes were obtained as a result of authorization: {expected_fields}"):
            Assertions.assert_json_has_keys(response2, expected_fields)

    #Ex16: Запрос данных другого пользователя
    @allure.description("This test trying to get user data with auth by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Positive test")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step(f"User authorization with email = {data['email']}"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step(f"Request to receive data of another user with ID = 1 according to user authorization data with email={data['email']}"):
            response2 = MyRequests.get(
                "/user/1",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Checking the attributes of the query result, only the username attribute is expected"):
            Assertions.assert_json_has_key(response2, "username")
            Assertions.assert_json_has_not_key(response2, "email")
            Assertions.assert_json_has_not_key(response2, "firstName")
            Assertions.assert_json_has_not_key(response2, "lastName")
