import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

# Initializations...
load_dotenv()
ticker_list = ['AMZN', 'TSLA', 'NVDA', 'JNJ', 'XOM', 'ARKK']

def download_news(ticker_symbol):

    #
    # Initialize the necessary params
    #
    polygon_url = 'https://api.polygon.io/v2/reference/news'
    pub_var='published_utc.gt'
    pub_mon_list=['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01']
    polygon_api_key=os.getenv('POLYGON_API_KEY')
    
    #
    # Max of 1000 results is only possible per query.
    # To work aroudn this, we request for 1000 results
    # for each month & discard the duplicates to build
    # a 5 month worth of news
    #
    data_dict = { }
    for pub_mon in pub_mon_list:
        params = dict({pub_var:pub_mon},
                      ticker=ticker_symbol,
                      limit='1000',
                      apiKey=polygon_api_key,
                      order='asc')
        
        resp = requests.get(url=polygon_url, params=params)
        data = resp.json()
    
        #
        # Create a dictionary with only the fields on our interest
        #
        for item in data['results']:
            try:
                data_dict[item['id']] = [item['published_utc'],
                                         item['title'],
                                         item['description']]
            except:
                continue
    
    #
    # Create data frame from the dict values
    #
    data_list = list(data_dict.values())
    data_df = pd.DataFrame(data_list, columns=['Date', 'Title', 'Description'])
    print(data_df.head())
    
    #
    # Save it as a .csv
    #
    data_csv_path = Path("Resources/news/" + ticker_symbol + ".csv")
    data_df.to_csv(data_csv_path, index=False)
    
#
# Walk throught the ticker list - download news & export it to csv
#
for ticker in ticker_list:
    print('Downloading ticker {}'.format(ticker))
    download_news(ticker)
    print('Wait for 90 secs...')
    time.sleep(90)

