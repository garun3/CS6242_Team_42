import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
feature_map = dict()
feature_map["Happiness Rank"] = "Happiness_Score_Percentile"

app.layout = html.Div([
    html.H4('World happiness visualization'),
    html.P("Select a feature to visualize:"),
    dcc.RadioItems(
        id='feature', 
        options=["Happiness Rank", "Social Support", "Log GDP per capita", "Life Expectancy", "Freedome to make life choices"],
        value="Happiness Rank",
        inline=True
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("feature", "value")
    )

def display_choropleth(feature):
    # df = px.data.election() # replace with your own data source
    # geojson = px.data.election_geojson()
    # fig = px.choropleth(
    #     df, geojson=geojson, color=candidate,
    #     locations="district", featureidkey="properties.district",
    #     projection="mercator", range_color=[0, 6500])
    # fig.update_geos(fitbounds="locations", visible=False)


    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})
    # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #    counties = json.load(response)
    # geojson = counties
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig = px.choropleth(df, geojson=geojson, locations='fips', color='unemp',
    #                        color_continuous_scale="Viridis",
    #                        range_color=(0, 12),
    #                        scope="usa",
    #                        labels={'unemp':'unemployment rate'}
    #                       )
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    feature_val = "Happiness_Score_Percentile" # feature_map[feature]
    df = pd.read_csv("normalized_data.csv")
    json_file = open("world_countries.json")
    geojson = json.load(json_file)
    json_file.close()
    fig = px.choropleth(df, geojson=geojson, locations='Country', color=feature_val,
                           color_continuous_scale="Viridis",
                           range_color=(0, 9),
                           scope='world',
                           labels={'Happiness_Score_Percentile': 'Happiness Rank'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


app.run_server(debug=True)

# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

# # counties["features"][0]
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})
# # df.head()

# fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="usa",
#                            labels={'unemp':'unemployment rate'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
