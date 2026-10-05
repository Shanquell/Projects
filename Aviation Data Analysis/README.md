# Airline Analytics: Flight Delay Prediction & Market Entry Analysis

This repository contains two aviation data analytics projects focused on
operational performance, flight delays, profitability, and strategic
decision-making in the airline industry.

The projects demonstrate the use of data analytics and machine learning to
answer two different aviation business questions:

1. Can flight characteristics be used to predict whether a flight will be delayed?
2. Which airline routes provide attractive opportunities for a new airline investment?

---

## Projects

### 1. Flight Delay Classification

#### Project Overview

The Flight Delay Classification project evaluates whether flight
characteristics can be used to predict whether a commercial flight will be
delayed.

The analysis investigated the predictive value of:

- Scheduled departure time
- Airline carrier
- Origin airport
- Destination airport
- Flight distance

A **J48 decision-tree classifier** was created in WEKA and evaluated using
**10-fold cross-validation**.

---

### Dataset

The project used U.S. commercial flight data from 2007.

The original dataset contained:

- 30,000 flights
- 30 attributes

A subset of **300 flights** was selected for the classification analysis.

The primary variables retained for modeling were:

| Variable | Description |
|---|---|
| CRSDepTime | Scheduled departure time |
| UniqueCarrier | Airline carrier |
| Origin | Departure airport |
| Dest | Destination airport |
| Distance | Flight distance |
| Delayed | Flight delay status |

`Delayed` was designated as the target/class variable.

---

### Data Preparation

The dataset was reduced to variables considered relevant to predicting flight
delays.

The cleaned dataset was imported into WEKA, and `Delayed` was configured as
the class variable.

Ten-fold cross-validation divided the 300 observations into approximately 30
observations per fold, allowing each observation to be used for both training
and testing during different iterations.

---

### Machine Learning Model

The project used the **J48 Decision Tree** classifier in WEKA.

J48 builds a decision tree by selecting attributes that provide useful
separation between target classes and pruning unnecessary branches to reduce
overfitting.

The resulting model produced a very simple tree:

```text
CRSDepTime <= 12:59
    → Not Delayed

CRSDepTime > 12:59
    → Delayed
```

Scheduled departure time was therefore the only variable selected by the final
decision tree.

---

### Classification Results

The model correctly classified:

```text
178 of 300 flights
```

This resulted in an overall accuracy of:

```text
59.33%
```

#### Performance Metrics

| Metric | Result |
|---|---:|
| Correctly Classified | 178 |
| Incorrectly Classified | 122 |
| Accuracy | 59.33% |
| Misclassification Rate | 40.67% |
| Kappa Statistic | 0.0907 |
| Mean Absolute Error | 0.4786 |
| Root Mean Squared Error | 0.4933 |

The low Kappa statistic indicates that the model only modestly improved over
chance classification.

---

### Flight Delay Classification Conclusion

Scheduled departure time showed some predictive value for flight delays, but
the overall performance of the J48 model was limited.

The results suggest that flight delays depend on additional operational and
environmental factors that were not represented sufficiently in the selected
predictors.

Future models could include variables such as:

- Weather conditions
- Airport traffic
- Aircraft availability
- Seasonal patterns
- Late aircraft delays
- National Airspace System delays
- Security delays

---

# 2. Airline Market Entry Analysis

## Project Overview

The Airline Market Entry Analysis evaluates potential opportunities for
investors considering the launch of a new airline.

The project uses aviation and financial data to provide data-driven insight
into three major business questions:

1. Which roundtrip routes are the most profitable?
2. How many flights would be required to recover a $90 million investment?
3. How do flight delays affect airline costs and operational risk?

---

## Data Sources

The analysis used three datasets from **2019**:

### Flight Dataset

Contained operational information such as:

- Carrier
- Tail number
- Origin airport
- Destination airport
- Arrival time
- Departure time
- Air time
- Cancellation status
- Distance
- Occupancy rate

### Ticket Dataset

Contained booking information such as:

- Ticket ID
- Origin
- Destination
- Roundtrip status
- Carrier
- Itinerary fare

### Airport Dataset

Contained airport characteristics such as:

- IATA airport code
- Airport name
- Geographic location
- Airport size

The datasets were merged using shared variables, creating a combined dataset
with **46 variables**.

---

## Data Preparation

After preprocessing and filtering, the analytical dataset contained:

```text
1,823,260 observations
```

The final dataset focused on:

- Uncancelled flights
- Roundtrip flights
- Medium-sized airports
- Large airports

Missing values were converted to `NaN` using NumPy to reduce their influence
on statistical calculations.

---

## Feature Engineering

Eleven additional variables were created to support the financial analysis.

### Passenger Count

Passenger count was estimated using aircraft occupancy:

```text
Passenger Count = Occupancy Rate × 200
```

The analysis assumed a 200-seat aircraft.

### Baggage Revenue

Half of passengers were assumed to purchase checked baggage at $70:

```text
Baggage Revenue = (Passenger Count × $70) / 2
```

### Flight Operations Cost

```text
Flight Operations Cost = Distance × 8
```

### Overhead Cost

```text
Overhead Cost = Distance × 1.18
```

### Ticket Revenue

```text
Ticket Revenue = Itinerary Fare × Passenger Count
```

### Airport Costs

Airport costs were assigned according to airport size:

| Airport Size | Cost |
|---|---:|
| Medium | $5,000 |
| Large | $10,000 |

Costs from both the origin and destination airports were included.

### Delay Fees

Arrival and departure delays beyond 15 minutes generated a cost of:

```text
$75 per minute
```

### Profit

Profit per flight was calculated by subtracting operational costs from total
revenue.

---

# Most Profitable Routes

Five routes were identified as the highest-performing routes in the analysis.

| Rank | Route |
|---:|---|
| 1 | Salt Lake City (SLC) ↔ Magic Valley Regional (TWF) |
| 2 | Eagle County (EGE) ↔ John F. Kennedy (JFK) |
| 3 | Florence Regional (FLO) ↔ Charlotte Douglas (CLT) |
| 4 | Pocatello Regional (PIH) ↔ Salt Lake City (SLC) |
| 5 | Honolulu (HNL) ↔ Guam (GUM) |

The **SLC–TWF route** was identified as the highest-profit route in the
analysis.

---

# Break-Even Analysis

The project evaluated the number of roundtrip flights required to recover an
initial investment of:

```text
$90,000,000
```

Break-even requirements were estimated using:

```text
Break-Even Flights = $90,000,000 / Profit per Route
```

### Estimated Break-Even Flights

| Route | Flights Required |
|---|---:|
| SLC ↔ TWF | **46** |
| EGE ↔ JFK | **218** |
| FLO ↔ CLT | **230** |
| PIH ↔ SLC | **253** |
| HNL ↔ GUM | **265** |

Based on the analysis, the SLC–TWF route provided the shortest estimated
break-even period among the five routes.

---

# Flight Delay Analysis

The market-entry analysis identified:

```text
12,595 delayed flights
```

Possible contributors discussed in the analysis included:

- Severe weather
- Staffing shortages
- High passenger demand
- Airport capacity limitations

Medium-sized airports exhibited more delays than large airports in the
analysis.

Flight delays represent both an operational and financial concern because
they can generate direct delay costs while also affecting customer
satisfaction.

---

# Visual Analysis

The project includes several visualizations to communicate the results.

These include:

- Distribution of arrival delays
- Top routes by total revenue
- Average arrival delay by origin airport type

These visualizations help connect operational performance with route
profitability and airport characteristics.

---

# Key Findings

The two projects provide complementary perspectives on airline operations.

### Flight Delay Classification

- J48 achieved **59.33% accuracy**.
- Scheduled departure time was the only predictor selected by the final tree.
- Flights scheduled after 12:59 were classified as delayed.
- The low Kappa statistic indicated limited predictive strength.
- Additional operational and environmental variables are needed to improve
  classification.

### Airline Market Entry Analysis

- The final analytical dataset contained more than **1.8 million observations**.
- **SLC ↔ TWF** was identified as the highest-profit route.
- The SLC–TWF route required an estimated **46 flights** to recover a
  $90 million investment.
- The analysis identified **12,595 delayed flights**.
- Delay costs represent an important operational risk when evaluating airline
  profitability.

---

# Technologies and Tools

These projects demonstrate experience with:

- Python
- NumPy
- Pandas
- Matplotlib
- Data visualization
- WEKA
- J48 Decision Trees
- Machine learning
- Classification
- 10-fold cross-validation
- Data cleaning
- Data integration
- Feature engineering
- Exploratory data analysis
- Financial analysis
- Business analytics

---

# Skills Demonstrated

- Large dataset analysis
- Data preprocessing
- Dataset integration
- Missing-value handling
- Feature engineering
- Exploratory data analysis
- Decision-tree classification
- Cross-validation
- Model evaluation
- Profitability analysis
- Break-even analysis
- Route analysis
- Operational risk analysis
- Data visualization
- Business decision support
- Translating analytical results into business recommendations

---

# Suggested Repository Structure

```text
airline-analytics/
│
├── flight-delay-classification/
│   ├── data/
│   ├── weka/
│   ├── figures/
│   └── report/
│
├── airline-market-entry-analysis/
│   ├── data/
│   ├── notebooks/
│   ├── figures/
│   └── report/
│
├── requirements.txt
└── README.md
```

---

# Running the Python Analysis

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

## 4. Install Python Dependencies

```bash
pip install pandas numpy matplotlib jupyter
```

## 5. Start Jupyter Notebook

```bash
jupyter notebook
```

Open the airline market-entry notebook and run the cells in order.

---

# Running the Flight Delay Model in WEKA

1. Open **WEKA Explorer**.
2. Select the **Preprocess** tab.
3. Load the prepared flight dataset.
4. Set `Delayed` as the class attribute.
5. Open the **Classify** tab.
6. Select:

```text
trees → J48
```

7. Choose:

```text
10-fold cross-validation
```

8. Run the classifier.
9. Review the decision tree, accuracy, Kappa statistic, MAE, and RMSE.

---

# Limitations

The flight-delay classification model used only 300 observations from the
larger flight dataset, which limits its ability to capture the complexity of
airline delays.

The J48 model ultimately relied only on scheduled departure time, indicating
that additional predictors are necessary for stronger classification.

The market-entry analysis also depends on assumptions regarding aircraft
capacity, baggage purchases, airport costs, delay costs, and operating
expenses. Actual airline costs and revenue could differ from these analytical
assumptions.

Therefore, the profitability and break-even estimates should be interpreted
as analytical projections rather than guaranteed financial outcomes.

---

# Future Improvements

Future work could include:

- Training flight-delay models on larger datasets
- Comparing J48 with Random Forest and Gradient Boosting
- Incorporating weather data
- Incorporating airport congestion data
- Modeling seasonal travel patterns
- Predicting passenger demand
- Forecasting route revenue
- Evaluating revenue lost from empty seats
- Performing deeper route optimization
- Building interactive airline profitability dashboards
- Combining delay prediction with route profitability analysis

---

# Conclusion

Together, these projects demonstrate how data analytics can support both
operational and strategic decision-making in the airline industry.

The **Flight Delay Classification** project demonstrates the application of
machine learning to operational prediction, while the **Airline Market Entry
Analysis** demonstrates how large-scale aviation data can be transformed into
financial and strategic insights.

Combining these approaches could support a more comprehensive airline
decision-support system in which investors evaluate not only expected route
profitability but also the operational risk associated with flight delays.

---

# Author

**Shanquell Thompson-Sanders**

Data Science | Machine Learning | Business Analytics | Aviation Analytics
