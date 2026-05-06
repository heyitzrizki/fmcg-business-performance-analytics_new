import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    add_page_style,
    format_currency,
    format_pct,
    load_data,
)


st.set_page_config(page_title="P&L & Margin Analysis", layout="wide")
add_page_style()
data = load_data()

st.title("P&L & Margin Analysis")
st.caption("Analyze profitability structure, margin pressure, cost ratios, and loss-making transaction patterns.")

pnl_summary = data["pnl_dashboard_summary"]
pnl_waterfall = data["pnl_waterfall"]
pnl_monthly = data["pnl_monthly"]
pnl_category = data["pnl_category"]
pnl_channel = data["pnl_channel"]
pnl_region = data["pnl_region"]
negative_profit = data["negative_profit_summary"]


def get_pnl_metric(metric_name):
    if pnl_summary.empty:
        return None
    row = pnl_summary[pnl_summary["metric"] == metric_name]
    if row.empty:
        return None
    try:
        return float(row["value"].iloc[0])
    except Exception:
        return row["value"].iloc[0]


c1, c2, c3, c4 = st.columns(4)
c1.metric("Gross Sales", format_currency(get_pnl_metric("Gross Sales")))
c2.metric("Net Revenue", format_currency(get_pnl_metric("Net Revenue")))
c3.metric("Gross Profit", format_currency(get_pnl_metric("Gross Profit")))
c4.metric("Profit", format_currency(get_pnl_metric("Profit")))

c5, c6, c7, c8 = st.columns(4)
c5.metric("Gross Margin", format_pct(get_pnl_metric("Gross Margin")))
c6.metric("Contribution Margin", format_pct(get_pnl_metric("Contribution Margin")))
c7.metric("Profit Margin", format_pct(get_pnl_metric("Profit Margin")))
c8.metric("Marketing Spend", format_currency(get_pnl_metric("Marketing Spend")))

st.markdown(
    """
    <div class="warning-box">
        <b>How to read this page:</b><br>
        This page separates revenue, direct costs, marketing spend, logistics costs, and profit.
        It helps identify whether business performance is driven by topline growth, cost efficiency,
        or margin pressure.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Overall P&L Waterfall")

if not pnl_waterfall.empty:
    fig = go.Figure(
        go.Waterfall(
            name="P&L",
            orientation="v",
            measure=pnl_waterfall["type"],
            x=pnl_waterfall["step"],
            y=pnl_waterfall["amount"],
            text=[f"${x:,.0f}" for x in pnl_waterfall["amount"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Overall P&L Waterfall",
        yaxis_title="USD",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Margin Trend")

if not pnl_monthly.empty:
    pnl_monthly_sorted = pnl_monthly.sort_values(["Year", "Month"])

    fig = px.line(
        pnl_monthly_sorted,
        x="Year_Month",
        y=["gross_margin", "contribution_margin", "profit_margin"],
        markers=True,
        title="Monthly Margin Trend",
    )
    fig.update_layout(yaxis_tickformat=".1%")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Category and Channel Profitability")

c1, c2 = st.columns(2)

with c1:
    if not pnl_category.empty:
        fig = px.bar(
            pnl_category.sort_values("profit_margin", ascending=False),
            x="Product_Category",
            y="profit_margin",
            title="Profit Margin by Product Category",
        )
        fig.update_layout(yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

with c2:
    if not pnl_channel.empty:
        fig = px.bar(
            pnl_channel.sort_values("profit_margin", ascending=False),
            x="Sales_Channel",
            y="profit_margin",
            title="Profit Margin by Sales Channel",
        )
        fig.update_layout(yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("## Cost Pressure")

c3, c4 = st.columns(2)

with c3:
    if not pnl_category.empty:
        cost_df = pnl_category[
            ["Product_Category", "cogs_ratio", "logistics_ratio", "marketing_ratio"]
        ].copy()

        cost_long = cost_df.melt(
            id_vars="Product_Category",
            value_vars=["cogs_ratio", "logistics_ratio", "marketing_ratio"],
            var_name="Cost Type",
            value_name="Ratio",
        )

        fig = px.bar(
            cost_long,
            x="Product_Category",
            y="Ratio",
            color="Cost Type",
            barmode="group",
            title="Cost Ratios by Product Category",
        )
        fig.update_layout(yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

with c4:
    if not pnl_region.empty:
        fig = px.bar(
            pnl_region.sort_values("logistics_ratio", ascending=False),
            x="Region",
            y="logistics_ratio",
            title="Logistics Cost Ratio by Region",
        )
        fig.update_layout(yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("## Negative Profit Review")

if not negative_profit.empty:
    st.markdown(
        """
        <div class="section-card">
            <div class="muted">
            This table highlights product-channel-promotion combinations that generated negative profit.
            These rows can be reviewed for pricing, promotion efficiency, logistics cost, or product mix issues.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_cols = [
        "Product_Category",
        "Sales_Channel",
        "Promotion_Type",
        "loss_transaction_count",
        "net_revenue",
        "total_loss",
        "avg_profit_margin",
        "avg_discount_pct",
        "marketing_spend",
        "logistics_cost",
    ]

    existing_cols = [c for c in display_cols if c in negative_profit.columns]
    st.dataframe(
        negative_profit[existing_cols].head(30),
        use_container_width=True,
        hide_index=True,
    )

st.markdown("## Category P&L Table")

if not pnl_category.empty:
    st.dataframe(pnl_category, use_container_width=True, hide_index=True)

