import requests

print(requests.get("http://127.0.0.1:5000/api/v2/users").json())
print(requests.get("http://127.0.0.1:5000/api/v2/users/1").json())
print(requests.get("http://127.0.0.1:5000/api/v2/users/99").json())
print(requests.get("http://127.0.0.1:5000/api/v2/users/hello").json())
print(requests.delete("http://127.0.0.1:5000/api/v2/users/99").json())
print(requests.delete("http://127.0.0.1:5000/api/v2/users/2").json())
print(requests.get("http://127.0.0.1:5000/api/v2/users").json())
print(requests.post("http://127.0.0.1:5000/api/v2/users", json={
    "surname": "Мотвеева",
    "name": "Александра",
    "age": "25",
    "position": "Геолог",
    "speciality": "Геолог",
    "address": "module_59",
    "email": "mat@mars.com",
    "password": "marsYesterday"
}).json())
print(requests.post("http://127.0.0.1:5000/api/v2/users", json={
    "surname": "Мотвеева",
    "name": "Александра",
    "age": "25",
    "position": "Геолог",
    "speciality": "Геолог",
    "address": "module_59",
    "email": "mat@mars.com",
    "password": "marsYesterday"
}).json())
print(requests.post("http://127.0.0.1:5000/api/v2/users", json={
    "surname": "Мотвеева",
}).json())
print(requests.get("http://127.0.0.1:5000/api/v2/users").json())
print(requests.put("http://127.0.0.1:5000/api/v2/users/2", json={
    "surname": "Матвеева",
}).json())
print(requests.put("http://127.0.0.1:5000/api/v2/users/99", json={
    "surname": "Матвеева",
    "old_password": "marsYesterday"
}).json())
print(requests.put("http://127.0.0.1:5000/api/v2/users/2", json={
    "surname": "Матвеева",
    "old_password": "marsYesterday"
}).json())
print(requests.get("http://127.0.0.1:5000/api/v2/users").json())