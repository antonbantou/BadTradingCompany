import requests
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import time
#dont forget to download libs: requests, pandas, matplotlib

while True:
	url = "http://api.coincap.io/v2/assets/bitcoin/history?interval=m1"

	payload = {}
	headers = {}

	response = requests.request("GET", url, headers = headers, data = payload)

	json_data = json.loads(response.text.encode("utf8"))
	bitcoin_data = json_data["data"]

	#Turning the raw json data into a dataframe so matlab doesnt piss its pants
	bitcoindf = pd.DataFrame(bitcoin_data)


	#Get rid of time column, obsolete when we have date
	bitcoindf = pd.DataFrame(bitcoin_data, columns=['time', 'priceUsd'])

	#saving data to the csv
	bitcoindf.to_csv("bitcoin-usd.csv", index=False)
	time.sleep(60)
#Turning price from object to float
#bitcoindf['priceUsd'] = pd.to_numeric((bitcoindf['priceUsd']).fillna(0, downcast="infer"))
