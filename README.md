# Exploratory Data Analysis Template (Finance & Economics)

This repository provides a lightweight starting point for analyzing public
finance and macroeconomic time series using Python. It shows how to
pull data from the Federal Reserve Economic Data (FRED) service, summarize it,
and generate quick visual diagnostics.

## Prerequisites

- Python 3.10+
- `pip install -r requirements.txt`
- A network connection for retrieving data from FRED via `pandas-datareader`.

## Project structure

```
├── data
│   ├── raw/            # Place any downloaded CSVs here
│   └── processed/      # Auto-generated summaries
├── figures/            # Auto-generated charts
├── notebooks/          # Space for Jupyter notebooks
└── src/eda_template.py # Reusable helper functions and example workflow
```

## Quickstart

Run the built-in workflow to fetch CPI, unemployment, Fed funds, and S&P 500
series from FRED, then save summary tables and charts:

```bash
python -m src.eda_template
```

Outputs will be written to `data/processed/summary.csv` and PNG figures under
`figures/`.

## Using the helpers in a notebook

1. Start Jupyter Lab/Notebook: `jupyter lab` or `jupyter notebook`.
2. Import the utilities and fetch any set of FRED series:

```python
from src.eda_template import (
    fetch_fred_series,
    summarize_timeseries,
    plot_time_series,
    plot_correlation_heatmap,
    plot_distribution,
)

fred_series = {
    "industrial_production": "INDPRO",
    "retail_sales": "RSAFS",
    "ten_year_treasury": "DGS10",
}

macro = fetch_fred_series(fred_series, start="2015-01-01")
summarize_timeseries(macro)
plot_time_series(macro, title="Macro indicators")
plot_correlation_heatmap(macro)
```

Feel free to replace the default series, add custom cleaning steps, or extend
the plotting helpers with more domain-specific visuals (e.g., rolling betas,
recession shading, or log returns).
