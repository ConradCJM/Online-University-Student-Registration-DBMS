import os
from dotenv import load_dotenv
import oracledb



class Connection:
    def __init__(self):
        load_dotenv()

        self._username = os.getenv("ORACLE_USER")
        self._password = os.getenv("ORACLE_PASSWORD")
        self._dsn = os.getenv("ORACLE_DSN")

        missing = [
            name for name, value in (
                ("ORACLE_USER", self._username),
                ("ORACLE_PASSWORD", self._password),
                ("ORACLE_DSN", self._dsn),
            ) if not value
        ]
        if missing:
            raise RuntimeError(f"Missing {', '.join(missing)} in the project-root .env file.")

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

            return self.cursor, self.connection

        except oracledb.Error as error:
            raise RuntimeError("Could not connect to Oracle Database. Check your .env settings and network/VPN access.") from error

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
