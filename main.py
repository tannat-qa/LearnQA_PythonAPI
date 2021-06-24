import requests

print("Hello from Tatyana Tsareva")

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
