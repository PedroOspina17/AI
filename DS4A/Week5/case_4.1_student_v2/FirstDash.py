import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import json
import dash_core_components as dcc
import dash_bootstrap_components as dbc

#Create the app
app = dash.Dash(__name__,external_stylesheets = [dbc.themes.BOOTSTRAP])

#Create Layout

df = pd.read_csv('App/Data/superstore.csv', parse_dates=['Order Date', 'Ship Date'])


with open('App/Data/us.json') as geo:
    geojson = json.loads(geo.read())

with open('App/Data/states.json') as f:
    states_dict = json.loads(f.read())


df['State_abbr'] = df['State'].map(states_dict)

scatter_fig = px.scatter(df, x="Sales", y="Profit", color="Category")

dff=df.groupby('State_abbr').sum().reset_index()

#Here we can see the syntax used for the creation of choropleth maps:

map_fig = px.choropleth_mapbox(dff,                         #Data
        locations='State_abbr',                   #Column containing the identifiers used in the GeoJSON file 
        color='Sales',                            #Column giving the color intensity of the region
        geojson=geojson,                          #The GeoJSON file
        zoom=3,                                   #Zoom
        mapbox_style="carto-positron",            #Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 37.0902, "lon": -95.7129}, #Center
        color_continuous_scale="Viridis",         #Color Scheme
        opacity=0.5,                              #Opacity of the map
        )



app.layout = html.Div([
    html.H2("US Sales Map", id='title'), #Creates the title of the app
    html.Div([
        html.P(['Hola a todos'],className="text-center"),
        html.P(['Problemas con dash! no hay'])
    ]),
    dcc.Markdown('''
    # Este es un titulo
    Locus, podemos escribir [link Natesh](https://scholar.google.com/citations?user=iKRpHLgAAAAJ&hl=en)
    Tambien podemos poner codigo
    ```python
    import pandas
    ```
    Or include even latex !! $x^2 + y^2 = sqrt(z)$
    '''),
    dcc.Graph(figure=scatter_fig, id='main-figure-scatter'),
    dcc.Graph(figure=map_fig, id='main-figure-map'),
    dcc.Slider(min=0,max=1,marks={0:'US Map', 1:'Scatter Plot'},value=0,id='fig-slider',)
    
])



@app.callback(
    Output('main-figure-map','figure'),
    [Input('fig-slider','value')])

def slider_interaction(slider_val):
    if slider_val==0:
        fig=map_fig
    else:
        fig=scatter_fig

    return fig 

#Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(debug=True)