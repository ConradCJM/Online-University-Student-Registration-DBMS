import os
from dotenv import load_dotenv
import oracledb



class Connection:
    def __init__(self):
        load_dotenv()

        self._username = os.getenv("USER")
        self._password = os.getenv("PASSWORD")
        self._dsn = os.getenv("DSN")

    def create_session(self):
        try:
            # Connect to Oracle Database
            connection = oracledb.connect(
                user=self._username,
                password=self._password,
                dsn=self._dsn
            )

            print("Successfully connected to Oracle Database!")

            # Create a cursor (similar to JDBC Statement/ResultSet)
            self.cursor = connection.cursor()
            self.connection = connection

            return self.cursor

        except oracledb.Error as error:
                    print("Oracle Database Error:", error)

    def close_session(self):

         # Close cursor and connection
        self.cursor.close()
        self.connection.close()

        print("\nDatabase connection closed.")


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