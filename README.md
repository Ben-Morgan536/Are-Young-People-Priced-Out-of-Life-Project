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

```Bash
pip install -r requirements.txt
```
### 3. Run the full pipeline 
```Bash
make
```

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

### How to Replicate

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

## Web Scraping: Graduate Labour Market

To better reflect the economic reality faced by young people, this project incorporates web scraping of graduate job listings.

Using Python libraries such as `requests` and `BeautifulSoup`, data was collected on:

- Graduate job titles
- Estimated salaries
- Number of available positions

This allows the analysis to move beyond average wages and instead focus on entry-level labour market conditions.

The scraped data is processed and saved in:
data/processed/graduate_jobs.csv

A summary dataset is created:
data/processed/graduate_summary.csv

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

### 3. Cost Pressure Indicator

A composite cost pressure indicator was constructed using inflation in key categories such as housing, food, transport, and education.

The graph shows:
- A gradual increase in cost pressures over time,  
- A pronounced spike around 2021–2023,  
- Sustained high levels thereafter.

The rolling average highlights that this is not just short-term volatility, but part of a broader upward trend in living costs.

---

### 4. Rent Prices (Short-Run Analysis)

Using data available from 2015 onwards, rent prices were analysed as an additional measure of housing pressure.

The graph shows:
- Consistent increases in rental costs,  
- Limited evidence of downward adjustment,  
- Rising rent-to-wage ratios over time.

This indicates that even those unable to buy are facing increasing financial pressure in the rental market.

---

### 5. Key Insights from the Graphs

Taken together, the visual evidence suggests:

- Housing costs have grown substantially faster than wages,  
- Affordability has deteriorated steadily over time,  
- Cost-of-living pressures have intensified, particularly in recent years,  
- Both buyers and renters are experiencing increasing financial strain.

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

### Link to Project Question

This analysis strengthens the overall conclusion that young people are increasingly being priced out of life, as the factors affecting affordability have evolved over time rather than remaining constant.

---

### 6. Conclusion from Visual Evidence

The graphical analysis provides strong evidence that young people are increasingly being priced out of life in the UK.

The issue appears to be driven primarily by the divergence between income growth and housing costs, rather than short-term fluctuations. While inflation contributes to financial pressure, the sustained rise in house prices and rent relative to wages points to deeper structural challenges in the housing market.
