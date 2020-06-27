#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#Data 
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#Recall app
from app import app
import dataload as data


###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from lib import title, sidebar, us_map, stats

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    [ 
      us_map.map,
      stats.stats,
      title.title,
      sidebar.sidebar,
    ],
    className="ds4a-app", #You can also add your own css files by locating them into the assets folder
)

 
    
###############################################   
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
#Load and modify the data that will be used in the app.
#################################################################




#############################################################
# LINE PLOT : Add sidebar interaction here
#############################################################



#############################################################
# PROFITS BY CATEGORY : Add sidebar interaction here
#############################################################



#############################################################
# TREEMAP PLOT : Add sidebar interaction here
#############################################################
@app.callback(
# [
#     Output('map-figure','figure'),
#  Output('scatter-figure','figure'),
 Output('line-figure','figure')
# ]
    ,
[Input('date-picker','start_date'),Input('date-picker','end_date'),Input('state-dropdown','value')]
)
def changePlots(start_date,end_date,states):
    df = data.df
    scatter_fig = px.scatter(df, x="Sales", y="Profit", color="Category", hover_data=['State','Sub-Category','Order ID','Product Name'])  
    print(states)
    
    infoToPlot = df[df["State_abbr"].isin(states)].copy()
    print(infoToPlot)
    infoToPlot = infoToPlot.groupby(["State","Order_Month"]).sum().reset_index()
    infoToPlot
    line_fig = px.line(infoToPlot,x="Order_Month",y="Sales",color="State")

    return line_fig


#############################################################
# MAP : Add interactions here
#############################################################

#MAP date interaction

# @app.callback(
#     Output('state_dropdown','value'),
#     [
#         Input('US_map','clickData')
#     ],
#     [
#         State('state_dropdown','value')
#     ]
# )
# def click_saver(clickData,state):
#     if clickData is None:
#         raise PreventUpdate
#     #print(clickData)
#     state.append(clickData['points'][0]['location'])
#     return state

#MAP click interaction

# @app.callback(
# Output('main-figure-map','figure'),
# [Input('date-picker','start_date'),Input('date-picker','end_date')]
# )
# def mapInteraction(start_date,end_date):
#     tempDf = (df[""] > start_date) & (df[""] < end_date)
    
#     dff=tempDf.groupby('State_abbr').sum().reset_index()

#     map_fig = px.choropleth_mapbox(dff,                         #Data
#         locations='State_abbr',                   #Column containing the identifiers used in the GeoJSON file 
#         color='Sales',                            #Column giving the color intensity of the region
#         geojson=geojson,                          #The GeoJSON file
#         zoom=3,                                   #Zoom
#         mapbox_style="carto-positron",            #Mapbox style, for different maps you need a Mapbox account and a token
#         center={"lat": 37.0902, "lon": -95.7129}, #Center
#         color_continuous_scale="Viridis",         #Color Scheme
#         opacity=0.5,                              #Opacity of the map
#         )

#     map_fig.update_layout(title='US Map',paper_bgcolor="#F8F9F9")
    
#     return map_fig
                                                 
           
        

if __name__ == "__main__":
    app.run_server(debug=True)
