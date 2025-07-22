import matplotlib.pyplot as plt
import seaborn as sns

def plot_esg_trends(esg_df):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots()
    sectors = esg_df.groupby("Sector")["ESG Score"].mean().sort_values()
    sectors.plot(kind="barh", ax=ax, color="green")
    ax.set_title("Average ESG Score by Sector")
    ax.set_xlabel("ESG Score")
    ax.set_ylabel("Sector")
    return fig

def plot_carbon_impact(df):
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x="Ticker", y="Carbon Footprint", ci=None, ax=ax, palette="Reds_d")
    ax.set_title("Carbon Footprint per Asset (Weighted by Portfolio)")
    ax.set_xlabel("Ticker")
    ax.set_ylabel("Carbon Footprint (kg CO₂)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig



