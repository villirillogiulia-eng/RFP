import pandas as pd

try:
    # Convert UNHCR PRMN
    print("Converting UNHCR PRMN to CSV...")
    unhcr_df = pd.read_excel('unhcr_prmn.xlsx')
    unhcr_df.to_csv('unhcr_prmn_displacement.csv', index=False)
    print("Successfully created unhcr_prmn_displacement.csv")

    # Convert IOM DTM
    print("Converting IOM DTM to CSV...")
    iom_df = pd.read_excel('iom_dtm.xlsx')
    iom_df.to_csv('iom_dtm_baseline_assessment.csv', index=False)
    print("Successfully created iom_dtm_baseline_assessment.csv")
except Exception as e:
    print(f"Error during conversion: {e}")
