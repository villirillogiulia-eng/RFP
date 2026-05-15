import pandas as pd
import json
import random

def process_flood_data():
    ett_file = 'data.md/IOM_DTM_ETT_SOM_Tracker_sinceFeb2025_w60.xlsx - Full dataset by assessment.csv'
    df = pd.read_csv(ett_file)
    
    # Filter for Mudug and Floods
    mudug_flood = df[(df['Region Name'] == 'Mudug') & (df['Reason of Displacement'].str.contains('Flood', case=False, na=False))].copy()
    
    # Date col name is weird
    date_col = [c for c in df.columns if 'Date' in c][0]
    hazard_col = 'Main Cause of Displacement (type of Natural hazard)'
    arrival_col = 'Total new arrivals since last week'
    
    # Group by Settlement
    flood_summary = mudug_flood.groupby('Settlement Name').agg({
        date_col: 'max',
        arrival_col: 'sum',
        hazard_col: 'first',
        'District Name': 'first'
    }).reset_index()
    
    # Galkayo coordinates for fallback
    GALKAYO_LAT = 6.769726
    GALKAYO_LON = 47.430826
    
    out = []
    for _, row in flood_summary.iterrows():
        name = row['Settlement Name']
        
        # Jitter slightly if centered on Galkayo to avoid overlapping markers
        lat = GALKAYO_LAT + random.uniform(-0.02, 0.02)
        lon = GALKAYO_LON + random.uniform(-0.02, 0.02)
        
        out.append({
            'name': name,
            'lat': lat,
            'lon': lon,
            'date': row[date_col],
            'arrivals': int(row[arrival_col]),
            'type': row[hazard_col]
        })
    
    with open('flood_data.js', 'w') as f:
        f.write('const floodData = ' + json.dumps(out) + ';\n')
    print(f"Generated flood_data.js with {len(out)} locations.")

if __name__ == "__main__":
    process_flood_data()
