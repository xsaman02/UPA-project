# UPA-project
VUT FIT project for UPA

## Popis přiložených skriptů

Skript ```mongo_init.py``` slouží k překopírování dat z xml souborů do NoSQL Mongo databáze.
    přepínače: '-d'  Před začátkem nahrávání dat z xml smaže starou databázi a vytvoří novou prázdnou databázi.
                '-f <cesta_ke_složce_s_daty>'  Definuje cestu ke složce, ze které se mají nahrát xml soubory. (default: data).

Skript ```data_analyzer.py``` slouží ke zpracování dat z Mongo databáze a nahrání výsledků do MySQL databáze.
                            Zároveň umožňuje vypsat výsledky jednotlivých SELECT dotazů.
    přepínače:  '-r'  Provede SELECT dotazy ze souboru src/MySQL/UPA_SQL_DB_SELECTS.sql a vypíše výsledek na standardní výstup.


### Detaily spuštění

Ke spuštění slouží připravený Makefile ve složce src/, obsluha je následující:

    (Pozn.: Při spuštění make/make build/make run budete několikrát vyzvání k zadání hesla pro účet "root" kvůli provedení operací nad MySQL databází.)

    > make
    Provede rozbalení testovacích dat ve složce data/ a následně spustí nový build databází pomocí skriptů mongo_init.py a data_analyzer.py. Po dokončení buildů vypíše výsledky zadaných SELECT dotazů (v souboru src/MySQL/UPA_SQL_DB_SELECTS.sql) na standardní výstup terminálu.

    > make unzip_dataset
    Rozbalí xml záznamy z archívu pocasi.zip do složky data.

    > make build
    Provede build NoSQL a MySQL databází, přijímá 1 argument ve formátu: MONGO_ARGS="<argumenty>", kde <argumenty> jsou přepínače skriptu mongo_init.py (popis viz výše).
        Příklad spuštění: make build MONGO_ARGS="-d"

    > make run
    Spustí zadané SELECT dotazy ze souboru src/MySQL/UPA_SQL_DB_SELECTS.sql a výsledky vypíše na standardní výstup.