import requests
r = requests.get('http://localhost:5000/')
print(r.status_code)
print(r.text)
r = requests.get('http://localhost:5000/data_to')
print(r.status_code)
print(r.text)

