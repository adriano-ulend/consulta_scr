import requests

url = "https://www.ulend.com.br/"
r = requests.get(url)
print(r.status_code)
