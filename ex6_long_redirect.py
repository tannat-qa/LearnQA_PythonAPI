import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

print("Count redirects: ", len(response.history))
print("Final URL: " + response.url)
