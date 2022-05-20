import requests
import json
import datetime
from datetime import timedelta
import time
import logging

def create_snap():

    # Logger init
    formatter = logging.Formatter(f"%(asctime)s %(levelname)s %(message)s ")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    snap_logger = logging.getLogger()
    snap_logger.addHandler(handler)
    snap_logger.setLevel(logging.INFO)
    
    # Timestamp for snapshot
    timestr = time.strftime("%Y-%m-%d_%H:%M:%S")
    today = datetime.datetime.now()
    date_time = today.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
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
    
    # # Data source query
    # ds_db_query = "SELECT last(\"uptime_format\") AS \"value\" FROM \"system\" WHERE \"host\" =~ /learn-python$/ AND time >= now() - 1h and time <= now() GROUP BY time(30s)&epoch=ms"
    # ds_url = f"http://0ddf75494e1c.mylabserver.com:3000/api/datasources/proxy/1/query?db=test&q={ds_db_query}"
    # ds_query = requests.get(ds_url, headers=headers)
    # ds_load = json.loads(ds_query.text)
    # ds_parse = json.dumps(ds_load, indent=3, sort_keys=True)
    # # print(ds_query.status_code)
    # # print(ds_parse)



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
    snap_name = {"name": "Testing-snapshot-creation--" + timestr}
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
    logging.info(f"Snapshot for dashboard: \"{dashboard_name}\" has been created. It can be accessed via URL: {post_snap_url}")

create_snap()