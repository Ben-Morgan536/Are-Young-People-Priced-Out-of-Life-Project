# Are Young People Being Priced Out of Life in the UK?

## Overview
This project analyses whether young people in the UK are being priced out of housing by comparing wages, rent, and house prices over time.

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
