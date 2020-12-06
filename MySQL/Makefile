CC = mysql
FILE = UPA_SQL_DB.sql
DROP = UPA_SQL_DB_DROP.sql
SELECT = UPA_SQL_SELECTS.sql
FLAGS = -u root
PWDFLAGS = -u root -p

run:
	$(CC) $(FLAGS) < $(FILE)

drop:
	$(CC) $(FLAGS) < $(DROP)

select:
	$(CC) $(FLAGS) < $(SELECT)

runpwd:
	$(CC) $(PWDFLAGS) < $(FILE)

droppwd:
	$(CC) $(PWDFLAGS) < $(DROP)

selectpwd:
	$(CC) $(PWDFLAGS) < $(SELECT)