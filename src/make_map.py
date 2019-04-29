import folium
import pandas as pd

map=folium.Map(location=[42.8864, -78.8784], zoom_start=12)

# folium.GeoJson(
#     'data/processed/food_index.geojson',
#     name='geojson',
#     style_function=lambda x: {'fillColor':'green' if x['properties']['number_options'] == 1 else 'orange'}
# ).add_to(map)

scores = pd.read_csv('data/processed/food_index_scores.csv')

folium.Choropleth(
    geo_data='data/processed/food_index.geojson',
    name='choropleth',
    data=scores,
    columns=['grid_index', 'number_options_produce'],
    key_on='feature.properties.grid_index',
    fill_color='YlGn',

    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Food Desert Index'
).add_to(map)

map.save(outfile='data/processed/map.html')