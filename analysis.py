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

def plot_carbon_impact(portfolio_df):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots()
    sorted_df = portfolio_df.sort_values("Carbon Footprint", ascending=False)
    ax.barh(sorted_df["Ticker"], sorted_df["Carbon Footprint"], color="gray")
    ax.set_xlabel("Carbon Footprint (tons CO₂)")
    ax.set_title("Carbon Footprint by Asset")
    return fig




