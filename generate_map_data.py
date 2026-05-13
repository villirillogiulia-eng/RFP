import pandas as pd
import json
import re

def extract_coords_from_wkt(wkt):
    try:
        match = re.search(r'POINT\s*\(([-\d.]+)\s+([-\d.]+)\)', str(wkt))
        if match:
            return float(match.group(2)), float(match.group(1)) # lat, lon
    except:
        pass
    return None, None

# Load Risk Mapping (Updated v3)
risk_df = pd.read_csv('data.md/mudug_school_risk_mapping_v3.csv')
schools = []
for _, row in risk_df.iterrows():
    schools.append({
        'name': row['School Name'],
        'district': row['District'],
        'lat': row['Latitude'],
        'lon': row['Longitude'],
        'risk': row['Risk Level'],
        'distance': row['Distance (km)'],
        'conflict_year': row['Year of Conflict']
    })

# Load Conflict Data for background points
conflict_df = pd.read_csv('data.md/mudug_conflict_data_som - Foglio2.csv')
conflicts = []
for _, row in conflict_df.iterrows():
    lat, lon = extract_coords_from_wkt(row['geom_wkt'])
    if lat and lon:
        conflicts.append({
            'id': row['id'],
            'lat': lat,
            'lon': lon,
            'name': row['conflict_name'],
            'side_a': row['side_a'],
            'side_b': row['side_b'],
            'year': int(row['year'])
        })

# Write to JS file
with open('map_data.js', 'w') as f:
    f.write('const schoolData = ' + json.dumps(schools) + ';\n')
    f.write('const conflictData = ' + json.dumps(conflicts) + ';\n')

print("map_data.js generated successfully.")
