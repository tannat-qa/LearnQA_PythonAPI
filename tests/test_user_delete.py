from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import time
import allure

@allure.epic("Delete user test cases")
class TestUserDelete(BaseCase):
    # Ex18: Тесты на DELETE
    # Попытка удалить пользователя по ID 2.
    @allure.description("This test trying to delete user with ID=2")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Negative test")
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Logs user with email {data['email']} into the system"):
            response1 = MyRequests.post("/user/login", data=data)

        with allure.step("Checking the value of the user_id attribute, expected value = 2"):
            Assertions.assert_json_value_by_name(response1, "user_id", 2, f"User with email vinkotov@example.com has id <> 2 and cannot be checked for delete")

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step(f"Deleting a user with ID = {user_id_from_auth_method}"):
            response2 = MyRequests.delete(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Checking response code status, response text"):
            Assertions.assert_code_status(response2,400)
            assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

        with allure.step("Checking that the user is not deleted: getting information about the user, checking the username attribute"):
            response3 = MyRequests.get(f"/user/{user_id_from_auth_method}")
            Assertions.assert_code_status(response3, 200)
            Assertions.assert_json_value_by_name(response3, "username", "Vitaliy", "User with id=2 was deleted or change username")

    # Ex18: Тесты на DELETE
    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    @allure.description("This test create user, delete it and check its data by ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Positive test")
    def test_get_user_data_after_delete_user(self):
        with allure.step("Create a user, get his ID"):
            data = self.prepare_registration_data()
            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

        with allure.step(f"Log in as a new user, obtain authorization data email: {data['email']}"):
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response2, "user_id")

        with allure.step(f"Deleting a user with ID={user_id_from_auth_method}"):
            response3 = MyRequests.delete(
                f"/user/{user_id_from_auth_method}",
                headers = {"x-csrf-token": token},
                cookies = {"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response3, 200)

        with allure.step(f"Getting user information by his ID = {user_id_from_auth_method}, checking response code status, response message"):
            response4 = MyRequests.get(f"/user/{user_id_from_auth_method}")
            Assertions.assert_code_status(response4, 404)
            assert response4.content.decode("utf-8") == f"User not found"

    # Ex18: Тесты на DELETE
    #Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test trying to delete user by another user auth data")
    @allure.story("Negative test")
    def test_delete_not_authorized_user(self):
        with allure.step("Create user 1, get his ID"):
            data = self.prepare_registration_data()
            data['username'] = 'username1'

            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id_1 = self.get_json_value(response1, "id")

        time.sleep(1)

        with allure.step("Create user 2, get his ID"):
            data = self.prepare_registration_data()
            data['username'] = 'username2'
            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

        with allure.step(f"User authorization 2 with email = {data['email']}, obtaining his authorization data"):
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # Удалить пользователя 1
        with allure.step(f"Delete user 1 with ID={user_id_1} with authorization data for user 2"):
            response3 = MyRequests.delete(
                f"/user/{user_id_1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        # Проверяем, что пользователь 1 не удален
        with allure.step("Checking that user 1 is not deleted"):
            response4= MyRequests.get(f"/user/{user_id_1}")
            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_value_by_name(response4, "username", "username1", "User with id=2 was deleted or change username")
