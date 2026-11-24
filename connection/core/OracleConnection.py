import os
from dotenv import load_dotenv
import oracledb

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
dsn = os.getenv("DSN")

try:
    # Connect to Oracle Database
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )

    print("Successfully connected to Oracle Database!")

    # Create a cursor (similar to JDBC Statement/ResultSet)
    cursor = connection.cursor()

    # Execute embedded SQL SELECT statement
    cursor.execute("SELECT NAME, NUM FROM TESTJDBC")

    # Retrieve and display records
    print("\nNAME\tNUM")
    print("-------------------------")

    for row in cursor:
        print(row[0], "\t", row[1])

    # Close cursor and connection
    cursor.close()
    connection.close()

    print("\nDatabase connection closed.")

except oracledb.Error as error:
    print("Oracle Database Error:", error)


# NOTES:
#
# Java JDBC                         Python
# ------------------------------------------------
# DriverManager.getConnection()     oracledb.connect()
# Connection                       connection
# Statement                        cursor
# executeQuery()                   cursor.execute()
# ResultSet                        cursor (iteration)
# rs.next()                        for row in cursor
# rs.getString(1)                  row[0]
# rs.getInt(2)                     row[1]
#
# The cursor executes SQL and retrieves query results.
#
# Python-oracledb uses Thin mode by default.
# No Oracle JDBC JAR file is required.
#
# For the school database, connect to TMU VPN
# if accessing it from outside the university network.