import pandas as pd

#Data Extraction
def run_extraction():
    try:
        data = pd.read_csv(r'zipco_transaction.csv')
        print("Data extraction successful!")
    except Exception as e:
        print(f"Error during data extraction: {e}")

    