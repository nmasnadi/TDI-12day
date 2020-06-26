from flask import Flask, render_template, request
import helper
from bokeh.embed import components
from bokeh.resources import CDN
import numpy as np
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        current_ticker = request.form['ticker_symbol']
        ticker_data, error, ticker_list = helper.read_data(current_ticker, num_days = 30)
        if len(error) == 0:
            p = helper.make_plot(ticker_data, current_ticker)
            script, div = components(p)
            return render_template("index2.html", script = script, div = div, \
            current_ticker = current_ticker, \
            resources = CDN.render())
        else:
            script = "Error!"
            # script = """
            # <h3>Error!</h3>
            # <br>
            # <h4>{}</h4>
            # <br>
            # <h3>Best matches:</h3>
            # <br>
            # <h4>{}</h4>
            # """.format(error, ", ".join(ticker_list))
            return render_template("index2.html", script = script, resources = CDN.render())
    else:
        return render_template("index2.html")#, resources = CDN.render())

if __name__ == '__main__':
    app.run(port=33507)
