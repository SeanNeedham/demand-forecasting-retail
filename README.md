# Retail Demand Forecasting

**Python | statsmodels | Streamlit | 1,067,371 raw transactions | 5 SKUs forecast weekly**

A demand-planning workflow that runs from raw transaction data through to a live dashboard planners can actually use.

**[→ Open the live Streamlit app](https://demand-forecasting-retail-kg5mko7xnqxbjmzgcffz5y.streamlit.app/)**

---

## Executive Summary

### The Problem

Inventory and planning teams needed weekly demand forecasts, but the source data was not fit to forecast on. The Online Retail II workbook held over a million rows containing cancellations, stock adjustments, postage and fee lines, zero-price records, duplicate rows and a duplicated December 2010 overlap between worksheets. Forecasting it unaltered would have modelled administrative noise as if it were demand.

### The Solution

Clean to genuine merchandise demand, screen for forecastability, then test five methods per product.

- Reversed sales were matched to their **same-day cancellations** and removed as pairs — netting quantities alone would have left the demand signal distorted.
- Products were **screened before modelling** against history length, demand regularity and volatility, so effort went only where a forecast could be trusted.
- Models were evaluated on a **12-week time-based hold-out**, not a random sample, because a random split leaks future information into training.

### The Impact

- Produced a **per-product model recommendation** rather than one blanket method.
- Quantified planning risk per SKU using a single comparable error metric.
- Delivered the results as a **live Streamlit app** built around planning decisions, not model output.

## Dashboard Preview

![Retail Demand Forecasting Streamlit Dashboard](images/streamlit_dashboard.png)

## Key Operational Insights

### Weekly aggregation is the right grain; daily is not
Daily demand was highly volatile. Weekly aggregation produced a clear enough signal to model. This decision came before any forecasting and shaped everything after it.

### No single method wins across the range
The best model differed by product — a result that argues directly against standardising on one forecasting approach.

| Stock Code | Best model | WMAPE |
|---|---|---:|
| 84879 | Exponential smoothing | **26.62%** |
| 84077 | Exponential smoothing | 38.40% |
| 21212 | Holt trend | 41.55% |
| 85099B | Holt trend | 41.75% |
| 85123A | Naive baseline | **42.05%** |

85123A is best served by the naive baseline. The more complex methods did not improve out-of-sample accuracy for this SKU, reinforcing the importance of benchmarking sophisticated models against simple alternatives.

### Forecast accuracy and peak-demand risk are different
Products with more stable demand were generally easier to forecast, but peak-demand risk did not always align with average forecast error. 84879 and 84077 had the highest peak-to-average demand ratios while also achieving the two lowest WMAPE values. Their normal demand levels were relatively forecastable, but occasional extreme weeks still created inventory risk that the point forecast could not fully capture.

### WMAPE was chosen for a specific reason
MAE and RMSE were both calculated, but WMAPE was used to select models because it is comparable **across products with different demand volumes**. MAE on a high-volume SKU cannot be read against MAE on a lower-volume one.

### Demand is seasonal and the calendar is not clean
Demand strengthens through autumn and the pre-Christmas period. Some weeks around Christmas and New Year show reduced or zero trading — real gaps in the calendar rather than missing data, and they have to be treated as such.

### Demand is broad, not concentrated
Activity spread across a wide product range rather than clustering in a few SKUs. The **United Kingdom** accounted for the majority of total demand.

---

## Recommendations & Business Actions

**1. Set review frequency by forecast error, not by product value.**
Higher-WMAPE products warrant more frequent review and more cautious planning to limit both stockout and excess-inventory risk.

**2. Add stock protection for spike-prone products, specifically 84879 and 84077.**
The average weekly forecast will not absorb a surge on its own.

**3. Bring peak-season planning forward to before September.**
Demand strengthens across September to November, so forecast reviews need to precede that window rather than respond to it.

**4. Keep model selection at product level.**
The results show method performance varies by SKU. Re-run the comparison as new products enter scope rather than applying one default.

### Next steps
- Test additional forecasting methods.
- Introduce external drivers — promotions, holidays, pricing.
- Extend the approach across a larger product range.
- Move to rolling model validation.
- Automate forecast refreshes.
- Track forecast bias and service-level outcomes over time.

### What this analysis cannot tell you
- Forecasts rest on historical demand alone; promotions, price changes and holiday effects are not modelled as drivers.
- Only five screened products were forecast, so the results do not generalise to the full catalogue.
- The screen deliberately excluded sparse and highly volatile products — those remain unforecast, not proven unforecastable.
- Records with missing Customer IDs were retained for demand purposes, so customer-level conclusions cannot be drawn from this dataset.

---

## The Dataset & Metrics

**Source:** [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) — approximately two years of retail transactions across two annual worksheets. **1,067,371 raw rows.**

**Fields used**

- Invoice number
- Product StockCode
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

**Metrics measured**

- Weekly aggregated demand per product
- **MAE** — mean absolute error
- **RMSE** — root mean squared error
- **WMAPE** — weighted mean absolute percentage error *(primary metric)*
- Demand regularity: share of available weeks with demand
- Demand volatility per product

**Product screening criteria**

| Criterion | Threshold |
|---|---|
| History available | ≥ 52 weeks |
| Weeks with demand | ≥ 70% |
| Volatility | Moderate — extremes excluded |

Five high-volume products passed and were carried into modelling.

---

## Methodology & Technical Stack

**Stack:** Python · pandas · NumPy · Matplotlib · statsmodels · Streamlit · Jupyter Notebook · Git / GitHub

### 1. Data understanding and cleaning — `01_data_understanding_and_cleaning.ipynb`
- Removed exact duplicate transaction rows.
- Resolved the duplicated December 2010 overlap between worksheets.
- Excluded negative quantities representing cancellations, returns and stock adjustments.
- Excluded zero and negative prices.
- Matched and removed positive sales fully reversed by same-day cancellations.
- Excluded non-merchandise StockCodes — postage, fees, discounts, manual adjustments.
- **Retained** missing Customer IDs where product, quantity and date remained valid.
- **Retained** legitimate high-volume customer orders rather than stripping statistical outliers automatically.

Result: 1,004,262 cleaned transaction rows representing positive merchandise-order demand.

### 2. Exploratory analysis — `02_exploratory_analysis.ipynb`
Compared daily against weekly aggregation, examined seasonality and trading gaps, assessed demand spread across the product range, and screened products for forecastability.

### 3. Forecasting — `03_forecasting_models.ipynb`
Five methods tested per product: naive baseline, four-week moving average, seasonal naive, simple exponential smoothing, Holt's trend method. Evaluated on a **12-week time-based test period**, scored on MAE, RMSE and WMAPE.

### 4. Business insights — `04_business_insights_and_recommendations.ipynb`
Converted model performance into planning risk ratings and inventory actions.

### 5. Streamlit application — `streamlit_app/app.py`
Built for non-technical stakeholders. Users can select any of the five forecast products, view the recommended method, see forecast error and planning risk, review historical weekly demand, compare actual against forecast, compare methods side by side, and read product-specific planning actions.

### Repository structure

```text
demand-forecasting-retail/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_forecasting_models.ipynb
│   └── 04_business_insights_and_recommendations.ipynb
│
├── streamlit_app/
│   ├── app.py
│   └── data/
│
├── requirements.txt
├── README.md
└── .gitignore
```
