all: process run

process:
	python3 /mnt/c/Users/paul/OneDrive/Ben/Uni/Year_2/Data_Science/Are-Young-People-Priced-Out-of-Life-Project/src/data_cleaning.py

run:
	jupyter lab blog.ipynb