import shapely.geometry
import pyproj
import geopandas as gpd

# Set up projections
p_ll = pyproj.Proj(init='epsg:4326')
p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

# Create corners of rectangle to be transformed to a grid
nw = shapely.geometry.Point((-78.919453, 42.826039))
se = shapely.geometry.Point((-78.795168, 42.966469))

stepsize = 400

# Project corners to target projection
s = pyproj.transform(p_ll, p_mt, nw.x, nw.y) # Transform NW point to 3857
e = pyproj.transform(p_ll, p_mt, se.x, se.y) # .. same for SE

# Iterate over 2D area
grid = []
x = s[0]
while x < e[0]:
    y = s[1]
    row = []
    while y < e[1]:
        p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
        row.append(p)
        y += stepsize
    grid.append(row)
    x += stepsize

# turn grid into square polygons
squares = []
for i in range(0, len(grid) - 1):
    for j in range(0, len(row) - 1):
        points = [grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]]
        square = shapely.geometry.Polygon([[p.x, p.y] for p in points])
        squares.append(square)

gdf = gpd.GeoDataFrame(geometry=squares) 
gdf.to_file('data/interim/square_grid.geojson', driver='GeoJSON')
