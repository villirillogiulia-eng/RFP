import pandas as pd
import json
import re
from math import radians, cos, sin, asin, sqrt

# --- CONFIGURATION ---
# Define the files in your 'data.md' folder
CONFLICT_FILE = 'data.md/mudug_conflict_data_som - Foglio2.csv'
SCHOOL_FILE = 'data.md/mudug-education-facilities.xlsx - School Master List,.csv'

# Risk Thresholds (as adjusted)
HIGH_THRESHOLD = 10
MEDIUM_THRESHOLD = 25

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r

def extract_coords_from_wkt(wkt):
    try:
        match = re.search(r'POINT\s*\(([-\d.]+)\s+([-\d.]+)\)', str(wkt))
        if match:
            return float(match.group(2)), float(match.group(1))
    except:
        pass
    return None, None

def run_update():
    print("Starting automated data refresh...")
    
    # 1. Load Data
    try:
        conflict_df = pd.read_csv(CONFLICT_FILE)
        school_df = pd.read_csv(SCHOOL_FILE)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # 2. Extract Coordinates for Conflict
    # ACLED refined file uses WKT
    conflict_df['lat'], conflict_df['lon'] = zip(*conflict_df['geom_wkt'].apply(extract_coords_from_wkt))
    conflict_events = conflict_df[['id', 'lat', 'lon', 'conflict_name', 'side_a', 'side_b', 'year']].dropna()

    # 3. Process Schools & Risk
    school_results = []
    for _, school in school_df.iterrows():
        s_lat, s_lon = school['Latitude'], school['Longitude']
        if pd.isna(s_lat) or pd.isna(s_lon): continue
        
        min_dist = float('inf')
        closest_event = None
        
        for _, event in conflict_events.iterrows():
            dist = haversine(s_lat, s_lon, event['lat'], event['lon'])
            if dist < min_dist:
                min_dist = dist
                closest_event = event
        
        risk = 'High' if min_dist <= HIGH_THRESHOLD else ('Medium' if min_dist <= MEDIUM_THRESHOLD else 'Low')
        
        school_results.append({
            'name': school['Name of school / Learning Center'],
            'district': school['District (Select the appropriate District in the dropdown list)'],
            'lat': s_lat,
            'lon': s_lon,
            'risk': risk,
            'distance': round(min_dist, 2),
            'conflict_year': int(closest_event['year']) if closest_event is not None else 'N/A'
        })

    # 4. Save for Map
    with open('map_data.js', 'w') as f:
        f.write('const schoolData = ' + json.dumps(school_results) + ';\n')
        
        # Format recent conflicts for map points
        conflicts_js = []
        for _, row in conflict_events.head(100).iterrows():
            conflicts_js.append({
                'id': row['id'],
                'lat': row['lat'],
                'lon': row['lon'],
                'name': row['conflict_name'],
                'side_a': row['side_a'],
                'side_b': row['side_b'],
                'year': int(row['year'])
            })
        f.write('const conflictData = ' + json.dumps(conflicts_js) + ';\n')

    print("Success: map_data.js has been regenerated.")

if __name__ == "__main__":
    run_update()
