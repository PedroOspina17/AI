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
import dataload as data



#############################
# Load map data
#############################


dff=data.df.groupby('State_abbr').sum().reset_index()

#Here we can see the syntax used for the creation of choropleth maps:

map_fig = px.choropleth_mapbox(dff,                         #Data
        locations='State_abbr',                   #Column containing the identifiers used in the GeoJSON file 
        color='Sales',                            #Column giving the color intensity of the region
        geojson=data.geojson,                          #The GeoJSON file
        zoom=3,                                   #Zoom
        mapbox_style="carto-positron",            #Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 37.0902, "lon": -95.7129}, #Center
        color_continuous_scale="Viridis",         #Color Scheme
        opacity=0.5,                              #Opacity of the map
        )

map_fig.update_layout(title='US Map',paper_bgcolor="#F8F9F9")

##############################
#Map Layout
##############################
map=html.Div([
 #Place the main graph component here:
    dcc.Graph(figure=map_fig, id='map-figure') 
], className="ds4a-body")
    