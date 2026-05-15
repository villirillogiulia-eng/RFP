import json

def generate_roads():
    # Primary Main Roads for Mudug (approximate paths for visualization)
    features = [
        # Galkayo to Garowe (Northbound Highway)
        {
            "type": "Feature",
            "properties": {"name": "Mogadishu-Garowe Highway", "type": "trunk"},
            "geometry": {
                "type": "LineString",
                "coordinates": [[47.43, 6.77], [47.5, 7.0], [48.0, 7.5], [48.4, 8.4]]
            }
        },
        # Galkayo to Mogadishu (Southbound Highway)
        {
            "type": "Feature",
            "properties": {"name": "Mogadishu-Garowe Highway", "type": "trunk"},
            "geometry": {
                "type": "LineString",
                "coordinates": [[47.43, 6.77], [47.4, 6.5], [47.3, 6.0], [47.2, 5.5], [47.0, 5.0]]
            }
        },
        # Galkayo to Hobyo (Coastal Route)
        {
            "type": "Feature",
            "properties": {"name": "Galkayo-Hobyo Road", "type": "primary"},
            "geometry": {
                "type": "LineString",
                "coordinates": [[47.43, 6.77], [47.8, 6.5], [48.1, 6.0], [48.52, 5.35]]
            }
        },
        # Galkayo to Galdogob
        {
            "type": "Feature",
            "properties": {"name": "Galkayo-Galdogob Road", "type": "secondary"},
            "geometry": {
                "type": "LineString",
                "coordinates": [[47.43, 6.77], [47.2, 6.9], [47.0, 7.03]]
            }
        }
    ]
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open('mudug_roads.js', 'w') as f:
        f.write('const mudugRoads = ' + json.dumps(geojson) + ';\n')
    print("Generated mudug_roads.js with backbone highway network.")

if __name__ == "__main__":
    generate_roads()
