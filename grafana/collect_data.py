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
logon = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

def parse_json(object, indent_value=None):
    return json.dumps(object, indent=indent_value, sort_keys=True)

def load_json(object):
    return json.loads(object.text)

def search_dashboard(header):
    # Search query for dashboard UID
    search_url = f"http://localhost:3000/api/search?query=Telegraf%test%XD"
    get_dashboard = load_json(requests.get(search_url, headers=header))
    # Retrieving dashboard uid value
    dashboard_uid = str([item["uid"] for item in get_dashboard]).strip('[|]|\'')
    return dashboard_uid

def get_dashboard_metadata(dashboard_uid, header):
    # Getting dashboard metadata by UID
    metadata_url = f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}"
    get_metadata = load_json(requests.get(metadata_url, headers=header))
    return dict(get_metadata)

def panel_templ(get_metadata):
    all_panels = {k: v for k, v in get_metadata['dashboard'].items() if k.startswith('panels')}
    return parse_json(all_panels, 2)

def main():
    uid = search_dashboard(logon)
    metadata = get_dashboard_metadata(uid, logon)
    print(panel_templ(metadata))

if __name__ == "__main__":
    main()