import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
feature_map = dict()
feature_map = {"Happiness Rank": "Happiness_Score_Percentile",
                'Social Support':'Social support',
                'Log GDP per capita': 'Log GDP per capita',
                'Life Expectancy': 'Healthy life expectancy at birth',
                'Freedom to make life choices': 'Freedom to make life choices'
}

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
], 
style={"width": "100%", "height" : "100%"}
    )

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
    #print(feature)
    feat = feature_map[feature]
    fig = px.choropleth(df, locations="Country",
                    color=feat, 
                    hover_name="Country",
                    hover_data=['Happiness_Score_Percentile','Social support', 'Log GDP per capita', 'Healthy life expectancy at birth', 'Freedom to make life choices'], 
                    color_continuous_scale='RdYlGn',
                    locationmode='country names',
                    #range_color=[1, 10],
                    projection='natural earth',
                    scope ='world') 
    fig.update_layout(margin={"r" : 0, "t" : 10, "l" : 0, "b" : 0}, 
                        autosize=False, width=1300, height=500,
                        coloraxis_colorbar=dict(
                        title=feature,
                        orientation='h'
                        #thicknessmode="pixels",
                        #lenmode="pixels",
                        #yanchor="top",y=1,
                        #ticks="outside",
                        #tickvals=[1,2,3,4,5,6,7,8,9,10],#[10,9,8,7,6,5,4,3,2,1],
                        #ticktext=[1,2,3,4,5,6,7,8,9,10]#[10,9,8,7,6,5,4,3,2,1]
))
    fig.update_coloraxes(colorbar_len=0.75)
    return fig


app.run_server(debug=False)
