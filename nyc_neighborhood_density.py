
import pandas as pd
import json
import math
import plotly.express as px
from area import area

# read the neighborhood population data into a DataFrame and load the GeoJSON data
df = pd.read_csv('New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv')
nycmap = json.load(open("nyc_neighborhoods.geojson"))

# create dictionary of nta codes mapping to area (square miles)
d = {}
neighborhood = nycmap["features"]
for n in neighborhood:
    code = n["properties"]["ntacode"]
    a = area(n["geometry"])/(1609*1609) # converts from m^2 to mi^2
    d[code] = a

# create new columns in df for area and density
df["area"] = df["NTA Code"].map(d)
df = df.dropna(subset=["area"])
df["density"] = df["Population"]/df["area"]

# call Plotly Express choropleth function to visualize data
fig = px.choropleth_mapbox(df,
                           geojson=nycmap,
                           locations="NTA Code",
                           featureidkey="properties.ntacode",
                           color="density",
                           color_continuous_scale="viridis",
                           mapbox_style="carto-positron",
                           zoom=9, center={"lat": 40.7, "lon": -73.9},
                           opacity=0.7,
                           hover_name="NTA Name"
                           )

fig.show()