import pandas as pd
import json

def process_under18_data():
    print("Processing Under-18 data from IOM DTM...")
    df = pd.read_csv('iom_dtm_baseline_assessment.csv', low_memory=False)
    
    # Filter for Mudug
    mudug_df = df[df['M-0303: Region name'] == 'Mudug'].copy()
    
    # Identify relevant columns
    # Residents Under 18: Male (0-5 + 6-17) + Female (0-5 + 6-17)
    res_m_0_5 = 'M-1477: # of Male Resident Infants (0-5 years)'
    res_m_6_17 = 'M-1478: # of Male Resident Children (6-17 years)'
    res_f_0_5 = 'M-1484: # of Female Resident Infant (0-5 years)'
    res_f_6_17 = 'M-1485: # of Female Resident Children (6-17 years)'
    
    # IDPs Under 18: Male (0-5 + 6-17) + Female (0-5 + 6-17)
    idp_m_0_5 = 'M-1477: # of Male IDP Infant (0-5 years)'
    idp_m_6_17 = 'M-1478: # of Male IDP Children (6-17 years)'
    idp_f_0_5 = 'M-1484: # of Female IDP Infant (0-5 years)'
    idp_f_6_17 = 'M-1485: # of Female IDP Children (6-17 years)'
    
    # Location classification: 'M-0337: What is the location type?'
    # We'll treat 'Rural (Tulo/Village)' as settlements and 'Urban (Waah/Neighbourhood)' as cities
    class_col = 'M-0337: What is the location type?'
    
    # Convert columns to numeric
    numeric_cols = [res_m_0_5, res_m_6_17, res_f_0_5, res_f_6_17, 
                    idp_m_0_5, idp_m_6_17, idp_f_0_5, idp_f_6_17]
    for col in numeric_cols:
        mudug_df[col] = pd.to_numeric(mudug_df[col], errors='coerce').fillna(0)
    
    # Calculate Under 18 totals
    mudug_df['residents_u18'] = mudug_df[res_m_0_5] + mudug_df[res_m_6_17] + mudug_df[res_f_0_5] + mudug_df[res_f_6_17]
    mudug_df['idps_u18'] = mudug_df[idp_m_0_5] + mudug_df[idp_m_6_17] + mudug_df[idp_f_0_5] + mudug_df[idp_f_6_17]
    
    # Classification based on M-0337
    mudug_df['is_urban'] = mudug_df[class_col].str.contains('Urban', case=False, na=False)
    
    # Aggregation
    # IDPs in Settlements (Rural)
    idps_in_settlements = mudug_df[~mudug_df['is_urban']]['idps_u18'].sum()
    
    # Residents in Cities (Urban)
    residents_in_cities = mudug_df[mudug_df['is_urban']]['residents_u18'].sum()
    
    # Extra for context
    idps_in_cities = mudug_df[mudug_df['is_urban']]['idps_u18'].sum()
    residents_in_settlements = mudug_df[~mudug_df['is_urban']]['residents_u18'].sum()

    stats = {
        "idps_u18_settlements": int(idps_in_settlements),
        "residents_u18_cities": int(residents_in_cities),
        "idps_u18_cities": int(idps_in_cities),
        "residents_u18_settlements": int(residents_in_settlements)
    }
    
    print(f"Stats: {stats}")
    
    with open('pop_u18_data.js', 'w') as f:
        f.write('const popU18Data = ' + json.dumps(stats) + ';\n')
    
    print("pop_u18_data.js generated.")

if __name__ == "__main__":
    process_under18_data()
