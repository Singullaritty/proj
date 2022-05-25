import requests
import json
import datetime
import sys
import ijson
from datetime import timedelta
from loguru import logger


def create_snap():

    null = None

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
    payload = json.dumps(get_result, indent=3, sort_keys=True)

    # Write to a file
    with open('sample.json', 'w') as outfile:
        outfile.write(payload)

def parse_json(json_filename):
    with open(json_filename, 'rb') as input_file:
        # load json
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            print(f'prefix={prefix}, event={event}, value={value}')

create_snap()
parse_json('sample.json')