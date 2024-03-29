import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
feature_map = {"Happiness_Score_Percentile" : "Happiness Rank",
                'Social support' : 'Social Support',
                'Healthy life expectancy at birth' : 'Life Expectancy',}

df = pd.read_csv("all_data_2.csv")
df['Happiness_Score_Percentile'] = abs(df['Happiness_Score_Percentile'] - 10)
df['Regression_Prediction'] = abs(df['Regression_Prediction'] - 10)
df['Decision_Tree_Prediction'] = abs(df['Decision_Tree_Prediction'] - 10)
df = df.drop(columns=['Life Expectancy'])
df = df.rename(columns=feature_map)

table = pd.read_csv("feature_description.csv")

app.layout = html.Div([
    html.H4('World Happiness Visualization', style={'marginTop': '10', 'marginBottom': '0'}),
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
    ], style={'width': '96%', 'height' : '100px'}),
    # Div where the main graphs go
    html.Div(
        dbc.Row([ 
            dbc.Col([
                dcc.Graph(id="graph")]), # Main chloropleth map
        ])
    ),
    # Div for the feature label
    html.Div([
        html.H3("Features", style={"text-align":"center"})
    ], style={"margin-top":"50px"}),
    # Div for the feature table and variance graph
    html.Div(
        [
        dbc.Row([
            dbc.Col([
                dbc.Table.from_dataframe(table, striped=True, bordered=True, size="sm") # Feature table
            ], width=7),
            dbc.Col(dcc.Graph(id="country-timeseries"), width=5) # Country time series graph
        ]),
    ], style={"margin-top":"10px", "margin-right":"15px"})

], style={"width": "100%", "height" : "100%", "margin":"20px"}) # End layout div

# chloropleth callback
@app.callback(
    Output("graph", "figure"), 
    Input("feature", "value"),
    Input("year", "value")
)
def display_choropleth(feature, year):
    year = 2000 + int(year)
    dff = df[df['Year'] == year]
    hover_data = {"Country" : False, "Happiness Rank" : True, "Regression_Prediction" : True, "Decision_Tree_Prediction" : True, "Social Support" : ":.3f", "Log GDP per capita" : ":.3f", "Life Expectancy" : ":.2f", "Freedom to make life choices" : ":.3f"}
    fig = px.choropleth(dff, locations="Country",
                    color=feature, 
                    hover_name="Country",
                    hover_data=hover_data,
                    color_continuous_scale='RdYlGn',
                    locationmode='country names',
                    projection='natural earth',
                    scope ='world',
                    custom_data=["Country"]) 
    fig.update_layout(margin={"r" : 0, "t" : 10, "l" : 0, "b" : 0}, 
                        autosize=True, height=500,
                        coloraxis_colorbar=dict(
                        title=feature,
                        orientation='h'
                    ))
    fig.update_coloraxes(colorbar_len=0.75, colorbar_thickness=10)
    fig.update_traces(marker_line_width=0.5, marker_line_color='white')
    fig.update_geos(visible=False, showcountries=True, countrycolor="lightgray")
    return fig

# time series graph helper function
def create_timeseries(dff, feature, country, feature_range):
    fig = px.scatter(dff, x="Year", y=feature, color_discrete_sequence=['gray'])
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear')
    fig.update_layout(height=500, margin={'l': 0, 'b': 0, 'r': 60, 't': 35}, title_text=feature + " for " + country,  title_x=0.5, yaxis_range=feature_range, plot_bgcolor="whitesmoke")
    return fig
# time series graph callback
@app.callback(
    Output("country-timeseries", "figure"), 
    Input("graph", "clickData"),
    Input("feature", "value")
    )
def update_timeseries(clickData, feature):
    country = "United States"
    if clickData is not None:
        country = clickData["points"][0]["location"]
    dff = df[df["Country"] == country]
    feature_range = (0, df[feature].max() * 1.03)
    return create_timeseries(dff, feature, country, feature_range)  

app.run_server(debug=False)
