import pandas as pd

def load_esg_data(path="data/esg_scores.csv"):
    df = pd.read_csv(path)
    # Basic cleaning or type casting if needed
    df['ESG Score'] = df['ESG Score'].astype(float)
    df['Carbon Footprint'] = df['Carbon Footprint'].astype(float)
    return df
