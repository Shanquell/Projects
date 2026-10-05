# Health Data Analytics & Predictive Modeling Projects

This repository contains two data science projects focused on analyzing
National Health and Nutrition Examination Survey (NHANES) data.

The projects demonstrate skills in data cleaning, data integration,
exploratory data analysis, statistical analysis, data visualization,
regression modeling, regularization, and predictive modeling.

---

## Projects

### 1. National Survey Data Analysis

#### Project Overview

This project analyzes data from the National Health and Nutrition
Examination Survey (NHANES) 2015–2016 to investigate relationships
between depression, cigarette smoking, and physical activity among
young men.

The analysis focuses on the following research questions:

- Does depression influence cigarette smoking among young men?
- Does depression influence physical activity?
- Which age groups are most affected by cigarette smoking?

#### Data Source

Data were obtained from several NHANES survey components, including:

- Depression Screener (DPQ)
- Physical Activity Questionnaire (PAQ)
- Smoking Questionnaire (SMQ)
- Demographic Data (DEMO)

The datasets were merged and filtered to focus on male participants
experiencing symptoms of depression.

#### Key Variables

| Variable | Description |
|----------|-------------|
| DPQ020 | Frequency of feeling down, depressed, or hopeless |
| PAQ670 | Days participating in moderate physical activity |
| SMQ040 | Current cigarette smoking status |
| SMD650 | Number of cigarettes smoked per day |
| LPA | Physical activity status |
| SMOKE | Smoking status |
| RIAGENDR | Gender |
| RIDAGEYR | Age |

#### Methods

The analysis included:

- Data cleaning
- Dataset integration
- Participant filtering
- Descriptive statistics
- Frequency distributions
- Exploratory data analysis
- Bar charts
- Pie charts
- Histograms

#### Key Findings

Among the depressed young men included in the analysis:

- 79.59% were classified as smokers.
- 20.41% were classified as non-smokers.
- 68.33% had normal physical activity levels.
- 31.67% had low physical activity levels.

The smoking age distribution also showed concentrations around the
mid-30s and early 60s.

#### Conclusion

The analysis found a strong prevalence of smoking within the selected
sample of depressed young men. However, most participants maintained
normal physical activity levels despite experiencing depression.

These findings demonstrate how national health survey data can be used
to explore relationships among mental health, lifestyle behaviors, and
demographic characteristics.

---

### 2. Cardiovascular Predictive Modeling

#### Project Overview

This project uses NHANES 2021–2023 data to investigate whether dietary
intake can help predict cardiovascular health outcomes.

The analysis evaluates whether the following dietary variables are
associated with blood pressure and cholesterol:

- Protein
- Sugar
- Dietary fiber
- Total fat

#### Data Preparation

NHANES cholesterol, blood pressure, dietary, and demographic datasets
were merged into a combined dataset containing:

- 7,801 participants
- 208 variables

Seven primary variables were selected for modeling:

- Cholesterol
- Systolic blood pressure
- Diastolic blood pressure
- Protein
- Sugar
- Fiber
- Fat

Missing continuous values were handled using mean imputation, and a
sample of 200 participants was used for the final modeling analysis.

#### Exploratory Data Analysis

Pearson correlation analysis was used to examine relationships between
dietary variables and cardiovascular outcomes.

The analysis found generally weak linear relationships.

Protein and fiber showed the strongest associations with cholesterol,
while protein and fat showed the strongest relationships with blood
pressure.

Most correlation p-values were not statistically significant,
suggesting that dietary intake alone provided limited explanatory
power.

#### Predictive Models

The following regression models were evaluated:

- Simple Linear Regression
- Multiple Linear Regression
- Polynomial Regression
- Ridge Regression
- Lasso Regression
- Elastic Net Regression

Polynomial regression used degree 2 to investigate possible nonlinear
relationships.

Regularization models were also evaluated:

- Ridge: alpha = 1.0
- Lasso: alpha = 1.0
- Elastic Net: alpha = 1.0, L1 ratio = 0.2

#### Model Performance

##### Cholesterol Prediction

| Model | MSE | R² |
|------|-----:|---:|
| Multiple Linear Regression | 0.0458 | 0.0373 |
| Polynomial Regression | 0.0460 | 0.0325 |
| Ridge | 0.0538 | -0.2545 |
| Lasso | 0.0465 | -0.1712 |
| Elastic Net | 0.0463 | -0.7046 |

Multiple linear regression produced the best reported R² among these
cholesterol models, although its overall predictive power remained low.

##### Blood Pressure Prediction

| Model | MSE | R² |
|------|-----:|---:|
| Single Linear Regression | 0.0333 | 0.0026 |
| Multiple Linear Regression | 0.0388 | 0.0265 |
| Polynomial Regression | 0.0378 | 0.0514 |
| Ridge | 0.0382 | -0.7909 |
| Lasso | 0.0364 | -0.7046 |
| Elastic Net | 0.0364 | -0.7046 |

Polynomial regression achieved the highest R² for blood pressure,
suggesting that limited nonlinear relationships may exist between
dietary intake and cardiovascular outcomes.

#### Conclusion

The analysis found that sugar, protein, fiber, and fat had relatively
weak linear relationships with blood pressure and cholesterol.

Polynomial regression captured some nonlinear patterns, but overall
predictive performance remained limited.

The findings suggest that cardiovascular outcomes cannot be reliably
predicted using the selected dietary variables alone.

Future models could incorporate additional predictors such as:

- Age
- Body mass index (BMI)
- Sodium intake
- Physical activity
- Genetics
- Lifestyle behaviors
- Repeated blood pressure measurements

Larger sample sizes and more advanced machine learning approaches may
also improve predictive performance.

---

## Technologies and Tools

The projects demonstrate experience with:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Statistical analysis
- Exploratory data analysis
- Data visualization
- Regression modeling
- Predictive modeling
- Machine learning
- NHANES public health data

---

## Skills Demonstrated

- Data cleaning and preprocessing
- Merging multiple health datasets
- Missing-value handling
- Exploratory data analysis
- Descriptive statistics
- Correlation analysis
- Data visualization
- Feature selection
- Linear regression
- Polynomial regression
- Ridge regression
- Lasso regression
- Elastic Net regression
- Model evaluation using MSE and R²
- Interpretation of public health data
- Communicating analytical results

---

## Repository Structure

```text
health-data-projects/
│
├── national-survey-data-analysis/
│   ├── data/
│   ├── notebooks/
│   ├── figures/
│   └── report/
│
├── cardiovascular-predictive-modeling/
│   ├── data/
│   ├── notebooks/
│   ├── figures/
│   └── report/
│
└── README.md
