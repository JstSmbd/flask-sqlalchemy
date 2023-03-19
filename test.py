import requests
from json import dumps, dump, loads

# Тестирование ответа сервера
print(requests.get('http://localhost:5000/api/jobs').json())
print(requests.get('http://localhost:5000/api/jobs/1').json())
print(requests.get('http://localhost:5000/api/jobs/999').json())
print(requests.get('http://localhost:5000/api/jobs/hello').json())

# Тестирование POST-запроса
# id уже существует
print(requests.post('http://localhost:5000/api/jobs', json={
    "id": 1,  # <------
    "job": "Изучение Марса",
    "team_leader": 1,
    "work_size": 55,
    "collaborators": "1, 2",
    "is_finished": True
}).json())
# неправильный тип аргументов
print(requests.post('http://localhost:5000/api/jobs', json={
    "id": 4,
    "job": "Изучение Марса",
    "team_leader": "gee",  # <------
    "work_size": 55,
    "collaborators": "1, 2",
    "is_finished": True
}).json())
# отсутствие аргумента
print(requests.post('http://localhost:5000/api/jobs', json={
    "id": 4,
    "job": "Изучение Марса",
    "team_leader": 1,
    "work_size": 55,
    "collaborators": "1, 2",
    # "is_finished": True <-----
}).json())
print(requests.post('http://localhost:5000/api/jobs', json={
    "id": 4,
    "job": "Изучение Марса",
    "team_leader": 1,
    "work_size": 55,
    "collaborators": "1, 2",
    "is_finished": True
}).json())
print(requests.get('http://localhost:5000/api/jobs').json())