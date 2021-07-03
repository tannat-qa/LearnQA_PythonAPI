import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

#1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response = requests.get(url)
print("1. " + response.text)

#2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response = requests.head(url)
print("2. " + str(response.status_code) + " " + response.text)

#3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response = requests.post(url, data={"method":"POST"})
print("3. " + response.text)

#4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок.
print("4.")
method_param = ["GET", "POST", "PUT", "DELETE"]
for i in method_param:
    print("method parameter = " + i)
    response = requests.get(url, params={"method":i})
    print("GET request type. Result: " + response.text)
    response = requests.post(url, data={"method":i})
    print("POST request type. Result: " + response.text)
    response = requests.put(url, data={"method":i})
    print("PUT request type. Result: " + response.text)
    response = requests.delete(url, data={"method":i})
    print("DELETE request type. Result: " + response.text)
    print()
