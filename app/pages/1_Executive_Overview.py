<<<<<<< HEAD
import plotly.express as px
import streamlit as st

from utils import (
    add_page_style,
    format_currency,
    format_pct,
    get_metric_value,
    load_data,
)


st.set_page_config(page_title="Executive Overview", layout="wide")
add_page_style()
data = load_data()

st.title("Executive Overview")
st.caption("High-level snapshot of FMCG sales performance, profitability, budget achievement, and forecast outlook.")

kpi = data["executive_dashboard_kpi"]
insights = data["executive_insights"]
monthly = data["monthly_kpi"]
category = data["category_kpi"]
channel = data["channel_kpi"]
region = data["region_kpi"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net Revenue", format_currency(get_metric_value(kpi, "Net Revenue")))
c2.metric("Profit", format_currency(get_metric_value(kpi, "Profit")))
c3.metric("Profit Margin", format_pct(get_metric_value(kpi, "Profit Margin")))
c4.metric("Next 6M Forecast", format_currency(get_metric_value(kpi, "Next 6-Month Forecast Revenue")))

c5, c6, c7, c8 = st.columns(4)
c5.metric("COGS Ratio", format_pct(get_metric_value(kpi, "COGS Ratio")))
c6.metric("Marketing Ratio", format_pct(get_metric_value(kpi, "Marketing Spend Ratio")))
c7.metric(
    "Revenue Budget Achievement",
    format_pct(get_metric_value(kpi, "Latest Year Revenue Budget Achievement")),
)
c8.metric("Forecast Test MAPE", format_pct(get_metric_value(kpi, "Forecast Test MAPE")))

st.markdown("## Business Insights")

if not insights.empty:
    cols = st.columns(3)
    for idx, row in insights.iterrows():
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="insight-box">
                    <b>{row['insight_title']}</b><br>
                    <span class="muted">{row['insight_text']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("## Performance Trends")

if not monthly.empty:
    monthly_sorted = monthly.sort_values(["Year", "Month"])

    fig = px.line(
        monthly_sorted,
        x="Year_Month",
        y="net_revenue",
        markers=True,
        title="Monthly Net Revenue Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        monthly_sorted,
        x="Year_Month",
        y="profit",
        markers=True,
        title="Monthly Profit Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Revenue Breakdown")

b1, b2 = st.columns(2)

with b1:
    if not category.empty:
        fig = px.bar(
            category.sort_values("net_revenue", ascending=False),
            x="Product_Category",
            y="net_revenue",
            title="Net Revenue by Product Category",
        )
        st.plotly_chart(fig, use_container_width=True)

with b2:
    if not channel.empty:
        fig = px.bar(
            channel.sort_values("net_revenue", ascending=False),
            x="Sales_Channel",
            y="net_revenue",
            title="Net Revenue by Sales Channel",
        )
        st.plotly_chart(fig, use_container_width=True)

if not region.empty:
    fig = px.bar(
        region.sort_values("net_revenue", ascending=False),
        x="Region",
        y="net_revenue",
        title="Net Revenue by Region",
    )
    st.plotly_chart(fig, use_container_width=True)
=======
import plotly.express as px
import streamlit as st

from utils import (
    add_page_style,
    format_currency,
    format_pct,
    get_metric_value,
    load_data,
)


st.set_page_config(page_title="Executive Overview", layout="wide")
add_page_style()
data = load_data()

st.title("Executive Overview")
st.caption("High-level snapshot of FMCG sales performance, profitability, budget achievement, and forecast outlook.")

kpi = data["executive_dashboard_kpi"]
insights = data["executive_insights"]
monthly = data["monthly_kpi"]
category = data["category_kpi"]
channel = data["channel_kpi"]
region = data["region_kpi"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net Revenue", format_currency(get_metric_value(kpi, "Net Revenue")))
c2.metric("Profit", format_currency(get_metric_value(kpi, "Profit")))
c3.metric("Profit Margin", format_pct(get_metric_value(kpi, "Profit Margin")))
c4.metric("Next 6M Forecast", format_currency(get_metric_value(kpi, "Next 6-Month Forecast Revenue")))

c5, c6, c7, c8 = st.columns(4)
c5.metric("COGS Ratio", format_pct(get_metric_value(kpi, "COGS Ratio")))
c6.metric("Marketing Ratio", format_pct(get_metric_value(kpi, "Marketing Spend Ratio")))
c7.metric(
    "Revenue Budget Achievement",
    format_pct(get_metric_value(kpi, "Latest Year Revenue Budget Achievement")),
)
c8.metric("Forecast Test MAPE", format_pct(get_metric_value(kpi, "Forecast Test MAPE")))

st.markdown("## Business Insights")

if not insights.empty:
    cols = st.columns(3)
    for idx, row in insights.iterrows():
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="insight-box">
                    <b>{row['insight_title']}</b><br>
                    <span class="muted">{row['insight_text']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("## Performance Trends")

if not monthly.empty:
    monthly_sorted = monthly.sort_values(["Year", "Month"])

    fig = px.line(
        monthly_sorted,
        x="Year_Month",
        y="net_revenue",
        markers=True,
        title="Monthly Net Revenue Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        monthly_sorted,
        x="Year_Month",
        y="profit",
        markers=True,
        title="Monthly Profit Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Revenue Breakdown")

b1, b2 = st.columns(2)

with b1:
    if not category.empty:
        fig = px.bar(
            category.sort_values("net_revenue", ascending=False),
            x="Product_Category",
            y="net_revenue",
            title="Net Revenue by Product Category",
        )
        st.plotly_chart(fig, use_container_width=True)

with b2:
    if not channel.empty:
        fig = px.bar(
            channel.sort_values("net_revenue", ascending=False),
            x="Sales_Channel",
            y="net_revenue",
            title="Net Revenue by Sales Channel",
        )
        st.plotly_chart(fig, use_container_width=True)

if not region.empty:
    fig = px.bar(
        region.sort_values("net_revenue", ascending=False),
        x="Region",
        y="net_revenue",
        title="Net Revenue by Region",
    )
    st.plotly_chart(fig, use_container_width=True)
>>>>>>> e24fd67 (update)
