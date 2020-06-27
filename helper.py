import numpy as np
import pandas as pd
import requests
from bokeh.plotting import figure, show
from bokeh.palettes import Spectral4
import json


def read_data(tickerSymbol, num_days = 30):
    # obtain data from AlphaVantage API
    alphaKey = 'NB9OQA12MMYF402C'
    if num_days < 100:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+\
        tickerSymbol + '&apikey=' + alphaKey
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
        tickerSymbol + '&outputsize=full&apikey=' + alphaKey

    r = requests.get(url)
    data_json = json.loads(r.text)
    if "Error Message" in data_json:
        error = data_json["Error Message"]
        url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' +\
        tickerSymbol + '&apikey=' + alphaKey
        r = requests.get(url)
        data_json = json.loads(r.text)
        try:
            ticker_list = [s['1. symbol'] for s in data_json['bestMatches']]
        except:
            ticker_list = []
        data_pd = None
    elif "Note" in data_json:
        error = data_json["Note"]
        data_pd = None
        ticker_list = []
    elif 'Time Series (Daily)' in data_json:
        error = ""
        ticker_list = []
        data_pd = pd.DataFrame(data_json['Time Series (Daily)'], dtype = np.float64).T
        data_pd.index = pd.to_datetime(data_pd.index)
        # slice the data for the inquired dates
        start =  np.datetime64('today') - np.timedelta64(num_days, 'D')
        data_pd = data_pd[data_pd.index >= start]
    else:
        error = "Something went wrong! Please try again"

    return data_pd, error, ticker_list


def make_plot(data, tickerSymbol, cols):

    if cols == []:
        cols = ["Close"]
    pd_cols = {'Open':'1. open', 'High':'2. high', 'Low':'3. low',
    'Close':'4. close'}
    p = figure(title = tickerSymbol.upper(),
       tools="pan,box_zoom,reset,save",
       plot_width=800, plot_height=450, x_axis_type="datetime"
    )
    p.title.align = "center"
    p.title.text_font_size = "25px"
    p.xaxis.axis_label = "date"
    p.xaxis.axis_label_text_font_size = "25px"
    p.yaxis.axis_label = "price"
    p.yaxis.axis_label_text_font_size = "25px"

    x = np.array(data.index, dtype = np.datetime64)

    for col, color in zip(cols, Spectral4):
        y = data[pd_cols[col]].to_numpy()
        p.circle(x, y, color="darkgray", fill_alpha=0.5, size=15, legend_label = col)
        p.line(x, y, color = color, line_width = 2, legend_label = col)

    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    return p

if __name__ == '__main__':
    a, error, tlist = read_data("GOOG", num_days = 30)
    p = make_plot(a, "GOOG", ["Close"])
    show(p)
