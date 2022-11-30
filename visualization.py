import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
feature_map = {"Happiness_Score_Percentile" : "Happiness Rank",
                'Social support' : 'Social Support',
                'Healthy life expectancy at birth' : 'Life Expectancy',}

app.layout = html.Div([
    html.H3('World Happiness Visualization', style={'marginTop': '10', 'marginBottom': '0'}),
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
    html.H4('Index:'),
    html.P('Happiness Rank: Measured from 1 to 10, with 10 meaning a country is in the top 10% of countries for happiness'),
    html.P('Social Support: Average of binary responses to the question "If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?"'),
    html.P('Log GDP per capita: GDP per capita on a log scale'),
    html.P('Life Expectancy: Displayed in years'),
    html.P('Freedom to make life choices: Average of binary responses to the question "Are you satisfied or dissatisfied with your freedom to choose what you do with your life?"')
], style={"width": "100%", "height" : "100%"})

@app.callback(
    Output("graph", "figure"), 
    Input("feature", "value"),
    Input("year", "value")
)

def display_choropleth(feature, year):
    year = 2000 + int(year)
    df = pd.read_csv("all_data.csv")
    df = df[df['Year'] == year]
    df['Happiness_Score_Percentile'] = abs(df['Happiness_Score_Percentile'] - 10)
    df = df.drop(columns=['Life Expectancy'])
    df = df.rename(columns=feature_map)
    hover_data = {"Country" : False, "Happiness Rank" : True, "Social Support" : ":.3f", "Log GDP per capita" : ":.3f", "Life Expectancy" : ":.2f", "Freedom to make life choices" : ":.3f"}
    fig = px.choropleth(df, locations="Country",
                    color=feature, 
                    hover_name="Country",
                    hover_data=hover_data,
                    color_continuous_scale='RdYlGn',
                    locationmode='country names',
                    projection='natural earth',
                    scope ='world') 
    fig.update_layout(margin={"r" : 0, "t" : 10, "l" : 0, "b" : 0}, 
                        autosize=False, width=1300, height=500,
                        coloraxis_colorbar=dict(
                        title=feature,
                        orientation='h'
                    ))
    fig.update_coloraxes(colorbar_len=0.75, colorbar_thickness=10)
    fig.update_traces(marker_line_width=0.5, marker_line_color='white')
    fig.update_geos(visible=False, showcountries=True, countrycolor="lightgray")
    return fig


app.run_server(debug=False)
