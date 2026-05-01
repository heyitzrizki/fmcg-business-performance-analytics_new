import plotly.express as px
import streamlit as st

from utils import add_page_style, format_currency, format_number, format_pct, load_data


st.set_page_config(page_title="Product Portfolio", layout="wide")
add_page_style()
data = load_data()

st.title("Product Portfolio Strategy")
st.caption("Segment products and categories by revenue contribution, profitability, and strategic action.")

product_portfolio = data["product_portfolio"]
category_portfolio = data["category_portfolio"]
segment_summary = data["portfolio_segment_summary"]
negative_profit = data["negative_profit_summary"]

if product_portfolio.empty:
    st.error("product_portfolio.csv is missing or empty.")
    st.stop()

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Portfolio Logic</div>
        <div class="muted">
        Products and categories are segmented using revenue share and profit margin.
        The goal is to support portfolio decisions: which products to grow, improve, selectively invest in,
        or review for rationalization.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

segments = sorted(product_portfolio["portfolio_segment"].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Portfolio Segment",
    segments,
    default=segments,
)

filtered = product_portfolio[
    product_portfolio["portfolio_segment"].isin(selected_segments)
].copy()

total_sku = filtered["SKU"].nunique()
total_revenue = filtered["net_revenue"].sum()
total_profit = filtered["profit"].sum()
avg_margin = total_profit / total_revenue if total_revenue else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("SKU Count", format_number(total_sku))
c2.metric("Net Revenue", format_currency(total_revenue))
c3.metric("Profit", format_currency(total_profit))
c4.metric("Profit Margin", format_pct(avg_margin))

st.markdown("## Portfolio Segment Summary")

if not segment_summary.empty:
    fig = px.bar(
        segment_summary.sort_values("net_revenue", ascending=False),
        x="portfolio_segment",
        y="net_revenue",
        title="Net Revenue by Portfolio Segment",
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        segment_summary.sort_values("profit", ascending=False),
        x="portfolio_segment",
        y="profit",
        title="Profit by Portfolio Segment",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(segment_summary, use_container_width=True, hide_index=True)

st.markdown("## Product Revenue-Margin Matrix")

if not filtered.empty:
    fig = px.scatter(
        filtered,
        x="revenue_share",
        y="profit_margin",
        size="net_revenue",
        color="portfolio_segment",
        hover_data=[
            "Product_Category",
            "Brand",
            "Product_Name",
            "SKU",
            "net_revenue",
            "profit",
            "strategic_action",
        ],
        title="Product Portfolio Matrix",
    )
    fig.update_layout(
        xaxis_tickformat=".2%",
        yaxis_tickformat=".1%",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## Category Portfolio")

if not category_portfolio.empty:
    fig = px.scatter(
        category_portfolio,
        x="revenue_share",
        y="profit_margin",
        size="net_revenue",
        color="portfolio_segment",
        hover_data=[
            "Product_Category",
            "net_revenue",
            "profit",
            "strategic_action",
        ],
        title="Category Portfolio Matrix",
    )
    fig.update_layout(
        xaxis_tickformat=".1%",
        yaxis_tickformat=".1%",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(category_portfolio, use_container_width=True, hide_index=True)

st.markdown("## Product Portfolio Table")

display_cols = [
    "Product_Category",
    "Brand",
    "Product_Name",
    "SKU",
    "net_revenue",
    "profit",
    "profit_margin",
    "revenue_share",
    "portfolio_segment",
    "strategic_action",
]

existing_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[existing_cols].sort_values("net_revenue", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.markdown("## Loss-Making Combination Review")

if not negative_profit.empty:
    st.markdown(
        """
        <div class="section-card">
            <div class="muted">
            Loss-making combinations may indicate issues in discounting, logistics cost, marketing efficiency,
            pricing, or product-channel fit.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(negative_profit.head(30), use_container_width=True, hide_index=True)