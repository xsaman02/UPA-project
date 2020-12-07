# UPA-project
VUT FIT project for UPA

## Spuštění script.py

Skript ```script.py``` slouží k překopírování dat z xml souborů do mongo datbáze.

### Detaily spuštění

``-d`` vymaže celou mongo databázi, pokud argument chybí přidá data k existujícím datům.

``-f`` specifikace soubory/složky s xml soubory s daty. Pokud chybí data se načítají ze složky ``src`` umístěné ve stejném adresáři jako skript.
