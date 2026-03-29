all: process analyse

process:
	python src/process.py

analyse:
	python src/analyse.py

run:
	jupyter notebook blog.ipynb