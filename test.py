import requests

print(requests.get("http://127.0.0.1:5000/api/jobs").json())
print(requests.delete("http://127.0.0.1:5000/api/jobs/4").json())
print(requests.delete("http://127.0.0.1:5000/api/jobs/hello").json())
print(requests.delete("http://127.0.0.1:5000/api/jobs/999").json())
print(requests.get("http://127.0.0.1:5000/api/jobs").json())