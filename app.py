from flask import Flask, render_template, request, redirect
from helper import read_data, make_plot
# from bokeh.embed import json_item
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.resources import INLINE
import numpy as np
import json
from jinja2 import Template

app = Flask(__name__)

ticker_list = ["GOOG", "IBM", "MSFT"]

@app.route('/')
def index():
    current_ticker = request.args.get("ticker_symbol")
    print(current_ticker)
    if current_ticker == None:
        current_ticker = "GOOG"
    a = read_data(current_ticker, data_size = 'short')
    x = np.array(a.index, dtype = np.datetime64)
    y = a['4. close'].to_numpy()
    p = make_plot(x, y)
    script, div = components(p)
    return render_template("index2.html", script = script, div = div, \
    ticker_list = ticker_list, current_ticker = current_ticker, \
    resources = CDN.render())

# @app.route('/plot')
# def plot():
#     a = read_data(data_size = 'full')
#     x = np.array(a.index, dtype = np.datetime64)
#     y = a['4. close'].to_numpy()
#     p = make_plot(x, y)
#     script, div = components(p)
#     return render_template("index2.html", script = script, div = div)
    # return json.dumps(json_item(p, "myplot"))

# @app.route('/about')
# def about():
#     return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
