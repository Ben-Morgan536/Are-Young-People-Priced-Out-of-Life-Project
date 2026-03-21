# Are Young People Being Priced Out of Life in the UK?

## Overview
This project analyses whether young people in the UK are being priced out of housing by comparing wages, rent, and house prices over time.

### Data Sources
- Data is downloaded from the Office for National Statistics (ONS) in Excel format and stored in the `data/raw/` folder. These files are processed using Python scripts to create clean datasets for analysis.
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
