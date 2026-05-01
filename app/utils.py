from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_data():
    """Load all dashboard-ready processed artifacts."""
    files = {
        "executive_dashboard_kpi": "executive_dashboard_kpi.csv",
        "executive_insights": "executive_insights.csv",
        "monthly_kpi": "monthly_kpi.csv",
        "category_kpi": "category_kpi.csv",
        "channel_kpi": "channel_kpi.csv",
        "region_kpi": "region_kpi.csv",
        "country_kpi": "country_kpi.csv",
        "promotion_kpi": "promotion_kpi.csv",
        "product_kpi": "product_kpi.csv",
        "sales_dashboard_data": "sales_dashboard_data.csv",
        "pnl_dashboard_summary": "pnl_dashboard_summary.csv",
        "pnl_monthly": "pnl_monthly.csv",
        "pnl_category": "pnl_category.csv",
        "pnl_channel": "pnl_channel.csv",
        "pnl_region": "pnl_region.csv",
        "pnl_waterfall": "pnl_waterfall.csv",
        "negative_profit_summary": "negative_profit_summary.csv",
        "budget_dashboard_data": "budget_dashboard_data.csv",
        "budget_summary_year": "budget_summary_year.csv",
        "category_budget_summary": "category_budget_summary.csv",
        "budget_assumptions": "budget_assumptions.csv",
        "business_insights": "business_insights.csv",
        "forecast_dashboard_data": "forecast_dashboard_data.csv",
        "forecast_metrics": "forecast_metrics.csv",
        "future_forecast_dashboard_data": "future_forecast_dashboard_data.csv",
        "forecast_summary": "forecast_summary.csv",
        "forecast_interpretation": "forecast_interpretation.csv",
        "ml_forecast_interpretation": "ml_forecast_interpretation.csv",
        "product_portfolio": "product_portfolio.csv",
        "category_portfolio": "category_portfolio.csv",
        "portfolio_segment_summary": "portfolio_segment_summary.csv",
        "project_narrative_summary": "project_narrative_summary.csv",
    }

    data = {}
    missing = []

    for key, filename in files.items():
        path = PROCESSED_DIR / filename
        if path.exists():
            data[key] = pd.read_csv(path)
        else:
            data[key] = pd.DataFrame()
            missing.append(filename)

    for key in [
        "sales_dashboard_data",
        "forecast_dashboard_data",
        "future_forecast_dashboard_data",
    ]:
        if not data[key].empty:
            for col in ["Order_Date", "date"]:
                if col in data[key].columns:
                    data[key][col] = pd.to_datetime(data[key][col], errors="coerce")

    data["_missing_files"] = missing
    return data


def get_metric_value(kpi_df: pd.DataFrame, metric_name: str, default=np.nan):
    if kpi_df.empty or "metric" not in kpi_df.columns or "value" not in kpi_df.columns:
        return default

    row = kpi_df[kpi_df["metric"] == metric_name]
    if row.empty:
        return default

    value = row["value"].iloc[0]

    try:
        return float(value)
    except (ValueError, TypeError):
        return value


def format_currency(value, decimals=0):
    if pd.isna(value):
        return "-"
    return f"${value:,.{decimals}f}"


def format_number(value, decimals=0):
    if pd.isna(value):
        return "-"
    return f"{value:,.{decimals}f}"


def format_pct(value, decimals=1):
    if pd.isna(value):
        return "-"
    return f"{value * 100:.{decimals}f}%"


def format_ratio(value, decimals=2):
    if pd.isna(value):
        return "-"
    return f"{value:.{decimals}f}x"


def safe_divide(numerator, denominator):
    if denominator in [0, None] or pd.isna(denominator):
        return np.nan
    return numerator / denominator


def render_kpi_card(label, value, help_text=None):
    st.metric(label=label, value=value, help=help_text)


def add_page_style():
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1450px;
                padding-top: 1.8rem;
            }
            .section-card {
                background: rgba(255,255,255,0.035);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 1.05rem 1.15rem;
                margin-bottom: 1rem;
            }
            .section-title {
                font-size: 1.15rem;
                font-weight: 700;
                margin-bottom: 0.55rem;
            }
            .muted {
                color: #AAB3C2;
                font-size: 0.95rem;
                line-height: 1.65;
            }
            .small-note {
                color: #AAB3C2;
                font-size: 0.88rem;
                line-height: 1.55;
            }
            .insight-box {
                background: rgba(255,255,255,0.035);
                border-left: 4px solid rgba(78,166,153,0.9);
                border-radius: 12px;
                padding: 0.85rem 1rem;
                margin-bottom: 0.75rem;
            }
            .warning-box {
                background: rgba(255, 193, 7, 0.08);
                border: 1px solid rgba(255, 193, 7, 0.22);
                border-radius: 14px;
                padding: 1rem;
                margin-bottom: 1rem;
                color: #F4E4B3;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_sales_filters(df: pd.DataFrame):
    if df.empty:
        return df

    filtered = df.copy()

    with st.sidebar:
        st.header("Filters")

        if "Year" in filtered.columns:
            years = sorted(filtered["Year"].dropna().unique())
            selected_years = st.multiselect("Year", years, default=years)
            filtered = filtered[filtered["Year"].isin(selected_years)]

        for col, label in [
            ("Region", "Region"),
            ("Country", "Country"),
            ("Product_Category", "Product Category"),
            ("Brand", "Brand"),
            ("Sales_Channel", "Sales Channel"),
            ("Customer_Type", "Customer Type"),
            ("Promotion_Type", "Promotion Type"),
        ]:
            if col in filtered.columns:
                options = sorted(filtered[col].dropna().astype(str).unique())
                selected = st.multiselect(label, options, default=options)
                filtered = filtered[filtered[col].astype(str).isin(selected)]

    return filtered


def summarize_filtered_sales(df: pd.DataFrame):
    if df.empty:
        return {
            "net_revenue": np.nan,
            "profit": np.nan,
            "units_sold": np.nan,
            "profit_margin": np.nan,
            "avg_discount": np.nan,
            "avg_selling_price": np.nan,
        }

    net_revenue = df["Net_Revenue_USD"].sum()
    profit = df["Profit_USD"].sum()
    units = df["Units_Sold"].sum()

    return {
        "net_revenue": net_revenue,
        "profit": profit,
        "units_sold": units,
        "profit_margin": safe_divide(profit, net_revenue),
        "avg_discount": df["Discount_Pct"].mean() / 100 if df["Discount_Pct"].max() > 1 else df["Discount_Pct"].mean(),
        "avg_selling_price": safe_divide(net_revenue, units),
    }