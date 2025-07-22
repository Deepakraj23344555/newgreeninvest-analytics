import matplotlib.pyplot as plt
import seaborn as sns

def plot_esg_trends(df):
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x="Sector", y="ESG Score", ci=None, ax=ax, palette="Greens_d")
    ax.set_title("Average ESG Scores by Sector")
    ax.set_xlabel("Sector")
    ax.set_ylabel("ESG Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
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
