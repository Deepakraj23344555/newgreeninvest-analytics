def simulate_fossil_divestment(df):
    return df[df['Sector'] != 'Energy']
