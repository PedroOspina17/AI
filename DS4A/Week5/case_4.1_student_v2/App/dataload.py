import numpy as np
import datetime as dt
import pandas as pd
import json

df = pd.read_csv('Data/superstore.csv', parse_dates=['Order Date', 'Ship Date'])

with open('Data/us.json') as geo:
    geojson = json.loads(geo.read())

with open('Data/states.json') as f:
    states_dict = json.loads(f.read())

df['State_abbr'] = df['State'].map(states_dict)
df['Order_Month'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))