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
    timestr = time.strftime("%Y-%m-%d_%H:%M:%S")

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
    dashboard_name = str([item["title"] for item in load_query]).strip('[|]|\'')
    dashboard_uid = str([item["uid"] for item in load_query]).strip('[|]|\'')

    # Getting dashboard metadata by UID
    metadata_url = f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}"
    get_metadata = requests.get(metadata_url, headers=headers)
    get_result = json.loads(get_metadata.text)
    snap_name = {"name": "Testing-snapshot-creation--" + timestr}
    get_result.update(snap_name)
    payload = json.dumps(get_result, indent=4, sort_keys=True)

    # Creating snapshot
    snapshot_url = "http://localhost:3000/api/snapshots"
    post_data = requests.post(snapshot_url, headers=headers, data=payload)
    post_parsed = json.loads(post_data.text)
    post_snap_url = post_parsed["url"]
    logging.info(f"Snapshot for dashboard: \"{dashboard_name}\" has been created. It can be accessed via URL: {post_snap_url}")

create_snap()