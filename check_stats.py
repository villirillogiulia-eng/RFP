import json

with open('map_data.js', 'r') as f:
    content = f.read()
    school_data_str = content.split('const schoolData = ')[1].split(';\n')[0]
    data = json.loads(school_data_str)

print(f"Total: {len(data)}")
print(f"High: {len([s for s in data if s['risk'] == 'High'])}")
print(f"Medium: {len([s for s in data if s['risk'] == 'Medium'])}")
print(f"Low: {len([s for s in data if s['risk'] == 'Low'])}")
