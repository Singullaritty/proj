import requests
import json
import datetime
import sys
from datetime import timedelta
from loguru import logger


def create_snap():

    # # Logger init
    logger.remove(0)
    frmt =  "<green>{time}</green> | <blue>{level}</blue> | {message}"
    logger.add(sys.stderr, level="INFO", format=frmt)
    
    # Timestamp for snapshot
    today = datetime.datetime.now()
    snap_time = today.strftime("%H:%M:%S_%Y-%m-%d")
    one_hour_minus = today - timedelta(hours=1)

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
    time_value = {
            "from": f"{one_hour_minus}",
            "to": f"{today}",
            "raw": {
                "from": "now-1h",
                "to": "now"
                }
    }
    snap_name = {"name": "Testing-snapshot-creation--" + snap_time}
    get_result['dashboard']['time'] = time_value
    get_result.update(snap_name)
    payload = json.dumps(get_result, indent=3, sort_keys=True)

    # with open('pay_test.json', 'r') as json_file:
    #     file_read = json_file.read()
    #     data_loads = json.loads(file_read)
    #     print(json.dumps(data_loads, indent=3, sort_keys=True))

    # Creating snapshot
    snapshot_url = "http://localhost:3000/api/snapshots"
    post_data = requests.post(snapshot_url, headers=headers, data=payload)
    post_parsed = json.loads(post_data.text)
    post_snap_url = post_parsed["url"]
    logger.info(f"Snapshot for dashboard: \"{dashboard_name}\" has been created. It can be accessed via URL: {post_snap_url}", format=frmt, colorize=True)

create_snap()