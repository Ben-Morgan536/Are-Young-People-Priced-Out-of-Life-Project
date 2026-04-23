import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("default")
#Checking to find the path
#import os
#print(os.getcwd())
# Importing the dataset
wages_Initial = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/Median_Weekly_Earnings.xlsx", sheet_name="UK Median Time-series")
#Working out the structure of the dataset to make consistent with the other datasets
print("Raw Wages Data:")
print(wages_Initial.head())
print(wages_Initial.columns)
#Skipping junk rows
wages = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/Median_Weekly_Earnings.xlsx", sheet_name="UK Median Time-series", skiprows=12, header=None)
print("Raw Wages Data (After Skipping Junk Rows):")
print(wages.head())
print(wages.columns)
#Selecting only the relevant columns and renaming them for consistency
wages = wages.iloc[:, [1, 27]]
wages.columns = ['Year', 'Wages']
print("Cleaned Wages Data:")
print(wages.head())
wages = wages.dropna() # Removing rows with missing values in the Year and Wages columns
 # Removing any rows with missing values
#Sorting non integer values by removing exc values and removing the suffic on inc values
wages['Year'] = wages['Year'].astype(str) # Converting Year to string for manipulation
wages = wages[wages['Year'].str.contains('exc') == False] # Removing rows with 'exc' suffix
wages['Year'] = wages['Year'].str.extract(r'(\d+)') # Extracting only the numeric part of the Year
wages = wages.dropna(subset=['Year']) # Removing rows with missing Year values
wages['Year'] = wages['Year'].astype(int)  # Converting Year to integer
wages['Wages'] = wages['Wages'].astype(float)  # Converting Wages to float
wages = wages.sort_values('Year')  # Sorting by Year
wages = wages.drop_duplicates(subset=['Year'], keep='first')
print("Final Cleaned Wages Data:")                  
print(wages.head(20))
print(wages.info())
wages.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/wages_clean.csv", index=False)
# Now we have cleaned wages and converted to a CSV file for use in the analysis.

#Now we clean the house price data

#Have 2 datasets that need merging, one pre 2011 and one post 2011, so we need to clean both and then merge them together
#Cleaning the pre 2011 dataset
house_hist_initial = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/UKHPI_historic_file.xlsx", sheet_name="Table 1")
#Working out the structure of the dataset to make consistent with the other datasets
print("Raw House Price Data (Pre 2011):")
print(house_hist_initial.head())
print(house_hist_initial.columns)   
#Skipping junk rows
house_hist = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/UKHPI_historic_file.xlsx", sheet_name="Table 1", skiprows=116, header=None)
print("Raw House Price Data (Pre 2011, After Skipping Junk Rows):")
print(house_hist.head())
print(house_hist.columns)
#Forward filling the year values to fill in the missing year values
house_hist[0] = house_hist[0].ffill()
#Selecting relevant columns and renaming them for consistency
house_hist = house_hist.iloc[:, [0, 2]]
house_hist.columns = ['Year', 'House_Price']
#converting Year to integer and House_Price to float
#house_hist['Year'] = house_hist['Year'].astype(int)
house_hist['House_Price'] = house_hist['House_Price'].astype(float)
house_hist_yearly = house_hist.groupby('Year')['House_Price'].mean().reset_index() # Grouping by Year and calculating the mean House_Price for each year
house_hist_yearly = house_hist_yearly.dropna(subset=['Year', 'House_Price']) # Removing rows with missing values in Year or House_Price
#convert Year to integer and House_Price to float
house_hist_yearly['Year'] = house_hist_yearly['Year'].astype(int)
house_hist_yearly['House_Price'] = house_hist_yearly['House_Price'].astype(float)
print("Grouped House Price Data (Pre 2011):")
print(house_hist_yearly.tail())

#Cleaning the post 2011 dataset
house_recent_initial = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/House_Prices.xlsx", sheet_name="2")
#Working out the structure of the dataset to make consistent with the other datasets
print("Raw House Price Data (Post 2011):")
print(house_recent_initial.head())
print(house_recent_initial.columns)
#Skipping junk rows
house_recent = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/House_Prices.xlsx", sheet_name="2", skiprows=3, header=None)
print("Raw House Price Data (Post 2011, After Skipping Junk Rows):")
print(house_recent.head())
print(house_recent.columns)
house_recent = house_recent.iloc[:, [0, 1]] # Selecting relevant columns
house_recent.columns = ['Year', 'House_Price'] # Renaming columns for consistency
#Extracting the year from the Year column and converting to integer
house_recent['Year'] = house_recent['Year'].str.extract(r'(\d{4})') # Extracting the year using regex
#house_recent['Year'] = house_recent['Year'].astype(int) # Converting Year to integer

house_recent['House_Price'] = house_recent['House_Price'].astype(str).str.replace(',', '') # Removing commas from House_Price
house_recent['House_Price'] = house_recent['House_Price'].astype(float) # Converting House_Price to float
#Grouping by Year and calculating the mean House_Price for each year
house_recent_yearly = house_recent.groupby('Year')['House_Price'].mean().reset_index()
house_recent_yearly = house_recent_yearly.dropna(subset=['Year', 'House_Price']) # Removing rows with missing values in Year or House_Price
house_recent_yearly['Year'] = house_recent_yearly['Year'].astype(int) # Converting Year to integer
print("Grouped House Price Data (Post 2011):")
print(house_recent_yearly.head())

###Merging the two house price datasets together
house_prices_yearly = pd.concat([house_hist_yearly, house_recent_yearly], ignore_index=True)
print("Merged House Price Data:")
print(house_prices_yearly.head())
#Check if we have aby duplicate years in the merged dataset
print(house_prices_yearly['Year'].value_counts())
#removing any duplicate years by keeping the second occurrence
house_prices_yearly = house_prices_yearly.drop_duplicates(subset=['Year'], keep='last')
print("Merged House Price Data (After Removing Duplicates):")
print(house_prices_yearly['Year'].value_counts()) #check to make sure duplicates have been removed
#Convert and save the merged dataset to a CSV file for use in the analysis
house_prices_yearly.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/house_prices_clean.csv", index=False)

##Cleaning the rent price data

#working out the structure of the dataset to make consistent with the other datasets. Only readin rows 1-136 to avoid junk rows at the end of the dataset
rent_initial = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/Rent_Prices.xlsx", sheet_name="Table 1", nrows=136)
print("Raw Rent Price Data:")
print(rent_initial.head())
print(rent_initial.columns)
#Skipping junk rows at the start of the dataset and selecting relevant columns
rent = pd.read_excel(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/Rent_Prices.xlsx", sheet_name="Table 1", skiprows=3, header=None, nrows=133)
print("Raw Rent Price Data (After Skipping Junk Rows):")    
print(rent.head())
#Selecting relevant columns and renaming them for consistency
rent = rent.iloc[:, [0, 7]]
rent.columns = ['Year', 'Rent_Price']
print(rent.head())
#grouping by Year and calculating the mean Rent_Price for each year
rent['Year'] = rent['Year'].astype(str).str.extract(r'(\d{4})').astype(int) # Extracting the year from the first column and converting to integer
rent['Rent_Price'] = rent['Rent_Price'].astype(float) # Converting Rent_Price to float
rent_yearly = rent.groupby('Year')['Rent_Price'].mean().reset_index()
print("Grouped Rent Price Data:")
print(rent_yearly.tail())
#Convert and save the cleaned dataset to a CSV file for use in the analysis
rent_yearly.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/rent_prices_clean.csv", index=False)

##Cleand and merge CPI data sets
cpi_hist_initial = pd.read_csv (r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Raw_Data/CPI_historic_data.csv", usecols=[
        "Title","CPI INDEX 00: ALL ITEMS 2015=100","CPI INDEX 01 : FOOD AND NON-ALCOHOLIC BEVERAGES 2015=100","CPI INDEX 04 : HOUSING, WATER AND FUELS 2015=100","CPI INDEX 07 : TRANSPORT 2015=100","CPI INDEX 10 : EDUCATION 2015=100"],low_memory=False)
cpi_condensed2 = cpi_hist_initial[['Title','CPI INDEX 00: ALL ITEMS 2015=100','CPI INDEX 01 : FOOD AND NON-ALCOHOLIC BEVERAGES 2015=100','CPI INDEX 04 : HOUSING, WATER AND FUELS 2015=100','CPI INDEX 07 : TRANSPORT 2015=100','CPI INDEX 10 : EDUCATION 2015=100']]
cpi_condensed = cpi_condensed2.iloc[204:232]  # Selecting rows 204 to 232

print("Condensed CPI Data:")
print(cpi_condensed.head())
print(cpi_condensed.columns)

cpi = cpi_condensed.copy()
cpi.columns = ["Year","CPI_All","CPI_Food","CPI_Housing","CPI_Transport","CPI_Education"]
print(cpi.head())
#Extracting the year from the Year column and converting to integer
cpi['Year'] = cpi['Year'].str.extract(r'(\d{4})').astype(int) # Extracting the year using regex and converting to integer
#Converting the CPI columns to float
cpi[['CPI_All', 'CPI_Food', 'CPI_Housing', 'CPI_Transport', 'CPI_Education']] = cpi[['CPI_All', 'CPI_Food', 'CPI_Housing', 'CPI_Transport', 'CPI_Education']].astype(float)
print("Cleaned CPI Data:")
print(cpi.tail())
#convert the columns to numeric values and save to a CSV file for use in the analysis
cols = ['CPI_All', 'CPI_Food', 'CPI_Housing', 'CPI_Transport', 'CPI_Education']
cpi[cols] = cpi[cols].apply(pd.to_numeric, errors='coerce')
cpi.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/cpi_clean.csv", index=False)

###Merging the cleaned datasets together into one master dataset for use in the analysis###

#First we merge the wages and house price datasets together on the Year column using an inner join to keep only the years that are present in both datasets
main_data = pd.merge(wages, house_prices_yearly, on='Year', how='inner')
print("Merged Wages and House Price Data:")
print(main_data.head())
#Now add CPI data to the merged dataset using an inner join on the Year column
main_data = pd.merge(main_data, cpi, on='Year', how='inner')
print("Merged Wages, House Price and CPI Data:")
print(main_data.head())
#Now add rent price data to the merged dataset using an inner join on the Year column
#main_data = pd.merge(main_data, rent_yearly, on='Year', how='inner')
print("Final Merged Dataset:")
print(main_data.head())
print(main_data.tail())
print(main_data.shape)
#Creating new variables for the analysis using the existing variables in the dataset

#Creating a real wage variable using the CPI_All variable to adjust the nominal wages for inflation
main_data['Real_Wages'] = main_data['Wages'] / (main_data['CPI_All'] / 100)
#Creating a real house price variable using the CPI_All variable to adjust the nominal house prices for inflation
main_data['Real_House_Price'] = main_data['House_Price'] / (main_data['CPI_All'] / 100)
#Creating a house price to wage ratio variable to show house affordability
main_data['House_Price_to_Wage_Ratio'] = main_data['House_Price'] / main_data['Wages']
#Creating a house price to wage ratio variable using real wages and real house prices to show real house affordability
main_data['Real_House_Price_to_Real_Wage_Ratio'] = main_data['Real_House_Price'] / main_data['Real_Wages']

#Creating cost pressure indicators by calculating the year on year percentage change in the CPI variables to show the inflation rates for each category
#Housing inflation
main_data['Housing_Inflation'] = main_data['CPI_Housing'].pct_change() * 100
#Food inflation 
main_data['Food_Inflation'] = main_data['CPI_Food'].pct_change() * 100
#Transport inflation
main_data['Transport_Inflation'] = main_data['CPI_Transport'].pct_change() * 100
#Education inflation
main_data['Education_Inflation'] = main_data['CPI_Education'].pct_change() * 100
#Overall inflation
main_data['Overall_Inflation'] = main_data['CPI_All'].pct_change() * 100
#Creating a cost pressure indicator by taking the average of the housing, food, transport and education inflation rates
main_data['Cost_Pressure_Indicator'] = main_data[['Housing_Inflation', 'Food_Inflation', 'Transport_Inflation', 'Education_Inflation']].mean(axis=1)

#Creating indexes for wages and house prices using 1998 as the base year (1998 = 100)
main_data['Wage_Index'] = main_data['Wages'] / main_data.loc[main_data['Year'] == 1998, 'Wages'].values[0] * 100
main_data['House_Price_Index'] = main_data['House_Price'] / main_data.loc[main_data['Year'] == 1998, 'House_Price'].values[0] * 100

#Indexing other relevant variables to 1998 as the base year (1998 = 100) to show how they have changed relative to the base year
main_data['Real_Wage_Index'] = main_data['Real_Wages'] / main_data.loc[main_data['Year'] == 1998, 'Real_Wages'].values[0] * 100
main_data['Real_House_Price_Index'] = main_data['Real_House_Price'] / main_data.loc[main_data['Year'] == 1998, 'Real_House_Price'].values[0] * 100

#changing the base year of the CPI variables to 1998 (1998 = 100) to show how they have changed relative to the base year
main_data['CPI_All_Index'] = main_data['CPI_All'] / main_data.loc[main_data['Year'] == 1998, 'CPI_All'].values[0] * 100
main_data['CPI_Food_Index'] = main_data['CPI_Food'] / main_data.loc[main_data['Year'] == 1998, 'CPI_Food'].values[0] * 100
main_data['CPI_Housing_Index'] = main_data['CPI_Housing'] / main_data.loc[main_data['Year'] == 1998, 'CPI_Housing'].values[0] * 100
main_data['CPI_Transport_Index'] = main_data['CPI_Transport'] / main_data.loc[main_data['Year'] == 1998, 'CPI_Transport'].values[0] * 100
main_data['CPI_Education_Index'] = main_data['CPI_Education'] / main_data.loc[main_data['Year'] == 1998, 'CPI_Education'].values[0] * 100

#Creating a monthly wage variable by timesing the weekly wage variable by 52 and dividing by 12 to show the average monthly wage
main_data['Monthly_Wages'] = main_data['Wages'] * 52 / 12

#Rounding all variables to 2 decimal places for easier interpretation
main_data = main_data.round(2)

print("Final Dataset with New Variables:")
print(main_data.head())
print(main_data.shape)
#Creating a short main dataset to include rent data for where we have it available (2015-2025)
main_data_short = main_data[main_data['Year'] >= 2015]
#merging rent in to the short main dataset
main_data_short = pd.merge(main_data_short, rent_yearly, on='Year', how='inner')
#Creating a real rent price variable using the CPI_All variable to adjust the nominal rent prices for
main_data_short['Real_Rent_Price'] = main_data_short['Rent_Price'] / (main_data_short['CPI_All'] / 100)
#Creating a rent price to wage ratio variable to show rent affordability
main_data_short['Rent_Price_to_Wage_Ratio'] = main_data_short['Rent_Price'] / main_data_short['Wages']
#Creating a rent price to wage ratio variable using real wages and real rent prices to show real
main_data_short['Real_Rent_Price_to_Real_Wage_Ratio'] = main_data_short['Real_Rent_Price'] / main_data_short['Real_Wages']

#Removing all the CPI index variables as already have base year of 2015 for the short main dataset 
main_data_short = main_data_short.drop(columns=['CPI_All_Index', 'CPI_Food_Index', 'CPI_Housing_Index', 'CPI_Transport_Index', 'CPI_Education_Index'])


#Adding a rent,wage and house price index using 2015 as the base year (2015 = 100) for the short main dataset
main_data_short['Rent_Price_Index'] = main_data_short['Rent_Price'] / main_data_short.loc[main_data_short['Year'] == 2015, 'Rent_Price'].values[0] * 100
main_data_short['Wage_Index'] = main_data_short['Wages'] / main_data_short.loc[main_data_short['Year'] == 2015, 'Wages'].values[0] * 100
main_data_short['House_Price_Index'] = main_data_short['House_Price'] / main_data_short.loc[main_data_short['Year'] == 2015, 'House_Price'].values[0] * 100
#real wage and real house price indexes using 2015 as the base year (2015 = 100) for the short main dataset
main_data_short['Real_Wage_Index'] = main_data_short['Real_Wages'] / main_data_short.loc[main_data_short['Year'] == 2015, 'Real_Wages'].values[0] * 100
main_data_short['Real_House_Price_Index'] = main_data_short['Real_House_Price'] / main_data_short.loc[main_data_short['Year'] == 2015, 'Real_House_Price'].values[0] * 100

#Rounding all variables in the short main dataset to 2 decimal places for easier interpretation
main_data_short = main_data_short.round(2)

print("Short Main Dataset with Rent Data:")
print(main_data_short.head())
print(main_data_short.shape)
#Saving the final merged datasets to CSV files for use in the analysis
main_data.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/main_data.csv", index=False)
main_data_short.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/main_data_short.csv", index=False)

### Saving Figures in to output folder for use in the report

#Figure 1
plt.figure(figsize=(10,6))

plt.plot(main_data["Year"], main_data["Real_Wage_Index"], label="Real Wage Index", linewidth=2)
plt.plot(main_data["Year"], main_data["Real_House_Price_Index"], label="Real House Price Index", linewidth=2)

plt.title("Divergence Between Wages and House Prices in the UK", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Real Values (Indexed to 1998=100)")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/Figure_1.png")
plt.close()

#Figure 2

plt.figure(figsize=(10,6))

plt.plot(main_data["Year"], main_data["House_Price_to_Wage_Ratio"], label="House Price to Wage Ratio", linewidth=2)

plt.title("Housing Affordability Has Worsened Over Time", fontsize=14)
plt.xlabel("Year")

plt.grid(alpha=0.3)
plt.tight_layout()


plt.axhline(y=main_data["House_Price_to_Wage_Ratio"].mean(), linestyle="--", color="red", linewidth=2, label="Average Ratio")
plt.legend()
plt.savefig(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/Figure_2.png")
plt.close()

#Figure 3

plt.figure(figsize=(10,6))

plt.plot(main_data["Year"], main_data["Housing_Inflation"], label="Housing", linewidth=2)
plt.plot(main_data["Year"], main_data["Overall_Inflation"], label="Overall CPI", linewidth=2)
plt.plot(main_data["Year"], main_data["Education_Inflation"], label="Education", linewidth=1, linestyle=":", color="maroon")
plt.plot(main_data["Year"], main_data["Transport_Inflation"], label="Transport", linewidth=1, linestyle=":", color="orange")

plt.legend()
plt.title("Housing Inflation vs Overall Inflation")
plt.xlabel("Year")
plt.ylabel("Inflation Rate")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/Figure_3.png")
plt.close()

#Figure 4

plt.figure()

plt.plot(main_data_short["Year"], main_data_short["Rent_Price_to_Wage_Ratio"])

plt.title("Rent to Wage Ratio")
plt.xlabel("Year")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/Figure_4.png")
plt.close()

#Figure 5

plt.figure(figsize=(10,6))

plt.plot(main_data["Year"], main_data["Cost_Pressure_Indicator"], linewidth=2, label="Composite Cost Pressure Indicator")
plt.axhline(y=main_data["Cost_Pressure_Indicator"].mean(), linestyle="--", color="red", linewidth=2, label="Average Pressure")

main_data["Cost_Pressure_Rolling"] = main_data["Cost_Pressure_Indicator"].rolling(window=5).mean()
plt.plot(main_data["Year"], main_data["Cost_Pressure_Rolling"], label="5-Year Rolling Average", linewidth=2.5)


plt.axvspan(2008, 2009, alpha=0.2, label="Recession")
plt.axvspan(2020, 2020.5, alpha=0.2, label="COVID-19 Pandemic", color="gray")

plt.legend()

plt.title("Rising Cost Pressure on Households")
plt.xlabel("Year")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/Figure_5.png")
plt.close()

#Figure 6

main_data["d_ratio"] = main_data["House_Price_to_Wage_Ratio"].pct_change()

df_reg = main_data.dropna()

import statsmodels.api as sm

X = df_reg[["Housing_Inflation","Overall_Inflation"]]
y = df_reg["d_ratio"]
X = sm.add_constant(X)
model_main = sm.OLS(y, X).fit()
with open(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/figure_6_regression_results.csv", "w") as f:
    f.write(model_main.summary().as_text())

# Save clean coefficients table
results_df = model_main.params.to_frame(name="Coefficient")
results_df["P-value"] = model_main.pvalues
results_df["Std_Error"] = model_main.bse
results_df.to_csv(r"/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/output/figure_6_regression_results.csv")