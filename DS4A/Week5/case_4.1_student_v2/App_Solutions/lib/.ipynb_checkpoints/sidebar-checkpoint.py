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
# State Dropdown 
#############################################################################
with open('data\\states.json') as f:
    states = json.loads(f.read())

dropdown=dcc.Dropdown(
        id="state_dropdown",
        options=[{"label":key, "value":states[key]} for key in states.keys()],
        value=["NY",'CA'],
        multi=True
        )


##############################################################################
# Date Picker 
##############################################################################

date_picker=dcc.DatePickerRange(
                id='date_picker',
                min_date_allowed=dt(2014, 1, 2),
                max_date_allowed=dt(2017, 12, 31),
                start_date=dt(2016,1,1).date(),
                end_date=dt(2017, 1, 1).date()
            )


#############################################################################
# Sidebar Layout
#############################################################################
sidebar=html.Div(
    [   DS4A_Img, #Add the DS4A_Img located in the assets folder
        html.Hr(), #Add an horizontal line
        ####################################################
        #Place the rest of Layout here
        ####################################################
        html.H5("Select dates"),
        date_picker,
        html.Hr(),
        html.H5("Select states"),
        dropdown,
        html.Hr(),
         


    ],className='ds4a-sidebar'
    
)





