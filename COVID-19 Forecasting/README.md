# COVID-19 Time Series & Public Health Forecasting

This repository contains two public health forecasting projects focused on the
COVID-19 pandemic. The projects use time-series analysis and statistical
forecasting techniques to examine COVID-19 cases across Europe and forecast
COVID-19 deaths in France.

These projects demonstrate practical experience with epidemiological data,
time-series analysis, forecasting, statistical modeling, model evaluation,
and public health research.

---

## Projects

### 1. COVID-19 Case Time Series Forecasting

#### Project Overview

This project analyzes COVID-19 cases across European countries from 2020–2022
and evaluates several time-series forecasting approaches.

The goal was to determine how effectively historical COVID-19 case data could
be used to predict future cases and to compare the forecasting performance of
multiple models.

#### Data Source

COVID-19 case data were obtained from the World Health Organization (WHO).

The dataset was:

- Loaded from a CSV file
- Filtered to European countries
- Aggregated to create a single European COVID-19 case time series
- Restricted to the 2020–2022 study period

The final time series contained 156 observations.

#### Exploratory Data Analysis

Exploratory analysis was used to investigate patterns in COVID-19 cases.

The analysis included:

- Time-series visualization
- 7-day rolling mean
- 7-day rolling standard deviation
- Trend analysis
- Seasonal decomposition
- Examination of residual patterns

The time series demonstrated substantial volatility and several major pandemic
waves. Rolling statistics indicated changes in both the mean and variance over
time, while seasonal decomposition identified trend, seasonal, and residual
components.

#### Forecasting Models

Three forecasting approaches were evaluated:

- Baseline persistence model
- ARIMA
- Holt-Winters Exponential Smoothing

The baseline model predicted that future observations would equal the most
recently observed value.

ARIMA was used to model temporal dependencies through autoregressive and moving
average components.

The exponential smoothing model incorporated additive trend and seasonal
components.

#### Train/Test Strategy

The data were divided chronologically using an:

- 80% training set
- 20% testing set

Maintaining chronological order prevented future observations from being used
to predict earlier observations.

#### Model Evaluation

Forecasting performance was evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

| Model | MAE | RMSE | Rank |
|---|---:|---:|---:|
| Baseline | 237,423.31 | 303,287.07 | 1 |
| ARIMA | 610,071.99 | 738,376.84 | 2 |
| Exponential Smoothing | 2,411,650.58 | 2,657,136.06 | 3 |

#### Results

The baseline model achieved the lowest MAE and RMSE and therefore produced the
best forecasting performance.

ARIMA ranked second and produced smoother forecasts that did not fully capture
sharp fluctuations in COVID-19 cases.

Exponential smoothing produced the largest errors and had difficulty modeling
the sudden spikes and extreme variability in the time series.

#### Limitations

Major limitations included:

- No ARIMA hyperparameter tuning
- No exponential smoothing hyperparameter tuning
- No external predictors
- Potential reporting delays
- Potential underreporting
- Differences in testing practices between countries

External variables such as vaccination rates, government policies, mobility,
and emerging variants could potentially improve future forecasting models.

#### Future Improvements

Future work could evaluate:

- SARIMA
- Optimized ARIMA models
- Machine learning forecasting techniques
- Additional external predictors
- Alternative seasonal models

---

## 2. Forecasting COVID-19 Deaths in France

### Project Overview

This public health forecasting project evaluates multiple statistical modeling
frameworks for short-term forecasting of COVID-19 deaths in France.

The study generated forecasts 1–4 weeks ahead using weekly COVID-19 mortality
data.

A total of 1,760 forecasts were conducted across:

- 10 models
- 44 dates
- Four modeling frameworks
- 1–4 week forecasting horizons

### Data Source

Weekly confirmed COVID-19 death data for France were obtained from the
European COVID-19 Forecast Hub.

The study analyzed weekly deaths between March 5, 2021 and March 4, 2022.

A 10-week calibration period was used to generate retrospective sequential
forecasts.

### Modeling Frameworks

The project evaluated four major forecasting approaches:

#### ARIMA

Autoregressive Integrated Moving Average models were used to identify temporal
patterns within COVID-19 mortality data.

Model parameters were selected using the `auto.arima` methodology and AICc
criteria.

#### Generalized Additive Models

Generalized Additive Models (GAMs) were used to capture nonlinear relationships
between time and COVID-19 deaths using smooth functions.

#### Simple Linear Regression

Simple linear regression was evaluated using time as the primary covariate.

#### Sub-Epidemic Modeling

Sub-epidemic models represented epidemic trajectories as combinations of
overlapping sub-epidemics.

Both top-ranked and ensemble sub-epidemic approaches were evaluated.

### Forecasting Strategy

Models generated retrospective forecasts at four horizons:

- 1 week ahead
- 2 weeks ahead
- 3 weeks ahead
- 4 weeks ahead

The forecasting strategy allowed performance to be compared as the prediction
horizon increased.

### Performance Metrics

Models were evaluated using:

- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- 95% Prediction Interval Coverage
- Weighted Interval Score (WIS)

These metrics evaluated both forecast accuracy and forecast uncertainty.

### ARIMA Performance

ARIMA achieved the strongest overall forecasting performance.

| Forecast Horizon | MSE | MAE | 95% PI Coverage | WIS |
|---|---:|---:|---:|---:|
| 1 Week | 60,876.37 | 156.89 | 74.42% | 109.71 |
| 2 Weeks | 95,556.95 | 191.76 | 75.00% | 138.21 |
| 3 Weeks | 132,746.65 | 223.58 | 73.98% | 166.85 |
| 4 Weeks | 143,148.87 | 241.41 | 73.75% | 179.16 |

ARIMA consistently performed strongly across the 1–4 week forecasting
horizons.

Although GAM produced good model fits during several calibration periods,
ARIMA provided better overall forecasting performance.

### Results

The study found that ARIMA outperformed the individual sub-epidemic,
sub-epidemic ensemble, GAM, and simple linear regression approaches for
short-term forecasting.

The results demonstrate the value of time-series forecasting for anticipating
changes in infectious disease mortality and supporting short-term public
health planning.

### Limitations

The project identified several limitations.

The spatial-wave sub-epidemic framework could not be successfully evaluated,
limiting comparisons between modeling approaches.

ARIMA also has limitations for:

- Long-term forecasting
- Predicting epidemic turning points
- Computational requirements

Future research could further evaluate GAM and spatial-wave sub-epidemic
approaches and compare them with ARIMA.

---

# Comparison of the Two Projects

These projects demonstrate two approaches to COVID-19 forecasting.

| Project | Outcome | Geographic Area | Main Models | Best Model |
|---|---|---|---|---|
| COVID-19 Case Time Series Forecasting | COVID-19 Cases | Europe | Baseline, ARIMA, Exponential Smoothing | Baseline |
| Public Health Forecasting | COVID-19 Deaths | France | ARIMA, GAM, Linear Regression, Sub-Epidemic Models | ARIMA |

Together, the projects demonstrate how model performance can vary substantially
depending on the forecasting problem, data structure, forecast horizon, and
modeling strategy.

---

# Technologies and Tools

The projects demonstrate experience with:

- Python
- R / RStudio
- MATLAB
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Time-series analysis
- ARIMA modeling
- Exponential smoothing
- Generalized Additive Models
- Linear regression
- Epidemiological modeling
- Statistical forecasting
- Public health data analysis

---

# Skills Demonstrated

- Time-series preprocessing
- Exploratory data analysis
- Time-based train/test splitting
- Rolling statistics
- Seasonal decomposition
- Trend and seasonality analysis
- ARIMA forecasting
- Exponential smoothing
- Generalized Additive Models
- Regression modeling
- Sub-epidemic modeling
- Multi-horizon forecasting
- Model comparison
- Forecast evaluation
- Public health data interpretation
- Data visualization
- Scientific communication

---

# Suggested Repository Structure

```text
covid-19-forecasting/
│
├── covid-case-time-series/
│   ├── data/
│   ├── notebooks/
│   ├── figures/
│   └── report/
│
├── france-public-health-forecasting/
│   ├── data/
│   ├── code/
│   ├── figures/
│   └── report/
│
├── requirements.txt
└── README.md
```

---

# Running the Python Time-Series Project

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate the Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```bash
pip install pandas numpy matplotlib statsmodels scikit-learn jupyter
```

## 5. Start Jupyter Notebook

```bash
jupyter notebook
```

Open the project notebook and execute the cells in order.

> Additional R and MATLAB dependencies may be required to reproduce the
> France COVID-19 mortality forecasting project.

---

# Key Takeaways

These projects demonstrate that selecting an appropriate forecasting model
depends heavily on the structure and behavior of the time series.

For the European COVID-19 case analysis, the simple persistence baseline
outperformed ARIMA and exponential smoothing.

For the France mortality forecasting study, ARIMA demonstrated the strongest
overall short-term forecasting performance across the 1–4 week forecast
horizons.

The projects also highlight the importance of comparing sophisticated
forecasting techniques against simple baseline models rather than assuming
that greater model complexity will automatically produce better predictions.

---

# Future Work

Potential improvements include:

- SARIMA modeling
- Automated hyperparameter optimization
- Cross-validation designed for time-series data
- Additional machine learning forecasting models
- Inclusion of vaccination data
- Mobility and government policy variables
- Variant prevalence
- Improved uncertainty estimation
- Additional countries and geographic regions
- Longer forecasting periods
- Ensemble forecasting methods

---

# Authors

**Shanquell Thompson-Sanders**

**Tatyana Valteau** — Co-author, France COVID-19 mortality forecasting study

---

# Project Focus

**Data Science | Time Series Forecasting | Epidemiology | Statistical Modeling | Public Health Analytics | Machine Learning**
