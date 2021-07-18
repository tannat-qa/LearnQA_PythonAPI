from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import time
import allure

@allure.epic("Edit user test cases")
class TestUserEdit(BaseCase):
    @allure.description("This test edit just created user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Positive test")
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()

        with allure.step(f"Create new user with email: {register_data['email']} and getting his ID attribute value"):
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

        with allure.step("Authorization of the newly created user"):
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"

        with allure.step(f"Edit user data, attribute firstName={new_name}"):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )
            Assertions.assert_code_status(response3, 200)

        #GET
        with allure.step("User authorization"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step(f"Checking firstName attribute, expected value: {new_name}"):
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    #Ex17: Негативные тесты на PUT
    #1. Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.description("This test trying to change user data without authorization")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Negative test")
    def test_edit_user_without_auth(self):
        with allure.step("Edit user with ID=2"):
            data = self.prepare_registration_data()
            response = MyRequests.put("/user/2",data=data)

        with allure.step("Check that response code status is 400 and response text has error message"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Auth token not supplied"

    #Ex17: Негативные тесты на PUT
    #2. Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.description("This test trying to change user data with authorization data by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Negative test")
    def test_edit_user_with_auth_by_another_user(self):
        # Регистрируем нового пользователя (1), получаем его ID
        data = self.prepare_registration_data()
        data['username'] = "username1"


        with allure.step(f"User registration with username={data['username']}, getting new user ID attribute"):
            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            new_user_id1 = self.get_json_value(response1, "id")

        # Регистрируем второго пользователя, получаем его ID
        # Ждем 1 сек перед регистрацией
        time.sleep(1)

        data = self.prepare_registration_data()
        data['username'] = "username2"

        with allure.step(f"User registration with username={data['username']}"):
            response2 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

        # Авторизуемся вторым пользователем
        with allure.step(f"Authorizing a user named username={data['username']}"):
            response3 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        # Меняем данные пользователя 1 (неавторизованного)
        new_name = "new_user_name1"

        with allure.step("Changing the username attribute of an unauthorized user"):
            response4 = MyRequests.put(
                f"/user/{new_user_id1}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"username": new_name}
            )

        Assertions.assert_code_status(response4, 200)

        #Проверяем, что у пользователя 1 имя не изменилось
        with allure.step("Checking that the username attribute of an unauthorized user has not changed"):
            response5 = MyRequests.get(f"/user/{new_user_id1}")

            Assertions.assert_json_has_key(response5, "username")
            assert self.get_json_value(response5, "username") == "username1", "Attribute 'username' have been changed"

    #Ex17: Негативные тесты на PUT
    #3. Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    @allure.description("This test trying to change user email to incorrect email without symbol @")
    @allure.story("Negative test")
    def test_edit_user_incorrect_email(self):
        data = self.prepare_registration_data()

        with allure.step(f"User registration with username={data['username']}"):
            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        with allure.step("User authorization"):
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Меняем данные пользователя: email без @
        new_email = "email.com"

        with allure.step(f"Edit the email attribute user to invalid: {new_email}"):
            response3 = MyRequests.put(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )

        with allure.step("Check response code status is 400 and response text has error message"):
            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode("utf-8") == f"Invalid email format"

    #Ex17: Негативные тесты на PUT
    #4. Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    @allure.description("This test trying to change user firstName attribute to very short name")
    @allure.story("Negative test")
    def test_edit_user_short_firstName(self):
        # Регистрируем нового пользователя, получаем его ID
        data = self.prepare_registration_data()

        with allure.step(f"User registration with username={data['username']}"):
            response1 = MyRequests.post("/user", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        with allure.step("User authorization"):
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Меняем данные пользователя: firstName короткий (один символ)
        new_firstName = "a"

        with allure.step(f"Edit the firstName attribute user to invalid (very short): {new_firstName}"):
            response3 = MyRequests.put(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_firstName}
            )

        with allure.step("Check response code status is 400 and response text has error message"):
            Assertions.assert_code_status(response3, 400)
            Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName", "Expected text error message is not correct")
