import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd

#Recall app
from app import app




#############################
# Load map data
#############################
df = pd.read_csv('Data\\superstore.csv', parse_dates=['Order Date', 'Ship Date'])

with open('Data\\us.json') as geo:
    geojson = json.loads(geo.read())

with open('Data\\states.json') as f:
    states_dict = json.loads(f.read())

df['State_abbr'] = df['State'].map(states_dict)


#Create the map:
dff=df.groupby('State_abbr').sum().reset_index()
Map_Fig=px.choropleth_mapbox(dff,                         
        locations='State_abbr',                   
        color='Sales',                            
        geojson=geojson,                          
        zoom=3,                                   
        mapbox_style="carto-positron",            
        center={"lat": 37.0902, "lon": -95.7129}, 
        color_continuous_scale="Viridis",         
        opacity=0.5,                              
        )
Map_Fig.update_layout(title='US map',paper_bgcolor="#F8F9F9")


##############################
#Map Layout
##############################
map=html.Div([
 #Place the main graph component here:
  dcc.Graph(figure=Map_Fig, id='US_map')
], className="ds4a-body")
    