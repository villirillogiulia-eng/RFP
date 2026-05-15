import pandas as pd
import json

def generate_school_status():
    df = pd.read_excel('data.md/raw data/somalia-education-facilities.xlsx')
    mudug = df[df['Region (Select the appropriate Region 1 in the dropdown list)'] == 'Mudug'].copy()
    
    out = []
    for index, row in mudug.iterrows():
        out.append({
            'name': row['Name of school / Learning Center'],
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'boys': int(row['Enrolment\nBoys\n(As at January 2022)']) if pd.notna(row['Enrolment\nBoys\n(As at January 2022)']) else 0,
            'girls': int(row['Enrolment Girls (As at January 2022)']) if pd.notna(row['Enrolment Girls (As at January 2022)']) else 0,
            'male_teachers': int(row['Male Teachers working at school']) if pd.notna(row['Male Teachers working at school']) else 0,
            'female_teachers': int(row['Female Teachers working at school']) if pd.notna(row['Female Teachers working at school']) else 0
        })
    
    with open('school_status_data.js', 'w') as f:
        f.write('const schoolStatusData = ' + json.dumps(out) + ';\n')
    print("Generated school_status_data.js")

if __name__ == "__main__":
    generate_school_status()
