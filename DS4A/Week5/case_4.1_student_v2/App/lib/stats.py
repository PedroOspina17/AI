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

df = data.df

##############################################################
# SCATTER PLOT
###############################################################

scatter_fig = px.scatter(df, x="Sales", y="Profit", color="Category", hover_data=['State','Sub-Category','Order ID','Product Name'])  
scatter_col = dbc.Col([ dcc.Graph(figure=scatter_fig, id='scatter-figure')],className="Col")
###############################################################
# LINE PLOT
###############################################################


states = ["California", "New York"]

infoToPlot = df[df["State"].isin(states)].groupby(["State","Order_Month"]).sum().reset_index()
infoToPlot
line_fig = px.line(infoToPlot,x="Order_Month",y="Sales",color="State")

linePlotCol = dbc.Col([ dcc.Graph(figure=line_fig, id='line-figure') ],className="Col")

#################################################################################
# Here the layout for the plots to use.
#################################################################################
statsRow = dbc.Row([ 
    linePlotCol,
    scatter_col
],className="Row")


stats=html.Div([ 
	#Place the different graph components here.
  statsRow
	],className="ds4a-body")



