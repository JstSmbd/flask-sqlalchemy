import requests

print(requests.get("http://127.0.0.1:5000/api/jobs").json())
print(requests.put("http://127.0.0.1:5000/api/jobs/3", json={
    "work_size": 250
}).json())
print(requests.put("http://127.0.0.1:5000/api/jobs/3", json={
    "work_sizes": 250
}).json())
print(requests.put("http://127.0.0.1:5000/api/jobs/99", json={
    "work_size": 250
}).json())
print(requests.put("http://127.0.0.1:5000/api/jobs/3", json={
    "work_size": "hello"
}).json())
print(requests.get("http://127.0.0.1:5000/api/jobs").json())