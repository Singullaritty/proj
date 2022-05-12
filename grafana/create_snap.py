import requests
import json
import time

# Timestamp for snapshot
timestr = time.strftime("%H:%M:%S_%Y/%m/%d")

# Auth for HTTP API
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJrIjoialhtbTJ6SXlyOXdxNXBxRTNMY1VoWmQ4dEJXNEpxQzIiLCJuIjoic25hcF9jcmVhdGUiLCJpZCI6MX0="
}

# Search for dashboard UID
search_query = requests.get("http://localhost:3000/api/search?query=Telegraf%test%XD", headers=headers)
load_query = json.loads(search_query.text)
# Retrieving dashboard uid value
for i in load_query:
    dashboard_uid = i["uid"]


# Getting dashboard metadata by UID
r_metadata = requests.get(f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}", headers=headers)
r_result = json.loads(r_metadata.text)
snap_name = {"name": "Testing-snapshot-creation--" + timestr}
r_result.update(snap_name)
payload = json.dumps(r_result, indent=4, sort_keys=True)


# Writing data to a json file
# with open('test_data.json', 'w') as f:
#     data = json.dumps(data, indent=4, sort_keys=True)
#     f.write(data)

# Update json file with snap-name
# snapshot_name = {"name": "Testing-snapshot-creation"}

# Creating a snapshot from file

# with open('test_data.json', 'r') as json_file:
#     payload = json.load(json_file)

# Creating snapshot
url = "http://localhost:3000/api/snapshots"

p = requests.post(url, headers=headers, data=payload)
parsed = json.loads(p.text)
# print(p)
# print(p.status_code)
print(json.dumps(parsed, indent=4, sort_keys=True))
