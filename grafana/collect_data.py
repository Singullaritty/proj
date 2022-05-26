import requests
import json
import datetime
import sys
import ijson
import io
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

def dumps_json(object, indent_value=None):
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
    with open('file_to_parse.json', 'r+') as json_f:
        file_dumps = dumps_json(get_metadata, 2)
        json_f.write(file_dumps)
    return dict(get_metadata), json_f.name

def parse_json(json_filename):
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        data = []
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
           data.append(f'prefix={prefix}, event={event}, value={value}')
        nl_data = '\n'.join(data)
        return str(nl_data).strip('[|]').replace('\'','')

def extract_ds_queries(json_filename):
    with open(json_filename, 'rb') as input_file:
        q_list = []
        queries = ijson.items(input_file, 'dashboard.panels.item.targets.item.query')
        for query in queries:
            q_list.append(f'{query}')
        return q_list


# def get_panels(get_metadata):
#     panels_dict = {k:v for k,v in get_metadata['dashboard'].items() if k == 'panels'}
#     return parse_json(panels_dict).replace('targets', 'snapshotData')
        
# def get_query(get_panels):
#     dict_q = json.loads(get_panels)
#     for key, value in dict_q.items():
#         for k, v in value.items():
#             print(v)
#     return type(dict_q)

def main():
    uid = search_dashboard(logon)
    metadata = get_dashboard_metadata(uid, logon)[0]
    file = get_dashboard_metadata(uid, logon)[1]
    print(extract_ds_queries(file))

if __name__ == "__main__":
    main()