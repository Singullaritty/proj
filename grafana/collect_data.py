import requests
import json
import datetime
import sys
import ast
from datetime import timedelta
from loguru import logger

# # Logger init
logger.remove(0)
frmt =  "<green>{time}</green> | <blue>{level}</blue> | {message}"
logger.add(sys.stderr, level="INFO", format=frmt)

# Read API token from file
with open('/home/cloud_user/api_token', 'r') as api_file:
    api_token = api_file.read().strip('\n')

# Auth for HTTP API
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

def parse_json(object, indent_value=None):
    return json.dumps(object, indent=indent_value, sort_keys=True)

def search_dashboard(header):
    # Search query for dashboard UID
    search_url = f"http://localhost:3000/api/search?query=Telegraf%test%XD"
    search_query = requests.get(search_url, headers=header)
    load_query = json.loads(search_query.text)
    # Retrieving dashboard uid value
    dashboard_uid = str([item["uid"] for item in load_query]).strip('[|]|\'')
    return dashboard_uid

def get_dashboard_metadata(dashboard_uid):
    # Getting dashboard metadata by UID
    metadata_url = f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}"
    get_metadata = requests.get(metadata_url, headers=headers)
    get_result = json.loads(get_metadata.text)
    #get_meta_parsed = json.dumps(get_result, indent=3, sort_keys=True)
    return get_result

def panel_templ(get_result):
    all_panels = [item for item in get_result['dashboard']['panels'] if item["title"] != None]
    all_panels = parse_json(all_panels, 2)
    return all_panels

def main():
    uid = search_dashboard(headers)
    metadata = get_dashboard_metadata(uid)
    print(panel_templ(metadata))

if __name__ == "__main__":
    main()