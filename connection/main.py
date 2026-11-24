from core.OracleConnection import Connection

connection = Connection()
cursor = connection.create_session()

cursor.execute("SELECT table_name FROM user_tables")

for row in cursor:
        print(row[0], "\t")

connection.close_session()