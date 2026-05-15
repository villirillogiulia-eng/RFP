import pandas as pd
import json

def update_settlement_data():
    # Load settlements from settlements_data.js
    with open('settlements_data.js', 'r') as f:
        content = f.read()
        json_str = content.split('const settlementData = ')[1].split(';')[0]
        settlements = json.loads(json_str)
    
    # Load detailed population and accessibility data
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
    
    # Create a lookup dictionary
    lookup = {}
    for index, row in mudug.iterrows():
        lookup[row['M-0445: Settlement Name'].lower()] = {
            'u18': int(row['u18_total']),
            'accessible': row['Is the area accessible to humanitarian partners?']
        }
    
    # Update settlements
    updated_settlements = []
    for s in settlements:
        name_lower = s['name'].lower()
        if name_lower in lookup:
            s['u18'] = lookup[name_lower]['u18']
            s['accessible'] = lookup[name_lower]['accessible']
        else:
            s['u18'] = 0
            s['accessible'] = "Unknown"
        updated_settlements.append(s)
        
    with open('settlements_data.js', 'w') as f:
        f.write('const settlementData = ' + json.dumps(updated_settlements) + ';\n')
    print("Updated settlements_data.js")

if __name__ == "__main__":
    update_settlement_data()
