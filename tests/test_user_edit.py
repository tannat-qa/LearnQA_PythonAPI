from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import time

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data = register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    #Ex17: Негативные тесты на PUT
    #1. Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_without_auth(self):
        data = self.prepare_registration_data()
        response = MyRequests.put("/user/2",data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Auth token not supplied"

    #Ex17: Негативные тесты на PUT
    #2. Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_with_auth_by_another_user(self):
        # Регистрируем нового пользователя (1), получаем его ID
        data = self.prepare_registration_data()
        data['username'] = "username1"
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        new_user_id1 = self.get_json_value(response1, "id")

        # Регистрируем второго пользователя, получаем его ID
        # Ждем 1 сек перед регистрацией
        time.sleep(1)
        data = self.prepare_registration_data()
        data['username2'] = "username2"
        response2 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        new_user_id2 = self.get_json_value(response2, "id")

        # Авторизуемся вторым пользователем
        response3 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Меняем данные пользователя 1 (неавторизованного)
        new_name = "new_user_name1"
        response4 = MyRequests.put(
            f"/user/{new_user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"username": new_name}
        )

        Assertions.assert_code_status(response4, 200)

        #Проверяем, что у пользователя 1 имя не изменилось
        response5 = MyRequests.get(f"/user/{new_user_id1}")

        Assertions.assert_json_has_key(response5, "username")
        assert self.get_json_value(response5, "username") == "username1"

    #Ex17: Негативные тесты на PUT
    #3. Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_incorrect_email(self):
        # Регистрируем нового пользователя, получаем его ID
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Меняем данные пользователя: email без @
        new_email = "email.com"
        response3 = MyRequests.put(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format"

    #Ex17: Негативные тесты на PUT
    #4. Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_short_firstName(self):
        # Регистрируем нового пользователя, получаем его ID
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Меняем данные пользователя: firstName короткий (один символ)
        new_firstName = "a"
        response3 = MyRequests.put(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstName}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName", "Expected text error message is not correct")
