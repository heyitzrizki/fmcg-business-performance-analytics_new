# FMCG Business Performance Analytics Dashboard

A business analytics dashboard for monitoring FMCG commercial performance, analyzing revenue and profitability, tracking budget variance, and supporting data-driven business planning decisions.

The main question this project answers is:

**What is driving business performance, where are the gaps, and what actions should management consider?**

## Project Overview

FMCG businesses operate across multiple products, categories, regions, and sales channels. Business teams need to monitor revenue, cost, margin, budget achievement, and performance variance in a clear and structured way.

This project simulates how a business planning or commercial analytics team can turn sales and financial performance data into an executive-ready dashboard. The focus is not only on reporting numbers, but also on helping users understand performance drivers and planning implications.

## Business Problem

Commercial teams often need to answer questions such as:

- Is revenue growing or declining?
- Which categories, products, regions, or channels are driving performance?
- Is actual revenue above or below budget?
- Which areas have the largest positive or negative variance?
- Which products generate high revenue but weak margin?
- Which channels are profitable and which require management attention?
- What actions should be considered for future planning?

This project addresses those questions through a structured FMCG performance analytics workflow.

## Data Scope

The project is designed around typical FMCG commercial performance data, including:

- Date or reporting month
- Region or market
- Sales channel
- Product category
- Product or SKU
- Revenue
- Budget or target
- Units sold
- Cost of goods sold
- Gross profit
- Gross margin
- Budget variance
- Variance percentage

If synthetic data are used, the dataset should be interpreted as simulated business data for portfolio demonstration purposes.

## Analytics Workflow

The project follows a business performance analytics workflow:

1. Load sales, budget, product, category, region, and channel data
2. Clean and standardize the dataset
3. Create monthly reporting periods
4. Calculate business KPIs such as revenue, gross profit, gross margin, budget variance, and target achievement
5. Analyze revenue trends and growth patterns
6. Compare actual performance against budget
7. Identify top-performing and underperforming categories, products, channels, and regions
8. Analyze profitability and margin performance
9. Present insights in a business-friendly dashboard

## Key Metrics

The dashboard focuses on practical business KPIs:

- **Total Revenue**: total sales generated
- **Revenue Growth**: change in revenue over time
- **Gross Profit**: revenue minus cost of goods sold
- **Gross Margin**: gross profit divided by revenue
- **Budget Variance**: actual revenue minus budget revenue
- **Variance %**: budget variance relative to budget
- **Target Achievement**: actual performance divided by budget
- **Revenue Share**: contribution of a category, channel, product, or region to total revenue

## Dashboard Focus

The dashboard is designed for non-technical business users and may include the following sections:

- **Executive Overview**: total revenue, gross profit, gross margin, budget variance, and key business takeaway
- **Revenue Performance**: monthly revenue trend, growth, category contribution, region contribution, and channel contribution
- **Budget vs Actual**: actual performance compared with budget or target
- **Profitability Analysis**: gross profit and margin by category, channel, product, or region
- **Category and Channel Insights**: ranking of business segments and identification of performance drivers
- **Business Recommendations**: summary of key issues, possible actions, and planning implications

## Repository Structure

```text
.
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── notebooks/
├── src/
├── outputs/
├── requirements.txt
└── README.md
```

Adjust the structure if the repository uses different file names or folders.

## How to Run

Clone the repository:

```bash
git clone https://github.com/heyitzrizki/fmcg-business-performance-analytics_new.git
cd fmcg-business-performance-analytics_new
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app/streamlit_app.py
```

If the dashboard file uses a different name, adjust the command accordingly.

## Example Business Insights

The dashboard is designed to surface insights such as:

- Revenue is growing, but growth is concentrated in only a few categories.
- A category may have high revenue but weaker margin.
- Some channels may drive volume but reduce profitability due to promotion or distribution cost.
- Budget underperformance may be concentrated in specific regions or products.
- Margin pressure may require pricing, promotion, or cost review.
- High-margin categories may deserve more planning attention even if their revenue share is smaller.

## Business Value

This project demonstrates the ability to translate raw commercial and financial data into business-ready insights. It connects revenue, budget, cost, margin, variance, category performance, channel performance, and management implications in one dashboard.

The project is relevant for roles in business planning, commercial analytics, sales analytics, financial analysis, and data-driven strategy.

## Limitations

This project is a portfolio prototype. If synthetic or simplified data are used, the results should be interpreted as simulated business analysis rather than actual company performance. Business recommendations require validation with real company context, stakeholder input, and operational constraints.

## Tech Stack

Python, Pandas, NumPy, Plotly, Streamlit, Excel/CSV data processing, business KPI engineering, and dashboard storytelling.