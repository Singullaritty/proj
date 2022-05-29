import requests
import json
import datetime
import sys
import ijson
from datetime import timedelta
from loguru import logger

# influxdb instance name
database_name = 'test'

# # Logger init
logger.remove(0)
frmt_info =  "<green>{time}</green> | <blue>{level}</blue> | {message}"
logger.add(sys.stderr, level="INFO", format=frmt_info)
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

# return parsed json object
def dumps_json(object, indent_value=None):
    return json.dumps(object, indent=indent_value, sort_keys=True)

# loads object as json 
def load_json(object):
    return json.loads(object.text)

# search for a dashboard and retrieve metadata from it
def get_dashboard(header):
    def search_dashboard():
        logger.debug("load_json")
        # Search query for dashboard UID
        search_url = f"http://localhost:3000/api/search?query=Telegraf%test%XD"
        get_dashb = load_json(requests.get(search_url, headers=header))
        # Retrieving dashboard uid value
        dashboard_uid = str([item["uid"] for item in get_dashb]).strip('[|]|\'')
        return dashboard_uid

    def get_dashboard_metadata():
        logger.debug("get_dashboard_metadata")
        # Getting dashboard metadata by UID
        metadata_url = f"http://localhost:3000/api/dashboards/uid/{search_dashboard()}"
        get_metadata = load_json(requests.get(metadata_url, headers=header))
        with open('file_to_parse.json', 'w+') as json_f:
            file_dumps = dumps_json(get_metadata, 2)
            json_f.write(file_dumps)
        return dict(get_metadata), json_f.name
    
    return get_dashboard_metadata(), search_dashboard()

# parse json object and return list of object
def parse_json(json_filename):
    logger.debug("parse_json")
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        data = []
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
           data.append(f'prefix={prefix}, event={event}, value={value}')
        nl_data = '\n'.join(data)
        input_file.write(nl_data)
        return str(nl_data).strip('[|]').replace('\'','')

# extracting data for snapshot template
def extract_json_data(json_filename, header):
    logger.debug("extract_json_data")
    # extract list of the queries from dashboard metadata
    def extract_all_data():
        logger.debug("extract_all_data")
        with open(json_filename, 'rb') as input_file:
            snap_data_list = []
            queries = ijson.items(input_file, 'dashboard.panels.item.targets.item.query')
            color_mode = ijson.items(input_file, 'dashboard.panels.item.fieldConfig.defaults.color.mode')
            thresholds_mode = ijson.items(input_file, 'dashboard.panels.item.fieldConfig.defaults.thresholds.mode')
            thresholds_data = ijson.items(input_file, 'dashboard.panels.item.fieldConfig.defaults.thresholds')


            # Update queries with needed syntax for API call
            # for query in queries:
            #     print(f"Query: \n {query} \n")

            for c_mode in color_mode:
                print(f"Color mode: \n {c_mode}")
            input_file.seek(0,0)

            for thrm in thresholds_mode:
                print(f"Threshold mode: \n {thrm}\n")
            input_file.seek(0,0)

            for thrd in thresholds_data:
                print(f"Thresholds data: \n {thrd}\n")
            input_file.seek(0,0)


            # snap_data_list = [w.replace('$timeFilter', 'time >= now() - 1h and time <= now()') for w in snap_data_list]
            # snap_data_list = [w.replace('$interval', '30s') for w in snap_data_list]
            # snap_data_list = [w.replace('$server', 'learn-python') for w in snap_data_list]
            # snap_data_list = [w.replace(',', '%2C') for w in snap_data_list]
            # snap_data_list = [w.replace(' ', '%20') for w in snap_data_list]
            # snap_data_list = [w.replace('"', '%22') for w in snap_data_list]
            # snap_data_list = [s + '&epoch=ms' for s in snap_data_list]

            # for c_mode in color_mode:
            #     snap_data_list.append(f"{c_mode}")
            # input_file.seek(0, 0)

            # for thrm in thresholds_mode:
            #     snap_data_list.append(f"{thrm}")
            # input_file.seek(0, 0)

            # for thrd in thresholds_data:
            #     snap_data_list.append(f"{thrd}")
            # input_file.seek(0, 0)

        return snap_data_list

    # extract data for snapshot template
    def extract_snap_templ_data():
        logger.debug("extract_snap_templ_data")
        pass
    
    # execute queries and return results as list
    # def get_ds_values():
    #     logger.debug("get_ds_values")
    #     response_q = []
    #     for query in extract_all_data():
    #         query_url = f"http://localhost:3000/api/datasources/proxy/1/query?db={database_name}&q={query}"
    #         query_result = load_json(requests.get(query_url, headers=header))
    #         for data in query_result.items():
    #             response_q.append(f'{data}')
    #     return response_q
    
    # extract values from executed queries
    def extract_ds_values():
        logger.debug("extract_ds_values")
        pass

    return extract_all_data()#, get_ds_values()

# main function
def main():
    #print(get_dashboard(logon)[0][0])
    uid = get_dashboard(logon)[1]
    metadata, file_to_parse = get_dashboard(logon)[0][0], get_dashboard(logon)[0][1]
    #queries_list, ds_values = 
    extract_json_data(file_to_parse, logon)#[0], extract_json_data(file_to_parse, logon)[1]
    #print(ds_values[1])

if __name__ == "__main__":
    main()