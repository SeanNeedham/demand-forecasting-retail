from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

WEEKLY_FILE = DATA_DIR / "weekly_forecast_data.csv"
FORECAST_FILE = DATA_DIR / "final_forecast_results.csv"
MODEL_FILE = DATA_DIR / "model_summary.csv"

weekly_data = pd.read_csv(
    WEEKLY_FILE,
    parse_dates=["invoice_date"]
)

forecast_results = pd.read_csv(
    FORECAST_FILE,
    parse_dates=["invoice_date"]
)

model_summary = pd.read_csv(
    MODEL_FILE
)

st.title("Retail Demand Forecasting")
st.caption(
    "Weekly demand outlook, forecast performance and planning actions"
)

st.subheader("Performance Overview")

product_options = (
    weekly_data[
        ["stock_code", "description"]
    ]
    .drop_duplicates()
    .sort_values("stock_code")
)

product_options["label"] = (
    product_options["stock_code"].astype(str)
    + " | "
    + product_options["description"]
)

selected_label = st.selectbox(
    "Select product",
    product_options["label"]
)

selected_stock_code = selected_label.split(" | ")[0]

selected_model = model_summary[
    model_summary["stock_code"].astype(str)
    == selected_stock_code
].iloc[0]

selected_history = weekly_data[
    weekly_data["stock_code"].astype(str)
    == selected_stock_code
].sort_values("invoice_date")

average_weekly_demand = (
    selected_history["weekly_demand"].mean()
)

peak_weekly_demand = (
    selected_history["weekly_demand"].max()
)

peak_to_average_ratio = (
    peak_weekly_demand / average_weekly_demand
)

best_wmape = min(
    selected_model["baseline_WMAPE"],
    selected_model["moving_avg_WMAPE"],
    selected_model["seasonal_WMAPE"],
    selected_model["exp_smoothing_WMAPE"],
    selected_model["holt_WMAPE"]
)

if best_wmape < 30:
    planning_risk = "Lower"
elif best_wmape < 40:
    planning_risk = "Moderate"
else:
    planning_risk = "Higher"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Recommended forecast method",
    selected_model["best_model"]
)

col2.metric(
    "Forecast error",
    f"{best_wmape:.1f}%"
)

col3.metric(
    "Planning risk",
    planning_risk
)

col4.metric(
    "Average weekly demand",
    f"{average_weekly_demand:,.0f}"
)

col5.metric(
    "Peak vs normal demand",
    f"{peak_to_average_ratio:.1f}x"
)

st.subheader("Demand & Outlook")

st.line_chart(
    selected_history.set_index("invoice_date")["weekly_demand"]
)

st.caption(
    "Historical weekly demand trend"
)

product_forecast = forecast_results[
    forecast_results["stock_code"].astype(str)
    == selected_stock_code
].sort_values("invoice_date")

forecast_chart = (
    product_forecast[
        ["invoice_date", "weekly_demand", "final_forecast"]
    ]
    .set_index("invoice_date")
    .rename(columns={
        "weekly_demand": "Actual demand",
        "final_forecast": "Forecast"
    })
)

st.line_chart(forecast_chart)

st.caption(
    f"Test-period forecast using {selected_model['best_model']}"
)

if planning_risk == "Lower":
    outlook_text = (
        "Forecast performance is relatively reliable for this product, "
        "so the forecast can be used with greater confidence for short-term planning."
    )
elif planning_risk == "Moderate":
    outlook_text = (
        "Forecast performance is reasonably stable, but weekly demand can still vary. "
        "Use the forecast alongside recent demand changes when planning stock."
    )
else:
    outlook_text = (
        "Forecast uncertainty is higher for this product. "
        "Use the forecast as a planning guide and review demand frequently before making stock decisions."
    )

st.info(outlook_text)

st.subheader("Forecast Performance")

st.write(
    f"**Recommended method:** {selected_model['best_model']} "
    f"with {best_wmape:.1f}% forecast error."
)

performance_data = pd.DataFrame({
    "Method": [
        "Naive baseline",
        "4-week moving average",
        "Seasonal naive",
        "Exponential smoothing",
        "Holt trend"
    ],
    "Forecast error": [
        selected_model["baseline_WMAPE"],
        selected_model["moving_avg_WMAPE"],
        selected_model["seasonal_WMAPE"],
        selected_model["exp_smoothing_WMAPE"],
        selected_model["holt_WMAPE"]
    ]
})

fig, ax = plt.subplots(figsize=(8, 4))

performance_plot = performance_data.sort_values(
    "Forecast error",
    ascending=False
)

bars = ax.barh(
    performance_plot["Method"],
    performance_plot["Forecast error"]
)

ax.set_title("Forecast Error by Method")
ax.set_xlabel("Forecast Error (%)")
ax.set_ylabel("")

ax.bar_label(
    bars,
    labels=[
        f"{value:.1f}%"
        for value in performance_plot["Forecast error"]
    ],
    padding=3
)

plt.tight_layout()

st.pyplot(fig)

st.caption(
    "Lower forecast error indicates better performance for the selected product."
)

st.subheader("Planning Actions")

if planning_risk == "Higher":
    st.warning(
        "This product has higher forecast uncertainty. "
        "Review demand frequently and avoid relying on the forecast alone for stock decisions."
    )

elif planning_risk == "Moderate":
    st.info(
        "This product has moderate forecast uncertainty. "
        "Use the forecast alongside recent demand and stock-position checks."
    )

else:
    st.success(
        "This product has relatively lower forecast uncertainty. "
        "The forecast can be used with greater confidence for short-term planning."
    )
    

if peak_to_average_ratio >= 5:
    st.warning(
        "Peak demand risk is high. Consider additional stock protection "
        "and closer monitoring for sudden demand surges."
    )
elif peak_to_average_ratio >= 3:
    st.info(
        "Demand can rise well above normal weekly levels. "
        "Maintain some additional stock protection during higher-risk periods."
    )
else:
    st.success(
        "Peak demand risk is relatively controlled compared with the other selected products."
    )

st.info(
    "Demand typically strengthens during the autumn and pre-Christmas period. "
    "Increase forecast reviews and inventory planning ahead of September to November."
)

st.markdown("### Recommended Planning Focus")

st.write(
    f"""
    **Product:** {selected_label}

    **Planning approach:** Use **{selected_model['best_model']}** as the primary forecasting method.

    **Inventory focus:** {planning_risk} planning risk means stock decisions should be reviewed
    {"more frequently" if planning_risk == "Higher" else "regularly"}.

    **Peak demand:** Demand has previously reached **{peak_to_average_ratio:.1f}x** normal weekly levels.
    """
)
