import pandas as pd
import json

def generate_detailed_data():
    df = pd.read_csv('iom_dtm_baseline_assessment.csv', low_memory=False)
    mudug = df[df['M-0303: Region name'] == 'Mudug'].copy()
    
    # Calculate Under 18
    res_u18 = mudug['M-1477: # of Male Resident Infants (0-5 years)'].fillna(0).astype(float) + \
              mudug['M-1478: # of Male Resident Children (6-17 years)'].fillna(0).astype(float) + \
              mudug['M-1484: # of Female Resident Infant (0-5 years)'].fillna(0).astype(float) + \
              mudug['M-1485: # of Female Resident Children (6-17 years)'].fillna(0).astype(float)
              
    idp_u18 = mudug['M-1477: # of Male IDP Infant (0-5 years)'].fillna(0).astype(float) + \
              mudug['M-1478: # of Male IDP Children (6-17 years)'].fillna(0).astype(float) + \
              mudug['M-1484: # of Female IDP Infant (0-5 years)'].fillna(0).astype(float) + \
              mudug['M-1485: # of Female IDP Children (6-17 years)'].fillna(0).astype(float)
              
    mudug['u18_total'] = res_u18 + idp_u18
    
    # We need lat/lon for these settlements. 
    # Let's try to find them in settlementData or just use district centers if missing
    # But for a map they need coords. The IOM data doesn't seem to have direct lat/lon in these columns
    # Wait, let me check the IOM headers again for coordinates.
    
    out = []
    for index, row in mudug.iterrows():
        out.append({
            'name': row['M-0445: Settlement Name'],
            'district': row['M-0304: District name'],
            'u18': int(row['u18_total']),
            'accessible': row['Is the area accessible to humanitarian partners?'],
            'type': row['M-0337: What is the location type?']
        })
    
    with open('detailed_settlements.js', 'w') as f:
        f.write('const detailedSettlementData = ' + json.dumps(out) + ';\n')
    print("Generated detailed_settlements.js")

if __name__ == "__main__":
    generate_detailed_data()
