import pandas as pd
import plotly.graph_objs as go
import json
import math
import plotly.express as px
import geopy.distance
import numpy as np
from sklearn import neighbors

# load geojson data for manhattan
nycmap = json.load(open("nycpluto_manhattan.geojson"))

# load library data from csv file, convert coordinates to radians, and create coordinate pairs
libs = pd.read_csv('manhattanlibraries.csv', usecols=['facname', 'latitude', 'longitude'])
libs['latitude'] = libs['latitude'].apply(func=math.radians)
libs['longitude'] = libs['longitude'].apply(func=math.radians)
libs['coord'] = list(zip(libs['latitude'], libs['longitude']))

# load library data into BallTree
libcoords = np.asarray(list(libs['coord']))
tree = neighbors.BallTree(libcoords, metric="haversine")

# load lot data from csv file, convert coordinates to radians, and create coordinate pairs
df = pd.read_csv('pluto_small.csv')
df = df.dropna(subset=['assesstot', 'bldgarea', 'lotarea', 'latitude', 'longitude'])
df['latitude'] = df['latitude'].apply(func=math.radians)
df['longitude'] = df['longitude'].apply(func=math.radians)
df['coord'] = list(zip(df['latitude'], df['longitude']))

# query the BallTree and save results back in df
lotcoords = np.asarray(list(df['coord']))
dist, _ = tree.query(X=lotcoords, k=1)
df['dist'] = dist
df['dist'] = df['dist'].apply(lambda x: x*3960)

# use Plotly express function to create a choropleth map
fig = px.choropleth_mapbox(df,
                           geojson=nycmap,
                           locations="bbl",
                           featureidkey="properties.bbl",
                           color="dist",
                           color_continuous_scale=px.colors.sequential.thermal[::-1],
                           range_color=(0, 0.5),
                           mapbox_style="carto-positron",
                           zoom=9, center={"lat": 40.7, "lon": -73.7},
                           opacity=0.7,
                           hover_name="ownername"
                           )

fig.show()