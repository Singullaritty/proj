import requests
import json
import datetime
import sys
import ijson
import io
from datetime import timedelta
from loguru import logger


database_name = 'test'
# # Logger init
logger.remove(0)
frmt =  "<green>{time}</green> | <blue>{level}</blue> | {message}"
logger.add(sys.stderr, level="INFO", format=frmt)
logger.add(sys.stderr, level="DEBUG")

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
    logger.debug("load_json")
    # Search query for dashboard UID
    search_url = f"http://localhost:3000/api/search?query=Telegraf%test%XD"
    get_dashboard = load_json(requests.get(search_url, headers=header))
    # Retrieving dashboard uid value
    dashboard_uid = str([item["uid"] for item in get_dashboard]).strip('[|]|\'')
    return dashboard_uid

def get_dashboard_metadata(dashboard_uid, header):
    logger.debug("get_dashboard_metadata")
    # Getting dashboard metadata by UID
    metadata_url = f"http://localhost:3000/api/dashboards/uid/{dashboard_uid}"
    get_metadata = load_json(requests.get(metadata_url, headers=header))
    with open('file_to_parse.json', 'w+') as json_f:
        file_dumps = dumps_json(get_metadata, 2)
        json_f.write(file_dumps)
    return dict(get_metadata), json_f.name

def parse_json(json_filename):
    logger.debug("parse_json")
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        data = []
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
           data.append(f'prefix={prefix}, event={event}, value={value}')
        nl_data = '\n'.join(data)
        return str(nl_data).strip('[|]').replace('\'','')

def extract_data(json_filename, header):
    logger.debug("extract_ds_queries")
    # extract list of the queries from dashboard metadata
    def extract_queries_list():
        logger.debug("extract_queries_list")
        with open(json_filename, 'rb') as input_file:
            q_list = []
            queries = ijson.items(input_file, 'dashboard.panels.item.targets.item.query')
            for query in queries:
                q_list.append(f'{query}')
            q_list = [w.replace('$timeFilter', 'time >= now() - 1h and time <= now()') for w in q_list]
            q_list = [w.replace('$interval', '30s') for w in q_list]
            q_list = [w.replace('$server', 'learn-python') for w in q_list]
            q_list = [w.replace(',', '%2C') for w in q_list]
            q_list = [w.replace(' ', '%20') for w in q_list]
            q_list = [w.replace('"', '%22') for w in q_list]
            q_list = [s + '&epoch=ms' for s in q_list]
            return q_list
    # extract data for snapshot template
    def extract_snap_templ_data():
        logger.debug("extract_snap_templ_data")
        pass

    def get_ds_values():
        logger.debug("get_ds_values")
        response_q = []
        for query in extract_queries_list():
            query_url = f"http://localhost:3000/api/datasources/proxy/1/query?db={database_name}&q={query}"
            query_result = load_json(requests.get(query_url, headers=header))
            for data in query_result.items():
                response_q.append(f'{data}')
        return response_q
    
    # extract values from executed queries
    def extract_ds_values():
        logger.debug("extract_ds_values")
        pass

    return extract_queries_list(), get_ds_values()



def main():
    uid = search_dashboard(logon)
    metadata = get_dashboard_metadata(uid, logon)[0]
    file = get_dashboard_metadata(uid, logon)[1]
    queries_list, ds_values = extract_data(file, logon)[0], extract_data(file, logon)[1]
    print(ds_values)

if __name__ == "__main__":
    main()