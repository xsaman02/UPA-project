CC = mysql
FILE = UPA_SQL_DB.sql
DROP = UPA_SQL_DB_DROP.sql
SELECT = UPA_SQL_SELECTS.sql
FLAGS = -u root
PWDFLAGS = -u root -p
FORMAT_FLAG = -t

run:
	$(CC) $(FLAGS) < $(FILE)

drop:
	$(CC) $(FLAGS) < $(DROP)

select:
	$(CC) $(FLAGS) < $(SELECT) $(FORMAT_FLAG)

runpwd:
	$(CC) $(PWDFLAGS) < $(FILE)

droppwd:
	$(CC) $(PWDFLAGS) < $(DROP)

selectpwd:
	$(CC) $(PWDFLAGS) < $(SELECT) $(FORMAT_FLAG)
