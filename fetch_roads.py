import requests
import json

def fetch_mudug_roads():
    # Overpass API query for major roads in Mudug bounding box
    # Mudug approx: 4.5, 46.5 to 7.5, 49.5
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:25];
    (
      way["highway"~"^(primary|secondary|trunk)$"](4.5,46.5,7.5,49.5);
    );
    out body;
    >;
    out skel qt;
    """
    
    print("Fetching roads from Overpass API...")
    response = requests.post(overpass_url, data={'data': overpass_query})
    data = response.json()
    
    # Convert OSM JSON to GeoJSON
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
                    "properties": element.get('tags', {}),
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
