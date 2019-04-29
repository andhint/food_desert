import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np

grid = gpd.read_file('data/interim/square_grid.geojson')

# read in grid
grid['centroid'] = grid.geometry.centroid

# read in store locations
df = pd.read_csv('data/raw/store_locations.csv')

# create stores geodataframe
geometry = [Point(xy) for xy in zip(df['store_lon'], df['store_lat'])]
df = df.drop(['store_lon', 'store_lat'], axis=1)
crs = {'init': 'epsg:4326'}
stores = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

def haversine(lat1, lon1, lat2, lon2):
    MILES = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    total_miles = MILES * c
    return total_miles

def number_within_radius(grid_square, stores, radius):
    distances = haversine(grid_square.centroid.y, grid_square.centroid.x, stores.geometry.y, stores.geometry.x)
    return (distances < radius).sum()

grid['number_options'] = grid.apply(number_within_radius, stores=stores, radius=1, axis=1)
grid['number_options_produce'] = grid.apply(number_within_radius, stores=stores[stores['produce']==True], radius=1, axis=1)
grid['grid_index'] = grid.index

# trim to buffalo
buffalo = gpd.read_file('data/raw/buffalo_municipal_boundary.geojson')
grid = gpd.sjoin(grid, buffalo, how='inner', op='intersects')

# write to file
grid[['geometry', 'number_options', 'number_options_produce', 'grid_index']].to_file('data/processed/food_index.geojson', driver='GeoJSON')
grid[['grid_index', 'number_options', 'number_options_produce']].to_csv('data/processed/food_index_scores.csv', index=False)