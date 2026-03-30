import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://en.wikipedia.org/wiki/Graduate_unemployment"

response = requests.get(url)

# Check if page loaded properly
print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# Extract ALL text from page
text = soup.get_text()

# Find salary-like numbers (e.g. 30000, 45,000)
salary_matches = re.findall(r'\d{2,3},?\d{3}', text)

# Clean salaries
salaries = []

for s in salary_matches:
    val = int(s.replace(",", ""))
    
    # Filter realistic graduate salaries
    if 15000 < val < 200000:
        salaries.append(val)

# Create DataFrame
grad_salaries = pd.DataFrame({"Salary": salaries})

# Drop duplicates (nice touch)
grad_salaries = grad_salaries.drop_duplicates()

# Summary
avg_salary = grad_salaries["Salary"].mean()
num_obs = len(grad_salaries)

print("Average Salary:", avg_salary)
print("Number of observations:", num_obs)
print(grad_salaries.head())

# Save
grad_salaries.to_csv(r'/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/grad_salaries.csv', index=False)

summary_grad = pd.DataFrame({
    "Year": [2025],
    "Avg_Graduate_Salary": [avg_salary],
    "Observations": [num_obs]
})

summary_grad.to_csv(r'/mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/data/Processed/summary_grad', index=False)


