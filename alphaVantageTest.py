from alpha_vantage.timeseries import TimeSeries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ts = TimeSeries(key='NB9OQA12MMYF402C', output_format='pandas')
data, meta_data = ts.get_daily(symbol = 'GOOGL', outputsize = "full")

a = data["4. close"]
plt.plot(a)
plt.show()
