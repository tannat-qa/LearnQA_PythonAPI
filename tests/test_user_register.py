from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import allure

@allure.epic("Register user test cases")
class TestUserRegister(BaseCase):
    exclude_params = [
        ('email'),
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName')
    ]

    @allure.description("This test create user successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Positive test")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        with allure.step(f"Create user with email={data['email']}"):
            response = MyRequests.post("/user", data=data)

        with allure.step("Check that response code status is 200 and has attribute 'id'"):
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.description("This test trying to create user with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Negative test")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Create user with existing email={data['email']}"):
            response = MyRequests.post("/user", data=data)

        with allure.step("Check that response code status is 400 and has error message"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    #Ex15: Тесты на метод user
    # 1. Создание пользователя с некорректным email - без символа @
    @allure.description("This test create user with incorrect email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Negative test")
    def test_create_user_with_incorrect_email(self):
        email = 'testemail.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Create user with incorrect email={data['email']}"):
            response = MyRequests.post("/user", data=data)

        with allure.step("Check that response code status is 400 and has error message"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Invalid email format"

    #Ex15: Тесты на метод user
    # 2. Создание пользователя без указания одного из полей - с помощью дата-провайдера необходимо проверить,
    # что отсутствие любого параметра не дает зарегистрировать пользователя
    @allure.description("This test create user without sending one of mandatory parameter")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Negative test")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_main_parameter(self, condition):
        data = self.prepare_registration_data()
        del data[condition]

        with allure.step(f"Create user without one of mandatory attribute: {condition}"):
            response = MyRequests.post("/user", data=data)

        with allure.step(f"Check that response code status is 400 and has error message with missed attribute {condition}"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: {condition}"

    #Ex15: Тесты на метод user
    # 3. Создание пользователя с очень коротким именем в один символ
    @allure.description("This test create user with short name with one symbol")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Negative test")
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'

        with allure.step(f"Create user with short name: {data['username']}"):
            response = MyRequests.post("/user", data=data)

        with allure.step("Check that response code status is 400 and has error message"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    #Ex15: Тесты на метод user
    # 4. Создание пользователя с очень длинным именем - длиннее 250 символов
    @allure.description("This test create user with very long name (longer than 255 symbols)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Negative test")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'*256

        with allure.step(f"Create user with long name (more than 255 symbols): {data['username']}"):
            response = MyRequests.post("/user", data=data)

        with allure.step("Check that response code status is 400 and has error message"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of 'username' field is too long"
