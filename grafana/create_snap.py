import requests
import json

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJrIjoialhtbTJ6SXlyOXdxNXBxRTNMY1VoWmQ4dEJXNEpxQzIiLCJuIjoic25hcF9jcmVhdGUiLCJpZCI6MX0="
}

# r = requests.get("http://localhost:3000/api/dashboards/uid/oyg53Ql7z", headers=headers)
# print(r)
# print(r.text)
# print(r.status_code)

with open('json_dashboard.json') as f:
    snapshot = json.load(f)

# payload = {"snapshot": snapshot}
url = "http://localhost:3000/api/snapshots"

p = requests.post(url, headers=headers, json=snapshot)

print(p)
print(p.status_code)
print(p.text)
