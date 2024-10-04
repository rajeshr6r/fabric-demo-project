import calendar
import datetime
import requests
import json
import time

# read the config.json to load all params and get started 
with open('config.json', 'r') as file:
    config = json.load(file)

# loop through the stocksymbols loaded from config
for stocksymbol in config.get('stocksymbols'):
    # loop through the years loaded from config
    for year in config.get('years'):
        # loop through the all months
        for month in range(1,13):
            lastdate = datetime.datetime(year,month,calendar.monthrange(year, month)[1]).strftime('%Y-%m-%d')
            firstdate = datetime.datetime(year,month,1).strftime('%Y-%m-%d')
            # construct the payload and request            
            full_url = f"{config.get('base_url')}/company-news?symbol={stocksymbol}&from={firstdate}&to={lastdate}&token={config.get('api_key')}"
            response = requests.get(full_url)
            filename = f"stock_{stocksymbol}_content_month_{month}_year_{year}.json"
            if response.status_code==200:
                data = {
                        "firstdate":firstdate,
                        "lastdate":lastdate,
                        "stocksymbol":stocksymbol,
                        "responsestatus":response.status_code,
                        "content":response.json()
                        }
                with open(filename, 'w') as f:
                    json.dump(data, f)
            else:
                print("failed")
                data = {
                        "firstdate":firstdate,
                        "lastdate":lastdate,
                        "responsestatus":response.status_code,
                        "content":response.json()
                        }
                with open(filename, 'w') as f:
                    json.dump(data, f)
            time.sleep(config.get('apicalltimedelayinseconds')) # sleep for 30 seconds to avoid overloading the api 
