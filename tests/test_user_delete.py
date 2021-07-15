from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import time

#DELETE-метод https://playground.learnqa.ru/api/user/{id}
class TestUserDelete(BaseCase):
    # Ex18: Тесты на DELETE
    # Попытка удалить пользователя по ID 2.
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        Assertions.assert_json_value_by_name(response1, "user_id", 2, f"User with email vinkotov@example.com has id <> 2 and cannot be checked for delete")

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")


        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2,400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

        # Проверяем, что пользователь не удален
        response3 = MyRequests.get(f"/user/{user_id_from_auth_method}")
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(response3, "username", "Vitaliy", "User with id=2 was deleted or change username")

    # Ex18: Тесты на DELETE
    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_get_user_data_after_delete_user(self):
        # Создание пользователя
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Удаление пользователя
        response3 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # Получение данных пользователя
        response4 = MyRequests.get(f"/user/{user_id_from_auth_method}")
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found"

    # Ex18: Тесты на DELETE
    #Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_not_authorized_user(self):
        # Создаем пользователя 1
        data = self.prepare_registration_data()
        data['username'] = 'username1'
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id_1 = self.get_json_value(response1, "id")

        # Создаем пользователя 2
        time.sleep(1)
        data = self.prepare_registration_data()
        data['username'] = 'username2'
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id_2 = self.get_json_value(response1, "id")

        # Авторизация пользователя 2
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удалить пользователя 1
        response3 = MyRequests.delete(
            f"/user/{user_id_1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверяем, что пользователь 1 не удален
        response4= MyRequests.get(f"/user/{user_id_1}")
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "username", "username1", "User with id=2 was deleted or change username")
