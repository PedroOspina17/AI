#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#Data
import json
from datetime import datetime as dt

#Recall app
from app import app
import dataload as data


####################################################################################
# Add the DS4A_Img
####################################################################################

DS4A_Img=html.Div(
            children=[
                html.Img(
                    src=app.get_asset_url("ds4a-img.svg"),
                    id="ds4a-image",
                )
            ],
        )

#############################################################################
# State Dropdown Card
#############################################################################

ddlCtl = dcc.Dropdown(
        id='state-dropdown',
        options=[{"label": key, "value": value } for key, value in data.states_dict.items()],
        value=['NY','CA'],
        multi=True
    )

##############################################################################
# Date Picker Card
##############################################################################

datePickerCtl = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=dt(2014, 1, 2),
        max_date_allowed=dt(2017, 12, 31),
        initial_visible_month=dt(2014, 4, 17),
        start_date=dt(2014, 4, 17).date(),
        end_date=dt(2014, 4, 17).date()
    ),
    html.Div(id='output-container-date-picker-range')
])



#############################################################################
# Sidebar Layout
#############################################################################
sidebar=html.Div(
    [   DS4A_Img, #Add the DS4A_Img located in the assets folder
        html.Hr(), #Add an horizontal line
        ####################################################
        #Place the rest of Layout here
        ####################################################
        datePickerCtl,
        ddlCtl

    ],className='ds4a-sidebar'
    
)





