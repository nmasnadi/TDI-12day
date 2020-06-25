# from alpha_vantage.timeseries import TimeSeries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

def read_data(tickerSymbol = "GOOG", plotting = False):

    alphaKey = 'NB9OQA12MMYF402C'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+\
    tickerSymbol + '&apikey=' + alphaKey

    r = requests.get(url)
    data_json = json.loads(r.text)
    data_pd = pd.DataFrame(data_json['Time Series (Daily)'], dtype = np.float64).T
    data_pd.index = pd.to_datetime(data_pd.index)
    if plotting:
        data_pd['4. close'].plot()
        plt.show()
    return data_pd

if __name__ == '__main__':
    read_data(plotting = True)
