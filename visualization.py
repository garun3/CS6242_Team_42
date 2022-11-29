import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
feature_map = dict()
feature_map["Happiness Rank"] = "Happiness_Score_Percentile"

app.layout = html.Div([
    html.H3('World happiness visualization', style={'marginTop': '10', 'marginBottom': '0'}),
    html.Div([
        html.Div([
            html.P("Select a feature to visualize:"),
            dcc.Dropdown(["Happiness Rank", "Social Support", "Log GDP per capita", "Life Expectancy", "Freedom to make life choices"], 'Happiness Rank', id='feature'),
        ], style={"width": "30%", 'float': 'left'}),
        html.Div([
            html.P("Select the year to visualize:"),
            dcc.Slider(13, 21, step=None,
                marks={
                13: '2013',
                14: '2014',
                15: '2015',
                16: '2016',
                17: '2017',
                18: '2018',
                19: '2019',
                20: '2020',
                21: '2021',
                }, value=13, id='year'),
        ], style={"width": "65%", 'float': 'right'}),
    ], style={'width': '100%', 'height' : '100px'}),
    dcc.Graph(id="graph"),
], style={"width": "100%", "height" : "100%"})

@app.callback(
    Output("graph", "figure"), 
    Input("feature", "value"),
    Input("year", "value")
)

def display_choropleth(feature, year):
    year = 2000 + int(year)
    df = pd.read_csv("normalized_data.csv")
    df = df[df['Year'] == year]
    fig = px.choropleth(df, locations="Country",
                    color="Happiness_Score_Percentile", 
                    hover_name="Country",
                    hover_data=['Happiness_Score_Percentile','Social support', 'Log GDP per capita', 'Healthy life expectancy at birth', 'Freedom to make life choices'], 
                    color_continuous_scale='Greens',
                    locationmode='country names',
                    range_color=[0, 9],
                    projection='natural earth',
                    scope ='world') 
    fig.update_layout(margin={"r" : 0, "t" : 10, "l" : 0, "b" : 0}, 
                        autosize=False, width=1300, height=600)
    fig.update_coloraxes(colorbar_len=0.75)
    return fig


app.run_server(debug=False)
