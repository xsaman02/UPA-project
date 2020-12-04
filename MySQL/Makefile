CC = mysql
FILE = UPA_SQL_DB.sql
DROP = UPA_SQL_DB_DROP.sql
FLAGS = -u root -p

run:
	$(CC) $(FLAGS) < $(FILE)

drop:
	$(CC) $(FLAGS) < $(DROP)