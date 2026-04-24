# Are Young People Being Priced Out of Life in the UK?

## Overview
This project analyses whether young people in the UK are being priced out of housing by comparing wages, rent, and house prices over time.

## How to Reproduce the Analysis

### 1. Clone the repository:
```Bash
git clone https://github.com/Ben-Morgan536/Are-Young-People-Priced-Out-of-Life-Project.git
cd Are-Young-People-Priced-Out-of-Life-Project
```
### 2. Install required packages
All required packages are listed in `Requirements.txt`.

```Bash
pip install -r requirements.txt
```
### 3. Run the full pipeline 
```Bash
make
```
## Advanced Techniques

#### Workfile Automation
A Makefile is used to automate the entire workflow.

Key commands:
- `make` → runs full pipeline  
- `make process` → runs data cleaning  
- `make analyse` → runs analysis  
This ensures that all results can be reproduced without manual intervention.

The project is fully reproducible from raw data to final outputs, with no manual steps required.

Additionally, a **structural break analysis** was conducted to examine whether the drivers of affordability changed over time.

### Data Sources
- Data is downloaded from the Office for National Statistics (ONS) in Excel format and stored in the `data/raw/` folder. Raw data files in `data/raw/` are kept unchanged and permissions changed to read-only (using 'chmod'). All cleaning and transformations are performed in Python scripts, with outputs saved to `data/processed/`.
##### The Data Used:
- Median earnings data (wages)
- UK House Price Index
- Private rental price index
- Consumer Price Index (CPI)

### Project Structure
- data/ → raw datasets
- src/ → Python scripts
- output/ → figures and results
- blog.ipynb → final analysis and write-up

### How to Reproduce the analysis

1. Clone the repository:
   git clone <your repo link>

2. Install required packages:
   pip install pandas matplotlib seaborn

3. Run data cleaning:
   python src/data_cleaning.py

4. Run analysis:
   python src/analysis.py

5. Open the blog:
   blog.ipynb

Version control was used throughout the project to track changes and ensure reproducibility.

### Methods
- Data cleaning and merging
- Creation of affordability ratios
- Time-series analysis
- Regression analysis

## Key Question
Are housing and rental costs increasing faster than wages in the UK?

# Data Cleaning

### Wages Dataset

The wages dataset (median weekly earnings) was downloaded from the Office for National Statistics (ONS) in Excel format.

Several preprocessing steps were required due to the structure of the raw data:

- Skipped non-data rows at the top of the file
- Selected only the relevant columns (Year and Median Wage (male and female adult))
- Rennamed columns for consistency (`Year`, `Wages`)
- Removed missing values
- Cleaned the `Year` variable:
  - Some entries contained suffixes such as "inc" (included) and "exc" (excluded)
  - Rows containing "exc" were removed
  - "inc" suffixes were stripped to retain only the numeric year
- Converted data types (`Year` to integer, `Wages` to float)
- Sorted the dataset by year

The cleaned dataset is saved in:
`data/processed/wages_clean.csv`

### House Prices Dataset

House price data was constructed by combining two datasets from the Office for National Statistics (ONS):

- A historical dataset covering earlier years
- A more recent dataset covering 2011–2025

Several preprocessing steps were required to create a consistent time series:

- Both datasets were cleaned separately:
  - Selected relevant columns (date and house price values)
  - Removed missing values
  - Converted date variables into a standard datetime format

- As both datasets were provided at a monthly frequency, values were aggregated to annual data by taking the mean house price within each year

- The two datasets were then merged into a single dataset:
  - Duplicate years were removed
  - Where overlap existed, values from the more recent dataset were retained to ensure consistency with the latest methodology

- The final dataset was sorted by year and saved as:
  `data/processed/house_prices_yearly.csv`

This results in a continuous annual house price series suitable for comparison with wages and rental data.

### CPI (Consumer Price Index) Dataset

The CPI dataset was obtained from the Office for National Statistics (ONS) and includes multiple inflation measures across different categories.

To make the dataset suitable for analysis, the following preprocessing steps were carried out:

- Loaded the dataset from CSV format and addressed data-type inconsistencies by adjusting import settings
- Selected a subset of relevant CPI indices:
  - Headline CPI (All Items)
  - Food and non-alcoholic beverages
  - Housing, water, and fuels
  - Transport
  - Education
- Renamed columns to shorter, consistent labels for ease of use (e.g. `CPI_All`, `CPI_Housing`)
- Converted the `Year` variable into an integer format
- Converted CPI variables to numeric format, handling any non-numeric values
- Removed missing observations and sorted the dataset by year

The cleaned dataset was saved as:
`data/processed/cpi_clean.csv`

These CPI measures are used to:
- Adjust wages for inflation (real wages)
- Compare changes in specific cost-of-living components (e.g. housing, food, transport)

## Data Integration and Variable Construction

All cleaned datasets were merged into a two analytical datasets using the `Year` variable as the key.

- Wages, house prices and CPI datasets were merged using an inner join to ensure consistent time periods
- This resulted in a final dataset containing only overlapping years across all variables (excluding rent prices as data is only from 2015)

  A short dataset was also created to include rent prices in the data using the same method, just starting from 2015.
 
### Constructed Variables

Several new variables were created to support the analysis:

- **Real Wages**: wages adjusted for inflation using CPI
- **House Price-to-Wage Ratio**: a measure of housing affordability
- **Rent-to-Wage Ratio**: a measure of rental affordability
- **Real House Prices**: house prices adjusted for inflation
- **House price to monthly/yearly wage ration**: a measure of housing affordability using different time frames

Additionally, differences between category-specific CPI measures and headline CPI were calculated to capture cost-of-living pressures (e.g. housing inflation relative to overall inflation).

The final dataset was saved as:
`data/processed/final_dataset.csv`

All steps are fully reproducible via the scripts in `src/`.

### Indexing of Variables

To enable clear comparison of trends over time, key variables were transformed into index form using 1998 as the base year (1998 = 100).

The following variables were indexed:
- Wages
- Real wages
- House prices
- Real house prices
- Rent prices
- Real rent prices

Indexing allows variables measured in different units to be directly compared, highlighting relative growth over time.

Ratio variables (e.g. house price-to-wage ratio) were not indexed, as they are already scale-independent.

All indexed variables are included in the final dataset with the suffix `_Index`.

## Workflow Automation

This project uses a Makefile to automate the data processing and analysis pipeline.

This allows the entire project to be reproduced with a single command:

    make

The Makefile executes the following steps:

1. Data cleaning (`src/data_cleaning.py`)
2. Data analysis (`src/analysis.py`)

Additional commands are available:

- `make process` → runs data cleaning only
- `make analyse` → runs analysis only
- `make run` → opens the blog notebook

This approach ensures that all results can be reproduced efficiently and consistently.


## Visual Analysis: Are Young People Priced Out of Life?

This project uses a series of time-series graphs to examine how economic conditions have evolved in the UK, with a particular focus on housing affordability. The visualisations provide the primary evidence base for assessing whether young people are being “priced out of life.”

### 1. Wages vs House Prices

The first set of graphs compares real wages with real house prices over time. While wages show steady but relatively modest growth, house prices increase at a significantly faster rate, particularly after the early 2000s and again following 2020.

This divergence indicates that income growth has not kept pace with the cost of purchasing a home. As a result, individuals relying on wages—particularly young people—face increasing difficulty entering the housing market.

---

### 2. House Price-to-Wage Ratio

The house price-to-wage ratio provides a direct measure of affordability. The graph shows a clear upward trend, meaning that housing is becoming less affordable over time.

Notably:
- There are brief periods of stabilisation (e.g. post-2008),  
- But the long-run trend is consistently upward,  
- With a sharp deterioration in affordability in recent years.

This suggests that the problem is persistent and structural rather than temporary.

---
### 3. Housing inflation vs overall inflation
The third graph shows that housing inflation consistently runs above overall CPI inflation, meaning the cost of accommodation has been rising faster than general living costs for most of the period.

Key patterns include:
- Housing inflation remains higher than overall inflation in nearly every year,
- The gap widens during major economic shocks, especially after 2020,
- Even when overall inflation stabilises, housing inflation stays elevated, keeping pressure on affordability.

This persistent divergence indicates that young people face a higher effective inflation rate than the average household because a larger share of their spending goes toward housing.

---
### 4. Movement of rent to wage ratio
The fourth graph tracks the rent‑to‑wage ratio over the past decade and shows that rent affordability has fluctuated but remains broadly unchanged at a high level, offering only limited relief for young renters.

Key patterns include:
- A sharp rise in the ratio around 2016, indicating a period of worsening affordability,
- A gradual decline between 2018 and 2022, suggesting temporary improvement,
- A renewed increase after 2022, showing affordability pressures returning.

Overall, the ratio remains close to its long‑run level, implying that even when conditions improve slightly, young people continue to face persistent strain in meeting rental costs.

---
### 5. Rising cost pressure on households

The fifth graph shows how overall cost pressures have evolved over time, combining multiple inflation components into a single measure that highlights periods of financial strain more clearly than any individual series.

Key patterns include:
- Noticeable spikes during major economic shocks, particularly the 2008 recession and the post‑2020 period,
- A clear upward drift in the 5‑year rolling average, indicating that cost pressures have been rising structurally rather than temporarily,
- Periods of relief (e.g., mid‑2010s) that are short‑lived and quickly reversed by renewed increases.

Taken together, the indicator shows that young people have faced increasingly intense and persistent cost‑of‑living pressures, with recent years marking some of the highest levels in the entire series.

---

### 5. Key Insights from the Graphs

Taken together, the visual evidence suggests:

- Housing costs have grown substantially faster than wages,  
- Affordability has deteriorated steadily over time,  
- Cost-of-living pressures have intensified, particularly in recent years,  
- Both buyers and renters are experiencing increasing financial strain.
---
### 6.Regression: Housing Inflation, Overall Inflation, and Affordability Changes

The sixth figure presents the regression results examining how changes in housing inflation and overall inflation relate to year‑to‑year movements in the rent‑to‑wage ratio.

Key patterns include:
- Housing inflation has a positive but statistically insignificant effect on affordability changes, suggesting it contributes to pressure but not strongly enough to stand out on its own,
- Overall inflation shows a negative coefficient that is close to significance, indicating that when general inflation rises, the rent‑to‑wage ratio tends to fall slightly,
- The model explains only a small share of the variation (R² ≈ 0.18), showing that affordability shifts are driven by broader structural forces rather than short‑term inflation movements.

Overall, the regression reinforces the idea that affordability pressures are persistent and not easily explained by inflation alone, supporting the earlier conclusion that young people face deeper, long‑run structural challenges.

---

## Output Generation and Storage

All figures and tables in this project are generated programmatically and saved automatically to the `outputs/` directory.

### Figures

All visualisations are saved as `.png` files and the regressions are saved as `.csv` in /output folder.

---
## Structural Change in Housing Affordability

To examine whether the drivers of housing affordability have changed over time, the dataset was split into two periods: a pre-crisis period and a post-crisis period (around the 2008 financial crisis).

Separate regressions were estimated for each period to assess whether the relationship between housing inflation and affordability remained stable.

### Results

- **Pre-crisis period:**
  - Constant ≈ 0.103  
  - Housing Inflation ≈ -0.007  

- **Post-crisis period:**
  - Constant ≈ 0.002  
  - Housing Inflation ≈ -0.002  

### Interpretation

The results indicate a substantial decline in the constant term, suggesting that affordability was deteriorating much more rapidly in the earlier period compared to the period after the financial crisis.

The coefficient on housing inflation is negative in both periods but becomes smaller in magnitude in the later period. This suggests that the relationship between housing inflation and affordability has weakened over time.

### Key Insight

These findings provide evidence that the dynamics of housing affordability are not stable over time. Instead, they appear to change across different economic periods.

This supports the idea that the decline in affordability is not driven by a single consistent factor, but reflects broader structural changes in the economy.

---
## Counterfactual Analysis

To further assess the scale of the housing affordability problem, a counterfactual scenario was constructed.

This scenario estimates what wages would look like if they had grown at the same rate as real house prices over time.

### Method

A counterfactual wage series was generated by applying the growth rate of real house prices to the initial wage level:

```python
main_data["hp_growth"] = main_data["Real_House_Prices"].pct_change()
main_data["Counterfactual_Wages"] = main_data["Yearly_Real_Wages"].iloc[0] * (1 + main_data["hp_growth"]).cumprod()
```
---
### Link to Project Question

This analysis strengthens the overall conclusion that young people are increasingly being priced out of life, as the factors affecting affordability have evolved over time rather than remaining constant.

---

### 6. Conclusion from Visual Evidence

The graphical analysis provides strong evidence that young people are increasingly being priced out of life in the UK.

The issue appears to be driven primarily by the divergence between income growth and housing costs, rather than short-term fluctuations. While inflation contributes to financial pressure, the sustained rise in house prices and rent relative to wages points to deeper structural challenges in the housing market.
