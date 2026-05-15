import pandas as pd
import os

def clean_unhcr_prmn():
    print("Cleaning UNHCR PRMN data...")
    df = pd.read_csv('unhcr_prmn_displacement.csv')
    
    # Filter for Mudug as arrival region
    mudug_arrival = df[df['Current (Arrival) Region'] == 'Mudug'].copy()
    
    # Standardize column names for ease of use
    mudug_arrival.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').lower() for c in mudug_arrival.columns]
    
    # Save cleaned Mudug-specific data
    mudug_arrival.to_csv('cleaned_mudug_unhcr_prmn.csv', index=False)
    print(f"Saved {len(mudug_arrival)} records to cleaned_mudug_unhcr_prmn.csv")
    return mudug_arrival

def clean_iom_dtm():
    print("Cleaning IOM DTM data...")
    # The IOM file has a complex header structure, we need to be careful
    df = pd.read_csv('iom_dtm_baseline_assessment.csv')
    
    # Mapping the complex headers to simpler names
    # Based on the head output earlier:
    # M-0303: Region name -> region
    # M-0304: District name -> district
    # M-0310: Estimated # of IDP Individuals -> idp_individuals
    # M-0328: Estimated # of Resident Individuals -> resident_individuals
    
    # Let's find the exact column names by searching for keywords
    cols = df.columns.tolist()
    region_col = [c for c in cols if 'Region name' in c][0]
    district_col = [c for c in cols if 'District name' in c][0]
    idp_col = [c for c in cols if 'IDP Individuals' in c and 'Estimated' in c][0]
    resident_col = [c for c in cols if 'Resident Individuals' in c and 'Estimated' in c][0]
    settlement_col = [c for c in cols if 'Settlement Name' in c][0]
    
    # Filter for Mudug
    mudug_dtm = df[df[region_col] == 'Mudug'].copy()
    
    # Select and rename key columns
    cleaned_dtm = mudug_dtm[[
        settlement_col, district_col, idp_col, resident_col
    ]].copy()
    
    cleaned_dtm.columns = ['settlement', 'district', 'idp_individuals', 'resident_individuals']
    
    # Convert to numeric, handling potential errors
    cleaned_dtm['idp_individuals'] = pd.to_numeric(cleaned_dtm['idp_individuals'], errors='coerce').fillna(0)
    cleaned_dtm['resident_individuals'] = pd.to_numeric(cleaned_dtm['resident_individuals'], errors='coerce').fillna(0)
    
    # Save cleaned Mudug-specific data
    cleaned_dtm.to_csv('cleaned_mudug_iom_dtm.csv', index=False)
    print(f"Saved {len(cleaned_dtm)} settlement records to cleaned_mudug_iom_dtm.csv")
    return cleaned_dtm

if __name__ == "__main__":
    clean_unhcr_prmn()
    clean_iom_dtm()
