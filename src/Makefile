CC = python3
MONGO = mongo_init.py
DATA_ANALYZER = data_analyzer.py

all:
	make unzip_dataset
	make build MONGO_ARGS="-d"
	make run

unzip_dataset:
	unzip ../data/pocasi.zip -d ../data

build:
	$(CC) $(MONGO) $(MONGO_ARGS)
	$(CC) $(DATA_ANALYZER)

run:
	$(CC) $(DATA_ANALYZER) -r