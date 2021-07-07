import requests
import json
import time

# проверка формата ответа, должен быть JSON
def get_parsed_response(response):
    try:
        parsed_response_text = response.json()
        return(parsed_response_text)
    except JSONDecodeError:
        print("Response is not a JSON format")

# 1. Создание задачи
url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)

# 2. Получение токена и количества секунд из ответа
parsed_response_text = get_parsed_response(response)
token = parsed_response_text["token"]
seconds = parsed_response_text["seconds"]

# 3. Запрос с token ДО того, как задача готова, проверяем ответ
response = requests.get(url, params={"token":token})
parsed_response_text = get_parsed_response(response)
status = parsed_response_text["status"]

if status == 'Job is NOT ready':
    # 4. Ожидание нужного количества секунд
    time.sleep(seconds)

    # 5. Еще раз выполняем запрос с token после того, как задача готова, проверяем ответ
    response = requests.get(url, params={"token":token})
    parsed_response_text = get_parsed_response(response)

    # 6. Убеждаемся в правильности поля status и наличии поля result
    obj = json.loads(response.text)
    key = "status"
    if key in obj and obj[key] == 'Job is ready':
        key = "result"
        if key in obj:
            print("Status: " + obj["status"] + ", result: " + obj["result"])
        else:
            print(f"Ключа {key} в ответе JSON нет")
    else:
        print("Probably Job is NOT READY yet: " + response.text)

else:
    print("Probably JOB is ready: " + response.text)