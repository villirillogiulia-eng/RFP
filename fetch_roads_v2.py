import requests
import json

def fetch_mudug_roads():
    # Use a more reliable Overpass server and a simpler query
    overpass_url = "https://overpass.kumi.systems/api/interpreter"
    # Mudug Somalia approx: 4.5, 46.5 to 7.5, 49.5
    # Fetching major highways: primary, secondary, trunk
    overpass_query = """
    [out:json][timeout:30];
    (
      way["highway"~"^(primary|secondary|trunk)$"](4.5,46.0,7.5,50.0);
    );
    out body;
    >;
    out skel qt;
    """
    
    print("Fetching roads from Overpass API (Kumi Systems)...")
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=45)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching from Kumi, trying main Overpass API: {e}")
        overpass_url = "https://overpass-api.de/api/interpreter"
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=45)
        data = response.json()
    
    nodes = {n['id']: (n['lat'], n['lon']) for n in data['elements'] if n['type'] == 'node'}
    
    features = []
    for element in data['elements']:
        if element['type'] == 'way':
            coords = []
            for node_id in element['nodes']:
                if node_id in nodes:
                    lat, lon = nodes[node_id]
                    coords.append([lon, lat])
            
            if coords:
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": element.get('tags', {}).get('name', 'Unnamed Road'),
                        "type": element.get('tags', {}).get('highway', 'road')
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    }
                })
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open('mudug_roads.js', 'w') as f:
        f.write('const mudugRoads = ' + json.dumps(geojson) + ';\n')
    
    print(f"Successfully saved {len(features)} road segments to mudug_roads.js")

if __name__ == "__main__":
    fetch_mudug_roads()
