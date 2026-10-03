# Data Science, AI & Analytics Portfolio

Welcome to my Data Science, AI, and Analytics portfolio. This repository showcases academic projects demonstrating practical experience in data science, statistical analysis, machine learning, generative AI, time-series forecasting, database management, public health analytics, and aviation analytics.

## Technical Skills

- **Programming & Databases:** Python, SQL, PostgreSQL, SAS, R, MATLAB
- **Machine Learning & Statistics:** Predictive Modeling, Linear Regression, Polynomial Regression, Ridge, Lasso, Elastic Net, Decision Trees, Time-Series Forecasting
- **Artificial Intelligence:** Large Language Models (LLMs), Claude API Integration, Multi-Agent Systems, Natural-Language Routing, Prompt Engineering
- **Data Science:** Data Cleaning, Data Integration, Exploratory Data Analysis, Feature Selection, Statistical Analysis, Model Evaluation, Data Visualization
- **Software & Tools:** WEKA, RStudio, psycopg2, pytest, tabulate

---

# Academic Projects

## 1. AI-Assisted Web Credibility Scorer

Developed an enhanced automated system for evaluating the credibility of web sources by combining rule-based scoring, webpage-level evidence, and an optional Claude LLM layer.

### Key Accomplishments

- Enhanced a Python-based credibility scoring algorithm using URL and webpage-level signals.
- Evaluated authorship, publication dates, references, peer-review indicators, corrections, retractions, HTTPS usage, DOI patterns, and publisher reputation.
- Improved handling of `.edu` websites and preprint repositories.
- Integrated Claude as an additional LLM-based credibility assessment layer.
- Evaluated the system using 24 URLs.
- Reduced Mean Absolute Error (MAE) from **0.143 to 0.091**.
- Increased credibility band accuracy from **62.5% to 83.3%**.
- Reduced worst individual prediction error from **0.410 to 0.230**.
- Used calibration analysis to compare predicted and expected credibility scores.

**Technologies:** Python, Claude LLM, API Integration, Rule-Based Algorithms, Web Analysis, Data Visualization, Model Evaluation

---

## 2. Persona Orchestrator – Multi-Agent AI System

Developed a Python-based multi-agent AI system capable of creating persistent personas, processing natural-language commands, and generating conversations between AI agents.

### Key Accomplishments

- Created and stored persistent personas using Markdown files.
- Developed natural-language routing for persona creation, selection, conversations, and participant resolution.
- Designed agents capable of maintaining assigned roles throughout multi-turn conversations.
- Implemented conversation history and downloadable transcripts.
- Supported adjustable conversation lengths and multiple participants.
- Integrated both offline and live Claude language-model functionality.
- Implemented bounded conversation history to control context size.
- Developed automated tests using `pytest`.
- Achieved **45 passing automated tests** covering agents, conversations, personas, LLM functionality, routing, and error handling.

**Technologies:** Python, Generative AI, Claude LLM, Multi-Agent Systems, Natural-Language Processing, Prompt Engineering, pytest

---

## 3. PostgreSQL Transaction Management & Database Operations

Developed a Python application that connects to a PostgreSQL relational database and performs transaction-controlled SQL operations.

### Key Accomplishments

- Connected Python applications to PostgreSQL using `psycopg2`.
- Executed SQL `INSERT`, `DELETE`, and `SELECT` operations.
- Managed related Product, Stock, and Depot records.
- Implemented transaction isolation.
- Used `COMMIT` and `ROLLBACK` operations to maintain transaction integrity.
- Implemented exception handling and database connection cleanup.
- Retrieved database records and displayed query results using `tabulate`.

**Technologies:** Python, SQL, PostgreSQL, psycopg2, Relational Databases, Transaction Management

---

## 4. Cardiovascular Predictive Modeling

Analyzed National Health and Nutrition Examination Survey (NHANES) data from 2021–2023 to investigate whether dietary intake could predict cholesterol and blood pressure.

### Key Accomplishments

- Integrated dietary, blood pressure, cholesterol, and demographic datasets.
- Worked with an initial combined dataset containing **7,801 participants and 208 variables**.
- Examined protein, sugar, fat, and fiber as cardiovascular predictors.
- Performed exploratory data analysis using correlation matrices and Pearson correlations.
- Developed Linear Regression and Multiple Linear Regression models.
- Implemented Polynomial Regression to investigate nonlinear relationships.
- Developed Ridge, Lasso, and Elastic Net regularization models.
- Evaluated models using Mean Squared Error (MSE) and R².
- Polynomial Regression produced an R² of **0.0514** for blood pressure, the highest reported R² among the tested blood-pressure models.
- Identified opportunities for future modeling using age, BMI, sodium intake, physical activity, genetics, and lifestyle factors.

**Technologies:** Python, NHANES, Predictive Modeling, Regression, Regularization, EDA, Statistical Analysis

---

## 5. COVID-19 Time-Series Forecasting

Analyzed World Health Organization COVID-19 case data across European countries from 2020–2022 to evaluate different forecasting methods.

### Key Accomplishments

- Filtered WHO data to include European observations.
- Aggregated COVID-19 case data into a univariate time series.
- Examined trends, volatility, non-stationarity, and weekly patterns.
- Developed a persistence baseline forecasting model.
- Developed an ARIMA forecasting model.
- Implemented Holt-Winters Exponential Smoothing.
- Used an **80/20 chronological train/test split**.
- Evaluated model performance using MAE and RMSE.
- Found that the baseline persistence model generated the lowest error among the tested approaches.
- Identified SARIMA, machine learning, and external predictors as potential future improvements.

**Technologies:** Python, Time-Series Analysis, ARIMA, Exponential Smoothing, Forecasting, MAE, RMSE

---

## 6. Flight Delay Classification

Developed a J48 decision-tree classifier using U.S. commercial aviation data to investigate factors associated with flight delays.

### Key Accomplishments

- Prepared a sample containing **300 flight records**.
- Examined scheduled departure time, airline carrier, origin, destination, and flight distance.
- Built a J48 decision-tree classifier using WEKA.
- Evaluated the model using **10-fold cross-validation**.
- Achieved **59.33% classification accuracy**.
- Identified scheduled departure time as the variable selected by the resulting decision tree.
- Identified weather, airport traffic, aircraft availability, and seasonal factors as potential additional predictors.

**Technologies:** WEKA, J48 Decision Trees, Machine Learning, Classification, Cross-Validation

---

## 7. Airline Market Entry Analysis

Analyzed airline traffic and route performance to identify flight-delay patterns, profitability, and potential market-entry opportunities.

### Key Accomplishments

- Identified **12,595 delayed flights** in the analyzed dataset.
- Compared delay patterns across airport sizes.
- Evaluated airline routes using revenue and profitability.
- Identified the **SLC ↔ TWF** roundtrip as the highest-revenue and highest-profit route in the analysis.
- Identified additional routes for potential future investment.
- Proposed additional analysis involving empty-seat costs and route optimization.
- Identified revenue and passenger-volume forecasting as potential future modeling opportunities.

**Technologies:** Data Analysis, Aviation Analytics, Profitability Analysis, Route Analysis, Business Analytics

---

## 8. National Survey Data Analysis

Analyzed National Health and Nutrition Examination Survey (NHANES) data to examine relationships among depression, cigarette smoking, physical activity, and age.

### Key Accomplishments

- Cleaned and analyzed national health survey data.
- Applied stratified sampling methods.
- Examined smoking patterns among depressed young men.
- Investigated physical-activity patterns among the study population.
- Used statistical visualizations to evaluate distributions and relationships among variables.

**Technologies:** SAS, NHANES, Public Health Analytics, Survey Analysis, Data Cleaning, Statistical Analysis

---

## 9. Public Health Forecasting

Analyzed publicly available COVID-19 mortality data to investigate short-term forecasting of deaths in France.

### Key Accomplishments

- Collected and organized weekly mortality data from the European COVID-19 Forecast Hub.
- Analyzed data covering March 2021 through March 2022.
- Applied statistical forecasting methods using MATLAB and RStudio.
- Compared forecasting approaches during periods of declining COVID-19 deaths.
- Examined the value of short-term forecasting for public health decision-making.

**Technologies:** MATLAB, R, RStudio, Time-Series Forecasting, Public Health Analytics

---

## 10. ReachOut Health Promotion Plan

Developed a public health promotion plan focused on expanding access to mental health services for high school students in rural Georgia.

### Key Accomplishments

- Developed a Text-4-Help support-line intervention.
- Planned telehealth and in-person counseling services.
- Developed peer-led outreach and group counseling initiatives.
- Planned household counseling services.
- Organized a youth mental health expo.
- Developed family and career service resources.
- Designed community-level engagement initiatives.

**Skills:** Public Health Program Planning, Health Promotion, Community Outreach, Intervention Design

---

# Portfolio Focus

These projects demonstrate experience throughout the data science lifecycle, including:

- Data collection and preparation
- Data cleaning and integration
- Exploratory data analysis
- Statistical analysis
- Predictive modeling
- Machine learning
- Generative AI and LLM integration
- Multi-agent AI development
- Time-series forecasting
- SQL and relational database management
- Model evaluation and calibration
- Automated software testing
- Data visualization
- Communication of analytical findings

My work applies these skills to real-world problems involving **public health, epidemiology, artificial intelligence, web credibility, aviation, business analytics, and database systems**.

---

# Education

### Master of Science in Data Science
**Pace University**  
May 2027

### Master of Public Health in Epidemiology
**Georgia State University**  
July 2023

### Bachelor of Science in Health Studies
**Texas Southern University**  
May 2020

