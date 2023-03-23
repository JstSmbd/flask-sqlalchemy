import requests

# <---- start users ---->
print("start users:")
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
print("end users\n")
# <---- end users ---->

# <---- start jobs ---->
print("start jobs:")
print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs/1").json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs/99").json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs/hello").json())
print(requests.delete("http://127.0.0.1:5000/api/v2/jobs/99").json())
print(requests.delete("http://127.0.0.1:5000/api/v2/jobs/3").json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
print(requests.post("http://127.0.0.1:5000/api/v2/jobs", json={
    "team_leader": 2,
    "job": "Изучение Марса",
    "work_size": 50,
    "collaborators": "1, 2",
    "is_finished": False
}).json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
print(requests.put("http://127.0.0.1:5000/api/v2/jobs/3", json={
    "work_size": "la"
}).json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
print(requests.put("http://127.0.0.1:5000/api/v2/jobs/3", json={
    "is_finished": True
}).json())
print(requests.get("http://127.0.0.1:5000/api/v2/jobs").json())
print("end jobs")
# <---- end jobs ---->
