import requests
import json
import pandas as pd
import numpy as np

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json]
[bbox:42.82603863,-78.91945281,42.96646854,-78.79516771];

(
  node["shop"~"supermarket|greengrocer|organic|grocery|convenience"];
  way["shop"~"supermarket|greengrocer|organic|grocery|convenience"];
);

out center;
"""
response = requests.get(overpass_url, params={'data': overpass_query})

# save as json
# with open('data/raw/store_locations.json', 'wb') as outf:
#     outf.write(response.content)

data = json.loads(response.content)

df = pd.io.json.json_normalize(data['elements'])
df = df[['id', 
         'type', 
         'center.lat',
         'center.lon',
         'lat',
         'lon', 
         'tags.name',
         'tags.addr:housenumber',
         'tags.addr:street',
         'tags.addr:city',
         'tags.addr:state',
         'tags.addr:postcode',
         'tags.shop',
         ]]

df['store_lat'] = df['center.lat'].combine_first(df['lat'])
df['store_lon'] = df['center.lon'].combine_first(df['lon'])
df['full_address'] = df['tags.addr:housenumber'] + ' ' \
                      + df['tags.addr:street'] + ' ' \
                      + df['tags.addr:city'] + ', ' \
                      + df['tags.addr:state'] + ' ' \
                      + df['tags.addr:postcode']
df = df.drop(['center.lat', 'center.lon', 'lat', 'lon', 'tags.addr:housenumber', 'tags.addr:street', 'tags.addr:city', 'tags.addr:state', 'tags.addr:postcode'], axis=1)
df = df.rename(columns={'tags.name': 'store_name', 'tags.shop': 'shop_type'})
df['produce'] = df['shop_type'].isin(['organic', 'greengrocer', 'grocer', 'supermarket'])
df['price'] = np.random.choice([1, 2, 3], len(df))

# write to csv
df.to_csv('data/raw/store_locations.csv', index=False)