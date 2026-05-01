import plotly.express as px
import streamlit as st

from utils import (
    add_page_style,
    apply_sales_filters,
    format_currency,
    format_number,
    format_pct,
    load_data,
    summarize_filtered_sales,
)


st.set_page_config(page_title="Sales Performance", layout="wide")
add_page_style()
data = load_data()

st.title("Sales Performance")
st.caption("Analyze sales performance across time, region, country, channel, category, brand, product, and promotion type.")

sales = data["sales_dashboard_data"]

if sales.empty:
    st.error("sales_dashboard_data.csv is missing or empty.")
    st.stop()

filtered = apply_sales_filters(sales)
summary = summarize_filtered_sales(filtered)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net Revenue", format_currency(summary["net_revenue"]))
c2.metric("Profit", format_currency(summary["profit"]))
c3.metric("Units Sold", format_number(summary["units_sold"]))
c4.metric("Profit Margin", format_pct(summary["profit_margin"]))

c5, c6 = st.columns(2)
c5.metric("Average Discount", format_pct(summary["avg_discount"]))
c6.metric("Average Selling Price", format_currency(summary["avg_selling_price"], decimals=2))

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.markdown("## Sales Trend")

monthly = (
    filtered.groupby(["Year", "Month", "Year_Month"], as_index=False)
    .agg(
        net_revenue=("Net_Revenue_USD", "sum"),
        profit=("Profit_USD", "sum"),
        units_sold=("Units_Sold", "sum"),
    )
    .sort_values(["Year", "Month"])
)

fig = px.line(
    monthly,
    x="Year_Month",
    y="net_revenue",
    markers=True,
    title="Filtered Monthly Net Revenue",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## Sales Breakdown")

c1, c2 = st.columns(2)

with c1:
    category = (
        filtered.groupby("Product_Category", as_index=False)
        .agg(net_revenue=("Net_Revenue_USD", "sum"), profit=("Profit_USD", "sum"))
        .sort_values("net_revenue", ascending=False)
    )
    fig = px.bar(category, x="Product_Category", y="net_revenue", title="Revenue by Product Category")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    channel = (
        filtered.groupby("Sales_Channel", as_index=False)
        .agg(net_revenue=("Net_Revenue_USD", "sum"), profit=("Profit_USD", "sum"))
        .sort_values("net_revenue", ascending=False)
    )
    fig = px.bar(channel, x="Sales_Channel", y="net_revenue", title="Revenue by Sales Channel")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    promo = (
        filtered.groupby("Promotion_Type", as_index=False)
        .agg(
            net_revenue=("Net_Revenue_USD", "sum"),
            profit=("Profit_USD", "sum"),
            avg_discount=("Discount_Pct", "mean"),
        )
        .sort_values("net_revenue", ascending=False)
    )
    fig = px.bar(promo, x="Promotion_Type", y="net_revenue", title="Revenue by Promotion Type")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    country = (
        filtered.groupby("Country", as_index=False)
        .agg(net_revenue=("Net_Revenue_USD", "sum"), profit=("Profit_USD", "sum"))
        .sort_values("net_revenue", ascending=False)
        .head(15)
    )
    fig = px.bar(country, x="Country", y="net_revenue", title="Top Countries by Revenue")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Top Products")

top_products = (
    filtered.groupby(["Product_Category", "Brand", "Product_Name", "SKU"], as_index=False)
    .agg(
        net_revenue=("Net_Revenue_USD", "sum"),
        profit=("Profit_USD", "sum"),
        units_sold=("Units_Sold", "sum"),
    )
    .sort_values("net_revenue", ascending=False)
    .head(20)
)

st.dataframe(top_products, use_container_width=True, hide_index=True)