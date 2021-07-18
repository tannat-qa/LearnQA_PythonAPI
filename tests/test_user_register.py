from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest

class TestUserRegister(BaseCase):
    exclude_params = [
        ('email'),
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName')
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    #Ex15: Тесты на метод user
    # 1. Создание пользователя с некорректным email - без символа @
    def test_create_user_with_incorrect_email(self):
        email = 'testemail.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    #Ex15: Тесты на метод user
    # 2. Создание пользователя без указания одного из полей - с помощью дата-провайдера необходимо проверить,
    # что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_main_parameter(self, condition):
        data = self.prepare_registration_data()
        del data[condition]

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}"

    #Ex15: Тесты на метод user
    # 3. Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    #Ex15: Тесты на метод user
    # 4. Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'*256

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long"
