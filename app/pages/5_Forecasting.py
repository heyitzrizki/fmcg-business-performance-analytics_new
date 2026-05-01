import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import add_page_style, format_currency, format_pct, load_data


st.set_page_config(page_title="Forecasting", layout="wide")
add_page_style()
data = load_data()

st.title("Forecasting")
st.caption("Compare forecasting methods and review the short-term net revenue planning outlook.")

forecast_results = data["forecast_dashboard_data"]
forecast_metrics = data["forecast_metrics"]
future_forecast = data["future_forecast_dashboard_data"]
forecast_summary = data["forecast_summary"]
forecast_interpretation = data["forecast_interpretation"]
ml_interpretation = data["ml_forecast_interpretation"]

if forecast_results.empty or future_forecast.empty:
    st.error("Forecasting artifacts are missing. Run Notebook 04 and Notebook 05 first.")
    st.stop()


def summary_value(metric_name, default="-"):
    row = forecast_summary[forecast_summary["metric"] == metric_name]
    if row.empty:
        return default
    return row["value"].iloc[0]


best_model = summary_value("Best Forecast Model")
best_group = summary_value("Best Model Group")
test_mape = float(summary_value("Test MAPE", 0))
next_month = float(summary_value("Next Month Forecast Revenue", 0))
next_3m = float(summary_value("Next 3-Month Forecast Revenue", 0))
next_6m = float(summary_value("Next 6-Month Forecast Revenue", 0))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Best Forecast Model", str(best_model))
c2.metric("Model Group", str(best_group))
c3.metric("Test MAPE", format_pct(test_mape))
c4.metric("Next Month Forecast", format_currency(next_month))

c5, c6 = st.columns(2)
c5.metric("Next 3-Month Forecast", format_currency(next_3m))
c6.metric("Next 6-Month Forecast", format_currency(next_6m))

st.markdown(
    """
    <div class="warning-box">
        <b>Forecasting note:</b><br>
        The forecast is designed for business planning support. Planning bands are based on test-period error
        and should not be interpreted as formal statistical confidence intervals.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Test Period: Actual vs Forecast")

forecast_results["date"] = forecast_results["date"].astype("datetime64[ns]")
future_forecast["date"] = future_forecast["date"].astype("datetime64[ns]")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=forecast_results["date"],
        y=forecast_results["actual_net_revenue"],
        mode="lines+markers",
        name="Actual Net Revenue",
    )
)

forecast_col = (
    "final_best_model_forecast"
    if "final_best_model_forecast" in forecast_results.columns
    else "best_model_forecast"
)

fig.add_trace(
    go.Scatter(
        x=forecast_results["date"],
        y=forecast_results[forecast_col],
        mode="lines+markers",
        name=f"Forecast ({best_model})",
    )
)

fig.update_layout(
    title="Actual vs Forecast — Test Period",
    xaxis_title="Month",
    yaxis_title="Net Revenue USD",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## Forecast Model Comparison")

if not forecast_metrics.empty:
    metrics_plot = forecast_metrics.copy()
    metrics_plot["MAPE_pct"] = metrics_plot["MAPE"] * 100

    fig = px.bar(
        metrics_plot.sort_values("MAPE"),
        x="model",
        y="MAPE_pct",
        color="model_group" if "model_group" in metrics_plot.columns else None,
        text="MAPE_pct",
        title="Model Comparison by Test MAPE",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(yaxis_title="MAPE (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(forecast_metrics, use_container_width=True, hide_index=True)

st.markdown("## Future Forecast Outlook")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=future_forecast["date"],
        y=future_forecast["forecast_net_revenue"],
        mode="lines+markers",
        name="Forecast Net Revenue",
    )
)

if "upper_planning_band" in future_forecast.columns:
    fig.add_trace(
        go.Scatter(
            x=future_forecast["date"],
            y=future_forecast["upper_planning_band"],
            mode="lines",
            name="Upper Planning Band",
            line=dict(dash="dash"),
        )
    )

if "lower_planning_band" in future_forecast.columns:
    fig.add_trace(
        go.Scatter(
            x=future_forecast["date"],
            y=future_forecast["lower_planning_band"],
            mode="lines",
            name="Lower Planning Band",
            line=dict(dash="dash"),
        )
    )

if "budget_net_revenue" in future_forecast.columns:
    fig.add_trace(
        go.Scatter(
            x=future_forecast["date"],
            y=future_forecast["budget_net_revenue"],
            mode="lines+markers",
            name="Budget Outlook",
        )
    )

fig.update_layout(
    title="6-Month Net Revenue Forecast Outlook",
    xaxis_title="Month",
    yaxis_title="Net Revenue USD",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## Forecast vs Budget Outlook")

if "forecast_vs_budget_gap" in future_forecast.columns:
    fig = px.bar(
        future_forecast,
        x="Year_Month",
        y="forecast_vs_budget_gap",
        color="budget_gap_status",
        title="Forecast vs Budget Gap",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(future_forecast, use_container_width=True, hide_index=True)

st.markdown("## Interpretation")

if not forecast_interpretation.empty:
    for _, row in forecast_interpretation.iterrows():
        st.markdown(
            f"""
            <div class="insight-box">
                <b>{row['insight_type']}</b><br>
                <span class="muted">{row['insight']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

if not ml_interpretation.empty:
    with st.expander("ML benchmark interpretation"):
        st.dataframe(ml_interpretation, use_container_width=True, hide_index=True)