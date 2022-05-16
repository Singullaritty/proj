import requests
import json
import time
import logging

def create_snap():

    formatter = logging.Formatter(f"%(asctime)s %(levelname)s %(message)s ")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    snap_logger = logging.getLogger()
    snap_logger.addHandler(handler)
    snap_logger.setLevel(logging.INFO)
    
    # Timestamp for snapshot
    timestr = time.strftime("%H:%M:%S_%Y/%m/%d")

    # Read API token from file
    with open('/home/cloud_user/api_token', 'r') as api_file:
        api_token = api_file.read().strip('\n')

    # Auth for HTTP API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # Search query for dashboard UID
    search_url = "http://localhost:3000/api/search?query=Telegraf%test%XD"
    search_query = requests.get(search_url, headers=headers)
    load_query = json.loads(search_query.text)
    # Retrieving dashboard uid value
    dashboard_uid = str([item["uid"] for item in load_query]).strip('[|]|\'')

    # Getting dashboard metadata by UID
    metadata_url = f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}"
    get_metadata = requests.get(metadata_url, headers=headers)
    get_result = json.loads(get_metadata.text)
    snap_name = {"name": "Testing-snapshot-creation--" + timestr}
    get_result.update(snap_name)
    payload = json.dumps(get_result, indent=4, sort_keys=True)

    # Creating snapshot
    url = "http://localhost:3000/api/snapshots"

    post_data = requests.post(url, headers=headers, data=payload)
    post_parsed = json.loads(post_data.text)
    # print(p)
    # print(p.status_code)
    post_snap_url = post_parsed["url"]

    logging.info(f"Snapshot has been created for dashboard UID: {dashboard_uid} Snapshot URL: {post_snap_url}")

create_snap()