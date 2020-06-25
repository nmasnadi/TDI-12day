import numpy as np
import pandas as pd
import requests
from bokeh.plotting import figure, show
import json

def read_data(tickerSymbol = "GOOG", data_size = 'short'):

    alphaKey = 'NB9OQA12MMYF402C'

    if data_size == 'short':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+\
        tickerSymbol + '&apikey=' + alphaKey
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
        tickerSymbol + '&outputsize=full&apikey=' + alphaKey

    r = requests.get(url)
    data_json = json.loads(r.text)
    data_pd = pd.DataFrame(data_json['Time Series (Daily)'], dtype = np.float64).T
    data_pd.index = pd.to_datetime(data_pd.index)
    return data_pd


def make_plot(x, y):
    p = figure(
       tools="pan,box_zoom,reset,save",
       plot_width=800, plot_height=350, x_axis_type="datetime"
    )
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "price"
    p.circle(x, y, color="darkgray", fill_alpha=0.5, size=5)
    p.line(x, y, color = 'black')
    return p

if __name__ == '__main__':
    a = read_data(data_size = 'full')
    x = np.array(a.index, dtype = np.datetime64)
    y = a['4. close'].to_numpy()
    p = make_plot(x, y)
    show(p)
