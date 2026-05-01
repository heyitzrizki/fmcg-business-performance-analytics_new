import streamlit as st

from utils import add_page_style, load_data


st.set_page_config(
    page_title="FMCG Business Performance Analytics",
    page_icon="📊",
    layout="wide",
)

add_page_style()
data = load_data()

st.title("FMCG Business Performance & P&L Analytics Dashboard")
st.caption(
    "Business planning dashboard for sales performance, profitability, budget variance, forecasting, and product portfolio strategy."
)

if data["_missing_files"]:
    with st.expander("Missing processed files", expanded=False):
        st.warning(
            "Some processed files were not found. Run notebooks 02–05 before deploying the dashboard."
        )
        st.write(data["_missing_files"])

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Project Overview</div>
        <div class="muted">
        This dashboard simulates how an FMCG business planning analyst can connect sales, cost,
        marketing, budget, forecast, and product portfolio data into one decision-support system.
        The goal is not only to report sales, but to explain where performance comes from,
        whether the business is profitable, whether it is meeting plan, and what categories or
        products should be prioritized.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Business Performance</div>
            <div class="muted">
            Track net revenue, profit, margin, sales channel contribution, regional performance,
            and category-level business drivers.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Planning & Forecasting</div>
            <div class="muted">
            Compare actual performance against simulated budget targets and generate a short-term
            revenue forecast for business planning discussions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Portfolio Strategy</div>
            <div class="muted">
            Segment products and categories into Core Growth, Margin Improvement,
            Niche Opportunity, and Review / Rationalize groups.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("## Dashboard Modules")

st.markdown(
    """
    1. **Executive Overview** — high-level business performance snapshot.  
    2. **Sales Performance** — sales, category, channel, country, promotion, and product analysis.  
    3. **P&L & Margin Analysis** — profitability structure, cost ratios, and margin pressure.  
    4. **Budget vs Actual** — simulated budget achievement and variance review.  
    5. **Forecasting** — model comparison, short-term revenue forecast, and planning outlook.  
    6. **Product Portfolio** — revenue-margin segmentation and strategic action guidance.
    """
)

st.markdown(
    """
    <div class="warning-box">
        <b>Important note:</b><br>
        This is a portfolio prototype using a public FMCG-style dataset. Budget values are simulated
        using prior-year same-month performance and target growth assumptions. Forecast planning bands
        are based on test error and should not be interpreted as formal financial guidance.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Methodology Summary")

st.markdown(
    """
    - Business KPI engineering for revenue, cost, margin, marketing efficiency, and contribution profit.
    - P&L analysis across month, product category, channel, and region.
    - Simulated budget planning using prior-year same-month performance and growth assumptions.
    - Forecast model comparison using Seasonal Naive, Moving Average, Holt-Winters, SARIMA, and a leakage-safe ML benchmark.
    - Product portfolio segmentation using revenue share and profit margin.
    """
)