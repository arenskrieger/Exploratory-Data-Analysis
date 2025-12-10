"""
Finance and economics exploratory data analysis template.

This module offers functions to download public macro-finance time series
from FRED and quickly generate summary statistics and exploratory visualizations.
It is designed as a starting point for new analyses; customize the helpers
with domain-specific logic as needed.
"""

from datetime import datetime
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import seaborn as sns

# Visualization defaults
sns.set_theme(style="whitegrid")


def fetch_fred_series(series: Dict[str, str], start: str = "2000-01-01", end: str | None = None) -> pd.DataFrame:
    """Download multiple FRED series.

    Args:
        series: Mapping of friendly column names to FRED series identifiers.
        start: Start date in YYYY-MM-DD format.
        end: End date in YYYY-MM-DD format. Defaults to today when omitted.

    Returns:
        DataFrame indexed by date with columns in the provided order.
    """

    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    frames: List[pd.Series] = []
    for label, fred_id in series.items():
        ts = web.DataReader(fred_id, "fred", start=start, end=end)
        ts = ts.rename(columns={fred_id: label})
        frames.append(ts)

    combined = pd.concat(frames, axis=1)
    return combined


def summarize_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    """Compute exploratory summary statistics for time series data."""

    summary = df.describe().T
    summary["missing_pct"] = df.isna().mean() * 100
    summary["start_date"] = df.apply(lambda col: col.first_valid_index())
    summary["end_date"] = df.apply(lambda col: col.last_valid_index())
    return summary


def plot_time_series(df: pd.DataFrame, title: str = "Macro & Market Time Series") -> plt.Figure:
    """Line chart of all series in the frame."""

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend(title="Series", bbox_to_anchor=(1.05, 1), loc="upper left")
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, title: str = "Correlation (monthly freq)") -> plt.Figure:
    """Correlation heatmap after monthly resampling to align frequencies."""

    monthly = df.resample("M").mean()
    corr = monthly.corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_distribution(df: pd.DataFrame, columns: Iterable[str] | None = None) -> plt.Figure:
    """Histogram and KDE for selected columns."""

    cols = list(columns) if columns is not None else list(df.columns)
    fig, axes = plt.subplots(len(cols), 1, figsize=(8, 3 * len(cols)))
    if len(cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, cols):
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
    fig.tight_layout()
    return fig


def run_quick_eda() -> None:
    """Example workflow that fetches US macro and markets data and saves outputs."""

    fred_series = {
        "cpi": "CPIAUCSL",  # US CPI (Index 1982-1984=100)
        "unemployment_rate": "UNRATE",  # Civilian unemployment rate
        "fed_funds_rate": "FEDFUNDS",  # Effective federal funds rate
        "sp500": "SP500"  # S&P 500 index
    }

    df = fetch_fred_series(fred_series, start="2010-01-01")
    summary = summarize_timeseries(df)
    summary.to_csv("data/processed/summary.csv")

    fig1 = plot_time_series(df)
    fig1.savefig("figures/time_series.png", dpi=200)

    fig2 = plot_correlation_heatmap(df)
    fig2.savefig("figures/correlation.png", dpi=200)

    fig3 = plot_distribution(df, columns=["cpi", "unemployment_rate", "fed_funds_rate"])
    fig3.savefig("figures/distributions.png", dpi=200)

    print("Exploratory analysis complete. Outputs saved to data/processed and figures/")


if __name__ == "__main__":
    run_quick_eda()
