import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import add_page_style, format_currency, format_pct, load_data


st.set_page_config(page_title="Budget vs Actual", layout="wide")
add_page_style()
data = load_data()

st.title("Budget vs Actual")
st.caption("Review simulated budget achievement, monthly variance, and category-level performance gaps.")

budget = data["budget_dashboard_data"]
budget_year = data["budget_summary_year"]
category_budget = data["category_budget_summary"]
budget_assumptions = data["budget_assumptions"]
business_insights = data["business_insights"]

if budget.empty:
    st.error("budget_dashboard_data.csv is missing or empty.")
    st.stop()

st.markdown(
    """
    <div class="warning-box">
        <b>Budget simulation note:</b><br>
        Budget values in this project are simulated using prior-year same-month actual performance
        and target growth assumptions. They are used for business planning demonstration, not as real company budgets.
    </div>
    """,
    unsafe_allow_html=True,
)

latest_year = int(budget["Year"].max())
latest_year_df = budget_year[budget_year["Year"] == latest_year]

if not latest_year_df.empty:
    latest = latest_year_df.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue Achievement", format_pct(latest["revenue_budget_achievement"]))
    c2.metric("Profit Achievement", format_pct(latest["profit_budget_achievement"]))
    c3.metric("Revenue Variance", format_currency(latest["revenue_variance"]))
    c4.metric("Profit Variance", format_currency(latest["profit_variance"]))

below_budget_months = int((budget["budget_status"] == "Below Budget").sum())
total_months = len(budget)

c5, c6, c7 = st.columns(3)
c5.metric("Below-Budget Months", f"{below_budget_months}/{total_months}")
c6.metric("Latest Year", str(latest_year))
c7.metric("Budget Basis", "Prior-year same-month")

st.markdown("## Actual vs Budget Trend")

budget_sorted = budget.sort_values(["Year", "Month"])

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=budget_sorted["Year_Month"],
        y=budget_sorted["net_revenue"],
        mode="lines+markers",
        name="Actual Net Revenue",
    )
)
fig.add_trace(
    go.Scatter(
        x=budget_sorted["Year_Month"],
        y=budget_sorted["budget_net_revenue"],
        mode="lines+markers",
        name="Budget Net Revenue",
    )
)
fig.update_layout(
    title="Actual vs Budget Net Revenue",
    xaxis_title="Month",
    yaxis_title="USD",
)
st.plotly_chart(fig, use_container_width=True)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=budget_sorted["Year_Month"],
        y=budget_sorted["profit"],
        mode="lines+markers",
        name="Actual Profit",
    )
)
fig.add_trace(
    go.Scatter(
        x=budget_sorted["Year_Month"],
        y=budget_sorted["budget_profit"],
        mode="lines+markers",
        name="Budget Profit",
    )
)
fig.update_layout(
    title="Actual vs Budget Profit",
    xaxis_title="Month",
    yaxis_title="USD",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## Monthly Variance")

fig = px.bar(
    budget_sorted,
    x="Year_Month",
    y="revenue_variance",
    color="budget_status",
    title="Monthly Revenue Variance",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## Category Budget Performance")

if not category_budget.empty:
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            category_budget.sort_values("revenue_budget_achievement", ascending=False),
            x="Product_Category",
            y="revenue_budget_achievement",
            title="Revenue Budget Achievement by Category",
        )
        fig.update_layout(yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            category_budget.sort_values("revenue_variance", ascending=True),
            x="Product_Category",
            y="revenue_variance",
            title="Revenue Variance by Category",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(category_budget, use_container_width=True, hide_index=True)

st.markdown("## Budget Assumptions")

if not budget_assumptions.empty:
    st.dataframe(budget_assumptions, use_container_width=True, hide_index=True)

st.markdown("## Business Insights")

if not business_insights.empty:
    for _, row in business_insights.iterrows():
        st.markdown(
            f"""
            <div class="insight-box">
                <b>{row['insight_type']}</b><br>
                <span class="muted">{row['insight']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )