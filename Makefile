all: process analyse run

process:
	python3 /mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/src/data_cleaning.py

analyse:
	python3 /mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/src/analysis.py

run:
	jupyter notebook blog.ipynb
