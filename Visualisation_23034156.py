# import libraries
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"  # to render the visualisations in browser
import plotly.graph_objects as go


# import geojson file
uk_dist_geo = json.load(open("local-authority-district.geojson", "r"))

# extract all locations from geojson file
all_geo_locations = [
    feature["properties"]["reference"] for feature in uk_dist_geo["features"]
]

# import uk house price dataset
df_hpi = pd.read_csv("uk_hpi_pp2.csv")


# select only needed cloumns
df = df_hpi[
    ["Date", "RegionName", "AreaCode", "AveragePrice", "SalesVolume", "12m%Change"]
]

# convert Data to appopriate datatype and specify the format for correct conversion
df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")

# sort dataframe by date
df = df.sort_values(by="Date").copy()

# save dataframe with only data for geojson locations
df_map = df[df["AreaCode"].isin(all_geo_locations)]

# function to make choropleth map
def choroplot(df, titlex):

    fig = px.choropleth_mapbox(
        df,
        geojson=uk_dist_geo,
        locations="AreaCode",
        color="AveragePrice",
        featureidkey="properties.reference",
        mapbox_style="carto-positron",
        zoom=5.4,
        center={"lat": 52.9232, "lon": -1.4720},
        opacity=0.5,
        labels={"AveragePrice": "Average Price"},
        title="Average England house prices in " + titlex,
        hover_name="RegionName",
        hover_data=["AveragePrice"],
        color_continuous_scale="OrRd",
    )

    fig.update_layout(
        height=800,
        width=800,
    )

    fig.show()

# use dec 2013 data for choroplot
df_2013 = df_map[df_map.Date == "2013-12-01"]
choroplot(df_2013, "2013 December")

# use dec 2023 data for choroplot
df_2023 = df_map[df_map.Date == "2023-12-01"]
choroplot(df_2023, "2023 December")

# save dataframe with only dec 2022 data
df_2022 = df_map[df_map.Date == "2022-12-01"]

# manually selected city list for analysis and visualisation
cities = [
    "City of London",
    "Newcastle-under-Lyme",
    "Manchester",
    "North Yorkshire",
    "Oxford",
    "Birmingham",
    "Cambridge",
    "Kensington and Chelsea",
    "Greenwich",
    "Stoke-on-Trent",
]

# bubble plot
fig = px.scatter(
    df_2022.query("RegionName in @cities"),
    x="12m%Change",
    y="AveragePrice",
    size="SalesVolume",
    color="RegionName",
    hover_name="RegionName",
    log_x=True,
    size_max=60,
)

# update layout
fig.update_layout(
    title="Housing Sales in England: 2022 December",
    xaxis_title="Percent Change from Previous Year",
    yaxis_title="Average Price",
    height=800,
)
fig.show()

# save dataframe with data of only select cities
df_cities = df_map[["Date", "AveragePrice", "RegionName"]].query(
    "RegionName in @cities"
)

# pivot dataframe for automatic grouping
df_cities = df_cities.pivot(index="Date", columns="RegionName", values="AveragePrice")

# multi-line plot
fig = px.line(df_cities)

# update layout
fig.update_layout(
    title="England Average Housing prices time series",
    xaxis_title="Date",
    yaxis_title="Average Price",
    height=800,
)

fig.show()

# Initialise dictionary
data = {
    "line_x": [],
    "line_y": [],
    "2013": [],
    "2023": [],
    "colors": [],
    "years": [],
    "regions": [],
}

# Fill data dictionary
for region in cities:
    price_2013 = df_2013.loc[df_2013["RegionName"] == region, "AveragePrice"].iloc[0]
    price_2023 = df_2023.loc[df_2023["RegionName"] == region, "AveragePrice"].iloc[0]
    data["2013"].append(price_2013)
    data["2023"].append(price_2023)
    data["line_x"] += [price_2013, price_2023, None]
    data["line_y"] += [region, region, None]
    data["regions"].append(region)

# Plot Dumbbell plot
fig = go.Figure(
    data=[
        go.Scatter(
            x=data["line_x"],
            y=data["line_y"],
            mode="lines",
            showlegend=False,
            marker=dict(color="grey"),
        ),
        go.Scatter(
            x=data["2013"],
            y=cities,
            mode="markers",
            name="2013",
            marker=dict(color="green", size=10),
        ),
        go.Scatter(
            x=data["2023"],
            y=cities,
            mode="markers",
            name="2023",
            marker=dict(color="blue", size=10),
        ),
    ]
)

# update layout
fig.update_layout(
    title="England Housing prices comparison: 2013 and 2023",
    height=800,
    legend_itemclick=False,
    xaxis_title="Average Price",
    yaxis_title="Region",
)

fig.show()
