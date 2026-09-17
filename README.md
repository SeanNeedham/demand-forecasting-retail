# Retail Demand Forecasting

[View the live Streamlit app](https://demand-forecasting-retail-kg5mko7xnqxbjmzgcffz5y.streamlit.app/)

Interactive dashboard for weekly demand trends, forecast performance and inventory-planning actions.

## Project Overview

This project analyses historical retail transaction data to understand product demand patterns and build weekly forecasts for selected products.

The aim was to create a practical demand-planning workflow that could help inventory and planning teams:

- understand demand trends and seasonality
- identify products suitable for forecasting
- compare different forecasting approaches
- select the most accurate model for each product
- highlight products with higher planning risk
- turn forecast results into practical inventory recommendations

The project covers the full analytics workflow from raw-data investigation and cleaning through exploratory analysis, forecasting, business recommendations and an interactive Streamlit application.

## Business Questions

The analysis was designed to answer:

1. How does product demand change over time?
2. Is weekly or daily demand more suitable for forecasting?
3. Which products have sufficient history and regular demand to forecast reliably?
4. Which forecasting method performs best for each selected product?
5. Which products carry the greatest forecast and demand-volatility risk?
6. What actions could demand and inventory planners take from the results?

## Dataset

The project uses the Online Retail II transaction dataset covering approximately two years of retail activity.

The raw workbook contained 1,004,262 transaction rows across two annual worksheets.

Key fields included:

- invoice number
- product StockCode
- product description
- quantity
- invoice date
- unit price
- customer ID
- country

The raw data required investigation before it could be used for demand forecasting because it included cancellations, stock adjustments, duplicate records, overlapping worksheets, zero-price transactions and other non-product activity.

## Data Preparation

The cleaning process focused on creating a dataset representing positive merchandise-order demand.

Key decisions included:

- removed exact duplicate transaction rows
- resolved the duplicated December 2010 overlap between worksheets
- excluded negative quantities representing cancellations, returns and stock adjustments
- excluded zero and negative prices
- identified and removed positive sales that were fully reversed by matching same-day cancellations
- excluded non-merchandise StockCodes such as postage, fees, discounts and manual adjustments
- retained missing Customer IDs where valid product, quantity and date information remained
- retained legitimate high-volume customer orders rather than removing statistical outliers automatically

The final cleaned dataset contained approximately **1 million valid transaction rows**.

## Exploratory Analysis

The exploratory analysis focused on understanding demand behaviour before selecting forecasting methods.

Key findings included:

- daily demand was highly volatile, while weekly aggregation produced a clearer signal
- demand showed recurring strength during the autumn and pre-Christmas period
- some weeks around Christmas and New Year had reduced or zero trading activity
- demand was spread across a broad product range rather than being dominated by only a few SKUs
- products differed significantly in demand regularity and volatility
- the United Kingdom accounted for the majority of total demand

To keep the modelling stage focused, products were screened using:

- at least 52 weeks of available history
- demand in at least 70% of available weeks
- moderate rather than extreme demand volatility

Five high-volume products were selected for forecasting.

## Forecasting Approach

Five forecasting methods were tested for each selected product:

1. Naive baseline
2. Four-week moving average
3. Seasonal naive
4. Simple exponential smoothing
5. Holt's trend method

A 12-week time-based test period was used so the models were evaluated on future demand rather than a random sample.

Model performance was assessed using:

- MAE
- RMSE
- WMAPE

WMAPE was used as the primary model-selection metric because it allows forecast error to be compared across products with different demand volumes.

## Forecasting Results

The best-performing model differed by product.

| Stock Code | Best Model | WMAPE |
|---|---|---:|
| 21212 | Holt trend | 41.55% |
| 84077 | Exponential smoothing | 38.40% |
| 84879 | Exponential smoothing | 26.62% |
| 85099B | Holt trend | 41.75% |
| 85123A | Naive baseline | 42.05% |

The results showed that no single forecasting method performed best across every SKU.

Products with more stable demand were generally easier to forecast, while products with larger short-term demand spikes produced higher forecast error.

## Business Recommendations

### 1. Use forecast reliability to guide inventory decisions
Products with higher forecast error should be reviewed more frequently and planned with greater caution to reduce the risk of stockouts or excess inventory.

### 2. Protect high-volatility products
Products with large demand surges, particularly 84879 and 84077, should receive additional stock protection rather than relying only on the average weekly forecast.

### 3. Prepare earlier for peak season
Demand strengthens during the autumn and pre-Christmas period, so forecast reviews and inventory planning should increase ahead of September to November.

## Streamlit Application

An interactive Streamlit application was built to make the forecasting results easier to use for non-technical stakeholders.

The app allows users to:

- select one of the five forecasted products
- view the recommended forecasting method
- see forecast error and planning risk
- review historical weekly demand
- compare actual demand against the selected forecast
- compare forecasting methods
- view product-specific planning actions

The interface is designed around business decisions rather than technical model output.

## Tools Used

- Python
- pandas
- NumPy
- Matplotlib
- statsmodels
- Streamlit
- Jupyter Notebook
- Git / GitHub

## Project Structure

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

## Key Skills Demonstrated

This project demonstrates:

- data quality investigation and cleaning
- time-series aggregation and exploratory analysis
- demand segmentation and product selection
- forecasting model comparison
- MAE, RMSE and WMAPE evaluation
- translating model results into inventory-planning actions
- stakeholder-focused dashboard design
- end-to-end project delivery from raw data to interactive application

## Next Steps

Possible future improvements include:

- testing additional forecasting methods
- adding external drivers such as promotions, holidays or pricing
- extending the approach to a larger product range
- introducing rolling model validation
- adding automated forecast refreshes
- tracking forecast bias and service-level outcomes over time